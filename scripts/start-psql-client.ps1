function Show-Help {
    Write-Output "Usage: start-psql-client.ps1 [--help] [--network NETWORK_NAME]"
    Write-Output ""
    Write-Output "This script inspects the Docker network settings of a specified container or uses a provided network name to run a PostgreSQL client connected to that network."
    Write-Output ""
    Write-Output "Options:"
    Write-Output "  --help       Display this help message."
    Write-Output "  --network    Specify the network name directly."
    Write-Output ""
    Write-Output "Ensure Docker is installed and running on your system."
    Write-Output "Replace 'student-management-system-db-server' with the appropriate container name if different."
    Write-Output ""
}

# Check if '--help' is provided
if ($args -contains '--help') {
    Show-Help
    exit 0
}

# Check if '--network' is provided
$networkName = $null
if ($args -contains '--network') {
    $networkNameIndex = [Array]::IndexOf($args, '--network') + 1
    if ($networkNameIndex -lt $args.Length) {
        $networkName = $args[$networkNameIndex]
    } else {
        Write-Output "Error: '--network' parameter requires a network name."
        Show-Help
        exit 1
    }
}

# If network name is not provided, retrieve it from Docker container inspection
if (-not $networkName) {
    $dockerInspectOutput = docker inspect -f '{{json .NetworkSettings.Networks}}' student-management-system-db-server
    $networks = $dockerInspectOutput | ConvertFrom-Json
    $networkName = $networks.PSObject.Properties.Name
}

if (-not $networkName) {
    Write-Output "Failed to retrieve network name."
    exit 1
}

Write-Output ""
Write-Output "Network: $networkName"
Write-Output ""
Write-Output "Running Docker run for the PSQL client..."
Write-Output ""

docker run `
  --name student-management-system-db-client `
  -it `
  --rm `
  --network $networkName `
  postgres `
  psql `
  -h student-management-system-db-server `
  -U postgres
