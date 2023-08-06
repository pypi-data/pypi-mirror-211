from .db import OfficeDB
from ..compendium import Compendium

from dktoparserhtml import ParserHTML

def get_alternatives(self):


    db = OfficeDB()

    self.update_db()
    infos = db.get_infos(self.calendar, self.date, self.office, self.source)
    datas = db.get_hunfolding(self.calendar, self.date, self.office, self.source, name_elements=True)
    db.close()


    out = {}

    additionnals = Compendium().collectionkey2data([e["cle_element"] for e in datas])
    content = {}

    if additionnals :

        for e in additionnals:

            if not e["usage"] in content.keys():
                content[e["usage"]] = []
            #endIf

            content[e["usage"]]+=[
                {
                    "titre": e["title"],
                    "editeur": e["editor"],
                    "auteur": e["author"],
                    "reference": e["collection"],
                    "disambiguation":e["disambiguation"],
                    "langue":e["language"],
                    "key":e["key"]
                }
            ]

        #endFor

        rglo = range(len(datas))

        for i in rglo:  # Add additionnal values to the alternatives
            if datas[i]["cle_element"] in content.keys() and content[datas[i]["cle_element"]] :

                # Il y a t il deja des alternatives de prevu ?
                if "alternative" in datas[i].keys():
                    datas[i]["alternative"] += content[datas[i]["cle_element"]]
                else:
                    datas[i]["alternative"] = content[datas[i]["cle_element"]]
                #endIf

            #endIf

        #endFor

    #endIf

    infos_parser = ParserHTML(
        infos,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=["date", "date_requete", "id_office"],
    )
    infos_parser.utf8_to_html(inplace=True)

    datas_parser = ParserHTML(
        datas,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]
    )

    datas_parser.utf8_to_html(inplace=True)

    if self.format_output == "html" :

        out = {
            "informations":infos_parser.html_to_utf8(),
            self.office:datas_parser.html_to_utf8()
        }

    elif self.format_output == "markdown" :

        out = {
            "informations":infos_parser.html_to_markdown(),
            self.office:datas_parser.html_to_markdown()
        }

    #endIf

    # Nettoyer :
    # Post traitement : si l'alternative correspond au titre
    rglo = range(len(out[self.office]))

    for i in rglo:
        d = out[self.office][i]
        if "alternative" in d.keys():

            keys_first_alt = d["alternative"][0].keys()

            for j in range(len(d["alternative"])-1, 0, -1):

                # size-1, car on decroit, et que le 1er element est inclus et pas le dernier, mais on ne regarde pas la valeur 0 si elle vient d'aelf
                if d["alternative"][0]["titre"] == d["alternative"][j]["titre"]:

                    for k, v in d["alternative"][j].items():

                        if not k in keys_first_alt:
                            out[self.office][i]["alternative"][0][k] = v
                        #endIf

                    #endFor

                    del out[self.office][i]["alternative"][j]
                #endIf
            #endFor
        #endIf
    #endFor

    return out
#endDef
