"""
Main application entry point for Agile Teams Flow Metrics Simulation.
"""

import dash
from dash import dcc, html
import logging

from ui_components import LayoutBuilder
from callbacks import CallbackManager
from models import FlowMetricsCalculator, DEFAULT_PARAMS
from visualization import FlowMetricsVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgileFlowSimulationApp:
    """Main application class for the Agile Flow Metrics Simulation."""
    
    def __init__(self):
        """Initialize the application."""
        self.app = self._create_dash_app()
        self.layout_builder = LayoutBuilder()
        self.callback_manager = None
        
        self._setup_application()
    
    def _create_dash_app(self) -> dash.Dash:
        """Create and configure the Dash application."""
        app = dash.Dash(
            __name__,
            title="Agile Teams Flow Metrics Simulation",
            update_title=None,
            external_stylesheets=[
                'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css'
            ]
        )
        
        # Configure server
        app.server.config.update(
            SECRET_KEY='your-secret-key-here',  # Change in production
            SEND_FILE_MAX_AGE_DEFAULT=0  # Disable caching for development
        )
        
        return app
    
    def _setup_application(self):
        """Set up the application layout and callbacks."""
        try:
            # Set up layout
            self.app.layout = self.layout_builder.build_layout()
            
            # Initialize callbacks
            self.callback_manager = CallbackManager(self.app)
            
            logger.info("Application setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error setting up application: {str(e)}")
            self._setup_error_layout(str(e))
    
    def _setup_error_layout(self, error_msg: str):
        """Set up an error layout when application setup fails."""
        self.app.layout = html.Div([
            html.H1("Application Error", style={'color': 'red', 'textAlign': 'center'}),
            html.P(f"Failed to initialize application: {error_msg}"),
            html.P("Please check the logs for more details.")
        ], style={'padding': '50px', 'textAlign': 'center'})
    
    def run(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8050):
        """
        Run the application.
        
        Args:
            debug: Whether to run in debug mode
            host: Host to bind the server to
            port: Port to bind the server to
        """
        try:
            logger.info(f"Starting application on http://{host}:{port}")
            self.app.run_server(
                debug=debug,
                host=host,
                port=port,
                dev_tools_ui=debug,
                dev_tools_props_check=debug
            )
        except Exception as e:
            logger.error(f"Failed to start application: {str(e)}")
            raise

def create_initial_figure():
    """Create the initial figure for the application."""
    try:
        calculator = FlowMetricsCalculator()
        visualizer = FlowMetricsVisualizer()
        
        # Calculate initial metrics
        metrics = calculator.calculate_metrics(
            DEFAULT_PARAMS.to_hash_key(),
            DEFAULT_PARAMS
        )
        
        # Create initial figure
        return visualizer.create_flow_chart(metrics)
        
    except Exception as e:
        logger.error(f"Error creating initial figure: {str(e)}")
        # Return empty figure on error
        import plotly.graph_objects as go
        return go.Figure().add_annotation(
            text=f"Error loading initial data: {str(e)}",
            x=0.5, y=0.5,
            showarrow=False
        )

# Global application instance
app_instance = None

def get_app():
    """Get or create the global application instance."""
    global app_instance
    if app_instance is None:
        app_instance = AgileFlowSimulationApp()
    return app_instance

def main():
    """Main entry point for the application."""
    try:
        # Create and run the application
        app = get_app()
        app.run(debug=True)
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()