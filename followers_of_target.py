import pandas as pd
import networkx as nx
import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
import shutil


def get_followers_of_target(target, df):
    df_followers_of_target = df[df.Target == target]
    return df_followers_of_target

def visualize_followers_of_target(target, df):
    G = nx.from_pandas_edgelist(df, 'Follower', 'Target', create_using=nx.DiGraph())

    pos = nx.circular_layout(G)

    # Create a Pyvis network
    net = Network(notebook=False, width="100%", height="900px", directed=True)
    net.toggle_hide_edges_on_drag(False)
    net.toggle_physics(True)

    for node in G.nodes:
        size = 35 if node == target else 25  # Increase the size for better visibility
        color = '#FF9999' if node == target else '#4169E1'  # Light blue color for regular nodes
        border_color = '#00008B'  # Dark blue border for contrast
        title = f"ID: {node}"  # The title will be shown on hover
        net.add_node(node, label=str(node), x = pos[node][0]*1000, y=pos[node][1]*1000, size=size, color=color, title=title, borderWidth=2, borderColor=border_color, font={'size': 14, 'color': '#000000'})

    for edge in G.edges:
        net.add_edge(edge[0], edge[1], width=0.5)  # Keep edges thin

    # Use hierarchical layout to potentially improve the clarity
    net.set_options("""
    {
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 100,
          "springConstant": 0.01,
          "nodeDistance": 120,
          "damping": 0.09
        },
        "minVelocity": 0.75,
        "solver": "hierarchicalRepulsion"
      },
      "nodes": {
        "scaling": {
          "label": {
            "enabled": true
          }
        }
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "layout": {
        "hierarchical": {
          "enabled": false,
          "levelSeparation": 150,
          "nodeSpacing": 100,
          "treeSpacing": 200,
          "blockShifting": true,
          "edgeMinimization": true,
          "parentCentralization": true,
          "direction": "DU", 
          "sortMethod": "directed" 
        }
      }
    }
    """)

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    
    # Generate the network in the temporary file
    net.save_graph(temp_file.name)

    return temp_file.name

def run(df):

    data = df

    st.subheader("Visualize All Followers of a Target User")
    
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
            df_filtered = get_followers_of_target(user_id, data)
            temp_file_path = visualize_followers_of_target(user_id, df_filtered)
            
            # Read from the temporary file
            with open(temp_file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
                components.html(source_code, width=700, height=800)

            # Clean up: delete the temporary file
            os.remove(temp_file_path)
            shutil.rmtree('lib')

if __name__ == "__main__":
    run()