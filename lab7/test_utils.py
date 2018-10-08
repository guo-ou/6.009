import ast
import lab

from collections import OrderedDict

_unprep_funcs = {
    'OrderedDict': OrderedDict,
    'frozenset': frozenset,
    'set': set,
}
for i in ('Add', 'Sub', 'Mul', 'Div', 'Var', 'Num'):
    _a = getattr(lab, i, None)
    if _a is not None:
        _unprep_funcs[i] = _a

def safe_eval(node_or_string):
    if isinstance(node_or_string, str):
        node_or_string = ast.parse(node_or_string, mode='eval')
    if isinstance(node_or_string, ast.Expression):
        node_or_string = node_or_string.body
    def _convert(node):
        if isinstance(node, (ast.Str, ast.Bytes)):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, ast.List):
            return list(map(_convert, node.elts))
        elif isinstance(node, ast.Set):
            return set(map(_convert, node.elts))
        elif isinstance(node, ast.Dict):
            return dict((_convert(k), _convert(v)) for k, v
                        in zip(node.keys, node.values))
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif isinstance(node, ast.UnaryOp) and \
             isinstance(node.op, (ast.UAdd, ast.USub)) and \
             isinstance(node.operand, (ast.Num, ast.UnaryOp, ast.BinOp)):
            operand = _convert(node.operand)
            if isinstance(node.op, ast.UAdd):
                return + operand
            else:
                return - operand
        elif isinstance(node, ast.BinOp) and \
             isinstance(node.op, (ast.Add, ast.Sub)) and \
             isinstance(node.right, (ast.Num, ast.UnaryOp, ast.BinOp)) and \
             isinstance(node.left, (ast.Num, ast.UnaryOp, ast.BinOp)):
            left = _convert(node.left)
            right = _convert(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            else:
                return left - right
        elif isinstance(node, ast.Call) and \
             isinstance(node.func, ast.Name) and \
             node.func.id in _unprep_funcs:
            return _unprep_funcs[node.func.id](*(_convert(i) for i in node.args))
        elif isinstance(node, ast.Call) and \
             isinstance(node.func, ast.Attribute) and \
             node.func.attr in _unprep_funcs:
            return _unprep_funcs[node.func.attr](*(_convert(i) for i in node.args))
        raise ValueError('malformed node or string: ' + repr(node))
    return _convert(node_or_string)
