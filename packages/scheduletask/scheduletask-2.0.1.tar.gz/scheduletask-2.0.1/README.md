# scheduletask
Script to quickly create google calendar events from the command line. I created this script as a means to quickly jot down ideas for later. Pulling up GNOME Calendar and using my moues is *of course* too much work.

I'm working on a PyPI release soon, didn't realize I couldn't just *upload* it and it works. I thought computers were magic, damnit!
# Requirements

## Google Cloud Project
Follow the Prerequisites in this link : https://developers.google.com/calendar/api/quickstart/python. The downloaded credentials should be renamed to credentials.json.

On Windows, they should be put in as: `C:\Users\$USER\.credentials\credentials.json`

On Linux, they should be put in as:
`/home/$USER/.credentials/credentials.json`
## Google Calendar Simple API

https://github.com/kuzmoyev/google-calendar-simple-api

`pip install gcsa`

## Beautiful Date

https://github.com/kuzmoyev/beautiful-date

`pip install beauitful-date`

You also need an enviroment variable called "SCHEDULE_EMAIL" with your email. These are instructions on how to create them temporarily for the means of testing.

How to create one on Linux:  
`export SCHEDULE_EMAIL="example@example.org"`

How to create one on Windows (Powershell):
`$env:SCHEDULE_EMAIL = "example@example.org"`

# Roadmap:
Create some GitHub Actions workflows to automate package publishing alongside testing (For Windows, Linux, and Mac(Soon)).
