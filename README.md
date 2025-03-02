# just-chat
Make your LLM agent and chat with it simple and fast!

![Easy chat with your Agent](images/screenshot.jpg)
*Setting up your agent and your chat in few clicks*

## Quick start

Just clone repository and run docker-compose!
```bash
git clone https://github.com/winternewt/just-chat.git
USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up
```
And the chat with your agent is ready to go! Open `http://localhost:3000` in your browser and start chatting with your agent!
Note: container will be started with the user and group of the host machine to avoid permission issues. If you want to change this, you can modify the `USER_ID` and `GROUP_ID` variables in the `docker-compose.yml` file.

If you prefer Podman or use RPM-based distro where it is the default option, you can use alternative Podman installation:
```bash
git clone https://github.com/winternewt/just-chat.git
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
- 🚀 Start chatting with one command ( docker compose up )
- 🤖 Customize your AI assistant using a YAML file (can be edited with a text editor)
- 🛠️ Add new capabilities with Python tools (can add additional functions and libraries)
- 🌐 Talk with agent with a chat web interface at 0.0.0.0:3000
- 🐳 Run everything in Docker containers
- 📦 Works without Python or Node.js on your system


We use [just-agents](https://github.com/longevity-genie/just-agents) library to initialize agents from YAML, so most of the modern models ( DeepSeek Reasoner, ChatGPT, LLAMA3.3, etc.) are supported. 
However, you might need to add your own keys to the environment variables. We provide a free Groq key by default but it is very rate-limited. We recommend getting your own keys,  [Groq](https://console.groq.com/playground) can be a good place to start as it is free and contains many open-source models.

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
 - [Docker-compose Standalone Installation Guide](https://docs.docker.com/compose/install/standalone/).
 
For Ubuntu users, you can review and use the provided convenience.sh script:
```bash
./scripts/install_docker_ubuntu.sh
```

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

For Ubuntu users (especially Ubuntu 24.04+):
```bash
# Install Podman
sudo apt-get update
sudo apt-get install -y podman

# Install Python3 and pip if not already installed
sudo apt-get install -y python3 python3-pip

# Install Podman Compose
pip3 install podman-compose
```

For legacy Ubuntu users (22.04 LTS):
You will have, sadly, to build podman from source. Due to outdated go-lang version in Ubuntu 22.04 LTS, you will have to add ppa repository and install a newer version of go-lang as a prerequisite and a bunch of libraries:

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
docker compose up
```


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
     docker compose down
     ```
   Note: Depending on your system and installation, you might need to use `docker-compose` (with dash) 
   instead of `docker compose` (without dash).

5. Best practices for container management:
   - Always stop containers when done using either:
     - `docker compose down` (or `docker-compose down`)
     - `Ctrl+C` followed by `docker compose down`
   - To run in background mode, use:
     - `docker compose up -d`
   - This prevents port conflicts in future sessions
 
 6. for editing the model used in chat_agent_profiles.yaml , the types are found [here](https://github.com/longevity-genie/just-agents/blob/main/core/just_agents/llm_options.py)
    It is the [just-agents library](https://github.com/longevity-genie/just-agents)


## Environment Variables & API Keys Configuration

The application uses environment variables to store API keys for various Language Model providers. A default configuration file is created under `env/.env.keys` during the initialization process. You can customize these keys to enable integrations with your preferred LLM providers.


### Included and Supported Providers

- **GROQ**: A default API key is provided on the first run if no keys are present. However, this key is shared with other users and is rate-limited (you can get rate limit errors from time to time). We recommend getting your own key from [Groq](https://console.groq.com/playground).
For additional LLM providers and their respective key configurations, please refer to the [LiteLLM Providers Documentation](https://docs.litellm.ai/docs/providers/).


### Logging and Observability
- By default, the application logs to the console and to timestamped files in the `/logs` directory.
- In case you run the application in background mode, you can still access and review the console logs by running:
`docker compose logs -f just-chat-ui-agents`.
- **Langfuse**: Uncomment and fill in your credentials in `env/.env.keys` to enable additional observability for LLM calls.
- Note: Langfuse is not enabled by default.
- NB! `docker compose down` will flush the container logs, but application logs will still be available in the `/logs` directory unless you delete them manually.

### How to Update the API Keys

1. **Editing the API Keys File:**  
   The API keys are stored in `/app/env/.env.keys`. You can update this file manually or run the initialization script located at `scripts/init_env.py` to automatically add commented hints for missing keys.

2. **Using Environment Variables:**  
   When running the application via Docker, these keys are automatically loaded into the container's environment. Feel free to use other means to populate the environment variables as long as the application can access them.

3. **Restart the Application:**  
   After updating the API keys, restart your Docker containers to apply the new settings, you may need to stop and start the containers to ensure the new keys are loaded:
   ```bash
   docker compose down
   docker compose up
   ```

Happy chatting!

## Acknowledgments

This project is supported by:

[![HEALES](images/heales.jpg)](https://heales.org/)

*HEALES - Healthy Life Extension Society*

and

[![IBIMA](images/IBIMA.jpg)](https://ibima.med.uni-rostock.de/)

[IBIMA - Institute for Biostatistics and Informatics in Medicine and Ageing Research](https://ibima.med.uni-rostock.de/)