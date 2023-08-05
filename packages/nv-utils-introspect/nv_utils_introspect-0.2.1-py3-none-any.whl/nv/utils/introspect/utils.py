from inspect import isfunction


def islambda(obj):
    return isfunction(obj) and obj.__qualname__.endswith('<lambda>')
