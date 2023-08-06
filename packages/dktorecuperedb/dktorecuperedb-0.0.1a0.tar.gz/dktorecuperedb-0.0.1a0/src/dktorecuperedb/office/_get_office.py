import sys
if __name__=="__main__":
    import os
    sys.path.insert(0, os.path.abspath('../..'))
#end

from dktoparserhtml import ParserHTML

from .db import OfficeDB
from ..compendium import Compendium

def insert_doxologie(lst):
    """
    Insère un élément spécifique après chaque élément ayant "b" à True dans une liste de dictionnaires.

    Args:
        lst (list): La liste de dictionnaires.

    Returns:
        list: La liste modifiée avec l'insertion de l'élément supplémentaire.
    """
    result = []
    next_id = 0
    i = 0
    for item in lst:

        item["id_deroule"] = next_id
        result.append(item)
        next_id += 1

        if "ajouter_doxologie" in item.keys() and item["ajouter_doxologie"]:

            new_item = {"id_deroule": next_id, "cle_element":f"doxologie", "texte": "INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER"}
            result.append(new_item)
            next_id += 1
            i += 1

        #endIf

    #endFor

    return result
#endDef

if __name__=="__main__":
    # Exemple d'utilisation
    data = [
        {"id_deroule": 1, "ajouter_doxologie": True, "t": "coucou"},
        {"id_deroule": 2, "ajouter_doxologie": None, "t": "Bonjour"},
        {"id_deroule": 3, "ajouter_doxologie": False, "t": "Hello"},
        {"id_deroule": 4, "ajouter_doxologie": True, "t": "Bye"},
        {"id_deroule": 5, "ajouter_doxologie": False, "t": "Haa", "p": "papa"},
    ]

    modified_data = insert_doxologie(data)
    print(modified_data)
#endIf

def get_office(self, format_output:str=None, **kwargs)->None:
    """Recuperer tout l'office a partir de la base de donnee, retourne les donnees au format self.format_output

    :returns: office
    :rtypes: dict
    """
    
    self.update_db()
    db = OfficeDB()

    # 3. (dict) info, (dict) hunfolding, (dict) office (=nom_office) = call_db_complet(date_office, calendrier, source="aelf"))
    elements = db.get_elements(self.calendar, self.date, self.office, self.source)
    infos = db.get_infos(self.calendar, self.date, self.office, self.source)

    db.close()

    # 4. Si formatting = html : conversion recursive
    # 4. Si formatting = markdown : conversion recursive

    # Modification des donnees :
    elements = insert_doxologie(elements)

    if kwargs and not "doxologie" in kwargs.keys():
        kwargs["doxologie"] = "doxologie_court"
    else:
        kwargs = {"doxologie":"doxologie_court"}
    #endIf

    for k, v in kwargs.items():

        cles = [e['cle_element'] if 'cle_element' in e.keys() else None for e in elements]
        mask_cle = [k == e for e in cles]

        if v is None or not v or v.lower() == "aelf": # utiliser la valeur par defaut
            continue
        #endIf

        if not k in cles: # Ne pas ajouter d'element qui ne serait pas présent dans le déroulé
            sys.stderr.write(f"Key {k} is not in the hunfolding: {cles}\n")
            continue
        #endIf

        comp = Compendium(key=v)
        exec_code = comp.name2data()

        if exec_code == 0:

            content={
                "titre": comp.title,
                "texte": comp.text,
                "editeur": comp.editor,
                "auteur": comp.author,
                "reference": comp.collection,
                "disambiguation":comp.disambiguation,
                "langue":comp.language,
            }

            # Il n'y a que la que j ai besoin de nettoyer, car le contenu d'AELF l'a ete
            content = ParserHTML(content).utf8_to_html(
                cleanHTML=(
                    True or self.format_output in ["simple_html", "markdown"]
                )
            )

            for i in range(len(elements)):
                if mask_cle[i]:
                    for k, v in content.items():
                        elements[i][k] = v
                    #endFor
                #endIf
            #endFor

        #endIf

    #endFor

    #endIf

    if self.format_output=="native":
        return  {
            "informations":infos,
            self.office:elements
        }
    #endIf
    
    infos_parser = ParserHTML(
        infos,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=["date", "date_requete", "id_office"],
    )
    infos_parser.utf8_to_html(inplace=True)

    elements_parser = ParserHTML(
        elements,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]
    )

    elements_parser.utf8_to_html(inplace=True)

    # 5. Retourner les infos
    print("FORMAT :             ", self.format_output)
    if self.format_output == "simple_html" :
        return {
            "informations":infos_parser.html_to_utf8(),
            self.office:elements_parser.html_to_utf8()
        }
    elif self.format_output == "html" :
        return {
            "informations":infos_parser.data, #TODO : create a get_data()
            self.office:elements_parser.data
        }
    elif self.format_output == "markdown" :
        return {
            "informations":infos_parser.html_to_markdown(),
            self.office:elements_parser.html_to_markdown()
        }
    #endIf

    return None
#endDef
