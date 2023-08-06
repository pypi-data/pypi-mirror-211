from .verse import Verse
from .db import BibleDB

def parse_ref(self,content:str)->None:

    global previous_sep
    global chapter
    tmp = ""
    chapter=None
    previous_sep = None
    listRefs = []

    bible_db = BibleDB()

    self.book_title = bible_db.get_biblebook(self.book)

    if self.book_title is None:
        print(f"{__file__}  : book {self.book} not found in db")
        return None
    #endIf

    # TODO : arreter les range, et faire des appels a la BDD avec BETWEEN !


    if not self.chapter_sep in content or content[-len(self.chapter_sep)] == self.chapter_sep:

        content = content.replace(self.chapter_sep,"")

        min_verse = bible_db.getMinVerse(self.book, content)
        max_verse = bible_db.getMaxVerse(self.book, content)

        self.references = [
            Verse(chapter=ch, verse=vrs, text=txt)
            for bk, ch, vrs, txt in bible_db.get_rangeVerse(
                    book = self.book,
                    start_chapter = content,
                    start_verse = min_verse,
                    end_verse = max_verse
            )
        ]

        return
    #endIf

    for char in content:

        if char==self.chapter_sep:

            #previous_sep = self.chapter_sep
            chapter = tmp
            tmp = ""

        elif char==self.verse_interv: # "-"

            self.fill_previous(tmp, char, previous_sep, chapter)
            previous_sep = self.verse_interv
            tmp = ""

        elif char==self.verse_concat: # ","

            chapter = self.fill_previous(tmp, char, previous_sep, chapter)
            previous_sep = self.verse_concat
            tmp = ""

        else:

            tmp += char

        #endIf

    #endFor

    if content[-(len(self.verse_interv))] == self.verse_interv:

        max_verse = bible_db.getMaxVerse(self.book, self.references[-1].chapter)

        self.references += [
            Verse(chapter=ch, verse=vrs, text=txt)
            for bk, ch, vrs, txt in bible_db.get_rangeVerse(
                    book = self.book,
                    start_chapter = listRefs[-1].chapter,
                    start_verse = listRefs[-1].verse+1,
                    end_verse = max_verse
            )
        ]

    elif content[-(len(self.verse_concat))] == self.verse_concat:

        pass

    else:

        self.fill_previous(tmp, "", previous_sep, chapter)

    #endIf

    # print( [ e.to_dict() for e in self.references] )

#endDef
