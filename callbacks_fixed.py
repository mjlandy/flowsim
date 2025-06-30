"""
Simplified callback handlers for Agile Teams Flow Metrics Simulation.
"""

from dash import Input, Output, State, callback_context
from typing import Tuple, List, Any, Dict
import logging

from models import (
    SimulationParameters, TeamConfiguration, FlowMetricsCalculator,
    GoalSeeker, DEFAULT_PARAMS, DEFAULT_SKILL_SETS
)
from visualization import FlowMetricsVisualizer, ParameterImpactDescriptor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CallbackManager:
    """Manages all callbacks for the application."""
    
    def __init__(self, app):
        self.app = app
        self.calculator = FlowMetricsCalculator()
        self.goal_seeker = GoalSeeker(self.calculator)
        self.visualizer = FlowMetricsVisualizer()
        self.impact_descriptor = ParameterImpactDescriptor()
        
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register all application callbacks."""
        
        @self.app.callback(
            [
                Output("flow-graph", "figure"),
                Output("change-notification", "children"),
                Output("teams-slider", "value"),
                Output("dev-count-slider", "value"),
                Output("dev-service-slider", "value"),
                Output("test-count-slider", "value"),
                Output("test-service-slider", "value"),
                Output("arch-count-slider", "value"),
                Output("arch-service-slider", "value"),
                Output("demand-slider", "value"),
                Output("proficiency-slider", "value"),
                Output("defects-slider", "value"),
                Output("rework-slider", "value"),
                Output("dependencies-slider", "value"),
                Output("ai-slider", "value")
            ],
            [
                # Slider inputs
                Input("teams-slider", "value"),
                Input("dev-count-slider", "value"),
                Input("dev-service-slider", "value"),
                Input("test-count-slider", "value"),
                Input("test-service-slider", "value"),
                Input("arch-count-slider", "value"),
                Input("arch-service-slider", "value"),
                Input("demand-slider", "value"),
                Input("proficiency-slider", "value"),
                Input("defects-slider", "value"),
                Input("rework-slider", "value"),
                Input("dependencies-slider", "value"),
                Input("ai-slider", "value"),
                
                # Goal seeking buttons
                Input("seek-util-btn", "n_clicks"),
                Input("seek-flow-btn", "n_clicks"),
                Input("seek-stability-btn", "n_clicks")
            ],
            [
                # Goal seeking target
                State("target-util-input", "value")
            ]
        )
        def update_simulation(*args):
            """Main callback for updating the simulation."""
            return self._handle_simulation_update(*args)
    
    def _handle_simulation_update(self, *args) -> Tuple:
        """Handle the main simulation update logic."""
        try:
            # Parse arguments - first 13 are slider values, next 3 are button clicks, last 1 is target util
            slider_values = args[:13]
            button_clicks = args[13:16]
            target_util = args[16] if len(args) > 16 else 80
            
            # Create current parameters
            current_params = self._create_parameters_from_sliders(slider_values)
            
            # Check if goal seeking was triggered
            ctx = callback_context
            trigger_id = None
            if ctx.triggered:
                trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            # Apply goal seeking if triggered
            if trigger_id == "seek-util-btn" and target_util:
                new_demand = self.goal_seeker.seek_utilization(target_util / 100, current_params)
                current_params = self._update_demand(current_params, new_demand)
                change_text = f"Optimized demand to {new_demand} for {target_util}% utilization"
            elif trigger_id == "seek-flow-btn":
                new_demand = self.goal_seeker.seek_value_flow(current_params)
                current_params = self._update_demand(current_params, new_demand)
                change_text = f"Optimized demand to {new_demand} for maximum throughput"
            elif trigger_id == "seek-stability-btn":
                new_demand = self.goal_seeker.seek_date_stability(current_params)
                current_params = self._update_demand(current_params, new_demand)
                change_text = f"Optimized demand to {new_demand} for minimum variability"
            else:
                change_text = "Parameters updated - metrics recalculated"
            
            # Calculate metrics
            metrics = self.calculator.calculate_metrics(
                current_params.to_hash_key(), current_params
            )
            
            # Create visualization
            figure = self.visualizer.create_flow_chart(metrics)
            
            # Return all outputs
            return (
                figure,
                change_text,
                current_params.teams,
                current_params.skill_sets["Developers"].count,
                [current_params.skill_sets["Developers"].service_time_min,
                 current_params.skill_sets["Developers"].service_time_max],
                current_params.skill_sets["Testers"].count,
                [current_params.skill_sets["Testers"].service_time_min,
                 current_params.skill_sets["Testers"].service_time_max],
                current_params.skill_sets["Architects"].count,
                [current_params.skill_sets["Architects"].service_time_min,
                 current_params.skill_sets["Architects"].service_time_max],
                current_params.demand,
                current_params.proficiency,
                current_params.defects,
                current_params.rework,
                current_params.dependencies,
                current_params.ai_impact
            )
            
        except Exception as e:
            logger.error(f"Error in simulation update: {str(e)}")
            return self._create_error_outputs(str(e))
    
    def _create_parameters_from_sliders(self, slider_values) -> SimulationParameters:
        """Create SimulationParameters from slider values."""
        try:
            # Ensure we have the right number of values and handle defaults
            teams = slider_values[0] if slider_values[0] is not None else 1
            dev_count = slider_values[1] if slider_values[1] is not None else 3
            dev_service = slider_values[2] if slider_values[2] is not None else [1.0, 2.0]
            test_count = slider_values[3] if slider_values[3] is not None else 2
            test_service = slider_values[4] if slider_values[4] is not None else [2.0, 3.0]
            arch_count = slider_values[5] if slider_values[5] is not None else 1
            arch_service = slider_values[6] if slider_values[6] is not None else [1.5, 2.5]
            demand = slider_values[7] if slider_values[7] is not None else 10
            proficiency = slider_values[8] if slider_values[8] is not None else 0.8
            defects = slider_values[9] if slider_values[9] is not None else 0.2
            rework = slider_values[10] if slider_values[10] is not None else 0.5
            dependencies = slider_values[11] if slider_values[11] is not None else 0.2
            ai_impact = slider_values[12] if slider_values[12] is not None else 0.3
            
            skill_sets = {
                "Developers": TeamConfiguration(
                    count=dev_count,
                    service_time_min=dev_service[0],
                    service_time_max=dev_service[1]
                ),
                "Testers": TeamConfiguration(
                    count=test_count,
                    service_time_min=test_service[0],
                    service_time_max=test_service[1]
                ),
                "Architects": TeamConfiguration(
                    count=arch_count,
                    service_time_min=arch_service[0],
                    service_time_max=arch_service[1]
                )
            }
            
            return SimulationParameters(
                teams=teams,
                skill_sets=skill_sets,
                demand=demand,
                proficiency=proficiency,
                defects=defects,
                rework=rework,
                dependencies=dependencies,
                ai_impact=ai_impact
            )
        except Exception as e:
            logger.warning(f"Error creating parameters, using defaults: {str(e)}")
            return DEFAULT_PARAMS
    
    def _update_demand(self, params: SimulationParameters, new_demand: int) -> SimulationParameters:
        """Create new parameters with updated demand."""
        return SimulationParameters(
            teams=params.teams,
            skill_sets=params.skill_sets,
            demand=new_demand,
            proficiency=params.proficiency,
            defects=params.defects,
            rework=params.rework,
            dependencies=params.dependencies,
            ai_impact=params.ai_impact
        )
    
    def _create_error_outputs(self, error_msg: str) -> Tuple:
        """Create default outputs when an error occurs."""
        default_params = DEFAULT_PARAMS
        
        try:
            metrics = self.calculator.calculate_metrics(
                default_params.to_hash_key(), default_params
            )
            figure = self.visualizer.create_flow_chart(metrics)
        except:
            import plotly.graph_objects as go
            figure = go.Figure().add_annotation(
                text=f"Error: {error_msg}",
                x=0.5, y=0.5,
                showarrow=False
            )
        
        return (
            figure,
            f"Error occurred: {error_msg}. Using default values.",
            default_params.teams,
            default_params.skill_sets["Developers"].count,
            [default_params.skill_sets["Developers"].service_time_min,
             default_params.skill_sets["Developers"].service_time_max],
            default_params.skill_sets["Testers"].count,
            [default_params.skill_sets["Testers"].service_time_min,
             default_params.skill_sets["Testers"].service_time_max],
            default_params.skill_sets["Architects"].count,
            [default_params.skill_sets["Architects"].service_time_min,
             default_params.skill_sets["Architects"].service_time_max],
            default_params.demand,
            default_params.proficiency,
            default_params.defects,
            default_params.rework,
            default_params.dependencies,
            default_params.ai_impact
        )