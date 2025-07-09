"""
Module for creating interactive visualizations.
"""

import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd

# Custom color palette
COLORS = px.colors.qualitative.Set3

def plot_bar(df: pd.DataFrame, x: str, y: str, title: str = None) -> go.Figure:
    """
    Create a bar chart using Plotly.
    
    Args:
        df (pd.DataFrame): Data to plot
        x (str): Column name for x-axis
        y (str): Column name for y-axis
        title (str, optional): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Validate column names
    if x not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame. Available columns: {df.columns.tolist()}")
    if y not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame. Available columns: {df.columns.tolist()}")
    
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLORS
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def plot_histogram(df: pd.DataFrame, column: str, title: str = None) -> go.Figure:
    """
    Create a histogram using Plotly.
    
    Args:
        df (pd.DataFrame): Data to plot
        column (str): Column name to plot
        title (str, optional): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=title,
        color_discrete_sequence=COLORS
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def plot_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str = None,
    size: str = None,
    title: str = None
) -> go.Figure:
    """
    Create a scatter plot using Plotly.
    
    Args:
        df (pd.DataFrame): Data to plot
        x (str): Column name for x-axis
        y (str): Column name for y-axis
        color (str, optional): Column name for color encoding
        size (str, optional): Column name for size encoding
        title (str, optional): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        title=title,
        color_discrete_sequence=COLORS
    )
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def plot_sunburst(df: pd.DataFrame, path: List[str], title: str = None) -> go.Figure:
    """
    Create a sunburst chart using Plotly.
    
    Args:
        df (pd.DataFrame): Data to plot
        path (List[str]): List of columns defining the hierarchy
        title (str, optional): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.sunburst(
        df,
        path=path,
        title=title,
        color_discrete_sequence=COLORS
    )
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def plot_box(df: pd.DataFrame, x: str, y: str, title: str = None) -> go.Figure:
    """
    Create a box plot using Plotly.
    
    Args:
        df (pd.DataFrame): Data to plot
        x (str): Column name for x-axis (categories)
        y (str): Column name for y-axis (values)
        title (str, optional): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.box(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLORS
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_gauge_chart(
    value: float,
    title: str,
    min_val: float = 0,
    max_val: float = 10
) -> go.Figure:
    """
    Create a gauge chart using Plotly.
    
    Args:
        value (float): Value to display
        title (str): Chart title
        min_val (float): Minimum value
        max_val (float): Maximum value
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': COLORS[0]},
            'steps': [
                {'range': [min_val, max_val/3], 'color': "lightgray"},
                {'range': [max_val/3, 2*max_val/3], 'color': "gray"},
                {'range': [2*max_val/3, max_val], 'color': "darkgray"}
            ]
        }
    ))
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig 