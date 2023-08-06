from types import LambdaType, FunctionType, MethodType, CodeType,\
    ModuleType, CellType

JSON_TYPE: str = r"<class '(\w\S+)'>_"
JSON = ('''{{
    "{type}_{id:x}": {{
    {items}
    }}
}}''')


XML_TYPE: str = r'type="(\w+)"'
XML = ('''
<object type="{type}" id="{id:x}">
{items}
</object>
''')
XML_ITEM = ('''
<item>
    <key>
        {key}
    </key>
    <value>
        {value}
    </value>
</item>
''')
XML_PRIMITIVE = '<primitive type="{type}">{obj}</primitive>'

PRIMITIVE_TYPES: tuple = (int, float, complex, str, bool, type(None))

BOOL_TYPE: dict[bool, str] = {
        None: 'null',
        True: 'true',
        False: 'false'
    }

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

