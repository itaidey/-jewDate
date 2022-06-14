#!/usr/bin/python3

import requests #to send https requests
import json # to parse the web answer
import webbrowser
import geocoder
from datetime import datetime, timezone, date
from dateutil import tz # this is for time zone
from geopy.geocoders import Nominatim





"""
these are our constants.
"""
GET_TIMES_BASE_URL = r"https://api.sunrise-sunset.org/json?"
NEEDED_TIME_FIELDS = ['sunrise', 'sunset', 'day_length']
TIMES_FIELDS = ['sunrise', 'sunset']
DEFAULT_LOCATION = 'Herzeliya'


class JewishDate:

    def __init__(self, requested_date: date = date.today(), requested_location: str = DEFAULT_LOCATION):
        if(not isinstance(requested_date, date)):
            raise TypeError('sorry not type of date')

        self.date = requested_date
        self._requested_location_str = requested_location
        self.location = Nominatim(user_agent='Jewish-time-app').geocode(self._requested_location_str)
        self.refresh_my_times()


    def refresh_my_times(self):
        date_str = self.date.strftime('%Y-%m-%d')
        params = {"lat":self.location.latitude, "lng":self.location.longitude, "date":date_str , "formatted":0}
        self.my_times = JewishDate._get_times_with_url(GET_TIMES_BASE_URL, params)
        self.remove_not_needed_times()
        self.convert_to_location_time_zone()


    def remove_not_needed_times(self):
        """
        keeps only fields according to NEEDED_TIME_FIELDS
        """
        self.my_times = {k: v for (k,v) in self.my_times.items() if k in NEEDED_TIME_FIELDS}


    def convert_to_location_time_zone(self):
        
        temp_dict = {}
        for (k,v) in self.my_times.items():
            if k in TIMES_FIELDS:
                temp_dict[k] = JewishDate.datetime_from_utc_time_to_local_zone(v, self._requested_location_str)
            else:
                temp_dict[k] = v

        self.my_times = temp_dict


    def get_sunrise(self) -> str:
        return self.my_times['sunrise']


    def get_sunset(self) -> str:
        return self.my_times['sunset']
        

    def __str__(self):
        jd_str = f"date:\t\t{self.date}\n"
        jd_str += f"location:\t{self._requested_location_str}\n"
        jd_str += f"sunrise:\t{self.my_times['sunrise']}\n"
        jd_str += f"sunset:\t\t{self.my_times['sunset']}\n"

        return jd_str



    def set_date(self, new_date: date = date.today()):
        self.date = new_date
        self.refresh_my_times()



    def set_location(self, new_location: str = DEFAULT_LOCATION):
        self._requested_location_str = new_location
        self.location = Nominatim(user_agent='Jewish-time-app').geocode(self._requested_location_str)
        self.refresh_my_times()


    def get_requested_location(self) -> str:
        return self._requested_location_str

    @staticmethod
    def _get_times_with_url(times_url: str, params: json) -> json:
        reply = requests.get(times_url, params=params)
        reply = json.loads(reply.text)
        reply = reply["results"]
        return reply

    @staticmethod
    def datetime_from_utc_time_to_local_zone(utc_time: str, to_location: str) -> datetime:
        """
        this function gets a utc time string and location string
        and converts the time zone to the location
        """
        utc_zone = tz.tzutc()
        local_zone = tz.tzlocal()### change
    
        dt_utc = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S+00:00")
        dt_utc = dt_utc.replace(tzinfo=utc_zone)
        dt_local = dt_utc.astimezone(local_zone)
        return dt_local





if __name__ =="__main__":
    jd = JewishDate(requested_date = date.today(), requested_location='Herzeliya')
    print(jd)

    jd.set_location('Jerusalem')
    print(jd)