# File: levels.py

class LevelObjectives:
    def __init__(self, target_service_level, max_cost, time_limit):
        self.target_service_level = target_service_level
        self.max_cost = max_cost
        self.time_limit = time_limit  # in months

class InventoryLevels:
    @staticmethod
    def get_levels():
        return {
            "level_1": {
                "name": "Fast-Moving Consumer Goods",
                "description": """
                Common consumer goods with steady demand.
                Examples: Food items, toiletries, office supplies.
                
                Characteristics:
                - High turnover rate
                - Relatively stable demand
                - Short lead times
                - Low unit costs
                - Low order costs
                """,
                "params": {
                    "demand_distribution": "normal",
                    "storage_cost": 2.0,
                    "order_cost": 50.0,
                    "cpv_cost": 10.0,
                    "lead_time": 1,
                    "shortage_cost": 15.0,
                    "initial_stock": 100,
                    "average_demand": 30.0,
                    "sd_demand": 5.0
                }
            },
            "level_2": {
                "name": "Seasonal Products",
                "description": """
                Products with seasonal demand patterns.
                Examples: Clothing, seasonal decorations, sports equipment.
                
                Characteristics:
                - Variable demand based on season
                - Medium lead times
                - Moderate unit costs
                - Higher storage costs
                """,
                "params": {
                    "demand_distribution": "gamma",
                    "storage_cost": 4.0,
                    "order_cost": 150.0,
                    "cpv_cost": 30.0,
                    "lead_time": 3,
                    "shortage_cost": 45.0,
                    "initial_stock": 200,
                    "average_demand": 50.0,
                    "sd_demand": 20.0
                }
            },
            "level_3": {
                "name": "Critical Spare Parts",
                "description": """
                Essential maintenance parts for equipment.
                Examples: Machine parts, critical components.
                
                Characteristics:
                - Sporadic demand
                - Long lead times
                - High shortage costs
                - High unit costs
                """,
                "params": {
                    "demand_distribution": "poisson",
                    "storage_cost": 8.0,
                    "order_cost": 300.0,
                    "cpv_cost": 150.0,
                    "lead_time": 5,
                    "shortage_cost": 500.0,
                    "initial_stock": 50,
                    "average_demand": 5.0,
                    "sd_demand": 3.0
                }
            },
            "level_4": {
                "name": "MRO Supplies",
                "description": """
                General maintenance and repair supplies.
                Examples: Tools, lubricants, general spare parts.
                
                Characteristics:
                - Irregular demand
                - Medium lead times
                - Moderate shortage costs
                - Various unit costs
                """,
                "params": {
                    "demand_distribution": "exponential",
                    "storage_cost": 5.0,
                    "order_cost": 200.0,
                    "cpv_cost": 75.0,
                    "lead_time": 4,
                    "shortage_cost": 150.0,
                    "initial_stock": 80,
                    "average_demand": 10.0,
                    "sd_demand": 8.0
                }
            },
            "level_5": {
                "name": "Project-Based Materials",
                "description": """
                Materials used in project-based operations.
                Examples: Construction materials, project-specific components.
                
                Characteristics:
                - Highly variable demand
                - Long lead times
                - High storage costs
                - High order costs
                """,
                "params": {
                    "demand_distribution": "uniform",
                    "storage_cost": 10.0,
                    "order_cost": 400.0,
                    "cpv_cost": 200.0,
                    "lead_time": 7,
                    "shortage_cost": 300.0,
                    "initial_stock": 150,
                    "average_demand": 20.0,
                    "sd_demand": 15.0
                }
            }
        }