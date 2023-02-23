from datetime import timedelta
import database.transactionsBT as db


def generate_quarters(start_date, end_date):
    quarters = []

    current_quarter_start = start_date

    while current_quarter_start < end_date:
        current_quarter_end = current_quarter_start + timedelta(days=89)
        if current_quarter_end > end_date:
            current_quarter_end = end_date
        quarters.append(
            {
                "from": current_quarter_start.strftime("%Y-%m-%d"),
                "to": current_quarter_end.strftime("%Y-%m-%d"),
            }
        )
        current_quarter_start = current_quarter_end + timedelta(days=1)
    return quarters


def saveDataToDatabase(df, tableName, columnNames, procedure):
    try:
        data = [tuple(row) for row in df.to_numpy()]
        placeholders = ", ".join(["%s"] * len(columnNames))
        sql_query = f"INSERT INTO {tableName} ({', '.join(columnNames)}) VALUES ({placeholders})"
        db.fncSaveDataMany(sql_query, data)
        db.fncUpdateData(procedure)
    except Exception as e:
        raise (e)
