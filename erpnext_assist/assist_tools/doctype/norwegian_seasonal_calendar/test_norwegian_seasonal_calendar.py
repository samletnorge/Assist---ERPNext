"""Test Norwegian Seasonal Calendar."""

import frappe
import unittest


class TestNorwegianSeasonalCalendar(unittest.TestCase):
    """Test cases for Norwegian Seasonal Calendar DocType."""
    
    def setUp(self):
        """Set up test data."""
        # Clean up any existing test data
        frappe.db.sql("DELETE FROM `tabNorwegian Seasonal Calendar` WHERE crop_name='Test Tomato'")
        frappe.db.commit()
    
    def tearDown(self):
        """Clean up test data."""
        frappe.db.sql("DELETE FROM `tabNorwegian Seasonal Calendar` WHERE crop_name='Test Tomato'")
        frappe.db.commit()
    
    def test_create_seasonal_calendar(self):
        """Test creating a seasonal calendar entry."""
        calendar = frappe.get_doc({
            "doctype": "Norwegian Seasonal Calendar",
            "crop_name": "Test Tomato",
            "norwegian_name": "Tomat",
            "crop_type": "Vegetable",
            "climate_zone": "Southern Norway (Sør-Norge)",
            "growing_season": "April - September",
            "harvest_details": "Harvest when fruits are fully colored",
            "planting_details": [
                {
                    "activity_type": "Sowing Indoors",
                    "month": "March",
                    "activity_description": "Sow seeds indoors",
                    "indoor_outdoor": "Indoor",
                    "soil_temperature": "18-20°C"
                },
                {
                    "activity_type": "Transplanting",
                    "month": "May",
                    "activity_description": "Transplant to greenhouse or outdoors after frost",
                    "indoor_outdoor": "Outdoor",
                    "soil_temperature": "15°C"
                }
            ]
        })
        
        calendar.insert()
        self.assertTrue(calendar.name)
        self.assertEqual(calendar.crop_name, "Test Tomato")
        self.assertEqual(len(calendar.planting_details), 2)
    
    def test_get_planting_schedule(self):
        """Test getting planting schedule."""
        calendar = frappe.get_doc({
            "doctype": "Norwegian Seasonal Calendar",
            "crop_name": "Test Tomato",
            "norwegian_name": "Tomat",
            "crop_type": "Vegetable",
            "climate_zone": "Southern Norway (Sør-Norge)",
            "planting_details": [
                {
                    "activity_type": "Sowing Indoors",
                    "month": "March",
                    "activity_description": "Sow seeds indoors"
                }
            ]
        })
        
        calendar.insert()
        
        # Get full schedule
        schedule = calendar.get_planting_schedule()
        self.assertEqual(len(schedule), 1)
        self.assertEqual(schedule[0]["month"], "March")
        
        # Get specific month
        march_schedule = calendar.get_planting_schedule(month="March")
        self.assertEqual(len(march_schedule), 1)
        
        april_schedule = calendar.get_planting_schedule(month="April")
        self.assertEqual(len(april_schedule), 0)
