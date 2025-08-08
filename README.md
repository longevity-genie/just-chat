# just-chat
Make your LLM agent and chat with it simple and fast!

![Easy chat with your Agent](images/screenshot.jpg)
*Setting up your agent and your chat in few clicks*

## Quick start

Just clone repository and run docker-compose!
```bash
git clone git@github.com:longevity-genie/just-chat.git
USER_ID=$(id -u) GROUP_ID=$(id -g) docker-compose up
```
And the chat with your agent is ready to go! Open `http://localhost:3000` in your browser and start chatting with your agent!
Note: container will be started with the user and group of the host machine to avoid permission issues. If you want to change this, you can modify the `USER_ID` and `GROUP_ID` variables in the `docker-compose.yml` file.

If you prefer Podman or use RPM-based distro where it is the default option, you can use alternative Podman installation:
```bash
git clone git@github.com:longevity-genie/just-chat.git
podman-compose up 
```
Unlike Docker, Podman is rootless-by-design maps user and group id automatically. 
NB! Ubuntu 22 contains podman v.3 which is not fully compatible with this setup, assume podman v4.9.3 or higher is required.



You can customize your setup by:
1. Editing `chat_agent_profiles.yaml` to customize your agent
2. Adding tools to `/agent_tools` directory to empower your agent
3. Modifying `docker-compose.yml` for advanced settings (optional)

The only requirement is Docker (or Podman, both are supported)! We provide detailed installation instructions for both Linux and Windows in the [Installation](#installation) section.
Also check the [notes](#some-notes) section for further information.


## What can you do with Just-Chat?
- 🚀 Start chatting with one command ( docker-compose up )
- 🤖 Customize your AI assistant using a YAML file (can be edited with a text editor)
- 🛠️ Add new capabilities with Python tools (can add additional functions and libraries)
- 🌐 Talk with agent with a chat web interface at 0.0.0.0:3000
- 🐳 Run everything in Docker containers
- 📦 Works without Python or Node.js on your system


We use [just-agents](https://github.com/longevity-genie/just-agents) library to initialize agents from YAML, so most of the modern models ( DeepSeek Reasoner, ChatGPT, LLAMA3.3, etc.) are supported. 
However, you might need to add your own keys to the environment variables. We provide a free Groq key by default but it is very rate-limited. We recommend getting your own keys,  [Groq](https://console.groq.com/playground) can be a good place to start as it is free and contains many open-source models.

## What if I want to use Podman instead of Docker?

Podman is a safer container environment than Docker. If you prefer Podman or use Fedora or any other RPM-based Linux distribution, you can use it instead of Docker:
```bash
git clone https://github.com/winternewt/just-chat.git
podman compose up 
```
Unlike Docker, Podman is rootless-by-design and maps user and group id automatically. 

⚠️ **NOTE**: Ubuntu versions have different Podman availability:

- **Ubuntu 24.04+**: Podman v4.9.3+ available via apt (recommended)
- **Ubuntu 22.04**: Contains old Podman v.3 in apt, requires manual installation
- Our installation script handles this automatically for Ubuntu 22.04

The only requirement is Docker (or Podman, both are supported)! We provide detailed installation instructions for both Linux and Windows in the [Installation](#installation) section.
Also check the [notes](#some-notes) section for further information.

## Project Structure

- [`chat_agent_profiles.yaml`](chat_agent_profiles.yaml) - Configure your agents, their personalities and capabilities, example agents provided.
- [`/agent_tools/`](agent_tools/README.md) - Python tools to extend agent capabilities. Contains example tools and instructions for adding your own tools with custom dependencies.
- [`/data/`](data/README.md) - Application data storage if you want to let your agent work with additional data.
- [`docker-compose.yml`](docker-compose.yml) - Container orchestration and service configuration.
- [`/env/`](env/README.md) - Environment configuration files and settings.
- [`images/`](images/README.md) - Images for the README.
- [`/logs/`](logs/README.md) - Application logs.
- [`/scripts/`](scripts/README.md) - Utility scripts including Docker installation helpers.
- [`/volumes/`](volumes/README.md) - Docker volume mounts for persistent storage.
- `/logs/` - Application logs. We use eliot library for logging

Note: Each folder contains additional README file with more information about the folder contents!

## Installation

Just-Chat is a containerized application. To run it you can use either Docker or Podman.
You can skip this section if you already have any of them installed. If you do not have a preference we recommend Podman as more modern and secure container engine.

Detailed docker instructions:
<details>
<summary>Docker Installation on Linux</summary>

### Install Docker and Docker-compose Standalone

Refer to the official guides: 
 - [Docker Installation Guide](https://docs.docker.com/engine/install/ubuntu/).
 - [Docker Compose Standalone Installation Guide](https://docs.docker.com/compose/install/standalone/).
 
For Ubuntu 22.04+ users, you can use our automated installation script:
```bash
sudo ./scripts/install_docker_ubuntu.sh
```
This script automatically handles Docker installation and Podman v4+ (builds from source on 22.04, installs from apt on 24.04+).

Or follow these manual steps:

#### Setup Docker's apt repository
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

#### Install latest Docker packages
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
```

Note: at many systems it can be `docker compose` (without `-`)

</details>

<details>
<summary>Docker Installation on Windows</summary>

### Prerequisites
- Windows 10 (Pro, Enterprise, Education) Version 1909 or later
- Windows 11 (any edition)
- WSL 2 (Windows Subsystem for Linux) enabled (recommended) - [WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- Hyper-V enabled (if using Windows 10 Pro/Enterprise)
- At least 4GB of RAM (recommended)

### Installation Steps
1. Download [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
2. Run the installer and follow the prompts
3. Restart your PC
4. Launch Docker Desktop
5. Docker Compose is included with Docker Desktop

For detailed instructions and troubleshooting, see the [official Windows installation guide](https://docs.docker.com/desktop/install/windows-install/).
</details>

<details>

If you prefer Podman, you can use the following instructions:

<summary>Podman Installation on Linux</summary>

### Ubuntu 24.04+ (Recommended - Simple Installation)
Modern Ubuntu versions have Podman v4.9.3+ in their repositories:
```bash
# Install Podman
sudo apt-get update
sudo apt-get install -y podman

# Install Python3 and pip if not already installed
sudo apt-get install -y python3 python3-pip

# Install Podman Compose (using pipx to avoid PEP 668 issues)
pipx install podman-compose
```

### Ubuntu 22.04 LTS (Legacy - Complex Installation)

**Option 1: Use our automated script (RECOMMENDED)**
```bash
sudo ./scripts/install_docker_ubuntu.sh
```
This automatically installs Docker and builds/installs Podman v4.9.3 from source with all dependencies.

**Option 2: Manual installation**
You will have to build Podman from source due to outdated go-lang version in Ubuntu 22.04 LTS. You'll need to add a PPA repository and install newer go-lang plus dependencies:

```bash
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt update
sudo sysctl kernel.unprivileged_userns_clone=1
sudo apt install git build-essential btrfs-progs gcc git golang-go go-md2man iptables libassuan-dev libbtrfs-dev libc6-dev libdevmapper-dev libglib2.0-dev libgpgme-dev libgpg-error-dev libprotobuf-dev libprotobuf-c-dev libseccomp-dev libselinux1-dev libsystemd-dev make containernetworking-plugins pkg-config uidmap
sudo apt install runc # only if you don't have docker installed
```

Clone the podman repository and checkout the latest stable version from 24 LTS:
```bash
git clone https://github.com/containers/podman.git
cd podman/
git checkout v4.9.3
make
sudo make install
podman --version
```

For other Linux distributions, refer to:
- [Podman Installation Guide](https://podman.io/docs/installation)
- [Podman Compose Installation Guide](https://github.com/containers/podman-compose)
</details>

<details>
<summary>Podman Installation on Windows</summary>

### Prerequisites
- Windows 10/11
- WSL 2 enabled
- 4GB RAM (recommended)

### Installation Steps
1. Download and install [Podman Desktop](https://podman-desktop.io/downloads)
2. Initialize Podman:
```powershell
podman machine init
podman machine start
```
3. Install Podman Compose:
```powershell
pip3 install podman-compose
```

For detailed instructions, see the [official Podman documentation](https://podman.io/docs/installation#windows).
</details>

## Clone Just-Chat repository
```bash
git clone https://github.com/winternewt/just-chat.git
```

## Start the application
```bash
USER_ID=$(id -u) GROUP_ID=$(id -g) docker-compose up
```
Note: Here we use USER_ID=$(id -u) GROUP_ID=$(id -g) to run as current user instead of root, but if it does not matter for you can simply run docker-compose up
We also provide experimental start and stop bash (for Linux) and bat (for Windows) scripts.

## Using Semantic Search with MeiliSearch

Just-Chat provides semantic search capabilities using MeiliSearch, which allows your agent to find and reference relevant information from documents based on meaning rather than just keywords:

1. After starting the application, access the API documentation at `localhost:9000/docs`
2. Use the API to index markdown files (use try it out button):
   - Example: Index the included GlucoseDAO markdown files to the "glucosedao" index:  
     `/index_markdown` for the `/app/data/glucosedao_markdown` folder
3. Enable semantic search in your agent:
   - Uncomment the system prompt sections in `chat_agent_profiles.yaml` corresponding to search
   - Set the index to "glucosedao" (or your custom index name if you indexed other content)

Note: the container has everything that you copy to ./data folder as /app/data/

This feature allows your agent to search and reference specific knowledge bases during conversations.

### MeiliSearch Dumps - Import & Export

Just-Chat includes a convenient tool for creating and importing MeiliSearch dumps, allowing you to backup and restore your search indexes. Due to MeiliSearch limitations, this is the primary way to synchronize search data between environments.

#### Creating a Dump

Use the provided dump script to create a backup of your MeiliSearch data:

```bash
# Create a dump (saved to ./dumps/ folder)
python3 scripts/meilisearch_dump.py

# With custom settings
python3 scripts/meilisearch_dump.py --host localhost --port 7700 --api-key your_key
```

#### Common Use Case Scenarios

##### Scenario A: Development to Production Workflow

**Step-by-step process for moving updated indices from development to production:**

1. **On Development Environment:**
   ```bash
   # After updating your indices with new data/documents
   # Create a dump of your current indices
   python3 scripts/meilisearch_dump.py
   
   # The script creates dumps with datetime format (e.g., 20250714-212239660.dump)
   # Check ./dumps/ folder for the latest dump file
   ls -la ./dumps/
   
   # Rename the latest dump to the expected import name
   # Find the most recent dump and rename it
   LATEST_DUMP=$(ls -t ./dumps/*.dump | head -n1 | xargs basename)
   cp ./dumps/$LATEST_DUMP ./dumps/just_chat_rag.dump
   
   # Or manually if you prefer:
   # cp ./dumps/20250714-212239660.dump ./dumps/just_chat_rag.dump
   ```

2. **Transfer Dump to Production:**
   ```bash
   # Copy dump file to production environment
   scp ./dumps/just_chat_rag.dump user@production-host:/path/to/just-chat/dumps/
   
   # Or using rsync for better transfer control:
   rsync -avz ./dumps/just_chat_rag.dump user@production-host:/path/to/just-chat/dumps/
   
   # For local environments, you might simply copy to a shared location:
   cp ./dumps/just_chat_rag.dump /shared/path/to/production/dumps/
   ```

3. **On Production Environment:**
   ```bash
   # Navigate to your just-chat directory
   cd /path/to/just-chat
   
   # Verify the dump file is present and properly named
   # MeiliSearch expects the dump file to be named exactly 'just_chat_rag.dump'
   ls -la ./dumps/just_chat_rag.dump
   
   # Stop the current services
   docker compose down
   
   # Start with volume recreation (-V flag) to force import
   USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up -V
   ```

**Important Notes for Scenario A:**
- **Critical**: The dump script creates files with datetime format (e.g., `20250714-212239660.dump`), but MeiliSearch import expects `just_chat_rag.dump` - you must rename!
- The `-V` flag recreates anonymous volumes (MeiliSearch data) while preserving named volumes (MongoDB chat history)
- The import happens automatically when MeiliSearch starts with a fresh volume and finds the correctly named dump file

##### Scenario B: Handling Conflicts and Data Synchronization

**🆕 NEW: Automatic Conflict Resolution with Export (Meilisearch 1.16+)**

Starting with Meilisearch 1.16, the new **export feature** provides intelligent conflict resolution and additive data synchronization between instances. This solves the previous limitation where dumps required complete data replacement.

**✅ Recommended: Use Export for Conflict Resolution (Meilisearch 1.16+)**
```bash
# Direct instance-to-instance migration with automatic conflict resolution
uv run scripts/meilisearch_dump.py --export \
  --host localhost --port 7702 --api-key "source_key" \
  --target-url "http://production.example.com:7700" \
  --target-api-key "target_key"

# The export automatically:
# - Preserves existing documents in target
# - Adds new documents from source
# - Replaces duplicates (same document ID) with source version
# - Maintains all index settings and configurations

# For Docker container-to-host exports, use host gateway IP:
uv run scripts/meilisearch_dump.py --export \
  --host localhost --port 7702 --api-key "fancy_master_key" \
  --target-url "http://172.17.0.1:7700" \
  --target-api-key "fancy_master_key"
```

**Requirements for Export Feature:**
- Both source and target instances must be **Meilisearch 1.16.0 or higher**
- Update your instances: `docker compose pull && docker compose up -d`
- Verify versions: `curl "http://localhost:7700/version"`

**Legacy Approaches (for older Meilisearch versions < 1.16):**

When using traditional dumps, conflict resolution is **not** automatic. You must choose one of these strategies:

**Option 1: Replace Production Data (Most Common)**
```bash
# This completely replaces production search data with development data
# Follow Scenario A steps above - this overwrites all production indices
```

**Option 2: Replace Development Data with Production**
```bash
# 1. On Production: Create a dump
python3 scripts/meilisearch_dump.py

# 2. Transfer dump to Development
scp user@production-host:/path/to/just-chat/dumps/just_chat_rag.dump ./dumps/

# 3. On Development: Import production data
docker compose down
USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up -V
```

**Option 3: Manual Reindexing (When you need to merge changes)**
If you need to combine data from both environments, you must:
1. Choose one environment as the base (usually production)
2. Manually re-index the additional documents from the other environment
3. Use the API endpoints (`localhost:9000/docs`) to add the missing documents
4. Create a new dump with the combined data

**Best Practices for Data Synchronization:**

**With Export Feature (Meilisearch 1.16+):**
- Use export for seamless data synchronization between environments
- Export regularly from development to staging/production for incremental updates
- The additive nature means you can safely sync without losing existing data
- Use selective export with `--index-patterns` for specific index synchronization

**For Legacy Setups:**
- Establish a single source of truth for your search data
- Use version control for your source documents
- Document which environment contains the "master" version of your indices
- Consider creating dated backup dumps before major updates

#### Manual Import Process

If you need to manually import a dump:

1. **Place your dump file** at `dumps/just_chat_rag.dump`
2. **Reset and restart** the MeiliSearch container to force import:

```bash
# For Docker:
docker-compose down
USER_ID=$(id -u) GROUP_ID=$(id -g) docker-compose up -V

# For Podman:
podman compose down
podman compose up -V
```

#### Troubleshooting Tips

- **Dump not importing?** 
  - Ensure the file is named exactly `just_chat_rag.dump`
  - Remember: dump script creates `YYYYMMDD-HHMMSS.dump` but import needs `just_chat_rag.dump`
- **Old data still present?** Make sure you used the `-V` flag to recreate volumes
- **Large dumps taking time?** MeiliSearch import happens during startup - wait for the container to fully initialize
- **Import failed?** Check container logs: `docker compose logs -f meilisearch`
- **Wrong dump file?** Use `ls -t ./dumps/*.dump | head -n1` to find the most recent dump

**Note**: This process only resets MeiliSearch data (anonymous volume) while preserving MongoDB chat history (named volume).

## Some notes
0. Be sure to use ```docker pull``` (or podman pull if you use Podman) from time to time since the containers do not always automatically update when image was called with `:latest`
   It might even cause errors in running - so keep this in mind.
   
2. After the application is started, you can access the chat interface at `0.0.0.0:3000`

3. Key settings in `docker-compose.yml` (or podman-compose.yml if you use Podman):
   - UI Port: `0.0.0.0:3000` (under `huggingchat-ui` service)
   - Agent Port: `127.0.0.1:8091:8091` (under `just-chat-ui-agents` service)
   - MongoDB Port: `27017` (under `chat-mongo` service)
   - Container image versions:
     - just-chat-ui-agents: `ghcr.io/longevity-genie/just-agents/chat-ui-agents:main`
     - chat-ui: `ghcr.io/longevity-genie/chat-ui/chat-ui:sha-325df57`
     - mongo: `latest`

4. Troubleshooting container conflicts:
   - Check running containers: `docker ps` (or podman ps if you use Podman)
   - Stop conflicting containers: 
     ```bash
     cd /path/to/container/directory
     docker-compose down
     ```
   Note: Depending on your system and installation, you might need to use `docker compose` (without dash) 
   instead of `docker-compose` (with dash).

5. Best practices for container management:
   - Always stop containers when done using either:
     - `docker-compose down` (or `docker compose down`)
     - `Ctrl+C` followed by `docker-compose down`
   - To run in background mode, use:
     - `docker-compose up -d`
   - This prevents port conflicts in future sessions
 
 6. for editing the model used in chat_agent_profiles.yaml , the types are found [here](https://github.com/longevity-genie/just-agents/blob/main/core/just_agents/llm_options.py)
    It is the [just-agents library](https://github.com/longevity-genie/just-agents)


## Environment Variables & API Keys Configuration

The application uses environment variables to store API keys for various Language Model providers. A default configuration file is created under `env/.env.keys` during the initialization process. You can customize these keys to enable integrations with your preferred LLM providers.


### Included and Supported Providers

- **GROQ**: A default API key is provided on the first run if no keys are present. However, this key is shared with other users and is rate-limited (you can get rate limit errors from time to time). We recommend getting your own key from [Groq](https://console.groq.com/playground).
For additional LLM providers and their respective key configurations, please refer to the [LiteLLM Providers Documentation](https://docs.litellm.ai/docs/providers/).

### Setting up MeiliSearch and adding additional sources

We provide meilisearch semantic search with an ability to add your own documents. You can use corresponding REST API methods either via calls or with a default SWAGGER UI (just open just-chat-agents which uses localhost:8091 by default)
For your own documents we use MISTRAL_OCR to parse PDFs, so if you want to upload PDFs, please add MISTRAL_API_KEY to env/.env.keys
For autoannotation free GROQ key may no be enough because of rate limits. Please, either provide a paid GROQ key or change the model at annotation_agent.


### Logging and Observability
- By default, the application logs to the console and to timestamped files in the `/logs` directory.
- In case you run the application in background mode, you can still access and review the console logs by running:
`docker-compose logs -f just-chat-ui-agents`.
- **Langfuse**: Uncomment and fill in your credentials in `env/.env.keys` to enable additional observability for LLM calls.
- Note: Langfuse is not enabled by default.
- NB! `docker-compose down` will flush the container logs, but application logs will still be available in the `/logs` directory unless you delete them manually.

### How to Update the API Keys

1. **Editing the API Keys File:**  
   The API keys are stored in `/app/env/.env.keys`. You can update this file manually or run the initialization script located at `scripts/init_env.py` to automatically add commented hints for missing keys.

2. **Using Environment Variables:**  
   When running the application via Docker, these keys are automatically loaded into the container's environment. Feel free to use other means to populate the environment variables as long as the application can access them.

3. **Restart the Application:**  
   After updating the API keys, restart your Docker containers to apply the new settings, you may need to stop and start the containers to ensure the new keys are loaded:
   ```bash
   docker-compose down
   docker-compose up
   ```

Happy chatting!

## Advanced Development

While just-chat is designed for no-code use through YAML configuration files and simple Python tools, developers can extend it with advanced agentic flows and custom implementations:

### Development Environment Setup

For those who want to contribute to the codebase or develop advanced custom agents:

1. **DevContainer Support**: The project includes a pre-configured development container in `.devcontainer/devcontainer.json`
2. **IDE Integration**: Open the project in VS Code and it will automatically detect the devcontainer configuration
3. **Development Tools**: The devcontainer comes with Python, Docker tools, and all necessary extensions pre-installed

### Advanced Customization Options

- **Custom Agent Workflows**: Develop sophisticated multi-agent systems beyond simple tool calling
- **Advanced Tool Development**: Create complex tools with custom dependencies and integrations
- **API Extensions**: Extend the REST API for custom functionality
- **Database Integration**: Work directly with MongoDB for advanced data operations
- **Custom UI Components**: Modify the chat interface for specialized use cases

The devcontainer provides a complete development environment where you can modify core functionality while maintaining the containerized approach that makes just-chat easy to deploy and distribute.

## Acknowledgments

This project is supported by:

[![HEALES](images/heales.jpg)](https://heales.org/)

*HEALES - Healthy Life Extension Society*

and

[![IBIMA](images/IBIMA.jpg)](https://ibima.med.uni-rostock.de/)

[IBIMA - Institute for Biostatistics and Informatics in Medicine and Ageing Research](https://ibima.med.uni-rostock.de/)