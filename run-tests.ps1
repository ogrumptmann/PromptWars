# Run all tests locally before committing
# This script runs tests in Docker containers

$ErrorActionPreference = "Stop"

Write-Host "Running all tests..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Backend Tests..." -ForegroundColor Yellow
docker-compose exec -T backend python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=50
if ($LASTEXITCODE -ne 0) {
    Write-Host "Backend tests failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Backend tests passed!" -ForegroundColor Green
Write-Host ""

Write-Host "Frontend Tests..." -ForegroundColor Yellow
docker-compose exec -T frontend npm test -- --run
if ($LASTEXITCODE -ne 0) {
    Write-Host "Frontend tests failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Frontend tests passed!" -ForegroundColor Green
Write-Host ""

Write-Host "All tests passed! Ready to commit." -ForegroundColor Green

