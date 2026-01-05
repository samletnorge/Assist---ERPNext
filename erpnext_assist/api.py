"""
API endpoints for ERPNext Assist Tools

Provides whitelisted methods that can be called from the UI or external clients.
"""

import frappe
import json
from typing import Dict, Any


@frappe.whitelist()
def remove_image_background(image_data: str, enhance: bool = True) -> Dict[str, Any]:
    """
    Remove background from an image.
    
    Args:
        image_data: Base64 encoded image data
        enhance: Whether to also enhance the image
    
    Returns:
        Dictionary with processed image data
    """
    try:
        from erpnext_assist.utils.image_processing import process_camera_image
        
        if isinstance(enhance, str):
            enhance = enhance.lower() == "true"
        
        processed_image = process_camera_image(
            image_data,
            remove_bg=True,
            enhance=enhance,
            return_base64=True
        )
        
        return {
            "success": True,
            "processed_image": processed_image,
            "message": "Background removed successfully"
        }
    except Exception as e:
        frappe.log_error(f"Background removal error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to remove background"
        }


@frappe.whitelist()
def enhance_image(image_data: str, brightness: float = 1.1, contrast: float = 1.1, sharpness: float = 1.2) -> Dict[str, Any]:
    """
    Enhance image quality.
    
    Args:
        image_data: Base64 encoded image data
        brightness: Brightness factor (default 1.1)
        contrast: Contrast factor (default 1.1)
        sharpness: Sharpness factor (default 1.2)
    
    Returns:
        Dictionary with enhanced image data
    """
    try:
        from erpnext_assist.utils.image_processing import enhance_image as enhance_img
        
        # Convert string parameters to float
        brightness = float(brightness)
        contrast = float(contrast)
        sharpness = float(sharpness)
        
        enhanced_image = enhance_img(
            image_data,
            enhance_brightness=brightness,
            enhance_contrast=contrast,
            enhance_sharpness=sharpness,
            return_base64=True
        )
        
        return {
            "success": True,
            "enhanced_image": enhanced_image,
            "message": "Image enhanced successfully"
        }
    except Exception as e:
        frappe.log_error(f"Image enhancement error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to enhance image"
        }


@frappe.whitelist()
def quick_add_item(
    image_data: str,
    warehouse: str,
    item_group: str = None,
    valuation_rate: float = None,
    remove_background: bool = True,
    enhance_image_quality: bool = True
) -> Dict[str, Any]:
    """
    Quick add item with camera image and automatic background removal.
    
    Args:
        image_data: Base64 encoded image data
        warehouse: Target warehouse
        item_group: Optional item group
        valuation_rate: Optional valuation rate
        remove_background: Whether to remove background
        enhance_image_quality: Whether to enhance image
    
    Returns:
        Dictionary with item creation result
    """
    try:
        from erpnext_assist.mcp_server.server import quick_add_item_from_camera
        
        # Convert string booleans
        if isinstance(remove_background, str):
            remove_background = remove_background.lower() == "true"
        if isinstance(enhance_image_quality, str):
            enhance_image_quality = enhance_image_quality.lower() == "true"
        if valuation_rate:
            valuation_rate = float(valuation_rate)
        
        result = quick_add_item_from_camera(
            image_data=image_data,
            warehouse=warehouse,
            item_group=item_group,
            valuation_rate=valuation_rate,
            remove_background=remove_background,
            enhance_image=enhance_image_quality
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Quick add item error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add item"
        }


@frappe.whitelist()
def scan_receipt(
    receipt_image: str,
    add_as: str = "stock",
    warehouse: str = None,
    cost_center: str = None
) -> Dict[str, Any]:
    """
    Scan a receipt and add items automatically.
    
    Args:
        receipt_image: Base64 encoded receipt image
        add_as: Type to add items as ('stock' or 'asset')
        warehouse: Target warehouse for stock items
        cost_center: Cost center for asset items
    
    Returns:
        Dictionary with scan results
    """
    try:
        from erpnext_assist.mcp_server.server import scan_receipt_and_add_items
        
        result = scan_receipt_and_add_items(
            receipt_image=receipt_image,
            add_as=add_as,
            warehouse=warehouse,
            cost_center=cost_center
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Receipt scan error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to scan receipt"
        }


@frappe.whitelist()
def compare_prices(
    item_name: str,
    search_prisjakt: bool = True
) -> Dict[str, Any]:
    """
    Compare vendor prices for an item.
    
    Args:
        item_name: Name of item to search
        search_prisjakt: Whether to search Prisjakt.no
    
    Returns:
        Dictionary with price comparisons
    """
    try:
        from erpnext_assist.mcp_server.server import compare_vendor_prices
        
        if isinstance(search_prisjakt, str):
            search_prisjakt = search_prisjakt.lower() == "true"
        
        result = compare_vendor_prices(
            item_name=item_name,
            search_prisjakt=search_prisjakt
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Price comparison error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to compare prices"
        }


@frappe.whitelist()
def ask_inventory(query: str) -> Dict[str, Any]:
    """
    Ask a natural language question about inventory.
    
    Args:
        query: Natural language question
    
    Returns:
        Dictionary with answer
    """
    try:
        from erpnext_assist.mcp_server.server import query_inventory_natural_language
        
        result = query_inventory_natural_language(query=query)
        
        return result
    except Exception as e:
        frappe.log_error(f"Inventory query error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to process query"
        }


@frappe.whitelist()
def plan_pickup_route(
    listings: str,
    start_location: str = None,
    preferred_date: str = None
) -> Dict[str, Any]:
    """
    Plan an optimized pickup route for marketplace listings.
    
    Args:
        listings: JSON string of listing IDs
        start_location: Starting location
        preferred_date: Preferred pickup date
    
    Returns:
        Dictionary with route plan
    """
    try:
        from erpnext_assist.mcp_server.server import orchestrate_pickup_route
        import json
        
        listing_ids = json.loads(listings) if isinstance(listings, str) else listings
        
        result = orchestrate_pickup_route(
            listings=listing_ids,
            start_location=start_location,
            preferred_date=preferred_date
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Pickup route error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to plan pickup route"
        }
