"""
Road Project DocType

Stores information about road construction projects from the Norwegian Public Roads Administration (Statens vegvesen).
Supports tracking project details, locations, timelines, and strategic value forecasting.
"""

import frappe
from frappe.model.document import Document
from typing import Dict, Any, Optional
import json


class RoadProject(Document):
    """Road Project DocType for tracking Vegvesen road construction projects."""
    
    def before_save(self):
        """Validate and process data before saving."""
        self.validate_coordinates()
        self.calculate_strategic_value()
    
    def validate_coordinates(self):
        """Validate latitude and longitude if provided."""
        if self.latitude:
            if not -90 <= self.latitude <= 90:
                frappe.throw("Latitude must be between -90 and 90 degrees")
        
        if self.longitude:
            if not -180 <= self.longitude <= 180:
                frappe.throw("Longitude must be between -180 and 180 degrees")
    
    def calculate_strategic_value(self):
        """
        Calculate strategic value based on project attributes.
        This can be enhanced with more sophisticated algorithms.
        """
        if not self.strategic_value:
            # Default strategic value calculation
            score = 0
            
            # Priority contributes to strategic value
            if self.priority == "Critical":
                score += 4
            elif self.priority == "High":
                score += 3
            elif self.priority == "Medium":
                score += 2
            elif self.priority == "Low":
                score += 1
            
            # Project type impacts value
            if self.project_type in ["New Road", "Road Expansion", "Bridge", "Tunnel"]:
                score += 2
            elif self.project_type in ["Intersection", "Maintenance"]:
                score += 1
            
            # Cost indicates project scale
            if self.estimated_cost:
                if self.estimated_cost > 1000000000:  # > 1 billion NOK
                    score += 3
                elif self.estimated_cost > 500000000:  # > 500 million NOK
                    score += 2
                elif self.estimated_cost > 100000000:  # > 100 million NOK
                    score += 1
            
            # Map score to strategic value
            if score >= 8:
                self.strategic_value = "Very High"
            elif score >= 6:
                self.strategic_value = "High"
            elif score >= 4:
                self.strategic_value = "Medium"
            elif score >= 2:
                self.strategic_value = "Low"
            else:
                self.strategic_value = "Very Low"
    
    def get_map_data(self) -> Dict[str, Any]:
        """
        Get map-ready data for plotting this project.
        
        Returns:
            Dictionary with project data formatted for map display
        """
        map_data = {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "strategic_value": self.strategic_value,
            "status": self.status,
            "estimated_cost": self.estimated_cost,
            "start_date": str(self.start_date) if self.start_date else None,
            "end_date": str(self.end_date) if self.end_date else None,
            "project_type": self.project_type
        }
        
        # Parse geometry data if available
        if self.geometry_data:
            try:
                map_data["geometry"] = json.loads(self.geometry_data)
            except json.JSONDecodeError:
                pass
        
        return map_data
    
    def analyze_nearby_impact(self, radius_km: float = 10.0) -> Dict[str, Any]:
        """
        Analyze potential impact on nearby warehouses, properties, and assets.
        
        Args:
            radius_km: Search radius in kilometers (default 10km)
        
        Returns:
            Dictionary with impact analysis
        """
        if not self.latitude or not self.longitude:
            return {"error": "Project location coordinates not available"}
        
        # Find nearby warehouses
        warehouses = frappe.get_all(
            "Warehouse",
            fields=["name", "warehouse_name", "latitude", "longitude"],
            filters={"latitude": ["is", "set"], "longitude": ["is", "set"]}
        )
        
        nearby_warehouses = []
        for warehouse in warehouses:
            if warehouse.get("latitude") and warehouse.get("longitude"):
                distance = self._calculate_distance(
                    self.latitude, self.longitude,
                    warehouse.latitude, warehouse.longitude
                )
                if distance <= radius_km:
                    nearby_warehouses.append({
                        "name": warehouse.name,
                        "warehouse_name": warehouse.warehouse_name,
                        "distance_km": round(distance, 2)
                    })
        
        # Update nearby_locations field
        if nearby_warehouses:
            location_text = "\n".join([
                f"{w['warehouse_name']} ({w['distance_km']} km)"
                for w in nearby_warehouses
            ])
            self.nearby_locations = location_text
            self.impact_radius_km = radius_km
        
        return {
            "nearby_warehouses": nearby_warehouses,
            "radius_km": radius_km,
            "impact_description": self._generate_impact_forecast(nearby_warehouses)
        }
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula.
        
        Returns:
            Distance in kilometers
        """
        from math import radians, cos, sin, asin, sqrt
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        # Earth radius in kilometers
        r = 6371
        
        return c * r
    
    def _generate_impact_forecast(self, nearby_warehouses: list) -> str:
        """Generate impact forecast description."""
        if not nearby_warehouses:
            return "No significant nearby assets identified within impact radius."
        
        count = len(nearby_warehouses)
        impact_text = f"This road project may significantly impact {count} nearby warehouse(s). "
        
        if self.strategic_value in ["High", "Very High"]:
            impact_text += "Due to high strategic value, these locations may experience increased accessibility and property value appreciation. "
        
        if self.project_type in ["New Road", "Road Expansion"]:
            impact_text += "New road infrastructure typically increases logistics efficiency and reduces transportation costs for nearby facilities."
        
        return impact_text


@frappe.whitelist()
def get_projects_for_map(county: Optional[str] = None, strategic_value: Optional[str] = None) -> list:
    """
    Get road projects formatted for map display.
    
    Args:
        county: Optional county code filter
        strategic_value: Optional strategic value filter
    
    Returns:
        List of projects with map data
    """
    filters = {}
    if county:
        filters["county"] = county
    if strategic_value:
        filters["strategic_value"] = strategic_value
    
    projects = frappe.get_all(
        "Road Project",
        filters=filters,
        fields=["name"]
    )
    
    map_data = []
    for project in projects:
        doc = frappe.get_doc("Road Project", project.name)
        if doc.latitude and doc.longitude:
            map_data.append(doc.get_map_data())
    
    return map_data


@frappe.whitelist()
def analyze_project_impact(project_id: str, radius_km: float = 10.0) -> Dict[str, Any]:
    """
    Analyze impact of a specific road project.
    
    Args:
        project_id: Road Project ID
        radius_km: Search radius in kilometers
    
    Returns:
        Impact analysis results
    """
    try:
        doc = frappe.get_doc("Road Project", project_id)
        return doc.analyze_nearby_impact(float(radius_km))
    except Exception as e:
        frappe.log_error(f"Error analyzing project impact: {str(e)}")
        return {"error": str(e)}
