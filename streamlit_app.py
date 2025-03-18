"""
MaLDReTH Streamlit Application

This Streamlit application visualizes the MaLDReTH (Mapping the Landscape of Digital 
Research Tools Harmonised) framework, developed by the Research Data Alliance to help 
researchers navigate the complex ecosystem of digital tools used throughout the research data lifecycle.

Author: MaLDReTH Project
Date: March 17, 2025
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import json
import plotly.graph_objects as go
from pathlib import Path
import base64

# Page configuration
st.set_page_config(
    page_title="MaLDReTH - Research Data Lifecycle",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
@st.cache_resource
def get_connection():
    """Create a connection to the SQLite database."""
    # Check if running on Streamlit Cloud and use resources folder
    if os.path.exists("resources/research_data_lifecycle.db"):
        db_path = "resources/research_data_lifecycle.db"
    else:
        db_path = "research_data_lifecycle.db"
        
    # Initialize database if it doesn't exist
    if not os.path.exists(db_path):
        init_database(db_path)
        
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_database(db_path):
    """Initialize the database with schema and sample data."""
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    
    # Read schema SQL
    schema_path = "resources/schema.sql"
    if not os.path.exists(schema_path):
        st.error(f"Schema file not found at {schema_path}")
        return
    
    with open(schema_path, 'r') as f:
        schema_script = f.read()
    
    # Execute schema script
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_script)
    
    # Import tool data if available
    if os.path.exists("resources/tools.csv"):
        import_tool_data(db_path, "resources/tools.csv")

def import_tool_data(db_path, csv_path):
    """Import tool data from CSV file."""
    try:
        df = pd.read_csv(csv_path)
        with sqlite3.connect(db_path) as conn:
            # Process each row and insert into appropriate tables
            # This is a simplified version - adjust according to your CSV structure
            for _, row in df.iterrows():
                stage_name = row.get('RESEARCH DATA LIFECYCLE STAGE', '').strip()
                category_name = row.get('TOOL CATEGORY TYPE', '').strip()
                description = row.get('DESCRIPTION (1 SENTENCE)', '').strip()
                tools = row.get('EXAMPLES', '').strip()
                
                if not stage_name or not category_name:
                    continue
                
                # Get stage ID
                cursor = conn.execute("SELECT id FROM stages WHERE name = ?", (stage_name,))
                stage = cursor.fetchone()
                if not stage:
                    continue
                stage_id = stage[0]
                
                # Insert category
                conn.execute(
                    "INSERT INTO tool_categories (stage_id, name, description) VALUES (?, ?, ?)",
                    (stage_id, category_name, description)
                )
                category_id = cursor.lastrowid
                
                # Insert tools
                for tool_name in tools.split(','):
                    tool_name = tool_name.strip()
                    if tool_name:
                        conn.execute(
                            "INSERT INTO tools (category_id, name, description) VALUES (?, ?, ?)",
                            (category_id, tool_name, f"Example tool for {category_name}")
                        )
    except Exception as e:
        st.error(f"Error importing tool data: {e}")

# Data loading functions
@st.cache_data
def load_stages():
    """Load all lifecycle stages from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stages ORDER BY order_index")
    return [dict(row) for row in cursor.fetchall()]

@st.cache_data
def load_connections():
    """Load all connections between lifecycle stages."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM connections")
    return [dict(row) for row in cursor.fetchall()]

@st.cache_data
def load_tool_categories(stage_id=None):
    """Load tool categories, optionally filtered by stage."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if stage_id:
        cursor.execute("SELECT * FROM tool_categories WHERE stage_id = ? ORDER BY name", (stage_id,))
    else:
        cursor.execute("SELECT * FROM tool_categories ORDER BY stage_id, name")
    
    return [dict(row) for row in cursor.fetchall()]

@st.cache_data
def load_tools(category_id=None):
    """Load tools, optionally filtered by category."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if category_id:
        cursor.execute("SELECT * FROM tools WHERE category_id = ? ORDER BY name", (category_id,))
    else:
        cursor.execute("SELECT * FROM tools ORDER BY category_id, name")
    
    return [dict(row) for row in cursor.fetchall()]

@st.cache_data
def search_tools(query):
    """Search for tools by name or description."""
    if not query:
        return []
        
    conn = get_connection()
    cursor = conn.cursor()
    search_pattern = f"%{query}%"
    
    cursor.execute("""
        SELECT t.*, c.name as category_name, s.name as stage_name,
               c.id as category_id, s.id as stage_id
        FROM tools t
        JOIN tool_categories c ON t.category_id = c.id
        JOIN stages s ON c.stage_id = s.id
        WHERE t.name LIKE ? OR t.description LIKE ?
        ORDER BY s.order_index, c.name, t.name
    """, (search_pattern, search_pattern))
    
    return [dict(row) for row in cursor.fetchall()]

# Visualization functions
def create_lifecycle_visualization(stages, connections, selected_stage=None):
    """Create a circular visualization of the research data lifecycle."""
    # Create a circular layout
    n_stages = len(stages)
    angles = [i * 2 * 3.14159 / n_stages for i in range(n_stages)]
    
    # Set radius
    radius = 1
    
    # Calculate stage positions
    x_positions = [radius * 0.8 * -1 * (-1) ** (i % 2) for i in range(n_stages)]
    y_positions = [radius * (-1) ** (i % 2) for i in range(n_stages)]
    
    # Create figure
    fig = go.Figure()
    
    # Add connections
    for conn in connections:
        from_id = conn['from_stage_id'] - 1  # Adjust for 0-based indexing
        to_id = conn['to_stage_id'] - 1
        
        if from_id < n_stages and to_id < n_stages:
            # Calculate line style based on connection type
            line_style = dict(color='rgba(120, 120, 120, 0.6)', width=1)
            if conn['connection_type'] == 'alternative':
                line_style['dash'] = 'dash'
            
            # Add the connection line
            fig.add_trace(go.Scatter(
                x=[x_positions[from_id], x_positions[to_id]],
                y=[y_positions[from_id], y_positions[to_id]],
                mode='lines',
                line=line_style,
                showlegend=False,
                hoverinfo='none'
            ))
    
    # Add stage nodes
    for i, stage in enumerate(stages):
        # Determine color based on selection
        if selected_stage and stage['id'] == selected_stage:
            color = 'rgba(90, 159, 23, 1)'  # Darker green for selected
            size = 30
        else:
            color = 'rgba(122, 193, 66, 0.8)'  # Regular green
            size = 25
        
        # Add the stage node
        fig.add_trace(go.Scatter(
            x=[x_positions[i]],
            y=[y_positions[i]],
            mode='markers+text',
            marker=dict(size=size, color=color),
            text=stage['name'],
            textposition="middle center",
            name=stage['name'],
            customdata=[stage['id']],
            hovertemplate="%{text}<br>%{hovertext}<extra></extra>",
            hovertext=stage['description']
        ))
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=600,
        width=800
    )
    
    return fig

# App sections
def render_header():
    """Render the application header."""
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Display logo
        if os.path.exists("resources/maldreth-logo.svg"):
            with open("resources/maldreth-logo.svg", "r") as f:
                svg = f.read()
                b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
                html = f'<img src="data:image/svg+xml;base64,{b64}" width="100px">'
                st.markdown(html, unsafe_allow_html=True)
        else:
            # Fallback if logo not found
            st.markdown("🔄")
    
    with col2:
        st.title("MaLDReTH: Research Data Lifecycle")
        st.markdown("### Mapping the Landscape of Digital Research Tools")

def render_search():
    """Render the search section."""
    query = st.text_input("Search for tools:", placeholder="Enter tool name...")
    if query:
        results = search_tools(query)
        if results:
            st.subheader(f"Search Results for '{query}'")
            
            # Group results by stage
            results_by_stage = {}
            for result in results:
                stage_name = result['stage_name']
                if stage_name not in results_by_stage:
                    results_by_stage[stage_name] = []
                results_by_stage[stage_name].append(result)
            
            # Display results by stage
            for stage_name, tools in results_by_stage.items():
                with st.expander(f"{stage_name} ({len(tools)} tools)", expanded=True):
                    df = pd.DataFrame([{
                        'Tool': tool['name'], 
                        'Category': tool['category_name'], 
                        'Description': tool.get('description', '')
                    } for tool in tools])
                    st.dataframe(df, use_container_width=True)
        else:
            st.info(f"No tools found matching '{query}'")

def render_visualization():
    """Render the lifecycle visualization section."""
    st.header("Research Data Lifecycle Visualization")
    
    stages = load_stages()
    connections = load_connections()
    
    # Get selected stage from URL params or sidebar
    params = st.experimental_get_query_params()
    selected_stage_id = params.get('stage', [None])[0]
    
    if selected_stage_id:
        selected_stage_id = int(selected_stage_id)
    else:
        selected_stage_id = None
    
    # Create and display visualization
    fig = create_lifecycle_visualization(stages, connections, selected_stage_id)
    st.plotly_chart(fig, use_container_width=True)
    
    # Instructions
    st.markdown("**Click on a stage to explore its tool categories**")
    
    # Handle click events (this is approximated in Streamlit)
    # For selected stage, show its details and tool categories
    if selected_stage_id:
        selected_stage = next((s for s in stages if s['id'] == selected_stage_id), None)
        if selected_stage:
            st.subheader(f"Selected Stage: {selected_stage['name']}")
            st.markdown(selected_stage['description'])
            
            # Get categories for this stage
            categories = load_tool_categories(selected_stage_id)
            
            # Display categories and tools
            if categories:
                for category in categories:
                    with st.expander(f"{category['name']}", expanded=True):
                        st.markdown(f"*{category['description']}*")
                        
                        # Get tools for this category
                        tools = load_tools(category['id'])
                        if tools:
                            st.markdown("**Example Tools:**")
                            for tool in tools:
                                st.markdown(f"- {tool['name']}")
                        else:
                            st.markdown("*No example tools available*")
            else:
                st.markdown("*No tool categories defined for this stage*")

def render_all_tools():
    """Render the complete tools section."""
    st.header("Tool Categories by Lifecycle Stage")
    
    stages = load_stages()
    
    # Add stage selector
    selected_stage = st.selectbox(
        "Filter by stage:",
        ["All Stages"] + [stage['name'] for stage in stages]
    )
    
    # Filter by stage if needed
    if selected_stage == "All Stages":
        # Show all stages
        for stage in stages:
            with st.expander(f"{stage['name']}", expanded=False):
                st.markdown(f"*{stage['description']}*")
                
                # Get categories for this stage
                categories = load_tool_categories(stage['id'])
                
                if categories:
                    for category in categories:
                        st.markdown(f"**{category['name']}**")
                        st.markdown(f"*{category['description']}*")
                        
                        # Get tools for this category
                        tools = load_tools(category['id'])
                        if tools:
                            cols = st.columns(3)
                            for i, tool in enumerate(tools):
                                cols[i % 3].markdown(f"- {tool['name']}")
                        else:
                            st.markdown("*No example tools available*")
                else:
                    st.markdown("*No tool categories defined for this stage*")
    else:
        # Show only the selected stage
        stage = next((s for s in stages if s['name'] == selected_stage), None)
        if stage:
            st.markdown(f"*{stage['description']}*")
            
            # Get categories for this stage
            categories = load_tool_categories(stage['id'])
            
            if categories:
                for category in categories:
                    st.markdown(f"**{category['name']}**")
                    st.markdown(f"*{category['description']}*")
                    
                    # Create an expandable section for tools
                    with st.expander("Example Tools", expanded=True):
                        # Get tools for this category
                        tools = load_tools(category['id'])
                        if tools:
                            for tool in tools:
                                st.markdown(f"- {tool['name']}")
                        else:
                            st.markdown("*No example tools available*")
            else:
                st.markdown("*No tool categories defined for this stage*")

def render_about():
    """Render the about section."""
    st.header("About MaLDReTH")
    
    st.markdown("""
    **MaLDReTH** (Mapping the Landscape of Digital Research Tools Harmonised) is a comprehensive framework 
    developed by the Research Data Alliance (RDA) to help researchers, data managers, and tool developers 
    navigate the complex ecosystem of digital tools used throughout the research data lifecycle.
    
    ### Project Goals
    
    - Provide a unified approach to understanding and categorizing research tools
    - Make it easier for researchers to find the right tools for their specific needs
    - Help tool developers understand the ecosystem and identify integration opportunities
    - Support the development of the national and international open research commons
    
    ### Who Benefits
    
    - **Researchers** seeking appropriate tools for each stage of their research
    - **Data support professionals** providing guidance on tool selection
    - **Tool developers** understanding gaps and interoperability needs
    - **Research organizations** making informed recommendations about research tools
    - **Publishers** guiding authors on data management tools
    - **Funders** assessing data management plans
    
    ### About the Research Data Lifecycle
    
    The research data lifecycle consists of 12 interconnected stages, each representing a critical phase 
    in the research process:
    
    1. **Conceptualise**: Formulating research ideas and defining data requirements
    2. **Plan**: Creating structured frameworks for research project management
    3. **Fund**: Acquiring financial resources to support the research project
    4. **Collect**: Gathering reliable, high-quality data
    5. **Process**: Preparing data for analysis through cleaning and structuring
    6. **Analyse**: Deriving insights and knowledge from processed data
    7. **Store**: Securely recording data while maintaining integrity
    8. **Publish**: Making research data available with appropriate metadata
    9. **Preserve**: Ensuring long-term data safety and accessibility
    10. **Share**: Making data available to humans and machines
    11. **Access**: Controlling and managing data access
    12. **Transform**: Creating new data from original sources
    
    ### Project Team
    
    This project is maintained by the Research Data Alliance (RDA) and Oracle for Research 
    "Mapping the Landscape of Digital Research Tools" Working Group.
    """)

def main():
    """Main function to run the Streamlit application."""
    # CSS customization
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #5a9f17;
    }
    .stExpander {
        border-left: 2px solid #7ac142;
    }
    .css-1adrfps {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Search", "Lifecycle Visualization", "Tool Categories", "About"]
    )
    
    # Render header
    render_header()
    
    # Render selected page
    if page == "Search":
        render_search()
    elif page == "Lifecycle Visualization":
        render_visualization()
    elif page == "Tool Categories":
        render_all_tools()
    elif page == "About":
        render_about()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "© 2025 MaLDReTH Project. Licensed under [CC-BY 4.0 International](https://creativecommons.org/licenses/by/4.0/)."
    )

if __name__ == "__main__":
    main()
