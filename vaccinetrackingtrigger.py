import sched, time
import datetime
import json
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import cachetools.func
import pandas as pd
import requests
from retry import retry


def get_all_district_ids():
    district_df_all = None
    for state_code in range(1, 40):
        response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code), timeout=3)
        district_df = pd.DataFrame(json.loads(response.text))
        district_df = pd.json_normalize(district_df['districts'])
        if district_df_all is None:
            district_df_all = district_df
        else:
            district_df_all = pd.concat([district_df_all, district_df])

        district_df_all.district_id = district_df_all.district_id.astype(int)

    district_df_all = district_df_all[["district_name", "district_id"]].sort_values("district_name")
    return district_df_all

@cachetools.func.ttl_cache(maxsize=100, ttl=30 * 60)
@retry(KeyError, tries=5, delay=2)
def get_data(URL):
    response = requests.get(URL, timeout=3)
    print(response)
    data = json.loads(response.text)['centers']
    return data

def get_availability(district_ids: List[int], min_age_limit: int):
    INP_DATE = datetime.datetime.today().strftime("%d-%m-%Y")

    all_date_df = None

    for district_id in district_ids:
        print(f"checking for INP_DATE:{INP_DATE} & DIST_ID:{district_id}")
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={}&date={}".format(district_id, INP_DATE)
        data = get_data(URL)
        df = pd.DataFrame(data)
        if len(df):
            df = df.explode("sessions")
            df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
            df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
            df['date'] = df.sessions.apply(lambda x: x['date'])
            df = df[["date", "min_age_limit", "available_capacity", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
            
            if all_date_df is not None:
                all_date_df = pd.concat([all_date_df, df])
            else:
                all_date_df = df

    if all_date_df is not None:
        all_date_df = all_date_df.drop(["block_name"], axis=1).sort_values(["min_age_limit", "available_capacity", "date", "district_name"], ascending=[True, False, True, True])
        # all_date_df = all_date_df[all_date_df.min_age_limit >= min_age_limit]
        all_date_df = all_date_df[(all_date_df.min_age_limit == min_age_limit)]
      
        all_date_df = all_date_df[all_date_df.available_capacity>0]
        all_date_df.set_index('date', inplace=True)
        return all_date_df
    return pd.DataFrame()


def send_email(data_frame, age,sender_email, receiver_email):
    if data_frame is None or len(data_frame.index) == 0:
        print("No Slots Available")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = "Availability for Age {} Count {}".format(age, len(data_frame.index))
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hi,
    Please refer vaccine availability"""

    html_header = """\
    <html>
      <body>
        <p>

    """

    html_footer = """\
    
        </p>
      </body>
    </html>
    """

    html = "{}{}{}".format(html_header, data_frame.to_html(), html_footer)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, "Enter 16 digit App Password") #PLEASE ENTER YOUR APP PASSWORD for eg:"CHGFYWLDJHAUDHJAN"
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Fetching details for Slot Availability...")
    min_age_limit = 18
    #Enter the districts with district id in the given format and include that component in dist_ids:
    # Ahmedabad = 154
    # Ahmedabad_Corporation = 770
    # Rajkot_Corporation = 775
    # Bangalore_Urban=265
    dist_ids = [Ahmedabad,Ahmedabad_Corporation,Rajkot_Corporation,Bangalore_Urban] #Remove the Unwanted Cities and Add your own
    sender_email="xyz@gmail.com"
    receiver_email = "abc@gmail.com"

    availability_data = get_availability(dist_ids, min_age_limit)
    send_email(availability_data, min_age_limit,sender_email, receiver_email)

    s.enter(30, 1, do_something, (sc,)) #Here 60 represents 1min=60 secs.You can increase the period accordingly to receive email updates.

s.enter(1, 1, do_something, (s,))
s.run()
