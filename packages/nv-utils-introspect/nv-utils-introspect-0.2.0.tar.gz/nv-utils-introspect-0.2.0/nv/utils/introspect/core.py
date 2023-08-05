from collections.abc import Iterator
from functools import cached_property
from importlib import import_module
from typing import Optional, Any

from .parsers.objects import ObjectParser, DEFAULT_MODULE_DELIMITER
from .parsers.expressions import parse_expression, Expression, Token
from .types import UNSET


__ALL__ = ['DottedPath', 'get_attr', 'get_attr_parent']


class DottedPath:

    _object_parser = ObjectParser(module_delimiter=DEFAULT_MODULE_DELIMITER)

    def __init__(self, namespace: [str | Any], expression: str | Expression | None = None):
        if not isinstance(namespace, str):
            namespace, name = self._object_parser.get_name_components(namespace)
            if name:
                expression = f"{name}.{expression!s}" if expression else name
                expression = parse_expression(expression)

        self._namespace = namespace
        self._expression = parse_expression(expression) if isinstance(expression, str) else expression

    @classmethod
    def from_str(cls, s: str) -> 'DottedPath':
        namespace, expression = cls._object_parser.split_full_qualname(s)
        return cls(namespace=namespace, expression=expression)

    @classmethod
    def from_obj(cls, obj: Any) -> 'DottedPath':
        namespace, expression = cls._object_parser.get_name_components(obj)
        return cls(namespace=namespace, expression=expression)

    @property
    def expression(self) -> Expression | None:
        return self._expression

    @property
    def token(self) -> Token | None:
        return self._expression.token if self._expression else None

    @cached_property
    def path(self) -> Optional[str]:
        return str(self._expression) if self._expression else None

    @cached_property
    def full_path(self) -> Optional[str]:
        return self._object_parser.render_name(self._namespace, self.path or '')

    @property
    def namespace(self) -> str:
        return self._namespace

    @cached_property
    def parent(self) -> Optional['DottedPath']:
        if not self._expression:
            return None

        parent_token = self.token.parent

        return DottedPath(self.namespace, Expression(parent_token)) if parent_token else DottedPath(self.namespace, None)

    def __str__(self):
        return self.full_path

    def __repr__(self):
        expression = str(self._expression) if self._expression else self._expression
        return f'{self.__class__.__name__}({self._namespace}, {expression!r})'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (other is self) or hash(other) == hash(self)
        return NotImplemented

    def iter_parents(self) -> Iterator['DottedPath']:
        parent = self.parent
        if parent:
            yield parent
            yield from parent.iter_parents()

    def iter_defaults(self) -> Iterator['DottedPath']:
        yield from self.iter_parents()

    def unsafe_build(self, package=None):
        module = import_module(self.namespace, package=package)
        return self.expression.eval(module.__dict__, unsafe=True)

    def build_from_namespace(self, namespace):
        return self.expression.eval(namespace.__dict__)


def get_attr(obj: Any, expression: str | Expression, default: Any = UNSET, unsafe: bool = False):
    try:
        expression = parse_expression(expression) if isinstance(expression, str) else expression
        return expression.eval(obj.__dict__, unsafe=unsafe)
    except (AttributeError, KeyError) as e:
        if default is UNSET:
            raise AttributeError(f"{expression!s}") from e


def get_attr_parent(obj: Any, expression: str | Expression, default: Any = UNSET, unsafe: bool = False):
    if not expression:
        return None

    try:
        expression = parse_expression(expression) if isinstance(expression, str) else expression
        parent = expression.token.parent
        return (parent.eval(obj.__dict__, unsafe=unsafe), expression.token) if parent else (obj, expression.token)
    except (AttributeError, KeyError) as e:
        if default is UNSET:
            raise AttributeError(f"{expression!s}") from e
