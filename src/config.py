# File: config.py
import streamlit as st
from game_state import GameState
from translations import get_text

def config_parameters():
    # Ensure language is initialized
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    lang = st.session_state.language
    st.sidebar.header(get_text('simulation_parameters', lang))
    
    # Define parameter configurations
    param_config = {
        'demand_distribution': {
            'options': ['normal', 'poisson', 'uniform', 'exponential', 'gamma'],
            'key': 'demand_distribution'
        },
        'storage_cost': {'min_value': 0.0, 'value': 2.0, 'step': 0.1},
        'order_cost': {'min_value': 0.0, 'value': 100.0, 'step': 10.0},
        'cpv_cost': {'min_value': 0.0, 'value': 20.0, 'step': 0.1},
        'lead_time': {'min_value': 0, 'value': 2, 'step': 1},
        'shortage_cost': {'min_value': 0.0, 'value': 50.0, 'step': 0.1},
        'initial_stock': {'min_value': 0, 'value': 100, 'step': 10},
        'average_demand': {'min_value': 0.0, 'value': 25.0, 'step': 0.1},
        'sd_demand': {'min_value': 0.1, 'value': 5.0, 'step': 0.1}
    }
    
    params = {}
    
    # Create input fields based on configuration
    params['demand_distribution'] = st.sidebar.selectbox(
        get_text('demand_distribution', lang),
        options=param_config['demand_distribution']['options']
    )
    
    for key, config in param_config.items():
        if key != 'demand_distribution':
            params[key] = st.sidebar.number_input(
                get_text(key, lang),
                **{k: v for k, v in config.items() if k != 'key'}
            )
    
    if st.sidebar.button(get_text('reset_simulation', lang)):
        st.session_state.game_state = GameState(params)
    
    return params
    # Demand Distribution Selection
    params['demand_distribution'] = st.sidebar.selectbox(
        "Demand Distribution",
        options=['normal', 'poisson', 'uniform', 'exponential', 'gamma']
    )
    
    params['storage_cost'] = st.sidebar.number_input(
        "Storage Cost per Unit", 
        min_value=0.0, 
        value=2.0, 
        step=0.1
    )
    params['order_cost'] = st.sidebar.number_input(
        "Fixed Order Cost", 
        min_value=0.0, 
        value=100.0, 
        step=10.0
    )
    params['cpv_cost'] = st.sidebar.number_input(
        "Cost per Unit", 
        min_value=0.0, 
        value=20.0, 
        step=0.1
    )
    params['lead_time'] = st.sidebar.number_input(
        "Lead Time (days)", 
        min_value=0, 
        value=2, 
        step=1
    )
    params['shortage_cost'] = st.sidebar.number_input(
        "Shortage Cost per Unit", 
        min_value=0.0, 
        value=50.0, 
        step=0.1
    )
    params['initial_stock'] = st.sidebar.number_input(
        "Initial Stock", 
        min_value=0, 
        value=100, 
        step=10
    )
    params['average_demand'] = st.sidebar.number_input(
        "Average Daily Demand", 
        min_value=0.0, 
        value=25.0, 
        step=0.1
    )
    params['sd_demand'] = st.sidebar.number_input(
        "Demand Variability", 
        min_value=0.1, 
        value=5.0, 
        step=0.1
    )

    
    return params