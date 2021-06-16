from timezonefinder import TimezoneFinder
from datetime import datetime
from geopy import geocoders
import pytz

GEOLOC_APP_NAME = 'Locator-request-app'


class Location:
    def __init__(self, name):
        self.name = name

        # get latitude, longitude
        geolocator = geocoders.Nominatim(user_agent=GEOLOC_APP_NAME)
        self.point = geolocator.geocode(self.name)

        if self.point == None:
            exit(f'ERROR: Can not find place by name.')

        # get timezone
        tf = TimezoneFinder()
        self.timezone = tf.timezone_at(
            lat=self.point.latitude, lng=self.point.longitude)

    def get_location_name(self):
        return self.name

    def get_local_time(self):
        tz = pytz.timezone(self.timezone)
        return datetime.now(tz)

    def get_local_time_utc(self):
        local_time = self.get_local_time()
        return local_time.astimezone(pytz.utc)

    def get_local_time_str(self, date_format):
        # for ex. date_format = '%m/%d/%Y'
        return self.get_local_time().strftime(date_format)

    def get_latitude_longitude(self):
        return self.point.latitude, self.point.longitude
