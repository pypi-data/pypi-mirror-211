from .request2str import return_str

def get_biblebook(self, book):

    query = f"""
SELECT book_title
FROM  {self.db_name}
WHERE book LIKE '{book}'
GROUP BY book
"""

    result = self.request_db(query)
    print(f"DB_BOOK_NAME> {result}")

    return return_str(result, self.to_html)
#endDef
