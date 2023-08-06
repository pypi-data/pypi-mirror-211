from types import LambdaType, FunctionType, MethodType, \
    CodeType, ModuleType, CellType, GeneratorType

BOOL_TYPES = {True: "true", False: "false", None: "null"}
PRIMITIVES: tuple = (int, float, complex, str, bool, type(None))

TYPE_MAPPING = {
    'int': int,
    'float': float,
    'complex': complex,
    'str': str,
    'bool': bool,
    'NoneType': type(None),
    'bytes': bytes,
    'list': list,
    'tuple': tuple,
    'set': set,
    'dict': dict,
    'code': CodeType,
    'cell': CellType,
    'function': FunctionType,
    'lambda': LambdaType,
    'method': MethodType,
    'staticmethod': staticmethod,
    'classmethod': classmethod,
    'type': type,
    'module': ModuleType,
    'object': object,
    'property': property,
    'generator': GeneratorType
}

IGNORED_FIELDS: set[str] = {
        '__weakref__',
        '__subclasshook__',
        '__dict__',
        '__doc__'
}
IGNORED_FIELD_TYPES: set[str] = {
    'BuiltinFunctionType', 'BuiltinMethodType',
    'WrapperDescriptorType', 'MethodDescriptorType',
    'MappingProxyType', 'GetSetDescriptorType',
    'MemberDescriptorType'
}