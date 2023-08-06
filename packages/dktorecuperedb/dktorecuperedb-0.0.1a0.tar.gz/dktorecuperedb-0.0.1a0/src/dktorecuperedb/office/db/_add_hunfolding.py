def add_hunfolding(self, datas={}):
    """Ajouter un deroulement

    :param dict|list datas: Datas to add  {cle_element, id_deroule, ...} | [{cle_element, id_deroule, ...},...]
    """

    cols = ("id_deroule", "nom_office", "cle_element", "titre_particulier", "ajouter_doxologie", "element_defaut")

    if isinstance(datas, dict):
        datas = [datas,]
    #endIf

    for elt in datas:

        values = [elt[e] if e in elt.keys() else None for e in cols]

        self.insert_data(self.db_thunfolding_name, {cols[i]:values[i] for i in range(len(cols))}, allow_duplicates=False, commit=False)
    #endFor

    self.commit()

    return 0
#endDef
