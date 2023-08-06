from ..db import CompendiumDB
from .sort_datas import sort_datas

def _collectionkey2data(usage:str)->None:
    """Retourne les collections
    """

    c_db = CompendiumDB()

    list_keys = [
        "key", "collection",
        "title",
        "disambiguation", "language",
        "author", "editor" #, "default"
    ]

    out = c_db.get_alternatives(
        items=list_keys,
        alternative_usage=usage
    )


    return out
#endDef
