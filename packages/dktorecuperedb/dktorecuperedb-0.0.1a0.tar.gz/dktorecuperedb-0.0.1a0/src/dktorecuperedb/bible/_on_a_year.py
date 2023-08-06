import os
import sqlite3

from .db import BibleDB

def on_a_year(self, day:int):
    db_name = os.environ.get("RECUPEREDB_BIBLE1YEAR_NAME", "bible_references")
    db_file = os.environ.get("RECUPEREDB_BIBLE1YEAR_PATH", "./datas/bible1year.db")

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    queries = f'''
SELECT book, chapter, start_verse, end_chapter, end_verse
FROM {db_name}
WHERE day = ?
ORDER BY id'''

    values = []
    c.execute(queries, [str(day),])
    result = c.fetchall()
    conn.close()

    out = {}
    for elt in result:
        ref, content = refColumns2Str(*elt)
        out[ref] = content
    #end

    return out
#endDef


def refColumns2Str(book, chapter, start_verse, end_chapter, end_verse):
    bible_db = BibleDB()
    if chapter is None or chapter == 9999:
        # Aller chercher chapitre min et max, versets min et max
        chapter = bible_db.getMinChapter(book) # min_chapter
        end_chapter = bible_db.getMaxChapter(book) # max_chapter
    #endIf

    if end_chapter is None:
        # Aller chercher versets min et max de chapter
        end_chapter = chapter
    #endIf


    if start_verse is None:
        start_verse = bible_db.getMinVerse(book, chapter) # min_verse de chapter
    #endIf

    if end_verse is None:
        end_verse = bible_db.getMaxVerse(book, end_chapter) # min_verse de chapter
    #endIf

    reference = f"{book} {chapter}:{start_verse}-{end_chapter}:{end_verse}"
    db_datas = bible_db.get_rangeVerse(
        book = book,
        start_chapter = chapter,
        end_chapter = end_chapter,
        start_verse = start_verse,
        end_verse = end_verse
    )

    chapter_previous = -1
    content = ""

    for book, chapter, verse, text in db_datas:
        if chapter != chapter_previous:
            if chapter != -1:
                content += "<br/>\n "
            #endIf
            content += f"<b><u>{chapter}</u></b> "
            chapter_previous = chapter
        #endIf

        content += f" <b>{verse}</b> {text}\n"
    #endFor

    return reference, content
#endDef

