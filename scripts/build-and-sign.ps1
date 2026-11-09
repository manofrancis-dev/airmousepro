# Builds, code-signs and optionally publishes the AirMouse Pro installer.
# Requires a code-signing certificate: pass -CertThumbprint (cert in CurrentUser\My)
# or -PfxPath (+ password in env AIRMOUSE_PFX_PASSWORD). Without one this script stops.
param(
    [string]$CertThumbprint,
    [string]$PfxPath,
    [string]$PfxPasswordEnv = 'AIRMOUSE_PFX_PASSWORD',
    [switch]$SkipBuild,
    [switch]$Publish
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$signtool = 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe'
$iscc = 'C:\Users\Manoj\tools\Inno Setup 6\ISCC.exe'
if (-not (Test-Path $signtool)) { throw "signtool not found at $signtool" }
if (-not (Test-Path $iscc)) { throw "Inno Setup ISCC not found at $iscc" }

$signArgs = @('sign', '/fd', 'SHA256', '/tr', 'http://timestamp.digicert.com', '/td', 'SHA256')
if ($PfxPath) {
    $pw = [Environment]::GetEnvironmentVariable($PfxPasswordEnv)
    if (-not $pw) { throw "Set env $PfxPasswordEnv to the PFX password" }
    $signArgs += @('/f', $PfxPath, '/p', $pw)
} elseif ($CertThumbprint) {
    $signArgs += @('/sha1', $CertThumbprint)
} else {
    throw 'No certificate supplied. Pass -CertThumbprint <sha1> or -PfxPath <file>. Smart App Control / SmartScreen will keep blocking unsigned builds.'
}

$exe = Join-Path $root 'dist\AirMousePro\AirMousePro.exe'
if (-not $SkipBuild) {
    python -m PyInstaller --clean --noconfirm AirMousePro.spec
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed' }
}
if (-not (Test-Path $exe)) { throw "built exe missing: $exe" }

& $signtool @signArgs $exe
if ($LASTEXITCODE -ne 0) { throw 'signing inner exe failed' }

& $iscc (Join-Path $root 'AirMousePro.iss')
if ($LASTEXITCODE -ne 0) { throw 'Inno Setup compile failed' }

$setup = Join-Path $root 'Output\AirMousePro_Setup.exe'
$final = Join-Path $root 'Output\AirMousePro_Setup_v1.0.0.exe'
Copy-Item $setup $final -Force
& $signtool @signArgs $final
if ($LASTEXITCODE -ne 0) { throw 'signing installer failed' }

& $signtool verify /pa $final
if ($LASTEXITCODE -ne 0) { throw 'signature verification failed' }

if ($Publish) {
    gh release upload v1.0.0 $final --clobber
    if ($LASTEXITCODE -ne 0) { throw 'release upload failed' }
}
Write-Host "Signed installer ready: $final"