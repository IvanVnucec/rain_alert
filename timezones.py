from timezonefinder import TimezoneFinder
from datetime import datetime
from geopy import geocoders
import pytz


class Location:
    __GEOLOC_APP_NAME = 'Locator-request-app'

    def __init__(self, name):
        self.__tf = TimezoneFinder()
        self.name = name

        # get latitude, longitude
        geolocator = geocoders.Nominatim(user_agent=self.__GEOLOC_APP_NAME)
        self.point = geolocator.geocode(self.name)

        self.timezone = self.__tf.timezone_at(
            lat=self.point.latitude, lng=self.point.longitude)

    def get_local_time(self):
        tz = pytz.timezone(self.timezone)
        return datetime.now(tz)
