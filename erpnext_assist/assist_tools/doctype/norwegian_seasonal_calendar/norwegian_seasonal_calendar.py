"""Norwegian Seasonal Calendar DocType for Norwegian farming planting and harvest schedules."""

import frappe
from frappe.model.document import Document


class NorwegianSeasonalCalendar(Document):
    """
    Norwegian Seasonal Calendar for tracking crop planting and harvest schedules
    tailored to Norwegian climate zones.
    """
    
    def validate(self):
        """Validate the seasonal calendar entry."""
        if not self.crop_name:
            frappe.throw("Crop name is required")
        
        if not self.norwegian_name:
            frappe.throw("Norwegian name is required")
    
    def get_planting_schedule(self, month=None):
        """
        Get planting schedule for this crop.
        
        Args:
            month: Optional specific month to filter by
            
        Returns:
            List of planting activities
        """
        if not self.planting_details:
            return []
        
        schedule = []
        for item in self.planting_details:
            if month and item.month != month:
                continue
            schedule.append({
                "activity_type": item.activity_type,
                "month": item.month,
                "description": item.activity_description,
                "indoor_outdoor": item.indoor_outdoor,
                "soil_temperature": item.soil_temperature,
                "notes": item.notes
            })
        
        return schedule
    
    def get_current_month_activities(self):
        """Get activities for the current month."""
        from datetime import datetime
        current_month = datetime.now().strftime("%B")
        return self.get_planting_schedule(month=current_month)


@frappe.whitelist()
def get_seasonal_calendar(crop_name=None, climate_zone=None, crop_type=None):
    """
    Get seasonal calendar data filtered by crop name, climate zone, or crop type.
    
    Args:
        crop_name: Optional crop name to filter
        climate_zone: Optional climate zone to filter
        crop_type: Optional crop type to filter
        
    Returns:
        List of seasonal calendar entries
    """
    filters = {}
    
    if crop_name:
        filters["crop_name"] = ["like", f"%{crop_name}%"]
    
    if climate_zone:
        filters["climate_zone"] = ["in", [climate_zone, "All Zones"]]
    
    if crop_type:
        filters["crop_type"] = crop_type
    
    calendars = frappe.get_all(
        "Norwegian Seasonal Calendar",
        filters=filters,
        fields=["name", "crop_name", "norwegian_name", "crop_type", "climate_zone", 
                "growing_season", "harvest_details", "notes"]
    )
    
    # Get detailed planting info for each calendar
    for calendar in calendars:
        doc = frappe.get_doc("Norwegian Seasonal Calendar", calendar.name)
        calendar["planting_schedule"] = doc.get_planting_schedule()
    
    return calendars


@frappe.whitelist()
def get_current_month_crops(climate_zone=None):
    """
    Get crops that should be planted or harvested in the current month.
    
    Args:
        climate_zone: Optional climate zone to filter
        
    Returns:
        List of crops with activities for current month
    """
    from datetime import datetime
    current_month = datetime.now().strftime("%B")
    
    filters = {}
    if climate_zone:
        filters["climate_zone"] = ["in", [climate_zone, "All Zones"]]
    
    calendars = frappe.get_all(
        "Norwegian Seasonal Calendar",
        filters=filters,
        fields=["name", "crop_name", "norwegian_name", "crop_type", "climate_zone"]
    )
    
    current_crops = []
    for calendar in calendars:
        doc = frappe.get_doc("Norwegian Seasonal Calendar", calendar.name)
        activities = doc.get_current_month_activities()
        
        if activities:
            current_crops.append({
                "crop_name": calendar.crop_name,
                "norwegian_name": calendar.norwegian_name,
                "crop_type": calendar.crop_type,
                "climate_zone": calendar.climate_zone,
                "activities": activities
            })
    
    return {
        "month": current_month,
        "climate_zone": climate_zone or "All",
        "crops": current_crops,
        "count": len(current_crops)
    }
