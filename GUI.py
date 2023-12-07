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
    # Set page config
    st.set_page_config(page_title="Network Analysis Tool", layout="wide")
    
    # Initialize the Streamlit app
    st.title("Friendship/Followship Network Analysis Tool")

    # Create a sidebar menu for model selection
    with st.sidebar:
        
        # Model selection
        st.markdown("## Analysis Options")
        selected_model = st.selectbox("Select an Analysis", 
                                      ["Visualize Followers of a Target User", 
                                       "Visualize Targets a User Follows", 
                                       "Bidirectional View of a User", 
                                       "Global Statistics of the Network"], index=None, key="model_selection")
        
        # Data source selection
        st.markdown("## Data Source")
        dataset_choice = st.radio("Choose your data source:", 
                                  ["Upload CSV", "Use Default Dataset"], index=None, key="data_source_selection")
        
    if dataset_choice == "Upload CSV":
        user_file_path = st.sidebar.file_uploader("Upload a CSV file", type="csv")
        
        if user_file_path is not None:
            if 'df' not in st.session_state or st.session_state['uploaded_file'] != user_file_path:
                load_data(user_file_path)
                st.session_state['uploaded_file'] = user_file_path

    elif dataset_choice == "Use Default Dataset":
        default_file_path = 'Twitter-dataset/data/edges.csv'
        if 'df' not in st.session_state:
            load_data(default_file_path)
    
    # Main area for content
    with st.container():
        # Check if the data is loaded and then pass it to the selected model
        if 'df' in st.session_state:
            df = st.session_state['df']

            if selected_model == "Visualize Followers of a Target User":
                fot.run(df)
            elif selected_model == "Visualize Targets a User Follows":
                tof.run(df)
            elif selected_model == "Bidirectional View of a User":
                bv.run(df)
            elif selected_model == "Global Statistics of the Network":
                gs.run(df)
        else:
            st.error("Please select a data source to proceed")

if __name__ == "__main__":
    main()
