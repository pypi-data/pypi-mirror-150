#!/usr/bin/env python3
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event

from beautiful_date import *

import sys, os
def do():
    if len(sys.argv) <= 1:
        print('Missing arguments!')
        exit(1)
    task = sys.argv[1]
    time = sys.argv[2]
    day, month, year = int(D.now().day), int(D.now().month), int(D.now().year)
    calendar = GoogleCalendar(os.environ['SCHEDULE_EMAIL'])
    event = Event(task,
                 start=(day/M[month]/year)[int(time[:2]):int(time[2:])],
                 location="Operation Hope",
                 minutes_before_popup_reminder=30)
    calendar.add_event(event)
    print('Check your calendar...')

def main():
    if len(sys.argv)-1 and (sys.argv[1] == 'help' or sys.argv[1] == '-h' or sys.argv[1] == '--help' == ''):
        print("Simple commmand line script to create Google Calendar events on the fly to some extent.\n"
            "You will need at least 2 arguments, the task name itself and the time."
            "The first argument should be the task name itself in parantheses, like: \"Testing!\"\n"
            "The second argument is military time, like so: 1900")
        exit(0)
    do()

if __name__ == '__main__':
    main()