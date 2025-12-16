# How to Import Certificate in Windows (Step-by-Step)

## Method 1: Using Certificate Manager (certmgr.msc)

### Step 1: Open Certificate Manager
1. Press `Win + R` (Windows key + R)
2. Type: `certmgr.msc`
3. Press Enter

### Step 2: Navigate to Trusted Root Store
1. In the left panel, expand **"Trusted Root Certification Authorities"**
2. Click on **"Certificates"** (under Trusted Root Certification Authorities)

### Step 3: Import the Certificate
1. **Right-click** on "Certificates" folder
2. Select **"All Tasks"** → **"Import..."**
3. Click **"Next"** on the welcome screen
4. Click **"Browse..."** button
5. **Important:** Change file type dropdown to **"All Files (*.*)"** or **"PEM (*.pem)"**
6. Navigate to: `D:\UNI\ACS\ACSProject\ACS_Project\backend\cert.pem`
7. Select `cert.pem` and click **"Open"**
8. Click **"Next"**
9. Select **"Place all certificates in the following store"**
10. Verify it says: **"Trusted Root Certification Authorities"**
11. Click **"Next"**
12. Click **"Finish"**
13. Click **"Yes"** on the security warning

### Step 4: Verify Import
1. Look in the list of certificates
2. Find one with:
   - **Issued to:** localhost
   - **Issued by:** Course Registration System
3. If you see it, the import was successful!

---

## Method 2: Using PowerShell (Alternative)

Run this in PowerShell **as Administrator**:

```powershell
# Navigate to backend directory
cd D:\UNI\ACS\ACSProject\ACS_Project\backend

# Import certificate to Trusted Root store
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2("cert.pem")
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store([System.Security.Cryptography.X509Certificates.StoreName]::Root, "LocalMachine")
$store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
$store.Add($cert)
$store.Close()

Write-Host "Certificate imported successfully!" -ForegroundColor Green
```

---

## After Importing

### 1. Restart Your Browser
- **Close ALL browser windows completely**
- Don't just close tabs - close the entire browser
- Restart the browser

### 2. Clear Browser Cache (Optional but Recommended)
- Press `Ctrl + Shift + Delete`
- Select "Cached images and files"
- Click "Clear data"

### 3. Test the Certificate
- Visit: `https://localhost:8000`
- Should show **green lock** (secure connection)
- No certificate warnings

---

## Troubleshooting

### Still Shows "Not Secure"?

1. **Check you imported to the RIGHT location:**
   - Must be: **"Trusted Root Certification Authorities"** → **"Certificates"**
   - NOT: "Personal" or "Intermediate Certification Authorities"

2. **Verify the certificate is there:**
   - In certmgr.msc, look for certificate with "localhost" or "Course Registration System"
   - If not found, re-import following steps above

3. **Browser cache:**
   - Some browsers cache certificate warnings
   - Try **incognito/private mode**: `Ctrl + Shift + N`
   - Or clear all browsing data

4. **Try different browser:**
   - Test in Chrome, Edge, or Firefox
   - If one works, it's a browser-specific cache issue

5. **Check certificate format:**
   - Make sure you selected `cert.pem` (not `key.pem`)
   - File should start with `-----BEGIN CERTIFICATE-----`

---

## Quick Verification

After importing, run this to verify:

```powershell
cd D:\UNI\ACS\ACSProject\ACS_Project\backend
powershell -ExecutionPolicy Bypass -File troubleshoot_certificate.ps1
```

It should show: `[OK] Found certificate in Trusted Root Certification Authorities`


