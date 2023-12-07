import streamlit as st
import pandas as pd
import bidirectional_view_of_user as bv
import followers_of_target as fot
import targets_of_follower as tof
import global_stats as gs

def load_data(file_path):
    # This function loads the data and stores it in the session state
    with st.spinner("Loading dataset..."):
        df = pd.read_csv(file_path, header=None, names=['Follower', 'Target'])
        st.session_state['df'] = df
        st.success("Data Loaded Successfully. Please select a model to proceed")

def main():
    # Initialize the Streamlit app
    st.title("Twitter Followship Network Analysis")
    
    # Create a sidebar menu for model selection
    selected_model = st.sidebar.radio("Select a Model", 
                                      ["Visualize Followers of A Target", 
                                       "Visualize Targets of A Follower", 
                                       "Bidirectional View of A User", 
                                       "Global Statistics of the Network"], 
                                      index=None)

    # Option to use a default dataset or upload a file
    dataset_choice = st.radio("Choose your data source:", 
                              ["Upload CSV", "Use Default Dataset"], 
                              index=None)
    
    if dataset_choice == "Upload CSV":
        user_file_path = st.file_uploader("Upload a CSV file", type="csv")
        
        if user_file_path is not None:
            if 'df' not in st.session_state or st.session_state['uploaded_file'] != user_file_path:
                load_data(user_file_path)
                st.session_state['uploaded_file'] = user_file_path

    elif dataset_choice == "Use Default Dataset":
        default_file_path = 'Twitter-dataset\data\edges.csv'
        if 'df' not in st.session_state:
            load_data(default_file_path)

    # Check if the data is loaded and then pass it to the selected model
    if 'df' in st.session_state:
        df = st.session_state['df']

        if selected_model == "Visualize Followers of A Target":
            fot.run(df)
        elif selected_model == "Visualize Targets of A Follower":
            tof.run(df)
        elif selected_model == "Bidirectional View of A User":
            bv.run(df)
        elif selected_model == "Global Statistics of the Network":
            gs.run(df)
    else:
        st.error("Please select a data source to proceed")

if __name__ == "__main__":
    main()
