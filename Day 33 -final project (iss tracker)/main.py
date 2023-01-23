import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -7.702910
MY_LONG = 114.014748

gmail_server_addr = "smtp.gmail.com"
yahoo_server_addr = "smtp.mail.yahoo.com"

my_gmail = "errtest44@gmail.com"
my_gmail_pw = "zjyumsqwdrndcqpj"

yahoo_email = "err_test45@yahoo.com"
yahoo_email_pw = "N!.5MjHjuX?))kS"

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

check = 0


def send_email(provider, from_add, pw, to_add, subject, message):
    with smtplib.SMTP(provider, 587, timeout=120) as connection:  # a way to connect to email provider
        connection.starttls()
        connection.login(user=from_add, password=pw)
        connection.sendmail(
            from_addr=from_add,
            to_addrs=to_add,
            msg=f"Subject:{subject}\n\n{message}"
        )
    print("mail has sent!")


# # add ISS location
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()
# data = response.json()
#
# iss_latitude = float(data["iss_position"]["latitude"])
# iss_longitude = float(data["iss_position"]["longitude"])

def iss_loc():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_loc_dict = {
        "iss_latitude": iss_latitude,
        "iss_longitude": iss_longitude,
    }
    return iss_loc_dict


# # add sunrise and suset hour
# response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
# response.raise_for_status()
# data = response.json()
# sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
# sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

def sunrise_sunset_hr():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    dict = {
        "sunrise": sunrise,
        "sunset": sunset
    }
    return dict


# add time now


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


def run():
    global check
    check += 1
    time_now = datetime.now()
    iss_now = iss_loc()
    st_sr_hr = sunrise_sunset_hr()
    print(f"{check}St check")
    print(
        f"Date now: {time_now}\n"
        f"(sunrise_hr, sunset_hr) = ({st_sr_hr['sunrise']}, {st_sr_hr['sunset']})\n"
        f"my loc vs iss (lat, lng) :: ({MY_LAT},{MY_LONG}) vs ({iss_now['iss_latitude']},{iss_now['iss_longitude']})"
    )

    if iss_now['iss_latitude'] + 5 >= MY_LAT >= iss_now['iss_latitude'] - 5 and iss_now[
        'iss_longitude'] + 5 >= MY_LAT >= iss_now['iss_longitude'] - 5:
        if st_sr_hr["sunrise"] >= time_now.hour >= st_sr_hr['sunset']:
            send_email(
                gmail_server_addr,
                my_gmail,
                my_gmail_pw,
                yahoo_email,
                "ISS Tracker",
                "yooo, look up to the sky✨✨. ISS is above youu😎!!"
            )
    time.sleep(60)   # perbarui data tiap 60 detik
    print("")
    run()


run()
