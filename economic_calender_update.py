import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase


api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
economic_url = "https://financialmodelingprep.com/api/v3/economic_calendar"


start_date = date.today()
end_date = (datetime.now() + timedelta(days=365)).strftime("%Y, %m, %d")
end_date = date(
    int(end_date.split(", ")[0]),
    int(end_date.split(", ")[1]),
    int(end_date.split(", ")[2]),
)

quarters = generate_quarters(start_date, end_date)


def economicCalenarUpdate():
    economic_df = pd.DataFrame(
        columns=[
            "event",
            "date",
            "country",
            "actual",
            "previous",
            "change",
            "changePercentage",
            "estimate",
            "impact",
        ]
    )

    for quarter in quarters:
        params = {"from": quarter["from"], "to": quarter["to"], "apikey": api_key}

        # earnings
        response = requests.get(economic_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        economic_df = pd.concat([economic_df, data_df], ignore_index=True)

    economic_df["url"] = "https://site.financialmodelingprep.com/developer/docs/"

    # earnings
    economic_df["date"] = pd.to_datetime(economic_df["date"])
    economic_df = economic_df.sort_values(by=["date"])
    economic_df["date"] = economic_df["date"].dt.tz_localize(None)
    economic_calendar = economic_df.drop_duplicates(
        subset=["event", "date", "country"], keep="first"
    )
    # economic_calendar = economic_df.drop_duplicates(subset=["symbol"], keep="last")

    # economic_calendar.to_csv("economicCalender.csv", index=False)

    economic_calendar["actual"].fillna(0.0, inplace=True)
    economic_calendar["previous"].fillna(0.0, inplace=True)
    economic_calendar["change"].fillna(0.0, inplace=True)
    economic_calendar["changePercentage"].fillna(0.0, inplace=True)
    economic_calendar["estimate"].fillna(0.0, inplace=True)

    saveDataToDatabase(
        economic_calendar,
        "Temp_EconomicCalendar",
        [
            "event",
            "dtDate",
            "country",
            "actual",
            "previous",
            "change",
            "changePercentage",
            "estimate",
            "impact",
            "url",
        ],
        "Exec prcGetUpdateEconomicData",
    )
