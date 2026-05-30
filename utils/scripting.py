import subprocess
import os
import sys

class ScriptingTools:
    @staticmethod
    def execute_python_code(code: str) -> str:
        """
        Executes a Python script locally and returns the output.
        Args:
            code: The Python code to execute.
        """
        try:
            os.makedirs("assets/scripts", exist_ok=True)
            script_path = "assets/scripts/temp_script.py"
            with open(script_path, "w") as f:
                f.write(code)

            # Execute with a timeout for safety
            # Use sys.executable to ensure we use the same python interpreter
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout
            errors = result.stderr

            if errors:
                return f"I ran the script, but encountered some errors, Sir:\n{errors}\nOutput:\n{output}"
            return f"Execution complete, Sir. Here is the output:\n{output}"

        except subprocess.TimeoutExpired:
            return "The script was terminated as it exceeded the 30-second time limit, Sir."
        except Exception as e:
            return f"I failed to execute the script, Sir. Error: {str(e)}"

scripting_tools_list = [ScriptingTools.execute_python_code]
