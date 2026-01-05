# Installation Guide for Private Local ERPNext Instance

This guide walks you through installing ERPNext Assist on your own private local ERPNext instance.

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu 20.04 LTS or later (recommended), macOS, or Windows with WSL2
- **Python**: 3.10 or higher
- **Node.js**: 14.x or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 10GB free

### Required Software
- ERPNext v14 or v15 installed and running
- Frappe Bench setup
- Git
- pip (Python package manager)

## Installation Steps

### Step 1: Access Your ERPNext Instance

First, ensure your ERPNext instance is running:

```bash
# Navigate to your bench directory
cd /path/to/frappe-bench

# Check bench status
bench status
```

If ERPNext is not running, start it:

```bash
bench start
```

### Step 2: Get the ERPNext Assist App

There are two ways to get the app:

#### Option A: Clone from GitHub (Recommended)

```bash
# From your bench directory
cd /path/to/frappe-bench

# Get the app
bench get-app https://github.com/samletnorge/Assist---ERPNext erpnext_assist
```

#### Option B: Install from Local Directory

If you have the app downloaded locally:

```bash
# From your bench directory
cd /path/to/frappe-bench

# Get the app from local path
bench get-app /path/to/Assist---ERPNext
```

### Step 3: Install the App on Your Site

```bash
# Install on your site (replace 'your-site-name' with your actual site name)
bench --site your-site-name install-app erpnext_assist

# Example:
# bench --site mycompany.localhost install-app erpnext_assist
```

To find your site name:
```bash
bench --site list
```

### Step 4: Install Python Dependencies

The app requires additional Python libraries:

```bash
# Navigate to the app directory
cd apps/erpnext_assist

# Install required dependencies
pip install -r requirements.txt
```

**Core Dependencies:**
- `mcp[cli]>=1.0.0` - Model Context Protocol
- `rembg>=2.0.0` - AI background removal (U²-Net model)
- `pillow>=10.0.0` - Image processing

**Optional Dependencies:**

For receipt scanning (OCR):
```bash
# Install system package first
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
# or
brew install tesseract              # macOS

# Then install Python package
pip install pytesseract>=0.3.10
```

### Step 5: Download AI Models (First Time Only)

The background removal feature uses AI models that need to be downloaded on first use:

```bash
# Pre-download the U²-Net model (optional but recommended)
python3 << EOF
from rembg import remove
print("Downloading U²-Net model...")
# Model will be downloaded automatically on first import
print("Model downloaded successfully!")
EOF
```

This may take a few minutes depending on your internet connection.

### Step 6: Restart Your ERPNext Instance

```bash
# Navigate back to bench directory
cd /path/to/frappe-bench

# Restart all services
bench restart
```

### Step 7: Verify Installation

Run the included verification script:

```bash
# From the app directory
cd apps/erpnext_assist
python verify_installation.py
```

Expected output should show:
```
✅ Python 3.10+ - OK
✅ App package - found
✅ MCP server - found
✅ All DocTypes - found
```

### Step 8: Access ERPNext Assist

1. **Log in to your ERPNext instance**:
   ```
   http://your-site-name:8000
   ```

2. **Navigate to Assist Tools**:
   - Go to: Modules → Assist Tools
   - Or search for "Assist Tool Draft" in the search bar

3. **Create your first tool**:
   - Click "New" to create an Assist Tool Draft
   - Follow the visual tool builder to create a custom tool

## Configuration

### MCP Server Setup

The MCP server allows AI integration with various providers.

#### For Local Development (stdio mode)

```bash
# Navigate to app directory
cd apps/erpnext_assist

# Run MCP server in stdio mode (default)
python -m erpnext_assist.mcp_server.server
```

#### For Remote Access (HTTP mode)

```bash
# Set environment variables
export MCP_TRANSPORT=streamable-http
export MCP_PORT=8000

# Run MCP server
python -m erpnext_assist.mcp_server.server
```

#### As a Systemd Service (Production)

Create `/etc/systemd/system/erpnext-mcp.service`:

```ini
[Unit]
Description=ERPNext Assist MCP Server
After=network.target

[Service]
Type=simple
User=frappe
WorkingDirectory=/path/to/frappe-bench/apps/erpnext_assist
Environment="MCP_TRANSPORT=streamable-http"
Environment="MCP_PORT=8000"
ExecStart=/usr/bin/python3 -m erpnext_assist.mcp_server.server
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable erpnext-mcp
sudo systemctl start erpnext-mcp
sudo systemctl status erpnext-mcp
```

### AI Client Configuration

#### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "erpnext-assist": {
      "command": "python3",
      "args": ["-m", "erpnext_assist.mcp_server.server"],
      "cwd": "/path/to/frappe-bench/apps/erpnext_assist"
    }
  }
}
```

#### Ollama (Offline AI)

Install Ollama for offline AI capabilities:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model (e.g., llama2)
ollama pull llama2

# Start Ollama
ollama serve
```

The MCP server works with Ollama automatically.

## Testing the Installation

### Test 1: Visual Tool Builder

1. Navigate to: **Assist Tools → Assist Tool Draft**
2. Click **New**
3. Create a simple tool:
   - **Tool Name**: "Test Tool"
   - **Description**: "A test tool"
   - **Prompt**: "Return success message"
   - **Action Type**: "Custom Code"
   - **Code**: `result = {"success": True, "message": "Test passed!"}`
4. Save and enable the tool

### Test 2: Background Removal

Test the AI background removal feature:

```python
# In ERPNext Console (bench console)
import frappe
from erpnext_assist.api import remove_image_background

# Test with a sample image (base64 encoded)
result = remove_image_background(
    image_data="your_base64_image_data",
    enhance=True
)
print(result)
```

### Test 3: Natural Language Queries

```python
# In ERPNext Console
from erpnext_assist.api import ask_inventory

result = ask_inventory("do we have any items in stock?")
print(result['response'])
```

### Test 4: MCP Server

```bash
# Test MCP server is running
cd apps/erpnext_assist
python -m erpnext_assist.mcp_server.server

# Should output:
# Loaded X user-drafted tools
# MCP server running on stdio transport
```

## Troubleshooting

### Issue: App Installation Fails

**Error**: `App erpnext_assist not found`

**Solution**:
```bash
# Ensure the app is in the apps directory
ls apps/ | grep erpnext_assist

# If not found, re-run get-app
bench get-app https://github.com/samletnorge/Assist---ERPNext erpnext_assist
```

### Issue: Module Import Errors

**Error**: `No module named 'mcp'` or `No module named 'rembg'`

**Solution**:
```bash
# Reinstall dependencies
cd apps/erpnext_assist
pip install -r requirements.txt

# For virtual environment
source env/bin/activate
pip install -r apps/erpnext_assist/requirements.txt
```

### Issue: Background Removal Not Working

**Error**: `Failed to remove background`

**Solution**:
```bash
# Install rembg and download models
pip install rembg>=2.0.0

# Pre-download model
python3 -c "from rembg import remove; print('Model ready')"
```

### Issue: Permission Errors

**Error**: `Permission denied`

**Solution**:
```bash
# Fix ownership
sudo chown -R $USER:$USER /path/to/frappe-bench/apps/erpnext_assist

# Fix permissions
chmod -R 755 /path/to/frappe-bench/apps/erpnext_assist
```

### Issue: Port Already in Use (MCP Server)

**Error**: `Address already in use`

**Solution**:
```bash
# Find and kill the process using the port
lsof -i :8000
kill -9 <PID>

# Or use a different port
export MCP_PORT=8001
python -m erpnext_assist.mcp_server.server
```

### Issue: Database Migration Errors

**Error**: `Migration failed`

**Solution**:
```bash
# Run migrations manually
bench --site your-site-name migrate

# If that fails, try:
bench --site your-site-name migrate --skip-failing
```

## Updating the App

To update to the latest version:

```bash
# Navigate to bench directory
cd /path/to/frappe-bench

# Pull latest changes
cd apps/erpnext_assist
git pull origin main

# Go back to bench directory
cd ../..

# Run migrations
bench --site your-site-name migrate

# Clear cache
bench --site your-site-name clear-cache

# Restart
bench restart
```

## Uninstallation

If you need to remove the app:

```bash
# Uninstall from site
bench --site your-site-name uninstall-app erpnext_assist

# Remove app files
rm -rf apps/erpnext_assist

# Restart
bench restart
```

## Security Considerations

### For Production Environments

1. **Use HTTPS**: Always use HTTPS for remote MCP server access
   ```bash
   # Use nginx or similar reverse proxy
   # Configure SSL certificates
   ```

2. **Firewall Rules**: Restrict MCP server port access
   ```bash
   # Only allow specific IPs
   sudo ufw allow from 192.168.1.0/24 to any port 8000
   ```

3. **Authentication**: Enable authentication for MCP server
   ```bash
   # Set environment variable
   export MCP_AUTH_TOKEN="your-secure-token"
   ```

4. **File Permissions**: Ensure proper file permissions
   ```bash
   # Restrict access to app directory
   chmod 750 /path/to/frappe-bench/apps/erpnext_assist
   ```

5. **Regular Updates**: Keep the app updated
   ```bash
   # Set up automatic updates (optional)
   crontab -e
   # Add: 0 2 * * * cd /path/to/frappe-bench/apps/erpnext_assist && git pull
   ```

## Performance Optimization

### Enable Caching

```bash
# In site_config.json
{
  "cache_backend": "redis",
  "redis_cache": "redis://localhost:6379"
}
```

### Background Job Queue

For heavy operations like background removal:

```bash
# Start background workers
bench worker --queue short,default,long
```

### Database Optimization

```bash
# Optimize database
bench --site your-site-name mariadb
> OPTIMIZE TABLE `tabAssist Tool Draft`;
> OPTIMIZE TABLE `tabMarketplace Listing`;
> exit
```

## Getting Help

### Documentation
- **README.md** - Overview and features
- **QUICKSTART.md** - Quick start guide
- **EXAMPLES.md** - 13 tool examples
- **STANDARDS_TOOLS.md** - RDS 81346 & S1000D guide
- **NEW_TOOLS_SUMMARY.md** - New tools documentation

### Community
- [GitHub Issues](https://github.com/samletnorge/Assist---ERPNext/issues)
- [ERPNext Forum](https://discuss.erpnext.com)

### Logs
Check logs for debugging:
```bash
# Frappe logs
tail -f /path/to/frappe-bench/logs/bench.log

# Error logs
tail -f /path/to/frappe-bench/logs/error.log

# MCP server logs (if running as service)
sudo journalctl -u erpnext-mcp -f
```

## Next Steps

After successful installation:

1. **Explore Built-in Tools**: Try the 12 built-in MCP tools
2. **Create Custom Tools**: Use the visual tool builder
3. **Configure AI**: Set up your preferred AI provider
4. **Read Examples**: Check EXAMPLES.md for 13 ready-to-use templates
5. **Join Community**: Share your tools and get help

## Advanced Configuration

### Multi-Site Setup

For multiple ERPNext sites:

```bash
# Install on multiple sites
bench --site site1.local install-app erpnext_assist
bench --site site2.local install-app erpnext_assist

# Run separate MCP servers
MCP_PORT=8001 FRAPPE_SITE=site1.local python -m erpnext_assist.mcp_server.server &
MCP_PORT=8002 FRAPPE_SITE=site2.local python -m erpnext_assist.mcp_server.server &
```

### Docker Deployment

For Docker-based ERPNext:

```dockerfile
# Add to your Dockerfile
RUN pip install mcp[cli]>=1.0.0 rembg>=2.0.0 pillow>=10.0.0

# Optionally add OCR support
RUN apt-get update && apt-get install -y tesseract-ocr
RUN pip install pytesseract>=0.3.10
```

### Development Mode

For developers wanting to modify the app:

```bash
# Enable developer mode
bench --site your-site-name set-config developer_mode 1

# Watch for changes
bench watch

# Run in debug mode
bench --site your-site-name console
```

---

**Installation Complete!** You now have ERPNext Assist running on your private local instance. Start creating tools and automating your ERP workflows! 🎉
