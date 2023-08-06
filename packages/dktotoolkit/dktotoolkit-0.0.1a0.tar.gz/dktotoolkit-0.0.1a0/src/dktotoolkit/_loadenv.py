import os, sys

def load(self, filename=None, erase_variable=None):

    if filename is None:
        filename=self.filename
    #endIf

    if erase_variable is None:
        erase_variable = self.erase_variable
    #endIf

    sys.stdout.write(F"> Load environment file : {filename}\n")

    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split("\n")[0].split("#")[0].split("=")
            if len(l) > 1:
                var = l[0].strip()
                val = l[1].strip().replace(",",":").replace(";",":")

                if os.environ.get(var) and not erase_variable:
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


def getEnvironVar(varname:str):
    var = os.environ.get(varname)

    def castList(var:str, char:str):

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

    if var is None :
        return None
    #endVar
    for char in [":",";",","]:  # separators
        if char in var:

            L = castList(var, char)
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


if __name__=="__main__":
    #print(getEnvironVar("PWD"))
    #print(getEnvironVar("PATH"))
    fname=".env"
    load(fname)
    #print(getEnvironVar("BRPIERE_BELLS"))
