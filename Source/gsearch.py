import streamlit as st
from googlesearch import search

def google_search():
    st.header("Google Search")

    # Input box for the search query
    query = st.text_input("Enter your search query:", "")
    
    if query:
        num_results = st.slider("Select the number of results to display:", 1, 10, 5)
        
        # Perform the search
        results = []
        try:
            results = list(search(query, num_results=num_results))
        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Display the search results
        if results:
            st.write(f"Top {num_results} search results for query '{query}':")
            for idx, result in enumerate(results, start=1):
                st.write(f"**Result {idx}:**")
                st.write(f"[{result}]({result})")
        else:
            st.write("No results found.")
