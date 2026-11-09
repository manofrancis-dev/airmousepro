# Stages the built app into an MSIX layout and packs it for Microsoft Store submission.
# -IdentityName and -Publisher must come from your Partner Center app identity
# (Package/Identity/Name and Package/Identity/Publisher). Store re-signs on certification;
# for local sideload testing you must self-sign the .msix separately.
param(
    [Parameter(Mandatory)][string]$IdentityName,
    [Parameter(Mandatory)][string]$Publisher,
    [string]$OutFile
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$makeappx = 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\makeappx.exe'
if (-not (Test-Path $makeappx)) { throw "makeappx not found at $makeappx" }
if (-not $OutFile) { $OutFile = Join-Path $root 'store\out\AirMousePro.msix' }

$stage = Join-Path $root 'store\layout'
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stage | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $OutFile) | Out-Null

Copy-Item (Join-Path $root 'dist\AirMousePro') (Join-Path $stage 'AirMousePro') -Recurse

$manifest = Get-Content (Join-Path $root 'store\AppxManifest.xml') -Raw
$manifest = $manifest.Replace('__IDENTITY_NAME__', $IdentityName).Replace('__PUBLISHER__', $Publisher)
Set-Content -Path (Join-Path $stage 'AppxManifest.xml') -Value $manifest -Encoding UTF8

$py = @'
import sys, os
from PIL import Image
logo, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
im = Image.open(logo).convert('RGBA')
for name, size in {'StoreLogo.png': (50,50), 'Square44x44Logo.png': (44,44), 'Square150x150Logo.png': (150,150)}.items():
    im.resize(size, Image.LANCZOS).save(os.path.join(out, name))
wide = Image.new('RGBA', (310,150), (0,0,0,0))
tile = im.resize((150,150), Image.LANCZOS)
wide.paste(tile, (80,0), tile)
wide.save(os.path.join(out, 'Wide310x150Logo.png'))
'@
python -c $py (Join-Path $root 'AirMousePro-Website-SEO\assets\AirMousePro_logo_512.png') (Join-Path $stage 'Assets')
if ($LASTEXITCODE -ne 0) { throw 'asset generation failed' }

& $makeappx pack /d $stage /p $OutFile /o
if ($LASTEXITCODE -ne 0) { throw 'makeappx pack failed' }
Write-Host "MSIX ready: $OutFile"