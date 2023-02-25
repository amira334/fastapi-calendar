from fastapi import FastAPI
from divident_calender_update import dividentCalenarUpdate
from earnings_calendar_update import earningCalenarUpdate
from economic_calender_update import economicCalenarUpdate
from ipo_calendar_update import ipoCalenarUpdate
from stock_split_calendar_update import stockSplitCalenarUpdate
from market_update import marketCalendarUpdate

app = FastAPI()


@app.get("/divident-calender-data")
def dividentCalender():
    dividentCalenarUpdate()
    return {"message": "Data fetched and updated successfully"}


@app.get("/earning-calender-data")
def earningCalender():
    earningCalenarUpdate()
    return {"message": "Data fetched and updated successfully"}


@app.get("/economic-calender-data")
def economicCalender():
    economicCalenarUpdate()
    return {"message": "Data fetched and updated successfully"}


@app.get("/ipo-calender-data")
def ipoCalender():
    ipoCalenarUpdate()
    return {"message": "Data fetched and updated successfully"}


@app.get("/stocksplit-calender-data")
def stockSplitCalender():
    stockSplitCalenarUpdate()
    return {"message": "Data fetched and updated successfully"}


@app.get("/market-calender-data")
def marketCalendar():
    marketCalendarUpdate()
    return {"message": "Data fetched and updated successfully"}
