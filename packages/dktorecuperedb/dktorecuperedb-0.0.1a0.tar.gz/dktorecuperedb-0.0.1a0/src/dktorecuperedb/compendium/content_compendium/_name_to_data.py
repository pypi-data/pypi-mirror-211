from ..db import CompendiumDB
from .sort_datas import sort_datas

def set_from_db(self, data:dict):
    """
    Initialise les attributs de l'objet à partir des données fournies.

    :param dict data: Les données au format JSP ou autre.
    """
    self.key = data.get("key", None)
    self.title = data.get("title", None)
    self.text = data.get("text", None)

    self.collection = data.get("collection", None)
    self.language = data.get("language", None)
    self.disambiguation = data.get("disambiguation", None)
    self.author = data.get("author", None)
    self.editor = data.get("editor", None)

    self.default = data.get("default", None)
#endDef

def name2data(self)->None:
    """
    Convertit le nom de l'objet en données en utilisant la base de données :ref:`CompendiumDB`.

    :descr: Met à jour les attributs suivants :
        - self.text
        - self.collection
        - self.language
        - self.disambiguation
        - self.author
        - self.editor

    :return: 0 si les données sont récupérées avec succès, 1 si les données sont vides.
    :rtype: int
    """

    c_db = CompendiumDB()

    list_keys = [
        "key", "collection",
        "title", "text",
        "disambiguation", "language",
        "author", "editor" #, "default"
    ]

    unsorted_datas = c_db.get_item_compendium(
        items=list_keys,
        key=self.key,
        collection=self.collection,
        name=self.title,
        disambiguation=self.disambiguation,
        language=self.language
    )

    if not unsorted_datas : # Empty datas
        return 1
    #endIf

    sorted_datas = sort_datas(keys=list_keys, list_of_list_values=unsorted_datas)

    hasDefaultValue=False

    for elt in sorted_datas :
        if not hasDefaultValue or (elt.get("default", None) and not self.default):
            self.set_from_db(elt)
            hasDefaultValue = True
        #endIf
    #endFor

    return 0 # all rigth
#endDef
