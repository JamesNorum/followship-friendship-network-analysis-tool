import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
import plotly.graph_objects as go

def get_targets_user_follows(follower, df):
    df_targets_user_follows = df[df.Follower == follower]
    return df_targets_user_follows

def visualize_targets_user_follows(target, df):
    G = nx.from_pandas_edgelist(df, 'Follower', 'Target', create_using=nx.DiGraph())

    pos = nx.spring_layout(G)

    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_traces.append(go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                                      mode='lines',
                                      line=dict(width=1, color='rgba(50,50,50,0.5)'), # Make lines darker
                                      hoverinfo='none'))

    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=[50 if node == target else 25 for node in G.nodes()], # Larger size for the target node
            color=[1 if node == target else 0 for node in G.nodes()], # Different color for the target node
            colorscale=['#888', '#888'], # Grayscale colors
            line=dict(width=2, color='DarkSlateGrey')))

    # Set hover text to node IDs
    node_text = [f'ID: {node}' for node in G.nodes()]
    node_trace.text = node_text

    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title=f"Targets that User with ID: {target} follows",
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # Adding arrow annotations for directed edges
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        # Adjusting the arrow position to not overlap with the node
        adjust = 0.01  # increase adjust factor for better visibility
        ax = x0 + (x1 - x0) * adjust
        ay = y0 + (y1 - y0) * adjust

        fig.add_annotation(
            x=x1, y=y1,
            ax=ax, ay=ay,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=3, 
            arrowsize=2, 
            arrowwidth=2,
            arrowcolor='DarkSlateGrey' # Use a color that contrasts with the background
        )

    return fig

def run(df):

    data = df

    st.subheader("Visualize Who a Target User Follows")
    
    user_input = st.text_area('Enter Target Users ID')

    # Clean user_input
    user_input = user_input.strip()
    
    # Check if user_input is valid
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
        with st.spinner('Generating Visualization...'):
            df_filtered = get_targets_user_follows(user_id, data)
            plot = visualize_targets_user_follows(user_id, df_filtered) 
            st.plotly_chart(plot) # Display the matplotlib plot

if __name__ == "__main__":
    run()