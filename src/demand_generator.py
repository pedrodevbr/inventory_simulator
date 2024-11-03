# File: demand_generator.py
import numpy as np

class DemandGenerator:
    @staticmethod
    def normal(params):
        # Handle both sd_demand and demand_variability for backwards compatibility
        variability = params.get('sd_demand', params.get('demand_variability', 5.0))
        demand = np.random.normal(params['average_demand'], variability)
        return max(0, int(round(demand)))
    
    @staticmethod
    def poisson(params):
        demand = np.random.poisson(params['average_demand'])
        return demand
    
    @staticmethod
    def uniform(params):
        variability = params.get('sd_demand', params.get('demand_variability', 5.0))
        min_demand = max(0, params['average_demand'] - variability)
        max_demand = params['average_demand'] + variability
        demand = np.random.uniform(min_demand, max_demand)
        return int(round(demand))
    
    @staticmethod
    def exponential(params):
        demand = np.random.exponential(params['average_demand'])
        return int(round(demand))
    
    @staticmethod
    def gamma(params):
        variability = params.get('sd_demand', params.get('demand_variability', 5.0))
        shape = (params['average_demand'] / variability)**2
        scale = (variability**2) / params['average_demand']
        demand = np.random.gamma(shape, scale)
        return int(round(demand))