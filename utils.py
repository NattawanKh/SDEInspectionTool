from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


def get_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d,%H:%M:%S")


# For Controller Data =========================================================
def get_date_time_db():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_date_n_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d')

def get_time_n_date():
    now = datetime.now()
    return now.strftime('%H:%M:%S')

def get_date_one_hour_ago():
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    return one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')

def get_date_one_day_ago():
    now = datetime.now()
    one_day_ago = now - timedelta(days=1)
    return one_day_ago.strftime('%Y-%m-%d %H:%M:%S')


def get_date_one_week_ago():
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    return seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')

def get_date_one_month_ago():
    now = datetime.now()
    one_month_ago = now - relativedelta(months=1)
    return one_month_ago.strftime('%Y-%m-%d %H:%M:%S')

def get_date_one_year_ago():
    now = datetime.now()
    one_year_ago = now - relativedelta(years=1)
    return one_year_ago.strftime('%Y-%m-%d %H:%M:%S')

def get_date_one_thousand_year_ago():
    now = datetime.now()
    one_thousand_year_ago = now - relativedelta(years=1000)
    return one_thousand_year_ago.strftime('%Y-%m-%d %H:%M:%S')
    
#==============================================================================


def check_value_in_lists(data_list, target_value):
    return any(inner_list and inner_list[0] == target_value for inner_list in data_list)

get_time_n_date()
