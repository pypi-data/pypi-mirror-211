import sys
import os
from dktoparserhtml import ParserHTML

from .db import OfficeDB


def update_hunfolding(self, not_exist_ok:bool=True)->None:
    """Mise a jour de la base de donnee

:param bool not_exist_ok: Not raise ValueError if pathjson not found

:raise ValueError: pathjson not found ({RECUPEREDB_OFFICE_JSONPATH}/officename.json or {RECUPEREDB_OFFICE_PATH}/../office/officename.json)


    Voir aussi
    ----------

    :func:`OfficeDB.get_hunfolding` : Recuperer deroule
    :func:`OfficeDB.add_hunfolding` : Ajouter deroule
    """

    not_exist_ok = True

    db = OfficeDB()

    hunfolding = db.get_hunfolding(self.calendar, self.date, self.office, self.source)

    if not hunfolding:

        dir_db = os.path.dirname(os.environ.get('RECUPEREDB_OFFICE_PATH','./datas/office.db'))
        dir_json_default =os.path.join(dir_db,'../office')
        dir_json = os.environ.get('RECUPEREDB_OFFICE_JSONPATH',dir_json_default)
        pathjson = os.path.abspath(
            os.path.join(dir_json, f"{self.office}.json")
        )

        if os.path.exists(pathjson):

            content = self.hunfolding_from_json(pathjson)

            content_html = ParserHTML(
                content,
                convertEmptyNone=True,
                convert_keys=False,
                skip_values=["cle_element", "element_defaut", "nom_office"],
            ).utf8_to_html(cleanHTML=True,)

            db.add_hunfolding(content_html)

        elif not_exist_ok:
            sys.stderr.write(f"rdb_ouh> office (fichier json) pas trouve (verifier RECUPEREDB_OFFICE_JSONPATH et RECUPEREDB_OFFICE_PATH/../office) : {pathjson}\n")
            sys.stderr.write(f"rdb_ouh> Je ne vais donc pas ajouter le deroulement ici !\n\n")
        else:
            raise ValueError(f"office (fichier json) pas trouve (verifier RECUPEREDB_OFFICE_JSONPATH et RECUPEREDB_OFFICE_PATH/../office) : {pathjson}")
        #endIf

        content = [
            {
                "cle_element":"se_signer_office",
                "texte":"<i>(Faire le signe de Croix, au nom du Père, du Fils et du Saint Esprit, pendant <b>Dieu, viens à mon aide</b>)</i>"
            },
        ]

        content_html = ParserHTML(
            content,
            convertEmptyNone=True,
            convert_keys=False,
            skip_values=["cle_element", "id_office", "reference", "id_office"],
        ).utf8_to_html(cleanHTML=True,)

        db.add_additionnal(content_html) # S'il n'y a pas les deroulements, il y a peu de chances que les additionnals existent
    #endIf

    db.close()

    return None

#endDef
