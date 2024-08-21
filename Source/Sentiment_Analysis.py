import streamlit as st
import pandas as pd
import io
from textblob import TextBlob

def sentiment_analysis():
    if "data" not in st.session_state:
        st.session_state.data = None

    st.header("Welcome to the Aakash Natural Language Processing ToolBox.")

    with st.container():
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

            X_feature = st.selectbox("Select the Feature on which you want to run Sentiment Analysis.",
                        data.columns)

            if X_feature:
                X = data[X_feature]

                if data[X_feature].dtype == "object":
                    st.write("This is the feature you have selected for Sentiment Analysis.")
                    st.dataframe(X)

                    X.dropna(inplace=True)

                    def get_sentiment_polarity(text):
                        statement = TextBlob(text)
                        sentiment = statement.sentiment
                        return sentiment.polarity
                    
                    def get_sentiment_subjectivity(text):
                        statement = TextBlob(text)
                        sentiment = statement.sentiment
                        return sentiment.subjectivity
                                                
                    polarity = X.apply(get_sentiment_polarity)
                    subjectivity = X.apply(get_sentiment_subjectivity)

                    df = pd.DataFrame({'Polarity': polarity, 'Subjectivity': subjectivity})

                    st.dataframe(df)

                    avg_polarity = polarity.mean()
                    avg_subjectivity = subjectivity.mean()

                    st.write(f"**Average Polarity:** {avg_polarity}")
                    st.write(f"**Average Subjectivity:** {avg_subjectivity}")

                    # Interpretation of polarity
                    st.header("Sentiment Interpretation")

                    if avg_polarity > 0.5:
                        st.write(f"The overall sentiment is **Positive** 😄 with a polarity of {avg_polarity:.2f}")
                    elif avg_polarity > 0:
                        st.write(f"The overall sentiment is **Slightly Positive** 🙂 with a polarity of {avg_polarity:.2f}")
                    elif avg_polarity == 0:
                        st.write(f"The overall sentiment is **Neutral** 😐 with a polarity of {avg_polarity:.2f}")
                    elif avg_polarity > -0.5:
                        st.write(f"The overall sentiment is **Slightly Negative** 🙁 with a polarity of {avg_polarity:.2f}")
                    else:
                        st.write(f"The overall sentiment is **Negative** 😠 with a polarity of {avg_polarity:.2f}")

                    # Interpretation of subjectivity
                    if avg_subjectivity > 0.5:
                        st.write(f"The text is **Quite Subjective** with an average subjectivity of {avg_subjectivity:.2f}")
                    elif avg_subjectivity > 0:
                        st.write(f"The text has **Some Subjectivity** with an average subjectivity of {avg_subjectivity:.2f}")
                    else:
                        st.write(f"The text is **Very Objective** with an average subjectivity of {avg_subjectivity:.2f}")
                else:
                    st.warning("The selected feature is not of type 'object' and may not be suitable for sentiment analysis.")
                
