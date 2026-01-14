"""
Unit tests for Road Project DocType
"""

import unittest
import frappe


class TestRoadProject(unittest.TestCase):
    """Test Road Project DocType functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.test_project_id = "TEST-RV23-001"
    
    def tearDown(self):
        """Clean up test data."""
        if frappe.db.exists("Road Project", self.test_project_id):
            frappe.delete_doc("Road Project", self.test_project_id)
    
    def test_create_road_project(self):
        """Test creating a basic road project."""
        project = frappe.get_doc({
            "doctype": "Road Project",
            "project_id": self.test_project_id,
            "project_name": "Test Road Project E18",
            "county": "9745",
            "county_name": "Vestfold og Telemark",
            "status": "Planning",
            "latitude": 59.1234,
            "longitude": 10.5678,
            "estimated_cost": 500000000,
            "project_type": "Road Expansion",
            "priority": "High"
        })
        project.insert()
        
        self.assertTrue(frappe.db.exists("Road Project", self.test_project_id))
        self.assertEqual(project.strategic_value, "High")
    
    def test_coordinate_validation(self):
        """Test coordinate validation."""
        project = frappe.get_doc({
            "doctype": "Road Project",
            "project_id": self.test_project_id,
            "project_name": "Test Invalid Coordinates",
            "latitude": 95.0,  # Invalid latitude
            "longitude": 10.0
        })
        
        with self.assertRaises(frappe.ValidationError):
            project.insert()
    
    def test_strategic_value_calculation(self):
        """Test automatic strategic value calculation."""
        project = frappe.get_doc({
            "doctype": "Road Project",
            "project_id": self.test_project_id,
            "project_name": "Test Strategic Value",
            "estimated_cost": 1500000000,  # High cost
            "project_type": "New Road",
            "priority": "Critical"
        })
        project.insert()
        
        self.assertEqual(project.strategic_value, "Very High")
    
    def test_get_map_data(self):
        """Test getting map-ready data."""
        project = frappe.get_doc({
            "doctype": "Road Project",
            "project_id": self.test_project_id,
            "project_name": "Test Map Data",
            "latitude": 59.5,
            "longitude": 10.5,
            "strategic_value": "High"
        })
        project.insert()
        
        map_data = project.get_map_data()
        
        self.assertEqual(map_data["project_id"], self.test_project_id)
        self.assertEqual(map_data["latitude"], 59.5)
        self.assertEqual(map_data["longitude"], 10.5)
