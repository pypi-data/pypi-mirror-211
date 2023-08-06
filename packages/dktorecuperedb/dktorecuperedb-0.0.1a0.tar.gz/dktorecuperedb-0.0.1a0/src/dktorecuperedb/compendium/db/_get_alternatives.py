def get_alternatives(
        self,
        alternative_usage:str,
        items = [
            "key",
            "collection",
            "title",
            "text",
            "disambiguation",
            "language",
            "author",
            "editor",            #"default"
        ],
):


    keys = [f"{self.tcontent_name}.{e}" for e in items]
    keys += [f"{self.tcollection_name}.{e}" for e in ["usage"]]
    query = f"""
SELECT {",".join(keys)}
FROM {self.tcollection_name}
LEFT JOIN {self.tcontent_name} ON {self.tcontent_name}.key = {self.tcollection_name}.key_content
"""

    if isinstance(alternative_usage, str):

        query += f"WHERE {self.tcollection_name}.usage = ?"
        alternative_usage = [alternative_usage,]

    elif isinstance(alternative_usage, list) or isinstance(alternative_usage, tuple) and alternative_usage:

        query += f"WHERE "

        for e in alternative_usage[:-1]:
            query += f"{self.tcollection_name}.usage = ? OR "
        #endFor

        query += f"{self.tcollection_name}.usage = ?"

    elif not alternative_usage:

        print("db comp get alternative - Rein a sortir")
        return None

    #endIf

    query += f" ORDER BY {self.tcontent_name}.title"

    out =  self.request_db(query, alternative_usage)

    rglk = range(len(keys))

    z= list(({keys[i].split(".")[1]:a[i]  for i in rglk} for a in out)) # Transformer en dictionnaire

    return z
#endDef
