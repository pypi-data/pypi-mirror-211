from .request2int import return_int

def getMaxChapter(self, book):

    query = f"""
SELECT chapter
FROM  {self.db_name}
WHERE chapter_id=(
   SELECT MAX(chapter_id)
   FROM {self.db_name}
   WHERE book = ?
)"""

    result = self.request_db(query, (book,))
    return(return_int(result))
#endDef


def getMinChapter(self, book):

    query = f"""
SELECT chapter
FROM  {self.db_name}
WHERE chapter_id=(
   SELECT MIN(chapter_id)
   FROM {self.db_name}
   WHERE book = ?
)"""

    result = self.request_db(query, (book,))

    return return_int(result)

#endDef
