# Norwegian Farm Management System - Usage Guide

This guide demonstrates how to use the Norwegian Farm Management features in ERPNext Assist for Norwegian farmers.

## Features

### 1. Norwegian Seasonal Calendar (Norsk Sesongkalender)

The seasonal calendar helps Norwegian farmers plan planting and harvesting schedules based on:
- Norwegian climate zones
- Monthly planting schedules
- Soil temperature requirements
- Indoor/outdoor/greenhouse guidance

#### Pre-loaded Crops

The system comes with 10 common Norwegian crops:
1. **Tomato** (Tomat) - All Zones
2. **Carrot** (Gulrot) - All Zones
3. **Potato** (Potet) - All Zones
4. **Lettuce** (Salat) - All Zones
5. **Strawberry** (Jordbær) - All Zones
6. **Pea** (Ert) - All Zones
7. **Cabbage** (Kål) - All Zones
8. **Onion** (Løk) - All Zones
9. **Cucumber** (Agurk) - Southern Norway
10. **Rhubarb** (Rabarbra) - All Zones

#### Usage Examples

**Load Sample Data:**
```javascript
// In ERPNext client console or custom script
frappe.call({
    method: "erpnext_assist.api.load_sample_seasonal_calendar",
    callback: function(r) {
        if (r.message.success) {
            frappe.msgprint(`Loaded ${r.message.created} crops into seasonal calendar`);
        }
    }
});
```

**Get Current Month Planting Activities:**
```javascript
frappe.call({
    method: "erpnext_assist.api.get_seasonal_calendar",
    args: {
        climate_zone: "Southern Norway (Sør-Norge)",
        current_month_only: true
    },
    callback: function(r) {
        if (r.message.success) {
            let crops = r.message.crops;
            console.log(`${crops.length} crops to plant/harvest this month:`);
            crops.forEach(crop => {
                console.log(`- ${crop.norwegian_name}: ${crop.activities.length} activities`);
            });
        }
    }
});
```

**Search for Specific Crop:**
```javascript
frappe.call({
    method: "erpnext_assist.api.get_seasonal_calendar",
    args: {
        crop_name: "tomato"
    },
    callback: function(r) {
        if (r.message.success && r.message.calendars.length > 0) {
            let tomato = r.message.calendars[0];
            console.log(`${tomato.norwegian_name} (${tomato.crop_name})`);
            console.log(`Growing season: ${tomato.growing_season}`);
            console.log(`Planting activities:`);
            tomato.planting_schedule.forEach(activity => {
                console.log(`  ${activity.month}: ${activity.description}`);
            });
        }
    }
});
```

**Using MCP Tool (with AI Assistant):**
```python
# Via AI assistant with MCP integration
# "What should I plant in May in Eastern Norway?"

from erpnext_assist.mcp_server.server import get_norwegian_seasonal_calendar

result = get_norwegian_seasonal_calendar(
    climate_zone="Eastern Norway (Østlandet)",
    current_month_only=True
)
```

### 2. Weather Forecast from yr.no (Norwegian Meteorological Institute)

Get accurate weather forecasts for Norwegian farm locations with farming-specific recommendations.

#### Features
- Current weather conditions
- Hourly forecast (24 hours)
- 7-day daily forecast
- Farming recommendations:
  - Frost warnings
  - Irrigation planning
  - Spraying windows (wind conditions)
  - Temperature-based planting guidance

#### Usage Examples

**Get Weather for Your Farm:**
```javascript
frappe.call({
    method: "erpnext_assist.api.get_weather_forecast",
    args: {
        location_name: "My Farm in Lyngdal",
        latitude: 58.1367,
        longitude: 7.0756,
        altitude: 50  // meters above sea level
    },
    callback: function(r) {
        if (r.message.success) {
            let current = r.message.current;
            console.log(`Current temperature: ${current.temperature}°C`);
            console.log(`Wind speed: ${current.wind_speed} m/s`);
            console.log(`Humidity: ${current.humidity}%`);
            
            console.log("\nFarming recommendations:");
            r.message.farming_recommendations.forEach(rec => {
                console.log(`  ${rec}`);
            });
            
            console.log("\n7-Day forecast:");
            r.message.daily_forecast.forEach(day => {
                console.log(`  ${day.date}: ${day.temperature_min}°C - ${day.temperature_max}°C, ${day.precipitation_total}mm rain`);
            });
        }
    }
});
```

**Common Norwegian City Coordinates:**
```javascript
const norwegianLocations = {
    oslo: { lat: 59.9139, lon: 10.7522 },
    bergen: { lat: 60.3913, lon: 5.3221 },
    trondheim: { lat: 63.4305, lon: 10.3951 },
    stavanger: { lat: 58.9700, lon: 5.7331 },
    tromso: { lat: 69.6492, lon: 18.9553 },
    kristiansand: { lat: 58.1467, lon: 7.9956 },
    drammen: { lat: 59.7439, lon: 10.2045 },
    fredrikstad: { lat: 59.2181, lon: 10.9298 },
    lillehammer: { lat: 61.1153, lon: 10.4662 },
    bodo: { lat: 67.2804, lon: 14.4049 }
};
```

**Using MCP Tool (with AI Assistant):**
```python
# Via AI assistant with MCP integration
# "What's the weather forecast for my farm in Tromsø this week?"

from erpnext_assist.mcp_server.server import get_norwegian_weather_forecast

result = get_norwegian_weather_forecast(
    location_name="Tromsø Farm",
    latitude=69.6492,
    longitude=18.9553,
    altitude=20
)

print(f"Current temperature: {result['current']['temperature']}°C")
print("\nFarming recommendations:")
for rec in result['farming_recommendations']:
    print(f"  - {rec}")
```

### 3. Marketplace Integration for Farm Products

Sell your farm products on FINN.no and Facebook Marketplace using the existing marketplace posting tool.

#### Usage Example

```javascript
// Post fresh produce to marketplace
frappe.call({
    method: "erpnext_assist.mcp_server.server",
    args: {
        tool: "post_to_marketplace",
        marketplace: "FINN.no",
        title: "Fresh Organic Tomatoes - 5kg",
        description: "Locally grown organic tomatoes from Lyngdal. Harvested this morning. Sweet and juicy!",
        price: 150.00,
        item_code: "TOMATO-001",
        listing_type: "Sale",
        images: ["/files/tomatoes1.jpg", "/files/tomatoes2.jpg"]
    }
});
```

## Complete Farming Workflow Example

### Morning Planning Routine

```javascript
// 1. Check today's weather
frappe.call({
    method: "erpnext_assist.api.get_weather_forecast",
    args: {
        location_name: "My Farm",
        latitude: 59.9139,
        longitude: 10.7522
    },
    callback: function(r) {
        if (r.message.success) {
            console.log("=== Today's Farming Conditions ===");
            console.log(`Temperature: ${r.message.current.temperature}°C`);
            console.log(`Precipitation: ${r.message.current.precipitation}mm`);
            console.log(`Wind: ${r.message.current.wind_speed} m/s`);
            
            console.log("\n=== Recommendations ===");
            r.message.farming_recommendations.forEach(rec => {
                console.log(rec);
            });
        }
    }
});

// 2. Check what to plant/harvest this month
frappe.call({
    method: "erpnext_assist.api.get_seasonal_calendar",
    args: {
        climate_zone: "Eastern Norway (Østlandet)",
        current_month_only: true
    },
    callback: function(r) {
        if (r.message.success) {
            console.log("\n=== Current Month Activities ===");
            console.log(`Month: ${r.message.month}`);
            r.message.crops.forEach(crop => {
                console.log(`\n${crop.norwegian_name} (${crop.crop_name}):`);
                crop.activities.forEach(activity => {
                    console.log(`  - ${activity.activity_type}: ${activity.description}`);
                });
            });
        }
    }
});
```

## Climate Zones

Norwegian climate zones supported:
1. **Southern Norway (Sør-Norge)** - Warmest, longest growing season
2. **Eastern Norway (Østlandet)** - Inland climate, continental
3. **Western Norway (Vestlandet)** - Coastal, mild, wet
4. **Central Norway (Trøndelag)** - Transitional zone
5. **Northern Norway (Nord-Norge)** - Short growing season, midnight sun
6. **All Zones** - Crops suitable for all Norwegian regions

## Tips for Norwegian Farmers

### Spring (Vår)
- Start hardy crops like peas and lettuce in April
- Start tomatoes indoors in March for greenhouse planting
- Monitor frost warnings from yr.no before transplanting
- Plant potatoes when soil reaches 7-8°C

### Summer (Sommer)
- Peak planting time for most vegetables in May-June
- Succession plant lettuce and carrots every 2 weeks
- Use weather forecasts to plan irrigation
- Harvest early crops like radishes and spring onions

### Autumn (Høst)
- Harvest potatoes when foliage dies back (September)
- Continue harvesting until first hard frost
- Plant garlic in October for next year
- Prepare soil for winter

### Winter (Vinter)
- Plan next year's planting schedule
- Order seeds
- Review seasonal calendar for crop rotation
- Maintain equipment and greenhouses

## Integration with ERPNext

The farm management features integrate seamlessly with standard ERPNext:

- **Items**: Farm products (vegetables, fruits, eggs, honey)
- **Stock Entry**: Track harvest quantities
- **Sales Invoice**: Record farm sales
- **Marketplace Listing**: Post products for sale
- **Seasonal Calendar**: Plan planting and harvesting

## Support

For issues or questions:
- GitHub: https://github.com/samletnorge/Assist---ERPNext/issues
- Documentation: https://github.com/samletnorge/Assist---ERPNext/wiki

## Data Sources

- **Weather**: yr.no (Norwegian Meteorological Institute) - Free API
- **Seasonal Calendar**: Based on Norwegian agricultural practices and climate zones
- **Crop Data**: Traditional Norwegian crop growing guidelines

---

**Lykke til med gårdsdriften!** (Good luck with your farming!)
