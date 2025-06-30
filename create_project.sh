#!/bin/bash

# Create Agile Flow Metrics Project
echo "Creating Agile Flow Metrics project..."

# Create main directory
mkdir -p agile-flow-metrics
cd agile-flow-metrics

# Create tests directory
mkdir -p tests

echo "Creating project files..."

# Create requirements.txt
cat > requirements.txt << 'EOF'
dash==2.14.1
plotly==5.17.0
numpy==1.24.3
pandas==2.0.3
EOF

# Initialize git repository
git init

echo "Project structure created successfully!"
echo "To complete setup:"
echo "1. Copy the file contents from the conversation"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Run the app: python app.py"
echo ""
echo "Files to create:"
echo "- models.py"
echo "- visualization.py" 
echo "- ui_components.py"
echo "- callbacks.py"
echo "- app.py"
echo "- tests/__init__.py"
echo "- tests/test_models.py"
echo "- README.md"