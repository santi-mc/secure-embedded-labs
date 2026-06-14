param(
    [Parameter(Mandatory=$true)]
    [string]$Port,

    [Parameter(Mandatory=$true)]
    [ValidateSet("insecure", "hardened")]
    [string]$Profile,

    [string]$Output = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LabRoot = Resolve-Path (Join-Path $ScriptDir "..")

if ($Output -eq "") {
    $Output = Join-Path $LabRoot "evidence\lab01_${Profile}_console.log"
}

python (Join-Path $ScriptDir "capture_console_evidence.py") `
    --port $Port `
    --profile $Profile `
    --output $Output
