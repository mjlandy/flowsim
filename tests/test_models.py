"""
Unit tests for the models module.
"""

import pytest
import numpy as np
from models import (
    TeamConfiguration, SimulationParameters, FlowMetricsCalculator,
    GoalSeeker, DEFAULT_PARAMS, DEFAULT_SKILL_SETS
)

class TestTeamConfiguration:
    """Test cases for TeamConfiguration class."""
    
    def test_valid_configuration(self):
        """Test creating a valid team configuration."""
        config = TeamConfiguration(count=3, service_time_min=1.0, service_time_max=2.0)
        assert config.count == 3
        assert config.service_time_min == 1.0
        assert config.service_time_max == 2.0
    
    def test_invalid_count(self):
        """Test that negative count raises ValueError."""
        with pytest.raises(ValueError, match="Count cannot be negative"):
            TeamConfiguration(count=-1, service_time_min=1.0, service_time_max=2.0)
    
    def test_invalid_service_time_range(self):
        """Test that invalid service time range raises ValueError."""
        with pytest.raises(ValueError, match="Service time min .* must be less than max"):
            TeamConfiguration(count=3, service_time_min=2.0, service_time_max=1.0)
    
    def test_zero_service_time(self):
        """Test that zero service time raises ValueError."""
        with pytest.raises(ValueError, match="Service time min must be positive"):
            TeamConfiguration(count=3, service_time_min=0.0, service_time_max=2.0)

class TestSimulationParameters:
    """Test cases for SimulationParameters class."""
    
    def test_valid_parameters(self):
        """Test creating valid simulation parameters."""
        params = SimulationParameters(
            teams=2,
            skill_sets=DEFAULT_SKILL_SETS,
            demand=10,
            proficiency=0.8,
            defects=0.2,
            rework=0.5,
            dependencies=0.2,
            ai_impact=0.3
        )
        assert params.teams == 2
        assert params.demand == 10
        assert params.proficiency == 0.8
    
    def test_invalid_teams(self):
        """Test that invalid teams count raises ValueError."""
        with pytest.raises(ValueError, match="Teams must be positive"):
            SimulationParameters(
                teams=0,
                skill_sets=DEFAULT_SKILL_SETS,
                demand=10,
                proficiency=0.8,
                defects=0.2,
                rework=0.5,
                dependencies=0.2,
                ai_impact=0.3
            )
    
    def test_invalid_proficiency(self):
        """Test that invalid proficiency raises ValueError."""
        with pytest.raises(ValueError, match="Proficiency must be between 0 and 1"):
            SimulationParameters(
                teams=1,
                skill_sets=DEFAULT_SKILL_SETS,
                demand=10,
                proficiency=1.5,
                defects=0.2,
                rework=0.5,
                dependencies=0.2,
                ai_impact=0.3
            )
    
    def test_hash_key_generation(self):
        """Test that hash key generation works consistently."""
        params1 = DEFAULT_PARAMS
        params2 = SimulationParameters(
            teams=DEFAULT_PARAMS.teams,
            skill_sets=DEFAULT_PARAMS.skill_sets,
            demand=DEFAULT_PARAMS.demand,
            proficiency=DEFAULT_PARAMS.proficiency,
            defects=DEFAULT_PARAMS.defects,
            rework=DEFAULT_PARAMS.rework,
            dependencies=DEFAULT_PARAMS.dependencies,
            ai_impact=DEFAULT_PARAMS.ai_impact
        )
        
        assert params1.to_hash_key() == params2.to_hash_key()

class TestFlowMetricsCalculator:
    """Test cases for FlowMetricsCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = FlowMetricsCalculator()
    
    def test_basic_calculation(self):
        """Test basic metrics calculation."""
        calculator = FlowMetricsCalculator()
        metrics = calculator.calculate_metrics(
            DEFAULT_PARAMS.to_hash_key(),
            DEFAULT_PARAMS
        )
        
        assert len(metrics.utilizations) > 0
        assert len(metrics.lead_times) > 0
        assert len(metrics.throughputs) > 0
        assert len(metrics.variabilities) > 0
        assert len(metrics.scaled_variabilities) > 0
        
        # Check that all arrays have the same length
        assert len(metrics.utilizations) == len(metrics.lead_times)
        assert len(metrics.utilizations) == len(metrics.throughputs)
        assert len(metrics.utilizations) == len(metrics.variabilities)
        assert len(metrics.utilizations) == len(metrics.scaled_variabilities)
    
    def test_lead_time_increases_with_utilization(self):
        """Test that lead time generally increases with utilization."""
        calculator = FlowMetricsCalculator()
        metrics = calculator.calculate_metrics(
            DEFAULT_PARAMS.to_hash_key(),
            DEFAULT_PARAMS
        )
        
        # Lead times should generally increase
        assert metrics.lead_times[-1] > metrics.lead_times[0]
    
    def test_zero_teams_handling(self):
        """Test handling of edge case with zero teams."""
        calculator = FlowMetricsCalculator()
        
        # This should raise a validation error due to zero teams
        with pytest.raises(ValueError):
            invalid_params = SimulationParameters(
                teams=0,
                skill_sets=DEFAULT_SKILL_SETS,
                demand=10,
                proficiency=0.8,
                defects=0.2,
                rework=0.5,
                dependencies=0.2,
                ai_impact=0.3
            )
    
    def test_caching_works(self):
        """Test that caching mechanism works."""
        calculator = FlowMetricsCalculator()
        
        # First calculation
        metrics1 = calculator.calculate_metrics(
            DEFAULT_PARAMS.to_hash_key(),
            DEFAULT_PARAMS
        )
        
        # Second calculation with same parameters should use cache
        metrics2 = calculator.calculate_metrics(
            DEFAULT_PARAMS.to_hash_key(),
            DEFAULT_PARAMS
        )
        
        # Results should be identical
        assert metrics1.utilizations == metrics2.utilizations
        assert metrics1.lead_times == metrics2.lead_times

class TestGoalSeeker:
    """Test cases for GoalSeeker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = FlowMetricsCalculator()
        self.goal_seeker = GoalSeeker(self.calculator)
    
    def test_seek_utilization(self):
        """Test utilization goal seeking."""
        goal_seeker = GoalSeeker(FlowMetricsCalculator())
        
        target_util = 0.8  # 80%
        result_demand = goal_seeker.seek_utilization(
            target_util, DEFAULT_PARAMS
        )
        
        assert isinstance(result_demand, int)
        assert 5 <= result_demand <= 20  # Should be within valid range
    
    def test_seek_value_flow(self):
        """Test value flow optimization."""
        goal_seeker = GoalSeeker(FlowMetricsCalculator())
        
        result_demand = goal_seeker.seek_value_flow(DEFAULT_PARAMS)
        
        assert isinstance(result_demand, int)
        assert 5 <= result_demand <= 20
    
    def test_seek_date_stability(self):
        """Test date stability optimization."""
        goal_seeker = GoalSeeker(FlowMetricsCalculator())
        
        result_demand = goal_seeker.seek_date_stability(DEFAULT_PARAMS)
        
        assert isinstance(result_demand, int)
        assert 5 <= result_demand <= 20

class TestIntegration:
    """Integration tests for the complete model system."""
    
    def test_end_to_end_simulation(self):
        """Test complete end-to-end simulation."""
        # Create parameters
        params = SimulationParameters(
            teams=2,
            skill_sets={
                "Developers": TeamConfiguration(count=4, service_time_min=0.8, service_time_max=1.5),
                "Testers": TeamConfiguration(count=2, service_time_min=1.5, service_time_max=2.5),
                "Architects": TeamConfiguration(count=1, service_time_min=1.0, service_time_max=2.0)
            },
            demand=12,
            proficiency=0.9,
            defects=0.15,
            rework=0.4,
            dependencies=0.1,
            ai_impact=0.4
        )
        
        # Calculate metrics
        calculator = FlowMetricsCalculator()
        metrics = calculator.calculate_metrics(params.to_hash_key(), params)
        
        # Verify results are reasonable
        assert all(u >= 50 for u in metrics.utilizations)  # Utilization >= 50%
        assert all(u <= 100 for u in metrics.utilizations)  # Utilization <= 100%
        assert all(lt > 0 for lt in metrics.lead_times)  # Lead times positive
        assert all(tp >= 0 for tp in metrics.throughputs)  # Throughput non-negative
    
    def test_parameter_sensitivity(self):
        """Test that parameters affect results as expected."""
        calculator = FlowMetricsCalculator()
        
        # Base case
        base_metrics = calculator.calculate_metrics(
            DEFAULT_PARAMS.to_hash_key(),
            DEFAULT_PARAMS
        )
        
        # Higher demand should increase utilization
        high_demand_params = SimulationParameters(
            teams=DEFAULT_PARAMS.teams,
            skill_sets=DEFAULT_PARAMS.skill_sets,
            demand=DEFAULT_PARAMS.demand + 5,
            proficiency=DEFAULT_PARAMS.proficiency,
            defects=DEFAULT_PARAMS.defects,
            rework=DEFAULT_PARAMS.rework,
            dependencies=DEFAULT_PARAMS.dependencies,
            ai_impact=DEFAULT_PARAMS.ai_impact
        )
        
        high_demand_metrics = calculator.calculate_metrics(
            high_demand_params.to_hash_key(),
            high_demand_params
        )
        
        # Higher demand should lead to higher lead times
        assert max(high_demand_metrics.lead_times) > max(base_metrics.lead_times)

if __name__ == "__main__":
    pytest.main([__file__])