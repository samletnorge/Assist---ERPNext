"""Test weather integration with yr.no API."""

import unittest
from unittest.mock import MagicMock, patch
from erpnext_assist.utils.weather_yr_no import (
    YrNoWeatherAPI,
    get_farm_weather_forecast,
    get_weather_for_coordinates
)


class TestYrNoWeatherAPI(unittest.TestCase):
    """Test cases for yr.no weather API integration."""
    
    def test_weather_api_initialization(self):
        """Test that weather API client initializes correctly."""
        api = YrNoWeatherAPI()
        self.assertIsNotNone(api.session)
        self.assertEqual(api.session.headers.get("User-Agent"), YrNoWeatherAPI.USER_AGENT)
    
    def test_get_weather_for_coordinates(self):
        """Test getting weather for coordinates."""
        # This is a basic test structure - actual API call requires network
        result = get_weather_for_coordinates(lat=59.9139, lon=10.7522)
        # Should return a dictionary
        self.assertIsInstance(result, dict)
        # Should have success key
        self.assertIn("success", result)
    
    @patch('erpnext_assist.utils.weather_yr_no.requests.Session.get')
    def test_get_forecast_with_mock(self, mock_get):
        """Test weather forecast with mocked API response."""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "properties": {
                "meta": {
                    "updated_at": "2026-01-07T12:00:00Z"
                },
                "timeseries": [
                    {
                        "time": "2026-01-07T12:00:00Z",
                        "data": {
                            "instant": {
                                "details": {
                                    "air_temperature": 5.0,
                                    "wind_speed": 3.5,
                                    "relative_humidity": 75.0,
                                    "air_pressure_at_sea_level": 1013.0,
                                    "cloud_area_fraction": 50.0
                                }
                            },
                            "next_1_hours": {
                                "summary": {
                                    "symbol_code": "cloudy"
                                },
                                "details": {
                                    "precipitation_amount": 0.0
                                }
                            }
                        }
                    }
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Test the API call
        api = YrNoWeatherAPI()
        result = api.get_forecast(latitude=59.9139, longitude=10.7522)
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertIn("current", result)
        self.assertEqual(result["current"]["temperature"], 5.0)
        self.assertEqual(result["current"]["wind_speed"], 3.5)
    
    def test_coordinate_validation(self):
        """Test coordinate validation."""
        # Invalid latitude
        result = get_farm_weather_forecast(
            "Test Farm",
            latitude=91.0,  # Invalid
            longitude=10.0
        )
        # Should handle invalid coordinates
        self.assertIsInstance(result, dict)
    
    def test_farming_recommendations(self):
        """Test that farming recommendations are generated."""
        from erpnext_assist.utils.weather_yr_no import _generate_farming_recommendations
        
        # Mock forecast data
        forecast = {
            "current": {
                "temperature": 10.0,
                "precipitation": 0.0
            },
            "daily_forecast": [
                {
                    "date": "2026-01-07",
                    "temperature_min": -2.0,  # Frost warning
                    "temperature_max": 15.0,
                    "precipitation_total": 0.5,
                    "wind_speed_max": 5.0
                }
            ]
        }
        
        recommendations = _generate_farming_recommendations(forecast)
        
        # Should return a list
        self.assertIsInstance(recommendations, list)
        
        # Should have frost warning for negative temperature
        frost_warning = any("Frost warning" in rec or "frost" in rec.lower() 
                          for rec in recommendations)
        self.assertTrue(frost_warning, "Should have frost warning for sub-zero temperatures")


class TestWeatherIntegration(unittest.TestCase):
    """Integration tests for weather features."""
    
    def test_get_farm_weather_forecast_structure(self):
        """Test that farm weather forecast returns correct structure."""
        # Note: This makes a real API call if network is available
        result = get_farm_weather_forecast(
            location_name="Test Farm",
            latitude=59.9139,
            longitude=10.7522
        )
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        
        if result.get("success"):
            # If API call succeeded, check structure
            self.assertIn("current", result)
            self.assertIn("location", result)
            self.assertIn("farming_recommendations", result)
            self.assertIsInstance(result["farming_recommendations"], list)


if __name__ == "__main__":
    unittest.main()
