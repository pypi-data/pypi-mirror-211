def get_infos(self, calendar, date_office, name_office, source): #->list(dict(str))
    """Récupérer les infos

    :param str calendar: Calendrier (=zone a AELF)
    :param str date_office: YYYY-MM-DD
    :param str name_office: Nom de l'office

    :returns: Resultat ; d = {zone, date, nom, couleur, annee, ...} (idem qu'AELF)
    :rtypes: list(dict(str))
    """
    # non retourne : "id_office", "cle_office", "date_requete"
    keys = [
        "source",
        # vvv infos AELF vvv
        "zone",  # calendrier (romain si concordance)
        "calendrier",  # calendrier reellement demande
        "date", # date de l'office
        "nom", # nom de l'office
        "couleur",
        "annee",
        "temps_liturgique",
        "semaine",
        "jour",
        "jour_liturgique_nom", "fete", "degre",
        "ligne1", "ligne2", "ligne3",
        "couleur2","couleur3"
    ]

    keys_table=[f"{self.db_tinfo_name}.{e}" for e in keys]

    query=f"""
SELECT {','.join(keys_table)}
FROM {self.db_tinfo_name}
WHERE {self.db_tinfo_name}.calendrier = ? AND {self.db_tinfo_name}.date = ? AND {self.db_tinfo_name}.nom = ? AND {self.db_tinfo_name}.source = ?
    """
    out = self.request_db(query, (calendar, date_office, name_office, source))

    datas_out = [{keys[i]:e[i] for i in range(len(e))} for e in out]

    return datas_out
#EndDef
