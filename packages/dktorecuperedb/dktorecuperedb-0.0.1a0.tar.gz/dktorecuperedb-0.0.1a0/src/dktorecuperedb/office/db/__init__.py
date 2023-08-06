import os
from threading import Lock # verrou

from dktoeasysqlite3 import MyDB

class OfficeDB(MyDB):
    def __init__(self):
        self.db_path=os.path.abspath(os.environ.get("RECUPEREDB_OFFICE_PATH", "./datas/office.db"))

        self.db_tinfo_name=os.environ.get("RECUPEREDB_OFFICE_INFO_NAME", "office_info")
        self.db_telement_name=os.environ.get("RECUPEREDB_OFFICE_ELEMENT_NAME", "office_element")
        self.db_thunfolding_name=os.environ.get("RECUPEREDB_OFFICE_HUNFOLDING_NAME", "office_deroule")
        self.db_tadditionnal_name=os.environ.get("RECUPEREDB_OFFICE_ADDITIONNAL_NAME", "office_addition")


        db_cols={self.db_tinfo_name:{
                "id_office":"TEXT",
                "source":"TEXT",
                "date_requete":"TEXT",
                "zone":"TEXT",
                "calendrier":"TEXT",
                "date":"TEXT",
                "nom":"TEXT",
                "couleur":"TEXT",
                "annee":"TEXT",
                "temps_liturgique":"TEXT",
                "semaine":"TEXT",
                "jour":"TEXT",
                "jour_liturgique_nom":"TEXT",
                "fete":"TEXT",
                "degre":"TEXT",
                "ligne1":"TEXT",
                "ligne2":"TEXT",
                "ligne3":"TEXT",
                "couleur2":"TEXT",
                "couleur3":"TEXT"
        }}

        db_cols[self.db_telement_name]={
                "id_element":"TEXT",
                "id_office":"TEXT",
                "nom_office":"TEXT",
                "cle_element":"TEXT",
                "titre":"TEXT",
                "texte":"TEXT",
                "editeur":"TEXT",
                "auteur":"TEXT",
                "reference":"TEXT"
            }
        db_cols[self.db_thunfolding_name]={
                "id_deroule":"INTEGER",
                "nom_office":"TEXT",
                "id_deroule":"INTEGER",
                "cle_element":"TEXT",
                "titre_particulier":"TEXT",
                "ajouter_doxologie":"LOGICAL",
                "element_defaut":"TEXT"
        }

        db_cols[self.db_tadditionnal_name] = db_cols[self.db_telement_name]

        super().__init__(lock_in=Lock(), createIfNotExists=db_cols)

        self.to_html=True

    #endDef

    #
    # from ._get_office import get_office
    # get_office(nom, date, calendrier)
    # - aller chercher la cle dans aelf_info a partir de nom, date, calendrier
    # - si n'existe pas : REQUETE à AELF pour remplir aelf_data + aelf_info
    # return : dico complet avec elements office + infos (donc retourne tout ce qu'AELF donne)

    # from ._get_office import get_office_keys
    # get_office_keys(nom, date, calendrier)
    # return : clé des éléments [introduction, hymne, antienne 1, psaume 1, ...] qui ne sont pas vides !
    # return : None si tous sont vides

    # from ._get_info import get_info
    # get_info(date, calendrier)
    # si necessaire : REQUETE à AELF
    # return les infos comme sur AELF

    from ._add_additionnal import add_additionnal
    from ._add_elements import add_elements
    from ._add_hunfolding import add_hunfolding
    from ._add_office import add_office

    from ._delete_old_items import delete_old_items

    from ._get_elements import get_elements
    from ._get_hunfolding import get_hunfolding
    from ._get_infos import get_infos

#endClass
