import os
import sys

# Add the project's root directory and Lambda Layer's path to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

lambda_layer_path = os.path.join(project_root, 'api', 'layers', 'api_layer', 'python', 'lib', 'python3.9', 'site-packages')
sys.path.insert(0, lambda_layer_path)

lambda_layer_path = os.path.join(project_root, 'shared_layers', 'core_layer',  'python', 'lib', 'python3.9', 'site-packages')
sys.path.insert(0, lambda_layer_path)
