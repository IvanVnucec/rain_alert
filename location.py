from timezonefinder import TimezoneFinder
from datetime import datetime
from geopy import geocoders
import pytz
from utils import error, debug

GEOLOC_APP_NAME = 'Locator-request-app'


class Location:
    def __init__(self, name):
        self.name = name

        # get latitude, longitude
        try:
            geolocator = geocoders.Nominatim(user_agent=GEOLOC_APP_NAME)
            self.point = geolocator.geocode(self.name)
        except Exception as e:
            error(e)
        else:
            if self.point == None:
                error(f"Could not find '{self.name}'.")

            # get timezone
            tf = TimezoneFinder()
            self.timezone = tf.timezone_at(
                lat=self.point.latitude, lng=self.point.longitude)
            debug(f'Timezone: {self.timezone}')

    def get_location_name(self):
        return self.name

    def get_local_time(self):
        tz = pytz.timezone(self.timezone)
        local_time = datetime.now(tz) 
        debug(f'Local time: {local_time}')
        return local_time

    def get_local_time_utc(self):
        local_time = self.get_local_time()
        return local_time.astimezone(pytz.utc)

    def get_latitude_longitude(self):
        return self.point.latitude, self.point.longitude
