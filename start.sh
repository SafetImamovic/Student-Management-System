#!/bin/bash

function show_help {
    echo "Usage: start.sh [--help]"
    echo ""
    echo "This script runs a Docker Compose file to start PostgreSQL and FastAPI containers."
    echo ""
    echo "Options:"
    echo "  --help       Display this help message."
    echo ""
    echo "Ensure that Docker and docker-compose are installed before running this script."
    echo ""
    echo "Run: 'docker compose down' to stop and remove all instances started when 'start.sh' is called."
    echo ""
}

if [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

function test_command {
    command -v "$1" >/dev/null 2>&1
}

if ! test_command "docker"; then
    echo "Docker is not installed. Please install Docker and try again." >&2
    exit 1
fi

if ! test_command "docker-compose"; then
    echo "docker-compose is not installed. Please install docker-compose and try again." >&2
    exit 1
fi

script_dir=$(dirname "$(realpath "$0")")
cd "$script_dir" || exit

echo "Running docker-compose up..."
docker-compose up -d

containers=("student-management-system-db-server" "student-management-system-api")

for container in "${containers[@]}"; do
    container_status=$(docker inspect --format '{{.State.Status}}' "$container")

    if [[ "$container_status" == "running" ]]; then
        echo "Container '$container' is running."
        echo ""

        if [[ "$container" == "student-management-system-db-server" ]]; then
            echo "Container '$container' listening on port 5432."
            echo "Port 5432 is port forwarded to local port 5432."
            echo ""
        fi
        if [[ "$container" == "student-management-system-api" ]]; then
            echo "Container '$container' listening on port 8000 and host 0.0.0.0."
            echo "Port 8000 is port forwarded to local port 8000."
            echo ""
        fi
    else
        echo "Failed to start the container '$container'." >&2
    fi
done

echo "Currently running containers:"
docker ps
