import os
import sys
import ast
import json
import importlib.util
import inspect

# Path configuration for tools folder and requirements file.
TOOLS_DIR = os.path.dirname(__file__)
REQUIREMENTS_FILE = os.path.join(TOOLS_DIR, 'requirements.txt')

def install_requirements():
    """
    Install the requirements specified in the requirements.txt file.
    This is a placeholder: you might call pip programmatically or ensure that
    the container/virtual environment installs requirements on startup.
    """
    if os.path.exists(REQUIREMENTS_FILE):
        # For demonstration, we simply print the command.
        # In a real environment, you might use subprocess to run:
        # subprocess.run([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
        print(f"Installing requirements from {REQUIREMENTS_FILE}...")
    else:
        print("No requirements.txt found.")


def load_module(module_path, module_name):
    """
    Dynamically load a module from a file.
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def auto_import_tools():
    """
    Auto-import all modules from TOOLS_DIR and return a dict mapping
    module names to module objects.
    """
    modules = {}
    if os.path.exists(TOOLS_DIR):
        for filename in os.listdir(TOOLS_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"agent_tools.{filename[:-3]}"
                module_path = os.path.join(TOOLS_DIR, filename)
                try:
                    module = load_module(module_path, module_name)
                    modules[module_name] = module
                except Exception as e:
                    print(f"Error loading module {module_name}: {e}")
    else:
        print(f"Tools directory {TOOLS_DIR} does not exist.")
    return modules


def tool_map():
    """
    Scans the auto-imported modules and inspects exported functions.
    Returns a JSON string mapping module names to their functions and argument specs.

    Example return format:
    {
      "agent_tools.toy_tools": {
          "generate_random_matrix": {
              "args": {"rows": "int", "cols": "int"}
          }
      }
    }
    """
    modules = auto_import_tools()
    mapping = {}

    for module_name, module in modules.items():
        functions = {}
        # Iterate through attributes of the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if inspect.isfunction(attr) and attr.__module__ == module.__name__:
                # Get signature of the function
                sig = inspect.signature(attr)
                args = {name: str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
                        for name, param in sig.parameters.items()}
                functions[attr_name] = {"args": args}
        if functions:
            mapping[module_name] = functions

    return json.dumps(mapping, indent=2)


def validate_code(code_str):
    """
    Validates the submitted Python code by trying to parse it.
    Returns a tuple: (True, None) if valid, else (False, error_message).
    """
    try:
        ast.parse(code_str)
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"


def add_to_module(module_name, code_str):
    """
    Validates and appends the submitted code to the specified module.

    Parameters:
      - module_name: the target module (e.g., "agent_tools.toy_tools")
      - code_str: the Python code to be added

    Returns a dict with the result.
    """
    # Validate code first.
    valid, error = validate_code(code_str)
    if not valid:
        return {"success": False, "error": error}

    # Determine the file path from module_name.
    parts = module_name.split('.')
    if parts[0] != 'agent_tools' or len(parts) != 2:
        return {"success": False, "error": "Invalid module name. Must be in 'agent_tools' folder."}

    filename = f"{parts[1]}.py"
    file_path = os.path.join(TOOLS_DIR, filename)

    if not os.path.exists(file_path):
        return {"success": False, "error": f"Module file {filename} does not exist."}

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + code_str)
        return {"success": True, "message": "Code added successfully."}
    except Exception as e:
        return {"success": False, "error": f"Error writing to file: {e}"}


def get_requirements():
    """
    Reads the requirements.txt file and returns a dict.
    For simplicity, this assumes each line is in the format 'package==version'
    """
    reqs = {}
    if os.path.exists(REQUIREMENTS_FILE):
        with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "==" in line:
                        pkg, version = line.split("==", 1)
                        reqs[pkg.strip()] = version.strip()
                    else:
                        reqs[line] = None
    else:
        print("No requirements.txt found.")
    return reqs


def set_requirements(reqs_dict):
    """
    Writes the given requirements dict to the requirements.txt file.
    The dict format should be: {package: version or None}.
    If version is None, writes only the package name.
    """
    lines = []
    for pkg, version in reqs_dict.items():
        if version:
            lines.append(f"{pkg}=={version}")
        else:
            lines.append(pkg)
    try:
        with open(REQUIREMENTS_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return {"success": True, "message": "requirements.txt updated successfully."}
    except Exception as e:
        return {"success": False, "error": f"Error writing to requirements.txt: {e}"}


# When the application starts, install requirements and auto-import tools.
if __name__ == "__main__":
    install_requirements()
    # For demonstration, print the tool map.
    print("Tool Map:")
    print(tool_map())
