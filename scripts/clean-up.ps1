# PowerShell script to perform cleanup of Docker containers and networks

function Show-Help {
    Write-Output "Usage: clean-up.ps1 [--help] [--rmi] [--keep-client]"
    Write-Output ""
    Write-Output "This script stops and removes Docker containers and networks created by the start.ps1 and start-psql-client scripts."
    Write-Output "Optional parameters:"
    Write-Output "  --rmi           Remove images built in the docker-compose.yml"
    Write-Output "  --keep-client   [default = false] Keeps the client container running"
    Write-Output ""
}

# Default parameters
$removeImages = $false
$keepClient = $false

# Parse arguments manually
foreach ($arg in $args) {
    switch -Wildcard ($arg) {
        '--help' {
            Show-Help
            exit
        }
        '--rmi' {
            $removeImages = $true
        }
        '--keep-client' {
            $keepClient = $true
        }
        default {
            Write-Output "Unknown option: $arg"
            Show-Help
            exit 1
        }
    }
}

# Debug: Print parameters
Write-Output "Parameters:"
Write-Output "rmi: $removeImages"
Write-Output "keepClient: $keepClient"
Write-Output ""

# Navigate to the script directory
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
Set-Location -Path $scriptDir

Write-Output "Stopping and removing containers and networks with 'docker-compose down'..."
docker-compose down

# Remove client container if the --keep-client option is not set
if (-not $keepClient) {
    Write-Output "Removing client container..."
    docker container rm -f student-management-system-db-client
    Write-Output "Removing the network..."
    docker network rm student-management-system_student-management-system-network
}

if ($removeImages) {
    Write-Output "Removing student-management-system-api Image..."
    # List the images used by the current docker-compose setup

    $images = "student-management-system-api student-management-system-frontend"

    if ($images) {
        Write-Output ""
        Write-Output "Pre Removal:"
        Write-Output ""
        docker images
        docker rmi $images --force
        Write-Output ""
        Write-Output "Post Removal"
        Write-Output ""
        docker images
        Write-Output ""
    } else {
        Write-Output "No images to remove."
    }
}

Write-Output "Cleanup complete."
Write-Output ""
