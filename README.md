# ERPNext Assist

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-green.svg)](https://erpnext.com/)

> 🚀 Transform ERPNext into an AI-powered platform with visual tool creation, automatic background removal, and universal AI integration.

An ERPNext custom app that extends ERPNext with AI-powered tools using the Model Context Protocol (MCP). This app enables users to draft custom tools visually through the UI without programming knowledge, and integrates with various AI providers (online and offline).

## ✨ Quick Highlights

- 🎨 **No-Code Tool Builder** - Create custom tools visually, no programming required
- 📸 **AI Background Removal** - Professional product images with U²-Net AI
- 🤖 **Universal AI Support** - Works with Claude, OpenAI, Ollama, and custom providers
- 🔒 **Privacy-First** - All processing happens locally on your server
- 📦 **15 Ready-to-Use Tools** - Marketplace (with Norwegian message templates), camera, barcode, receipt scanner, price comparison, voice queries, RDS 81346, S1000D, GitHub import, warehouse finder, phone control, and more
- 🌐 **Offline Capable** - Full functionality without internet connection

## Features

### 🛠️ Visual Tool Drafting (No Programming Required)
- **Assist Tool Draft**: Create custom tools through an intuitive UI
- Define tool parameters, actions, and AI prompts visually
- Choose from multiple action types: Create Document, Update Document, API Call, or Custom Code
- Support for any AI provider (OpenAI, Claude, Local/Offline models via Ollama, etc.)

### 📦 Built-in Tools

#### 1. Marketplace Posting Tool with Pickup Orchestration & Norwegian Messages
- Post stock items or assets to marketplaces like Facebook Marketplace and FINN.no
- Automatically track and manage listings
- Save and monitor marketplace searches based on purchase or material requests
- **NEW**: Orchestrate efficient pickup routes by contacting sellers and scheduling optimal pickup days
- **NEW**: Standard Norwegian message templates for seller communication (price inquiries, storage, free goods, apologies)
- **NEW**: Phone control integration for automated marketplace browsing
- **NEW**: Material Request integration - automatically search for items from your purchase requests
- **DocTypes**: Marketplace Listing, Saved Marketplace Search
- **MCP Tools**: `post_to_marketplace`, `track_saved_search`, `orchestrate_pickup_route`, `manage_marketplace_listings_with_phone_ctrl`

#### 2. Camera-based Quick Item Addition with Dual AI Background Removal
- Quickly add new items (stock or assets) using camera capture
- **Dual AI-powered background removal**: 
  - Local processing with rembg + U²-Net AI model (privacy-focused, offline)
  - Cloud API via receipt-ocr.altlokalt.com (faster processing)
  - Automatic fallback between APIs
- Automatic image enhancement (brightness, contrast, sharpness)
- Perfect for warehouses with disorganized or new inventory
- Automatic image attachment and stock entry creation
- **MCP Tool**: `quick_add_item_from_camera`
- **API Endpoints**: 
  - `remove_image_background` - Remove background from any image (dual API support)
  - `enhance_image` - Enhance image quality
  - `quick_add_item` - Complete item addition with image processing

#### 3. Barcode Warehouse Location Scanner
- Scan barcodes to instantly check item warehouse locations
- View stock levels across all warehouses
- See default warehouse assignments
- **MCP Tool**: `scan_barcode_for_location`

#### 4. Receipt Scanner (OCR-powered)
- Scan receipt images and automatically extract items
- Add items as stock or assets with quantities and prices
- OCR-powered text extraction (requires pytesseract or similar)
- **MCP Tool**: `scan_receipt_and_add_items`

#### 5. Price Comparison with Prisjakt.no
- Compare prices across internal vendors and Prisjakt.no
- Pull complete vendor catalogs for suggestions
- Find the cheapest supplier for any item
- **MCP Tool**: `compare_vendor_prices`

#### 6. Natural Language Inventory Query (Voice-enabled)
- Ask inventory questions in plain language: "do we have pliers?"
- Voice-to-text compatible for hands-free operation
- Get instant answers about availability and location
- **MCP Tool**: `query_inventory_natural_language`

#### 7. RDS 81346 Equipment Reference Designation
- Generate ISO/IEC 81346 compliant reference designations
- Standardized equipment naming and documentation
- Support for function, product, location, and type aspects
- Hierarchical system structuring
- **MCP Tool**: `generate_rds_81346_designation`
- **API Endpoint**: `erpnext_assist.api.generate_rds_designation`

#### 8. S1000D Issue 6 Technical Documentation
- Create S1000D compliant data modules for technical publications
- XML-based modular documentation for aerospace/defense
- Common Source Database (CSDB) compatible structure
- Support for multiple content types (procedural, descriptive, fault, crew)
- **MCP Tool**: `create_s1000d_data_module`
- **API Endpoint**: `erpnext_assist.api.create_s1000d_module`

#### 9. GitHub Repos as Assets Importer
- Import all GitHub repositories from a user or organization
- Automatically create assets or items for each repository
- Capture metadata: stars, forks, language, description
- Support for private repos (with GitHub token)
- **MCP Tool**: `import_github_repos_as_assets`
- **API Endpoint**: `erpnext_assist.api.import_github_repos`

#### 10. Warehouse Finder (Norway-wide including Northern Norway)
- Find warehouses anywhere in Norway via FINN.no
- Search in northern regions like Tromsø, Bodø, Finnmark
- **Phone control support** for automated browsing
- Automatically add found warehouses to ERPNext
- Check 24/7 access and storage specifications
- **MCP Tool**: `find_warehouses_on_finn`
- **API Endpoint**: `erpnext_assist.api.find_warehouses`

#### 11. Enhanced Marketplace Communication with Material Requests
- Manage Facebook Marketplace and FINN.no listings with phone control
- Automatically fetch Material Request items for searching
- **Norwegian standard message templates** for seller communication:
  - **Standard**: "Hvor mye for hele bunken?"
  - **Storage**: "jeg vil gjerne prøve dere ut, passer idag og er tilgangen 24/7"
  - **Free Goods**: "Er disse forsatt ledig kan hente imørgen hvis det passer... 😃"
  - **Apology**: "Hei. Beklager sent svar men det var mange.., det er hentet"
- Add listings to saved lists for tracking
- **MCP Tool**: `manage_marketplace_listings_with_phone_ctrl`
- **API Endpoint**: `erpnext_assist.api.manage_marketplace_with_phone`

## Architecture

### MCP Integration
This app uses the Model Context Protocol (MCP) to expose ERPNext operations as tools that AI models can use. The MCP server:
- Runs locally or remotely
- Supports both stdio and HTTP transports
- Dynamically loads user-drafted tools from the database
- Works with any MCP-compatible AI client

### Directory Structure
```
erpnext_assist/
├── __init__.py              # App initialization
├── hooks.py                 # Frappe app hooks
├── modules.txt              # App modules
├── config/
│   └── desktop.py           # Desktop configuration
├── assist_tools/            # Main module
│   └── doctype/
│       ├── assist_tool_draft/          # Visual tool builder
│       ├── assist_tool_parameter/      # Tool parameters (child table)
│       ├── marketplace_listing/        # Marketplace listings
│       ├── marketplace_listing_image/  # Listing images (child table)
│       └── saved_marketplace_search/   # Saved searches
└── mcp_server/
    └── server.py            # MCP server implementation
```

## Installation

### Prerequisites
- ERPNext (v14 or v15)
- Python 3.10+
- Frappe Framework

### Install the App
```bash
# Get the app
bench get-app https://github.com/samletnorge/Assist---ERPNext

# Install on your site
bench --site [your-site-name] install-app erpnext_assist

# Restart bench
bench restart
```

## Usage

### Creating a Custom Tool (No Programming Required!)

1. Navigate to **Assist Tools > Assist Tool Draft**
2. Click **New**
3. Fill in the tool details:
   - **Tool Name**: A unique name for your tool
   - **Tool Description**: What the tool does
   - **AI Provider**: Choose your preferred AI (or "Any")
   - **Category**: Classify your tool (Inventory, Sales, etc.)

4. **Configure the AI Prompt**:
   - Write in natural language what you want the AI to do
   - Use `{{parameter_name}}` for variables
   - Example: "Create a purchase order for {{item_code}} with quantity {{qty}} from supplier {{supplier}}"

5. **Define Parameters**:
   - Add rows for each input your tool needs
   - Specify parameter name, type, and whether it's required
   - Example: item_code (Link to Item), qty (Number), supplier (Link to Supplier)

6. **Choose Action Type**:
   - **Create Document**: Create a new ERPNext document
   - **Update Document**: Modify an existing document
   - **API Call**: Call an external API endpoint
   - **Custom Code**: Write Python code (for advanced users)

7. **Save and Enable**: Your tool is now available through the MCP server!

### Running the MCP Server

#### Stdio Mode (for local AI clients)
```bash
cd /path/to/erpnext_assist
python -m erpnext_assist.mcp_server.server
```

#### HTTP Mode (for web-based AI clients)
```bash
export MCP_TRANSPORT=streamable-http
python -m erpnext_assist.mcp_server.server
```

### Using Built-in Tools

#### Post to Marketplace
```python
import frappe
from erpnext_assist.mcp_server.server import post_to_marketplace

result = post_to_marketplace(
    item_code="ITEM-001",
    marketplace="Facebook Marketplace",
    title="Quality Office Chair",
    description="Excellent condition, barely used",
    price=250.00,
    images=["/files/chair1.jpg", "/files/chair2.jpg"]
)
```

#### Quick Add Item from Camera with Background Removal
```python
from erpnext_assist.mcp_server.server import quick_add_item_from_camera

# With automatic background removal (default)
result = quick_add_item_from_camera(
    image_data="base64_encoded_image_data",
    warehouse="Main Warehouse",
    item_group="Products",
    valuation_rate=100.00,
    remove_background=True,  # AI-powered background removal
    enhance_image=True       # Automatic image enhancement
)

# Or use the API from client-side JavaScript
frappe.call({
    method: "erpnext_assist.api.quick_add_item",
    args: {
        image_data: base64_image,
        warehouse: "Main Warehouse",
        remove_background: true,
        enhance_image_quality: true
    },
    callback: function(r) {
        console.log(r.message);
    }
});
```

#### Remove Background from Existing Image
```python
from erpnext_assist.api import remove_image_background

result = remove_image_background(
    image_data="base64_encoded_image_data",
    enhance=True
)
# Returns: processed image with transparent background

)
```

#### Scan Barcode for Location
```python
from erpnext_assist.mcp_server.server import scan_barcode_for_location

result = scan_barcode_for_location(barcode="1234567890")
# Returns warehouse locations and stock levels
```

## MCP Client Configuration

### For Claude Desktop
Add to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "erpnext-assist": {
      "command": "python",
      "args": ["-m", "erpnext_assist.mcp_server.server"],
      "cwd": "/path/to/erpnext_assist"
    }
  }
}
```

### For Cursor/Other IDEs
Configure the MCP server endpoint in your IDE's settings to point to:
- Stdio: `python -m erpnext_assist.mcp_server.server`
- HTTP: `http://localhost:8000` (if running in HTTP mode)

## AI Provider Support

This app works with any AI provider that supports MCP:
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic Claude
- ✅ Local models via Ollama (Llama, Mistral, etc.) - **OFFLINE CAPABLE**
- ✅ Custom AI endpoints
- ✅ Any MCP-compatible AI client

## Image Processing Technology

### Automatic Background Removal
The camera tool uses AI-powered background removal (via `rembg` library) to create professional product images:
- **U²-Net model**: Deep learning model trained on thousands of images
- **Automatic subject detection**: Intelligently identifies the main subject
- **Clean transparent background**: Perfect for marketplaces and catalogs
- **Fast processing**: Typically completes in 2-5 seconds
- **Offline capable**: Runs locally without external API calls

### Image Enhancement
Automatic image quality improvements:
- **Brightness adjustment**: Ensures proper lighting (10% boost)
- **Contrast enhancement**: Makes details pop (10% boost)
- **Sharpness increase**: Crisper, clearer images (20% boost)

### Privacy & Performance
- All image processing happens **locally on your server**
- No external API calls or data sharing
- No subscription fees for image processing
- Works completely offline once models are downloaded

## Example Use Cases

### 1. Bulk Inventory Update Tool
Create a tool that updates multiple items at once:
- **Parameters**: item_codes (list), field_to_update (text), new_value (text)
- **Action**: Update Documents
- **No coding required** - just configure in the UI!

### 2. Smart Reorder Tool
Create a tool that analyzes stock and creates purchase orders:
- **Parameters**: warehouse (link), threshold (number)
- **Prompt**: "Analyze items below {{threshold}} quantity in {{warehouse}} and create purchase orders"
- **Action**: Multiple Actions

### 3. Customer Follow-up Scheduler
Create automated follow-ups:
- **Parameters**: customer (link), days_after_order (number)
- **Action**: Create Document (Task/ToDo)

## Development

### Running Tests
```bash
bench --site [site-name] run-tests --app erpnext_assist
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License

## Support
For issues and questions:
- GitHub Issues: https://github.com/samletnorge/Assist---ERPNext/issues
- Documentation: [Wiki](https://github.com/samletnorge/Assist---ERPNext/wiki)

## Credits
Built with:
- [Frappe Framework](https://frappeframework.com)
- [ERPNext](https://erpnext.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [machine-core](https://github.com/samletnorge/machine-core) for AI integration
