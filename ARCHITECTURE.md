# ERPNext Assist - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACES                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  ERPNext Web UI  │  │  Mobile Camera   │  │  Barcode Scanner │      │
│  │   (Tool Builder) │  │   (Item Photos)  │  │   (Locations)    │      │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘      │
│           │                     │                      │                 │
└───────────┼─────────────────────┼──────────────────────┼─────────────────┘
            │                     │                      │
            ↓                     ↓                      ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        ERPNEXT ASSIST APP                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                     API LAYER (api.py)                          │    │
│  │  • remove_image_background()  • enhance_image()                │    │
│  │  • quick_add_item()          • Whitelisted endpoints           │    │
│  └────────────────┬───────────────────────────┬───────────────────┘    │
│                   │                           │                         │
│  ┌────────────────┴─────────┐   ┌────────────┴──────────────────┐     │
│  │   UTILS (Image AI)       │   │    DOCTYPES (Data Layer)       │     │
│  │ ┌──────────────────────┐ │   │ • Assist Tool Draft           │     │
│  │ │ Image Processing:    │ │   │ • Assist Tool Parameter       │     │
│  │ │ • remove_background()│ │   │ • Marketplace Listing         │     │
│  │ │ • enhance_image()    │ │   │ • Marketplace Listing Image   │     │
│  │ │ • process_camera()   │ │   │ • Saved Marketplace Search    │     │
│  │ └──────────────────────┘ │   │                                │     │
│  │   (rembg + U²-Net AI)    │   │   (Frappe ORM)                 │     │
│  └──────────────────────────┘   └────────────────────────────────┘     │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │               MCP SERVER (mcp_server/server.py)                 │    │
│  │                                                                  │    │
│  │  Built-in Tools:                Dynamic Tools:                  │    │
│  │  ├─ post_to_marketplace()      ├─ load_user_drafted_tools()    │    │
│  │  ├─ track_saved_search()       ├─ Dynamically registered       │    │
│  │  ├─ quick_add_item_*()         └─ From DB at runtime           │    │
│  │  ├─ scan_barcode_*()                                            │    │
│  │  └─ get_item_details()                                          │    │
│  │                                                                  │    │
│  │  Transport: stdio / HTTP                                        │    │
│  └────────────────┬───────────────────────────┬───────────────────┘    │
│                   │                           │                         │
└───────────────────┼───────────────────────────┼─────────────────────────┘
                    │                           │
                    ↓                           ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          AI CLIENTS (MCP)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │   Claude   │  │   OpenAI   │  │   Ollama   │  │   Custom   │       │
│  │  Desktop   │  │    API     │  │  (Offline) │  │     AI     │       │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW EXAMPLE:                                │
│                    Visual Tool Creation (No Code!)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1. User creates tool in ERPNext UI                                      │
│     ├─ Fills form: name, description, parameters                         │
│     ├─ Writes prompt template in natural language                        │
│     └─ Selects action type (Create/Update/API/Custom)                    │
│                                                                           │
│  2. Tool saved to database (Assist Tool Draft DocType)                   │
│                                                                           │
│  3. MCP Server loads tool dynamically                                    │
│     ├─ Reads from database at startup                                    │
│     ├─ Converts to MCP tool function                                     │
│     └─ Registers with MCP protocol                                       │
│                                                                           │
│  4. AI client discovers and uses tool                                    │
│     ├─ Sends parameters via MCP                                          │
│     ├─ Tool executes in ERPNext context                                  │
│     └─ Returns result to AI                                              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW EXAMPLE:                                │
│               Camera Item Addition with Background Removal               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1. User takes photo via mobile/desktop camera                           │
│     └─ Image captured as base64                                          │
│                                                                           │
│  2. API call: quick_add_item(image, warehouse, remove_bg=True)           │
│                                                                           │
│  3. Image Processing Pipeline                                            │
│     ├─ process_camera_image()                                            │
│     ├─ remove_background() → U²-Net AI model                             │
│     │   └─ Transparent background PNG                                    │
│     └─ enhance_image() → Brightness/Contrast/Sharpness                   │
│         └─ Professional quality image                                    │
│                                                                           │
│  4. Item Creation                                                        │
│     ├─ Generate unique item code                                         │
│     ├─ Create Item DocType with processed image                          │
│     ├─ Attach image file                                                 │
│     └─ Create Stock Entry for warehouse                                  │
│                                                                           │
│  5. Response returned                                                    │
│     └─ { item_code, warehouse, background_removed: true }                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      KEY TECHNOLOGY STACK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Framework:        Frappe / ERPNext                                      │
│  Language:         Python 3.10+                                          │
│  AI Protocol:      Model Context Protocol (MCP)                          │
│  AI Background:    rembg (U²-Net deep learning model)                    │
│  Image Processing: Pillow (PIL)                                          │
│  HTTP Client:      requests                                              │
│  Database:         MariaDB (via Frappe ORM)                              │
│  Transport:        stdio / HTTP                                          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT OPTIONS                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Development:                                                            │
│  └─ bench get-app & install-app                                          │
│                                                                           │
│  MCP Server:                                                             │
│  ├─ Local (stdio):    python -m erpnext_assist.mcp_server.server        │
│  ├─ HTTP:             MCP_TRANSPORT=http python -m ...                   │
│  └─ Systemd Service:  For production deployments                         │
│                                                                           │
│  AI Integration:                                                         │
│  ├─ Claude Desktop:   JSON config file                                   │
│  ├─ Cursor IDE:       Settings JSON                                      │
│  ├─ Ollama:          Local AI models (offline)                          │
│  └─ Custom:          Any MCP-compatible client                          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Component Interactions

### 1. Visual Tool Creation Flow
```
ERPNext UI → Assist Tool Draft → Database → MCP Server → AI Client
     ↓              ↓                ↓           ↓            ↓
   Forms      Validation        Storage     Loading     Discovery
```

### 2. Camera Item Flow
```
Camera → API → Image AI → Item Creation → Stock Entry
  ↓      ↓       ↓            ↓              ↓
Photo  Base64  Remove BG   Save Item   Update Inventory
               Enhance
```

### 3. Marketplace Posting Flow
```
Item → MCP Tool → Marketplace Listing → External API → Tracking
 ↓        ↓            ↓                    ↓              ↓
Data   Process    DocType Creation       Post Online    Monitor
```

### 4. Barcode Scanning Flow
```
Barcode → MCP Tool → Database Query → Stock Levels → Location Info
   ↓         ↓            ↓               ↓               ↓
  Scan    Lookup      Item Bin        Warehouses       Results
```

## Security Layers

```
┌─────────────────────────────────────────┐
│         User Authentication             │  Frappe Session
├─────────────────────────────────────────┤
│       Permission Checks                 │  DocType Permissions
├─────────────────────────────────────────┤
│       Input Validation                  │  Parameter Validation
├─────────────────────────────────────────┤
│       SQL Injection Protection          │  ORM Layer
├─────────────────────────────────────────┤
│       Local Processing                  │  No External APIs
└─────────────────────────────────────────┘
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Tool Creation (UI) | < 1s | Form submission |
| Tool Loading | 100ms | Per tool at startup |
| Background Removal | 2-5s | First image: model load |
| Image Enhancement | < 500ms | Fast PIL operations |
| Barcode Scan | < 100ms | Database lookup |
| MCP Tool Call | < 1s | Excluding DocType ops |

## Scalability

- **Concurrent Users**: Limited by ERPNext/Frappe
- **Tools**: Unlimited user-drafted tools
- **Images**: Processed locally, no API limits
- **MCP Clients**: Multiple simultaneous connections (HTTP mode)
- **Database**: Standard Frappe/MariaDB scaling

## Innovation Summary

1. **First no-code MCP tool builder** for ERPNext
2. **AI-powered image processing** integrated into ERP
3. **Privacy-focused** local AI processing
4. **Universal AI compatibility** via MCP standard
5. **Offline capability** for all core features
