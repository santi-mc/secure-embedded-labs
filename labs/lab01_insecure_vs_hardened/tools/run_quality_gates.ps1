$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LabRoot = Resolve-Path (Join-Path $ScriptDir "..")
$FirmwareRoot = Join-Path $LabRoot "firmware"

Write-Host "[LAB01] Running static gates..."
python (Join-Path $ScriptDir "run_static_gates.py")

Write-Host "[LAB01] Running ESP-IDF build..."
Push-Location $FirmwareRoot
try {
    idf.py set-target esp32s3
    idf.py build
}
finally {
    Pop-Location
}

Write-Host "[LAB01] Quality gates completed."
