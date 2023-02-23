import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase


api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
earnings_url = "https://financialmodelingprep.com/api/v3/earning_calendar"
earnings_confirmed_url = (
    "https://financialmodelingprep.com/api/v4/earning-calendar-confirmed"
)

start_date = date.today()
end_date = (datetime.now() + timedelta(days=365)).strftime("%Y, %m, %d")
end_date = date(
    int(end_date.split(", ")[0]),
    int(end_date.split(", ")[1]),
    int(end_date.split(", ")[2]),
)

quarters = generate_quarters(start_date, end_date)


def earningCalenarUpdate():
    earnings_df = pd.DataFrame(
        columns=[
            "date",
            "symbol",
            "eps",
            "epsEstimated",
            "time",
            "revenue",
            "revenueEstimated",
            "updatedFromDate",
            "fiscalDateEnding",
        ]
    )
    earnings_confirmed_df = pd.DataFrame(
        columns=[
            "symbol",
            "exchange",
            "time",
            "when",
            "publicationDate",
            "url",
            "date",
            "title",
        ]
    )

    for quarter in quarters:
        params = {"from": quarter["from"], "to": quarter["to"], "apikey": api_key}

        # earnings
        response = requests.get(earnings_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        earnings_df = pd.concat([earnings_df, data_df], ignore_index=True)

        # earnings confirmed
        response = requests.get(earnings_confirmed_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        earnings_confirmed_df = pd.concat(
            [earnings_confirmed_df, data_df], ignore_index=True
        )

    # earnings
    earnings_df["date"] = pd.to_datetime(earnings_df["date"])
    earnings_df = earnings_df.sort_values(by=["date"])
    earnings_df["date"] = earnings_df["date"].dt.strftime("%Y-%m-%d")
    earnings_df = earnings_df.drop_duplicates(
        subset=["date", "symbol", "eps"], keep="first"
    )
    earnings_df = earnings_df.drop_duplicates(subset=["symbol"], keep="last")

    # earnings confirmed
    earnings_confirmed_df["date"] = pd.to_datetime(earnings_confirmed_df["date"])
    earnings_confirmed_df = earnings_confirmed_df.sort_values(by=["date"])
    earnings_confirmed_df["date"] = earnings_confirmed_df["date"].dt.strftime(
        "%Y-%m-%d"
    )
    earnings_confirmed_df = earnings_confirmed_df.drop_duplicates(
        subset=["symbol", "time", "date"], keep="first"
    )

    earnings_confirmed_df = earnings_confirmed_df.drop_duplicates(
        subset=["symbol"], keep="last"
    )
    earnings_confirmed_df = earnings_confirmed_df.drop(["date", "title"], axis=1)

    # merge earnings and confirmed data
    earnings_calendar = earnings_df.merge(earnings_confirmed_df, on=["symbol"])

    earnings_calendar["url"] = "https://site.financialmodelingprep.com/developer/docs/"

    earnings_calendar["eps"].fillna(0.0, inplace=True)
    earnings_calendar["epsEstimated"].fillna(0.0, inplace=True)
    earnings_calendar["revenue"].fillna(0.0, inplace=True)
    earnings_calendar["revenueEstimated"].fillna(0.0, inplace=True)

    # earnings_calender.to_csv("earningsCalender.csv", index=False)

    saveDataToDatabase(
        earnings_calendar,
        "Temp_EarningsCalendar",
        [
            "dtDate",
            "SymName",
            "eps",
            "epsEstimated",
            "earningCallTime",
            "revenue",
            "revenueEstimated",
            "updatedFromDate",
            "fiscalDateEnding",
            "exchange",
            "time",
            "[when]",
            "publicationDate",
            "url",
        ],
        "Exec prcGetUpdateEarningCalendarData",
    )
