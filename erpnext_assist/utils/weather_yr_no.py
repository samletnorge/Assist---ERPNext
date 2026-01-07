"""
Norwegian Weather Forecast Integration using yr.no API (Norwegian Meteorological Institute)

This module provides functionality to fetch weather forecasts from yr.no
for Norwegian farm locations to help with planning farm activities.
"""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class YrNoWeatherAPI:
    """
    Client for yr.no Locationforecast API v2.0
    
    Documentation: https://api.met.no/weatherapi/locationforecast/2.0/documentation
    """
    
    BASE_URL = "https://api.met.no/weatherapi/locationforecast/2.0"
    USER_AGENT = "ERPNext-Assist-FarmManagement/1.0 (github.com/samletnorge/Assist---ERPNext)"
    
    def __init__(self):
        """Initialize the yr.no weather API client."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT
        })
    
    def get_forecast(self, latitude: float, longitude: float, altitude: Optional[int] = None) -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            altitude: Altitude in meters (optional, improves accuracy)
            
        Returns:
            Dictionary with weather forecast data
        """
        try:
            # Build URL parameters
            params = {
                "lat": round(latitude, 4),
                "lon": round(longitude, 4)
            }
            
            if altitude is not None:
                params["altitude"] = int(altitude)
            
            # Make API request
            url = f"{self.BASE_URL}/compact"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and structure the forecast
            return self._parse_forecast(data)
            
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fetch weather forecast from yr.no"
            }
    
    def _parse_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the raw forecast data into a more usable format.
        
        Args:
            data: Raw API response data
            
        Returns:
            Structured forecast data
        """
        try:
            properties = data.get("properties", {})
            timeseries = properties.get("timeseries", [])
            
            if not timeseries:
                return {
                    "success": False,
                    "message": "No forecast data available"
                }
            
            # Parse current conditions (first entry)
            current = timeseries[0]
            current_data = current.get("data", {}).get("instant", {}).get("details", {})
            
            # Group forecast by days
            daily_forecast = self._group_by_day(timeseries)
            
            # Extract hourly forecast for next 24 hours
            hourly_forecast = self._extract_hourly(timeseries[:24])
            
            return {
                "success": True,
                "updated": data.get("properties", {}).get("meta", {}).get("updated_at"),
                "current": {
                    "time": current.get("time"),
                    "temperature": current_data.get("air_temperature"),
                    "wind_speed": current_data.get("wind_speed"),
                    "wind_from_direction": current_data.get("wind_from_direction"),
                    "humidity": current_data.get("relative_humidity"),
                    "pressure": current_data.get("air_pressure_at_sea_level"),
                    "cloud_area_fraction": current_data.get("cloud_area_fraction"),
                    "precipitation": self._get_precipitation(current)
                },
                "hourly_forecast": hourly_forecast,
                "daily_forecast": daily_forecast,
                "message": "Weather forecast retrieved successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to parse weather forecast data"
            }
    
    def _get_precipitation(self, timeseries_entry: Dict[str, Any]) -> Optional[float]:
        """Extract precipitation data from a timeseries entry."""
        data = timeseries_entry.get("data", {})
        
        # Try to get precipitation from next_1_hours
        for period in ["next_1_hours", "next_6_hours", "next_12_hours"]:
            if period in data:
                details = data[period].get("details", {})
                if "precipitation_amount" in details:
                    return details["precipitation_amount"]
        
        return None
    
    def _extract_hourly(self, timeseries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract hourly forecast data."""
        hourly = []
        
        for entry in timeseries:
            time = entry.get("time")
            instant = entry.get("data", {}).get("instant", {}).get("details", {})
            
            # Get symbol/summary
            next_1h = entry.get("data", {}).get("next_1_hours", {})
            symbol = next_1h.get("summary", {}).get("symbol_code", "")
            precipitation = next_1h.get("details", {}).get("precipitation_amount", 0)
            
            hourly.append({
                "time": time,
                "temperature": instant.get("air_temperature"),
                "wind_speed": instant.get("wind_speed"),
                "precipitation": precipitation,
                "symbol": symbol,
                "humidity": instant.get("relative_humidity")
            })
        
        return hourly
    
    def _group_by_day(self, timeseries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Group forecast data by day."""
        daily = {}
        
        for entry in timeseries:
            time_str = entry.get("time", "")
            if not time_str:
                continue
            
            # Extract date (YYYY-MM-DD)
            date = time_str.split("T")[0]
            
            if date not in daily:
                daily[date] = {
                    "date": date,
                    "temperatures": [],
                    "precipitations": [],
                    "wind_speeds": [],
                    "symbols": []
                }
            
            instant = entry.get("data", {}).get("instant", {}).get("details", {})
            
            # Collect data
            if "air_temperature" in instant:
                daily[date]["temperatures"].append(instant["air_temperature"])
            
            if "wind_speed" in instant:
                daily[date]["wind_speeds"].append(instant["wind_speed"])
            
            # Get precipitation and symbol
            for period in ["next_1_hours", "next_6_hours"]:
                if period in entry.get("data", {}):
                    details = entry["data"][period].get("details", {})
                    if "precipitation_amount" in details:
                        daily[date]["precipitations"].append(details["precipitation_amount"])
                    
                    symbol = entry["data"][period].get("summary", {}).get("symbol_code")
                    if symbol:
                        daily[date]["symbols"].append(symbol)
                    break
        
        # Calculate daily summaries
        daily_forecast = []
        for date, data in sorted(daily.items()):
            temps = data["temperatures"]
            precips = data["precipitations"]
            winds = data["wind_speeds"]
            
            daily_forecast.append({
                "date": date,
                "temperature_min": min(temps) if temps else None,
                "temperature_max": max(temps) if temps else None,
                "temperature_avg": sum(temps) / len(temps) if temps else None,
                "precipitation_total": sum(precips) if precips else 0,
                "wind_speed_max": max(winds) if winds else None,
                "wind_speed_avg": sum(winds) / len(winds) if winds else None,
                "dominant_symbol": max(set(data["symbols"]), key=data["symbols"].count) if data["symbols"] else None
            })
        
        return daily_forecast[:7]  # Return 7 days


def get_farm_weather_forecast(
    location_name: str,
    latitude: float,
    longitude: float,
    altitude: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get weather forecast for a farm location in Norway.
    
    Args:
        location_name: Name of the location (for reference)
        latitude: Latitude in decimal degrees
        longitude: Longitude in decimal degrees
        altitude: Altitude in meters (optional)
        
    Returns:
        Dictionary with weather forecast and farming recommendations
    """
    try:
        # Get forecast from yr.no
        api = YrNoWeatherAPI()
        forecast = api.get_forecast(latitude, longitude, altitude)
        
        if not forecast.get("success"):
            return forecast
        
        # Add location information
        forecast["location"] = {
            "name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude
        }
        
        # Add farming recommendations based on weather
        forecast["farming_recommendations"] = _generate_farming_recommendations(forecast)
        
        return forecast
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get weather forecast"
        }


def _generate_farming_recommendations(forecast: Dict[str, Any]) -> List[str]:
    """
    Generate farming recommendations based on weather forecast.
    
    Args:
        forecast: Weather forecast data
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    current = forecast.get("current", {})
    daily = forecast.get("daily_forecast", [])
    
    if not daily:
        return recommendations
    
    # Temperature recommendations
    today = daily[0] if daily else {}
    temp_min = today.get("temperature_min")
    temp_max = today.get("temperature_max")
    
    if temp_min is not None and temp_min < 0:
        recommendations.append("⚠️ Frost warning: Protect sensitive crops from freezing temperatures")
    
    if temp_max is not None and temp_max > 25:
        recommendations.append("☀️ Hot weather: Ensure adequate irrigation for crops")
    
    # Precipitation recommendations
    precip_total = today.get("precipitation_total", 0)
    
    if precip_total > 10:
        recommendations.append("🌧️ Heavy rain expected: Postpone spraying and consider drainage")
    elif precip_total < 1:
        # Check if next few days are also dry
        dry_days = sum(1 for d in daily[:3] if d.get("precipitation_total", 0) < 1)
        if dry_days >= 2:
            recommendations.append("🌤️ Dry period ahead: Plan irrigation schedule")
    
    # Wind recommendations
    wind_max = today.get("wind_speed_max")
    
    if wind_max is not None and wind_max > 10:
        recommendations.append("💨 Strong winds expected: Secure greenhouse structures and delay spraying")
    
    # Multi-day outlook
    if len(daily) >= 3:
        avg_temp = sum(d.get("temperature_avg", 0) for d in daily[:3]) / 3
        if 10 <= avg_temp <= 20:
            recommendations.append("🌱 Good conditions for planting: Temperatures are ideal for most crops")
    
    return recommendations


def get_weather_for_coordinates(lat: float, lon: float) -> Dict[str, Any]:
    """
    Simple wrapper to get weather for coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Weather forecast dictionary
    """
    return get_farm_weather_forecast("Custom Location", lat, lon)
