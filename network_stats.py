import pandas as pd
import numpy as np
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from multiprocessing import Pool

def most_active_followers(df, range_of_interest):
    # Calculate most active followers in the Network
    follower_freq = df.Follower.value_counts().rename_axis('Follower').reset_index(name='Frequency')
    
    # Calculate the statistics of the most active followers
    stats = follower_freq.Frequency.describe()

    plt.figure(figsize=(14, 8))

    bin_edges = np.logspace(np.log10(follower_freq['Frequency'].min()), np.log10(follower_freq['Frequency'].max()))
    plt.hist(follower_freq['Frequency'], bins=bin_edges, color='skyblue', edgecolor='black')

    # Set the scale of the x-axis and y-axis to logarithmic to handle the wide range of values.
    plt.xscale('log')
    plt.yscale('log')

    # Adding a title and labels
    plt.title('Log-Scale Distribution of "Following" Count', fontsize=20)
    plt.xlabel('Follower Count', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)

    # Customizing the tick marks and grid lines for better readability
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Make sure everything fits without overlapping
    plt.tight_layout()

    return follower_freq[0:range_of_interest], stats, plt

def most_followed_targets(df, range_of_interest):
    # Calculate most followed targets in the Network
    target_count = df.Target.value_counts().rename_axis('Target').reset_index(name='Frequency')

    # Calculate the statistics of the most followed targets
    stats = target_count.Frequency.describe()

    plt.figure(figsize=(14, 8))

    bin_edges = np.logspace(np.log10(target_count['Frequency'].min()), np.log10(target_count['Frequency'].max()))
    plt.hist(target_count['Frequency'], bins=bin_edges, color='skyblue', edgecolor='black')

    # Set the scale of the x-axis and y-axis to logarithmic to handle the wide range of values.
    plt.xscale('log')
    plt.yscale('log')

    # Adding a title and labels
    plt.title('Log-Scale Distribution of "Target" Count', fontsize=20)
    plt.xlabel('Target Count', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)

    # Customizing the tick marks and grid lines for better readability
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Make sure everything fits without overlapping
    plt.tight_layout()

    return target_count[0:range_of_interest], stats, plt

def create_subgraph(edges_list):
    return nx.from_pandas_edgelist(edges_list, 'Follower', 'Target', create_using=nx.DiGraph())

def get_pagerank(df, range_of_interest):

    data = df

    # Splitting the DataFrame into chunks for parallel processing
    df_split = np.array_split(data, 4)

    # Create a pool of processes
    with Pool(4) as pool:
        # Create subgraphs in parallel
        subgraphs = pool.map(create_subgraph, df_split)

    # Combine subgraphs into a single graph
    G = nx.DiGraph()
    for sg in subgraphs:
        G = nx.compose(G, sg)

    # Calculate the pagerank
    pagerank = nx.pagerank(G, alpha=0.85, max_iter=100, tol=1e-06)

    # Process the pagerank results
    pagerank_df = pd.DataFrame.from_dict(pagerank, orient='index', columns=['Pagerank'])
    pagerank_df['User ID'] = pagerank_df.index
    pagerank_df.reset_index(drop=True, inplace=False)

    # Get the top nodes efficiently
    top_pagerank_df = pagerank_df.nlargest(range_of_interest, 'Pagerank')

    return top_pagerank_df

def get_degree_centrality(df, range_of_interest):
    G = nx.from_pandas_edgelist(df, 'Follower', 'Target', create_using=nx.DiGraph())
    degree_centrality = nx.degree_centrality(G)

    # Convert to DataFrame
    degree_centrality_df = pd.DataFrame.from_dict(degree_centrality, orient='index', columns=['DegreeCentrality'])
    degree_centrality_df['User'] = degree_centrality_df.index
    degree_centrality_df.reset_index(drop=True, inplace=False)

    # Get the top nodes
    top_degree_centrality_df = degree_centrality_df.nlargest(range_of_interest, 'DegreeCentrality')

    return top_degree_centrality_df

def get_hits_scores(df, range_of_interest):
    # Create a graph from the dataframe
    G = nx.from_pandas_edgelist(df, 'Follower', 'Target', create_using=nx.DiGraph())

    # Compute the HITS algorithm
    hubs, authorities = nx.hits(G, max_iter=100, tol=1e-08)

    # Convert to DataFrames
    hubs_df = pd.DataFrame.from_dict(hubs, orient='index', columns=['HubScore'])
    authorities_df = pd.DataFrame.from_dict(authorities, orient='index', columns=['AuthorityScore'])

    # Reset index to have the user column
    hubs_df['User'] = hubs_df.index
    authorities_df['User'] = authorities_df.index

    hubs_df.reset_index(drop=True, inplace=False)
    authorities_df.reset_index(drop=True, inplace=False)

    # Get the top nodes by hub score and authority score
    top_hubs_df = hubs_df.nlargest(range_of_interest, 'HubScore')
    top_authorities_df = authorities_df.nlargest(range_of_interest, 'AuthorityScore')

    return top_hubs_df, top_authorities_df

def run(df):

    data = df

    # Display Global Statistics of the Network
    st.subheader("**Global Statistics of the Network**")

    # Sidebar for user input
    st.subheader("Settings")
    range_of_interest = st.slider("Select Range of Interest", 1, 100, 10)


    # Buttons for each metric
    if st.button("Show Most Active Followers"):
        with st.spinner("Calculating Most Active Followers..."):
            active_followers, stats_followers, plot_followers = most_active_followers(data, range_of_interest)
            st.write(f"### Top {range_of_interest} Most Active Followers")
            st.dataframe(active_followers)
            st.write("### Statistical Summary of Following Count")
            st.dataframe(stats_followers)
            st.markdown(f"**A follower has an average of {stats_followers['mean']} targets**")
            st.pyplot(plot_followers)

    if st.button("Show Most Followed Targets"):
        with st.spinner("Calculating Most Followed Targets..."):
            followed_targets, stats_targets, plot_targets = most_followed_targets(data, range_of_interest)
            st.write(f"### Top {range_of_interest} Most Followed Targets")
            st.dataframe(followed_targets)
            st.write("### Statistical Summary of Target Count")
            st.dataframe(stats_targets)
            st.markdown(f"**A target has an average of {stats_targets['mean']} followers**")
            st.pyplot(plot_targets)

    if st.button("Show Degree Centrality"):
        with st.spinner("Calculating Degree Centrality..."):
            degree_centrality = get_degree_centrality(data, range_of_interest)
            st.write(f"### Top {range_of_interest} Influential Users by Degree Centrality")
            st.dataframe(degree_centrality)
    
    if st.button("Show HITS Scores"):
        with st.spinner("Calculating HITS Scores..."):
            top_hubs, top_authorities = get_hits_scores(data, range_of_interest)
            st.write(f"### Top {range_of_interest} Hubs")
            st.dataframe(top_hubs)
            st.write(f"### Top {range_of_interest} Authorities")
            st.dataframe(top_authorities)

    if st.button("Show PageRank"):
        with st.spinner("Calculating PageRank..."):
            pagerank = get_pagerank(data, range_of_interest)
            st.write(f"### Top {range_of_interest} Influential Users by PageRank")
            st.dataframe(pagerank)


if __name__ == "__main__":
    run()