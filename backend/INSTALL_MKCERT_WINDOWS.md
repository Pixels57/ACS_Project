# Installing mkcert on Windows

## Option 1: Using Chocolatey (Recommended)

If you have Chocolatey installed:

```powershell
choco install mkcert
```

## Option 2: Manual Installation

1. **Download mkcert:**
   - Go to: https://github.com/FiloSottile/mkcert/releases
   - Download `mkcert-v1.4.4-windows-amd64.exe` (or latest version)
   - Rename it to `mkcert.exe`

2. **Add to PATH:**
   - Create a folder (e.g., `C:\tools\mkcert`)
   - Move `mkcert.exe` to that folder
   - Add the folder to your PATH:
     - Press `Win + X` → System → Advanced system settings
     - Click "Environment Variables"
     - Under "User variables", find "Path" and click "Edit"
     - Click "New" and add `C:\tools\mkcert` (or your folder path)
     - Click OK on all dialogs

3. **Verify installation:**
   ```powershell
   mkcert --version
   ```

## Option 3: Use Without Installing (Quick Test)

You can run mkcert directly without installing:

```powershell
# Download and run directly
# Replace with latest version from GitHub releases
.\mkcert-v1.4.4-windows-amd64.exe -install
.\mkcert-v1.4.4-windows-amd64.exe -key-file backend/key.pem -cert-file backend/cert.pem localhost 127.0.0.1 ::1
```

## After Installation

Once mkcert is installed:

```powershell
# Install the local CA
mkcert -install

# Generate trusted certificate
cd backend
mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1
```

---

## Alternative: Manual Certificate Trust (No mkcert Needed)

If you don't want to install mkcert, you can trust the existing certificate manually:

1. **Open Certificate Manager:**
   - Press `Win + R`
   - Type `certmgr.msc` and press Enter

2. **Import Certificate:**
   - Navigate to: `Trusted Root Certification Authorities` → `Certificates`
   - Right-click → `All Tasks` → `Import...`
   - Click "Browse" and navigate to `backend\cert.pem`
   - Select "PEM (*.pem)" from file type dropdown if needed
   - Click `Next` → `Finish`
   - Confirm the security warning

3. **Restart your browser** and visit `https://localhost:8000`
   - Should now show as secure (no warnings)


