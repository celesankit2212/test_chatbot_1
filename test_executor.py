
import pytest

def run_test():
    try:
        result = pytest.main(["tests/test_generated.py", "-q", "--tb=short"])
        return "Test Passed" if result == 0 else "Test Failed"
    except Exception as e:
        return f"Error during test run: {str(e)}"
