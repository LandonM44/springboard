import os
from twilio.rest import Client

account_sidz = 'AC7e88180ece0d5bf66ac3784fdeea8278'
auth_tokenz = '294bf875ef87ee49290d72edbbd8f863'
my_cell = '+17406448610'
my_twilio = '+15034384412'
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ[account_sidz]
auth_token = os.environ[auth_tokenz]
client = Client(account_sid, auth_token)

messages = client.messages.list(limit=20)

for record in messages:
    print(record.sid)