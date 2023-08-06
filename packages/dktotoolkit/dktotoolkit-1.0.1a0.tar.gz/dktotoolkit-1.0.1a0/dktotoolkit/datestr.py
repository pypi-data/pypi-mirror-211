import sys
import re
from datetime import date, time, timedelta
import traceback

def parser_date(the_day:str="today", verbose:bool=True):
    """Convert a date into the format YYYY-MM-DD

:param str the_day: The day (almost all formats, alors today, etc) (default: today)
:param bool verbose: Verbose (default: True)
"""
    if isinstance(the_day, date):

        return "{0:04d}-{1:02d}-{2:02d}".format(
                int(the_day.year),
                int(the_day.month),
                int(the_day.day)
        )

    elif isinstance(the_day, str):

        the_day = the_day.lower()

    else:

        raise parseError

    #endIf

    if the_day is None or the_day in ["today", "aujourd_hui"]:

        today = date.today()
        return "{0:04d}-{1:02d}-{2:02d}".format(
                int(today.year),
                int(today.month),
                int(today.day)
        )

    else:

        return _str2date(date_string=the_day, verbose=verbose)

    #endIf

    raise parseError
#endDef


def _parse_month(month_in):
    """Convert month to the month number

:param str month_in: The month to parse
:return: The month number
:rtypes: str "01"-"12" for months between january-december
"""

    month = "00" # Si on est en dehors des elements :

    all_months={
        "01":["janvier"  , "janv", "january" , "jan"  , "01","1"],
        "02":["fevrier"  , "fev" , "february", "febr" , "02","2"],
        "03":["mars"     , "mar" , "march"   ,          "03","3"],
        "04":["avril"    , "avr" , "april"   , "apr"  , "04","4"],
        "05":["mai"      ,         "may"     ,          "05","5"],
        "06":["juin"     ,         "june"             , "06","6"],
        "07":["juillet"  , "juil", "jully"   , "jul"  , "07","7"],
        "08":["aout"     ,         "august"  , "aug"  , "08","8"],
        "09":["septembre", "sept", "september",         "09","9"],
        "10":["octobre"  , "oct" , "october" ,          "10"],
        "11":["novembre" , "nov" , "november",          "11"],
        "12":["decembre" , "dec" , "december",          "12"]
    }

    for month_nb, values in all_months.items() :
        if month_in in values:
            month="{0:02d}".format(int(month_nb))
        #endIf
    #endFor

    return month
#endDef


def _str2date(date_string:str=None, format_us:bool=None, verbose:bool=True):
    """Convert an input date to a formated date

:param str date_string: The date
:param bool format_us: Set input format as YYYY MM DD
:param bool verbose: Verbose (default: True)

:return: date as format YYYY-MM-DD
:rtypes: str
"""
    if date_string is None:
        return None
    #endIf

    today = date.today() # j'en aurais potentiellement besoin plus tard

    splitDate_in = [e for e in re.split("-|/|_| |\xa0", date_string) if e]

    if len(splitDate_in)>1 and not ("hier" in date_string.lower()) and not ("demain" in date_string.lower()):
        # Recuperer l'annee
        pos_yr_in = 2  # De base, l'annee est en 3eme position, mais on va le verifier

        if len(splitDate_in) > 2:

            # Formattage US ou francais ?
            if format_us is None:
                format_us = (len(splitDate_in[0]) == 4)
            #endIf

            if format_us:
                pos_yr_in=0
            else:
                pos_yr_in=2
            #endIf

            if len(splitDate_in[pos_yr_in]) < 4:
                year="20{0:02d}".format(int(splitDate_in[pos_yr_in]))
            else:
                year=splitDate_in[pos_yr_in]
            #endIf

        else:
            year="{0:04d}".format(int(today.year))
        #endIf

        # Recuperer le jour
        if (pos_yr_in == 2)or(len(splitDate_in) < 3):
            pos_day_in=0
        else:
            pos_day_in=2
        #endIf

        # Recuperer le mois
        month = _parse_month(splitDate_in[1])

        if int(month) == 0: # si on a une inversion mois / jour (car mois > 12)
            if verbose:
                sys.stderr.write(f"pd> Warning : unknown month or inversion of month and days in {date_string} : {splitDate_in} ! I'll change month and day positions\n")
            #endIf
            pos_month_in = pos_day_in
            pos_day_in = 1

            month = _parse_month(splitDate_in[pos_month_in])

            if int(month) == 0:
                if verbose:
                    sys.stderr.write(f"pd> Warning : After one more test, unknown month in {date_string} : {splitDate_in} ! Delete month value\n")
                #endIf
                pos_day_in = pos_month_in
            #endIf

        #endIf

        day="{0:02d}".format(int(splitDate_in[pos_day_in]))

        return "{0:04d}-{1:02d}-{2:02d}".format(int(year),int(month),int(day))

    else:

        today = date.today()
        the_date = today
        if date_string.lower() in ["aujourd'hui", "aujourd hui", "aujourdhui", "today"]:
            pass
        elif date_string.lower() in ["hier","yesterday"]:
            the_date = today - timedelta(days=1)
        elif date_string.lower() in ["avant-hier","before-yesterday"]:
            the_date = today - timedelta(days=2)
        elif date_string.lower() in ["demain","tomorrow"]:
            the_date = today + timedelta(days=1)
        elif date_string.lower() in ["apres demain", "après-demain", "apres-demain", "après-demain","after-tomorrow"]:
            the_date = today + timedelta(days=2)
        else:
            t = traceback.format_list(traceback.extract_stack())
            sys.stderr.write("".join(t))
            sys.stderr.write("toolkit.datestr : Cas non implemente : {}\n".format(date_string))
            return "00-00-0000"
        #endIf

        return _date2str(the_date)
    #endIf

    sys.stderr.write("Warning : unexpected case : I return a wrong date !\n")
    return "00-00-0000"
#endDef

def _date2str(date):
    return "{0:04d}-{1:02d}-{2:02d}".format(
                int(date.year),
                int(date.month),
                int(date.day)
        )
#endDef
