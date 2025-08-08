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

### 3. `meilisearch_dump.py`
- **Description:**  
  A comprehensive tool for creating MeiliSearch dumps **AND** exporting data between instances. This script now supports both traditional dump creation and the new Meilisearch 1.16+ export functionality for direct instance-to-instance migration.

- **Key Features:**
  - **🆕 EXPORT MODE (Meilisearch 1.16+):** Direct instance-to-instance migration without dump files
  - **DUMP MODE (Traditional):** Creates timestamped backup files with monitoring
  - Conflict resolution: additive operations with document replacement
  - Selective export with index patterns and filters
  - Settings override capabilities for target instances
  - Configurable payload sizes for performance optimization
  - Detailed timing information and progress feedback

- **Usage:**  

  **🚀 Export Mode (NEW - Recommended for 1.16+)**
  ```bash
  # Basic export to another instance
  uv run scripts/meilisearch_dump.py --export \
    --target-url "http://production.example.com:7700" \
    --target-api-key "target_master_key"
  
  # Export specific indexes with settings override
  uv run scripts/meilisearch_dump.py --export \
    --target-url "http://staging.example.com:7700" \
    --target-api-key "staging_key" \
    --index-patterns "products,users*" \
    --override-settings \
    --payload-size "100MiB"
  
  # Export with document filtering
  uv run scripts/meilisearch_dump.py --export \
    --target-url "http://dev.example.com:7700" \
    --target-api-key "dev_key" \
    --filter "status = 'active'" \
    --index-patterns "products"
  ```

  **📁 Dump Mode (Traditional)**
  ```bash
  # Basic dump creation (uses environment defaults)
  uv run scripts/meilisearch_dump.py
  
  # With custom connection settings
  uv run scripts/meilisearch_dump.py --host localhost --port 7700 --api-key your_key
  
  # Custom dumps folder path
  uv run scripts/meilisearch_dump.py --dumps-path /custom/dumps/path
  ```

- **Important Notes:**

  **🆕 Export Mode (Meilisearch 1.16+):**
  - ✅ **No file management required** - direct instance-to-instance transfer
  - ✅ **Additive operation** - existing data is preserved, duplicates are replaced
  - ✅ **Real-time migration** - no intermediate files or manual import steps
  - ⚠️ **Requires target instance API access** - ensure target is accessible and has proper API key
  - ⚠️ **Network connectivity required** during the entire export process
  - 🐳 **Docker networking**: Use `172.17.0.1` (host gateway) instead of `localhost` for container-to-host communication
  - 🔒 **Version requirement**: Both source and target instances MUST be Meilisearch 1.16.0 or higher

  **📁 Dump Mode (Traditional):**
  - **Critical**: Creates dumps with datetime format, but MeiliSearch import expects `just_chat_rag.dump`
  - Always rename the latest dump for import: `cp ./dumps/YYYYMMDD-HHMMSS.dump ./dumps/just_chat_rag.dump`
  - Environment variables: `MEILISEARCH_HOST`, `MEILISEARCH_PORT`, `MEILI_MASTER_KEY`
  - Dump files are saved to `./dumps/` directory by default

- **Migration Workflows:**

  **🚀 Modern Workflow (Export Mode - Recommended)**
  1. Run export command with target instance details
  2. Data is directly migrated - no additional steps required!
  
  **📁 Traditional Workflow (Dump Mode)**
  1. Run the script to create a timestamped dump
  2. Rename the latest dump to `just_chat_rag.dump` for import compatibility
  3. Transfer to target environment if needed
  4. Use `docker compose up -V` to import the dump

- **Updating to Meilisearch 1.16+ for Export Features:**
  ```bash
  # Update your docker-compose.yml to use Meilisearch 1.16+
  # services:
  #   meilisearch:
  #     image: getmeili/meilisearch:v1.16.0
  
  # Pull and restart with updated image
  docker compose pull
  docker compose up -d
  
  # Verify version
  curl "http://localhost:7700/version"
  ```

### 4. `replacement_entrypoint.sh`
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
