from .request2str import return_str

def get_text_oneverse(self, book, chapter, verse):

    query = f"""
SELECT text
FROM  {self.db_name}
WHERE book LIKE '{book}'
AND chapter={chapter}
AND verse={verse}"""

    result = self.request_db(query)

    print(f"DB_TXT_ONE_VERSE> {result}")

    return return_str(result, self.to_html)
#endDef
