from collections import deque
from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from functools import partial
from inspect import ismodule, isclass, getmodule
from operator import itemgetter
from typing import Any
import sys

from .exceptions import TracingError
from .types import UNSET


main_module = sys.modules['__main__']


@dataclass(eq=True, frozen=True)
class TraceFinding:
    path: list[str]
    namespace: Any
    first_namespace: Any


# Object comparisons
def compare_is(a, b):
    return a is b


def compare_eq(a, b):
    return a == b


def compare_attr(a, b, attr, compare=compare_is):
    return compare(getattr(a, attr), getattr(b, attr))


# Namespace visiting clauses
def visit_classes(obj):
    return isclass(obj)


def visit_modules(obj):
    return ismodule(obj)


def visit_classes_and_modules(obj):
    return isclass(obj) or ismodule(obj)


def visit_custom_instances(obj):
    return hasattr(obj, '__class__') and type(obj.__class__) is type


def ignore_builtins(obj):
    return hasattr(obj, '__class__') and type(obj.__class__) is type and obj.__class__.__module__ != 'builtins'


def visit_if_all(*visit_clauses):
    def _visit(obj):
        return all(visit_clause(obj) for visit_clause in visit_clauses)
    return _visit


def visit_if_any(*visit_clauses):
    def _visit(obj):
        return any(visit_clause(obj) for visit_clause in visit_clauses)
    return _visit


# Ranking heuristics
def rank_by_proximity(finding: TraceFinding):
    return len(finding.path)


def rank_by_namespace(finding: TraceFinding, namespaces):
    namespaces = [*namespaces, finding.namespace]
    return namespaces.index(finding.namespace)


def rank_by_publicity(finding: TraceFinding):
    return sum(p for p in finding.path if p.startswith('_') and not (p.startswith('__') and p.endswith('__')))


def rank_finding(finding: TraceFinding, rankings):
    return tuple(rank(finding) for rank in rankings)


def rank_results(findings: Iterable[TraceFinding]):
    return [finding for _, finding in sorted(findings, key=itemgetter(0))]


def trace_object(
        obj,
        namespace,
        max_level:  int | None = None,
        comparisons=(compare_is, compare_eq),
        visit_clause=visit_if_any(visit_modules, visit_classes, ignore_builtins),
        rankings=None,
        debug=False,
        visited_namespaces=None,
        ):

    comparisons = comparisons if isinstance(comparisons, (tuple, list)) else (comparisons,)
    visit_clause = None if max_level == 0 else visit_clause

    # States
    stack = deque()
    visited_namespaces = visited_namespaces or set()

    # Kick-off
    stack.append((namespace, (), 0))

    while stack:
        cur_namespace, cur_path, cur_level = stack.popleft()

        if debug:
            print(" " * cur_level, f"namespace: {cur_namespace!r}")

        # Do not try to visit the same object twice
        if isinstance(cur_namespace, Hashable) and cur_namespace in visited_namespaces:
            continue

        for cur_name in dir(cur_namespace):

            try:
                cur_obj = getattr(cur_namespace, cur_name, UNSET)
            except Exception:
                if debug:
                    print("Error")
                continue

            if debug:
                print(" " * cur_level, f"- {cur_name!s:20} {type(obj)!r:40}: ", end="")

            if cur_obj is UNSET:
                if debug:
                    print("Skipping")
                continue

            if any(compare(cur_obj, obj) for compare in comparisons):
                finding = TraceFinding(path=(*cur_path, cur_name), namespace=cur_namespace, first_namespace=namespace)
                if rankings:
                    yield rank_finding(finding, rankings), finding
                else:
                    yield finding

            if debug:
                print("False")

            if (max_level is None) or (max_level and cur_level < max_level):
                if visit_clause and visit_clause(cur_obj):
                    if debug:
                        print(" " * cur_level, f"** stacking: {cur_obj} @ {cur_level}")
                    stack.append((cur_obj, (*cur_path, cur_name), cur_level + 1))

        if isinstance(cur_namespace, Hashable):
            visited_namespaces.add(cur_namespace)


def search_object(obj, namespaces=None, rankings=None, all_findings=True, include_ranking=False, default=UNSET, **kwargs):
    namespaces = namespaces or (getmodule(obj), main_module, )
    namespaces = namespaces if isinstance(namespaces, (tuple, list)) else (namespaces, )

    if rankings is None:
        rankings = (
            partial(rank_by_namespace, namespaces=namespaces),
            rank_by_proximity,
            rank_by_publicity,
        )

    visited_namespaces = set()
    tracer = partial(trace_object, obj, rankings=rankings, visited_namespaces=visited_namespaces, **kwargs)

    findings = list()
    for namespace in namespaces:
        for finding in tracer(namespace=namespace):
            findings.append(finding)

    # Sort by ranking tuples
    findings.sort(key=itemgetter(0))

    if not include_ranking:
        findings = [f for _, f in findings]

    if findings:
        return findings[0] if all_findings else findings
    else:
        if default in UNSET:
            raise TracingError(f"unable to find any reference for {obj!r}")
        return [default, ] if all_findings else default
