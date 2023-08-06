class Verse():
    def __init__(self, chapter:str=None, verse:str=None, text:str=None):
        try:
            self.chapter=int(chapter)
        except TypeError:
            self.chapter=chapter
        #endTry

        try:
            self.verse=int(verse)
        except TypeError:
            self.verse=verse
        #endTry

        self.text=text
    #endDef

    def to_dict(self):
        return {"chapter":self.chapter, "verse":self.verse, "text":self.text}
    #endDef

#endClass
