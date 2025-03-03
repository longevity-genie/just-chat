#!/bin/bash
# Script to stop Docker Compose with similar behavior as start.sh

# Exit on error
set -e

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Stop the just-chat application running in Docker or Podman"
    echo
    echo "Options:"
    echo "  -v, --volumes    Remove volumes when stopping containers"
    echo "  -h, --help       Show this help message"
    echo
    echo "Examples:"
    echo "  $0               # Stop containers"
    echo "  $0 --volumes     # Stop containers and remove volumes"
    echo
}

# Default - don't remove volumes
VOLUMES_FLAG=""

# Process command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--volumes)
            VOLUMES_FLAG="--volumes"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo "Stopping just-chat application..."
echo "Will attempt to use Docker or fall back to Podman if available"
echo "---------------------------------------------------------------------"

# Warning about experimental script
echo "⚠️  WARNING: This script is experimental ⚠️"
echo "You can simply use 'docker compose down' directly instead of this script"
echo "if you encounter any issues."
echo "---------------------------------------------------------------------"

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "Using Docker"
    USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose down $VOLUMES_FLAG
# If Docker is not available, try Podman
elif command -v podman &> /dev/null; then
    echo "Docker not found, falling back to Podman"
    USER_ID=$(id -u) GROUP_ID=$(id -g) podman-compose down $VOLUMES_FLAG
else
    echo "Error: Neither Docker nor Podman is installed or in PATH"
    exit 1
fi
