#!/usr/bin/env python3
"""
ERPNext Assist - Installation Verification Script

Run this script after installing the app to verify all components are working correctly.
"""

import sys
import importlib.util

def check_module(module_name, package_name=None):
    """Check if a Python module is installed."""
    display_name = package_name or module_name
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {display_name} - NOT INSTALLED")
        return False
    else:
        print(f"✅ {display_name} - installed")
        return True

def check_file(filepath, description):
    """Check if a file exists."""
    import os
    if os.path.exists(filepath):
        print(f"✅ {description} - found")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False

def main():
    print("=" * 70)
    print("ERPNext Assist - Installation Verification")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # Check Python version
    print("1. Python Version Check")
    print("-" * 70)
    py_version = sys.version_info
    if py_version >= (3, 10):
        print(f"✅ Python {py_version.major}.{py_version.minor}.{py_version.micro} - OK")
    else:
        print(f"⚠️  Python {py_version.major}.{py_version.minor}.{py_version.micro} - Version 3.10+ recommended")
        all_ok = False
    print()
    
    # Check required dependencies
    print("2. Core Dependencies")
    print("-" * 70)
    deps_ok = True
    deps_ok &= check_module("frappe")
    deps_ok &= check_module("mcp", "mcp[cli]")
    deps_ok &= check_module("requests")
    deps_ok &= check_module("rembg", "rembg (AI background removal)")
    deps_ok &= check_module("PIL", "Pillow (image processing)")
    all_ok &= deps_ok
    print()
    
    # Check app structure
    print("3. App Structure")
    print("-" * 70)
    structure_ok = True
    structure_ok &= check_file("erpnext_assist/__init__.py", "App package")
    structure_ok &= check_file("erpnext_assist/hooks.py", "Hooks file")
    structure_ok &= check_file("erpnext_assist/api.py", "API endpoints")
    structure_ok &= check_file("erpnext_assist/mcp_server/server.py", "MCP server")
    structure_ok &= check_file("erpnext_assist/utils/image_processing.py", "Image processing utils")
    all_ok &= structure_ok
    print()
    
    # Check DocTypes
    print("4. DocTypes")
    print("-" * 70)
    doctypes_ok = True
    doctypes_ok &= check_file(
        "erpnext_assist/assist_tools/doctype/assist_tool_draft/assist_tool_draft.json",
        "Assist Tool Draft"
    )
    doctypes_ok &= check_file(
        "erpnext_assist/assist_tools/doctype/assist_tool_parameter/assist_tool_parameter.json",
        "Assist Tool Parameter"
    )
    doctypes_ok &= check_file(
        "erpnext_assist/assist_tools/doctype/marketplace_listing/marketplace_listing.json",
        "Marketplace Listing"
    )
    doctypes_ok &= check_file(
        "erpnext_assist/assist_tools/doctype/saved_marketplace_search/saved_marketplace_search.json",
        "Saved Marketplace Search"
    )
    all_ok &= doctypes_ok
    print()
    
    # Check documentation
    print("5. Documentation")
    print("-" * 70)
    docs_ok = True
    docs_ok &= check_file("README.md", "Main README")
    docs_ok &= check_file("QUICKSTART.md", "Quick Start Guide")
    docs_ok &= check_file("EXAMPLES.md", "Examples")
    docs_ok &= check_file("ARCHITECTURE.md", "Architecture")
    all_ok &= docs_ok
    print()
    
    # Test imports
    print("6. Import Tests")
    print("-" * 70)
    try:
        from erpnext_assist.utils.image_processing import remove_background
        print("✅ Image processing module - imports OK")
    except ImportError as e:
        print(f"❌ Image processing module - import failed: {e}")
        all_ok = False
    
    try:
        from erpnext_assist.mcp_server.server import mcp
        print("✅ MCP server module - imports OK")
    except ImportError as e:
        print(f"❌ MCP server module - import failed: {e}")
        all_ok = False
    
    try:
        from erpnext_assist.api import remove_image_background
        print("✅ API module - imports OK")
    except ImportError as e:
        print(f"❌ API module - import failed: {e}")
        all_ok = False
    print()
    
    # Summary
    print("=" * 70)
    if all_ok:
        print("✅ ALL CHECKS PASSED - Installation verified successfully!")
        print()
        print("Next steps:")
        print("  1. Install the app: bench --site [site] install-app erpnext_assist")
        print("  2. Restart bench: bench restart")
        print("  3. Check QUICKSTART.md for usage instructions")
        print("  4. Run MCP server: python -m erpnext_assist.mcp_server.server")
    else:
        print("⚠️  SOME CHECKS FAILED - Please fix the issues above")
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("=" * 70)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
