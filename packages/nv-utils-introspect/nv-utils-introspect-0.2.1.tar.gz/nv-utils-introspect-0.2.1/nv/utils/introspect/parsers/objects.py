from inspect import ismodule, isclass, isfunction, ismethod, ismethoddescriptor, isdatadescriptor, getmodule
from typing import Tuple, Any

from ..exceptions import ParsingError
from ..tracer import search_object
from ..types import UNSET
from ..utils import islambda


__ALL__ = ['parse_object', 'split_full_qualname']


DEFAULT_MODULE_DELIMITER = ":"


def get_method_qualname(obj, definition_scope=None):
    definition_scope = definition_scope or obj.__self__
    found_instance = search_object(definition_scope)
    found_method = search_object(obj, namespaces=definition_scope, max_level=0)

    if not found_instance or not found_method:
        raise ParsingError(f"unable to determine a reference for {obj!r}")

    instance_path = found_instance.path
    module = found_instance.first_namespace
    method_path = found_method.path

    method_path = (*instance_path, *method_path)
    method_name = ".".join(method_path)

    return module.__name__, {method_name}


def search_qualname(obj, *namespaces):
    namespaces = namespaces or None
    finding = search_object(obj, namespaces=namespaces)
    module = getmodule(finding.namespace)
    qualname = ".".join(finding.path)

    return module.__name__, qualname


def get_scope_qualname(self, obj):
    definition_scope = getmodule(obj)
    return self.search_qualname(obj, definition_scope)


def get_attr_qualname(obj):
    name = getattr(obj, '__qualname__', getattr(obj, '__name__', None))
    if not name:
        raise ParsingError(f'unable to determine object name from: {obj!r}')
    return name


def get_module_name(obj):
    module_name = getattr(obj, '__module__', None)
    if not module_name:
        raise ParsingError(f'unable to determine object name from: {obj!r}')
    return module_name


class ObjectParser:

    PARSER_RULES = (
        (ismodule, None, lambda obj: obj.__name__),
        (isclass, get_attr_qualname, get_module_name),
        (islambda, get_scope_qualname, ),
        (isfunction, get_attr_qualname, get_module_name),  # This also covers simple methods
        (ismethoddescriptor, get_attr_qualname, get_module_name),  # class and static methods
        (isdatadescriptor, search_qualname,),
        (ismethod, get_method_qualname, ),
        (lambda _: True, search_qualname, ),
    )

    def __init__(self, module_delimiter=None):
        self.module_delimiter = module_delimiter or DEFAULT_MODULE_DELIMITER

    def get_name_components(self, obj):
        parsers = next((parsers for check, *parsers in self.PARSER_RULES if check(obj)), UNSET)

        if parsers is UNSET:
            raise ParsingError(f'unable to determine parser for {obj!r}')

        name_parser, *module_parsers = parsers

        parsed_name = name_parser(obj) if name_parser is not None else None

        if not module_parsers:
            module_name, object_name = parsed_name
        else:
            module_parser = module_parsers.pop()
            module_name = module_parser(obj)
            object_name = parsed_name

        return module_name, object_name

    def get_full_qualname(self, obj):
        parsers = next((parsers for check, *parsers in self.PARSER_RULES if check(obj)), None)

        if parsers is None:
            raise ParsingError(f'unable to determine parser for {obj!r}')

        name_parser, *module_parsers = parsers
        name = name_parser(obj)

        if not module_parsers:
            return name

        module_parser = module_parsers.pop()
        module_name = module_parser(obj)
        return f"{module_name}{self.module_delimiter}{name}" if module_name else name

    def split_full_qualname(self, full_qualname) -> Tuple[str, str]:
        module, delimiter, qualname = full_qualname.partition(self.module_delimiter)
        return (module, qualname) if delimiter else ('', full_qualname)

    def render_name(self, module_name, qualname):
        return f"{module_name}{self.module_delimiter}{qualname}"


__object_parser = ObjectParser(module_delimiter=DEFAULT_MODULE_DELIMITER)
parse_object = __object_parser.get_full_qualname
split_full_qualname = __object_parser.split_full_qualname
