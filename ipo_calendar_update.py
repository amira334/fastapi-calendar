import requests
from datetime import date, timedelta, datetime
import pandas as pd
from util import generate_quarters, saveDataToDatabase

api_key = "2b2bbacbc149bcba58903f591ae3d3c8"
ipo_url = "https://financialmodelingprep.com/api/v3/ipo_calendar"
ipo_prospectus_url = "https://financialmodelingprep.com/api/v4/ipo-calendar-prospectus"
ipo_confirmed_url = "https://financialmodelingprep.com/api/v4/ipo-calendar-confirmed"

start_date = date.today()
end_date = (datetime.now() + timedelta(days=365)).strftime("%Y, %m, %d")
end_date = date(
    int(end_date.split(", ")[0]),
    int(end_date.split(", ")[1]),
    int(end_date.split(", ")[2]),
)

quarters = generate_quarters(start_date, end_date)


def ipoCalenarUpdate():
    ipo_df = pd.DataFrame(
        columns=[
            "date",
            "company",
            "symbol",
            "exchange",
            "actions",
            "shares",
            "priceRange",
            "marketCap",
        ]
    )
    ipo_prospectus_df = pd.DataFrame(
        columns=[
            "symbol",
            "cik",
            "form",
            "filingDate",
            "acceptedDate",
            "effectivenessDate",
            "ipoDate",
            "pricePublicPerShare",
            "pricePublicTotal",
            "discountsAndCommissionsPerShare",
            "discountsAndCommissionsTotal",
            "proceedsBeforeExpensesPerShare",
            "proceedsBeforeExpensesTotal",
            "url",
        ]
    )
    ipo_confirmed_df = pd.DataFrame(
        columns=[
            "symbol",
            "cik",
            "form",
            "filingDate",
            "acceptedDate",
            "effectivenessDate",
            "url",
        ]
    )

    for quarter in quarters:
        params = {"from": quarter["from"], "to": quarter["to"], "apikey": api_key}

        # ipo
        response = requests.get(ipo_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        ipo_df = pd.concat([ipo_df, data_df], ignore_index=True)

        # ipo prospectus
        response = requests.get(ipo_prospectus_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        ipo_prospectus_df = pd.concat([ipo_prospectus_df, data_df], ignore_index=True)

        # ipo confirmed
        response = requests.get(ipo_confirmed_url, params=params)
        data = response.json()
        data_df = pd.DataFrame(data)
        ipo_confirmed_df = pd.concat([ipo_confirmed_df, data_df], ignore_index=True)

    # ipo
    ipo_df["date"] = pd.to_datetime(ipo_df["date"])
    ipo_df = ipo_df.sort_values(by=["date"])
    ipo_df["date"] = ipo_df["date"].dt.strftime("%Y-%m-%d")
    ipo_df = ipo_df.drop_duplicates(subset=["date", "symbol"], keep="first")
    ipo_df = ipo_df.drop_duplicates(subset=["symbol"], keep="last")

    # ipo prospectus
    ipo_prospectus_df["filingDate"] = pd.to_datetime(ipo_prospectus_df["filingDate"])
    ipo_prospectus_df = ipo_prospectus_df.sort_values(by=["filingDate"])
    ipo_prospectus_df["filingDate"] = ipo_prospectus_df["filingDate"].dt.strftime(
        "%Y-%m-%d"
    )
    ipo_prospectus_df = ipo_prospectus_df.drop_duplicates(
        subset=["cik", "symbol", "filingDate", "acceptedDate"], keep="first"
    )
    ipo_prospectus_df = ipo_prospectus_df.drop_duplicates(
        subset=["symbol"], keep="last"
    )
    ipo_prospectus_df = ipo_prospectus_df.drop("url", axis=1)

    # ipo confirmed
    ipo_confirmed_df["filingDate"] = pd.to_datetime(ipo_confirmed_df["filingDate"])
    ipo_confirmed_df = ipo_confirmed_df.sort_values(by=["filingDate"])
    ipo_confirmed_df["filingDate"] = ipo_confirmed_df["filingDate"].dt.strftime(
        "%Y-%m-%d"
    )
    ipo_confirmed_df = ipo_confirmed_df.drop_duplicates(
        subset=["cik", "symbol", "filingDate", "acceptedDate"], keep="first"
    )
    ipo_confirmed_df = ipo_confirmed_df.drop_duplicates(subset=["symbol"], keep="last")

    # merge ipo confirmed and prospectus data
    merge_confimred_prospectus_df = ipo_prospectus_df.merge(
        ipo_confirmed_df, on=["symbol", "cik"]
    )

    # merge ipo
    ipo_calendar = ipo_df.merge(merge_confimred_prospectus_df, on=["symbol"])

    ipo_calendar["url"] = "https://site.financialmodelingprep.com/developer/docs/"

    ipo_calendar["shares"].fillna(0.0, inplace=True)
    ipo_calendar["marketCap"].fillna(0.0, inplace=True)
    ipo_calendar["pricePublicPerShare"].fillna(0.0, inplace=True)
    ipo_calendar["pricePublicTotal"].fillna(0.0, inplace=True)
    ipo_calendar["discountsAndCommissionsPerShare"].fillna(0.0, inplace=True)
    ipo_calendar["discountsAndCommissionsTotal"].fillna(0.0, inplace=True)
    ipo_calendar["proceedsBeforeExpensesPerShare"].fillna(0.0, inplace=True)
    ipo_calendar["proceedsBeforeExpensesTotal"].fillna(0.0, inplace=True)

    saveDataToDatabase(
        ipo_calendar,
        "Temp_ipoCalendar",
        [
            "dtDate",
            "company",
            "SymName",
            "exchange",
            "actions",
            "shares",
            "priceRange",
            "marketCap",
            "cik",
            "formStock",
            "filingDate",
            "acceptedDate",
            "effectivenessDate",
            "ipoDate",
            "pricePublicPerShare",
            "pricePublicTotal",
            "discountsAndCommissionsPerShare",
            "discountsAndCommissionsTotal",
            "proceedsBeforeExpensesPerShare",
            "proceedsBeforeExpensesTotal",
            "form",
            "confirmedFilingDate",
            "confirmedAcceptedDate",
            "confirmedEffectivenessDate",
            "url",
        ],
        "Exec prcGetUpdateipoCalendarData",
    )


# ipo_calendar.to_csv("ipoCalenderUpdate.csv", index=False)
