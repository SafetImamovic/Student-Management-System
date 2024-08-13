#!/bin/bash

function show_help {
    echo "Usage: clean-up.sh [--help] [--rmi] [--keep-client]"
    echo ""
    echo "This script stops and removes Docker containers and networks created by the start.sh and start-psql-client scripts."
    echo "Optional parameters:"
    echo "  --rmi           Remove images built in the docker-compose.yml"
    echo "  --keep-client   [default = false] Keeps the client container running"
    echo ""
}

# Default parameters
remove_images=false
keep_client=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            show_help
            exit 0
            ;;
        --rmi)
            remove_images=true
            shift
            ;;
        --keep-client)
            keep_client=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Print parameters
echo "Parameters:"
echo "rmi: $remove_images"
echo "keepClient: $keep_client"
echo ""

# Navigate to the script directory
script_dir=$(dirname "$(realpath "$0")")
cd "$script_dir" || exit

echo "Stopping and removing containers and networks with 'docker-compose down'..."
docker-compose down

# Remove client container if the --keep-client option is not set
if [[ "$keep_client" == false ]]; then
    echo "Removing client container..."
    docker container rm -f student-management-system-db-client
    echo "Removing the network..."
    docker network rm student-management-system_student-management-system-network
fi

if [[ "$remove_images" == true ]]; then
    echo "Removing student-management-system-api Image..."
    # List the images used by the current docker-compose setup

    images="student-management-system-api"

    if [[ -n "$images" ]]; then
        echo ""
        echo "Pre Removal:"
        echo ""
        docker images
        docker rmi $images --force
        echo ""
        echo "Post Removal"
        echo ""
        docker images
        echo ""
    else
        echo "No images to remove."
    fi
fi

echo "Cleanup complete."
echo ""
