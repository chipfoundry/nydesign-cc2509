param(
  [string]$Uf2 = ".\tt-demo-rp2040-v2.0.4.uf2",
  [string]$IndexJson = ".\ttsky25b_for_sdk204.json",
  [string]$ShuttleId = "ttsky25b",
  [string]$Port = "auto",
  [switch]$SkipFlash
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-Mpremote {
  $cmd = Get-Command mpremote -ErrorAction SilentlyContinue
  if ($cmd) {
    return @{ exe = "mpremote"; baseArgs = @() }
  }

  $py = Get-Command py -ErrorAction SilentlyContinue
  if ($py) {
    return @{ exe = "py"; baseArgs = @("-m", "mpremote") }
  }

  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) {
    return @{ exe = "python"; baseArgs = @("-m", "mpremote") }
  }

  throw "mpremote not found. Install with: py -m pip install mpremote"
}

function Invoke-Mpremote {
  param(
    [hashtable]$Mpremote,
    [string[]]$Args,
    [switch]$IgnoreErrors
  )

  $allArgs = @()
  $allArgs += $Mpremote.baseArgs
  $allArgs += $Args

  if ($IgnoreErrors) {
    try {
      & $Mpremote.exe @allArgs | Out-Host
    } catch {
      Write-Host "Ignoring mpremote error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
  } else {
    & $Mpremote.exe @allArgs | Out-Host
  }
}

if (-not (Test-Path -LiteralPath $Uf2)) {
  throw "UF2 file not found: $Uf2"
}
if (-not (Test-Path -LiteralPath $IndexJson)) {
  throw "Index JSON not found: $IndexJson"
}

$uf2Path = (Resolve-Path -LiteralPath $Uf2).Path
$indexPath = (Resolve-Path -LiteralPath $IndexJson).Path
$targetName = "$ShuttleId.json"

if (-not $SkipFlash) {
  Write-Host "Step 1/2: Flash UF2 to board" -ForegroundColor Cyan
  Write-Host "Put the RP2040 board in BOOTSEL mode so it mounts as RPI-RP2." -ForegroundColor Cyan

  $volume = Get-Volume -FileSystemLabel "RPI-RP2" -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $volume) {
    throw "RPI-RP2 drive not found. Hold BOOTSEL, connect USB, and try again."
  }
  if (-not $volume.DriveLetter) {
    throw "RPI-RP2 volume found but no drive letter assigned."
  }

  $driveRoot = "$($volume.DriveLetter):\"
  Write-Host "Copying UF2 to $driveRoot ..." -ForegroundColor Cyan
  Copy-Item -LiteralPath $uf2Path -Destination $driveRoot -Force

  Write-Host "UF2 copied. Waiting for board to reboot..." -ForegroundColor Cyan
  Start-Sleep -Seconds 6
} else {
  Write-Host "Skipping UF2 flash (--SkipFlash)." -ForegroundColor Yellow
}

Write-Host "Step 2/2: Copy shuttle index via mpremote" -ForegroundColor Cyan
$mp = Resolve-Mpremote

Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "fs", "mkdir", ":/shuttles") -IgnoreErrors
Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "fs", "cp", $indexPath, ":/shuttles/$targetName")
Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "fs", "ls", ":/shuttles")
Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "exec", "import os; print('exists:', '$targetName' in os.listdir('/shuttles'))")
Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "reset")

Write-Host "Running post-reset verification sequence..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "exec", "import os; print('post_reset_exists:', '$targetName' in os.listdir('/shuttles'))")
Invoke-Mpremote -Mpremote $mp -Args @("connect", $Port, "exec", "from ttboard.demoboard import DemoBoard; tt=DemoBoard.get(); print('detected_shuttle:', tt.shuttle.run)")

Write-Host "Provisioning complete." -ForegroundColor Green
Write-Host "UF2: $uf2Path"
Write-Host "Index: $indexPath -> :/shuttles/$targetName"
