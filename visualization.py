"""
Visualization components for Agile Teams Flow Metrics Simulation.
"""

import plotly.graph_objects as go
from typing import List
import numpy as np
from models import FlowMetrics

class FlowMetricsVisualizer:
    """Creates visualizations for flow metrics data."""
    
    # Visualization constants
    CHART_WIDTH = 1000
    CHART_HEIGHT = 600
    THRESHOLD_90 = 90
    THRESHOLD_95 = 95
    
    def __init__(self):
        self.colors = {
            'lead_time': 'red',
            'throughput': 'blue',
            'variability': 'orange',
            'threshold_90': 'black',
            'threshold_95': 'gray'
        }
    
    def create_flow_chart(self, metrics: FlowMetrics) -> go.Figure:
        """
        Create the main flow metrics chart.
        
        Args:
            metrics: Flow metrics data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Add main traces
        self._add_lead_time_trace(fig, metrics)
        self._add_throughput_trace(fig, metrics)
        self._add_variability_trace(fig, metrics)
        
        # Add threshold lines and annotations
        self._add_threshold_lines(fig, metrics)
        self._add_cost_annotation(fig, metrics)
        
        # Configure layout
        self._configure_layout(fig, metrics)
        
        return fig
    
    def _add_lead_time_trace(self, fig: go.Figure, metrics: FlowMetrics):
        """Add lead time trace to the figure."""
        fig.add_trace(go.Scatter(
            x=metrics.utilizations,
            y=metrics.lead_times,
            name="Lead Time (Days)",
            line=dict(color=self.colors['lead_time'], width=3),
            yaxis="y1",
            hovertemplate="Utilization: %{x:.1f}%<br>Lead Time: %{y:.1f} days<extra></extra>"
        ))
    
    def _add_throughput_trace(self, fig: go.Figure, metrics: FlowMetrics):
        """Add throughput trace to the figure."""
        fig.add_trace(go.Scatter(
            x=metrics.utilizations,
            y=metrics.throughputs,
            name="Throughput (Features/Sprint)",
            line=dict(color=self.colors['throughput'], width=3),
            yaxis="y2",
            hovertemplate="Utilization: %{x:.1f}%<br>Throughput: %{y:.1f} features<extra></extra>"
        ))
    
    def _add_variability_trace(self, fig: go.Figure, metrics: FlowMetrics):
        """Add schedule variability trace to the figure."""
        if not metrics.scaled_variabilities:
            return
            
        # Calculate marker sizes based on variability
        marker_sizes = self._calculate_marker_sizes(metrics.scaled_variabilities)
        
        fig.add_trace(go.Scatter(
            x=metrics.utilizations,
            y=metrics.scaled_variabilities,
            name="Schedule Variability",
            mode="markers",
            marker=dict(
                size=marker_sizes,
                color=self.colors['variability'],
                opacity=0.6,
                line=dict(width=1, color='darkorange')
            ),
            yaxis="y1",
            hovertemplate="Utilization: %{x:.1f}%<br>Variability: %{marker.size}<extra></extra>"
        ))
    
    def _calculate_marker_sizes(self, scaled_variabilities: List[float]) -> List[float]:
        """Calculate marker sizes for variability visualization."""
        if not scaled_variabilities:
            return []
            
        min_var = min(scaled_variabilities)
        max_var = max(scaled_variabilities)
        
        if max_var == min_var:
            return [5] * len(scaled_variabilities)
        
        # Scale to marker size range 2-12
        sizes = []
        for v in scaled_variabilities:
            normalized = (v - min_var) / (max_var - min_var)
            size = 2 + normalized * 10
            sizes.append(max(2, min(12, size)))
        
        return sizes
    
    def _add_threshold_lines(self, fig: go.Figure, metrics: FlowMetrics):
        """Add threshold lines at 90% and 95% utilization."""
        if not metrics.lead_times:
            return
            
        y_min = min(metrics.lead_times) * 0.9
        y_max = max(metrics.lead_times) * 1.1
        
        # 90% threshold
        fig.add_shape(
            type="line",
            x0=self.THRESHOLD_90, x1=self.THRESHOLD_90,
            y0=y_min, y1=y_max,
            line=dict(color=self.colors['threshold_90'], width=2, dash="dash"),
            yref="y1"
        )
        
        # 95% threshold
        fig.add_shape(
            type="line",
            x0=self.THRESHOLD_95, x1=self.THRESHOLD_95,
            y0=y_min, y1=y_max,
            line=dict(color=self.colors['threshold_95'], width=2, dash="dash"),
            yref="y1"
        )
    
    def _add_cost_annotation(self, fig: go.Figure, metrics: FlowMetrics):
        """Add cost impact annotation."""
        if not metrics.lead_times:
            return
            
        max_lead_time = max(metrics.lead_times)
        min_lead_time = min(metrics.lead_times)
        lead_time_increase = int(max_lead_time - min_lead_time)
        cost_impact = int(max_lead_time * 10)  # $10K per day assumption
        
        fig.add_annotation(
            x=self.THRESHOLD_95,
            y=max_lead_time * 0.8,
            text=f">90% Utilization: +{lead_time_increase} Days = ${cost_impact}K Loss",
            showarrow=True,
            arrowhead=2,
            ax=20,
            ay=-30,
            font=dict(color="black", size=12),
            yref="y1",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1
        )
    
    def _configure_layout(self, fig: go.Figure, metrics: FlowMetrics):
        """Configure the chart layout and styling."""
        y1_range = None
        y2_range = None
        
        if metrics.lead_times:
            y1_min = min(min(metrics.lead_times), 
                        min(metrics.scaled_variabilities) if metrics.scaled_variabilities else float('inf'))
            y1_max = max(max(metrics.lead_times),
                        max(metrics.scaled_variabilities) if metrics.scaled_variabilities else 0)
            y1_range = [y1_min * 0.9, y1_max * 1.2]
        
        if metrics.throughputs:
            y2_range = [min(metrics.throughputs) * 0.9, max(metrics.throughputs) * 1.2]
        
        fig.update_layout(
            title=dict(
                text="Impact of Utilization on Agile Team Flow Metrics",
                x=0.5,
                xanchor="center",
                font=dict(size=18, color="darkblue")
            ),
            xaxis=dict(
                title="Resource Utilization (%)",
                range=[50, 100],
                gridcolor="lightgray",
                tickfont=dict(size=12),
                title_font=dict(size=14)
            ),
            yaxis=dict(
                title="Lead Time (Days) / Variability",
                title_font=dict(color=self.colors['lead_time'], size=14),
                tickfont=dict(color=self.colors['lead_time'], size=12),
                gridcolor="lightgray",
                range=y1_range
            ),
            yaxis2=dict(
                title="Throughput (Features/Sprint)",
                title_font=dict(color=self.colors['throughput'], size=14),
                tickfont=dict(color=self.colors['throughput'], size=12),
                overlaying="y",
                side="right",
                range=y2_range
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="black",
                borderwidth=1,
                font=dict(size=12)
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=14),
            margin=dict(l=60, r=60, t=80, b=60),
            autosize=True,
            height=self.CHART_HEIGHT,
            width=self.CHART_WIDTH,
            hovermode='closest'
        )
        
        # Add threshold annotations
        if metrics.lead_times:
            max_lead_time = max(metrics.lead_times)
            fig.add_annotation(
                x=self.THRESHOLD_90,
                y=max_lead_time * 1.05,
                text="90% Threshold",
                showarrow=False,
                yref="y1",
                font=dict(size=12, color=self.colors['threshold_90'])
            )
            fig.add_annotation(
                x=self.THRESHOLD_95,
                y=max_lead_time * 1.05,
                text="95% Threshold",
                showarrow=False,
                yref="y1",
                font=dict(size=12, color=self.colors['threshold_95'])
            )

class ParameterImpactDescriptor:
    """Describes the impact of parameter changes on metrics."""
    
    @staticmethod
    def get_impact_description(parameter_name: str) -> str:
        """
        Get description of how a parameter affects flow metrics.
        
        Args:
            parameter_name: Name of the parameter that changed
            
        Returns:
            Description of the impact
        """
        impact_descriptions = {
            'teams': "Changing Number of Teams updates Utilization, Lead Time, Throughput, and Variability based on total resources.",
            'dev-count': "Changing Developers updates Utilization, Lead Time, and Throughput based on resource capacity with team count.",
            'dev-service': "Changing Developers Service Time updates Lead Time and Throughput based on service rate.",
            'test-count': "Changing Testers updates Utilization, Lead Time, and Throughput based on total resources.",
            'test-service': "Changing Testers Service Time updates Lead Time and Throughput based on service rate.",
            'arch-count': "Changing Architects updates Utilization, Lead Time, and Throughput based on dependency resolution.",
            'arch-service': "Changing Architects Service Time updates Lead Time and Throughput based on service rate.",
            'demand': "Changing Demand updates Utilization, Lead Time, and Throughput based on workload.",
            'proficiency': "Changing Proficiency updates Lead Time and Throughput based on service efficiency.",
            'defects': "Changing Defect Rate updates Lead Time, Throughput, and Variability based on rework.",
            'rework': "Changing Rework Factor updates Lead Time and Throughput based on additional work.",
            'dependencies': "Changing Dependencies updates Lead Time and Throughput based on capacity reduction.",
            'ai': "Changing AI Impact updates Lead Time, Throughput, and Variability based on knowledge/speed boost.",
            'goal-seek': "Goal seeking optimization has adjusted parameters to meet the specified target."
        }
        
        return impact_descriptions.get(parameter_name, "Parameter updated - metrics recalculated.")