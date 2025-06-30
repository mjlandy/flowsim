"""
UI components for Agile Teams Flow Metrics Simulation.
"""

from dash import dcc, html
from typing import Dict, Any, List, Tuple
from models import DEFAULT_PARAMS, TeamConfiguration

class UIComponentFactory:
    """Factory for creating UI components."""
    
    @staticmethod
    def create_header() -> html.Div:
        """Create the application header."""
        return html.Div([
            html.H1(
                "Agile Teams Flow Metrics Simulation",
                style={
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '30px',
                    'fontFamily': 'Arial, sans-serif'
                }
            )
        ])
    
    @staticmethod
    def create_legend_section() -> html.Div:
        """Create the legend and explanation section."""
        return html.Div([
            html.H3("Understanding the Metrics", style={'color': '#34495e'}),
            html.P("This simulation models Agile team performance using queuing theory and Little's Law (L = λW)."),
            html.Ul([
                html.Li([
                    html.Strong("Utilization (%)"), 
                    ": Resource usage level. Low (50%) = underutilized, High (100%) = saturated."
                ]),
                html.Li([
                    html.Strong("Lead Time (Days)"), 
                    ": Time from start to delivery. Low (2 days) = fast, High (>10 days) = delays."
                ]),
                html.Li([
                    html.Strong("Throughput (Features/Sprint)"), 
                    ": Features delivered. Low (0) = saturated, High (10) = optimal."
                ]),
                html.Li([
                    html.Strong("Schedule Variability"), 
                    ": Uncertainty in lead time. Low (small markers) = stable, High (large markers) = unpredictable."
                ])
            ]),
            html.P([
                "Based on queuing theory principles. Higher utilization leads to exponentially increasing lead times and variability."
            ], style={'fontStyle': 'italic', 'marginTop': '15px'})
        ], style={
            'padding': '15px',
            'border': '1px solid #bdc3c7',
            'borderRadius': '5px',
            'margin': '15px 0',
            'backgroundColor': '#ecf0f1'
        })

class ParameterControlFactory:
    """Factory for creating parameter control components."""
    
    def __init__(self):
        self.default_params = DEFAULT_PARAMS
    
    def create_goal_seeking_section(self) -> html.Div:
        """Create goal seeking controls."""
        return html.Div([
            html.H4("Goal Seeking Optimization", style={'color': '#2980b9', 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.Label("Target Utilization (%)", style={'fontWeight': 'bold'}),
                    dcc.Input(
                        id="target-util",
                        type="number",
                        value=80,
                        min=50,
                        max=100,
                        step=1,
                        style={'width': '100px', 'marginLeft': '10px'}
                    ),
                    html.Button(
                        "Optimize",
                        id="seek-util-btn",
                        n_clicks=0,
                        style={'marginLeft': '10px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'padding': '5px 10px', 'borderRadius': '3px'}
                    )
                ], style={'marginBottom': '10px'}),
                
                html.Div([
                    html.Label("Maximize Throughput", style={'fontWeight': 'bold'}),
                    html.Button(
                        "Optimize",
                        id="seek-flow-btn",
                        n_clicks=0,
                        style={'marginLeft': '10px', 'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none', 'padding': '5px 10px', 'borderRadius': '3px'}
                    )
                ], style={'marginBottom': '10px'}),
                
                html.Div([
                    html.Label("Minimize Variability", style={'fontWeight': 'bold'}),
                    html.Button(
                        "Optimize",
                        id="seek-stability-btn",
                        n_clicks=0,
                        style={'marginLeft': '10px', 'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none', 'padding': '5px 10px', 'borderRadius': '3px'}
                    )
                ])
            ])
        ], style={
            'padding': '15px',
            'border': '1px solid #3498db',
            'borderRadius': '5px',
            'margin': '15px 0',
            'backgroundColor': '#f8f9fa'
        })
    
    def create_team_configuration_section(self) -> html.Div:
        """Create team configuration controls."""
        return html.Div([
            html.H4("Team Configuration", style={'color': '#8e44ad', 'marginBottom': '15px'}),
            
            # Number of teams
            self._create_slider_with_permute(
                "Number of Teams",
                "teams-slider",
                "permute-teams-btn",
                min_val=1, max_val=40, step=1,
                value=self.default_params.teams,
                marks={i: str(i) for i in range(1, 41, 5)},
                description="Total teams working; more teams increase capacity"
            ),
            
            # Developers section
            html.H5("Developers", style={'color': '#e67e22', 'marginTop': '20px'}),
            self._create_slider_with_permute(
                "Count",
                "dev-count-slider",
                "permute-dev-btn",
                min_val=1, max_val=10, step=1,
                value=self.default_params.skill_sets["Developers"].count,
                marks={i: str(i) for i in range(1, 11)},
                description="Number of developers per team"
            ),
            self._create_range_slider_with_permute(
                "Service Time (Days/Feature)",
                "dev-service-slider",
                "permute-dev-service-btn",
                min_val=0.5, max_val=3.0, step=0.1,
                value=[self.default_params.skill_sets["Developers"].service_time_min,
                       self.default_params.skill_sets["Developers"].service_time_max],
                marks={i/2: str(i/2) for i in range(1, 7)},
                description="Range of task duration for developers"
            ),
            
            # Testers section
            html.H5("Testers", style={'color': '#e67e22', 'marginTop': '20px'}),
            self._create_slider_with_permute(
                "Count",
                "test-count-slider",
                "permute-test-btn",
                min_val=1, max_val=10, step=1,
                value=self.default_params.skill_sets["Testers"].count,
                marks={i: str(i) for i in range(1, 11)},
                description="Number of testers per team"
            ),
            self._create_range_slider_with_permute(
                "Service Time (Days/Feature)",
                "test-service-slider",
                "permute-test-service-btn",
                min_val=0.5, max_val=3.0, step=0.1,
                value=[self.default_params.skill_sets["Testers"].service_time_min,
                       self.default_params.skill_sets["Testers"].service_time_max],
                marks={i/2: str(i/2) for i in range(1, 7)},
                description="Range of task duration for testers"
            ),
            
            # Architects section
            html.H5("Architects", style={'color': '#e67e22', 'marginTop': '20px'}),
            self._create_slider_with_permute(
                "Count",
                "arch-count-slider",
                "permute-arch-btn",
                min_val=0, max_val=5, step=1,
                value=self.default_params.skill_sets["Architects"].count,
                marks={i: str(i) for i in range(0, 6)},
                description="Number of architects per team"
            ),
            self._create_range_slider_with_permute(
                "Service Time (Days/Feature)",
                "arch-service-slider",
                "permute-arch-service-btn",
                min_val=0.5, max_val=3.0, step=0.1,
                value=[self.default_params.skill_sets["Architects"].service_time_min,
                       self.default_params.skill_sets["Architects"].service_time_max],
                marks={i/2: str(i/2) for i in range(1, 7)},
                description="Range of task duration for architects"
            )
        ], style={
            'padding': '15px',
            'border': '1px solid #8e44ad',
            'borderRadius': '5px',
            'margin': '15px 0',
            'backgroundColor': '#f8f9fa'
        })
    
    def create_workload_section(self) -> html.Div:
        """Create workload configuration controls."""
        return html.Div([
            html.H4("Workload Parameters", style={'color': '#d35400', 'marginBottom': '15px'}),
            
            self._create_slider_with_permute(
                "Demand (Features/Sprint)",
                "demand-slider",
                "permute-demand-btn",
                min_val=5, max_val=20, step=1,
                value=self.default_params.demand,
                marks={i: str(i) for i in range(5, 21, 5)},
                description="Workload input; higher values increase utilization"
            ),
            
            self._create_slider_with_permute(
                "Domain Knowledge Proficiency (%)",
                "proficiency-slider",
                "permute-proficiency-btn",
                min_val=0.5, max_val=1.0, step=0.1,
                value=self.default_params.proficiency,
                marks={i/10: f"{i*10}%" for i in range(5, 11)},
                description="Skill efficiency; higher values enhance service rate"
            )
        ], style={
            'padding': '15px',
            'border': '1px solid #d35400',
            'borderRadius': '5px',
            'margin': '15px 0',
            'backgroundColor': '#f8f9fa'
        })
    
    def create_quality_section(self) -> html.Div:
        """Create quality-related controls."""
        return html.Div([
            html.H4("Quality Parameters", style={'color': '#c0392b', 'marginBottom': '15px'}),
            
            self._create_slider_with_permute(
                "Defect Rate (%)",
                "defects-slider",
                "permute-defects-btn",
                min_val=0.0, max_val=0.5, step=0.05,
                value=self.default_params.defects,
                marks={i/100: f"{i}%" for i in range(0, 51, 10)},
                description="Error frequency; higher values increase rework"
            ),
            
            self._create_slider_with_permute(
                "Rework Factor",
                "rework-slider",
                "permute-rework-btn",
                min_val=0.0, max_val=1.0, step=0.1,
                value=self.default_params.rework,
                marks={i/10: str(i/10) for i in range(0, 11, 2)},
                description="Extra work per defect; higher values delay delivery"
            )
        ], style={
            'padding': '15px',
            'border': '1px solid #c0392b',
            'borderRadius': '5px',
            'margin': '15px 0',
            'backgroundColor': '#f8f9fa'
        })
    
    def create_constraints_section(self) -> html.Div:
        """Create constraint-related controls."""
        return html.Div([
            html.H4("External Constraints", style={'color': '#7f8c8d', 'marginBottom': '15px'}),
            
            self._create_slider_with_permute(
                "Cross-Team Dependencies (%)",
                "dependencies-slider",
                "permute-dependencies-btn",
                min_val=0.0, max_val=0.5, step=0.05,
                value=self.default_params.dependencies,
                marks={i/100: f"{i}%" for i in range(0, 51, 10)},
                description="Delay from other teams; higher values reduce capacity"
            ),
            
            self._create_slider_with_permute(
                "AI Impact (%)",
                "ai-slider",
                "permute-ai-btn",
                min_val=0.0, max_val=0.5, step=0.05,
                value=self.default_params.ai_impact,
                marks={i/100: f"{i}%" for i in range(0, 51, 10)},
                description="Knowledge/speed boost; higher values reduce gaps and defects"
            )
        ], style={
            'padding': '15px',
            'border': '1px solid #7f8c8d',
            'borderRadius': '5px',
            'margin': '15px 0',
            'backgroundColor': '#f8f9fa'
        })
    
    def _create_slider_with_permute(self, label: str, slider_id: str, button_id: str,
                                   min_val: float, max_val: float, step: float,
                                   value: float, marks: Dict[float, str],
                                   description: str) -> html.Div:
        """Create a slider with permute button."""
        return html.Div([
            html.Label(label, style={'fontWeight': 'bold'}),
            html.Span(f" ({description})", style={'fontSize': '12px', 'color': '#7f8c8d'}),
            html.Div([
                dcc.Slider(
                    id=slider_id,
                    min=min_val,
                    max=max_val,
                    step=step,
                    value=value,
                    marks=marks,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Button(
                    "Cycle",
                    id=button_id,
                    n_clicks=0,
                    style={
                        'marginLeft': '10px',
                        'backgroundColor': '#95a5a6',
                        'color': 'white',
                        'border': 'none',
                        'padding': '3px 8px',
                        'borderRadius': '3px',
                        'fontSize': '12px'
                    }
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'marginBottom': '15px'})
    
    def _create_range_slider_with_permute(self, label: str, slider_id: str, button_id: str,
                                         min_val: float, max_val: float, step: float,
                                         value: List[float], marks: Dict[float, str],
                                         description: str) -> html.Div:
        """Create a range slider with permute button."""
        return html.Div([
            html.Label(label, style={'fontWeight': 'bold'}),
            html.Span(f" ({description})", style={'fontSize': '12px', 'color': '#7f8c8d'}),
            html.Div([
                dcc.RangeSlider(
                    id=slider_id,
                    min=min_val,
                    max=max_val,
                    step=step,
                    value=value,
                    marks=marks,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Button(
                    "Cycle",
                    id=button_id,
                    n_clicks=0,
                    style={
                        'marginLeft': '10px',
                        'backgroundColor': '#95a5a6',
                        'color': 'white',
                        'border': 'none',
                        'padding': '3px 8px',
                        'borderRadius': '3px',
                        'fontSize': '12px'
                    }
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'marginBottom': '15px'})

class NotificationComponents:
    """Components for displaying notifications and feedback."""
    
    @staticmethod
    def create_change_notification() -> html.Div:
        """Create the change notification area."""
        return html.Div(
            id="change-notification",
            style={
                'margin': '15px 0',
                'padding': '10px',
                'borderRadius': '5px',
                'backgroundColor': '#d4edda',
                'border': '1px solid #c3e6cb',
                'color': '#155724',
                'fontSize': '14px',
                'minHeight': '20px'
            }
        )

class LayoutBuilder:
    """Builds the complete application layout."""
    
    def __init__(self):
        self.ui_factory = UIComponentFactory()
        self.control_factory = ParameterControlFactory()
        self.notification = NotificationComponents()
    
    def build_layout(self) -> html.Div:
        """Build the complete application layout."""
        return html.Div([
            # Header
            self.ui_factory.create_header(),
            
            # Main chart
            dcc.Graph(
                id="flow-graph",
                style={'width': '100%', 'height': '600px', 'marginBottom': '20px'}
            ),
            
            # Change notification
            self.notification.create_change_notification(),
            
            # Legend section
            self.ui_factory.create_legend_section(),
            
            # Goal seeking section
            self.control_factory.create_goal_seeking_section(),
            
            # Parameter sections in a two-column layout
            html.Div([
                html.Div([
                    self.control_factory.create_team_configuration_section(),
                    self.control_factory.create_workload_section()
                ], className="six columns"),
                
                html.Div([
                    self.control_factory.create_quality_section(),
                    self.control_factory.create_constraints_section()
                ], className="six columns")
            ], className="row"),
            
            # Hidden inputs for goal seeking
            dcc.Input(id="target-util", type="hidden"),
            dcc.Input(id="target-flow", type="hidden"),
            dcc.Input(id="target-stability", type="hidden")
            
        ], style={
            'padding': '20px',
            'maxWidth': '1200px',
            'margin': 'auto',
            'fontFamily': 'Arial, sans-serif'
        })