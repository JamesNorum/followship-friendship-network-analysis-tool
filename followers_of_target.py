import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def get_followers_of_target(target, df):
    df = df[df.Target == target]
    return df

def visualize_followers_of_target(target, df):
    G = nx.from_pandas_edgelist(df, source='Follower', target='Target', create_using=nx.DiGraph())
    plt.figure(figsize=(10, 6))  # Create a new figure
    nx.draw(G, with_labels=True, node_size=1000, alpha=0.5, arrows=True)
    plt.title('Followers of user with id {}'.format(target))
    st.write(df)
    return plt.gcf()  # Get the current figure

def run(df):

    df1 = df

    st.title("Visualize the Followers of A Target")
    
    user_input = st.text_area('Enter targets user id')
    
    valid_input = False
    try:
        user_id = int(user_input)
        if 1 <= user_id <= 11316811:
            valid_input = True
        else:
            st.error("User ID must be between 1 and 11316811.")
    except ValueError:
        st.error("Please enter a valid integer as User ID.")
    
    if st.button('Visualize'):
        df2 = get_followers_of_target(user_id, df1)
        plot = visualize_followers_of_target(user_id, df2)  # Corrected this line
        st.pyplot(plot)  # Display the matplotlib plot

if __name__ == "__main__":
    run()