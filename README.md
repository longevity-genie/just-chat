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

You can customize your setup by:
1. Editing `chat_agent_profiles.yaml` to customize your agent
2. Adding tools to `/agent_tools` directory to empower your agent
3. Modifying `docker-compose.yml` for advanced settings (optional)

The only requirement is Docker! We provide detailed installation instructions for both Linux and Windows in the [Installation](##_Installation) section.
Also check the [notes](##_Some_notes) section for further information


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

- [`agent_profiles.yaml`](agent_profiles.yaml) - Configure your agents, their personalities and capabilities, example agents provided.
- [`/agent_tools/`](agent_tools/README.md) - Python tools to extend agent capabilities. Contains example tools and instructions for adding your own tools with custom dependencies.
- [`/data/`](data/README.md) - Application data storage if you want to let your agent work with additional data.
- [`docker-compose.yml`](docker-compose.yml) - Container orchestration and service configuration.
- [`/env/`](env/README.md) - Environment configuration files and settings.
- [`images/`](images/README.md) - Images for the README.
- [`/logs/`](logs/README.md) - Application logs.
- [`/scripts/`](scripts/README.md) - Utility scripts including Docker installation helpers.
- [`/volumes/`](volumes/README.md) - Docker volume mounts for persistent storage.

Note: Each folder contains additional README file with more information about the folder contents!

## Installation

Detailed installation instructions. If you already have Docker and Docker Compose installed, you can probably skip this section.

### Install Docker and Docker Compose
If you never installed Docker and Docker Compose, you can use the following instructions to install them. Otherwise you can skip this step.
To check if you have Docker and Docker Compose installed, you can use the following commands:

```bash
docker --version
docker-compose --version
```
The commands apply to both Linux (bash) and Windows (PowerShell). After this point instaltion split into Linux and Windows.

Note: in some cases `docker-compose` is called `docker compose` (without `-`). It depends on the version of docker compose you have installed.


### On Linux
#### Install Docker and Docker-compose Standalone

Refer to the official guides: 
 - [Docker Installation Guide](https://docs.docker.com/engine/install/ubuntu/).
 - [Docker-compose Standalone Installation Guide](https://docs.docker.com/compose/install/standalone/).
 
 For Ubuntu users, you can review and use the provided convenience.sh script, executing the code below. Running the script will install Docker and Docker Compose.Otherwise you can follow the steps presented after this command.

  ```bash
  ./scripts/install_docker_ubuntu.sh
  ```


#### Setup Docker's apt repository

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
#Updates the package lists (apt-get update).
#Installs required packages (ca-certificates and curl) for handling HTTPS-based repositories.

sudo install -m 0755 -d /etc/apt/keyrings
#Creates the /etc/apt/keyrings directory with 0755 permissions (readable and executable by everyone, writable only by the owner).
#This directory is used to store GPG keys securely.

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
#Downloads Docker's official GPG key (used to verify package authenticity) and saves it to /etc/apt/keyrings/docker.asc.
#Changes file permissions so that all users can read it (a+r).


# Add the repository to Apt sources:
#Adds Docker's official repository to the system's package sources.
#dpkg --print-architecture ensures the right package architecture (amd64, arm64, etc.).
#. /etc/os-release && echo "VERSION_CODENAME" dynamically fetches your Ubuntu version codename (e.g., jammy for Ubuntu 22.04).
#Writes the repository URL into /etc/apt/sources.list.d/docker.list.
#> /dev/null discards unnecessary output.

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update

```


### Install latest Docker and docker-compose standalone packages

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
#Installs:
#docker-ce (Docker Community Edition engine)
#docker-ce-cli (Docker CLI tools)
#containerd.io (Container runtime for managing containers)
#docker-buildx-plugin (Next-gen build system for Docker)
#docker-compose-plugin (Plugin for Docker Compose v2)

curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-$(uname -m) -o /usr/local/bin/docker-compose
#Downloads the latest Docker Compose binary (v2.32.4) from GitHub.
#$(uname -m) ensures that the correct architecture (e.g., x86_64, aarch64) is downloaded.
#Saves it to /usr/local/bin/docker-compose.

chmod +x /usr/local/bin/docker-compose
#Changes file permissions to make it executable.

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
#Creates a symbolic link from /usr/local/bin/docker-compose to /usr/bin/docker-compose.
#This allows you to run Docker Compose commands without specifying the full path.
```


## On Windows

### Prerequisites
Before installing Docker on Windows, ensure your system meets the following requirements:

Windows 10 (Pro, Enterprise, Education) Version 1909 or later
Windows 11 (any edition)
WSL 2 (Windows Subsystem for Linux) enabled (recommended) link [here](https://learn.microsoft.com/en-us/windows/wsl/install)
Hyper-V enabled (if using Windows 10 Pro/Enterprise)
At least 4GB of RAM (recommended)

Though WSL is not strictly required for installation, it is highly recommended for running Linux-based containers efficiently.
If you don't want to use WSL during Docker Desktop installation, uncheck the option "Use WSL 2 instead of Hyper-V".
Docker will automatically switch to Windows Containers instead of Linux Containers.

Limitations Without WSL:
-You cannot run Linux-based containers (unless using a full virtual machine).
-Performance is slower because it uses Hyper-V (Windows 10 Pro/Enterprise) or Windows-native virtualization.
-Some Docker features (e.g., Kubernetes support) won't work.


### Install Docker Desktop
1. Download Docker Desktop [here](https://docs.docker.com/desktop/setup/install/windows-install/)

2. Install Docker Desktop:
-Locate the Docker Desktop Installer.exe file in your Downloads folder.
-Double-click to start the installation.
-Check the required options:
--Enable WSL 2 (recommended)
--Enable Windows Containers (optional, needed for Windows-based containers).
-Click Install and wait for it to complete.

3. Restart Your PC
After installation, restart your computer to apply the changes.

4. Run Docker Desktop
Open Start Menu and search for Docker Desktop.
Click to launch Docker.
Wait for it to start (it may take a few seconds).
You should see the Docker whale 🐳 icon in the taskbar.

5. Install Docker Compose on Windows
Docker Compose v2 is already built into Docker Desktop. 
If you need standalone Docker Compose v1, install it manually:

Download the latest Docker Compose binary:
In powershell
```
powershell
curl -SL "https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-windows-x86_64.exe" -o "C:\Program Files\Docker\Docker\resources\bin\docker-compose.exe"
```

Add Docker Compose to System Path (if not already).
Restart your system.

Docker works best with Windows Subsystem for Linux (WSL 2). 
Open Docker Desktop, go to Settings → General, and check:
Use WSL 2 for Linux containers.

6. Ensure Docker Starts on Boot (Optional)
To make Docker automatically start:
Open Docker Desktop.
Go to Settings → General.
Enable "Start Docker Desktop when you log in".


## For both operating systems

### Verify installation

```bash
sudo docker run hello-world
docker-compose --version
```

## Clone Just-Chat repository
```bash
git clone https://github.com/winternewt/just-chat.git
```

## Start the application
```bash
docker compose up
```


## Some notes
0. Be sure to use ```docker pull``` from time to time since the containers do not allways automatically update when image was called with `:latest`
   It might even cause errors in running -so keep this in mind
   
2. After the application is started, you can access the chat interface at `0.0.0.0:3000`

3. Key settings in `docker-compose.yml`:
   - UI Port: `0.0.0.0:3000` (under `huggingchat-ui` service)
   - Agent Port: `127.0.0.1:8089:8089` (under `just-chat-ui-agents` service)
   - MongoDB Port: `27017` (under `chat-mongo` service)
   - Container image versions:
     - just-chat-ui-agents: `ghcr.io/longevity-genie/just-agents/chat-ui-agents:main`
     - chat-ui: `ghcr.io/longevity-genie/chat-ui/chat-ui:sha-325df57`
     - mongo: `latest`

4. Troubleshooting container conflicts:
   - Check running containers: `docker ps`
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
 
 6. for editing the model used in agent_profiles.yaml , the types are found [here](https://github.com/longevity-genie/just-agents/blob/main/core/just_agents/llm_options.py)
    It is the [just-agents library](https://github.com/longevity-genie/just-agents)



## Environment Variables & API Keys Configuration

The application uses environment variables to store API keys for various Language Model providers. A default configuration file is created under `env/.env.keys` during the initialization process. You can customize these keys to enable integrations with your preferred LLM providers.


### Included and Supported Providers

- **GROQ**: A default API key is provided on the first run if no keys are present.
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