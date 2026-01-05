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
