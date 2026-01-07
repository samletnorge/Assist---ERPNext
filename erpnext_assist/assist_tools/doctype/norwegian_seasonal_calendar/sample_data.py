"""
Sample data for Norwegian Seasonal Calendar
Common crops suitable for Norwegian climate zones
"""

NORWEGIAN_CROPS_DATA = [
    {
        "crop_name": "Tomato",
        "norwegian_name": "Tomat",
        "crop_type": "Vegetable",
        "climate_zone": "All Zones",
        "growing_season": "March - October",
        "planting_details": [
            {
                "activity_type": "Sowing Indoors",
                "month": "March",
                "activity_description": "Start seeds indoors in warm location (18-22°C)",
                "indoor_outdoor": "Indoor",
                "soil_temperature": "18-22°C",
                "notes": "Use seed starting mix and provide good light"
            },
            {
                "activity_type": "Transplanting",
                "month": "May",
                "activity_description": "Transplant to greenhouse or outdoor after last frost",
                "indoor_outdoor": "Greenhouse",
                "soil_temperature": "15°C",
                "notes": "Harden off plants gradually before outdoor planting"
            }
        ],
        "harvest_details": "<p>Harvest from July to October when fruits are fully colored. Pick regularly to encourage more fruiting.</p>",
        "notes": "<p>Tomatoes grow best in greenhouses in most of Norway. Needs staking and regular feeding. Water consistently but avoid wetting leaves.</p>"
    },
    {
        "crop_name": "Carrot",
        "norwegian_name": "Gulrot",
        "crop_type": "Root Vegetable",
        "climate_zone": "All Zones",
        "growing_season": "April - October",
        "planting_details": [
            {
                "activity_type": "Direct Seeding",
                "month": "April",
                "activity_description": "Direct sow in prepared beds when soil can be worked",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "7°C",
                "notes": "Thin seedlings to 5cm apart when 5cm tall"
            },
            {
                "activity_type": "Direct Seeding",
                "month": "May",
                "activity_description": "Second sowing for continuous harvest",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "10°C",
                "notes": "Succession planting every 2-3 weeks possible"
            }
        ],
        "harvest_details": "<p>Harvest from July onwards when roots reach desired size. Can be left in ground and harvested as needed until first hard frost.</p>",
        "notes": "<p>Prefers loose, well-draining soil free of stones. Keep soil evenly moist. Thin seedlings properly for best root development.</p>"
    },
    {
        "crop_name": "Potato",
        "norwegian_name": "Potet",
        "crop_type": "Root Vegetable",
        "climate_zone": "All Zones",
        "growing_season": "April - October",
        "planting_details": [
            {
                "activity_type": "Direct Seeding",
                "month": "April",
                "activity_description": "Plant sprouted seed potatoes in Southern and Eastern Norway",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "7°C",
                "notes": "Plant 10-15cm deep, 30cm apart in rows"
            },
            {
                "activity_type": "Direct Seeding",
                "month": "May",
                "activity_description": "Plant in Central and Northern Norway",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "8°C",
                "notes": "Hill soil around plants as they grow"
            }
        ],
        "harvest_details": "<p>New potatoes ready 10-12 weeks after planting. Main crop ready when foliage dies back, usually September-October. Cure in cool, dark place before storage.</p>",
        "notes": "<p>Norway's most important food crop. Prefers slightly acidic soil. Hill regularly to prevent greening. Water during dry spells, especially during tuber formation.</p>"
    },
    {
        "crop_name": "Lettuce",
        "norwegian_name": "Salat",
        "crop_type": "Leafy Green",
        "climate_zone": "All Zones",
        "growing_season": "March - September",
        "planting_details": [
            {
                "activity_type": "Sowing Indoors",
                "month": "March",
                "activity_description": "Start early varieties indoors",
                "indoor_outdoor": "Indoor",
                "soil_temperature": "10-15°C",
                "notes": "Transplant after 3-4 weeks"
            },
            {
                "activity_type": "Direct Seeding",
                "month": "May",
                "activity_description": "Direct sow outdoors when soil is workable",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "7°C",
                "notes": "Succession planting every 2 weeks for continuous harvest"
            },
            {
                "activity_type": "Direct Seeding",
                "month": "June",
                "activity_description": "Continue succession planting",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "10°C",
                "notes": "Provide shade during hot weather"
            }
        ],
        "harvest_details": "<p>Harvest leaf lettuce by cutting outer leaves. Head lettuce ready 60-80 days from sowing. Pick in morning for best quality.</p>",
        "notes": "<p>Grows quickly in cool weather. Needs consistent moisture and fertile soil. Protect from slugs. Many varieties suitable for Norwegian climate.</p>"
    },
    {
        "crop_name": "Strawberry",
        "norwegian_name": "Jordbær",
        "crop_type": "Fruit",
        "climate_zone": "All Zones",
        "growing_season": "April - September",
        "planting_details": [
            {
                "activity_type": "Transplanting",
                "month": "April",
                "activity_description": "Plant bare-root or potted plants",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "10°C",
                "notes": "Space 30cm apart in rows 45cm apart"
            },
            {
                "activity_type": "Transplanting",
                "month": "August",
                "activity_description": "Late summer planting also possible",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "15°C",
                "notes": "Protect with mulch over winter"
            }
        ],
        "harvest_details": "<p>First harvest June-July in second year after planting. Pick berries when fully red. Morning harvest when cool gives best flavor and shelf life.</p>",
        "notes": "<p>Very popular in Norwegian gardens. Remove flowers first year to establish strong plants. Mulch with straw. Replace plants every 3-4 years. Protect from birds with netting.</p>"
    },
    {
        "crop_name": "Pea",
        "norwegian_name": "Ert",
        "crop_type": "Legume",
        "climate_zone": "All Zones",
        "growing_season": "April - August",
        "planting_details": [
            {
                "activity_type": "Direct Seeding",
                "month": "April",
                "activity_description": "Direct sow early varieties when soil is workable",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "5°C",
                "notes": "Peas tolerate cool soil and light frost"
            },
            {
                "activity_type": "Direct Seeding",
                "month": "May",
                "activity_description": "Succession planting for extended harvest",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "7°C",
                "notes": "Provide support for climbing varieties"
            }
        ],
        "harvest_details": "<p>Harvest shelling peas when pods are full but still bright green. Snow peas and snap peas when pods are flat or just starting to fill. Pick regularly to encourage more production.</p>",
        "notes": "<p>Cold-hardy crop perfect for Norwegian spring. Fix nitrogen in soil, improving fertility. Water during flowering and pod development. Many varieties from dwarf to tall climbers.</p>"
    },
    {
        "crop_name": "Cabbage",
        "norwegian_name": "Kål",
        "crop_type": "Vegetable",
        "climate_zone": "All Zones",
        "growing_season": "March - October",
        "planting_details": [
            {
                "activity_type": "Sowing Indoors",
                "month": "March",
                "activity_description": "Start early varieties indoors",
                "indoor_outdoor": "Indoor",
                "soil_temperature": "15-20°C",
                "notes": "Transplant when 4-6 leaves develop"
            },
            {
                "activity_type": "Transplanting",
                "month": "May",
                "activity_description": "Transplant hardened seedlings outdoors",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "10°C",
                "notes": "Space 45-60cm apart depending on variety"
            }
        ],
        "harvest_details": "<p>Harvest when heads are firm and before they split. Early varieties ready July-August, late varieties September-October. Some varieties improve after light frost.</p>",
        "notes": "<p>Traditional Norwegian crop, very cold-hardy. Needs rich soil and consistent moisture. Protect from cabbage worms with row covers. Store late varieties in cool cellar.</p>"
    },
    {
        "crop_name": "Onion",
        "norwegian_name": "Løk",
        "crop_type": "Vegetable",
        "climate_zone": "All Zones",
        "growing_season": "April - September",
        "planting_details": [
            {
                "activity_type": "Sowing Indoors",
                "month": "February",
                "activity_description": "Start from seed for bulb onions",
                "indoor_outdoor": "Indoor",
                "soil_temperature": "15-20°C",
                "notes": "Long growing season needed for large bulbs"
            },
            {
                "activity_type": "Transplanting",
                "month": "April",
                "activity_description": "Plant onion sets or seedlings",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "7°C",
                "notes": "Plant sets shallow, just covering tip"
            }
        ],
        "harvest_details": "<p>Harvest when tops fall over and begin to brown, usually August-September. Cure in dry, airy place for 2-3 weeks before storage. Store in cool, dry place.</p>",
        "notes": "<p>Staple crop in Norwegian kitchens. Needs full sun and well-drained soil. Weed carefully to avoid competition. Norwegian long-day varieties best for northern latitudes.</p>"
    },
    {
        "crop_name": "Cucumber",
        "norwegian_name": "Agurk",
        "crop_type": "Vegetable",
        "climate_zone": "Southern Norway (Sør-Norge)",
        "growing_season": "April - September",
        "planting_details": [
            {
                "activity_type": "Sowing Indoors",
                "month": "April",
                "activity_description": "Start seeds indoors in pots",
                "indoor_outdoor": "Indoor",
                "soil_temperature": "20-25°C",
                "notes": "Cucumber seeds don't transplant well, use large pots"
            },
            {
                "activity_type": "Greenhouse Planting",
                "month": "May",
                "activity_description": "Plant in greenhouse when established",
                "indoor_outdoor": "Greenhouse",
                "soil_temperature": "18°C",
                "notes": "Provide vertical support for climbing"
            }
        ],
        "harvest_details": "<p>Harvest regularly from July onwards when fruits reach desired size. Pick before they get too large and seedy. Regular harvesting encourages more production.</p>",
        "notes": "<p>Grows best in greenhouse in Norway. Needs warm temperatures and high humidity. Water regularly and feed weekly. Choose greenhouse varieties for best results.</p>"
    },
    {
        "crop_name": "Rhubarb",
        "norwegian_name": "Rabarbra",
        "crop_type": "Vegetable",
        "climate_zone": "All Zones",
        "growing_season": "April - August",
        "planting_details": [
            {
                "activity_type": "Transplanting",
                "month": "April",
                "activity_description": "Plant crowns or divisions",
                "indoor_outdoor": "Outdoor",
                "soil_temperature": "5°C",
                "notes": "Space plants 90cm apart, needs room to grow"
            }
        ],
        "harvest_details": "<p>Don't harvest first year. Light harvest second year. Full harvest from third year onwards, May-July. Pull stalks rather than cutting. Stop harvesting by mid-July to allow plant to recover.</p>",
        "notes": "<p>Very cold-hardy perennial, perfect for Norwegian climate. Grows in same spot for 15+ years. Needs rich soil and spring mulching. Remove flower stalks. Only stalks are edible, leaves are poisonous.</p>"
    }
]


def create_sample_seasonal_calendar():
    """Create sample seasonal calendar entries for common Norwegian crops."""
    import frappe
    
    created_count = 0
    skipped_count = 0
    
    for crop_data in NORWEGIAN_CROPS_DATA:
        # Check if crop already exists
        if frappe.db.exists("Norwegian Seasonal Calendar", crop_data["crop_name"]):
            print(f"Skipping {crop_data['crop_name']} - already exists")
            skipped_count += 1
            continue
        
        try:
            # Create the seasonal calendar entry
            doc = frappe.get_doc({
                "doctype": "Norwegian Seasonal Calendar",
                **crop_data
            })
            
            doc.insert(ignore_permissions=True)
            created_count += 1
            print(f"Created seasonal calendar for {crop_data['crop_name']}")
            
        except Exception as e:
            print(f"Error creating {crop_data['crop_name']}: {str(e)}")
    
    frappe.db.commit()
    
    return {
        "success": True,
        "created": created_count,
        "skipped": skipped_count,
        "total": len(NORWEGIAN_CROPS_DATA),
        "message": f"Created {created_count} seasonal calendar entries, skipped {skipped_count} existing"
    }
