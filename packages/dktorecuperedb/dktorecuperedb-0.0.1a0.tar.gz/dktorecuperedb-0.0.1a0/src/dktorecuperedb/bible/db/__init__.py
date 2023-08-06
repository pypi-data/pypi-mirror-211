import os
from threading import Lock # verrou

from dktoeasysqlite3 import MyDB

class BibleDB(MyDB):
    def __init__(self):

        self.db_path=os.path.abspath(os.environ.get("RECUPEREDB_BIBLE_PATH", "./datas/bible.db"))

        super().__init__(lock_in=Lock())

        self.db_name=os.environ.get("RECUPEREDB_BIBLE_NAME", "verses")

        self.to_html=True
    #endDef

    from ._get_text_one_verse import get_text_oneverse
    from ._get_min_max_verse_number import getMaxVerse, getMinVerse
    from ._get_min_max_chapter_number import getMaxChapter, getMinChapter

    from ._get_book_name import get_biblebook

    from ._get_range_verse import get_rangeVerse
#endClass
