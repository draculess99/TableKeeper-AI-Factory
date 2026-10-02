# Verify clean container build and deployment readiness

Write-Host "========================================================================"
Write-Host "TableKeeper - Clean Container Verification"
Write-Host "========================================================================"
Write-Host ""

Write-Host "Step 1: Checking Docker installation..." -ForegroundColor Yellow
try {
    $version = docker --version
    Write-Host "Docker found: $version" -ForegroundColor Green
}
catch {
    Write-Host "Docker not found. Please install Docker." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Building Docker image..." -ForegroundColor Yellow
try {
    docker build -t tablekeeper-stage1 stage-1
    Write-Host "Image built successfully" -ForegroundColor Green
}
catch {
    Write-Host "Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Starting container..." -ForegroundColor Yellow
try {
    $id = docker run -d --network none -p 5000:5000 tablekeeper-stage1
    Write-Host "Container started: $id" -ForegroundColor Green
    Start-Sleep -Seconds 2
}
catch {
    Write-Host "Failed to run container" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4: Verifying container..." -ForegroundColor Yellow
try {
    $cmd = "docker inspect -f `"{{.State.Running}}`" $id"
    $status = Invoke-Expression $cmd
    if ($status -eq "true") {
        Write-Host "Container is running" -ForegroundColor Green
    }
    else {
        Write-Host "Container failed to start" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "Failed to inspect container" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================================================"
Write-Host "SUCCESS: Container verification complete" -ForegroundColor Green
Write-Host "========================================================================"
Write-Host ""
Write-Host "Application is running at: http://localhost:5000"
Write-Host ""
Write-Host "Stop container: docker stop $id"
Write-Host "Remove image: docker rmi tablekeeper-stage1"
