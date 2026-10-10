import datetime


def cmd_date(args, shell=None):
    now = datetime.datetime.now().astimezone()
    return now.strftime("%a %b %d %H:%M:%S %Z %Y")
