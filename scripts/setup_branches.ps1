# ============================================================
# FedMed - Setup All 5 Member Branches
# Run this ONCE before starting Week 1
# Member 5 (Ravi) runs this on Day 1
# ============================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  FedMed - Creating All Member Branches   " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$branches = @(
    "feature/chaitanya/unet-architecture",
    "feature/ranjith/data-preprocessing",
    "feature/kushi/fl-server",
    "feature/vasusree/hospital-nodes",
    "feature/ravi/integration"
)

# Make sure we are on master/main
git checkout master 2>$null
if ($LASTEXITCODE -ne 0) { git checkout main }

# Create dev branch first
git checkout -b dev
Write-Host "[+] Created branch: dev" -ForegroundColor Green
git checkout master 2>$null
if ($LASTEXITCODE -ne 0) { git checkout main }

# Create each member's feature branch
foreach ($branch in $branches) {
    git checkout -b $branch
    Write-Host "[+] Created branch: $branch" -ForegroundColor Green
    git checkout master 2>$null
    if ($LASTEXITCODE -ne 0) { git checkout main }
}

Write-Host ""
Write-Host "All branches created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Branches:" -ForegroundColor Yellow
git branch --list
Write-Host ""
Write-Host "Next: Add GitHub remote and push all branches" -ForegroundColor Yellow
Write-Host "  git remote add origin https://github.com/<your-org>/fedmed.git" -ForegroundColor Gray
Write-Host "  git push --all origin" -ForegroundColor Gray
