# File: visualizations.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from translations import get_text

def get_current_language():
    return st.session_state.get('language', 'en')

def create_inventory_plot(history_df, policy_history):
    lang = get_current_language()
    
    # Create continuous policy lines
    days = list(range(len(history_df)))
    rp_values = [next((p['rp'] for p in reversed(policy_history) if p['day'] <= day), 
                     policy_history[0]['rp']) for day in days]
    max_values = [next((p['max_point'] for p in reversed(policy_history) if p['day'] <= day), 
                      policy_history[0]['max_point']) for day in days]

    traces = [
        go.Scatter(x=history_df['day'], y=history_df['stock'], 
                  name=get_text('current_stock', lang), line=dict(color='royalblue', width=2)),
        go.Scatter(x=history_df['day'], y=history_df['virtual_stock'], 
                  name=get_text('virtual_stock', lang), line=dict(color='mediumseagreen', width=2)),
        go.Scatter(x=history_df['day'], y=history_df['demand'], 
                  name=get_text('demand', lang), line=dict(color='firebrick', width=2)),
        go.Scatter(x=days, y=rp_values, 
                  name=get_text('reorder_point', lang), line=dict(color='orange', width=2, dash='dash')),
        go.Scatter(x=days, y=max_values, 
                  name=get_text('maximum_stock', lang), line=dict(color='purple', width=2, dash='dash'))
    ]

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=get_text('inventory_levels', lang),
        xaxis_title=get_text('day', lang),
        yaxis_title=get_text('units', lang),
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        hovermode='x unified'
    )

    return fig

def create_lead_time_demand_plot(history_df, lead_time):
    lang = get_current_language()
    
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=[
            get_text('lead_time_analysis', lang),
            get_text('lead_time_distribution', lang)
        ],
        vertical_spacing=0.5
    )
    
    mean_demand = history_df['grouped_demand'].mean()
    std_demand = history_df['grouped_demand'].std()
    
    # Add traces and statistics
    traces = [
        #(go.Scatter(x=history_df['day'], y=history_df['demand'],
        #           name=get_text('daily_demand', lang), line=dict(color='red', width=1)), 1, 1),
        (go.Scatter(x=history_df['day'], y=history_df['grouped_demand'],
                   name=f"{get_text('lead_time_analysis', lang)} ({lead_time} {get_text('day', lang)}s)", 
                   line=dict(color='blue')), 1, 1),
        (go.Histogram(x=history_df['grouped_demand'],
                     name=get_text('lead_time_distribution', lang),
                     nbinsx=20, marker_color='blue'), 2, 1)
    ]
    
    for trace, row, col in traces:
        fig.add_trace(trace, row=row, col=col)
    
    # Add statistical lines
    stats = [
        (mean_demand, "dash", "green", f"{get_text('mean', lang)}: {mean_demand:.1f}"),
        (mean_demand + std_demand, "dot", "orange", f"+1 {get_text('std_dev', lang)}: {(mean_demand + std_demand):.1f}"),
        (mean_demand - std_demand, "dot", "orange", f"-1 {get_text('std_dev', lang)}: {(mean_demand - std_demand):.1f}"),
        (mean_demand + 2*std_demand, "dot", "orange", f"+2 {get_text('std_dev', lang)}: {(mean_demand + 2*std_demand):.1f}"),
        (mean_demand - 2*std_demand, "dot", "orange", f"-2 {get_text('std_dev', lang)}: {(mean_demand - 2*std_demand):.1f}")

    ]
    
    for value, dash, color, text in stats:
        fig.add_hline(y=value, line_dash=dash, line_color=color,
                     annotation_text=text, row=1, col=1)
    
    fig.update_layout(height=600)
    
    return fig