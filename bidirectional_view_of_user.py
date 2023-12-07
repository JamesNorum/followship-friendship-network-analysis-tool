import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def get_followers_of_target(target, df):
    df = df[df.Target == target]
    return df

def get_targets_of_follower(follower, df):
    df = df[df.Follower == follower]
    return df

def bidirectional_view_of_target(user, followers_of_target, targets_of_follower):
    df = pd.concat([targets_of_follower, followers_of_target])
    G = nx.from_pandas_edgelist(df, source='Follower', target='Target', create_using=nx.DiGraph())
    nx.draw_circular(G, with_labels=True, node_size=1000, alpha=0.5, arrows=True)
    plt.title('Birectional view of user with id {}'.format(user))
    st.write(df)
    return plt

def run(df):
    return

if __name__ == "__main__":
    run()