from datetime import datetime

def get_current_date():
    date_string = datetime.now().strftime('%Y-%m-%d')
    return date_string

def get_current_datetime():
    date_time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return date_time_string


if __name__ == '__main__':
    print(get_current_date())
    print(get_current_datetime())






