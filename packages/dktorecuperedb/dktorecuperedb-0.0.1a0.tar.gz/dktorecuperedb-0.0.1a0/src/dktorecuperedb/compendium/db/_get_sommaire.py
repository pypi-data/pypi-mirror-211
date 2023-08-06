def get_sommaire(self, seq_name):
    """
input : key or title
output : ((key, title, text, collection, disambiguation, language, author), ...)
"""
    keys=["key", "key_name", "name", "gloria_patri", "same_page"]
    keys_table=[f"{self.tsequence_name}.{e}" for e in keys]

    query = f"""
SELECT {",".join(keys_table)}
FROM {self.tsequence_name}
WHERE {self.tsequence_name}.sequence_name = ? ORDER BY {self.tsequence_name}.id_key
"""
    return  self.request_db(query, (seq_name,))
#endDef
