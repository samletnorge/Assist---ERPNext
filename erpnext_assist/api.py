"""
API endpoints for ERPNext Assist Tools

Provides whitelisted methods that can be called from the UI or external clients.
"""

import frappe
import json
from typing import Dict, Any


@frappe.whitelist()
def remove_image_background(image_data: str, enhance: bool = True, use_altlokalt_api: bool = False) -> Dict[str, Any]:
    """
    Remove background from an image.
    
    Args:
        image_data: Base64 encoded image data
        enhance: Whether to also enhance the image
        use_altlokalt_api: If True, uses receipt-ocr.altlokalt.com API
    
    Returns:
        Dictionary with processed image data
    """
    try:
        from erpnext_assist.utils.image_processing import process_camera_image
        
        if isinstance(enhance, str):
            enhance = enhance.lower() == "true"
        if isinstance(use_altlokalt_api, str):
            use_altlokalt_api = use_altlokalt_api.lower() == "true"
        
        processed_image = process_camera_image(
            image_data,
            remove_bg=True,
            enhance=enhance,
            return_base64=True,
            use_altlokalt_api=use_altlokalt_api
        )
        
        return {
            "success": True,
            "processed_image": processed_image,
            "api_used": "altlokalt" if use_altlokalt_api else "rembg",
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


@frappe.whitelist()
def generate_rds_designation(
    equipment_name: str,
    function_aspect: str = None,
    product_aspect: str = None,
    location_aspect: str = None,
    parent_system: str = None
) -> Dict[str, Any]:
    """
    Generate RDS 81346 reference designation for equipment.
    
    Args:
        equipment_name: Name of equipment
        function_aspect: Functional classification
        product_aspect: Product classification
        location_aspect: Location classification
        parent_system: Parent system designation
    
    Returns:
        Dictionary with RDS designation
    """
    try:
        from erpnext_assist.mcp_server.server import generate_rds_81346_designation
        
        result = generate_rds_81346_designation(
            equipment_name=equipment_name,
            function_aspect=function_aspect,
            product_aspect=product_aspect,
            location_aspect=location_aspect,
            parent_system=parent_system
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"RDS designation error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate RDS designation"
        }


@frappe.whitelist()
def create_s1000d_module(
    item_code: str,
    data_module_code: str,
    title: str,
    content_type: str = "procedural",
    issue_number: str = "6"
) -> Dict[str, Any]:
    """
    Create S1000D Issue 6 data module for technical documentation.
    
    Args:
        item_code: ERPNext item code
        data_module_code: S1000D DMC
        title: Module title
        content_type: Content type
        issue_number: S1000D issue number
    
    Returns:
        Dictionary with data module structure
    """
    try:
        from erpnext_assist.mcp_server.server import create_s1000d_data_module
        
        result = create_s1000d_data_module(
            item_code=item_code,
            data_module_code=data_module_code,
            title=title,
            content_type=content_type,
            issue_number=issue_number
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"S1000D module error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create S1000D module"
        }


@frappe.whitelist()
def import_github_repos(
    username: str = None,
    organization: str = None,
    github_token: str = None,
    import_as_assets: bool = True,
    asset_category: str = None
) -> Dict[str, Any]:
    """
    Import all GitHub repositories as assets in ERPNext.
    
    Args:
        username: GitHub username
        organization: GitHub organization name
        github_token: GitHub personal access token (optional)
        import_as_assets: Create as assets (True) or items only (False)
        asset_category: Asset category to assign
    
    Returns:
        Dictionary with import results
    """
    try:
        from erpnext_assist.mcp_server.server import import_github_repos_as_assets
        
        if isinstance(import_as_assets, str):
            import_as_assets = import_as_assets.lower() == "true"
        
        result = import_github_repos_as_assets(
            username=username,
            organization=organization,
            github_token=github_token,
            import_as_assets=import_as_assets,
            asset_category=asset_category
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"GitHub import error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to import GitHub repositories"
        }


@frappe.whitelist()
def find_warehouses(
    location: str,
    search_query: str = "lager",
    region: str = None,
    add_to_erpnext: bool = True,
    phone_control: bool = False
) -> Dict[str, Any]:
    """
    Find warehouses on FINN.no in Norway (including northern regions).
    
    Args:
        location: Location to search (e.g., 'Tromsø', 'Bodø')
        search_query: Search query (default: 'lager')
        region: Optional region filter
        add_to_erpnext: Add found warehouses to ERPNext
        phone_control: Use phone control for automated browsing
    
    Returns:
        Dictionary with found warehouses
    """
    try:
        from erpnext_assist.mcp_server.server import find_warehouses_on_finn
        
        if isinstance(add_to_erpnext, str):
            add_to_erpnext = add_to_erpnext.lower() == "true"
        if isinstance(phone_control, str):
            phone_control = phone_control.lower() == "true"
        
        result = find_warehouses_on_finn(
            location=location,
            search_query=search_query,
            region=region,
            add_to_erpnext=add_to_erpnext,
            phone_control=phone_control
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Warehouse finder error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to find warehouses"
        }


@frappe.whitelist()
def manage_marketplace_with_phone(
    material_request_items: str = None,
    marketplace: str = "facebook",
    action: str = "search",
    message_template: str = "standard"
) -> Dict[str, Any]:
    """
    Manage marketplace listings with phone control and standard Norwegian messages.
    
    Args:
        material_request_items: JSON string of Material Request item IDs
        marketplace: Target marketplace ('facebook' or 'finn')
        action: Action to perform
        message_template: Message template to use
    
    Returns:
        Dictionary with marketplace management results
    """
    try:
        from erpnext_assist.mcp_server.server import manage_marketplace_listings_with_phone_ctrl
        import json
        
        item_ids = json.loads(material_request_items) if material_request_items else None
        
        result = manage_marketplace_listings_with_phone_ctrl(
            material_request_items=item_ids,
            marketplace=marketplace,
            action=action,
            message_template=message_template
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Marketplace management error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to manage marketplace listings"
        }


@frappe.whitelist()
def import_norwegian_accounts(standard: str = "NS4102", company: str = None) -> Dict[str, Any]:
    """
    Import Norwegian chart of accounts (NS 4102 or DFØ standard).
    
    Args:
        standard: "NS4102" for private sector or "DFO" for government sector
        company: Company name to import accounts for
    
    Returns:
        Dictionary with import results
    """
    try:
        from erpnext_assist.mcp_server.server import import_norwegian_chart_of_accounts
        
        result = import_norwegian_chart_of_accounts(
            standard=standard,
            company=company
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Norwegian accounts import error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to import Norwegian chart of accounts ({standard})"
        }


@frappe.whitelist()
def interact_with_skatteetaten(action: str, data: str = None) -> Dict[str, Any]:
    """
    Interact with Skatteetaten (Norwegian Tax Authority) API or via phone control.
    
    Args:
        action: Type of interaction (employee_registration, tax_report, deduction_request, check_deadlines, check_account)
        data: JSON string with additional data for the action
    
    Returns:
        Dictionary with interaction results
    """
    try:
        from erpnext_assist.mcp_server.server import manage_skatteetaten_submissions
        import json
        
        data_dict = json.loads(data) if data else {}
        
        result = manage_skatteetaten_submissions(
            action=action,
            data=data_dict
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Skatteetaten interaction error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to interact with Skatteetaten"
        }


@frappe.whitelist()
def submit_kommune_application(kommune: str, application_type: str, data: str = None) -> Dict[str, Any]:
    """
    Submit applications to Norwegian municipal services (kommune).
    
    Args:
        kommune: Municipality name (e.g., "Lyngdal")
        application_type: Type of application (building_permit, renovation_permit, property_upgrade)
        data: JSON string with application data
    
    Returns:
        Dictionary with submission results
    """
    try:
        from erpnext_assist.mcp_server.server import submit_lyngdal_kommune_application
        import json
        
        data_dict = json.loads(data) if data else {}
        
        result = submit_lyngdal_kommune_application(
            kommune=kommune,
            application_type=application_type,
            data=data_dict
        )
        
        return result
    except Exception as e:
        frappe.log_error(f"Kommune application error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to submit application to {kommune} Kommune"
        }
