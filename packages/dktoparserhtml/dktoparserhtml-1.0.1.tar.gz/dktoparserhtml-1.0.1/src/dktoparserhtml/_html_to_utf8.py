def html_to_utf8(self, data=None, recurs=False, inplace=False, **kwargs)->str:
    """Convert HTML to UTF8

:param str|list|dict data: Input datas
:param bool recurs: Use recursivity (if list, dict)
:param bool inplace: (False) Replace self.data and return None
"""

    if data is None and not recurs:
        data = self.data
    #endIf

    if not isinstance(data,str):
        return self.recurs_function(
            self.html_to_utf8,
            data=data,
            recurs=recurs,
            inplace=inplace,
            **kwargs
        )
    #endIf

    for k, v in self.characters_html_utf8.items():
        data = data.replace(k, v)
    #endFor

    if inplace:
        self.data = data
        return None
    else:
        return data
    #endIf

#endDef

