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

## Need More Examples?

Check the community forum or create an issue on GitHub with your use case!
