param(
    [Parameter(Mandatory = $true)]
    [string]$Port,

    [Parameter(Mandatory = $true)]
    [ValidateSet("insecure", "hardened")]
    [string]$Profile,

    [int]$Baudrate = 115200
)

$ErrorActionPreference = "Stop"

$LabRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Output = Join-Path $LabRoot "evidence\lab02_${Profile}_console.log"

python (Join-Path $PSScriptRoot "capture_console_evidence.py") `
    --port $Port `
    --baudrate $Baudrate `
    --profile $Profile `
    --output $Output

python (Join-Path $PSScriptRoot "check_lab02_identity_logs.py") `
    $Output `
    --profile $Profile
