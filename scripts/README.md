# Scripts Directory

This directory contains utility scripts for setting up, configuring, and managing various aspects of the application environment. Below is an overview of each script along with usage instructions.

## Available Scripts

### 1. `init_env.py`
- **Description:**  
  Updates and prepares the environment keys file located at `/app/env/.env.keys`. This script ensures that API keys hints and configuration hints (for providers such as OpenAI, Anthropic, Cohere, Hugging Face, etc.) are included. 
- **Key Functions:**
  - `load_env_file(path: str) -> List[str]`: Reads an environment file and returns its lines.
  - `write_env_file(path: str, lines: List[str]) -> None`: Writes a list of strings back to the environment file.
  - `main() -> None`: Checks for various API keys in the file and appends missing hints.
- **Usage:**  
 The script is automatically mounted to the container and runs when you start the application. 

### 2. `install_docker_ubuntu.sh`
- **Description:**  
  A shell script to install Docker on Ubuntu systems. It:
  - Updates the package list and installs required dependencies.
  - Purges any previous Docker installations.
  - Configures Docker's repository and imports the GPG key.
  - Installs Docker Compose (standalone version v2.32.4).
- **Usage:**  
  ```bash
  ./scripts/install_docker_ubuntu.sh
  ```

### 3. `replacement_entrypoint.sh`
- **Description:**  
  A customizable Docker entrypoint script that can replace the default entrypoint in the container. This script serves as a template that you can modify to add custom initialization logic. The script is particularly useful when you need to:
  - Add custom setup steps before the main application starts
  - Modify container environment or permissions
  - Install additional dependencies
  - Run initialization scripts

- **Usage:**  
  1. Modify the script according to your needs
  2. Mount it to the container by updating your `docker-compose.yml`:
  ```yaml
  volumes:
    - ./scripts/replacement_entrypoint.sh:/usr/local/bin/entrypoint.sh
  entrypoint: [ "/usr/local/bin/entrypoint.sh" ]
  ```

- **Customization:**  
  The script can be modified to include various initialization tasks such as:
  - Environment setup
  - Permission adjustments
  - Dependency installation
  - Pre-startup checks
  - Custom initialization scripts

## General Notes


- **Administrative Privileges:**  
  Some scripts (e.g., Docker installation or modifying system users/groups) require root or sudo privileges.

- **Customization:**  
  These scripts are provided as a baseline and can be tailored to fit specific project requirements.

For further details, please refer to the inline comments provided within each script.
