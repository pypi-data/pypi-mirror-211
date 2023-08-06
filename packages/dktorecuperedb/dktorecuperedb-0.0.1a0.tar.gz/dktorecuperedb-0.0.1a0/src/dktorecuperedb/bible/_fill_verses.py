from .db import BibleDB
from .verse import Verse

def fill_previous(self, tmp, char, previous_sep, chapter):

    def verse_interval(**kwargs):
        bible_db = BibleDB()
        return [
            Verse(chapter=ch, verse=vrs, text=txt)
            for bk, ch, vrs, txt in bible_db.get_rangeVerse(
                    book = self.book,**kwargs
            )
        ]
    #endDef


    # si on a "ch:verse-,tmp" : on terminer le chapitre ch + tmp = nouveau chapitre
    bible_db = BibleDB()
    verses = []

    if not tmp and char==self.verse_concat and len( self.references) >= 1:

        max_verse = bible_db.getMaxVerse(self.book, self.references[-1].chapter)
        self.references += verse_interval(
            start_chapter =  self.references[-1].chapter,
            end_chapter = chapter,
            start_verse =  self.references[-1].verse+1,
            end_verse = max_verse
        )
        chapter = str(int(chapter)+1)
        previous_sep = self.chapter_sep

    elif not tmp and char==self.verse_concat and len( self.references) < 1:

        print(f"{__file__} : fill_previous 2")

    elif previous_sep == self.verse_interv and len( self.references) >= 1:

        self.references += verse_interval(
            start_chapter =  self.references[-1].chapter,
            end_chapter = chapter,
            start_verse =  self.references[-1].verse+1,
            end_verse = tmp
        )

    elif previous_sep == self.verse_interv and len( self.references) < 1:

        print(f"{__file__} : fill_previous 1")

    else:

        self.references += verse_interval(
            start_chapter = chapter,
            start_verse=tmp
        )

    #endIf

    return chapter
#endDef
