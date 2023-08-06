def add_elements(self, elements, id_office=None, office=None, date=None, calendrier=None):
    """Add elements of the office to the database

    :params dict elements: Elements (cf Office class description)
    :param str id_office: Identificateur de l'office (unique, doit correspondre a add_office)
    """

    # self.dico2datas(self.db_telements_name, elements)
    # parser html des donnees

    cols=("id_element", "id_office", "nom_office", "cle_element",
          "titre", "texte", "editeur", "auteur", "reference"
          )

    for k, v in elements.items():

        if isinstance(v, dict):

            v["id_element"]=None
            v["id_office"]=id_office
            v["nom_office"]=office
            v["cle_element"] = k
            values = [v[e] if e in v.keys() else None for e in cols]

        else:

            d = {e:None for e in cols}
            d["id_element"]=None
            d["id_office"]=id_office
            d["nom_office"]=office

            if isinstance(v, str) and v.lower() not in ["none",]:
                d["texte"] = v
            elif v:
                d["texte"] = str(v)
            else:
                d["texte"] = None
            #endIf

            d["cle_element"] = k
            values = [d[e] if e in d.keys() else None for e in cols]

        #endIf

        self.insert_data(self.db_telement_name, {cols[i]:values[i] for i in range(len(cols))}, allow_duplicates=False, commit=False)

    #endFor

    self.commit()

    return
#endDef
