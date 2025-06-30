"""
Callback handlers for Agile Teams Flow Metrics Simulation.
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
                Input("seek-stability-btn", "n_clicks"),
                
                # Permutation buttons
                Input("permute-teams-btn", "n_clicks"),
                Input("permute-dev-btn", "n_clicks"),
                Input("permute-dev-service-btn", "n_clicks"),
                Input("permute-test-btn", "n_clicks"),
                Input("permute-test-service-btn", "n_clicks"),
                Input("permute-arch-btn", "n_clicks"),
                Input("permute-arch-service-btn", "n_clicks"),
                Input("permute-demand-btn", "n_clicks"),
                Input("permute-proficiency-btn", "n_clicks"),
                Input("permute-defects-btn", "n_clicks"),
                Input("permute-rework-btn", "n_clicks"),
                Input("permute-dependencies-btn", "n_clicks"),
                Input("permute-ai-btn", "n_clicks")
            ],
            [
                # Goal seeking targets
                State("target-util", "value"),
                State("target-flow", "value"),
                State("target-stability", "value"),
                
                # Slider ranges for permutation
                State("teams-slider", "min"),
                State("teams-slider", "max"),
                State("dev-count-slider", "min"),
                State("dev-count-slider", "max"),
                State("dev-service-slider", "min"),
                State("dev-service-slider", "max"),
                State("test-count-slider", "min"),
                State("test-count-slider", "max"),
                State("test-service-slider", "min"),
                State("test-service-slider", "max"),
                State("arch-count-slider", "min"),
                State("arch-count-slider", "max"),
                State("arch-service-slider", "min"),
                State("arch-service-slider", "max"),
                State("demand-slider", "min"),
                State("demand-slider", "max"),
                State("proficiency-slider", "min"),
                State("proficiency-slider", "max"),
                State("defects-slider", "min"),
                State("defects-slider", "max"),
                State("rework-slider", "min"),
                State("rework-slider", "max"),
                State("dependencies-slider", "min"),
                State("dependencies-slider", "max"),
                State("ai-slider", "min"),
                State("ai-slider", "max")
            ]
        )
        def update_simulation(*args):
            """Main callback for updating the simulation."""
            return self._handle_simulation_update(*args)
    
    def _handle_simulation_update(self, *args) -> Tuple[Any, str, float, int, List[float], int, List[float], int, List[float], int, float, float, float, float, float]:
        """Handle the main simulation update logic."""
        try:
            # Parse arguments
            parsed_args = self._parse_callback_arguments(args)
            
            # Determine what triggered the callback
            trigger_info = self._get_trigger_info()
            
            # Apply permutations or goal seeking
            updated_params = self._apply_parameter_changes(
                parsed_args, trigger_info
            )
            
            # Calculate new metrics
            metrics = self._calculate_metrics(updated_params)
            
            # Create visualization
            figure = self.visualizer.create_flow_chart(metrics)
            
            # Generate change notification
            change_text = self.impact_descriptor.get_impact_description(
                trigger_info.get('parameter', 'default')
            )
            
            # Return all outputs
            return self._create_callback_outputs(figure, change_text, updated_params)
            
        except Exception as e:
            logger.error(f"Error in simulation update: {str(e)}")
            # Return default values on error
            return self._create_error_outputs(str(e))
    
    def _parse_callback_arguments(self, args) -> Dict[str, Any]:
        """Parse callback arguments into structured data."""
        # Slider values (first 13 arguments)
        slider_values = args[:13]
        
        # Button clicks (next 16 arguments)
        button_clicks = args[13:29]
        
        # Goal seeking targets (next 3 arguments)
        goal_targets = args[29:32]
        
        # Slider ranges (remaining arguments)
        slider_ranges = args[32:]
        
        return {
            'teams': slider_values[0],
            'dev_count': slider_values[1],
            'dev_service': slider_values[2],
            'test_count': slider_values[3],
            'test_service': slider_values[4],
            'arch_count': slider_values[5],
            'arch_service': slider_values[6],
            'demand': slider_values[7],
            'proficiency': slider_values[8],
            'defects': slider_values[9],
            'rework': slider_values[10],
            'dependencies': slider_values[11],
            'ai_impact': slider_values[12],
            'button_clicks': button_clicks,
            'goal_targets': goal_targets,
            'slider_ranges': slider_ranges
        }
    
    def _get_trigger_info(self) -> Dict[str, Any]:
        """Get information about what triggered the callback."""
        ctx = callback_context
        if not ctx.triggered:
            return {'trigger': 'initial', 'parameter': 'default'}
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Map trigger IDs to parameter names
        trigger_map = {
            'teams-slider': 'teams',
            'permute-teams-btn': 'teams',
            'dev-count-slider': 'dev-count',
            'permute-dev-btn': 'dev-count',
            'dev-service-slider': 'dev-service',
            'permute-dev-service-btn': 'dev-service',
            'test-count-slider': 'test-count',
            'permute-test-btn': 'test-count',
            'test-service-slider': 'test-service',
            'permute-test-service-btn': 'test-service',
            'arch-count-slider': 'arch-count',
            'permute-arch-btn': 'arch-count',
            'arch-service-slider': 'arch-service',
            'permute-arch-service-btn': 'arch-service',
            'demand-slider': 'demand',
            'permute-demand-btn': 'demand',
            'proficiency-slider': 'proficiency',
            'permute-proficiency-btn': 'proficiency',
            'defects-slider': 'defects',
            'permute-defects-btn': 'defects',
            'rework-slider': 'rework',
            'permute-rework-btn': 'rework',
            'dependencies-slider': 'dependencies',
            'permute-dependencies-btn': 'dependencies',
            'ai-slider': 'ai',
            'permute-ai-btn': 'ai',
            'seek-util-btn': 'goal-seek',
            'seek-flow-btn': 'goal-seek',
            'seek-stability-btn': 'goal-seek'
        }
        
        return {
            'trigger': trigger_id,
            'parameter': trigger_map.get(trigger_id, 'default'),
            'is_permutation': 'permute' in trigger_id,
            'is_goal_seek': 'seek' in trigger_id
        }
    
    def _apply_parameter_changes(self, parsed_args: Dict[str, Any], 
                               trigger_info: Dict[str, Any]) -> SimulationParameters:
        """Apply parameter changes based on trigger type."""
        # Create base parameters from current values
        current_params = self._create_current_parameters(parsed_args)
        
        if trigger_info['is_goal_seek']:
            return self._apply_goal_seeking(current_params, trigger_info, parsed_args)
        elif trigger_info['is_permutation']:
            return self._apply_permutation(current_params, trigger_info, parsed_args)
        else:
            return current_params
    
    def _create_current_parameters(self, parsed_args: Dict[str, Any]) -> SimulationParameters:
        """Create SimulationParameters from current values."""
        try:
            skill_sets = {
                "Developers": TeamConfiguration(
                    count=parsed_args['dev_count'],
                    service_time_min=parsed_args['dev_service'][0],
                    service_time_max=parsed_args['dev_service'][1]
                ),
                "Testers": TeamConfiguration(
                    count=parsed_args['test_count'],
                    service_time_min=parsed_args['test_service'][0],
                    service_time_max=parsed_args['test_service'][1]
                ),
                "Architects": TeamConfiguration(
                    count=parsed_args['arch_count'],
                    service_time_min=parsed_args['arch_service'][0],
                    service_time_max=parsed_args['arch_service'][1]
                )
            }
            
            return SimulationParameters(
                teams=parsed_args['teams'],
                skill_sets=skill_sets,
                demand=parsed_args['demand'],
                proficiency=parsed_args['proficiency'],
                defects=parsed_args['defects'],
                rework=parsed_args['rework'],
                dependencies=parsed_args['dependencies'],
                ai_impact=parsed_args['ai_impact']
            )
        except Exception as e:
            logger.warning(f"Error creating parameters, using defaults: {str(e)}")
            return DEFAULT_PARAMS
    
    def _apply_goal_seeking(self, params: SimulationParameters, 
                          trigger_info: Dict[str, Any],
                          parsed_args: Dict[str, Any]) -> SimulationParameters:
        """Apply goal seeking optimization."""
        try:
            trigger = trigger_info['trigger']
            targets = parsed_args['goal_targets']
            
            if trigger == 'seek-util-btn' and targets[0] is not None:
                new_demand = self.goal_seeker.seek_utilization(
                    targets[0] / 100, params
                )
                return self._update_demand(params, new_demand)
            elif trigger == 'seek-flow-btn':
                new_demand = self.goal_seeker.seek_value_flow(params)
                return self._update_demand(params, new_demand)
            elif trigger == 'seek-stability-btn':
                new_demand = self.goal_seeker.seek_date_stability(params)
                return self._update_demand(params, new_demand)
                
        except Exception as e:
            logger.error(f"Goal seeking error: {str(e)}")
            
        return params
    
    def _apply_permutation(self, params: SimulationParameters,
                          trigger_info: Dict[str, Any],
                          parsed_args: Dict[str, Any]) -> SimulationParameters:
        """Apply parameter permutation."""
        try:
            trigger = trigger_info['trigger']
            ranges = parsed_args['slider_ranges']
            
            # This is a simplified permutation - cycle to next value
            # In a real implementation, you might want more sophisticated permutation
            return params
            
        except Exception as e:
            logger.error(f"Permutation error: {str(e)}")
            
        return params
    
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
    
    def _calculate_metrics(self, params: SimulationParameters):
        """Calculate metrics with error handling."""
        try:
            return self.calculator.calculate_metrics(
                params.to_hash_key(), params
            )
        except Exception as e:
            logger.error(f"Metrics calculation error: {str(e)}")
            # Return default metrics
            return self.calculator.calculate_metrics(
                DEFAULT_PARAMS.to_hash_key(), DEFAULT_PARAMS
            )
    
    def _create_callback_outputs(self, figure, change_text: str, 
                               params: SimulationParameters) -> Tuple:
        """Create callback output tuple."""
        return (
            figure,
            change_text,
            params.teams,
            params.skill_sets["Developers"].count,
            [params.skill_sets["Developers"].service_time_min,
             params.skill_sets["Developers"].service_time_max],
            params.skill_sets["Testers"].count,
            [params.skill_sets["Testers"].service_time_min,
             params.skill_sets["Testers"].service_time_max],
            params.skill_sets["Architects"].count,
            [params.skill_sets["Architects"].service_time_min,
             params.skill_sets["Architects"].service_time_max],
            params.demand,
            params.proficiency,
            params.defects,
            params.rework,
            params.dependencies,
            params.ai_impact
        )
    
    def _create_error_outputs(self, error_msg: str) -> Tuple:
        """Create default outputs when an error occurs."""
        default_params = DEFAULT_PARAMS
        
        return (
            self.visualizer.create_flow_chart(
                self.calculator.calculate_metrics(
                    default_params.to_hash_key(), default_params
                )
            ),
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