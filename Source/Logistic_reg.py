import pandas as pd
import streamlit as st
import io

def Log_reg():
    if "data" not in st.session_state:
        st.session_state.data = None

    st.header("Welcome to the Aakash Smart Machine Learning Model Building ToolBox.")

    with st.container(border = True):

        st.session_state.data = st.file_uploader("Upload your data file. (Please upload a CSV file.)")

        if st.session_state.data:
            data = pd.read_csv(st.session_state.data)
            st.dataframe(data)

            # Capture the output of data.info()
            buffer = io.StringIO()
            data.info(buf=buffer)
            info_str = buffer.getvalue()

            # Display the captured info as text
            st.header("Data Information")
            st.text(info_str)

            st.dataframe(data.describe())

            X_features = st.multiselect("Select the Features you want to keep for training the machine learning",
                        data.columns)

            if X_features:
                X = data[X_features]

                st.write("This are the features you have selected for training your machine learning model.")
                st.dataframe(X)
            
                y_feature = st.selectbox("Select the target variable for which you want to predict", data.columns)

                if y_feature:
                    y = data[y_feature]

                    st.write("This is the target feature for your machine learning model.")
                    st.dataframe(y)

                    category_cols = st.multiselect("Select the features that you think are categorical. After Selecting they will be one-hot coded.",
                                                X_features)
                    
                    dummies = None                
                    for i in category_cols:
                        dummies = pd.get_dummies(data[i], prefix=i, drop_first = True)
                        X.drop([i], axis = 1, inplace = True)
                        X = pd.concat([X, dummies], axis = 1)
                    
                    st.write("Your Features after One-hot encoding.")
                    st.dataframe(X)

                    st.write("It's time to break data into training and testing set.")
                    test_size = st.slider("Select the test size", 0.05, 0.9)

                    if test_size:
                        from sklearn.model_selection import train_test_split

                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

                        from sklearn.linear_model import LogisticRegression

                        model = LogisticRegression()

                        model.fit(X_train, y_train)

                        y_pred = model.predict(X_test)

                        from sklearn.metrics import accuracy_score, confusion_matrix

                        st.write(f"Accuracy Score: {accuracy_score(y_true = y_test, y_pred = y_pred)}")
                        
                        conf_mat = confusion_matrix(y_true = y_test, y_pred = y_pred)

                        info = """
    Confusion Matrix

                                Predicted
                        Positive        Negative
        Actual  Positive     TP        FN
                Negative     FP        TN

                

    """

                        st.markdown(info)
                        st.write(conf_mat)