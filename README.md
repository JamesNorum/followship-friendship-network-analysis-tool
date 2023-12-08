
# Network Analysis Tool

## Overview
This Network Analysis Tool is designed to provide insights into social media networks or similar datasets. It features interactive visualization and analysis of network relationships, focusing on followers, targets, and bidirectional views.

## Features
- **Bidirectional View**: Analyze and visualize the network relationship from both perspectives of a specific user.
- **Followers of Target**: Explore and visualize the followers of a particular target user.
- **Targets of Follower**: Examine and visualize the targets a specific follower is following.
- **Network Statistics**: Provides statistical analysis of the network, such as the most active followers, most followed targets, PageRank, Degree Centrality, and HITS Scores.
- **Interactive GUI**: User-friendly web interface built with Streamlit, enabling easy interaction with the tool's features.

## Installation
To set up the tool, ensure you have Python installed on your system. Then, follow the steps below:



Run the following command to create a virtual environment:
```bash
python -m venv venv
```

```bash
```

```bash
pip install requirements.txt
```

## Usage
To run the application, navigate to the directory containing the scripts and execute the following command:

```bash
streamlit run GUI.py
```

This will start a local web server and open the tool in your default web browser.

## Data Format
The tool expects data in a specific format, representing a network of followership or friendship. Ensure your dataset conforms to the required format before uploading it for analysis.

## Contributing
Contributions to the project are welcome. Please fork the repository, make your changes, and submit a pull request for review.
