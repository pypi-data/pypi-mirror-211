def add_additionnal(self, content:dict={}):
    """Ajouter un element supplementaire aux priere, ajout directement via les sources

    :param dict content: Content to add
    """
    #TODO : a ecrire
    # - lire le fichier
    # - parser html des donnees

    cols=("id_element", "nom_office", "cle_element",
          "titre", "texte", "editeur", "auteur", "reference"
          )

    for v in content:

        query_search = query =f"""
SELECT {",".join(cols)}
FROM {self.db_tadditionnal_name}
WHERE {' AND '.join([f'{e}=?' for e in cols if e in v.keys()])} ;
        """
        print(query_search)
        values = [v[e] for e in cols if e in v.keys()]
        print(values)
        result_search=self.request_db(query_search, values)
        print("!!!>>>",  result_search)

        if not result_search:
            query =f"""
INSERT INTO {self.db_tadditionnal_name} {cols}
VALUES ({','.join(['?' for e in cols])}) ;
"""

            d = {e:v[e] if e in v.keys() else None for e in cols}
            values = [d[e] if e in d.keys() else None for e in cols]

            self.add_db(query, values, commit=False)
        #endIf

    #endFor
    self.commit()

    return 0
#end
