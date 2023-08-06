
def get_rangeVerse(self,
                   book:str=None,
                   start_chapter:str=None, end_chapter:str=None,
                   start_verse:str=None, end_verse:str=None):

    if end_chapter is None or not end_chapter:
        end_chapter = start_chapter
    #endIf

    if end_verse is None or not end_verse:
        end_verse = start_verse
    #endIf

    if not book or not start_chapter or not start_verse or not end_chapter or not end_verse:
        print(f"WARNING {__file__}")
        print(f"_{book}__{start_chapter}:{start_verse}_-_{end_chapter}:{end_verse}_")
    #endIf

    query = f"""
SELECT book, chapter, verse, text
FROM {self.db_name}
WHERE
book = ?
AND
(
  chapter_id > (
      SELECT chapter_id from {self.db_name}
      WHERE book = ?
      AND chapter = ?
    )
  OR
  (
    chapter_id = (
      SELECT chapter_id from {self.db_name}
      WHERE book = ?
      AND chapter = ?
    )
    AND
    verse_id >= (
      SELECT verse_id from {self.db_name}
      WHERE book = ?
      AND chapter = ?
      AND verse= ?
    )
  )
)

AND
(
  chapter_id < (
      SELECT chapter_id from {self.db_name}
      WHERE book = ?
      AND chapter = ?
    )
  OR
  (
    chapter_id = (
      SELECT chapter_id from {self.db_name}
      WHERE book = ?
      AND chapter = ?
    )
    AND
    verse_id <= (
      SELECT verse_id from {self.db_name}
      WHERE book  = ?
      AND chapter = ?
      AND verse = ?
    )
  )
)

GROUP BY chapter, verse_id
"""
    var = (
        book,
        book, start_chapter,
        book, start_chapter,
        book, start_chapter, start_verse,
        book, end_chapter,
        book, end_chapter,
        book, end_chapter, end_verse )
    return self.request_db(query, var)
#endDef
