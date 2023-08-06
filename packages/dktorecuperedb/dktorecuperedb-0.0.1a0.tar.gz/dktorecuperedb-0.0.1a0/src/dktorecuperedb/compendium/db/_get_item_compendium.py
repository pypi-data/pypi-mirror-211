def add_condition(name, variable):

    if variable is not None:
        query = f"AND (LOWER({name}) = LOWER(?))"
        tuple_query = [variable,]
    else:
        query = ""
        tuple_query = []
    #endIf
    return query, tuple_query
#endDef

def get_item_compendium(
        self,
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
        key=None,   #TODO : verifier qu a chaque appel de cette fonction, je passe sous la forme args=val !
        name=None,
        collection=None,
        language=None,
        disambiguation=None,
        group=None
):
    """
input : key or title
output : ((key, collection, title, text, disambiguation, language, author, editor, default), ...)
"""

    query  = "SELECT "
    query += ", ".join(items)+"  "
    query +=f"FROM {self.tcontent_name} "

    if key or name or collection or language or disambiguation:
        query += "WHERE "
    #endIf

    tuple_query = []
    if name is not None:
        query += "(LOWER(key) = LOWER(?) OR LOWER(title) = LOWER(?)) "
        tuple_query=[name, name]
    elif key or name or collection or language or disambiguation:
        query += "TRUE "
    #endIf

    if key is not None:
        q, t = add_condition("key", key)
        query += q
        tuple_query += t
    #endIf

    if collection is not None:
        q, t = add_condition("collection", collection)
        query += q
        tuple_query += t
    #endIf

    if language is not None:
        q, t = add_condition("language", language)
        query += q
        tuple_query += t
    #endIf

    if disambiguation is not None:
        q, t = add_condition("disambiguation", disambiguation)
        query += q
        tuple_query += t
    #endIf

    if group is not None:
        query += "GROUP BY "

        if isinstance(group, str):
            query+=group
        elif  isinstance(group, (list, tuple)):
            query += ", ".join(group)
        #endIf
    #endIf
    query += " ORDER BY key "
    print(query, tuple_query, group)
    return self.request_db(query, tuple(tuple_query))
#endDef
