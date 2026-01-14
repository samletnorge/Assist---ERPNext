# New Tools Summary - Update

This document describes the new tools added based on user feedback.

## Overview

Following feedback from users, we've added powerful new tools to ERPNext Assist:

1. **Receipt Scanner** - OCR-powered automatic item addition
2. **Price Comparison** - Prisjakt.no integration with vendor catalogs
3. **Natural Language Voice Queries** - Spoken inventory questions
4. **Pickup Route Orchestration** - Enhanced marketplace tool
5. **Asset Rental Posting** - NEW! Post company assets to rental services like leid.no

## Tool 7: Asset Rental Posting 🛠️💰

**Purpose**: Post company-owned assets (tools, equipment) to rental services like leid.no

**MCP Tools**: 
- `post_asset_for_rental()` - Post assets to rental marketplaces
- `get_rental_eligible_assets()` - Query assets suitable for rental

**API Endpoints**: 
- `erpnext_assist.api.post_rental_listing` - Post asset for rental
- `erpnext_assist.api.get_rental_assets` - Get rental-eligible assets

**Features**:
- Post company-owned assets to leid.no and other rental services
- Automatic identification of rental-eligible assets by chart of account codes
- Support for Norwegian accounting standards (NS 4102):
  - 1202 - Maskiner og anlegg (Machinery and equipment)
  - 1203 - Inventar (Furniture and fixtures)
  - 1204 - Transportmidler (Transport equipment)
- Track rental listings separately from sales
- Set rental rates and terms

**Marketplace Listing Enhancements**:
- New "Listing Type" field: Sale or Rental
- New "Asset Code" field for linking assets
- New marketplace options: leid.no, Other Rental Service
- New status: "Rented" for tracking rental agreements
- Conditional display: Item Code for Sales, Asset Code for Rentals

**Parameters for `post_asset_for_rental()`**:
- `asset_code` (str): ERPNext asset code to rent out
- `marketplace` (str): Target rental service (e.g., "leid.no")
- `title` (str): Listing title
- `description` (str): Detailed description
- `rental_rate` (float): Rate per period (day/week/month)
- `images` (list, optional): Asset images

**Parameters for `get_rental_eligible_assets()`**:
- `company` (str, optional): Company name
- `asset_category` (str, optional): Filter by category
- `chart_of_account_code` (str, optional): Filter by account code (e.g., "1202")

**Returns from `get_rental_eligible_assets()`**:
```json
{
    "success": true,
    "company": "My Company",
    "count": 5,
    "assets": [
        {
            "asset_code": "DRILL-HYD-001",
            "asset_name": "Hydraulic Drill",
            "item_code": "DRILL-001",
            "category": "Machinery",
            "purchase_amount": 15000.00,
            "location": "Main Warehouse",
            "status": "Available for use"
        }
    ]
}
```

**Usage Examples**:

```python
# Get all machinery suitable for rental (account code 1202)
from erpnext_assist.mcp_server.server import get_rental_eligible_assets

result = get_rental_eligible_assets(
    company="My Company",
    chart_of_account_code="1202"  # Maskiner og anlegg
)

for asset in result["assets"]:
    print(f"{asset['asset_name']} - {asset['category']}")

# Post an asset to leid.no
from erpnext_assist.mcp_server.server import post_asset_for_rental

result = post_asset_for_rental(
    asset_code="DRILL-HYD-001",
    marketplace="leid.no",
    title="Professional Hydraulic Drill for Rent",
    description="High-power drill for heavy construction. Daily and weekly rates available.",
    rental_rate=750.00,  # NOK per day
    images=["/files/drill1.jpg", "/files/drill2.jpg"]
)
```

**From UI/API**:
```javascript
// Get rental assets
frappe.call({
    method: "erpnext_assist.api.get_rental_assets",
    args: {
        company: "My Company",
        chart_of_account_code: "1202"
    },
    callback: function(r) {
        console.log(r.message.assets);
    }
});

// Post rental listing
frappe.call({
    method: "erpnext_assist.api.post_rental_listing",
    args: {
        asset_code: "DRILL-HYD-001",
        marketplace: "leid.no",
        title: "Professional Hydraulic Drill",
        description: "Available for daily/weekly rental",
        rental_rate: 750.00,
        images: JSON.stringify(["/files/drill1.jpg"])
    }
});
```

**Use Cases**:
1. **Equipment Rental Business**: Post company tools to rental platforms
2. **Asset Utilization**: Monetize idle assets through rentals
3. **Seasonal Equipment**: Rent out equipment during off-peak seasons
4. **Tool Sharing**: Make company tools available to partners/contractors

**Chart of Account Code Reference** (Norwegian NS 4102):
- **1202** - Maskiner og anlegg (Machinery and equipment)
  - Construction equipment, industrial machinery
- **1203** - Inventar (Furniture and fixtures)
  - Office furniture, fixtures, tools
- **1204** - Transportmidler (Transport equipment)
  - Vehicles, trailers, transport tools

**Implementation Notes**:
- Validates listing type (Sale vs Rental)
- Conditional field display in UI
- Filters assets by account codes
- Tracks rental status separately
- Integration with ERPNext Asset module
- Supports multiple rental platforms

---

## Tool 4: Receipt Scanner 📸🧾

**Purpose**: Automatically scan receipt images and add items to ERPNext

**MCP Tool**: `scan_receipt_and_add_items()`

**API Endpoint**: `erpnext_assist.api.scan_receipt`

**Features**:
- OCR-powered text extraction from receipt images
- Automatic item, quantity, and price detection
- Add items as stock or assets
- Support for multiple items per receipt
- Warehouse and cost center assignment

**Parameters**:
- `receipt_image` (str): Base64 encoded receipt image
- `add_as` (str): "stock" or "asset"
- `warehouse` (str, optional): Target warehouse for stock items
- `cost_center` (str, optional): Cost center for assets

**Usage Example**:
```python
# From UI or API
frappe.call({
    method: "erpnext_assist.api.scan_receipt",
    args: {
        receipt_image: base64_image,
        add_as: "stock",
        warehouse: "Main Warehouse"
    }
})
```

**Implementation Notes**:
- Requires `pytesseract` library (optional dependency)
- Supports various receipt formats
- Automatically creates items and stock entries
- Logs all additions for audit trail

---

## Tool 5: Price Comparison with Prisjakt.no 💰

**Purpose**: Compare vendor prices across internal ERPNext suppliers and Prisjakt.no

**MCP Tool**: `compare_vendor_prices()`

**API Endpoint**: `erpnext_assist.api.compare_prices`

**Features**:
- Search internal ERPNext vendor catalog
- Integration with Prisjakt.no for market price comparison
- Pull complete vendor catalogs
- Suggest cheapest supplier
- Display price history and trends

**Parameters**:
- `item_name` (str): Item name or description to search
- `search_prisjakt` (bool): Whether to search Prisjakt.no (default: True)

**Returns**:
```json
{
    "success": true,
    "results": {
        "item_name": "Pliers",
        "internal_vendors": [
            {
                "supplier_name": "Supplier A",
                "item_code": "PLIERS-001",
                "last_purchase_rate": 150.00
            }
        ],
        "prisjakt_results": [],
        "recommendations": [
            {
                "type": "cheapest_internal",
                "supplier": "Supplier A",
                "price": 150.00
            }
        ]
    }
}
```

**Usage Example**:
```python
# Ask AI: "Find the cheapest pliers"
result = compare_vendor_prices(item_name="pliers")

# Or from UI
frappe.call({
    method: "erpnext_assist.api.compare_prices",
    args: {
        item_name: "pliers",
        search_prisjakt: true
    }
})
```

**Implementation Notes**:
- Prisjakt.no integration requires API setup or web scraping
- Caches results for performance
- Updates vendor catalogs automatically
- Supports price alerts and monitoring

---

## Tool 6: Natural Language Voice Queries 🗣️

**Purpose**: Ask inventory questions in plain language, with voice support

**MCP Tool**: `query_inventory_natural_language()`

**API Endpoint**: `erpnext_assist.api.ask_inventory`

**Features**:
- Natural language understanding
- Voice-to-text compatible
- Instant inventory answers
- Location and availability information
- Multi-item queries

**Supported Query Types**:
- Availability: "do we have pliers?"
- Location: "where is the hammer?"
- Quantity: "how many screws do we have?"
- General: "show me all tools in main warehouse"

**Parameters**:
- `query` (str): Natural language question

**Returns**:
```json
{
    "success": true,
    "query": "do we have pliers?",
    "response": "Yes, we have 15 units of Professional Pliers in Main Warehouse.",
    "items_found": [
        {
            "item_code": "PLIERS-001",
            "item_name": "Professional Pliers",
            "total_qty": 15,
            "warehouses": "Main Warehouse"
        }
    ]
}
```

**Usage Examples**:
```python
# Voice command: "Do we have pliers?"
result = query_inventory_natural_language("do we have pliers?")

# From UI with voice input
frappe.call({
    method: "erpnext_assist.api.ask_inventory",
    args: {
        query: voice_to_text_result
    }
})
```

**Voice Integration**:
Works seamlessly with:
- Web Speech API (browser)
- Google Speech-to-Text
- Azure Speech Services
- Local speech recognition (offline)

**Implementation Notes**:
- Parses natural language with keyword extraction
- Can be enhanced with NLP libraries (spaCy, NLTK)
- Supports multiple languages (with translation)
- Logs queries for continuous improvement

---

## Tool 1 Enhancement: Pickup Route Orchestration 🚗📍

**Purpose**: Optimize pickup routes for marketplace listings by contacting sellers

**MCP Tool**: `orchestrate_pickup_route()`

**API Endpoint**: `erpnext_assist.api.plan_pickup_route`

**Features**:
- Contact multiple sellers to schedule pickups
- Optimize route for minimum travel time
- Schedule all pickups for a single efficient day
- Map visualization of route
- Estimated time and distance

**Parameters**:
- `listings` (list): Array of Marketplace Listing IDs
- `start_location` (str, optional): Starting address
- `preferred_date` (str, optional): Preferred pickup date (YYYY-MM-DD)

**Returns**:
```json
{
    "success": true,
    "route_plan": {
        "date": "2026-01-10",
        "start_location": "Main Office",
        "listings": [
            {
                "listing_id": "ML-00001",
                "item": "CHAIR-001",
                "status": "scheduled",
                "seller_contacted": true,
                "pickup_time": "10:00"
            }
        ],
        "optimal_route": [...],
        "total_distance": 15.5,
        "estimated_time": 90
    }
}
```

**Usage Example**:
```python
# Plan route for multiple listings
result = orchestrate_pickup_route(
    listings=["ML-00001", "ML-00002", "ML-00003"],
    start_location="Main Office",
    preferred_date="2026-01-10"
)

# From UI
frappe.call({
    method: "erpnext_assist.api.plan_pickup_route",
    args: {
        listings: JSON.stringify(["ML-00001", "ML-00002"]),
        preferred_date: "2026-01-10"
    }
})
```

**Use Cases**:
1. **Bulk Marketplace Pickups**: When multiple items are sold on Facebook/FINN.no
2. **Efficient Collection Days**: Schedule all pickups for one efficient run
3. **Cost Optimization**: Minimize fuel and time costs
4. **Seller Coordination**: Automatic scheduling with seller availability

**Implementation Notes**:
- Can integrate with Google Maps API for route optimization
- Supports manual route adjustment
- Sends notifications to sellers
- Tracks pickup status and completion

---

## Integration with Visual Tool Builder

All these tools can also be created and customized using the Visual Tool Builder:

### Example: Custom Receipt Scanner Tool

```
Tool Name: "Quick Receipt Add"
Description: "Scan receipt and add items to warehouse"
Prompt: "Scan {{receipt_image}} and add items to {{warehouse}}"
Action Type: Custom Code
Code: 
    from erpnext_assist.mcp_server.server import scan_receipt_and_add_items
    result = scan_receipt_and_add_items(
        receipt_image=context['receipt_image'],
        add_as='stock',
        warehouse=context['warehouse']
    )
```

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `erpnext_assist.api.scan_receipt` | POST | Scan receipt and add items |
| `erpnext_assist.api.compare_prices` | POST | Compare vendor prices |
| `erpnext_assist.api.ask_inventory` | POST | Natural language queries |
| `erpnext_assist.api.plan_pickup_route` | POST | Optimize pickup routes |
| `erpnext_assist.api.get_rental_assets` | POST | Get rental-eligible assets |
| `erpnext_assist.api.post_rental_listing` | POST | Post asset to rental service |

## Requirements

### Required (Already Included)
- frappe
- mcp[cli]>=1.0.0
- requests
- rembg>=2.0.0
- pillow>=10.0.0

### Optional (For Extended Features)
- `pytesseract>=0.3.10` - For receipt OCR scanning
- `tesseract-ocr` - System package for OCR
- Google Maps API key - For route optimization
- Prisjakt.no API access - For price comparison

## Installation

These tools are automatically available after installing ERPNext Assist:

```bash
# Standard installation
bench --site [site] install-app erpnext_assist

# For OCR support (optional)
sudo apt-get install tesseract-ocr  # Linux
brew install tesseract              # macOS
pip install pytesseract
```

## Documentation

See the updated documentation:
- `EXAMPLES.md` - Examples 8-11 cover these new tools (including Road Project Tracking)
- `README.md` - Updated with tool descriptions
- `QUICKSTART.md` - Integration examples

## Tool 8: Vegvesen Road Project Tracking & Strategic Forecasting 🛣️📍

**Purpose**: Track road construction projects from Norwegian Public Roads Administration (Statens vegvesen), plot on maps, and forecast high-value locations

**MCP Tools**: 
- `track_vegvesen_road_projects()` - Fetch and sync projects from NVDB API
- `plot_road_projects_on_map()` - Visualize projects on interactive maps
- `forecast_location_value()` - Predict location value based on road infrastructure

**API Endpoints**: 
- `erpnext_assist.api.fetch_vegvesen_road_projects` - Fetch projects
- `erpnext_assist.api.get_road_projects_map` - Get map data
- `erpnext_assist.api.analyze_road_project_impact` - Analyze project impact

**DocType Created**:
- `Road Project` - Stores comprehensive road project information

**Features**:
- Integration with Vegvesen NVDB API
- Automatic strategic value calculation
- Map plotting with GeoJSON support
- Impact analysis on nearby warehouses and assets
- Location value forecasting for strategic planning
- Filter by county, project type, and strategic value
- Track estimated costs and timelines
- Identify high-value areas before competition

**Road Project Fields**:
- Project identification (ID, name, description)
- Location data (county, municipality, coordinates, geometry)
- Project details (dates, cost, type, phase, priority)
- Strategic analysis (value, impact forecast, nearby locations)
- Metadata (NVDB URL, sync timestamp, data source)

**Parameters for `track_vegvesen_road_projects()`**:
- `county` (str, optional): County code filter (e.g., '9745')
- `sync_to_erpnext` (bool): Create/update Road Project records
- `update_existing` (bool): Update existing projects with new data

**Parameters for `forecast_location_value()`**:
- `latitude` (float): Location latitude
- `longitude` (float): Location longitude
- `search_radius_km` (float): Search radius for nearby projects

**Use Cases**:
1. **Warehouse Site Selection**: Identify optimal locations near future road infrastructure
2. **Property Investment**: Forecast value appreciation due to new roads
3. **Logistics Planning**: Plan routes based on upcoming road improvements
4. **Strategic Planning**: Make data-driven expansion decisions
5. **Competitive Advantage**: Secure high-value locations before market awareness

**Value Calculation**:
The tool automatically calculates strategic value based on:
- Project priority (Critical, High, Medium, Low)
- Project type (New Road, Expansion, Bridge, Tunnel)
- Estimated cost (scale indicator)
- Proximity to existing assets
- Infrastructure investment volume

**Integration with ERPNext**:
- Links to Warehouse locations
- Analyzes impact on existing assets
- Tracks project updates via NVDB sync
- Supports GeoJSON for map visualization
- Provides strategic recommendations

## Future Enhancements

Potential improvements for these tools:
1. **Receipt Scanner**: Multi-language OCR, AI-powered item matching
2. **Price Comparison**: Historical price tracking, price alerts
3. **Voice Queries**: Multi-language support, context awareness
4. **Pickup Routes**: Real-time traffic integration, driver app
5. **Road Projects**: Real-time NVDB API integration, automatic alerts on project updates

## Feedback

These tools were implemented based on user feedback. More suggestions welcome!
