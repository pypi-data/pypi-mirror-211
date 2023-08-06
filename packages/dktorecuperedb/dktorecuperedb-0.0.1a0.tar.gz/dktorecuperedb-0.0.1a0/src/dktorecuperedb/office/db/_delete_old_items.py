def delete_old_items(self, date_office, date_requete)->None:
    """Supprimer les anciennes entrees : office d'un jour passé créé par un jour passé

    :param str date_office: (YYYY-MM-DD)  Date de l'office
    :param str date_request: (YYYY-MM-DD)  Date de la requete

    :returns: None
    """

    # Suppression des entrees de la table [Element]
    query=f"""
DELETE FROM {self.db_telement_name}
WHERE {self.db_telement_name}.nom_office = (
   SELECT {self.db_tinfo_name}.nom
   FROM {self.db_tinfo_name}
   WHERE {self.db_tinfo_name}.date < ? AND {self.db_tinfo_name}.date_requete < ?
)
"""
    self.request_db(query, (date_office, date_requete))

    # Suppression des entrees de la table [Office]
    query=f"""
DELETE FROM {self.db_tinfo_name}
WHERE {self.db_tinfo_name}.date < ? AND {self.db_tinfo_name}.date_requete < ?
    """
    self.request_db(query, (date_office, date_requete))

    return
#endIf
