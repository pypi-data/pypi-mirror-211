from .request2int import return_int

def getMaxVerse(self, book, chapter):

    query = f"""
SELECT verse
FROM  {self.db_name}
WHERE verse_id=(
   SELECT MAX(verse_id)
   FROM {self.db_name}
   WHERE book = ?
   AND chapter = ?
)"""

    result = self.request_db(query, (book, chapter))
    return(return_int(result))
#endDef


def getMinVerse(self, book, chapter):

    query = f"""
SELECT verse
FROM  {self.db_name}
WHERE verse_id=(
   SELECT MIN(verse_id)
   FROM {self.db_name}
   WHERE book = ?
   AND chapter = ?
)"""

    result = self.request_db(query, (book, chapter))

    return return_int(result)

#endDef
