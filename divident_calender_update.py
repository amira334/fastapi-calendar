import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase


api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
divident_url = "https://financialmodelingprep.com/api/v3/stock_dividend_calendar"


start_date = date.today()
end_date = (datetime.now() + timedelta(days=365)).strftime("%Y, %m, %d")
end_date = date(
    int(end_date.split(", ")[0]),
    int(end_date.split(", ")[1]),
    int(end_date.split(", ")[2]),
)

quarters = generate_quarters(start_date, end_date)


def dividentCalenarUpdate():
    divident_df = pd.DataFrame(
        columns=[
            "date",
            "label",
            "adjDividend",
            "symbol",
            "dividend",
            "recordDate",
            "paymentDate",
            "declarationDate",
        ]
    )
    for quarter in quarters:
        params = {"from": quarter["from"], "to": quarter["to"], "apikey": api_key}

        # divident
        response = requests.get(divident_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        divident_df = pd.concat([divident_df, data_df], ignore_index=True)

    divident_df["url"] = "https://site.financialmodelingprep.com/developer/docs/"

    # divident
    divident_df["date"] = pd.to_datetime(divident_df["date"])
    divident_df = divident_df.sort_values(by=["date"])
    divident_df["date"] = divident_df["date"].dt.strftime("%Y-%m-%d")
    divident_df = divident_df.drop_duplicates(
        subset=["date", "symbol", "recordDate", "paymentDate"], keep="first"
    )
    divident_calendar = divident_df.drop_duplicates(subset=["symbol"], keep="last")

    # divident_calendar.to_csv("dividentCalender.csv", index=False)

    divident_calendar["dtDate"].fillna(0, inplace=True)
    divident_calendar["label"].fillna(0, inplace=True)
    divident_calendar["adjDividend"].fillna(0.0, inplace=True)
    divident_calendar["dividend"].fillna(0.0, inplace=True)
    divident_calendar["SymName"].fillna(0, inplace=True)
    divident_calendar["recordDate"].fillna(0, inplace=True)
    divident_calendar["paymentDate"].fillna(0, inplace=True)
    divident_calendar["declarationDate"].fillna(0, inplace=True)
    divident_calendar["url"].fillna(0, inplace=True)

    saveDataToDatabase(
        divident_calendar,
        "Temp_Divident_Calendar",
        [
            "dtDate",
            "label",
            "adjDividend",
            "SymName",
            "dividend",
            "recordDate",
            "paymentDate",
            "declarationDate",
            "url",
        ],
        "Exec prcGetUpdateDividentCalendarData",
    )
