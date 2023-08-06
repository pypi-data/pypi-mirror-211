def get_elements(self, calendar, date_office, name_office, source_office="aelf"): #->list(dict(str))
    """Récupérer les éléments

    :param str calendar: Calendrier (=zone a AELF)
    :param str date_office: YYYY-MM-DD
    :param str name_office: Nom de l'office
    :param str source_office: Source de l'office (aelf)

    :returns: Resultat ; d = [{"id_deroule", "cle_element", ..., "titre", ...},...]
    :rtypes: list(dict(str))
    """

    # non retourne: "cle_deroule", "cle_element", "id_deroule"
    keys_hunfolding = [
        "id_deroule",
        "cle_element",
        "titre_particulier",
        "ajouter_doxologie",
        "element_defaut"
    ]

    # non retourne: "cle_element", "cle_office", "id_element"
    keys_elements = [
        "titre",
        "texte",
        "editeur",
        "auteur",
        "reference"
    ]

    keys_table=[f"{self.db_thunfolding_name}.{e}" for e in keys_hunfolding]
    #keys_table=keys_table + [f"{self.db_telement_name}.{e}" for e in keys_elements]
    keys_table=keys_table + [f"tabletmp.{e}" for e in keys_elements]
    # Utilisation d'une table temporaire pour merge

    keys = keys_hunfolding + keys_elements

    query=f"""
SELECT {','.join(keys_table)}
FROM {self.db_thunfolding_name}
LEFT JOIN (
   SELECT * FROM {self.db_telement_name}
   UNION
   SELECT * FROM  {self.db_tadditionnal_name}
) AS tabletmp
ON  tabletmp.cle_element = {self.db_thunfolding_name}.cle_element
WHERE (
  (
    tabletmp.id_office = (
      SELECT {self.db_tinfo_name}.id_office
      FROM {self.db_tinfo_name}
      WHERE {self.db_tinfo_name}.calendrier=?
        AND {self.db_tinfo_name}.date=?
        AND {self.db_tinfo_name}.nom=?
        AND {self.db_tinfo_name}.source=?
    )
   OR (
     tabletmp.id_office IS NULL
    )
  )
  AND tabletmp.texte IS NOT NULL
  AND {self.db_thunfolding_name}.nom_office = ?
)
ORDER BY  {self.db_thunfolding_name}.id_deroule
    """

    out = self.request_db(query, (calendar, date_office, name_office, source_office, name_office))

    datas_out = [{keys[i]:e[i] for i in range(len(e))} for e in out]

    return datas_out
