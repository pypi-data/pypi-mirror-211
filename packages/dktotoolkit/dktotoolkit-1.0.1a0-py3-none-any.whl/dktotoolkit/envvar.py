import os, sys

def load_dotenv(filename:str="./.env", erase_variable:bool=False):
    """Load .env file

:param str filename: Path and name of the file (default: ./.env)
:param bool erase_variable: Erase variable if already exists (default: False)
"""

    sys.stdout.write(F"> Load environment file : {filename}\n")

    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split("\n")[0].split("#")[0].split("=")
            if len(l) > 1:
                var = l[0].strip()
                val = l[1].strip().replace(",",":").replace(";",":")

                if os.environ.get(var, False) and not erase_variable:
                    sys.stdout.write(F"load_env> {var} = {os.environ.get(var)} (already set, erase_variable)\n")
                #endIf

                sys.stdout.write(F"load_env> {var} = {val} : ")
                if "\"" in val:
                    sys.stdout.write(F"warning : character \" in content (character removed)")
                    val = val.replace("\"","")
                else:
                    sys.stdout.write(F"Done")
                #endIf

                os.environ[var] = val
                sys.stdout.write("\n")

            #endIf
        #endFor
    #endWith

    sys.stdout.write(F"\n")

    #TODO : ajouter valeurs par defaut si pas presentes !

#endWith


def _castList(var:str, char:str):

    if "(" in var and ")" in var:
        sublist=[""]
        for e in var:
            if e=="(":
                sublist += ["",]
            elif e == ")":
                sublist += ["",]
            else:
                sublist[-1] += str(e)
            #endIf
        #endFor

        tr_sb_list = []
        for e in sublist:
            if not e or e in ["", ":"]:
                continue
            #endIf
            tr_sb_list += [castList(e, ":"),]
        #endFor

        return tr_sb_list
    #endIf

    try:

        if isinstance(var, list) or isinstance(var, tuple):
            return var
        else:
            L = [int(e.strip()) if e.strip().isdigit() else str(e.strip()) for e in var.split(char)]
            return L
        #endIf
    except ValueError:
        L = [str(e.strip()) for e in var.split(char)]
        return L
    except Exception as e:
        print(e)
        raise Exception
    #endTry
    return None
#endDef

def getEnvironVar(varname:str):
    var = os.environ.get(varname)

    if var is None :
        return None
    #endVar
    for char in [":",";",","]:  # separators
        if char in var:

            L = _castList(var, char)
            if L is not None:
                return L
            #endIf
        #endIf
    #endFor

    try:
        return int(var.strip())
    except ValueError:
        return str(var.strip())

    except Exception as e:
        print(e)
        raise Exception
    #endTry

#endDef


def getTimesReminder(dotenv_timevar="REMINDER", outdico=False):

    # If no tzinfo is given then UTC is assumed.
    tzone = ZoneInfo(getEnvironVar("TZONE", "Europe/Paris"))

    tuples_dotenv = getEnvironVar(dotenv_timevar)
    dico_out = {}

    if tuples_dotenv is None:
        return []
    #endIf

    for office, time in tuples_dotenv:
        l_hourMinSec = ["", "", ""]
        i = 0
        for char in time:

            if char.isdigit():
                l_hourMinSec[i] = l_hourMinSec[i]+char
                justchange=False
            elif not justchange:
                i += 1
                justchange = True
            #endIf
        #endFor
        l_hourMinSec = [int(e) if e else 0 for e in l_hourMinSec]
        d_hourMinSec = {"hour":l_hourMinSec[0],"minute":l_hourMinSec[1],"second":l_hourMinSec[2]}

        dico_out[office] = d_hourMinSec
        dico_out[office]["time"] = datetime.time(**d_hourMinSec ,tzinfo=tzone)
    #endFor

    if outdico:
        return dico_out
    else:
        return [v["time"] for k, v in dico_out.items()]
    #endIf

#endDef

if __name__=="__main__":
    #print(getEnvironVar("PWD"))
    #print(getEnvironVar("PATH"))
    fname=".env"
    load(fname)
    #print(getEnvironVar("BRPIERE_BELLS"))
