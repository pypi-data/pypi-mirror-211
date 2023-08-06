import html

from .db import BibleDB

def ref2text(self)->None:
    bible_db=BibleDB()

    chapter = -1
    content=""

    if self.references is None:
        print(f"{__file__} self.reference is none")
        self.errors += [{"book":self.book, "error:":"not in Bible"},]
        return
    #endIf

    for elt in self.references:

        if not elt.text:
            text=bible_db.get_text_oneverse(self.book, elt.chapter, elt.verse)
        else:
            text=elt.text
        #endIf

        if text is None:
            print(f"{__file__} text is none")
            self.errors += [{"book":self.book, "chapter":elt.chapter, "verse":elt.verse, "error:":"not in Bible"},]
            continue
        #endIf

        if chapter != elt.chapter:
            if chapter != -1:
                content += "<br/>\n "
            #endIf
            content += f'<span class="chapter_number">{elt.chapter}</span> '
            chapter = elt.chapter
        #endIf

        content += f' <span class="verse_number">{elt.verse}</span> {text}\n'

    #endFor

    self.text=content[:-2]  # supprimer le dernier retour a la ligne

    # print(self.text)

#endFor
