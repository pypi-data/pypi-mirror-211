from .parse_dates import _parse_date
from .dict2obj import _dict2obj



def parse_date(the_day=None):
    """Convert a date into the format YYYY-MM-DD

:param str the_day: The day (almost all formats, alors today, etc)
    """
    return _parse_date(the_day=the_day)
#endDef


def dict2obj(d=None, obj=None):
    """Convert nested Python dictionnary to object

:author: geeksforgeeks.org

:param dict d: input dictionnary
:param obj: a class (could be empty)
    """
    return _dict2obj(d=d, obj=obj)
#endDef

class LoadEnv:
    """Load .env file

:param str filename: Path and name of the file (default: ./.env)
:param bool erase_variable: Erase variable if already exists (default: False)
"""

    def __init__(self, filename:str="./.env", erase_variable:bool=False):
        self.erase_variable = False
        self.filename = filename

        self.load()
    #endDef

    from ._loadenv import load, getEnvironVar
#endClass

