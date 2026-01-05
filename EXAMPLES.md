# Example Custom Tools for ERPNext Assist

This document provides real-world examples of custom tools you can create without programming, using the Visual Tool Drafting interface.

## Example 1: Bulk Inventory Adjustment

**Tool Name**: `bulk_inventory_adjust`

**Description**: Quickly adjust inventory levels for multiple items at once

**Category**: Inventory

**AI Provider**: Any

**Prompt Template**:
```
Adjust inventory for the following items in {{warehouse}}:
{{item_list}}
Each item should be adjusted to {{adjustment_type}} by the specified quantity.
Create appropriate stock entries with reason: {{reason}}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| item_list | Long Text | ✓ | JSON array of items: [{"item_code": "X", "qty": 10}] |
| warehouse | Link | ✓ | Target warehouse |
| adjustment_type | Select | ✓ | increase/decrease |
| reason | Text | ✓ | Reason for adjustment |

**Action Type**: Custom Code

**Custom Code**:
```python
import json
items = json.loads(context.get('item_list', '[]'))
warehouse = context['warehouse']
adj_type = context['adjustment_type']
reason = context['reason']

for item_data in items:
    stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Material Receipt" if adj_type == "increase" else "Material Issue",
        "to_warehouse" if adj_type == "increase" else "from_warehouse": warehouse,
        "items": [{
            "item_code": item_data['item_code'],
            "qty": item_data['qty']
        }]
    })
    stock_entry.insert()
    stock_entry.submit()

result = f"Adjusted {len(items)} items in {warehouse}"
```

---

## Example 2: Smart Reorder Point Checker

**Tool Name**: `check_reorder_points`

**Description**: Analyze stock levels and suggest reorder for items below threshold

**Category**: Inventory

**AI Provider**: Any

**Prompt Template**:
```
Check all items in {{warehouse}} and identify items with stock below {{threshold}}.
For each item below threshold, suggest a reorder quantity based on average consumption.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| warehouse | Link | ✓ | Warehouse to check |
| threshold | Number | ✓ | Minimum stock level |

**Action Type**: Custom Code

**Custom Code**:
```python
warehouse = context['warehouse']
threshold = context['threshold']

items_below = frappe.db.sql("""
    SELECT item_code, actual_qty, item_name
    FROM `tabBin`
    WHERE warehouse = %s
    AND actual_qty < %s
    ORDER BY actual_qty ASC
""", (warehouse, threshold), as_dict=True)

result = {
    "items_below_threshold": len(items_below),
    "items": items_below,
    "message": f"Found {len(items_below)} items below threshold in {warehouse}"
}
```

---

## Example 3: Customer Follow-up Creator

**Tool Name**: `create_customer_followup`

**Description**: Automatically create follow-up tasks for customers after orders

**Category**: Sales

**AI Provider**: Any

**Prompt Template**:
```
Create a follow-up task for customer {{customer}} regarding {{subject}}.
Schedule it for {{days}} days from now.
Assign to {{assigned_to}}.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| customer | Link | ✓ | Customer name |
| subject | Text | ✓ | Follow-up subject |
| days | Number | ✓ | Days until follow-up |
| assigned_to | Link | ✓ | User to assign task |

**Action Type**: Create Document

**Target DocType**: Task

---

## Example 4: Supplier Performance Report

**Tool Name**: `supplier_performance`

**Description**: Generate quick performance report for a supplier

**Category**: Purchasing

**AI Provider**: Any

**Prompt Template**:
```
Generate performance report for supplier {{supplier}} covering the last {{months}} months.
Include: total orders, on-time delivery rate, quality issues.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| supplier | Link | ✓ | Supplier name |
| months | Number | ✓ | Number of months to analyze |

**Action Type**: Custom Code

**Custom Code**:
```python
from datetime import datetime, timedelta

supplier = context['supplier']
months = int(context['months'])
start_date = (datetime.now() - timedelta(days=30*months)).strftime('%Y-%m-%d')

# Get purchase orders
orders = frappe.get_all(
    "Purchase Order",
    filters={
        "supplier": supplier,
        "transaction_date": [">=", start_date]
    },
    fields=["name", "status", "grand_total", "schedule_date"]
)

total_orders = len(orders)
completed_orders = len([o for o in orders if o.status == "Completed"])
total_value = sum([o.grand_total for o in orders])

result = {
    "supplier": supplier,
    "period": f"Last {months} months",
    "total_orders": total_orders,
    "completed_orders": completed_orders,
    "completion_rate": f"{(completed_orders/total_orders*100):.1f}%" if total_orders > 0 else "N/A",
    "total_value": total_value,
    "message": f"Performance report generated for {supplier}"
}
```

---

## Example 5: Quick Quote Generator

**Tool Name**: `quick_quote`

**Description**: Generate a quotation for a customer with common items

**Category**: Sales

**AI Provider**: Any

**Prompt Template**:
```
Create a quotation for {{customer}} with the following items:
{{items}}
Valid for {{validity_days}} days.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| customer | Link | ✓ | Customer name |
| items | Long Text | ✓ | JSON: [{"item": "X", "qty": 1, "rate": 100}] |
| validity_days | Number |  | Quote validity (default: 30) |

**Action Type**: Custom Code

**Custom Code**:
```python
import json
from datetime import datetime, timedelta

customer = context['customer']
items_data = json.loads(context.get('items', '[]'))
validity = int(context.get('validity_days', 30))

quotation = frappe.get_doc({
    "doctype": "Quotation",
    "customer": customer,
    "valid_till": (datetime.now() + timedelta(days=validity)).strftime('%Y-%m-%d'),
    "items": [
        {
            "item_code": item['item'],
            "qty": item['qty'],
            "rate": item['rate']
        }
        for item in items_data
    ]
})

quotation.insert()

result = {
    "success": True,
    "quotation_id": quotation.name,
    "customer": customer,
    "total": quotation.grand_total,
    "message": f"Quotation {quotation.name} created for {customer}"
}
```

---

## Example 6: Warehouse Transfer Assistant

**Tool Name**: `warehouse_transfer`

**Description**: Transfer items between warehouses

**Category**: Warehouse

**AI Provider**: Any

**Prompt Template**:
```
Transfer {{item_code}} from {{source_warehouse}} to {{target_warehouse}}.
Quantity: {{quantity}}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| item_code | Link | ✓ | Item to transfer |
| source_warehouse | Link | ✓ | Source warehouse |
| target_warehouse | Link | ✓ | Destination warehouse |
| quantity | Number | ✓ | Quantity to transfer |

**Action Type**: Create Document

**Target DocType**: Stock Entry

*(Note: You'll need to configure the mapping in the tool settings)*

---

## Example 7: Expense Approval Reminder

**Tool Name**: `expense_reminder`

**Description**: Send reminders for pending expense approvals

**Category**: Custom

**AI Provider**: Any

**Prompt Template**:
```
Find all expense claims pending approval for more than {{days}} days.
Send reminder notification to approvers.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| days | Number | ✓ | Days pending threshold |

**Action Type**: Custom Code

**Custom Code**:
```python
from datetime import datetime, timedelta

days = int(context['days'])
cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

pending_expenses = frappe.get_all(
    "Expense Claim",
    filters={
        "status": "Draft",
        "posting_date": ["<=", cutoff_date]
    },
    fields=["name", "employee", "total_claimed_amount", "expense_approver"]
)

for expense in pending_expenses:
    if expense.expense_approver:
        # Create notification
        notification = frappe.get_doc({
            "doctype": "Notification Log",
            "for_user": expense.expense_approver,
            "type": "Alert",
            "document_type": "Expense Claim",
            "document_name": expense.name,
            "subject": f"Pending Expense Approval: {expense.name}",
        })
        notification.insert()

result = {
    "reminders_sent": len(pending_expenses),
    "message": f"Sent {len(pending_expenses)} reminders for expenses pending > {days} days"
}
```

---

## Tips for Creating Your Own Tools

### 1. Start Simple
- Begin with single-action tools
- Test thoroughly before adding complexity
- Use existing DocTypes when possible

### 2. Use Clear Parameter Names
- Avoid abbreviations
- Use descriptive names: `customer_name` not `cust`
- Add helpful descriptions

### 3. Write Good Prompts
- Be specific about what the AI should do
- Include all {{parameters}} the tool uses
- Describe expected output

### 4. Test with Sample Data
- Create test records first
- Verify tool behavior
- Check for edge cases

### 5. Handle Errors Gracefully
- Use try/except in custom code
- Provide clear error messages
- Log errors for debugging

### 6. Document Your Tools
- Add clear descriptions
- Note any prerequisites
- Explain what the tool does

## Security Best Practices

⚠️ **Important**: Custom code runs with full permissions!

- **Validate inputs**: Always check parameter values
- **Use permissions**: Check user permissions before actions
- **Sanitize data**: Clean user input to prevent injection
- **Limit scope**: Keep tools focused and minimal
- **Audit regularly**: Review custom tools periodically
- **Test thoroughly**: Test in a dev environment first

---

## Example 8: Receipt Scanner (Auto Stock/Asset Addition)

**Tool Name**: `receipt_scanner`

**Description**: Scan receipt images and automatically add items as stock or assets

**Category**: Inventory

**AI Provider**: Any

**Prompt Template**:
```
Scan the receipt image and extract all items with quantities and prices.
Add them to {{warehouse}} as {{add_as}}.
OCR the receipt and create appropriate stock entries.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| receipt_image | Attach Image | ✓ | Receipt image to scan |
| add_as | Select | ✓ | stock/asset |
| warehouse | Link | ✓ | Target warehouse (for stock) |
| cost_center | Link |  | Cost center (for assets) |

**Action Type**: Custom Code

**Custom Code**:
```python
# This uses the built-in MCP tool
from erpnext_assist.mcp_server.server import scan_receipt_and_add_items

result = scan_receipt_and_add_items(
    receipt_image=context['receipt_image'],
    add_as=context['add_as'],
    warehouse=context.get('warehouse'),
    cost_center=context.get('cost_center')
)

# Note: Requires OCR library (pytesseract) setup
```

---

## Example 9: Price Comparison (Prisjakt.no Integration)

**Tool Name**: `vendor_price_comparison`

**Description**: Compare vendor prices using Prisjakt.no and internal catalog

**Category**: Purchasing

**AI Provider**: Any

**Prompt Template**:
```
Search for {{item_name}} across all vendors.
Check Prisjakt.no for market prices and compare with internal suppliers.
Suggest the cheapest option and pull complete vendor catalog if available.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| item_name | Text | ✓ | Item to search for |
| search_prisjakt | Checkbox | ✓ | Search Prisjakt.no |

**Action Type**: Custom Code

**Custom Code**:
```python
# Use the built-in MCP tool
from erpnext_assist.mcp_server.server import compare_vendor_prices

result = compare_vendor_prices(
    item_name=context['item_name'],
    search_prisjakt=context.get('search_prisjakt', True)
)

# Returns vendor comparisons and recommendations
```

---

## Example 10: Natural Language Inventory Query (Voice Support)

**Tool Name**: `voice_inventory_query`

**Description**: Ask inventory questions in natural language - "do we have pliers?"

**Category**: Inventory

**AI Provider**: Any (works great with voice-to-text)

**Prompt Template**:
```
Answer the question: {{query}}
Search inventory and respond in natural language about availability and location.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | Long Text | ✓ | Natural language question |

**Action Type**: Custom Code

**Custom Code**:
```python
# Use the built-in MCP tool
from erpnext_assist.mcp_server.server import query_inventory_natural_language

result = query_inventory_natural_language(
    query=context['query']
)

# Returns natural language response with item details
```

**Example Queries**:
- "Do we have pliers?"
- "Where is the hammer?"
- "How many screws do we have?"
- "Show me all tools in the main warehouse"

---

## Example 11: Pickup Route Orchestration

**Tool Name**: `optimize_pickup_route`

**Description**: Schedule and optimize pickup routes for marketplace items

**Category**: Marketplace

**AI Provider**: Any

**Prompt Template**:
```
Orchestrate pickup for these listings: {{listings}}
Contact sellers to schedule pickups on {{preferred_date}}.
Optimize the route starting from {{start_location}}.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| listings | Long Text | ✓ | JSON array of listing IDs |
| start_location | Text |  | Starting address/location |
| preferred_date | Date | ✓ | Preferred pickup date |

**Action Type**: Custom Code

**Custom Code**:
```python
import json
from erpnext_assist.mcp_server.server import orchestrate_pickup_route

listing_ids = json.loads(context.get('listings', '[]'))

result = orchestrate_pickup_route(
    listings=listing_ids,
    start_location=context.get('start_location'),
    preferred_date=context.get('preferred_date')
)

# Returns optimized route plan with seller contact status
```

**Use Case**:
When you've posted multiple items on Facebook Marketplace or FINN.no and buyers want to pick them up, this tool:
1. Contacts all sellers to schedule pickup times
2. Optimizes the route to minimize travel
3. Creates an efficient pickup schedule for a single day

---

## Example 12: RDS 81346 Equipment Reference Designation

**Tool Name**: `rds_equipment_designator`

**Description**: Generate ISO/IEC 81346 compliant reference designations for equipment

**Category**: Inventory

**AI Provider**: Any

**Prompt Template**:
```
Generate RDS 81346 designation for {{equipment_name}}.
Function aspect: {{function_aspect}}
Product aspect: {{product_aspect}}
Location aspect: {{location_aspect}}
Parent system: {{parent_system}}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| equipment_name | Text | ✓ | Equipment name |
| function_aspect | Text |  | What it does (prefix =) |
| product_aspect | Text |  | What it is (prefix -) |
| location_aspect | Text |  | Where it is (prefix +) |
| parent_system | Text |  | Parent system reference |

**Action Type**: Custom Code

**Custom Code**:
```python
from erpnext_assist.mcp_server.server import generate_rds_81346_designation

result = generate_rds_81346_designation(
    equipment_name=context['equipment_name'],
    function_aspect=context.get('function_aspect'),
    product_aspect=context.get('product_aspect'),
    location_aspect=context.get('location_aspect'),
    parent_system=context.get('parent_system')
)

# Returns standardized RDS designation
# Example: "MAIN.=PUMP.=COOLING.-MOTOR.+ROOM1"
```

**Use Cases**:
- Industrial plant equipment documentation
- Building systems management
- Complex machinery tracking
- Multi-site facility management
- Compliance with ISO/IEC 81346 standards

**Example Designations**:
- Wind turbine: `=A1.-WQA1.+SITE1` (Function=A1, Product=WQA1, Location=SITE1)
- Cooling pump: `=COOL.-PUMP.+ROOM1`
- Motor controller: `MAIN.=DRIVE.-MC01.+PANEL2`

---

## Example 13: S1000D Issue 6 Technical Documentation

**Tool Name**: `s1000d_doc_generator`

**Description**: Create S1000D Issue 6 compliant data modules for technical publications

**Category**: Custom

**AI Provider**: Any

**Prompt Template**:
```
Create S1000D data module for {{item_code}}.
DMC: {{data_module_code}}
Title: {{title}}
Content type: {{content_type}}
Generate technical documentation following S1000D Issue 6 standards.
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| item_code | Link | ✓ | ERPNext item code |
| data_module_code | Text | ✓ | S1000D DMC identifier |
| title | Text | ✓ | Module title |
| content_type | Select | ✓ | procedural/descriptive/fault/crew |
| issue_number | Text |  | S1000D issue (default: 6) |

**Action Type**: Custom Code

**Custom Code**:
```python
from erpnext_assist.mcp_server.server import create_s1000d_data_module

result = create_s1000d_data_module(
    item_code=context['item_code'],
    data_module_code=context['data_module_code'],
    title=context['title'],
    content_type=context.get('content_type', 'procedural'),
    issue_number=context.get('issue_number', '6')
)

# Returns XML-based data module structure
# Compatible with Common Source Database (CSDB)
```

**Use Cases**:
- Aerospace technical manuals
- Defense equipment documentation
- Aircraft maintenance procedures
- Naval systems documentation
- Complex machinery service manuals

**S1000D Features**:
- **Modular Data**: Reusable documentation components
- **CSDB Integration**: Centralized source management
- **XML-based**: Digital publishing ready
- **Version Control**: Track documentation changes
- **International Standard**: NATO/DoD compliant

**Example Data Module Codes (DMC)**:
- `DMC-AIRCRAFT-A-00-00-00-00A-000A-A` - Aircraft system overview
- `DMC-ENGINE-A-72-10-00-00A-520A-A` - Engine maintenance procedure
- `DMC-AVIONICS-A-45-20-01-00A-040A-A` - Avionics troubleshooting

---

## Example 14: GitHub Repos as Assets Importer

**Tool Name**: `github_asset_importer`

**Description**: Import all GitHub repositories from a user or organization as assets

**Category**: Custom

**AI Provider**: Any

**Prompt Template**:
```
Import all GitHub repositories from {{username}} as assets.
Category: {{asset_category}}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| username | Text | * | GitHub username (or use organization) |
| organization | Text | * | GitHub organization name |
| github_token | Password | | Personal access token (for private repos) |
| import_as_assets | Check | | Create as assets (default: true) |
| asset_category | Text | | Asset category (default: Software) |

*One of username or organization is required

**Action Type**: Custom Code

**Custom Code**:
```python
from erpnext_assist.mcp_server.server import import_github_repos_as_assets

result = import_github_repos_as_assets(
    username=context.get('username'),
    organization=context.get('organization'),
    github_token=context.get('github_token'),
    import_as_assets=context.get('import_as_assets', True),
    asset_category=context.get('asset_category', 'Software')
)

# Returns imported repos with metadata
# Each repo becomes an asset with GitHub metadata
```

**Use Cases**:
- **Software Asset Management**: Track all company repositories as assets
- **Open Source Portfolio**: Import personal GitHub portfolio
- **Organization Audit**: Create asset records for all org repos
- **Project Tracking**: Monitor repository stars, forks, and languages
- **License Management**: Track software licenses across repos

**Features**:
- Automatically handles pagination (100+ repos)
- Captures metadata: stars, forks, language, description
- Creates both item and asset records
- Supports private repositories with token
- Skips existing assets to avoid duplicates

**Example Usage**:
```python
# Import personal repos
result = import_github_repos_as_assets(
    username="octocat",
    import_as_assets=True,
    asset_category="Software"
)

# Import organization repos (with private access)
result = import_github_repos_as_assets(
    organization="github",
    github_token="ghp_xxxxxxxxxxxx",
    import_as_assets=True,
    asset_category="Code Repository"
)
```

**Return Format**:
```json
{
    "success": true,
    "target": "octocat",
    "target_type": "user",
    "total_repos": 25,
    "imported_count": 23,
    "skipped_count": 2,
    "imported_assets": [
        {
            "repo_name": "Hello-World",
            "item_code": "REPO-HELLO-WORLD",
            "url": "https://github.com/octocat/Hello-World",
            "language": "Python",
            "stars": 1234
        }
    ],
    "skipped_repos": [
        {
            "name": "test-repo",
            "reason": "already exists"
        }
    ]
}
```

**Benefits**:
- **Asset Tracking**: All repos tracked in ERPNext asset management
- **Metadata Capture**: Stars, forks, language automatically captured
- **Bulk Import**: Import hundreds of repos in one operation
- **Private Repos**: Support for private repositories with token
- **Duplicate Prevention**: Automatically skips existing assets

---

## Need More Examples?

Check the community forum or create an issue on GitHub with your use case!
