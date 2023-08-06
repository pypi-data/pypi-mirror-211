import sys
import traceback

def compatMode(nom_var, list_var, verbose:bool=True, **kwargs):
    """Add a compatibility mode.

:param str nom_var: Name of the original variable.
:param list list_var: Names detecting a compatibility.
:param bool verbose: Verbose (default: True).
:param dict kwargs: All passing arguments.

:return: value for the original variable, kwargs (compatibility deleted).
:rtypes: tuple (2 elements).
"""
    out = None

    if not kwargs:
        return None, kwargs
    #endIf

    if isinstance(list_var, str):
        list_var = [list_var,]
    #endIF

    for e in list_var:
        if e in kwargs:

            if verbose:
                t = traceback.format_list(traceback.extract_stack())
                sys.stderr.write("".join(t))
                sys.stderr.write(f"> Compatibility mode:\n")
                sys.stderr.write(f"> Please correct the file {t[-4]}")
                sys.stderr.write(f"> Prefer {nom_var} than {e} in the call\n")

                if out:
                    sys.stderr.write(f"> Not the first time...")
                    sys.stderr.write(f"I'll change but please check your input parameters\n")
                #endIf
            #endIf

            out = kwargs[e]
            del kwargs[e]

        #endIf
    #endFor

    return out, kwargs

#endDef
