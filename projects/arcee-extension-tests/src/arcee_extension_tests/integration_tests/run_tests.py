import json
import sys
import pytest
import os
import argparse

def run_tests(test_folder_path: str, test_filter: str = None):
    absolute_path = os.path.abspath(test_folder_path)
    suite_name = os.path.basename(test_folder_path)
    logging_name = f"test_{suite_name}"
    
    if test_filter is not None:
        logging_name = f"{test_filter}"
    
    result_path = os.path.join(os.getcwd(), os.environ["TEST_RESULT_DIRECTORY"], "arcee_e2e", suite_name)
    
    log_file_path = os.path.join(result_path, f"{logging_name}.txt")
    json_file_path = os.path.join(result_path, f"{logging_name}.json")
    
    print(f"result_path: {result_path}")
    print(f"log_file_path: {log_file_path}")
    print(f"result_path exists: {os.path.exists(result_path)}")
    print(f"Current working directory: {os.getcwd()}")

    # Create the file if it doesn't exist
    os.makedirs(result_path, exist_ok=True)
    
    # Open the file in write mode to create it
    with open(log_file_path, 'w') as f:
        pass  # No content needed, just creating the file
    
    with open(json_file_path, 'w') as f:
        json.dump([], f)
    
    pytest_args = [
        '-rpP', 
        '-v', 
        f'--log-file={os.path.join(result_path, f"{logging_name}.log")}',
        f'--junitxml={os.path.join(result_path, f"{logging_name}.xml")}',
        '-o',
        f'junit_suite_name={suite_name}',  
        '-o',
        f'junit_family=xunit1',
        '--capture=no',
    ]

    if test_filter is not None:
        pytest_args.append('-k')
        pytest_args.append(f'{test_filter}')
    
    current_directory = os.getcwd()
    os.environ["SUITENAME"] = suite_name
    os.environ["JSON_FILE_PATH"] = json_file_path
    os.chdir(absolute_path)

    with open(log_file_path, 'w') as f:
        sys.stdout = f
        sys.stderr = f
        
        # Run pytest, now output will go to the file
        result = pytest.main(pytest_args)
    
    os.chdir(current_directory)
    # Checking the return code to determine the result of the test run
    return result

# Run the tests
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run tests using pytest.")
    parser.add_argument("--test-folder-path", required=True, help="Path to the folder containing the test files.")
    parser.add_argument("--test-filter", required=False, help="Filter to run specific tests.")
    
    args = parser.parse_args()
    result = run_tests(args.test_folder_path, args.test_filter)
    sys.exit(result)
