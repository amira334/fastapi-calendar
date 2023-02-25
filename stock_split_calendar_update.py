import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase


api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
stock_split_url = "https://financialmodelingprep.com/api/v3/stock_split_calendar"


start_date = date.today()
end_date = (datetime.now() + timedelta(days=365)).strftime("%Y, %m, %d")
end_date = date(
    int(end_date.split(", ")[0]),
    int(end_date.split(", ")[1]),
    int(end_date.split(", ")[2]),
)

quarters = generate_quarters(start_date, end_date)


def stockSplitCalenarUpdate():
    stock_split_df = pd.DataFrame(
        columns=["date", "label", "symbol", "numerator", "denominator"]
    )

    for quarter in quarters:
        params = {"from": quarter["from"], "to": quarter["to"], "apikey": api_key}

        # stock split
        response = requests.get(stock_split_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        stock_split_df = pd.concat([stock_split_df, data_df], ignore_index=True)

    stock_split_df["url"] = "https://site.financialmodelingprep.com/developer/docs/"

    # stock split
    stock_split_df["date"] = pd.to_datetime(stock_split_df["date"])
    stock_split_df = stock_split_df.sort_values(by=["date"])
    stock_split_df["date"] = stock_split_df["date"].dt.strftime("%Y-%m-%d")
    stock_split_df = stock_split_df.drop_duplicates(
        subset=["date", "symbol"], keep="first"
    )
    stock_split_calender = stock_split_df.drop_duplicates(
        subset=["symbol"], keep="last"
    )

    # stock_split_calender.to_csv("stockSplitCalender.csv", index=False)

    stock_split_calender["numerator"].fillna(0.0, inplace=True)
    stock_split_calender["denominator"].fillna(0.0, inplace=True)

    saveDataToDatabase(
        stock_split_calender,
        "Temp_StockSplitCalendar",
        ["dtDate", "label", "SymName", "numerator", "denominator", "url"],
        "Exec prcGetUpdateStockSplitData",
    )


#
