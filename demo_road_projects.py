#!/usr/bin/env python3
"""
Demonstration script for Vegvesen Road Project Tracking Tool

This script demonstrates how to use the new road project tracking functionality
to fetch projects, plot them on maps, and forecast location values.

Usage:
    python demo_road_projects.py
"""

import os
import sys

# Mock frappe for demonstration (would normally import from frappe)
class MockFrappe:
    """Mock frappe module for demonstration purposes."""
    
    @staticmethod
    def get_doc(doctype, name):
        """Mock get_doc method."""
        print(f"[DEMO] Would fetch {doctype}: {name}")
        return None
    
    @staticmethod
    def get_all(doctype, **kwargs):
        """Mock get_all method."""
        print(f"[DEMO] Would query {doctype} with filters: {kwargs.get('filters', {})}")
        return []


def demo_track_projects():
    """Demonstrate tracking road projects from Vegvesen."""
    print("\n" + "="*80)
    print("DEMO 1: Track Road Projects from Vegvesen NVDB API")
    print("="*80)
    
    print("\nFetching road projects for Vestfold og Telemark (county 9745)...")
    print("\nMCP Tool: track_vegvesen_road_projects()")
    print("Parameters:")
    print("  - county: '9745'")
    print("  - sync_to_erpnext: True")
    print("  - update_existing: False")
    
    print("\n[INFO] Using mock data (set USE_MOCK_VEGVESEN_DATA=true)")
    print("[SUCCESS] Fetched 1 road project(s) from Vegvesen NVDB API")
    print("[SUCCESS] Synced 1 project(s) to ERPNext")
    
    print("\nProject Details:")
    print("  - ID: RV-9745-001")
    print("  - Name: Road Project in County 9745")
    print("  - County: 9745 (Vestfold og Telemark)")
    print("  - Location: 59.1234°N, 10.2345°E")
    print("  - Estimated Cost: 500,000,000 NOK")
    print("  - Type: Road Expansion")
    print("  - Priority: High")
    print("  - Strategic Value: High (automatically calculated)")


def demo_map_visualization():
    """Demonstrate plotting projects on a map."""
    print("\n" + "="*80)
    print("DEMO 2: Plot Road Projects on Map with Strategic Value")
    print("="*80)
    
    print("\nVisualizing all high-value road projects...")
    print("\nMCP Tool: plot_road_projects_on_map()")
    print("Parameters:")
    print("  - county: '9745'")
    print("  - strategic_value: 'High'")
    print("  - include_impact_analysis: True")
    
    print("\n[SUCCESS] Retrieved 1 road project(s) for map visualization")
    
    print("\nMap Data:")
    print("  - Project: RV-9745-001 at (59.1234°N, 10.2345°E)")
    print("  - Strategic Value: High")
    print("  - Status: Planning")
    print("  - Impact Analysis: Analyzing nearby warehouses within 10km...")
    print("    * Found 0 nearby warehouses (demo environment)")
    print("    * Impact: This project may improve logistics in the region")


def demo_location_forecasting():
    """Demonstrate location value forecasting."""
    print("\n" + "="*80)
    print("DEMO 3: Forecast Location Value for Strategic Planning")
    print("="*80)
    
    print("\nForecasting value for a potential warehouse location...")
    print("\nMCP Tool: forecast_location_value()")
    print("Parameters:")
    print("  - latitude: 59.15")
    print("  - longitude: 10.25")
    print("  - search_radius_km: 20.0")
    
    print("\n[SUCCESS] Analyzed 1 road project(s) within 20.0km radius")
    
    print("\nValue Forecast:")
    print("  - Value Level: High")
    print("  - Value Score: 65/100")
    print("  - Nearby Projects: 1")
    print("  - High-Value Projects: 1")
    print("  - Total Investment: 500,000,000 NOK")
    
    print("\nNearby Projects:")
    print("  - RV-9745-001 (Road Project in County 9745)")
    print("    Distance: 3.2 km")
    print("    Strategic Value: High")
    print("    Cost: 500,000,000 NOK")
    print("    Type: Road Expansion")
    
    print("\nRecommendations:")
    print("  ✓ This location shows high potential due to planned road infrastructure")
    print("  ✓ Consider strategic investments or warehouse placement in this area")
    print("  ✓ Expected improvements in logistics and transportation efficiency")


def demo_impact_analysis():
    """Demonstrate impact analysis on existing assets."""
    print("\n" + "="*80)
    print("DEMO 4: Analyze Road Project Impact on Existing Assets")
    print("="*80)
    
    print("\nAnalyzing impact of RV-9745-001 on nearby warehouses...")
    print("\nAPI Endpoint: erpnext_assist.api.analyze_road_project_impact()")
    print("Parameters:")
    print("  - project_id: 'RV-9745-001'")
    print("  - radius_km: 15.0")
    
    print("\n[SUCCESS] Impact analysis completed successfully")
    
    print("\nImpact Analysis:")
    print("  - Search Radius: 15.0 km")
    print("  - Nearby Warehouses: 0 (demo environment)")
    print("  - Impact Description:")
    print("    'No significant nearby assets identified within impact radius.'")
    print("    (In production, this would show actual warehouses and their distances)")


def demo_api_usage():
    """Demonstrate API endpoint usage."""
    print("\n" + "="*80)
    print("DEMO 5: Using API Endpoints from Client Code")
    print("="*80)
    
    print("\nExample 1: Fetch and sync projects")
    print("""
frappe.call({
    method: "erpnext_assist.api.fetch_vegvesen_road_projects",
    args: {
        county: "9745",
        sync_to_erpnext: true
    },
    callback: function(r) {
        if (r.message.success) {
            console.log("Synced", r.message.projects_synced, "projects");
        }
    }
});
""")
    
    print("\nExample 2: Get map data")
    print("""
frappe.call({
    method: "erpnext_assist.api.get_road_projects_map",
    args: {
        strategic_value: "High"
    },
    callback: function(r) {
        if (r.message.success) {
            // Use r.message.projects to plot on map
            plot_on_leaflet_map(r.message.projects);
        }
    }
});
""")


def demo_use_cases():
    """Demonstrate real-world use cases."""
    print("\n" + "="*80)
    print("REAL-WORLD USE CASES")
    print("="*80)
    
    print("\n1. Warehouse Site Selection")
    print("   Scenario: Company expanding logistics operations in Norway")
    print("   Action: Track all road projects, filter by strategic value")
    print("   Result: Identify optimal locations near future highway infrastructure")
    
    print("\n2. Property Investment")
    print("   Scenario: Real estate company evaluating land purchases")
    print("   Action: Forecast location values based on planned roads")
    print("   Result: Secure high-value properties before market awareness")
    
    print("\n3. Logistics Planning")
    print("   Scenario: Distribution company optimizing delivery routes")
    print("   Action: Plot all road projects on map, analyze completion dates")
    print("   Result: Plan for future route optimizations")
    
    print("\n4. Strategic Expansion")
    print("   Scenario: Multi-site business planning 5-year expansion")
    print("   Action: Analyze multiple locations with value forecasting")
    print("   Result: Data-driven expansion decisions based on infrastructure")


def main():
    """Run all demonstrations."""
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + " "*20 + "VEGVESEN ROAD PROJECT TRACKING TOOL" + " "*23 + "#")
    print("#" + " "*25 + "Demonstration Script" + " "*33 + "#")
    print("#" + " "*78 + "#")
    print("#"*80)
    
    print("\nThis tool helps track road construction projects from Norwegian Public")
    print("Roads Administration (Vegvesen) and forecast high-value locations for")
    print("strategic business decisions.")
    
    # Run all demos
    demo_track_projects()
    demo_map_visualization()
    demo_location_forecasting()
    demo_impact_analysis()
    demo_api_usage()
    demo_use_cases()
    
    print("\n" + "="*80)
    print("INTEGRATION NOTES")
    print("="*80)
    print("\n1. Real NVDB API Integration:")
    print("   Set environment variable: USE_MOCK_VEGVESEN_DATA=false")
    print("   Research NVDB API object types from datakatalog")
    print("   Implement parsing logic for NVDB JSON responses")
    
    print("\n2. Map Visualization:")
    print("   Use Leaflet.js or similar for interactive maps")
    print("   Plot projects using latitude/longitude coordinates")
    print("   Color-code by strategic value (red=very high, green=low)")
    
    print("\n3. ERPNext Integration:")
    print("   Road projects stored in 'Road Project' DocType")
    print("   Links to Warehouse locations for impact analysis")
    print("   Automatic strategic value calculation on save")
    
    print("\n4. MCP Integration:")
    print("   All tools available through MCP protocol")
    print("   Works with Claude, OpenAI, Ollama, and custom AI")
    print("   Can be used conversationally or programmatically")
    
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + " "*25 + "Demo Complete!" + " "*40 + "#")
    print("#" + " "*78 + "#")
    print("#"*80 + "\n")


if __name__ == "__main__":
    main()
