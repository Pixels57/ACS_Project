# Guide: Trusting the Local Development Certificate

This guide explains how to trust the self-signed certificate generated for local development, so browsers and clients don't show certificate warnings.

## Quick Setup (Recommended: mkcert)

The easiest way to set up trusted local certificates is using [mkcert](https://github.com/FiloSottile/mkcert):

### Installation

**Windows:**
```powershell
# Using Chocolatey
choco install mkcert

# Or download from: https://github.com/FiloSottile/mkcert/releases
```

**macOS:**
```bash
brew install mkcert
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install libnss3-tools
# Download from: https://github.com/FiloSottile/mkcert/releases
```

### Setup

1. **Install the local CA:**
   ```bash
   mkcert -install
   ```

2. **Generate certificate for localhost:**
   ```bash
   cd backend
   mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1
   ```

3. **Done!** The certificate is now trusted by your system.

---

## Manual Setup: Trust the Generated Certificate

If you prefer to use the generated certificate, follow these steps:

### Windows

1. **Open Certificate Manager:**
   - Press `Win + R`
   - Type `certmgr.msc` and press Enter

2. **Import Certificate:**
   - Navigate to: `Trusted Root Certification Authorities` → `Certificates`
   - Right-click → `All Tasks` → `Import...`
   - Browse to `backend/cert.pem`
   - Click `Next` → `Finish`
   - Confirm the security warning

3. **Verify:**
   - Restart your browser
   - Visit `https://localhost:8000`
   - Should show as secure (no warnings)

### macOS

1. **Open Keychain Access:**
   - Open `Keychain Access` application
   - Or run: `open /Applications/Utilities/Keychain\ Access.app`

2. **Import Certificate:**
   - File → Import Items...
   - Select `backend/cert.pem`
   - Choose "System" keychain (requires password)

3. **Trust Certificate:**
   - Find the certificate in the list
   - Double-click to open
   - Expand "Trust" section
   - Set "When using this certificate" to "Always Trust"
   - Close and enter password

4. **Verify:**
   - Restart your browser
   - Visit `https://localhost:8000`
   - Should show as secure (no warnings)

### Linux

1. **Copy certificate to system store:**
   ```bash
   sudo cp backend/cert.pem /usr/local/share/ca-certificates/localhost.crt
   ```

2. **Update CA certificates:**
   ```bash
   sudo update-ca-certificates
   ```

3. **Verify:**
   ```bash
   curl https://localhost:8000
   # Should work without -k flag
   ```

---

## Frontend Configuration

The frontend Vite proxy is already configured to accept the certificate. If you need to verify:

**Check `frontend/vite.config.js`:**
```javascript
proxy: {
  '/api': {
    target: backendUrl,
    changeOrigin: true,
    secure: !useHttp ? false : undefined,  // false = accept self-signed certs
  }
}
```

The `secure: false` option tells the proxy to accept self-signed certificates.

---

## Python/Requests Configuration

If you're using Python requests or other clients:

### Option 1: Disable Verification (Not Recommended for Production)
```python
import requests
response = requests.get('https://localhost:8000', verify=False)
```

### Option 2: Use Custom CA Bundle (Recommended)
```python
import requests
response = requests.get('https://localhost:8000', verify='backend/cert.pem')
```

### Option 3: Add to System CA Store (Best)
After trusting the certificate in your system (see above), Python will automatically trust it:
```python
import requests
response = requests.get('https://localhost:8000')  # Works automatically
```

---

## Verification

### Browser Test
1. Visit `https://localhost:8000`
2. Should show secure connection (green lock icon)
3. No certificate warnings

### Command Line Test
```bash
# Should work without -k flag after trusting
curl https://localhost:8000

# Check certificate details
openssl s_client -connect localhost:8000 -showcerts
```

### Python Test
```python
import requests

# Should work after trusting certificate
try:
    response = requests.get('https://localhost:8000')
    print(f"Success: {response.status_code}")
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
    print("Certificate not trusted. Follow the guide above.")
```

---

## Troubleshooting

### Browser Still Shows Warning
- Clear browser cache and restart
- Make sure you imported to the correct certificate store
- Check that certificate is valid (not expired)
- Verify certificate Common Name matches `localhost`

### Python Requests Fails
- Make sure certificate is in system CA store
- Or use `verify='backend/cert.pem'` parameter
- Check certificate expiration date

### Certificate Expired
- Regenerate certificate: `python backend/generate_trusted_cert.py`
- Re-import to certificate store

---

## Security Notes

- **Development Only:** Self-signed certificates are for local development only
- **Production:** Use certificates from a trusted CA (Let's Encrypt, commercial CA)
- **Key Security:** Keep `key.pem` private and never commit to version control
- **Certificate Rotation:** Regenerate certificates periodically (annually recommended)


