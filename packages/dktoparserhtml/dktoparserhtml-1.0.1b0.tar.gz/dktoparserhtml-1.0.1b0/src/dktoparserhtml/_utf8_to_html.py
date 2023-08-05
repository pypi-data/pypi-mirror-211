def utf8_to_html(self, convertbreaklines=False, data=None, cleanHTML=False, recurs=False, inplace=False, **kwargs)->str:
    """ Convert utf8 / html+utf8 to pure HTML
:param bool convertbreaklines: Convert \n to <br/>
:param str|list|dict data: Input datas
:param bool recurs: Use recursivity (if list, dict)
:param bool inplace: (False) Replace self.data and return None
"""

    if data is None and not recurs:
        data = self.data

    if not isinstance(data,str):
        return self.recurs_function(
            self.utf8_to_html,
            data=data,
            convertbreaklines=convertbreaklines,
            cleanHTML=cleanHTML,
            recurs=recurs,
            inplace=inplace,
            **kwargs
        )
    #endIf

    if cleanHTML:
        data = self.simplify_html(content=data, recurs=False, **kwargs)
    #endIf

    balises_html = ["<", ">", " "]

    # Replace
    for k, v in self.characters_html_utf8.items():
        if v in balises_html:
            continue
        #endIf
        data = data.replace(v, k)
    #endFor

    convertbreaklines = False
    if convertbreaklines:
        data = data.replace("\n", "<br/>")
    #endIf

    if inplace:
        self.data = data
        return None
    else:
        return data
    #endIf

    return None

#endDef
