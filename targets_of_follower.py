import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def get_targets_of_follower(follower, df):
    df = df[df.Follower == follower]
    return df

def visualize_targets_of_follower(target, df):
    G = nx.from_pandas_edgelist(df, source='Follower', target='Target', create_using=nx.DiGraph())
    nx.draw(G, with_labels=True, node_size=1000, alpha=0.5, arrows=True)
    plt.title('Followers of user with id {}'.format(target))
    st.write(df)
    return plt

def run(df):
    return

if __name__ == "__main__":
    run()