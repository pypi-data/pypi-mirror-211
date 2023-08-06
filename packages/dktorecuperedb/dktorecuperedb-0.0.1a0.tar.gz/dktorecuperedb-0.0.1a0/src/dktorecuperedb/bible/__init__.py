class Bible():
    def __init__(self, book=None, ref=None):
        self.chapter_sep=":"
        self.verse_interv="-"
        self.verse_concat=","

        self.book=book
        self.book_title=None
        self.chapters_title=[]
        self.references=[]

        self.parse_ref(ref) #TODO : try statement here

        self.text=""
        self.errors=[]

        #
        # references :
        #
        # ch1:v1-v10    (intervale)
        # >> out ....   list(Verse(ch1,v1), Verse(ch1,v2), Verse(ch1, v3), ..., Verse(ch,v10))
        # ch:v-ch:v    ... idem
        # ch:v,v    (concat versets) ... idem
        # ch1:v1,v5-ch2:v2,ch2:v7
        # >> out ....   list(Verse(ch1,v1), Verse(ch1,v5), Verse(ch1, v6), ..., Verse(ch1,vfin), Verse(ch2,v1), Verse(ch2,v2),Verse(ch2,v7))
        #
        #
    #endDef

    from ._parse_ref import parse_ref
    from ._reference_to_text import ref2text
    from ._fill_verses import fill_previous

#endClass

class BibleOneYear:
    def __init__(self):
        True
    #endDef

    from ._on_a_year import on_a_year
