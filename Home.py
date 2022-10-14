import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from assets.data_staging import *

if __name__ == '__main__':
    # Stage data
    staged_data, staged_data_name = stage_data()

    # Set streamlit title
    st.title('US-EIA Web App')

    option = st.selectbox(
        'Which data series are you interested in?',
        np.sort(staged_data_name)
    )

    fig = create_wti_monthly_chart(staged_data_name, staged_data)

    st.pyplot(fig)


