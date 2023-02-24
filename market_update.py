import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase

api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
market_url = "https://financialmodelingprep.com/api/v3/is-the-market-open"
