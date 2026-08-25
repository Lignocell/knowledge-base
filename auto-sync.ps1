Set-Location "D:\knowledge_point"

Write-Host "Checking Git repository..."

git add -A

git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "No changes. Nothing to sync."
    exit 0
}

$date = Get-Date -Format "yyyy-MM-dd HH:mm"

Write-Host "Changes detected. Committing..."
git commit -m "Auto sync $date"

Write-Host "Pulling remote changes..."
git pull --rebase origin main

Write-Host "Pushing to GitHub..."
git push origin main

Write-Host "Sync completed."