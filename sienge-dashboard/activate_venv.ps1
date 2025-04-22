function Activate-Venv {
    param (
        [string]$Path = "."
    )
    
    $venvPath = Join-Path $Path "venv"
    if (Test-Path $venvPath) {
        & "$venvPath\Scripts\Activate.ps1"
    }
}

# Adiciona a função ao seu perfil do PowerShell
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $profilePath -Parent

if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force
}

if (-not (Test-Path $profilePath)) {
    New-Item -ItemType File -Path $profilePath -Force
}

# Adiciona a função ao perfil se ainda não estiver lá
$functionContent = Get-Content $PSCommandPath -Raw
if (-not (Select-String -Path $profilePath -Pattern "function Activate-Venv" -Quiet)) {
    Add-Content -Path $profilePath -Value "`n$functionContent"
}

Write-Host "Função Activate-Venv adicionada ao seu perfil do PowerShell."
Write-Host "Para usar, navegue até a pasta do projeto e execute: Activate-Venv" 