"""Download the hourly historic weather from the dutch weather agency KNMI and
   localize the data to a particular lon/lat
   
   Note: only works in the Netherlands
   
   All copyright of the data belongs to the KNMI. 
   Please see https://www.knmi.nl/nederland-nu/klimatologie/uurgegevens for more details"""

from .main import get_local_weather, column_descriptions

__all__ = ['get_local_weather', 'column_descriptions']