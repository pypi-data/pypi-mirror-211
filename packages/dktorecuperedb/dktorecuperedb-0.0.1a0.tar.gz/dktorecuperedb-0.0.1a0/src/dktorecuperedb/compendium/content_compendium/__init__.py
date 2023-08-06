from ._collection2data import _collectionkey2data

class SubclassCompendium:
    """
    SubclassCompendium class handles the functionalities related to the Compendium module.

    Attributes:
        key (str): The key attribute.
        title (str): The title attribute.
        text (str): The text attribute.
        collection (str): The collection attribute.
        language (str): The language attribute.
        disambiguation (str): The disambiguation attribute.
        default (bool): The default attribute.
        author (str): The author attribute.
        editor (str): The editor attribute.

    :func fetch_names: Récupère la liste des variantes du sous-compendium.
    :func fetch_variantes: Récupère la liste des variantes du sous-compendium.
    :func get_prayer: Récupère le texte de la prière du sous-compendium.
    """

    def __init__(self,
                 key:str=None,  # TODO : verifier qu'a tous les appels args=val !
                 title:str=None, text:str=None, collection:str=None,
                 disambiguation:str=None, language:str=None, default:bool=None,
                 author:str=None,editor:str=None
                 ):
        """
        Initialise une instance de la classe SubclassCompendium.
        """

        self.key = key
        self.title = title
        self.text = text
        self.collection = collection
        self.language = language
        self.disambiguation = disambiguation # par exemple, dominicain ou missel
        self.default = default
        self.author = author
        self.editor = editor
        self.default = default
    #endDef

    def fetch_names(self)->list:
        """
        Récupère la liste des variantes

        :return: Liste des variantes.
        :rtype: list
        """

        return (("name1", "variante1"),("name1", "variante2"), ("name2",))
    #endDef


    def fetch_variantes(self)->list:
        """
        Récupère la liste des variantes

        :return: Liste des variantes.
        :rtype: list
        """

        return ("variante1", "variante2")
    #endDef

    def get_prayer(self)->str:
        """
        Récupère le texte de la prière du sous-compendium.

        :return: Texte de la prière.
        :rtype: str
        """

        # Appel DB
        return "<p>Ma pri&eacute;re</p>"
    #endDef

    def to_dict(self)->dict:
        """
        Convert to dict
        :return: {key, name, collection, disambiguation, language, content, author, editor}
        :rtype: dict
        """
        return {
            "key":self.key,
            "name": self.title,
            "collection": self.collection,
            "disambiguation":self.disambiguation,
            "language":self.language,
            "content": self.text,
            "author": self.author,
            "editor": self.editor,
        }
    #endDef

    from ._name_to_data import name2data, set_from_db #TODO : name2data : ajouter option "return dict" + si plusieurs, creer une liste pour chaque attribu
    from ._get_index import get_index

    @staticmethod
    def collectionkey2data(usage:str="hymne_mariale"):
        return _collectionkey2data(usage=usage)
    #endIf

#endClass
