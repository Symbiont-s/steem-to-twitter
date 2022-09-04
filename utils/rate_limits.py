# Standar library
from datetime                   import datetime, timedelta, timezone
# Third party library
from tinydb                     import TinyDB, Query
# Local
from error.exception_handling   import exception_handling
from error.exceptions           import Exception_Handling
from utils.const                import MINUTES, HOURS, LIMIT_RATE_FOR_15_MINUTES, LIMIT_RATE_FOR_3_HOURS, TIME_IN_HOURS_OF_THE_RATE_LIMIT

limit = TinyDB("data/rate_limit.json")
pause = TinyDB("data/hard_pause.json")
User = Query()


def verify_limit_of_requests(time_unit: str, rate_limit: int, rate_limit_time: int, account:str="default") -> bool:
    try:
        unit = limit.search(((User.name == time_unit)&(User.account == account)))
        time_limit = generate_time_delta(time_unit, rate_limit_time)
        if len(unit) >= 1 and unit[0]["date"]:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            current_date = get_date(unit[0]["date"])
            if now - current_date < time_limit:
                if unit[0]["count"] >= rate_limit:
                    return True
            else:
                update_date(time_unit, "", 0, account)
        return False
    except Exception as e:
        dict_exceptions = Exception_Handling().verify_limit_of_requests
        exception_handling(e,"verify_limit_of_requests",dict_exceptions) 
        return True


def generate_time_delta(time_unit: str, rate_limit_time: int):
    if time_unit == MINUTES:
        return timedelta(minutes=rate_limit_time)
    elif time_unit == HOURS:
        return timedelta(hours=rate_limit_time)
    elif time_unit == "days":
        return timedelta(days=rate_limit_time)
    raise Exception


def get_date(str_date):
    try:
        if str_date:
            current_date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
            return current_date
        else:
            return datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=2)
    except Exception as e:
        raise e


def update_date(time_unit: str, current_date: str, count:int=0,account:str="default"):
    limit.update({"date": current_date, "count": count},
                 ((User.name == time_unit) & (User.account == account)))


def update_count(time_unit: str, count:int=0, account:str="default"):
    limit.update({"count": count}, ((User.name == time_unit) & (User.account == account)))


def register_or_update(time_unit: str, account:str):
    try:
        unit = limit.search(((User.name == time_unit)&(User.account == account)))
        if unit != []:
            current_date = unit[0]["date"]
            if current_date:
                update_count(time_unit, unit[0]["count"]+1, account)
            else:
                now = datetime.now(timezone.utc).replace(tzinfo=None)
                update_date(time_unit, now.strftime("%Y-%m-%d %H:%M:%S"), 1, account)
        else:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            limit.insert({"name": time_unit, "date": now.strftime(
                "%Y-%m-%d %H:%M:%S"), "count": 1, "account":account})
    except Exception as e:
        dict_exceptions = Exception_Handling().register_or_update
        exception_handling(e,"register_or_update",dict_exceptions) 


def hard_pause(account:str):
    try:
        record = pause.search((User.account == account))
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        # if there is a record
        if record:
            record = record[0]
            current = record["current"]
            value_date = get_date(record["date"])
            hours_limit = generate_time_delta(HOURS,TIME_IN_HOURS_OF_THE_RATE_LIMIT )
            time_elapsed = now - value_date
            # If a forced pause of 15 minutes or 3 hours occurred in less than 3 hours and the error of many transactions occurs,
            # then we stop the bot for 3 hours
            if (current == MINUTES or current == HOURS) and time_elapsed < hours_limit:
                pause.update({"current":HOURS, "date": now.strftime("%Y-%m-%d %H:%M:%S")}, 
                             (User.account == account))	
                limit.update({"date": now.strftime("%Y-%m-%d %H:%M:%S"), "count": LIMIT_RATE_FOR_3_HOURS}, 
                             ((User.account == account)&(User.name==HOURS)))
            # If a forced pause of 15 minutes or 3 hours occurred in more than 3 hours and the error of many transactions occurs,
            # then we stop the bot for 15 minutes
            elif (current == MINUTES or current == HOURS) and time_elapsed >=  hours_limit:
                pause.update({"current":MINUTES, "date": now.strftime("%Y-%m-%d %H:%M:%S")}, 
                             (User.account == account))	
                limit.update({"date": now.strftime("%Y-%m-%d %H:%M:%S"), "count": LIMIT_RATE_FOR_15_MINUTES}, 
                             ((User.account == account)&(User.name==MINUTES)))
        # if it doesn't exist, we stop sending tweets for 15 minutes
        else:
            pause.insert({"current":MINUTES,"date":now.strftime("%Y-%m-%d %H:%M:%S"),"account":account})
            limit.update({"date": now.strftime("%Y-%m-%d %H:%M:%S"), "count": LIMIT_RATE_FOR_15_MINUTES}, 
                            ((User.account == account)&(User.name==MINUTES)))
    except Exception as e:
        dict_exceptions = Exception_Handling().hard_pause
        exception_handling(e,"hard_pause",dict_exceptions) 
