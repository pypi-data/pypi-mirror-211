from ..db import CompendiumDB
from ..content_compendium import SubclassCompendium

class elementSequence(SubclassCompendium):
    def __init__(self,
                 title:str=None, text:str=None, collection:str=None,
                 disambiguation:str=None, language:str=None,
                 author:str=None,editor:str=None,
                 same_page:bool=False, gloria_patri:bool=False,
                 id_key:int=0, key_name:str=None):
        super().__init__(title=title, text=text, collection=collection,
                         disambiguation=disambiguation, language=language,
                         author=author,editor=editor)
        self.same_page=same_page
        self.gloria_patri=gloria_patri
        self.id_key=id_key
        self.key_name=key_name
    #endDef
#endClass



class SubclassSequence:
    def __init__(self, sequence_name:str=None, sommaire:dict={}, contents:dict={}):
        self.sequence_name = sequence_name
        self.sommaire = sommaire
        self.contents = contents # {key : elementSequence()}
    #endDef

    def _get_index(self):
        return True

    def get_sommaire(self):

        if self.sequence_name is None:
            return {}
        #endIf

        s_db = CompendiumDB()
        unsorted_datas = s_db.get_sommaire(self.sequence_name) # la, je l'ai deja triee par id<
        #elt = [id_key, key_name, name,  gloria_patri, same_page]

        self.sommaire = [
                elementSequence(
                    id_key = elt[0],
                    key_name = elt[1],
                    title = elt[2],
                    gloria_patri = elt[3],
                    same_page=elt[4]
                ) for elt in unsorted_datas
        ]

        return {
            elt.id_key:{
                "key":elt.key_name,
                "name":elt.title,
                "gloria_patri":elt.gloria_patri,
                "same_page":elt.same_page
            }
            for elt in self.sommaire
        }

    #endDef


    def get_sequence(self):

        if self.sequence_name is None:
            return {}
        #endIf

        s_db = CompendiumDB()
        unsorted_datas = s_db.get_sequence(self.sequence_name) # la, je l'ai deja triee par id<
        #elt = [id_key, key_name, name,  gloria_patri, same_page]

        self.sommaire = [
                elementSequence(
                    id_key = elt[0],
                    key_name = elt[1],
                    title = elt[2],
                    gloria_patri = elt[3],
                    same_page=elt[4],
                    #title_content=elt[5],
                    text=elt[6],
                    disambiguation=elt[7],
                    language=elt[8],
                    author=elt[9],
                    editor=elt[10]
                ) for elt in unsorted_datas
        ]

        return {
            elt.id_key:{
                "key":elt.key_name,
                "name":elt.title,
                "gloria_patri":elt.gloria_patri,
                "same_page":elt.same_page,
                "text":elt.text,
                "disambiguation":elt.disambiguation,
                "language":elt.language,
                "author":elt.author,
                "editor":elt.editor
            }
            for elt in self.sommaire
        }


    #endDef

#endClass
