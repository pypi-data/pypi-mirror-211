JSON = ('''{{
    "{type}_{id:x}": {{
    {items}
    }}
}}''')
JSON_TYPE: str = r"<class '(\w\S+)'>_"

XML = ('''
<object type="{type}" id="{id:x}">
{items}
</object>
''')
XML_TYPE: str = r'type="(\w+)"'
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