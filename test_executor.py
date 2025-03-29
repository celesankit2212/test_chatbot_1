 
import subprocess

def run_test():
    try:
        result = subprocess.run(["pytest", "tests/generated_test.py", "--tb=short", "-q"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)
