_this_file_="html._removeDuplicates.py"

import traceback
from bs4 import BeautifulSoup, Tag
from sys import stderr as sys_stderr

def _removeDuplicates(content, tag="br"):
    try:
        soup = BeautifulSoup(content)
    except Exception as e:
        sys_stderr.write(f"{_this_file_} (1)\n")
        traceback.print_exc()
        raise Exception
    #endTry
    for br in soup.find_all(tag):
        while isinstance(br.next_sibling, Tag) and br.next_sibling.name == tag:
            br.next_sibling.extract()
        #endWhile
    #endFor
    return str(soup)
#endDef
