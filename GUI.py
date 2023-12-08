import streamlit as st
import pandas as pd
import bidirectional_view_of_user as bv
import followers_of_target as fot
import targets_of_follower as tof
import network_stats as ns

def load_data(file):
    # This function loads the data from the uploaded file
    with st.spinner("Loading dataset..."):
        df = pd.read_csv(file, header=None, names=['Follower', 'Target'])
        st.session_state['df'] = df
        st.success("Data Loaded Successfully.")

def main():
    # Set page config
    st.set_page_config(page_title="Network Analysis Tool", layout="wide")
    
    # Initialize the Streamlit app
    st.title("Friendship/Followship Network Analysis Tool")

    # Dataset Structure Explanation
    with st.expander("Data Format Information"):
        st.markdown("""
        ### Default Dataset: `edges.csv`
        The default dataset, `edges.csv`, represents a friendship/followership network. 

        ### Basic statistics:
        ```
        Number of Nodes: 11,316,811
        ```
        ```
        Number of Edges: 85,331,846
        ```
        In this dataset, friends or followers are represented as directed edges in the format:
        ```
        Follower,Target
        ```
        For example, an entry `1,2` indicates that the user with ID `1` is following the user with ID `2`.
        
        ### Custom CSV Format
        If you wish to use your own data, please ensure it follows the same format. Each row should represent a directed edge from a follower to a target user. For instance:
        ```
        FollowerID,TargetID
        ```
        """)

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
        
    # Handling data source selection
    if dataset_choice == "Upload CSV":
        user_file_path = st.sidebar.file_uploader("Upload a CSV file", type="csv", key="csv_uploader")
        
        if user_file_path is not None:
            if 'last_uploaded_file' not in st.session_state or st.session_state['last_uploaded_file'] != user_file_path:
                load_data(user_file_path)
                st.session_state['last_uploaded_file'] = user_file_path  

        else:
            # Clear the dataframe from session state if the uploaded file is removed
            if 'df' in st.session_state:
                del st.session_state['df']
            if 'last_uploaded_file' in st.session_state:
                del st.session_state['last_uploaded_file']
            st.error("Please upload a CSV file to proceed")

    elif dataset_choice == "Use Default Dataset":
        default_file_path = 'Twitter-dataset/data/edges.csv'
        if 'default_df' not in st.session_state:
            st.session_state['default_df'] = pd.read_csv(default_file_path, header=None, names=['Follower', 'Target'])
            st.success("Data Loaded Successfully.")

    # Main area for content
    with st.container():
        
        if dataset_choice == "Upload CSV": #and 'df' in st.session_state:
            if 'df' in st.session_state:
                df = st.session_state['df']
                # Check if a model has been selected
                if selected_model is None or selected_model == "":
                    st.warning("Please select an analysis model from the sidebar to proceed.")
                    return
                if selected_model == "Visualize Followers of a Target User":
                    fot.run(df)
                    return
                elif selected_model == "Visualize Targets a User Follows":
                    tof.run(df)
                    return
                elif selected_model == "Bidirectional View of a User":
                    bv.run(df)
                    return
                elif selected_model == "Global Statistics of the Network":
                    ns.run(df)
                    return


        elif dataset_choice == "Use Default Dataset" and 'default_df' in st.session_state:
            df = st.session_state['default_df']
            if selected_model == "Visualize Followers of a Target User":
                fot.run(df)
                return
            elif selected_model == "Visualize Targets a User Follows":
                tof.run(df)
                return
            elif selected_model == "Bidirectional View of a User":
                bv.run(df)
                return
            elif selected_model == "Global Statistics of the Network":
                ns.run(df)
                return

        else:
            st.error("Please select a data source to proceed")
            return

if __name__ == "__main__":
    main()