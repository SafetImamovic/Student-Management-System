#!/bin/bash

show_help() {
  echo "Usage: start-psql-client.sh [--help] [--network NETWORK_NAME]"
  echo ""
  echo "This script inspects the Docker network settings of a specified container and runs a PostgreSQL client connected to that network."
  echo ""
  echo "Options:"
  echo "  --help       Display this help message."
  echo "  --network    Specify the network name directly."
  echo ""
  echo "Ensure Docker is installed and running on your system."
  echo "Replace 'student-management-system-db-server' with the appropriate container name if different."
  echo ""
}

# Default network name
networkName="student-management-system_student-management-system-network"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --help)
      show_help
      exit 0
      ;;
    --network)
      if [[ -n "$2" ]]; then
        networkName="$2"
        shift 2
      else
        echo "Error: --network requires a value."
        show_help
        exit 1
      fi
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Check if the network name is set
if [[ -z "$networkName" ]]; then
  echo -e "\nError: Failed to retrieve network name. Use --network to specify the network.\n"
  echo "To list all Docker networks, run: docker network ls"
  exit 1
fi

echo -e "\nNetwork: $networkName\n"
echo "Running Docker run for the PSQL client...\n"

# Run the PostgreSQL client within the specified Docker network
docker run \
  --name student-management-system-db-client \
  -it \
  --rm \
  --network "$networkName" \
  postgres \
  psql \
  -h student-management-system-db-server \
  -U postgres
