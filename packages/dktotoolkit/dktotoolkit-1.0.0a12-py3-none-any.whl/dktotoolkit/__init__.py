from .parse_dates import _parse_date
from .dict2obj import _dict2obj
from ._replace_with_mask import _replace_with_mask


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




import sys

def replace_with_mask(arr, mask, replacement, inplace=False):
    """
    Remplace les valeurs dans un tableau selon un masque.

    :param arr: Le tableau d'origine.
    :type arr: list
    :param mask: Le masque indiquant les valeurs à remplacer.
    :type mask: list
    :param replacement: La valeur de remplacement.
    :param inplace: Indique si la modification doit être effectuée sur place (par défaut: False).
    :type inplace: bool

    :return: Le tableau modifié.
    :rtype: list
    """
    return _replace_with_mask(arr=arr, mask=mask, replacement=replacement, inplace=False)
#endDef

