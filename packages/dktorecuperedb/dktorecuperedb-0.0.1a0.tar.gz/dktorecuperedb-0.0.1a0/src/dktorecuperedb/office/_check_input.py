import sys

def check_input(self):

    """
    Vérifie les paramètres d'entrée de l'objet OfficeAELF.

    :returns: Un dictionnaire contenant le statut de vérification.
        - Si les paramètres sont valides, le dictionnaire contient {"status": "200"}.
        - Si des erreurs sont détectées, le dictionnaire contient {"status": "404", "error": "<liste_des_erreurs>"}.
    :rtype: dict
    """

    err = []
    if self.format_output.lower() not in self.available_format_output:
        err += [f"OfficeAELF.__init__() : formatting = {self.format_output}, not in {self.available_format_output} ! I'll use '{self.available_format_output[0]}'",]
        self.format_output = self.available_format_output[0]
    #endIf

    if self.calendar.lower() not in self.available_calendar:
        err += [f"OfficeAELF.__init__() : calendar = {self.calendar}, not in {self.available_calendar} !  I'll use '{self.available_calendar[0]}'",]
        self.calendar = self.available_calendar[0]
    #endIf

    if self.source.lower() not in self.available_source:
        err += [f"OfficeAELF.__init__() : source = {self.source}, not in {self.available_source} ! I'll use '{self.available_source[0]}'",]
        self.source = self.available_source[0]
    #endIf

    if self.office.lower() not in self.available_office:
        err += [f"OfficeAELF.__init__() : office = {self.office}, not in {self.available_office} ! STOP'",]
        self.office = None
    #endIf

    if err:
        sys.stderr.write(">>"+"\n>>".join(err))
        return {"status" : "404", "error" : "\n".join(err)}
    else:
        return {"status":"200"}
    #endIf

    return {"status":"-1", "error":"unexpected"}
#endDef
