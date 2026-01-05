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
