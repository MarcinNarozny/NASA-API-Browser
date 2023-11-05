import requests
import json


with open('key.txt', 'r') as file:
    key = file.read()

class Handler:
    url_base = "https://api.nasa.gov/" 
    api_key = "api_key=" + key

    def __init__(self, api_id, *args):
        self.args = args
        self.api_id = api_id

    def build_url(self, *args):
        arguments = "&".join(args)+"&"
        url = self.url_base + self.api_id + arguments + self.api_key
        self.response = requests.get(url).json()

    def print_raw_data(self):
        for k in self.response:
            #print(k," - ",self.response[k])
            print(k)


class HandlerAPOD(Handler):
    def __init__(self, api_id, *args):
        super().__init__(api_id, *args)

    def single_day_image(self, date=""):
        date = "date=" + date
        self.build_url(date)

    def date2date_images(self, start_date, end_date):
        start_date = "start_date=" + start_date
        end_date = "end_date=" + end_date
        self.build_url(start_date,end_date)

    def random_images(self, count):
        count = "count=" + str(count)
        self.build_url(count)


class HandlerNEO_Feed(Handler):
    def __init__(self, api_id, *args):
        super().__init__(api_id, *args)

    def single_day_objects(self, start_date):
        end_date = "end_date=" + start_date
        start_date = "start_date=" + start_date
        self.build_url(start_date,end_date)

    def date2date_objects(self, start_date, end_date):
        start_date = "start_date=" + start_date
        end_date = "end_date=" + end_date
        self.build_url(start_date,end_date)