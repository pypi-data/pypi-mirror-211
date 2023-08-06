def get_collections(self):
    """
input : key or title
output : ((key, collection, title, text, disambiguation, language, author, editor, default), ...)
"""
    query  = "SELECT collection"
    query +=f"FROM {self.tcontent_name} "
    query += "GROUP BY collection"

    return self.request_db(query)
#endDef
