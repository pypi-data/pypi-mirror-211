def get_sequence_index(self):
    """
input : key or title
output : ((key, title, text, collection, disambiguation, language, author), ...)
"""
    query = f"""
SELECT
{self.tsequence_name}.sequence_name
FROM {self.tsequence_name}
GROUP BY {self.tsequence_name}.sequence_name
"""
    print(query)
    return  self.request_db(query)
#endDef
