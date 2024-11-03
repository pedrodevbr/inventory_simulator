# File: game_state.py
from demand_generator import DemandGenerator
import numpy as np
from collections import deque

class GameState:
    def __init__(self, level_params=None,lang='en'):
        if level_params is None:
            level_params = {
                'storage_cost': 2.0,
                'order_cost': 100.0,
                'cpv_cost': 20.0,
                'lead_time': 3,
                'shortage_cost': 50.0,
                'initial_stock': 100,
                'average_demand': 25.0,
                'sd_demand': 5.0,
                'demand_distribution': 'normal'
            }
        self.params = level_params
        self.current_stock = int(level_params['initial_stock'])
        self.virtual_stock = int(level_params['initial_stock'])
        self.pending_orders = []
        self.history = []
        self.policy_history = []
        self.demand_window = deque(maxlen=level_params['lead_time'])  # Fixed-size window for demand
        self.grouped_demands = []  # Store grouped demands
        self.day = 0
        self.total_cost = 0.0
        self.holding_costs = 0.0
        self.purchase_costs = 0.0
        self.shortage_costs = 0.0
        self.rp = int(level_params['initial_stock'] // 2)
        self.max_point = int(level_params['initial_stock'] * 1.5)
        self.game_over = False
        self.below_rp_flag = False
        self.order_placed_flag = False
        self.language = lang
        
        self.demand_generators = {
            'normal': DemandGenerator.normal,
            'poisson': DemandGenerator.poisson,
            'uniform': DemandGenerator.uniform,
            'exponential': DemandGenerator.exponential,
            'gamma': DemandGenerator.gamma
        }

        # Record initial policy
        self.policy_history.append({
            'day': 0,
            'rp': self.rp,
            'max_point': self.max_point
        })

    def generate_demand(self):
        """Generate demand based on the selected distribution."""
        generator = self.demand_generators.get(
            self.params['demand_distribution'], 
            DemandGenerator.normal
        )
        return generator(self.params)

    def calculate_lead_time_demand(self):
        """Calculate the sum of demands within the lead time window."""
        if len(self.demand_window) == self.params['lead_time']:
            grouped_demand = sum(self.demand_window)
            self.grouped_demands.append(grouped_demand)
            return grouped_demand
        return sum(self.demand_window)

    def process_daily_operations(self):
        if self.game_over:
            return

        # Check if policy changed
        if (not self.policy_history or 
            self.rp != self.policy_history[-1]['rp'] or 
            self.max_point != self.policy_history[-1]['max_point']):
            self.policy_history.append({
                'day': self.day,
                'rp': self.rp,
                'max_point': self.max_point
            })

        daily_holding_cost = 0
        daily_purchase_cost = 0
        daily_shortage_cost = 0

        # Process arriving orders and their costs
        arrived_orders = [order for order in self.pending_orders if order['arrival_day'] == self.day]
        self.pending_orders = [order for order in self.pending_orders if order['arrival_day'] != self.day]
        
        for order in arrived_orders:
            self.current_stock += order['quantity']
            daily_purchase_cost += (self.params['order_cost'] + 
                                  (order['quantity'] * self.params['cpv_cost']))

        # Generate and process demand
        demand = self.generate_demand()
        self.demand_window.append(demand)  # Add new demand to window
        
        # Calculate lead time demand
        lead_time_demand = self.calculate_lead_time_demand()
        
        # Process current demand
        fulfilled = min(demand, max(0, self.current_stock))
        shortage = demand - fulfilled
        self.current_stock = max(0, self.current_stock - fulfilled)
        
        # Update virtual stock
        self.virtual_stock = self.current_stock
        for order in self.pending_orders:
            self.virtual_stock += order['quantity']

        # Calculate costs
        daily_holding_cost = self.current_stock * self.params['storage_cost']
        daily_shortage_cost = shortage * self.params['shortage_cost']

        # Order placement logic
        if self.virtual_stock <= self.rp:
            if self.below_rp_flag and not self.order_placed_flag:
                order_quantity = int(self.max_point - self.virtual_stock)
                arrival_day = self.day + self.params['lead_time']
                
                self.pending_orders.append({
                    'quantity': order_quantity,
                    'arrival_day': arrival_day,
                    'order_day': self.day,
                    'order_cost': self.params['order_cost'],
                    'units_cost': order_quantity * self.params['cpv_cost']
                })

                self.virtual_stock += order_quantity
                self.below_rp_flag = False
                self.order_placed_flag = True
            else:
                self.below_rp_flag = True
        else:
            self.order_placed_flag = False
            self.below_rp_flag = False

        # Update costs
        self.holding_costs += daily_holding_cost
        self.purchase_costs += daily_purchase_cost
        self.shortage_costs += daily_shortage_cost
        self.total_cost = self.holding_costs + self.purchase_costs + self.shortage_costs

        # Update history
        self.history.append({
            'day': self.day,
            'stock': self.current_stock,
            'virtual_stock': self.virtual_stock,
            'demand': demand,
            'shortage': shortage,
            'holding_cost': daily_holding_cost,
            'purchase_cost': daily_purchase_cost,
            'shortage_cost': daily_shortage_cost,
            'total_cost': daily_holding_cost + daily_purchase_cost + daily_shortage_cost,
            'cumulative_cost': self.total_cost,
            'lead_time_demand': lead_time_demand,
            'grouped_demand': self.grouped_demands[-1] if self.grouped_demands else demand*self.params['lead_time'],
            'rp': self.rp,
            'max_point': self.max_point
        })

        self.day += 1
        
        if self.day >= 30:
            self.game_over = True