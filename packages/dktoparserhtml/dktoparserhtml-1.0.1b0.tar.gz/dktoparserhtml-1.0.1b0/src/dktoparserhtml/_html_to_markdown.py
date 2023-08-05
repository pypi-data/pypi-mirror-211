def html_to_markdown(self, displayMarkdown=False, data=None, recurs=False, inplace=False, **kwargs)->str:
    """Convert HTML to Markdown

:param bool displayMarkdown: Add backslash to display the markdown content
:param str|list|dict data: Input datas
:param bool recurs: Use recursivity (if list, dict)
:param bool inplace: (False) Replace self.data and return None
"""
    if data is None and not recurs:
        data = self.data
    #endIf

    if not isinstance(data,str):
        return self.recurs_function(
            self.html_to_markdown,
            data=data,
            recurs=recurs,
            displayMarkdown=displayMarkdown,
            inplace=inplace,
            **kwargs
        )
    #endIf

    escaped_markdown = ["&star;", "&lowbar;"]  # Necessite echappement

    for k, v in self.characters_html_utf8.items():
        if k in escaped_markdown:
            data = data.replace(k, f"\{v}")
        else:
            data = data.replace(k, v)
        #endIf
    #endFor


    if(displayMarkdown):
        balises_html_to_markdown = {
            "&gt;":"\>",
            "&lt;":"<",
            "&star;":"\\\\\*",
            "&plus;":"+",
            "&lowbar;":"\\\\\_",
            "_":"\_",
            "*":"\*"
        }
    else:
        balises_html_to_markdown={
            "&gt;":">",
            "&lt;":"<"
        }
    #endIf

    for k, v in self.balises_html_markdown.items():
        data = data.replace(k,v)
    #endFor

    if inplace:
        self.data = data
        return None
    else:
        return data
    #endIf

#endDef
