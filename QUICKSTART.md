# Quick Start Guide - ERPNext Assist

## Installation

### Step 1: Get the App
```bash
# Clone or get the app
cd /path/to/frappe-bench
bench get-app https://github.com/samletnorge/Assist---ERPNext erpnext_assist

# Or if already cloned
bench get-app /path/to/Assist---ERPNext
```

### Step 2: Install on Your Site
```bash
bench --site [your-site-name] install-app erpnext_assist
```

### Step 3: Install Dependencies
```bash
# The app requires additional Python packages
cd apps/erpnext_assist
pip install -r requirements.txt

# Download the background removal AI model (first time only)
# This happens automatically on first use, but you can pre-download:
python -c "from rembg import remove; print('Model downloaded!')"
```

### Step 4: Restart
```bash
bench restart
```

## First Steps

### 1. Create Your First Visual Tool (No Programming!)

1. Open ERPNext and navigate to: **Assist Tools > Assist Tool Draft**
2. Click **New**
3. Fill in:
   - **Tool Name**: "Quick Purchase Order Creator"
   - **Tool Description**: "Create a purchase order with one click"
   - **Category**: Purchasing
   - **AI Provider**: Any (or select your preferred AI)

4. In **Prompt Template**, write:
   ```
   Create a purchase order for {{item_code}} with quantity {{quantity}} 
   from supplier {{supplier}}. Set required by date to {{required_date}}.
   ```

5. Add **Parameters**:
   | Parameter Name | Type | Required | Description |
   |---------------|------|----------|-------------|
   | item_code | Link | ✓ | Item to purchase |
   | quantity | Number | ✓ | Quantity needed |
   | supplier | Link | ✓ | Supplier name |
   | required_date | Date | ✓ | When needed |

6. Set **Action Type**: "Create Document"
7. Set **Target DocType**: "Purchase Order"
8. Click **Save** and enable it!

Your tool is now available through the MCP server for AI assistants to use!

### 2. Try Camera-Based Item Addition

From your ERPNext mobile or desktop:

```javascript
// Take a photo and add item with background removal
frappe.call({
    method: "erpnext_assist.api.quick_add_item",
    args: {
        image_data: camera_base64_image,
        warehouse: "Main Warehouse",
        item_group: "Products",
        remove_background: true,  // AI removes background!
        enhance_image_quality: true
    },
    callback: function(r) {
        if (r.message.success) {
            frappe.msgprint(`Item ${r.message.item_code} created!`);
        }
    }
});
```

### 3. Scan Barcode for Location

```python
import frappe
from erpnext_assist.mcp_server.server import scan_barcode_for_location

# Quick barcode lookup
result = scan_barcode_for_location("1234567890")
print(f"Item: {result['item_name']}")
print(f"Main location: {result['default_warehouse']}")
print(f"All locations: {result['stock_locations']}")
```

### 4. Post to Marketplace

```python
from erpnext_assist.mcp_server.server import post_to_marketplace

result = post_to_marketplace(
    item_code="CHAIR-001",
    marketplace="Facebook Marketplace",
    title="Office Chair - Like New",
    description="Ergonomic office chair, barely used",
    price=150.00,
    images=["/files/chair_front.jpg"]
)
```

## Running the MCP Server

### For Local AI (Ollama, Claude Desktop, etc.)
```bash
cd apps/erpnext_assist
python -m erpnext_assist.mcp_server.server
```

### Configure Claude Desktop
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "erpnext": {
      "command": "python",
      "args": ["-m", "erpnext_assist.mcp_server.server"],
      "cwd": "/path/to/frappe-bench/apps/erpnext_assist"
    }
  }
}
```

Restart Claude Desktop, and your tools will be available!

## Troubleshooting

### Background Removal Not Working
```bash
# Install dependencies
pip install rembg pillow

# Test it
python -c "from erpnext_assist.utils.image_processing import remove_background; print('Working!')"
```

### MCP Server Won't Start
```bash
# Check if MCP is installed
pip install "mcp[cli]"

# Test the server
python -m erpnext_assist.mcp_server.server
# Should print: "Loaded X user-drafted tools"
```

### Tools Not Showing in AI
1. Make sure tools are **Enabled** in Assist Tool Draft
2. Restart the MCP server
3. Restart your AI client (Claude Desktop, etc.)

## Next Steps

- **Create more tools**: Build a library of custom tools for your workflow
- **Explore DocTypes**: Check out Marketplace Listing and Saved Marketplace Search
- **Integrate with AI**: Connect to your preferred AI provider
- **Customize**: Modify the MCP server for your specific needs

## Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/samletnorge/Assist---ERPNext/issues)
- 💬 [Community Forum](https://discuss.erpnext.com)
