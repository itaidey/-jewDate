#!/usr/bin/python3

import sys
from datetime import datetime, date

from tkinter import *  
import time #importing local time
from jewish_date import JewishDate

DEFAULT_LOCATION = 'Herzelia'



def get_sunrise(jd: JewishDate) -> datetime:
    jd.get_sunrise()

def get_sunset() -> datetime:
    jd.get_sunset()




class JewishClock:

    def __init__(self, requested_location: str = DEFAULT_LOCATION, requested_date: date = date.today()):
        print(f"requested_location: {requested_location}")
        self.jewish_datetime = JewishDate(requested_date, requested_location)


        #making window
        self.jewish_clock_window = Tk()
        self.jewish_clock_window.title('Digital Jewish Clock') #adding title to the window

        #adding the location
        self.location_stringVar = StringVar(self.jewish_clock_window)
        self.location_stringVar.set(self.jewish_datetime.get_requested_location())


        #giving name to our digital clock and styling it
        self.title_message = Label(self.jewish_clock_window, font=("arial",100,"italic"), text="Jewish Time", fg="black")
        self.title_message.pack()

        self.location_entry = self.create_and_pack_location_entry()
        self.ok_button = self.create_and_pack_ok_button()
    
        self.sunrise_message = Label(self.jewish_clock_window, font=("arial", 20, "italic"), text='sunrise: ' + self.jewish_datetime.get_sunrise().strftime('%H:%M:%S'), fg="blue")
        self.sunrise_message.pack(anchor='w')

        self.sunset_message = Label(self.jewish_clock_window, font=("arial", 20, "italic"), text='sunset: ' + self.jewish_datetime.get_sunset().strftime('%H:%M:%S'), fg="red")
        self.sunset_message.pack(anchor='w')

        self.clock_label = Label(self.jewish_clock_window, font=("times",150,"bold"),fg="black")
        self.clock_label.pack()
        
        self.jewish_clock()
        
        self.jewish_clock_window.mainloop() #loop is closed


    def set_location(self, new_location: str) -> bool:
        self.jewish_datetime.set_location(new_location)


    def jewish_clock(self):
        curr_time= time.strftime("%H:%M:%S")
        self.clock_label.config(text=curr_time)
        self.clock_label.after(100,self.jewish_clock)

    def create_and_pack_ok_button(self):
        ok_button = Button(self.jewish_clock_window, text='ok', command=self.change_location)
        ok_button.pack(anchor='w')
        return ok_button


    def create_and_pack_location_entry(self):
        location_entry = Entry(self.jewish_clock_window, width = 20, textvariable=self.location_stringVar)
        location_entry.pack(anchor='w')
        return location_entry


    def change_location(self):
        """
        this function happens when the ok button is pressed
        getting location string and refreshing the time
        """
        new_location = self.location_entry.get()
        self.jewish_datetime.set_location(new_location)
        self.refresh_times()

    def refresh_times(self):
        
        self.sunrise_message.config(text='sunrise: ' + self.jewish_datetime.get_sunrise().strftime('%H:%M:%S'))
        self.sunset_message.config(text='sunset: ' + self.jewish_datetime.get_sunset().strftime('%H:%M:%S'))



if __name__ == "__main__":
    jc = JewishClock('Jerusalem', date.today())


