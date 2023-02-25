import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase

api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
market_url = "https://financialmodelingprep.com/api/v3/is-the-market-open"


def marketCalendarUpdate():
    params = {
        "apikey": api_key,
    }

    response = requests.get(market_url, params=params)
    data = response.json()

    holidays = []
    for holiday_year in data["stockMarketHolidays"]:
        for holiday_name, holiday_date in holiday_year.items():
            if holiday_name != "year" and holiday_date is not None:
                holidays.append(
                    (
                        datetime.strptime(str(holiday_date), "%Y-%m-%d"),
                        "close",
                        holiday_name,
                    )
                )

    start_date = holidays[0][0]
    start_date = start_date.replace(month=1, day=1)

    end_date = holidays[-1][0]
    end_date = end_date.replace(month=12, day=31)

    holidays_df = pd.DataFrame(holidays, columns=["dtDate", "marketStatus", "holiday"])

    date_range = pd.date_range(start_date, end_date, freq="D")

    date_range_df = pd.DataFrame({"dtDate": date_range})

    market_calendar_df = pd.merge(date_range_df, holidays_df, how="left", on="dtDate")

    market_calendar_df["marketStatus"].fillna("open", inplace=True)

    independence_day_mask = market_calendar_df["holiday"] == "Independence Day"
    market_calendar_df.loc[
        independence_day_mask.shift(-1).fillna(False), "marketStatus"
    ] = "half"
    market_calendar_df.loc[independence_day_mask, "marketStatus"] = "close"

    thanksgiving_day_mask = market_calendar_df["holiday"] == "Thanksgiving Day"
    christmas_mask = market_calendar_df["holiday"] == "Christmas"
    market_calendar_df.loc[
        thanksgiving_day_mask.shift(1).fillna(False), "marketStatus"
    ] = "half"
    market_calendar_df.loc[thanksgiving_day_mask, "marketStatus"] = "close"
    market_calendar_df.loc[
        christmas_mask.shift(1).fillna(False), "marketStatus"
    ] = "half"
    market_calendar_df.loc[christmas_mask, "marketStatus"] = "close"

    market_calendar_df.loc[
        market_calendar_df["dtDate"].dt.dayofweek.isin([5, 6]), "marketStatus"
    ] = "close"

    market_calendar_df.drop("holiday", axis=1, inplace=True)

    open_mask = market_calendar_df["marketStatus"] == "open"
    market_calendar_df.loc[open_mask, "openingHour"] = data["stockMarketHours"][
        "openingHour"
    ]
    market_calendar_df.loc[open_mask, "closingHour"] = data["stockMarketHours"][
        "closingHour"
    ]

    half_mask = market_calendar_df["marketStatus"] == "half"
    market_calendar_df.loc[half_mask, "openingHour"] = data["stockMarketHours"][
        "openingHour"
    ]
    market_calendar_df.loc[half_mask, "closingHour"] = "01:00 p.m. ET"

    market_calendar_df.loc[open_mask, "preMarket"] = "4:00am - 9:30am ET"
    market_calendar_df.loc[open_mask, "postMarket"] = "4:00pm - 8:00pm ET"

    market_calendar_df["break"] = 0
    market_calendar_df["country"] = "USA"

    market_calendar_df["stockExchange"] = data["stockExchangeName"]

    market_calendar_df["url"] = "https://site.financialmodelingprep.com/developer/docs/"

    market_calendar_df.fillna(0, inplace=True)
    # market_calendar_df["openingHour"].fillna("0", inplace=True)
    # market_calendar_df["openingHour"].fillna("0", inplace=True)
    # market_calendar_df["openingHour"].fillna("0", inplace=True)

    print("print")

    saveDataToDatabase(
        market_calendar_df,
        "Temp_MarketCalendar",
        [
            "dtDate",
            "marketStatus",
            "openingHour",
            "closingHour",
            "preMarket",
            "postMarket",
            "[break]",
            "country",
            "stockExchange",
            "url",
        ],
        "Exec prcGetUpdateMarketCalendarData",
    )
