import sys
import yaml
import os
import argparse
from scheduler import app

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Test Runner')
    parser.add_argument('--config', '-c', 
                       default='config.yaml',
                       help='Path to config file (default: config.yaml)')
    
    args = parser.parse_args()
    
    try:
        print(f"Loading config from '{args.config}'")
        config = load_config(args.config)

        print("Setting environment variables...")   
        # Set environment variables
        for key, value in config.get('environment', {}).items():
            os.environ[key] = str(value)
        
        # Call Scheduler to run tests
        print("Starting test execution via Scheduler...")
        yaml_filename = "test_scheduling.yaml"

        try:
            app.run(yaml_filename)
        except Exception as ex:
            print(f"Failure occurred during scheduler run - {ex}")
            sys.exit(1)

    except FileNotFoundError:
        print(f"Config file '{args.config}' not found!")
        sys.exit(1)

if __name__ == "__main__":
    main()