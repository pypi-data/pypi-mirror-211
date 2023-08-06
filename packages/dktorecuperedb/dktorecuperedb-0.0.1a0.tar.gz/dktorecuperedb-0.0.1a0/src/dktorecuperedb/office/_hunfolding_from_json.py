import os
import json

def hunfolding_from_json(self, filename:str):
    """Lire fichier json et creer un dico pour le deroulement (pour la db)

    a partir d un fichier json

    :param str filename: chemin/nom.json du fichier
    :param str office: nom de l'office
    """

    if not os.path.exists(filename):
        raise ValueError(f"File does not exists ! {filename}")
    #endIf

    try:
        with open(filename, 'r') as f:
            datas = json.load(f, strict=False)
        #endWith
    except Exception as e:
        print(f"Exception : {e}")
    #endTry

    i = 1

    cols = ("id_deroule", "nom_office", "cle_element", "titre_particulier", "ajouter_doxologie", "element_defaut")

    outdatas = []

    for e in datas['deroulement']:
        d = {e:None for e in cols}
        d["id_deroule"] = i
        d["nom_office"] = self.office
        d["cle_element"] = e["key"]
        d["titre_particulier"] = e["name"] if "name" in e.keys() else None
        d["ajouter_doxologie"] = e["gloria_patri"] if "gloria_patri" in e.keys() else None

        if "fromfile" in e.keys() and e["fromfile"] :
            d["element_defaut"] = e["fromfile"]
        else:
            d["element_defaut"] = "aelf"
        #endIf

        i += 1
        outdatas = outdatas + [d,]
    #endFor

    return outdatas
#endDef
