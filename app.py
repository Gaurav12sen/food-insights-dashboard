"""
OpenFoodFacts India Dashboard - Professional Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Tuple

from src.data_fetch import fetch_all_products
from src.etl import products_to_df, save_processed_data
from src.analysis import (
    get_summary_stats,
    top_brands,
    nutrient_distribution,
    category_analysis,
    get_healthiest_products,
    get_additive_prevalence,
    get_data_quality_metrics
)
from src.visuals import (
    plot_bar,
    plot_histogram,
    plot_scatter,
    plot_sunburst,
    plot_box,
    create_gauge_chart
)

# Page configuration
st.set_page_config(
    page_title="OpenFoodFacts India Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_custom_css():
    """Load custom CSS for professional styling"""
    st.markdown("""
    <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Main container styling */
        .main {
            padding: 0rem 2rem;
            font-family: 'Inter', sans-serif;
        }
        
        /* Header styling */
        .dashboard-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .dashboard-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        
        .dashboard-subtitle {
            font-size: 1.2rem;
            font-weight: 300;
            text-align: center;
            opacity: 0.9;
        }
        
        .last-updated {
            font-size: 0.9rem;
            text-align: center;
            margin-top: 1rem;
            opacity: 0.8;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            font-weight: 500;
        }
        
        .metric-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: #f8f9fa;
            padding-top: 2rem;
        }
        
        .sidebar-logo {
            text-align: center;
            margin-bottom: 2rem;
            font-size: 2rem;
        }
        
        .filter-section {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .filter-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #2c3e50;
        }
        
        /* Chart containers */
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .chart-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2c3e50;
        }
        
        /* Section headers */
        .section-header {
            display: flex;
            align-items: center;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }
        
        .section-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        
        .section-title {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2c3e50;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* Health gauge */
        .health-gauge {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }
        
        /* Tip banner */
        .tip-banner {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            text-align: center;
            font-weight: 500;
        }
        
        /* Data table styling */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main {
                padding: 0rem 1rem;
            }
            
            .dashboard-title {
                font-size: 2rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Data loading with caching
@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    """Load and cache data with automatic refresh"""
    data_file = Path("data/processed/openfoodfacts_india.csv")
    
    if not data_file.exists() or (
        datetime.fromtimestamp(data_file.stat().st_mtime) < 
        datetime.now() - timedelta(days=1)
    ):
        with st.spinner("🔄 Fetching fresh data from OpenFoodFacts..."):
            raw_data = fetch_all_products(max_pages=50)
            df = products_to_df(raw_data)
            save_processed_data(df, data_file)
    else:
        df = pd.read_csv(data_file)
    
    return df

def create_metric_card(title: str, value: str, icon: str, delta: Optional[str] = None) -> None:
    """Create a professional metric card"""
    delta_html = f'<span style="color: #27ae60; font-size: 0.8rem; margin-top: 0.2rem;">{delta}</span>' if delta else ""
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div style="font-size: 2rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem;">{value}</div>
                <div style="font-size: 0.9rem; color: #7f8c8d; font-weight: 500;">{title}</div>
                {delta_html}
            </div>
            <div style="font-size: 1.5rem; margin-left: 1rem;">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_gauge_chart(value: float, title: str) -> go.Figure:
    """Create a gauge chart for health metrics"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 16}},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 50], 'color': "#ffebee"},
                {'range': [50, 80], 'color': "#fff3e0"},
                {'range': [80, 100], 'color': "#e8f5e8"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_header() -> None:
    """Create the dashboard header"""
    last_updated = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-title">🍽️ OpenFoodFacts India Analytics</div>
        <div class="dashboard-subtitle">Comprehensive insights into food products across India</div>
        <div class="last-updated">Last updated: {last_updated}</div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar(df: pd.DataFrame) -> Tuple[List[str], List[str], Tuple[float, float]]:
    """Create sidebar with filters and branding"""
    
    # Sidebar logo
    st.sidebar.markdown('<div class="sidebar-logo">🍽️</div>', unsafe_allow_html=True)
    st.sidebar.markdown("### Filters & Controls")
    
    # Brand filter
    with st.sidebar.expander("🏷️ Brand Selection", expanded=True):
        brands = sorted(df['brands'].dropna().unique())
        selected_brands = st.multiselect(
            "Choose brands to analyze:",
            brands,
            default=[],
            help="Select specific brands or leave empty for all brands"
        )
    
    # Category filter
    with st.sidebar.expander("📊 Category Selection", expanded=True):
        categories = sorted(df['categories'].dropna().unique())
        selected_categories = st.multiselect(
            "Choose categories to analyze:",
            categories,
            default=[],
            help="Select specific categories or leave empty for all categories"
        )
    
    # Nutrient score filter
    with st.sidebar.expander("🎯 Nutrient Score Range", expanded=True):
        min_score = float(df['nutrient_score'].min())
        max_score = float(df['nutrient_score'].max())
        score_range = st.slider(
            "Select nutrient score range:",
            min_score,
            max_score,
            (min_score, max_score),
            help="Filter products by their nutrient score"
        )
    
    # Reset filters button
    if st.sidebar.button("🔄 Reset All Filters"):
        st.experimental_rerun()
    
    # Feedback form
    with st.sidebar.expander("📝 Feedback", expanded=False):
        st.text_input("Your email (optional):", placeholder="user@example.com")
        st.text_area("Comments & suggestions:", placeholder="Help us improve...")
        st.button("Submit Feedback")
    
    return selected_brands, selected_categories, score_range

def create_tip_banner(df: pd.DataFrame) -> None:
    """Create a tip banner with actionable insights"""
    # Get a random insight
    insights = [
        f"💡 {df['categories'].value_counts().index[0]} has the most products ({df['categories'].value_counts().iloc[0]} items)",
        f"🍯 Average sugar content is {df['sugars_100g'].mean():.1f}g per 100g",
        f"🧂 {(df['salt_100g'] > 1.5).sum()} products exceed WHO salt recommendations",
        f"🏆 {df['brands'].value_counts().index[0]} leads with {df['brands'].value_counts().iloc[0]} products"
    ]
    
    import random
    tip = random.choice(insights)
    
    st.markdown(f"""
    <div class="tip-banner">
        <strong>💡 Daily Insight:</strong> {tip}
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Load custom CSS
    load_custom_css()
    
    # Load data
    try:
        df = load_data()
        if df.empty:
            st.error("❌ No data available. Please check your internet connection and try again.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()
    
    # Create header
    create_header()
    
    # Create sidebar filters
    selected_brands, selected_categories, score_range = create_sidebar(df)
    
    # Apply filters
    mask = pd.Series(True, index=df.index)
    if selected_brands:
        mask &= df['brands'].isin(selected_brands)
    if selected_categories:
        mask &= df['categories'].isin(selected_categories)
    mask &= df['nutrient_score'].between(*score_range)
    
    filtered_df = df[mask]
    
    # Display tip banner
    create_tip_banner(filtered_df)
    
    # Key Metrics Section
    st.markdown("## 📊 Key Performance Indicators")
    st.markdown("---")

    # Calculate stats
    stats = get_summary_stats(filtered_df)

    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Products",
            value=f"{stats['total_products']:,}",
            delta=None,
            help="Total number of products in the database"
        )

    with col2:
        st.metric(
            label="Unique Brands",
            value=f"{stats['unique_brands']:,}",
            delta=None,
            help="Number of distinct brands"
        )

    with col3:
        st.metric(
            label="Avg Nutrient Score",
            value=f"{stats['avg_nutrient_score']:.1f}",
            delta=None,
            help="Average nutritional score across all products"
        )

    with col4:
        st.metric(
            label="Data Quality",
            value=f"{stats['data_completeness']:.1f}%",
            delta=None,
            help="Overall data completeness score"
        )

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Health Gauge
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🏥</span>
        <span class="section-title">Data Health Overview</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        health_score = stats['data_completeness']
        gauge_fig = create_gauge_chart(health_score, "Data Completeness Score")
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    with col2:
        # Create a donut chart for category distribution
        cat_counts = filtered_df['categories'].value_counts().head(10)
        donut_fig = px.pie(
            values=cat_counts.values,
            names=cat_counts.index,
            title="Top 10 Categories Distribution",
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        donut_fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False
        )
        st.plotly_chart(donut_fig, use_container_width=True)
    
    # Brand Analysis
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🏆</span>
        <span class="section-title">Brand Performance Analysis</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Get top brands data
        top_brands_df = top_brands(filtered_df).head(15)
        
        # Debug print
        st.write("Debug - DataFrame columns:", top_brands_df.columns.tolist())
        st.write("Debug - DataFrame head:", top_brands_df.head())
        
        # Create bar chart
        brand_fig = px.bar(
            data_frame=top_brands_df,
            x='product_count',
            y='brand',
            orientation='h',
            title="Top 15 Brands by Product Count",
            color='product_count',
            color_continuous_scale='viridis'
        )
        brand_fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(brand_fig, use_container_width=True)
    
    with col2:
        st.download_button(
            "📥 Download Brand Data",
            top_brands_df.to_csv(index=False),
            "brand_analysis.csv",
            "text/csv"
        )
        
        # Show brand statistics
        st.markdown("### Brand Statistics")
        st.metric("Total Brands", len(filtered_df['brands'].unique()))
        st.metric("Top Brand Share", f"{(top_brands_df.iloc[0]['product_count'] / len(filtered_df) * 100):.1f}%")
        st.metric("Top 5 Brands Share", f"{(top_brands_df.head(5)['product_count'].sum() / len(filtered_df) * 100):.1f}%")
    
    # Nutrient Analysis
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🧬</span>
        <span class="section-title">Nutritional Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nutrient_options = {
            'Sugars (g/100g)': 'sugars_100g',
            'Fat (g/100g)': 'fat_100g',
            'Salt (g/100g)': 'salt_100g',
            'Proteins (g/100g)': 'proteins_100g'
        }
        
        selected_nutrient_display = st.selectbox(
            "Select nutrient to analyze:",
            list(nutrient_options.keys())
        )
        
        nutrient_col = nutrient_options[selected_nutrient_display]
        
        # Create histogram with KDE
        hist_fig = px.histogram(
            filtered_df.dropna(subset=[nutrient_col]),
            x=nutrient_col,
            nbins=50,
            title=f"Distribution of {selected_nutrient_display}",
            marginal="box",
            color_discrete_sequence=['#667eea']
        )
        hist_fig.update_layout(height=400)
        st.plotly_chart(hist_fig, use_container_width=True)
    
    with col2:
        # Box plot by category
        box_fig = px.box(
            filtered_df.dropna(subset=[nutrient_col, 'categories']),
            x='categories',
            y=nutrient_col,
            title=f"{selected_nutrient_display} by Category",
            color='categories'
        )
        box_fig.update_layout(
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(box_fig, use_container_width=True)
    
    # Category Deep Dive
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📈</span>
        <span class="section-title">Category Performance</span>
    </div>
    """, unsafe_allow_html=True)
    
    cat_analysis = category_analysis(filtered_df)
    
    scatter_fig = px.scatter(
        cat_analysis,
        x='product_count',
        y='nutrient_score',
        size='product_count',
        color='categories',
        title="Category Analysis: Product Count vs Average Nutrient Score",
        hover_data=['categories', 'product_count', 'nutrient_score']
    )
    scatter_fig.update_layout(height=500)
    st.plotly_chart(scatter_fig, use_container_width=True)
    
    # Healthiest Products
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🥇</span>
        <span class="section-title">Top Performing Products</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        healthiest = get_healthiest_products(filtered_df)
        
        # Format the DataFrame without background gradient
        formatted_df = healthiest.style.format({
            'nutrient_score': '{:.1f}',
            'sugars_100g': '{:.1f}g',
            'fat_100g': '{:.1f}g',
            'salt_100g': '{:.1f}g'
        })
        
        # Display with custom styling
        st.dataframe(
            formatted_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        st.download_button(
            "📥 Download Healthiest Products",
            healthiest.to_csv(index=False),
            "healthiest_products.csv",
            "text/csv"
        )
        
        # Health insights
        st.markdown("### Health Insights")
        st.metric("Best Score", f"{healthiest['nutrient_score'].min():.1f}")
        st.metric("Avg Sugar", f"{healthiest['sugars_100g'].mean():.1f}g")
        st.metric("Avg Salt", f"{healthiest['salt_100g'].mean():.1f}g")
    
    # Additives Analysis
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🧪</span>
        <span class="section-title">Additives Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        additives_df = get_additive_prevalence(filtered_df)
        
        if not additives_df.empty:
            additive_fig = px.bar(
                additives_df.head(15),
                x='percentage',
                y='additive',
                orientation='h',
                title="Most Common Additives (Top 15)",
                color='percentage',
                color_continuous_scale='Reds'
            )
            additive_fig.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(additive_fig, use_container_width=True)
        else:
            st.info("No additives data available for the selected filters.")
    except Exception as e:
        st.warning(f"Additives analysis unavailable: {str(e)}")
    
    # Data Quality Dashboard
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔍</span>
        <span class="section-title">Data Quality Assessment</span>
    </div>
    """, unsafe_allow_html=True)
    
    quality_metrics = get_data_quality_metrics(filtered_df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🎯 Completeness Score",
            f"{quality_metrics['completeness_score']:.1f}%"
        )
    
    with col2:
        st.metric(
            "🖼️ Products with Images",
            f"{quality_metrics['products_with_images']:.1f}%"
        )
    
    with col3:
        st.metric(
            "🔍 Duplicate Products",
            f"{quality_metrics['duplicate_products']:,}"
        )
    
    # Missing values visualization
    missing_vals = pd.DataFrame([
        {'Field': k, 'Missing_Percentage': v}
        for k, v in quality_metrics['missing_values'].items()
    ])
    
    if not missing_vals.empty:
        missing_fig = px.bar(
            missing_vals.sort_values('Missing_Percentage', ascending=True),
            x='Missing_Percentage',
            y='Field',
            orientation='h',
            title="Missing Values by Field (%)",
            color='Missing_Percentage',
            color_continuous_scale='Oranges'
        )
        missing_fig.update_layout(height=400)
        st.plotly_chart(missing_fig, use_container_width=True)
    
    # Download Section
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📥</span>
        <span class="section-title">Data Export</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📊 Download Filtered Dataset",
            filtered_df.to_csv(index=False).encode('utf-8'),
            "openfoodfacts_filtered.csv",
            "text/csv",
            key='download-main'
        )
    
    with col2:
        st.download_button(
            "📈 Download Summary Report",
            pd.DataFrame([stats]).to_csv(index=False).encode('utf-8'),
            "summary_report.csv",
            "text/csv",
            key='download-summary'
        )
    
    with col3:
        st.download_button(
            "🔍 Download Quality Metrics",
            pd.DataFrame([quality_metrics]).to_csv(index=False).encode('utf-8'),
            "quality_metrics.csv",
            "text/csv",
            key='download-quality'
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 2rem;">
        <p>Built with ❤️ using Streamlit | Data sourced from OpenFoodFacts</p>
        <p>© 2024 OpenFoodFacts India Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()