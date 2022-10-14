import time
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def stage_data():
    # Load in the data to a list of JSON object
    t_start_data = time.time()
    print(f'Beginning Data Staging.')

    # Set up for data staging
    eia_file = 'https://api.eia.gov/bulk/STEO.zip'
    staged_data = []
    staged_data_name = []

    # Point to the unzipped file that we want to read
    with ZipFile(BytesIO(urlopen(eia_file).read())) as f:
        # Loop through each row and append the JSON object to a list
        for idx, line in enumerate(f.open(f.namelist()[0])):
            # Add single row JSON object to list
            row_data = json.loads(line.decode('utf-8'))
            # Collect the names of the rows that have the 'name' key
            if 'name' in row_data.keys():
                staged_data_name.append(row_data['name'])
                staged_data.append(row_data)
            else:
                pass
        staged_data_name = pd.Series(staged_data_name)
    print(f'Completed Data Staging in {(time.time() - t_start_data):.2f}')
    return staged_data, staged_data_name


def filter_to_name_df(name, staged_data_name, staged_data):
    name_index = staged_data_name[staged_data_name == name].index[0]
    data = pd.DataFrame(staged_data[name_index])
    print(data)
    data_corrected = pd.DataFrame(data['data'].tolist(), columns=['c.date', 'c.val'])
    print(data_corrected)
    data = data.join(data_corrected)
    return data


def create_wti_monthly_chart(staged_data_name, staged_data):
    name = 'West Texas Intermediate Crude Oil Price, Monthly'
    df = filter_to_name_df(name, staged_data_name, staged_data)
    df['c.date'] = pd.to_datetime(df['c.date'], format='%Y%m')

    fig, ax = plt.subplots(figsize=[10,4])
    ax.plot(df['c.date'], df['c.val'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax.set(xlabel='Date', ylabel='WTI Crude Oil Price, Monthly \n [bbl/d]')
    plt.title('WTI Crude Oil Price History (Monthly Basis)')
    return fig

