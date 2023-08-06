import os
import sys
from zoneinfo import ZoneInfo
import datetime

if __name__=="__main__":
    path=os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(path, "../.."))
    path=None
#endIf

from lib.usefull.loadenv import getEnvironVar


#TODO : permettre de ne pas rentrer de timezone

def getTimesForBells(dotenv_timevar="BPRIERE_REMINDER", outdico=False):

    # If no tzinfo is given then UTC is assumed.
    tzone = ZoneInfo(getEnvironVar("BPRIERE_TZONE"))

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



def time2officeName(dico_times):

    if not dico_times:
        return ""
    #endIf

    cur=datetime.datetime.now(tz=ZoneInfo(os.environ.get("BPRIERE_TZONE")))
    today = datetime.datetime.today()

    try:
        t_inputs = {
            k:abs(
                cur.timestamp() -
                today.replace(hour=v["hour"], minute=v["minute"], second=v["second"]).timestamp())
            for k,v in dico_times.items()
        }
    except:
        print("EXCEPTION, time2officeName")
        print(e)
        raise Exception
    #endTry

    office_name = min(t_inputs, key=t_inputs.get)

    return office_name
#endDef
