"""
Core models and calculations for Agile Teams Flow Metrics Simulation.
Based on queuing theory and Little's Law (L = λW).
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, List
from functools import lru_cache
import hashlib
import json

# Constants
BASELINE_LEAD_TIME = 2.0
CONGESTION_FACTOR = 3.0
MAX_UTILIZATION = 0.999
MIN_UTILIZATION = 0.001
VARIABILITY_SCALE = 0.1
UTILIZATION_POINTS = 50

@dataclass
class TeamConfiguration:
    """Configuration for a team role."""
    count: int
    service_time_min: float
    service_time_max: float
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Validate team configuration parameters."""
        if self.count < 0:
            raise ValueError(f"Count cannot be negative: {self.count}")
        if self.service_time_min <= 0:
            raise ValueError(f"Service time min must be positive: {self.service_time_min}")
        if self.service_time_max <= 0:
            raise ValueError(f"Service time max must be positive: {self.service_time_max}")
        if self.service_time_min >= self.service_time_max:
            raise ValueError(f"Service time min ({self.service_time_min}) must be less than max ({self.service_time_max})")

@dataclass
class SimulationParameters:
    """Complete set of simulation parameters."""
    teams: int
    skill_sets: Dict[str, TeamConfiguration]
    demand: int
    proficiency: float
    defects: float
    rework: float
    dependencies: float
    ai_impact: float
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Validate all simulation parameters."""
        if self.teams <= 0:
            raise ValueError(f"Teams must be positive: {self.teams}")
        if self.demand <= 0:
            raise ValueError(f"Demand must be positive: {self.demand}")
        if not 0 <= self.proficiency <= 1:
            raise ValueError(f"Proficiency must be between 0 and 1: {self.proficiency}")
        if not 0 <= self.defects <= 1:
            raise ValueError(f"Defects must be between 0 and 1: {self.defects}")
        if not 0 <= self.rework <= 1:
            raise ValueError(f"Rework must be between 0 and 1: {self.rework}")
        if not 0 <= self.dependencies <= 1:
            raise ValueError(f"Dependencies must be between 0 and 1: {self.dependencies}")
        if not 0 <= self.ai_impact <= 1:
            raise ValueError(f"AI impact must be between 0 and 1: {self.ai_impact}")
    
    def to_hash_key(self) -> str:
        """Generate a hash key for caching purposes."""
        data = {
            'teams': self.teams,
            'skill_sets': {k: (v.count, v.service_time_min, v.service_time_max) 
                          for k, v in self.skill_sets.items()},
            'demand': self.demand,
            'proficiency': self.proficiency,
            'defects': self.defects,
            'rework': self.rework,
            'dependencies': self.dependencies,
            'ai_impact': self.ai_impact
        }
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

@dataclass
class FlowMetrics:
    """Results of flow metrics calculation."""
    utilizations: List[float]
    lead_times: List[float]
    throughputs: List[float]
    variabilities: List[float]
    scaled_variabilities: List[float]

class FlowMetricsCalculator:
    """Calculator for agile team flow metrics using queuing theory."""
    
    def __init__(self):
        self._utilization_range = np.linspace(0.5, 1.0, UTILIZATION_POINTS)
    
    @lru_cache(maxsize=128)
    def calculate_metrics(self, params_hash: str, params: SimulationParameters) -> FlowMetrics:
        """
        Calculate flow metrics using Little's Law and queuing theory.
        
        Args:
            params_hash: Hash key for caching
            params: Simulation parameters
            
        Returns:
            FlowMetrics object containing all calculated metrics
        """
        try:
            # Calculate total service capacity
            total_service_rate, total_resources = self._calculate_service_capacity(params)
            
            # Calculate effective demand considering defects and rework
            effective_demand = self._calculate_effective_demand(params)
            
            # Calculate base utilization
            base_utilization = effective_demand / total_service_rate if total_service_rate > 0 else 1.0
            utilizations = self._utilization_range * base_utilization
            
            # Calculate metrics for each utilization level
            lead_times, throughputs, variabilities = self._calculate_flow_metrics(
                utilizations, effective_demand, total_service_rate, total_resources, params
            )
            
            # Scale variabilities for visualization
            scaled_variabilities = self._scale_variabilities(variabilities, lead_times)
            
            return FlowMetrics(
                utilizations=(utilizations * 100).tolist(),
                lead_times=lead_times,
                throughputs=throughputs,
                variabilities=variabilities,
                scaled_variabilities=scaled_variabilities
            )
            
        except Exception as e:
            raise RuntimeError(f"Error calculating metrics: {str(e)}")
    
    def _calculate_service_capacity(self, params: SimulationParameters) -> Tuple[float, int]:
        """Calculate total service rate and resources."""
        total_service_rate = 0.0
        total_resources = 0
        
        for skill, config in params.skill_sets.items():
            if config.count == 0:
                continue
                
            avg_service_time = (config.service_time_min + config.service_time_max) / 2
            service_rate = (1 / avg_service_time * config.count * 
                          params.proficiency * (1 - params.dependencies) * 
                          (1 + params.ai_impact))
            
            total_service_rate += service_rate
            total_resources += config.count
        
        return total_service_rate * params.teams, total_resources * params.teams
    
    def _calculate_effective_demand(self, params: SimulationParameters) -> float:
        """Calculate effective demand considering defects and rework."""
        defect_multiplier = 1 + params.defects * params.rework * (1 - params.ai_impact * 0.2)
        return params.demand * defect_multiplier
    
    def _calculate_flow_metrics(self, utilizations: np.ndarray, effective_demand: float,
                               total_service_rate: float, total_resources: int,
                               params: SimulationParameters) -> Tuple[List[float], List[float], List[float]]:
        """Calculate lead time, throughput, and variability for each utilization level."""
        lead_times = []
        throughputs = []
        variabilities = []
        
        max_throughput = total_service_rate * (1 - params.defects * (1 - params.ai_impact * 0.2))
        
        for u in utilizations:
            # Ensure utilization doesn't exceed maximum
            u_clamped = min(u, MAX_UTILIZATION)
            
            # Calculate lead time using queuing theory
            if u_clamped >= MAX_UTILIZATION:
                lead_time = max(lead_times[-1] * 1.5 if lead_times else BASELINE_LEAD_TIME, 100)
                throughput = 0
            else:
                lead_time = BASELINE_LEAD_TIME + CONGESTION_FACTOR / (1 - u_clamped + MIN_UTILIZATION)
                degradation_factor = max(0, 1 - (u_clamped / 1.0))
                throughput = min(effective_demand, max_throughput * degradation_factor)
            
            # Calculate schedule variability
            wip = effective_demand * lead_time
            if total_resources > 0:
                base_utilization = effective_demand / total_service_rate if total_service_rate > 0 else 1.0
                variability = max(0, lead_time * (u_clamped / max(1, base_utilization)) * 
                                (wip / total_resources) * VARIABILITY_SCALE)
            else:
                variability = 0
            
            lead_times.append(lead_time)
            throughputs.append(throughput)
            variabilities.append(variability)
        
        return lead_times, throughputs, variabilities
    
    def _scale_variabilities(self, variabilities: List[float], lead_times: List[float]) -> List[float]:
        """Scale variabilities for visualization purposes."""
        if not variabilities or not lead_times:
            return []
            
        variability_midpoint = np.mean(variabilities)
        lead_time_midpoint = np.mean(lead_times)
        
        return [lead_time_midpoint + (v - variability_midpoint) * VARIABILITY_SCALE 
                for v in variabilities]

class GoalSeeker:
    """Goal-seeking optimization for simulation parameters."""
    
    def __init__(self, calculator: FlowMetricsCalculator):
        self.calculator = calculator
    
    def seek_utilization(self, target_util: float, params: SimulationParameters, 
                        max_iterations: int = 10, tolerance: float = 0.01) -> int:
        """Find demand that achieves target utilization."""
        demand = params.demand
        
        for _ in range(max_iterations):
            test_params = self._create_test_params(params, demand=demand)
            metrics = self.calculator.calculate_metrics(
                test_params.to_hash_key(), test_params
            )
            
            current_util = metrics.utilizations[-1] / 100
            
            if abs(current_util - target_util) < tolerance:
                break
                
            # Use gradient-based adjustment
            if current_util != 0:
                adjustment_factor = target_util / current_util
                demand = demand * adjustment_factor
            
            demand = max(5, min(20, int(demand)))
        
        return demand
    
    def seek_value_flow(self, params: SimulationParameters, 
                       max_iterations: int = 10) -> int:
        """Find demand that maximizes throughput."""
        best_demand = params.demand
        best_throughput = 0
        
        # Test range of demands around current value
        test_demands = range(max(5, params.demand - 5), min(21, params.demand + 6))
        
        for demand in test_demands:
            test_params = self._create_test_params(params, demand=demand)
            metrics = self.calculator.calculate_metrics(
                test_params.to_hash_key(), test_params
            )
            
            # Use second-to-last throughput (before saturation)
            if len(metrics.throughputs) >= 2:
                current_throughput = metrics.throughputs[-2]
                if current_throughput > best_throughput:
                    best_throughput = current_throughput
                    best_demand = demand
        
        return best_demand
    
    def seek_date_stability(self, params: SimulationParameters, 
                           max_iterations: int = 10) -> int:
        """Find demand that minimizes schedule variability."""
        best_demand = params.demand
        min_variability = float('inf')
        
        # Test range of demands around current value
        test_demands = range(max(5, params.demand - 5), min(21, params.demand + 6))
        
        for demand in test_demands:
            test_params = self._create_test_params(params, demand=demand)
            metrics = self.calculator.calculate_metrics(
                test_params.to_hash_key(), test_params
            )
            
            if metrics.variabilities:
                current_variability = max(metrics.variabilities) - min(metrics.variabilities)
                if current_variability < min_variability:
                    min_variability = current_variability
                    best_demand = demand
        
        return best_demand
    
    def _create_test_params(self, base_params: SimulationParameters, **overrides) -> SimulationParameters:
        """Create test parameters with overrides."""
        params_dict = {
            'teams': base_params.teams,
            'skill_sets': base_params.skill_sets,
            'demand': base_params.demand,
            'proficiency': base_params.proficiency,
            'defects': base_params.defects,
            'rework': base_params.rework,
            'dependencies': base_params.dependencies,
            'ai_impact': base_params.ai_impact
        }
        params_dict.update(overrides)
        return SimulationParameters(**params_dict)

# Default configurations
DEFAULT_SKILL_SETS = {
    "Developers": TeamConfiguration(count=3, service_time_min=1.0, service_time_max=2.0),
    "Testers": TeamConfiguration(count=2, service_time_min=2.0, service_time_max=3.0),
    "Architects": TeamConfiguration(count=1, service_time_min=1.5, service_time_max=2.5)
}

DEFAULT_PARAMS = SimulationParameters(
    teams=1,
    skill_sets=DEFAULT_SKILL_SETS,
    demand=10,
    proficiency=0.8,
    defects=0.2,
    rework=0.5,
    dependencies=0.2,
    ai_impact=0.3
)