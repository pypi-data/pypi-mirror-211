def add_office(self, infos, id_office=None, office=None, calendar=None):
    """Add the informations of the office to the database

    :params dict infos: The informations (cf Office class description)
    """
    # self.dico2datas(self.db_tinfo_name, infos)
    # parser html des donnees

    cols=("id_office", "source", "date_requete",
          "zone", "calendrier", "date", "nom", "couleur", "annee",
          "temps_liturgique", "semaine", "jour", "jour_liturgique_nom", "fete",
          "degre", "ligne1", "ligne2", "ligne3", "couleur2", "couleur3"
          )

    infos["id_office"]=id_office #f"{calendrier}_{date}_{office}"
    infos["nom"] = office
    infos["calendrier"] = calendar
    values = [infos[e] if e in infos.keys() else None for e in cols]

    self.insert_data(self.db_tinfo_name, {cols[i]:values[i] for i in range(len(cols))}, allow_duplicates=False, commit=True)

    return
#endDef
