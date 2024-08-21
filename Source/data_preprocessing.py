import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def automatic_data_processing(df):
    # Identifying numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=[object]).columns

    # Handling missing values
    if len(numeric_cols) > 0:
        num_imputer = SimpleImputer(strategy='mean')
        df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

    if len(categorical_cols) > 0:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

    # One-Hot Encoding with drop_first=True
    df = pd.get_dummies(df, drop_first=True)

    # Scaling only the numeric columns
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

def preprocess_data():
    st.header("Aakash Smart Data Preprocessing Tool")
    
    # File uploader for the dataset
    uploaded_file = st.file_uploader("Upload your data file (CSV format).")
    
    if uploaded_file:
        # Load the data
        data = pd.read_csv(uploaded_file)
        
        # Perform automatic data processing on the entire dataset
        processed_data = automatic_data_processing(data)

        # Display processed data
        st.subheader("Processed Data")
        st.dataframe(processed_data)

        # Provide a download button for the processed data
        processed_csv = processed_data.to_csv(index=False)
        st.download_button(
            label="Download Processed Data", 
            data=processed_csv, 
            file_name='processed_data.csv', 
            mime='text/csv'
        )

preprocess_data()
