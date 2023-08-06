from .content_compendium import SubclassCompendium
from .content_sequence import SubclassSequence
#from .sequence import ClassSequence

class Compendium(SubclassCompendium):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #endDef
#endClass


class Sequence(SubclassSequence):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #endDef
#endClass
