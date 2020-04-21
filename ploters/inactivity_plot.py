import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from dateutil import relativedelta


if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'activity_serie.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # let's transform the date
    df['unixDate'] = pd.to_datetime(df['unixDate'], unit='s').dt.date
    df = df.rename(columns={'unixDate': 'date'})
    # transform to monthly date
    df['date'] = df['date'].apply(lambda d: d.replace(day=1))

    # remove unused cols
    df = df.drop(columns=['actionType', 'userId'])

    # get now date
    now_date = datetime.now().replace(day=1)

    