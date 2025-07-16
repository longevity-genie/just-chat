#!/bin/bash

# Exit on error, undefined vars, pipe failures
set -euo pipefail

script_dir=$(dirname "$(readlink -f "$0")")

# Logging functions
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { log "❌ ERROR: $*" >&2; exit 1; }
info() { log "ℹ️  INFO: $*"; }
success() { log "✅ SUCCESS: $*"; }

# Check Ubuntu version and set Podman installation method
check_ubuntu_version() {
    if ! grep -qi ubuntu /etc/os-release; then
        error "This script is designed for Ubuntu only"
    fi
    
    local ubuntu_version=$(lsb_release -rs 2>/dev/null || echo "unknown")
    case "$ubuntu_version" in
        "22.04")
            UBUNTU_VERSION="22.04"
            PODMAN_FROM_APT=false
            success "Ubuntu 22.04 detected - will install Podman manually (apt version too old)"
            ;;
        "24.04"|"24.10"|"25.04"|"25.10")
            UBUNTU_VERSION="$ubuntu_version"
            PODMAN_FROM_APT=true
            success "Ubuntu $ubuntu_version detected - will install Podman from apt"
            ;;
        *)
            error "Unsupported Ubuntu version: $ubuntu_version. Supported: 22.04, 24.04+"
            ;;
    esac
}

# Check if Docker is already installed and working
check_existing_installation() {
    if command -v docker &> /dev/null; then
        info "Docker already installed, checking if it's working..."
        if su - "$SUDO_USER" -c "docker version &> /dev/null" 2>/dev/null; then
            success "Docker is already installed and working for user $SUDO_USER"
            exit 0
        else
            info "Docker installed but not working properly, continuing with setup..."
        fi
    fi
}

# Check if user is already in docker group
check_docker_group() {
    if groups "$SUDO_USER" | grep -q '\bdocker\b'; then
        info "User $SUDO_USER already in docker group"
        return 0
    else
        return 1
    fi
}

# Install Podman v4+ from source on Ubuntu 22.04
install_podman_from_source() {
    # Check if Podman v4+ is already installed
    if command -v podman &> /dev/null; then
        local existing_version=$(podman --version 2>/dev/null || echo "unknown")
        if echo "$existing_version" | grep -Eq "podman version [4-9]\."; then
            success "Podman v4+ already installed: $existing_version"
            return 0
        fi
    fi
    
    info "🔨 Installing Podman v4.9.3 from source for Ubuntu 22.04"
    info "⏱️  This process may take 10-15 minutes depending on your system"
    
    # Add golang PPA for newer Go version
    info "📦 Adding golang PPA for newer Go version"
    add-apt-repository -y ppa:longsleep/golang-backports || error "Failed to add golang PPA"
    apt-get update || error "Failed to update after adding golang PPA"
    
    # Enable unprivileged user namespaces
    info "⚙️  Enabling unprivileged user namespaces"
    sysctl kernel.unprivileged_userns_clone=1 || error "Failed to enable unprivileged user namespaces"
    
    # Install build dependencies
    info "📦 Installing Podman build dependencies"
    apt-get install -y git build-essential btrfs-progs gcc git golang-go go-md2man iptables \
        libassuan-dev libbtrfs-dev libc6-dev libdevmapper-dev libglib2.0-dev libgpgme-dev \
        libgpg-error-dev libprotobuf-dev libprotobuf-c-dev libseccomp-dev libselinux1-dev \
        libsystemd-dev make containernetworking-plugins pkg-config uidmap || error "Failed to install build dependencies"
    
    # Install runc if not already present
    if ! command -v runc &> /dev/null; then
        info "📦 Installing runc"
        apt-get install -y runc || error "Failed to install runc"
    fi
    
    # Save current directory and create temporary directory for building
    local original_dir=$(pwd)
    local build_dir="/tmp/podman-build-$$"
    mkdir -p "$build_dir" || error "Failed to create build directory"
    cd "$build_dir" || error "Failed to change to build directory"
    
    # Clone Podman repository
    info "📥 Cloning Podman repository"
    git clone https://github.com/containers/podman.git || error "Failed to clone Podman repository"
    cd podman || error "Failed to enter Podman directory"
    
    # Checkout specific version
    info "🏷️  Checking out Podman v4.9.3"
    git checkout v4.9.3 || error "Failed to checkout Podman v4.9.3"
    
    # Build Podman
    info "🔨 Building Podman (this may take several minutes)"
    make || error "Failed to build Podman"
    
    # Install Podman
    info "📦 Installing Podman"
    make install || error "Failed to install Podman"
    
    # Cleanup build directory and return to original location
    info "🗑️  Cleaning up build directory"
    cd "$original_dir" || cd / || true
    rm -rf "$build_dir" || true
    
    # Verify installation
    local podman_version=$(podman --version 2>/dev/null || echo "unknown")
    if [[ "$podman_version" == *"4.9.3"* ]]; then
        success "Podman v4.9.3 installed successfully"
    else
        error "Podman installation verification failed. Version: $podman_version"
    fi
}

# Get latest docker-compose version
get_latest_compose_version() {
    info "🔍 Fetching latest docker-compose version..."
    local version
    version=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*?(?=")' || echo "v2.38.1")
    if [[ -z "$version" ]]; then
        info "⚠️  Could not fetch latest version, using fallback v2.38.1"
        version="v2.38.1"
    else
        info "📦 Latest docker-compose version: $version"
    fi
    echo "$version"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "This script must be run as root. Please use: sudo $0"
fi

# Check if we have the original user
if [ -z "$SUDO_USER" ]; then
    error "SUDO_USER not set. Please run with 'sudo' to preserve user context."
fi

# Check Ubuntu version
check_ubuntu_version

# Check if already installed
check_existing_installation

info "🔧 Starting Docker installation for Ubuntu $UBUNTU_VERSION"

TO_REMOVE="docker-ce docker-ce-cli docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras"

info "📦 Updating package list"
apt-get update || error "Failed to update package list"

info "⬇️  Installing prerequisites"
apt-get install -y ca-certificates curl gnupg lsb-release python3 python3-pip pipx software-properties-common || error "Failed to install prerequisites"

info "🗑️  Removing old Docker packages"
apt-get purge -y $TO_REMOVE || true  # Don't fail if packages don't exist

info "🔑 Setting up Docker GPG key"
install -m 0755 -d /etc/apt/keyrings || error "Failed to create keyrings directory"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc || error "Failed to download Docker GPG key"
chmod a+r /etc/apt/keyrings/docker.asc || error "Failed to set GPG key permissions"

info "📋 Adding Docker repository"
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null || error "Failed to add Docker repository"

info "🔄 Updating package list with Docker repository"
apt-get update || error "Failed to update package list after adding Docker repository"

info "📦 Installing Docker packages"
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras || error "Failed to install Docker packages"

# Install Podman based on Ubuntu version
if [[ "$PODMAN_FROM_APT" == "true" ]]; then
    info "🐙 Installing Podman from apt (Ubuntu $UBUNTU_VERSION)"
    apt-get install -y podman netavark passt || error "Failed to install Podman from apt"
else
    info "🔨 Ubuntu $UBUNTU_VERSION detected - installing Podman v4.9.3 from source"
    install_podman_from_source
fi

# Add user to docker group (with idempotency check)
if ! check_docker_group; then
    info "👤 Adding user $SUDO_USER to docker group"
    usermod -aG docker "$SUDO_USER" || error "Failed to add user to docker group"
else
    info "👤 User $SUDO_USER already in docker group, skipping"
fi

# Install podman-compose if Podman is available
if command -v podman &> /dev/null; then
    info "🐙 Installing podman-compose via pipx"
    # Install pipx packages as the original user (not root)
    su - "$SUDO_USER" -c "pipx install podman-compose" || error "Failed to install podman-compose"
else
    info "⏭️  Skipping podman-compose installation (Podman not available)"
fi

info "🐳 Installing standalone docker-compose"
# Get user's home directory properly
USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
DOCKER_CONFIG=${DOCKER_CONFIG:-$USER_HOME/.docker}

# Create directory as the user, not root
su - "$SUDO_USER" -c "mkdir -p $DOCKER_CONFIG/cli-plugins" || error "Failed to create docker config directory"

# Get latest version dynamically
COMPOSE_VERSION=$(get_latest_compose_version)

info "⬇️  Downloading docker-compose $COMPOSE_VERSION"
curl -SL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-$(uname -m)" -o $DOCKER_CONFIG/cli-plugins/docker-compose || error "Failed to download docker-compose"
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose || error "Failed to make docker-compose executable"
ln -sf $DOCKER_CONFIG/cli-plugins/docker-compose /usr/local/bin/docker-compose || error "Failed to create docker-compose symlink"

info "🧪 Testing installations as user $SUDO_USER"
# Test docker installation as the user (not root) to validate group membership
echo "Testing Docker installation as user $SUDO_USER..."
su - "$SUDO_USER" -c "docker run hello-world" || error "Docker test failed - hello-world container could not run"
su - "$SUDO_USER" -c "docker-compose version" || error "docker-compose test failed"

# Test Podman if available
if command -v podman &> /dev/null; then
    echo "Testing Podman installation as user $SUDO_USER..."
    su - "$SUDO_USER" -c "podman run hello-world" || error "Podman test failed - hello-world container could not run"
    if command -v podman-compose &> /dev/null; then
        su - "$SUDO_USER" -c "podman-compose version" || error "podman-compose test failed"
    fi
fi

success "✅ Container runtime installation completed successfully!"
if command -v podman &> /dev/null; then
    info "🐳 Docker and Podman are both ready to use"
else
    info "🐳 Docker is ready to use"
fi
info "📝 Note: User $SUDO_USER may need to log out and back in for group changes to take effect"
