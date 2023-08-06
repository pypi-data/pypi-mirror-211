import sys
import traceback

def _compatMode(nom_var, list_var, **kwargs):

    out = None

    for e in list_var:
        if e in kwargs:

            t = traceback.format_list(traceback.extract_stack())
            sys.stderr.write("".join(t))
            sys.stderr.write(f"> Compatibility mode:\n")
            sys.stderr.write(f"> Please correct the file {t[-4]}")
            sys.stderr.write(f"> Prefer {nom_var} than {e} in the call\n")

            if out:
                sys.stderr.write(f"> Not the first time... I'll change but please check your input parameters\n")
            #endIf

            out = kwargs[e]
            del kwargs[e]

        #endIf
    #endFor

    return out, kwargs

#endDef
