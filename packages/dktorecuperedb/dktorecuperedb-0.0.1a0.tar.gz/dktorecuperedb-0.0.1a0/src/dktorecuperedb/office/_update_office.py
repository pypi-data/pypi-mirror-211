import os
from datetime import datetime
from dktoparserhtml import ParserHTML

from .db import OfficeDB


def update_office(self)->None:
    """Mise a jour de la base de donnee

    Voir aussi
    ----------

    :func:`OfficeDB.get_infos`
    :func:`call_api_aelf`
    :func:`OfficeDB.add_office` : parser html appele dedans
    :func:`OfficeDB.add_elements` : parser html appele dedans
    :func:`OfficeDB.delete_old_items` : delete items if date_today is passed or self.date is passed
    """

    db = OfficeDB()

    # 1. Aller chercher dans la bdd si le point existe
    # 2. Si le point existe : set la var infos
    info = db.get_infos(self.calendar, self.date, self.office, self.source)

    # 2. Si le point n'existe pas :
    if not info:
        date_today = datetime.today().strftime('%Y-%m-%d')
        # - supprimer les entrees de :
        # -- [ elements : cle_office = [ cle_office : date_requete = passé and date_office = passé]]
        # -- [office : date_requete = passé and date_office = passé] (en second)
        db.delete_old_items(self.date, date_today)

        # - infos, elements = call_api_aelf(date, calendrier) : set office={informations}, elements={nom_office}

        info, elements = self.call_api(self.source, self.calendar, self.date, self.office).values()
        # -- infos = {zone, date, ...}
        # -- elements =  {introduction = {titre, auteur, texte, ...}, hymne = {titre, auteur, texte, ...}, ...}


        # - add_to_db(infos, elements)
        info["source"] = self.source
        info["date_requete"] = date_today

        # Nettoyage
        info = {k:v if v else None for k,v in info.items()}

        info_html = ParserHTML(
            info,
            convertEmptyNone=True,
            convert_keys=False,
            skip_values=["date", "date_requete", "id_office"],
        ).utf8_to_html(cleanHTML=True,)

        elements_html = ParserHTML(
            elements,
            convertEmptyNone=True,
            convert_keys=False,
            skip_values=["cle_element", "element_defaut", "reference", "id_office"],
        ).utf8_to_html(cleanHTML=True,)

        id_office=f"{self.date}_{self.office}_{info['zone']}_{self.source}"

        db.add_office(
            info_html,
            id_office=id_office,
            office=self.office,
            calendar = self.calendar
        )

        db.add_elements(elements_html, id_office=id_office)  # Attention : la fonction ne reussi pas a ne pas ajouter de doublons : c est pour ca que c est fait avant

    #endIf

    db.close()

    return
#endDef
