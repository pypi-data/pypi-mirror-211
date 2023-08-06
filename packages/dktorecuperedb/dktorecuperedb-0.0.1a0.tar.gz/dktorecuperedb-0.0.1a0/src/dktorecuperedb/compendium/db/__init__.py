import os
from threading import Lock # verrou

from dktoeasysqlite3 import MyDB

class CompendiumDB(MyDB):
    def __init__(self):
        self.db_path=os.path.abspath(os.environ.get("RECUPEREDB_COMPENDIUM_PATH", "./datas/compendium.db"))

        super().__init__(lock_in=Lock())

        self.tcontent_name=os.environ.get("RECUPEREDB_COMPENDIUM_CONTENT_NAME", "content")
        self.tsequence_name=os.environ.get("RECUPEREDB_COMPENDIUM_SEQUENCE_NAME", "sequence")
        self.tcollection_name=os.environ.get("RECUPEREDB_COMPENDIUM_COLLECTION_NAME", "content_collection")

        self.to_html=True

    #endDef

    # Compendium
    from ._get_item_compendium import get_item_compendium
    from ._get_collections import get_collections

    # Sequence
    from ._get_sommaire import get_sommaire
    from ._get_sequence import get_sequence
    from ._get_sequence_index import get_sequence_index
    from ._get_alternatives import get_alternatives
#endClass
