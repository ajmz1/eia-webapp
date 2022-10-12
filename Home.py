import streamlit as st
import os
import pandas as pd
import json


if __name__ == '__main__':
    # Set streamlit title
    st.title('US-EIA Web App')

    # Change file path to access bulk data
    file_bulk_data = os.path.join(os.getcwd(), 'assets/STEO.txt')
    # Quick test of file path
    st.write(file_bulk_data)

    # Allocate data (should write this to parquet file later
    data = []
    with open(file_bulk_data) as f:
        for idx, line in enumerate(f):
            data.append(json.loads(line))

    # Export the first series of data to page
    df = pd.DataFrame.from_dict(data[0])
    st.dataframe(df)

    # Prove that we are still in the root path
    st.write(os.getcwd())
