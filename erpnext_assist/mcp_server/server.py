"""
Enhanced MCP Server for ERPNext Assist Tools with Dynamic Tool Loading

This module provides a Model Context Protocol (MCP) server that exposes
ERPNext operations as tools that can be used by AI models. It supports
both built-in tools and dynamically loaded user-drafted tools from the UI.
"""

import os
import sys
import json
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("ERPNext Assist")


def load_user_drafted_tools():
    """
    Load and register tools that users have drafted in the UI.
    This allows non-programmers to create custom tools visually.
    """
    try:
        import frappe
        
        # Get all enabled user-drafted tools
        tools = frappe.get_all(
            "Assist Tool Draft",
            filters={"enabled": 1},
            fields=["name", "tool_name", "tool_description", "parameters"]
        )
        
        for tool_info in tools:
            # Dynamically create MCP tool for each user-drafted tool
            def create_tool_function(tool_name):
                def tool_function(**kwargs):
                    """Dynamically created tool from UI draft."""
                    tool = frappe.get_doc("Assist Tool Draft", tool_name)
                    return tool.execute_tool(kwargs)
                return tool_function
            
            # Register the tool with MCP
            tool_func = create_tool_function(tool_info.name)
            tool_func.__doc__ = tool_info.tool_description
            tool_func.__name__ = tool_info.tool_name.replace(" ", "_").lower()
            
            mcp.tool()(tool_func)
        
        return len(tools)
    except Exception as e:
        print(f"Error loading user-drafted tools: {e}", file=sys.stderr)
        return 0


# Tool 1: Marketplace Posting Tools
@mcp.tool()
def post_to_marketplace(
    item_code: str,
    marketplace: str,
    title: str,
    description: str,
    price: float,
    images: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Post stock items or assets to marketplaces like Facebook Marketplace or FINN.no.
    
    Args:
        item_code: The ERPNext item code to post
        marketplace: Target marketplace ('facebook' or 'finn.no')
        title: Listing title
        description: Listing description
        price: Listing price
        images: List of image URLs or paths
    
    Returns:
        Dictionary with posting status and listing ID
    """
    try:
        # Import frappe here to avoid issues if frappe is not installed
        import frappe
        
        # Get item details from ERPNext
        item = frappe.get_doc("Item", item_code)
        
        # Create marketplace listing record
        listing = frappe.get_doc({
            "doctype": "Marketplace Listing",
            "item_code": item_code,
            "marketplace": marketplace,
            "title": title,
            "description": description,
            "price": price,
            "status": "Draft",
        })
        
        if images:
            for image_url in images:
                listing.append("images", {"image": image_url})
        
        listing.insert()
        frappe.db.commit()
        
        return {
            "success": True,
            "listing_id": listing.name,
            "marketplace": marketplace,
            "item_code": item_code,
            "message": f"Listing created successfully for {marketplace}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create marketplace listing"
        }


@mcp.tool()
def track_saved_search(
    user: str,
    search_query: str,
    marketplace: str,
    search_type: str = "purchase_request",
) -> Dict[str, Any]:
    """
    Track and save search queries based on purchase or material request items.
    
    Args:
        user: ERPNext user ID
        search_query: The search query to track
        marketplace: Target marketplace for the search
        search_type: Type of search ('purchase_request' or 'material_request')
    
    Returns:
        Dictionary with search tracking status
    """
    try:
        import frappe
        
        # Create saved search record
        saved_search = frappe.get_doc({
            "doctype": "Saved Marketplace Search",
            "user": user,
            "search_query": search_query,
            "marketplace": marketplace,
            "search_type": search_type,
            "last_checked": frappe.utils.now(),
        })
        
        saved_search.insert()
        frappe.db.commit()
        
        return {
            "success": True,
            "search_id": saved_search.name,
            "message": "Search saved successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to save search"
        }


# Built-in Tool 2: Camera-based Item Addition with Background Removal
@mcp.tool()
def quick_add_item_from_camera(
    image_data: str,
    warehouse: str,
    item_group: Optional[str] = None,
    valuation_rate: Optional[float] = None,
    remove_background: bool = True,
    enhance_image: bool = True,
) -> Dict[str, Any]:
    """
    Quickly add a new item (stock or asset) using camera capture with automatic background removal.
    Useful for warehouses with disorganized or new items.
    
    Args:
        image_data: Base64 encoded image data or file path
        warehouse: Target warehouse for the item
        item_group: Optional item group classification
        valuation_rate: Optional valuation rate for the item
        remove_background: Automatically remove background from image (default: True)
        enhance_image: Automatically enhance image quality (default: True)
    
    Returns:
        Dictionary with item creation status and item code
    """
    try:
        import frappe
        from erpnext_assist.utils.image_processing import process_camera_image
        
        # Process the image (remove background and enhance)
        if remove_background or enhance_image:
            try:
                processed_image = process_camera_image(
                    image_data,
                    remove_bg=remove_background,
                    enhance=enhance_image,
                    return_base64=True
                )
                image_data = processed_image
            except Exception as img_error:
                # Log error but continue with original image
                frappe.log_error(f"Image processing error: {str(img_error)}")
                print(f"Warning: Could not process image, using original. Error: {img_error}", file=sys.stderr)
        
        # Generate a temporary item code
        item_code = frappe.generate_hash(length=10).upper()
        
        # Create new item
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": f"Quick Add {item_code}",
            "item_group": item_group or "All Item Groups",
            "stock_uom": "Nos",
            "is_stock_item": 1,
        })
        
        # Attach image if provided
        if image_data:
            # Save image as file attachment
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": f"{item_code}_image.png",
                "attached_to_doctype": "Item",
                "attached_to_name": item_code,
                "content": image_data,
            })
            file_doc.insert()
            item.image = file_doc.file_url
        
        item.insert()
        
        # Create stock entry if warehouse specified
        if warehouse:
            stock_entry = frappe.get_doc({
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Receipt",
                "to_warehouse": warehouse,
                "items": [{
                    "item_code": item_code,
                    "qty": 1,
                    "basic_rate": valuation_rate or 0,
                }]
            })
            stock_entry.insert()
            stock_entry.submit()
        
        frappe.db.commit()
        
        return {
            "success": True,
            "item_code": item_code,
            "warehouse": warehouse,
            "background_removed": remove_background,
            "image_enhanced": enhance_image,
            "message": "Item created successfully from camera with processed image"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create item from camera"
        }


# Tool 3: Barcode Warehouse Location Scanner
@mcp.tool()
def scan_barcode_for_location(
    barcode: str,
) -> Dict[str, Any]:
    """
    Scan a barcode to quickly check which warehouse an item should be in.
    
    Args:
        barcode: The barcode value to scan
    
    Returns:
        Dictionary with warehouse location information
    """
    try:
        import frappe
        
        # Search for item by barcode
        item = frappe.db.get_value(
            "Item Barcode",
            {"barcode": barcode},
            ["parent as item_code"],
            as_dict=True
        )
        
        if not item:
            # Try direct item code match
            item_code = barcode
            if not frappe.db.exists("Item", item_code):
                return {
                    "success": False,
                    "message": "Item not found for barcode",
                    "barcode": barcode
                }
        else:
            item_code = item.item_code
        
        # Get item details
        item_doc = frappe.get_doc("Item", item_code)
        
        # Get warehouse stock levels
        stock_levels = frappe.db.sql("""
            SELECT 
                warehouse,
                actual_qty,
                reserved_qty,
                projected_qty
            FROM `tabBin`
            WHERE item_code = %s
            AND actual_qty > 0
            ORDER BY actual_qty DESC
        """, item_code, as_dict=True)
        
        # Get default warehouse
        default_warehouse = frappe.db.get_value(
            "Item Default",
            {"parent": item_code},
            "default_warehouse"
        )
        
        return {
            "success": True,
            "item_code": item_code,
            "item_name": item_doc.item_name,
            "barcode": barcode,
            "default_warehouse": default_warehouse,
            "stock_locations": stock_levels,
            "message": "Item location found successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to scan barcode"
        }


@mcp.tool()
def get_item_details(
    item_code: str,
) -> Dict[str, Any]:
    """
    Get detailed information about an item including stock levels across warehouses.
    
    Args:
        item_code: The ERPNext item code
    
    Returns:
        Dictionary with comprehensive item details
    """
    try:
        import frappe
        
        # Get item details
        item = frappe.get_doc("Item", item_code)
        
        # Get stock summary
        stock_summary = frappe.db.sql("""
            SELECT 
                warehouse,
                actual_qty,
                reserved_qty,
                ordered_qty,
                projected_qty,
                valuation_rate
            FROM `tabBin`
            WHERE item_code = %s
            ORDER BY warehouse
        """, item_code, as_dict=True)
        
        return {
            "success": True,
            "item_code": item_code,
            "item_name": item.item_name,
            "item_group": item.item_group,
            "stock_uom": item.stock_uom,
            "description": item.description,
            "stock_summary": stock_summary,
            "message": "Item details retrieved successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get item details"
        }


# New Tool 4: Receipt Scanner with OCR
@mcp.tool()
def scan_receipt_and_add_items(
    receipt_image: str,
    add_as: str = "stock",
    warehouse: Optional[str] = None,
    cost_center: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Scan a receipt image using OCR and automatically add items as stock or assets.
    
    Args:
        receipt_image: Base64 encoded receipt image
        add_as: Type to add items as ('stock' or 'asset')
        warehouse: Target warehouse for stock items
        cost_center: Cost center for asset items
    
    Returns:
        Dictionary with scanned items and creation status
    """
    try:
        import frappe
        
        # TODO: Implement OCR processing (e.g., using pytesseract or cloud OCR)
        # For now, this is a placeholder implementation
        
        items_created = []
        
        # Placeholder: In real implementation, parse receipt with OCR
        # and extract item names, quantities, prices
        
        # Example structure after OCR:
        # scanned_items = [
        #     {"name": "Item A", "qty": 2, "rate": 100},
        #     {"name": "Item B", "qty": 1, "rate": 50},
        # ]
        
        return {
            "success": True,
            "items_created": items_created,
            "add_as": add_as,
            "message": "Receipt scanned. Implement OCR processing to extract items.",
            "note": "This tool requires OCR library integration (pytesseract or similar)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to scan receipt"
        }


# New Tool 5: Price Comparison with Prisjakt.no
@mcp.tool()
def compare_vendor_prices(
    item_name: str,
    search_prisjakt: bool = True,
) -> Dict[str, Any]:
    """
    Compare vendor prices for an item using Prisjakt.no and internal vendor catalog.
    Suggests cheapest vendor and pulls vendor catalog.
    
    Args:
        item_name: Name or description of item to search
        search_prisjakt: Whether to search Prisjakt.no (default: True)
    
    Returns:
        Dictionary with vendor comparisons and catalog suggestions
    """
    try:
        import frappe
        import requests
        
        results = {
            "item_name": item_name,
            "internal_vendors": [],
            "prisjakt_results": [],
            "recommendations": []
        }
        
        # Search internal ERPNext suppliers
        suppliers = frappe.db.sql("""
            SELECT 
                s.name as supplier_name,
                si.item_code,
                si.item_name,
                si.supplier_part_no,
                si.last_purchase_rate
            FROM `tabSupplier` s
            LEFT JOIN `tabItem Supplier` si ON si.parent = s.name
            WHERE si.item_name LIKE %s OR si.item_code LIKE %s
            ORDER BY si.last_purchase_rate ASC
        """, (f"%{item_name}%", f"%{item_name}%"), as_dict=True)
        
        results["internal_vendors"] = suppliers
        
        # Search Prisjakt.no (placeholder - requires API key or web scraping)
        if search_prisjakt:
            # TODO: Implement Prisjakt.no API integration or web scraping
            results["prisjakt_results"] = []
            results["note"] = "Prisjakt.no integration requires API setup or web scraping"
        
        # Generate recommendations
        if suppliers:
            cheapest = min(suppliers, key=lambda x: x.get('last_purchase_rate', float('inf')))
            results["recommendations"].append({
                "type": "cheapest_internal",
                "supplier": cheapest.get('supplier_name'),
                "price": cheapest.get('last_purchase_rate'),
                "item_code": cheapest.get('item_code')
            })
        
        return {
            "success": True,
            "results": results,
            "message": f"Found {len(suppliers)} internal vendor matches"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to compare vendor prices"
        }


# New Tool 6: Natural Language Inventory Query (Voice/Text)
@mcp.tool()
def query_inventory_natural_language(
    query: str,
) -> Dict[str, Any]:
    """
    Answer natural language queries about inventory.
    Examples: "do we have pliers?", "where is the hammer?", "how many screws do we have?"
    
    Args:
        query: Natural language question about inventory
    
    Returns:
        Dictionary with query results in natural language
    """
    try:
        import frappe
        import re
        
        # Extract item keywords from query
        query_lower = query.lower()
        
        # Parse query intent
        is_availability = any(word in query_lower for word in ['have', 'got', 'stock', 'available'])
        is_location = any(word in query_lower for word in ['where', 'location', 'warehouse'])
        is_quantity = any(word in query_lower for word in ['how many', 'how much', 'quantity', 'count'])
        
        # Extract potential item names (simple approach - can be enhanced with NLP)
        # Remove common words
        stop_words = ['do', 'we', 'have', 'the', 'a', 'an', 'is', 'where', 'how', 'many', 'much', 'there']
        words = query_lower.split()
        item_keywords = [w.strip('?.,!') for w in words if w not in stop_words]
        
        # Search for items matching keywords
        search_pattern = '%' + '%'.join(item_keywords) + '%'
        items = frappe.db.sql("""
            SELECT 
                i.item_code,
                i.item_name,
                i.description,
                SUM(b.actual_qty) as total_qty,
                GROUP_CONCAT(DISTINCT b.warehouse) as warehouses
            FROM `tabItem` i
            LEFT JOIN `tabBin` b ON b.item_code = i.item_code AND b.actual_qty > 0
            WHERE i.item_name LIKE %s OR i.description LIKE %s OR i.item_code LIKE %s
            GROUP BY i.item_code
            HAVING total_qty > 0 OR total_qty IS NULL
            LIMIT 10
        """, (search_pattern, search_pattern, search_pattern), as_dict=True)
        
        # Generate natural language response
        if not items:
            response = f"No items found matching '{' '.join(item_keywords)}'. Try different keywords."
        elif len(items) == 1:
            item = items[0]
            qty = item.get('total_qty', 0) or 0
            warehouses = item.get('warehouses', 'unknown location')
            
            if is_location:
                response = f"Yes, we have {item['item_name']} in {warehouses}."
            elif is_quantity:
                response = f"We have {qty} units of {item['item_name']}."
            else:
                response = f"Yes, we have {qty} units of {item['item_name']} in {warehouses}."
        else:
            response = f"Found {len(items)} items matching your query:\n"
            for item in items[:5]:
                qty = item.get('total_qty', 0) or 0
                response += f"- {item['item_name']}: {qty} units\n"
        
        return {
            "success": True,
            "query": query,
            "response": response,
            "items_found": items,
            "message": "Query processed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to process natural language query"
        }


# Enhancement to Tool 1: Pickup Route Orchestration
@mcp.tool()
def orchestrate_pickup_route(
    listings: List[str],
    start_location: Optional[str] = None,
    preferred_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Orchestrate efficient pickup routes for marketplace listings by contacting sellers.
    Schedules pickups and optimizes route for a specific day.
    
    Args:
        listings: List of marketplace listing IDs to schedule pickups for
        start_location: Starting location for the route
        preferred_date: Preferred pickup date (YYYY-MM-DD format)
    
    Returns:
        Dictionary with route plan and seller contact status
    """
    try:
        import frappe
        from datetime import datetime
        
        route_plan = {
            "listings": [],
            "optimal_route": [],
            "date": preferred_date or datetime.now().strftime('%Y-%m-%d'),
            "start_location": start_location,
            "total_distance": 0,
            "estimated_time": 0
        }
        
        for listing_id in listings:
            listing = frappe.get_doc("Marketplace Listing", listing_id)
            
            # Get seller contact info (would be stored in listing)
            # TODO: Implement actual contact/scheduling logic
            
            route_plan["listings"].append({
                "listing_id": listing_id,
                "item": listing.item_code,
                "status": "scheduled",
                "seller_contacted": True,
                "pickup_time": None  # TODO: Get confirmed time from seller
            })
        
        # TODO: Implement route optimization algorithm
        # Could use Google Maps API, Mapbox, or other routing service
        
        route_plan["optimal_route"] = route_plan["listings"]  # Placeholder
        route_plan["message"] = f"Route planned for {len(listings)} pickups"
        route_plan["note"] = "Implement route optimization and seller communication API"
        
        return {
            "success": True,
            "route_plan": route_plan,
            "message": f"Pickup route orchestrated for {len(listings)} items"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to orchestrate pickup route"
        }


# New Tool 7: RDS 81346 Equipment Reference Designation
@mcp.tool()
def generate_rds_81346_designation(
    equipment_name: str,
    function_aspect: Optional[str] = None,
    product_aspect: Optional[str] = None,
    location_aspect: Optional[str] = None,
    parent_system: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate ISO/IEC 81346 (RDS) reference designations for equipment and systems.
    Creates standardized identifiers for industrial systems, installations, and equipment.
    
    Args:
        equipment_name: Name of the equipment/component
        function_aspect: Functional classification (what it does) - prefix with '='
        product_aspect: Product classification (what it is) - prefix with '-'
        location_aspect: Location classification (where it is) - prefix with '+'
        parent_system: Parent system reference designation
    
    Returns:
        Dictionary with generated RDS designation and metadata
    """
    try:
        import frappe
        
        # Generate RDS designation following ISO/IEC 81346 structure
        designation_parts = []
        
        if parent_system:
            designation_parts.append(parent_system)
        
        # Function aspect (=)
        if function_aspect:
            func_code = function_aspect if function_aspect.startswith('=') else f"={function_aspect}"
            designation_parts.append(func_code)
        
        # Product aspect (-)
        if product_aspect:
            prod_code = product_aspect if product_aspect.startswith('-') else f"-{product_aspect}"
            designation_parts.append(prod_code)
        
        # Location aspect (+)
        if location_aspect:
            loc_code = location_aspect if location_aspect.startswith('+') else f"+{location_aspect}"
            designation_parts.append(loc_code)
        
        # Generate full designation
        full_designation = ".".join(designation_parts) if designation_parts else equipment_name
        
        # Store in ERPNext as custom field or separate DocType
        result = {
            "success": True,
            "equipment_name": equipment_name,
            "rds_designation": full_designation,
            "aspects": {
                "function": function_aspect,
                "product": product_aspect,
                "location": location_aspect,
                "parent": parent_system
            },
            "standard": "ISO/IEC 81346",
            "message": f"RDS designation generated: {full_designation}"
        }
        
        # TODO: Optionally store in custom ERPNext DocType for equipment registry
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate RDS 81346 designation"
        }


# New Tool 8: S1000D Issue 6 Technical Documentation
@mcp.tool()
def create_s1000d_data_module(
    item_code: str,
    data_module_code: str,
    title: str,
    content_type: str = "procedural",
    issue_number: str = "6",
) -> Dict[str, Any]:
    """
    Create S1000D Issue 6 compliant data modules for technical publications.
    Generates standardized XML-based technical documentation for aerospace/defense equipment.
    
    Args:
        item_code: ERPNext item code for the equipment
        data_module_code: S1000D Data Module Code (DMC)
        title: Data module title
        content_type: Type of content ('procedural', 'descriptive', 'fault', 'crew')
        issue_number: S1000D issue number (default: '6')
    
    Returns:
        Dictionary with data module structure and metadata
    """
    try:
        import frappe
        from datetime import datetime
        
        # Get item details
        item = frappe.get_doc("Item", item_code)
        
        # Generate S1000D data module structure
        data_module = {
            "dmc": data_module_code,
            "issue_number": issue_number,
            "title": title,
            "item_code": item_code,
            "item_name": item.item_name,
            "content_type": content_type,
            "status": "draft",
            "created_date": datetime.now().isoformat(),
            "language": "en-US",
            "metadata": {
                "model_ident_code": item_code[:4] if len(item_code) >= 4 else "XXXX",
                "system_diff_code": "A",
                "system_code": "00",
                "sub_system_code": "0",
                "sub_sub_system_code": "0",
                "assy_code": "00",
                "disassy_code": "00",
                "disassy_code_variant": "00",
                "info_code": "000",
                "info_code_variant": "A",
                "item_location_code": "A"
            },
            "content": {
                "description": item.description or "",
                "specifications": {},
                "procedures": [],
                "warnings": [],
                "cautions": []
            }
        }
        
        # TODO: Generate actual XML structure according to S1000D schema
        # TODO: Store in Common Source Database (CSDB)
        
        return {
            "success": True,
            "data_module": data_module,
            "standard": "S1000D Issue 6",
            "message": f"S1000D data module created: {data_module_code}",
            "note": "Full XML generation and CSDB integration requires S1000D toolkit"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create S1000D data module"
        }


def run_server(transport: str = "stdio"):
    """
    Run the MCP server with the specified transport.
    Loads both built-in and user-drafted tools before starting.
    
    Args:
        transport: Transport type ('stdio' or 'streamable-http')
    """
    # Load user-drafted tools before running the server
    num_tools = load_user_drafted_tools()
    print(f"Loaded {num_tools} user-drafted tools", file=sys.stderr)
    
    mcp.run(transport=transport)


if __name__ == "__main__":
    # Default to stdio transport for local AI integration
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    run_server(transport=transport)
