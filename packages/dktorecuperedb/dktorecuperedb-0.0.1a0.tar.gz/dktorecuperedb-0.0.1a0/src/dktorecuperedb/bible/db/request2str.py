from dktoparserhtml import ParserHTML

def return_str(result:str, to_html:bool=True)->str:
    if result is None or len(result) < 1:
        return None
    elif to_html:
        parser = ParserHTML(result[0])
        html_parsed = parser.utf8_to_html(convertbreaklines=False)
        del parser
        return html_parsed
    #endIf
    return result[0]
#endIf
