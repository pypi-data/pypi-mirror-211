import os
import sys
import json

from dktotoolkit import parse_date

# classmethods
from ._call_api import _call_api

"""
Database:
---------

* All datas are in HTML - ascii

[office] :
- id_office => index
- source       = source de l'office = aelf uniquement pour le moement
- date_requete = yyyy-mm-dd
- zone         = calendrier  (AELF)
- calendrier   = calendrier  (dans le cas ou on utilise la zone "romain" pour un calendrier francais par exemple)
- date         = yyyy-mm-dd  (AELF)
- nom          = nom de l'office (AELF)
- couleur      = couleur liturgique (AELF)
- annee        = A, B ou C (pour les messes uniquement) (AELF)
- temps_liturgique = (AELF)
- semaine = (AELF)
- jour = (AELF)
- jour_liturgique_nom = (AELF)
- fete = (AELF)
- degre = (AELF)
- ligne1 = (AELF)
- ligne2 = (AELF)
- ligne3 = (AELF)
- couleur2 = (AELF)
- couleur3 = (AELF)

[liaison] :
- id_office
- id_element
- cle_element

[element] :
- id_element
- titre
- texte
- editeur
- auteur
- reference
# Remarque : a la difference d'AELF, je renvoie toujours cette structure, et éléments vides avec None

[deroule]:
- id_deroule => index
- nom_office
- id_deroule : position (exemple : intro des vepres = 0, confiteor des vepres = 1, hymne des vepres = 2, ...)
- cle_element : exemple : "psaume1", "antienne1" : bref, les cles d'AELF
- titre_particulier : pour forcer le titre
- ajouter_doxologie : ajouter la doxologie apres l'element s'il n'est pas vide
- element_defaut : aelf ou nom de la variante dans la BD compendium


                +--------------+
                |   office     |
                +--------------+
                  | id_office (PK)
                  | ...
                  |
                  |     +----------------+
                  |     |   liaison      |
                  |     +----------------+
                  |     | id_office (FK) |
                  |     | id_element (FK)|
                  |     | cle_element    |
                  |     +----------------+
                  |
                  |     +-----------------+
                  +---->|    element      |
                  |     +-----------------+
                  |     | id_element (PK) |
                  |     | titre           |
                  |     | texte           |
                  |     | editeur         |
                  |     | auteur          |
                  |     | reference       |
                  |     +-----------------+
                  |
                  |     +-------------------+
                  +---->|    deroule        |
                        +-------------------+
                        | id_deroule (PK)   |
                        | nom_office        |
                        | id_deroule        |
                        | cle_element       |
                        | titre_particulier |
                        | ajouter_doxologie |
                        | element_defaut    |
                        +-------------------+

"""

class Office:
    """
RECUPERER LES INFOS DU BOT (office)

:param list(str) available_source: = ["aelf", ]
:param list(str) available_format_output: = ["html", "markdown"]
:param list(str) available_calendar: = ["francais", "romain"]
:param list(str) available_office: = ["vepres", "complies"] #TODO : a remplir !!

:param str format_output: Format de sortie
:param str date: date (YYYY-MM-DD) Date de l'office
:param str calendar: Calendrier / zone utilisé
:param str office: nom de l'office
:param str source: source principale de l'office (uniquement AELF actuellement)
"""
    def __init__(self, format_output="html", date="today", calendar="francais", office=None, source="aelf"):
        """
Constructeur

:param str formatting: [html, markdown] format de sortie
:param str calendar: calendrier
:param str|Date date: date de l'office
:param str office: nom de l'office
:param str source: source (AELF uniquement actuellement)
"""
        self.available_source = ["aelf", ]
        self.available_format_output = ["simple_html", "html", "markdown", "native"]
        self.available_calendar = ["romain", "france", "luxembourg", "belgique"]
        self.available_office = ["laudes", "sextes", "nones", "vepres", "complies", "lectures", "messe"] #TODO : a remplir !!!

        self.format_output = format_output.lower()
        print("\n\nTODO : parse date !!!")
        print("from lib.calendar import parse_dates as dates ; dates.parse_date(the_day)")
        print("ENDTODO\n\n")

        self.date = parse_date(date)  # Appeler la fonction "convert_date" ou jsp comment : YYYY-MM-DD
        self.calendar = calendar.lower()
        self.source = source.lower()
        self.office = office.lower()

    #endDef

    # Update
    from ._update_office import update_office
    from ._update_hunfolding import update_hunfolding

    from ._check_input import check_input

    from ._get_info_from_db import get_info_from_db
    from ._get_office import get_office
    from ._get_hunfolding import get_hunfolding
    from ._get_alternatives import get_alternatives

    from ._hunfolding_from_json import hunfolding_from_json

    def update_attributes(self, format_output:str=None,**kwargs):
        """
        Update attributes of the class from the kwargs
        """
        if format_output is None:
            pass
        elif not isinstance(format_output, str):
            sys.stderr.write(f"> Office.get_office(): format_output={format_output} must be a string\n")
        elif format_output.lower() in self.available_format_output:
            self.format_output = format_output.lower()
        elif format_output.lower() not in self.available_format_output:
            sys.stderr.write(f"> Office.get_office(): format_output={format_output} not available ; please use one in {self.available_format_output}\n")
        else:
            sys.stderr.write(f"> Office.get_office(): format_output={format_output} unexpected\n")
        #endIf

        return kwargs
    #endDef

    def update_db(self):
        self.update_office()
        self.update_hunfolding()
    #endDef

    @classmethod
    def call_api(cls, source, calendar, date, office):
        """Selectionner l'API à utiliser - uniquement AELF pour le moment

        :param str source: Nom de la source : UNIQUEMENT AELF
        :param str calendar: Nom du calendrier (pour aelf)
        :param str date: Date YYYY-MM-DD
        :param str office: Nom de l'office
        """
        return _call_api(source, calendar, date, office)
    #endDef

#endClass
