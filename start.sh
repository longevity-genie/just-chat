#!/bin/bash
# Script to start Docker Compose with current user permissions

# Exit on error
set -e

# Warning about experimental status
echo "⚠️  WARNING: This script is experimental ⚠️"
echo "If you encounter any issues, you can run the following command directly:"
echo "UID=$(id -u) GID=$(id -g) docker compose up"
echo

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Start the just-chat application using Docker or Podman"
    echo
    echo "Options:"
    echo "  -d, --detach    Run containers in the background"
    echo "  -h, --help      Show this help message"
    echo
    echo "Examples:"
    echo "  $0              # Run in foreground mode"
    echo "  $0 --detach     # Run in background mode"
    echo
}

# Default to attached mode
DETACH_MODE=""

# Process command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--detach)
            DETACH_MODE="-d"
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

echo "Starting just-chat application..."
echo "Will attempt to run using Docker or fall back to Podman if available"
echo "---------------------------------------------------------------------"

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "Using Docker"
    if [ -n "$DETACH_MODE" ]; then
        echo "Running in detached mode"
    fi
    # Use USER_ID and GROUP_ID directly
    USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up $DETACH_MODE
# If Docker is not available, try Podman
elif command -v podman &> /dev/null; then
    echo "Docker not found, falling back to Podman"
    if [ -n "$DETACH_MODE" ]; then
        echo "Running in detached mode"
    fi
    # Use USER_ID and GROUP_ID directly
    USER_ID=$(id -u) GROUP_ID=$(id -g) podman-compose up $DETACH_MODE
else
    echo "Error: Neither Docker nor Podman is installed or in PATH"
    exit 1
fi