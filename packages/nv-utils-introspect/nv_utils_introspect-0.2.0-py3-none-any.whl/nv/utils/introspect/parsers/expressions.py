from abc import abstractmethod
import ast
from itertools import chain
from typing import Any, TypeVar, Union, Callable, Type, Optional

from ..exceptions import SafetyException, ParsingError


__ALL__ = ['parse_expression', ]


T = TypeVar('T')

IndexType = Union[str, int, slice]
ConstantType = Union[str, int, slice, bytes, bytearray, complex, float, type(None)]


class Token:
    @property
    def parent(self):
        return None

    @abstractmethod
    def eval(self, namespace: dict[str, Any], unsafe=False):
        raise NotImplementedError

    @staticmethod
    def eval_if_token(obj: Union['Token', ConstantType], namespace: dict[str, Any], unsafe=False):
        return obj.eval(namespace, unsafe=unsafe) if isinstance(obj, Token) else obj

    def unwrap(self):
        return self

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError


class SafetyMixin:
    @abstractmethod
    def unsafe_eval(self, namespace: dict[str, Any]):
        raise NotImplementedError

    def safe_eval(self, namespace: dict[str, Any]):
        raise SafetyException(f"unable to eval {self!s}; implement safe_eval or set unsafe=True")

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        return self.unsafe_eval(namespace) if unsafe else self.safe_eval(namespace)

    def unwrap(self):
        return self


class ValueToken(Token):
    def __init__(self, value: T):
        self.value = value

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        return self.value

    def unwrap(self):
        if not isinstance(self.value, Token):
            return self.value
        else:
            return self

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value!r})"

    def __str__(self):
        return str(self.value)


class RefToken(Token):
    ref_getter: Callable[[Any, T], Any] = NotImplemented

    def __init__(self, token: Token, value: T):
        self.token = token
        self.value = value

    @property
    def parent(self):
        return self.token

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        obj = self.token.eval(namespace, unsafe=unsafe)
        return self.ref_getter(obj, self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}(token={self.token!r}, value={self.value!r})"


class ContainerToken(ValueToken):
    container_cls = NotImplemented
    fmt_str = "({content})"

    def __init__(self, value=None):
        super().__init__(value or self.container_cls())

    def __str__(self):
        content = ", ".join(str(v) for v in self.value)
        return self.fmt_str.format(content=content)

    @classmethod
    def from_iterable(cls, i):
        i = i or list()
        return cls(cls.container_cls(i))

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        return self.container_cls(self.eval_if_token(e, namespace, unsafe=unsafe) for e in self.value)

    def unwrap(self):
        if all(not isinstance(v, Token) for v in self.value):
            return self.eval({})
        else:
            return self


class UnOp:
    @abstractmethod
    def eval(self, op):
        raise NotImplementedError


# Implementations
class Expression(RefToken):
    def __init__(self, token, node: Optional[ast.Expression] = None):
        super().__init__(token, None)
        self.node = node

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        return self.token.eval(namespace, unsafe=unsafe) if self.token else None

    def __str__(self):
        return str(self.token)

    def __repr__(self):
        return f"Expression({self.token!r})"


class Call(SafetyMixin, Token):
    def __init__(self,
                 clb: Token,
                 args: list[ConstantType | Token],
                 kwargs: dict[str, ConstantType | Token],
                 ):
        self.clb = clb
        self.args = args or list()
        self.kwargs = kwargs or dict()

    @property
    def parent(self):
        return self.clb

    def __repr__(self):
        return f"{self.__class__.__name__}({self.clb!r}, args={self.args!r}, kwargs={self.kwargs!r})"

    @staticmethod
    def _format_arg(k, v) -> str:
        v = str(v) if isinstance(v, Token) else repr(v)
        return f"{k!s}={v}" if k else v

    def __str__(self):
        args = (self._format_arg(None, v) for v in self.args)
        kwargs = (self._format_arg(k, v) for k, v in self.kwargs.items())
        all_args = ", ".join(chain(args, kwargs))
        return f"{self.clb!s}({all_args})"

    def unsafe_eval(self, namespace):
        clb = self.eval_if_token(self.clb, namespace, unsafe=True)
        args = [self.eval_if_token(arg, namespace, unsafe=True) for arg in self.args]
        kwargs = {k: self.eval_if_token(v, namespace, unsafe=True) for k, v in self.kwargs.items()}
        return clb(*args, **kwargs)


class Name(ValueToken):
    def eval(self, namespace: dict[str, Any], unsafe=False):
        return namespace[self.value]

    def unwrap(self):
        return self


class Attribute(RefToken):
    ref_getter = getattr

    def __str__(self):
        return f"{self.token!s}.{self.value!s}"


class Subscript(RefToken):
    def __str__(self):
        value = self.value
        if isinstance(value, slice):
            content = Slice.format_slice(value.start, value.stop, value.step)
        elif isinstance(value, Token):
            content = str(value)
        else:
            content = repr(value)

        index = f"[{content}]" if content else ""

        return f"{self.token!s}{index}" if content else ""

    @staticmethod
    def ref_getter(obj, ref):
        return obj[ref]


class Slice(Token):
    _attrs = ('start', 'stop', 'step')

    def __init__(self,
                 start: IndexType | Token | None,
                 stop: IndexType | Token | None,
                 step: IndexType | Token | None,
                 ):
        self.start = start or 0
        self.stop = stop or None
        self.step = step or 1

    def _iter_values(self):
        yield from (getattr(self, attr) for attr in self._attrs)

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        args = [self.eval_if_token(v, namespace, unsafe=unsafe) for v in self._iter_values()]
        return slice(*args)

    def unwrap(self):
        if all(not isinstance(v, Token) for v in self._iter_values()):
            return self.eval({})
        else:
            return self

    @staticmethod
    def format_slice(start, stop, step):
        start = str(start) if start else ""
        stop = str(stop) if stop else ""
        step = str(step) if step != 1 else ""
        if step:
            return f"{start}:{stop}:{step}"
        elif start or stop:
            return f"{start}:{stop}"
        else:
            return ""

    def __str__(self):
        return self.format_slice(self.start, self.stop, self.step)

    def __repr__(self):
        return f"{self.__class__.__name__}(start={self.start!r}, stop={self.stop!r}, step={self.step!r})"


class Constant(ValueToken):
    def __str__(self):
        return repr(self.value)


class Tuple(ContainerToken):
    container_cls = tuple
    fmt_str = "({content})"


class List(ContainerToken):
    container_cls = list
    fmt_str = "[{content}]"


class Set(ContainerToken):
    container_cls = set
    fmt_str = "{{{content}}}"


class Dict(ContainerToken):
    container_cls = dict

    def unwrap(self):
        if all(not isinstance(k, Token) and not isinstance(v, Token) for k, v in self.value.items()):
            return self.eval({})
        else:
            return self

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        return {
            self.eval_if_token(k, namespace, unsafe=unsafe): self.eval_if_token(v, namespace, unsafe=unsafe)
            for k, v in self.value.items()
        }

    @staticmethod
    def _format_item(k, v):
        return f"{str(k) if isinstance(k, Token) else repr(k)}: {str(v) if isinstance(v, Token) else repr(v)}"

    def __str__(self):
        items = (self._format_item(k, v) for k, v in self.value.items())
        content = ", ".join(items)
        return f"{{{content}}}"


class UnaryOp(Token):
    def __init__(self, unop_name: str, operand: ConstantType | Token):
        self.un_op = self.get_operator(unop_name)
        self.operand = operand

    def unwrap(self):
        if not isinstance(self.operand, Token):
            return self.un_op.eval(self.operand)
        return self

    def eval(self, namespace: dict[str, Any], unsafe=False):
        # print(f"{self.__class__.__name__} evaluating {self!s}")
        operand = self.eval_if_token(self.operand, namespace, unsafe=unsafe)
        return self.un_op.eval(operand)

    def __str__(self):
        return f"{self.un_op!s}{self.operand!s}"

    @classmethod
    def get_operator(cls, name):
        operator = getattr(cls, name, None)
        if operator is None:
            raise ParsingError(f"unary operator not implemented: {name}")
        return operator

    class UAdd(UnOp):
        @classmethod
        def eval(cls, op):
            return +op

        def __str__(self):
            return "+"

    class USub(UnOp):
        @classmethod
        def eval(cls, op):
            return -op

        def __str__(self):
            return "-"


class ASTParser:

    def __init__(self, unwrap=True):
        self._unwrap = unwrap

    def unwrap(self, token: Token):
        return token.unwrap() if self._unwrap else token

    def parse(self, s: str):
        entry_node = ast.parse(s, mode='eval')
        return self.parse_node(entry_node)

    def parse_node(self, node):
        type_name = node.__class__.__name__
        parser = getattr(self, f"parse_{type_name.lower()}", None)

        if parser is None:
            raise ParsingError(f"no parsing available for {type_name}: {ast.unparse(node)}")

        token = parser(node)
        return self.unwrap(token)

    # Object parsers named 'parser_{ast_type}'
    def parse_expression(self, node: ast.Expression):
        return Expression(self.parse_node(node.body), node=node)

    def parse_name(self, node: ast.Name):
        return Name(node.id)

    def parse_call(self, node: ast.Call):
        return Call(
            clb=self.parse_node(node.func),
            args=[self.parse_node(e) for e in node.args],
            kwargs={k.arg: self.parse_node(k.value).unwrap() for k in node.keywords},
        )

    def parse_attribute(self, node: ast.Attribute):
        return Attribute(token=self.parse_node(node.value), value=node.attr)

    def parse_subscript(self, node: ast.Subscript):
        return Subscript(token=self.parse_node(node.value), value=self.parse_node(node.slice))

    def parse_slice(self, node):
        attrs = ('lower', 'upper', 'step')
        values = (getattr(node, attr) for attr in attrs)
        args = [self.parse_node(n) for n in values]
        return Slice(*args)

    def parse_tuple(self, node: ast.Tuple):
        return self._parse_into_container(node, Tuple)

    def parse_list(self, node: ast.List):
        return self._parse_into_container(node, List)

    def parse_set(self, node: ast.Set):
        return self._parse_into_container(node, Set)

    def _parse_into_container(self, node, token_type: Type[ContainerToken]):
        return token_type.from_iterable(self.parse_node(i) for i in node.elts)

    def parse_dict(self, node: ast.Dict):
        keys = (self.parse_node(k) for k in node.keys)
        values = (self.parse_node(v) for v in node.values)
        return Dict(dict(zip(keys, values)))

    def parse_constant(self, node):
        return Constant(node.value)

    def parse_unaryop(self, node: ast.UnaryOp):
        unop_name = node.op.__class__.__name__
        operand = self.parse_node(node.operand)
        return UnaryOp(unop_name, operand)


def parse_ast(s: str):
    return ast.parse(s, mode='eval')


def dump_ast(s: str):
    tree = parse_ast(s)
    print(ast.dump(tree, indent=4))


parse_expression = ASTParser(unwrap=True).parse
