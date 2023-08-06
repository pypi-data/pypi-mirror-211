from ._compatMode import _compatMode

def compatMode(nom_var, list_var, **kwargs):
    """Add a compatibility mode

:param str nom_var: Name of the original variable
:param list list_var: Names detecting a compatibility
:param **kwargs: All passing arguments

:return: value for the original variable, **kwargs (compatibility deleted)
:rtypes: tuple (2 elements)
"""

    return _compatMode(nom_var, list_var, **kwargs)
#endDef
