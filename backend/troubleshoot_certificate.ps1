# PowerShell script to troubleshoot certificate trust issues

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Certificate Trust Troubleshooting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if certificate file exists
$certPath = "cert.pem"
if (Test-Path $certPath) {
    Write-Host "[OK] Certificate file exists: $certPath" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Certificate file not found: $certPath" -ForegroundColor Red
    Write-Host "Run: python generate_trusted_cert.py" -ForegroundColor Yellow
    exit
}

# Check if certificate is in Windows certificate store
Write-Host ""
Write-Host "Checking Windows Certificate Store..." -ForegroundColor Cyan
Write-Host ""

try {
    $cert = Get-ChildItem -Path Cert:\LocalMachine\Root | Where-Object { 
        $_.Subject -like "*localhost*" -or $_.Subject -like "*Course Registration System*"
    }
    
    if ($cert) {
        Write-Host "[OK] Found certificate in Trusted Root Certification Authorities:" -ForegroundColor Green
        Write-Host "    Subject: $($cert.Subject)" -ForegroundColor Gray
        Write-Host "    Thumbprint: $($cert.Thumbprint)" -ForegroundColor Gray
        Write-Host "    Valid Until: $($cert.NotAfter)" -ForegroundColor Gray
    } else {
        Write-Host "[WARNING] Certificate not found in Trusted Root store" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To import the certificate:" -ForegroundColor Yellow
        Write-Host "1. Open certmgr.msc" -ForegroundColor White
        Write-Host "2. Navigate to: Trusted Root Certification Authorities -> Certificates" -ForegroundColor White
        Write-Host "3. Right-click -> All Tasks -> Import..." -ForegroundColor White
        Write-Host "4. Select: $((Get-Location).Path)\cert.pem" -ForegroundColor White
        Write-Host "5. Click Next -> Finish" -ForegroundColor White
    }
} catch {
    Write-Host "[ERROR] Could not check certificate store: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Browser-Specific Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Chrome/Edge:" -ForegroundColor Yellow
Write-Host "1. Close ALL browser windows completely" -ForegroundColor White
Write-Host "2. Clear browser cache (Ctrl+Shift+Delete)" -ForegroundColor White
Write-Host "3. Restart browser" -ForegroundColor White
Write-Host "4. Visit: https://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Firefox:" -ForegroundColor Yellow
Write-Host "1. Firefox uses its own certificate store" -ForegroundColor White
Write-Host "2. Visit: https://localhost:8000" -ForegroundColor White
Write-Host "3. Click 'Advanced' -> 'Accept the Risk and Continue'" -ForegroundColor White
Write-Host "4. Or import cert.pem in Firefox: Settings -> Privacy & Security -> Certificates -> View Certificates -> Authorities -> Import" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan


