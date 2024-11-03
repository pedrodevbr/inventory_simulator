# File: pages/simulation.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import config_parameters
from game_state import GameState
from utils.visualizations import create_inventory_plot, create_lead_time_demand_plot
from translations import get_text

def format_cost(cost):
    """Format cost with currency symbol and thousand separators"""
    return f"${cost:,.2f}"

def simulation_page():

    lang = st.session_state.get('language', 'en')
    # Title with translation
    st.title(get_text('title', lang))
    
    params = config_parameters()
    # Initialize or get game state
    if 'game_state' not in st.session_state:
        st.session_state.game_state = GameState(params)
     
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(get_text('control_panel', lang))
        
        # Get the current game state
        game_state = st.session_state.game_state
        
        # Reorder point and max stock sliders
        col_rp, col_max = st.columns(2)
        with col_rp:
            new_rp = st.number_input(
                get_text('reorder_point', lang),
                min_value=0,
                max_value=int(game_state.params['initial_stock'] * 2),
                value=game_state.rp
            )
        with col_max:
            new_max = st.number_input(
                get_text('maximum_stock', lang),
                min_value=new_rp,
                max_value=int(game_state.params['initial_stock'] * 3),
                value=game_state.max_point
            )
        
        # Update policy if changed
        game_state.rp = new_rp
        game_state.max_point = new_max
        
        # Advance simulation button
        if st.button(get_text('advance_day', lang)):
            game_state.process_daily_operations()
    
    with col2:
        st.subheader(get_text('current_status', lang))
        
        # Display current metrics
        metrics = {
            get_text('day', lang): game_state.day,
            get_text('current_stock', lang): game_state.current_stock,
            get_text('virtual_stock', lang): game_state.virtual_stock,
        }
        
        # Create three columns for metrics
        metric_cols = st.columns(len(metrics))
        for col, (label, value) in zip(metric_cols, metrics.items()):
            col.metric(label, value)
        
        # Display costs
        st.write(f"### {get_text('costs', lang)}")
        costs = {
            get_text('holding_cost', lang): game_state.holding_costs,
            get_text('purchase_cost', lang): game_state.purchase_costs,
            get_text('shortage_cost', lang): game_state.shortage_costs,
            get_text('total_cost', lang): game_state.total_cost
        }
        
        for label, cost in costs.items():
            st.write(f"{label}: {format_cost(cost)}")
    
    # Create DataFrame from history
    if game_state.history:
        history_df = pd.DataFrame(game_state.history)
        
        # Main inventory plot
        st.subheader(get_text('inventory_levels', lang))
        inventory_fig = create_inventory_plot(history_df, game_state.policy_history)
        st.plotly_chart(inventory_fig, use_container_width=True)
        
        # Lead time demand analysis
        st.subheader(get_text('lead_time_analysis', lang))
        demand_fig = create_lead_time_demand_plot(history_df, game_state.params['lead_time'])
        st.plotly_chart(demand_fig, use_container_width=True)
        
        # Cost breakdown pie chart
        st.subheader(get_text('cost_breakdown', lang))
        cost_labels = [
            get_text('holding_cost', lang),
            get_text('purchase_cost', lang),
            get_text('shortage_cost', lang)
        ]
        cost_values = [
            game_state.holding_costs,
            game_state.purchase_costs,
            game_state.shortage_costs
        ]
        
        cost_fig = go.Figure(data=[go.Pie(
            labels=cost_labels,
            values=cost_values,
            hole=0.3
        )])
        cost_fig.update_layout(height=400)
        st.plotly_chart(cost_fig, use_container_width=True)
        
        # Pending orders table
        if game_state.pending_orders:
            st.subheader(get_text('pending_orders', lang))
            orders_df = pd.DataFrame(game_state.pending_orders)
            st.dataframe(orders_df)
    
    # Game over message
    if game_state.game_over:
        st.warning(get_text('simulation_complete', lang))
        
        # Final statistics
        st.subheader(get_text('final_statistics', lang))
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.write(f"### {get_text('demand_statistics', lang)}")
            if len(history_df) > 0:
                st.write(f"{get_text('avg_daily_demand', lang)}: {history_df['demand'].mean():.2f}")
                st.write(f"{get_text('max_daily_demand', lang)}: {history_df['demand'].max():.2f}")
                st.write(f"{get_text('min_daily_demand', lang)}: {history_df['demand'].min():.2f}")
        
        with col_stats2:
            st.write(f"### {get_text('stock_statistics', lang)}")
            if len(history_df) > 0:
                st.write(f"{get_text('avg_stock_level', lang)}: {history_df['stock'].mean():.2f}")
                st.write(f"{get_text('stockout_days', lang)}: {(history_df['stock'] == 0).sum()}")
                st.write(f"{get_text('service_level', lang)}: {(1 - history_df['shortage'].sum() / history_df['demand'].sum()):.2%}")

if __name__ == "__main__":
    simulation_page()