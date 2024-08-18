<#
.SYNOPSIS
    This script runs a Docker Compose file to start PostgreSQL and FastAPI containers.

.DESCRIPTION
    This PowerShell script performs the following steps:
    1. Checks if Docker is installed.
    2. Checks if docker-compose is installed.
    3. Navigates to the directory containing the docker-compose.yml file.
    4. Runs the docker-compose.yml file to start the PostgreSQL and FastAPI containers.
    5. Checks if the containers started successfully.
    6. Lists all running containers.

.PARAMETER None
    This script does not take any parameters.

.EXAMPLE
    PS> .\start.ps1
    This example runs the script from the current directory.

.NOTES
    Ensure that Docker and docker-compose are installed before running this script.
#>

function Show-Help {
    Write-Output "Usage: start.ps1 [--help]"
    Write-Output ""
    Write-Output "This script runs a Docker Compose file to start PostgreSQL and FastAPI containers."
    Write-Output ""
    Write-Output "Options:"
    Write-Output "  --help       Display this help message."
    Write-Output ""
    Write-Output "Ensure that Docker and docker-compose are installed before running this script."
    Write-Output ""
    Write-Output "Run: 'docker compose down' To stop and remove all instances which are started when 'start.ps1' is called"
    Write-Output ""
}

if ($args -contains '--help') {
    Show-Help
    exit 0
}

function Test-Command {
    param (
        [string]$command
    )
    return Get-Command $command -ErrorAction SilentlyContinue
}

if (-not (Test-Command -command "docker")) {
    Write-Error "Docker is not installed. Please install Docker and try again."
    exit 1
}

if (-not (Test-Command -command "docker-compose")) {
    Write-Error "docker-compose is not installed. Please install docker-compose and try again."
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
cd $scriptDir

Write-Output "Running docker-compose up..."
docker-compose up --build -d

$containers = @("student-management-system-db-server", "student-management-system-api")

foreach ($container in $containers) {
    $containerStatus = docker inspect --format '{{.State.Status}}' $container

    if ($containerStatus -eq "running") {
        Write-Output "Container '$container' is running."
        Write-Output ""

        if ($container -eq "student-management-system-db-server") {
            Write-Output "Container '$container' listening on port 5432."
            Write-Output "Port 5432 is port forwarded to local port 5432."
            Write-Output ""
        }
        if ($container -eq "student-management-system-api") {
            Write-Output "Container '$container' listening on port 8000 and host 0.0.0.0."
            Write-Output "Port 8000 is port forwarded to local port 8000."
            Write-Output ""
        }
    } else {
        Write-Error "Failed to start the container '$container'."
    }
}

Write-Output "Currently running containers:"
docker ps