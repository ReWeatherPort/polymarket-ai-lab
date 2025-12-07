# Simple smoke test for local static server + key pages
# Usage: Open PowerShell, run: `.	ools\smoke_test.ps1` or `powershell -NoProfile -File scripts/smoke_test.ps1`

Write-Host "Starting local static server (python -m http.server 8000)..."
try {
  $py = Get-Command python -ErrorAction Stop | Select-Object -ExpandProperty Source
} catch {
  Write-Error "Python not found in PATH. Install Python or run the server manually."; exit 1
}

$proc = Start-Process -FilePath $py -ArgumentList '-m','http.server','8000' -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 1

$urls = @(
  'http://localhost:8000/index.html',
  'http://localhost:8000/post.html?post=content/posts/okc-experiment-2025-01-01.md',
  'http://localhost:8000/post.html?post=content/posts/nba2024-25evkelly.md',
  'http://localhost:8000/new-post.html',
  'http://localhost:8000/experiments/index.html',
  'http://localhost:8000/assets/favicon/favicon.svg'
)

foreach ($u in $urls) {
  try {
    $r = Invoke-WebRequest -Uri $u -UseBasicParsing -Method GET -ErrorAction Stop -TimeoutSec 10
    Write-Host "$u => $($r.StatusCode)"
  } catch {
    Write-Host "$u => ERROR: $($_.Exception.Message)"
  }
}

Write-Host "Stopping local server (PID $($proc.Id))..."
try { Stop-Process -Id $proc.Id -ErrorAction SilentlyContinue } catch {}
Write-Host "Done."
