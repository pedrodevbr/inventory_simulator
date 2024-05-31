import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def authenticate(username, password):
    # For simplicity, we use a dummy check. Replace this with actual authentication logic.
    return username == "admin" and password == "password"

def login_page():
    
    st.title("Login")
    test = True
    if test:
        username = "admin"
        password = "password"
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.session_state['page'] = 'home'
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def home_page():
    st.title("Home")
    st.write("Welcome to the Inventory Simulator!")
    
    if st.button("Start Playing"):
        st.session_state['page'] = 'simulation'
        st.experimental_rerun()
    
    if st.button("Ranking"):
        st.session_state['page'] = 'ranking'
        st.experimental_rerun()
    
    if st.button("Configuration"):
        st.write("Configuration page (not implemented yet).")

def simulation_page():
    st.title("Inventory Simulation")

    st.sidebar.header("Simulation Parameters")
    storage_cost = st.sidebar.number_input("Storage Cost", value=1.0)
    order_cost = st.sidebar.number_input("Order Cost", value=50.0)
    cpv_cost = st.sidebar.number_input("Cost Per Unit", value=10.0)
    lead_time = st.sidebar.number_input("Lead Time", value=1)  # Lead time in months
    cpv_lead_time = st.sidebar.number_input("Cost Per Unit Lead Time", value=10)
    shortage_cost = st.sidebar.number_input("Shortage Cost", value=100.0)
    initial_stock = st.sidebar.number_input("Initial Stock", value=100)
    initial_rp = st.sidebar.number_input("Initial Replenishment Point", value=50)
    initial_max_point = st.sidebar.number_input("Initial Maximum Stock", value=200)
    average_demand = st.sidebar.number_input("Average Demand", value=20.0)
    sd_demand = st.sidebar.number_input("Demand Standard Deviation", value=5.0)
    
    # Initialize simulation variables
    if 'stock' not in st.session_state:
        st.session_state['stock'] = initial_stock
        st.session_state['month'] = 0
        st.session_state['orders'] = []
        st.session_state['cost'] = 0.0
        st.session_state['stock_history'] = [initial_stock]
        st.session_state['rp_history'] = [initial_rp]
        st.session_state['max_history'] = [initial_max_point]
        st.session_state['month_history'] = [0]
        st.session_state['scores'] = []

    st.write(f"Month: {st.session_state['month']}")
    st.write(f"Current Stock: {st.session_state['stock']}")
    st.write(f"Total Cost: {round(st.session_state['cost'])}")

    rp = st.number_input("Replenishment Point (RP)", value=initial_rp)
    max_stock = st.number_input("Maximum Stock (MAX)", value=initial_max_point)

    if st.button("Next Month"):
        demand = max(0, np.random.normal(average_demand, sd_demand))
        st.session_state['stock'] -= round(demand)
        st.session_state['month'] += 1

        # Calculate virtual stock
        orders_in_transit = sum([order[1] for order in st.session_state['orders']])
        virtual_stock = st.session_state['stock'] + orders_in_transit

        if virtual_stock < rp:
            order_quantity = max_stock - virtual_stock
            st.session_state['orders'].append((st.session_state['month'] + lead_time, round(order_quantity)))
            st.session_state['cost'] += order_cost + (round(order_quantity) * cpv_cost)
        
        arriving_orders = [order for order in st.session_state['orders'] if order[0] == st.session_state['month']]
        for order in arriving_orders:
            st.session_state['stock'] += order[1]
            st.session_state['orders'].remove(order)

        storage_cost_today = st.session_state['stock'] * storage_cost
        st.session_state['cost'] += round(storage_cost_today)
        
        if st.session_state['stock'] < 0:
            st.session_state['cost'] += abs(st.session_state['stock']) * shortage_cost
            st.session_state['stock'] = 0
        
        # Update history
        st.session_state['stock_history'].append(st.session_state['stock'])
        st.session_state['rp_history'].append(rp)
        st.session_state['max_history'].append(max_stock)
        st.session_state['month_history'].append(st.session_state['month'])

        # Check if it's the end of the year
        if st.session_state['month'] % 12 == 0:
            st.write(f"End of year! Total Cost: {round(st.session_state['cost'])}")
        
        st.experimental_rerun()

    if st.button("Stop Game"):
        st.session_state['scores'].append(round(st.session_state['cost']))
        st.session_state['stock'] = initial_stock
        st.session_state['month'] = 0
        st.session_state['orders'] = []
        st.session_state['cost'] = 0.0
        st.session_state['stock_history'] = [initial_stock]
        st.session_state['rp_history'] = [initial_rp]
        st.session_state['max_history'] = [initial_max_point]
        st.session_state['month_history'] = [0]
        st.experimental_rerun()

    # Plot the stock level history
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=st.session_state['month_history'], y=st.session_state['stock_history'],
                             mode='lines+markers', name='Stock Level'))
    fig.add_trace(go.Scatter(x=st.session_state['month_history'], y=st.session_state['rp_history'],
                             mode='lines', name='Replenishment Point (RP)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=st.session_state['month_history'], y=st.session_state['max_history'],
                             mode='lines', name='Maximum Stock (MAX)', line=dict(dash='dot')))

    fig.update_layout(title='Inventory Levels Over Time', xaxis_title='Month', yaxis_title='Stock Level')

    st.plotly_chart(fig)

def ranking_page():
    st.title("Ranking")
    if 'scores' in st.session_state and st.session_state['scores']:
        scores_df = pd.DataFrame(st.session_state['scores'], columns=['Score'])
        st.write(scores_df)
    else:
        st.write("No scores recorded yet.")
    
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'
        st.experimental_rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['logged_in']:
        if st.session_state['page'] == 'home':
            home_page()
        elif st.session_state['page'] == 'simulation':
            simulation_page()
        elif st.session_state['page'] == 'ranking':
            ranking_page()
    else:
        login_page()

if __name__ == "__main__":
    main()