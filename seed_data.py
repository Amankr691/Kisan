"""
Kisan Web Project - Comprehensive Database Seeder
Populates initial verified farmers, seasonal crops with farming workflows,
government schemes, modern agricultural tools, and community posts.
"""
from extensions import db
from models import User, Crop, Scheme, AgriculturalTool, CommunityPost

def seed_database():
    """Seed sample data if tables are empty."""
    db.create_all()
    print("[*] Checking and seeding initial Kisan Web Project data...")

    # 1. Seed Users (Admin, Agro-Experts, Verified Farmers)
    if User.query.count() == 0:
        print("  -> Seeding verified farmers & system users...")
        users_data = [
            {
                'name': 'Dr. Ramesh Chandra (Agro-Scientist)',
                'email': 'expert@kisan.org',
                'role': 'admin',
                'phone': '+91 98765 43210',
                'state': 'New Delhi',
                'district': 'IARI Pusa',
                'farm_size_acres': 0.0,
                'primary_crops': 'All Indian Agro-Climates',
                'is_verified': True,
                'password': 'AdminPassword2026!'
            },
            {
                'name': 'Sardar Gurpreet Singh',
                'email': 'gurpreet.farm@gmail.com',
                'role': 'farmer',
                'phone': '+91 94172 88390',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'farm_size_acres': 24.5,
                'primary_crops': 'Wheat (HD-3086), Basmati Rice (PB-1121)',
                'is_verified': True,
                'password': 'FarmerPassword123'
            },
            {
                'name': 'Rajendra Patidar',
                'email': 'rajendra.patidar@gmail.com',
                'role': 'farmer',
                'phone': '+91 98260 11244',
                'state': 'Madhya Pradesh',
                'district': 'Indore',
                'farm_size_acres': 18.0,
                'primary_crops': 'Soybean, Yellow Mustard, Wheat',
                'is_verified': True,
                'password': 'FarmerPassword123'
            },
            {
                'name': 'Kavita Devi',
                'email': 'kavita.agri@gmail.com',
                'role': 'farmer',
                'phone': '+91 97188 55432',
                'state': 'Uttar Pradesh',
                'district': 'Varanasi',
                'farm_size_acres': 7.5,
                'primary_crops': 'Vegetables, Hybrid Tomato, Chilli',
                'is_verified': True,
                'password': 'FarmerPassword123'
            },
            {
                'name': 'Mallikarjun Patil',
                'email': 'patil.farm@karnataka.in',
                'role': 'farmer',
                'phone': '+91 99001 23456',
                'state': 'Karnataka',
                'district': 'Dharwad',
                'farm_size_acres': 14.0,
                'primary_crops': 'Cotton, Maize, Sunflower',
                'is_verified': True,
                'password': 'FarmerPassword123'
            }
        ]

        for u_dict in users_data:
            pwd = u_dict.pop('password')
            u = User(**u_dict)
            u.set_password(pwd)
            db.session.add(u)
        db.session.commit()

    # 2. Seed Seasonal Crops
    if Crop.query.count() == 0:
        print("  -> Seeding seasonal crops and step-by-step farming workflows...")
        crops_data = [
            {
                'name': 'Wheat (Kanak)',
                'scientific_name': 'Triticum aestivum',
                'season': 'rabi',
                'crop_category': 'cereal',
                'growth_duration_days': 135,
                'ideal_temp_min': 12.0,
                'ideal_temp_max': 24.0,
                'ideal_rainfall_min': 35.0,
                'ideal_rainfall_max': 75.0,
                'soil_type': 'Well-drained fertile Loamy or Clay Loam',
                'ph_min': 6.0,
                'ph_max': 7.5,
                'hybrid_varieties': 'HD-2967, PBW-550, DBW-187, HD-3086 (Pusa Gautami)',
                'youtube_tutorial_id': '7_0vU_vjIeM',
                'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=800&q=80',
                'estimated_yield_per_acre': '22 - 28 Quintals',
                'market_price_range': '₹2,275 - ₹2,550 per Quintal (MSP)',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Land & Seed Bed Preparation',
                        'desc': 'Deep ploughing followed by 2 cross harrowings and planking to create fine tilt. Apply 10 tonnes well-rotted FYM/compost per acre.',
                        'timing': 'October - November'
                    },
                    {
                        'step': 2,
                        'title': 'Certified Seed Treatment',
                        'desc': 'Treat seeds with Vitavax or Thiram @ 2.5g/kg seed + Azotobacter bio-culture to prevent loose smut and enhance nitrogen fixation.',
                        'timing': 'Before Sowing'
                    },
                    {
                        'step': 3,
                        'title': 'Precision Sowing (Zero Till / Seed Drill)',
                        'desc': 'Sow at 20-22 cm row spacing with 4-5 cm depth using 40 kg certified seeds per acre for optimal tiller count.',
                        'timing': 'First Fortnight of November'
                    },
                    {
                        'step': 4,
                        'title': 'CRI (Crown Root Initiation) Critical Irrigation',
                        'desc': 'Apply 1st light irrigation at 20-25 days after sowing (CRI stage) along with first top dressing of urea (45 kg/acre).',
                        'timing': 'Day 21 - 25'
                    },
                    {
                        'step': 5,
                        'title': 'Weed Management & Foliar Nutrition',
                        'desc': 'Spray Clodinafop-propargyl for Phalaris minor grassy weeds at 30-35 DAS. Foliar spray 13:00:45 potassium nitrate at flag leaf stage.',
                        'timing': 'Day 35 - 75'
                    },
                    {
                        'step': 6,
                        'title': 'Harvesting & Safe Storage',
                        'desc': 'Harvest when grains become hard and moisture drops below 14%. Thresh and store in airtight silos with neem leaves.',
                        'timing': 'March - April'
                    }
                ]
            },
            {
                'name': 'Paddy / Basmati Rice (Dhan)',
                'scientific_name': 'Oryza sativa',
                'season': 'kharif',
                'crop_category': 'cereal',
                'growth_duration_days': 125,
                'ideal_temp_min': 22.0,
                'ideal_temp_max': 35.0,
                'ideal_rainfall_min': 150.0,
                'ideal_rainfall_max': 300.0,
                'soil_type': 'Heavy Clayey or Silty Clay Soils capable of water retention',
                'ph_min': 5.5,
                'ph_max': 7.0,
                'hybrid_varieties': 'Pusa Basmati 1121, Pusa 1509, PR-126, Arize 6444 Gold',
                'youtube_tutorial_id': '8mCqN_vC51I',
                'image_url': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1073&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                'estimated_yield_per_acre': '24 - 32 Quintals (Paddy), 18 - 22 (Basmati)',
                'market_price_range': '₹2,300 - ₹4,200 per Quintal',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Nursery Bed Sowing (DSR / Wet Nursery)',
                        'desc': 'Raise healthy nursery in raised beds. Treat seeds with Carbendazim (2g/kg) and soak for 24 hours before broadcast.',
                        'timing': 'May 20 - June 15'
                    },
                    {
                        'step': 2,
                        'title': 'Field Puddling & Basal Fertilizer',
                        'desc': 'Plough standing water twice to create impervious hardpan. Apply full P & K and 1/3 Nitrogen with 10 kg Zinc Sulphate.',
                        'timing': 'Mid June'
                    },
                    {
                        'step': 3,
                        'title': 'Transplanting (2-3 Seedlings per Hill)',
                        'desc': 'Transplant 22-25 days old seedlings at 20x15 cm spacing. Maintain 2-3 cm shallow water layer during early rooting.',
                        'timing': 'Late June - Early July'
                    },
                    {
                        'step': 4,
                        'title': 'Intermittent Water Regime (AWD)',
                        'desc': 'Alternate wetting and drying saves 30% water and aerates root zone. Apply remaining split urea at maximum tillering.',
                        'timing': 'Day 30 - 60'
                    },
                    {
                        'step': 5,
                        'title': 'Blast & Brown Planthopper Guard',
                        'desc': 'Monitor leaf collar and tillers. Apply Tricyclazole 75 WP at panicle emergence if leaf blast spots appear.',
                        'timing': 'Panicle Stage'
                    },
                    {
                        'step': 6,
                        'title': 'Drain Water & Combine Harvesting',
                        'desc': 'Drain standing water 10-12 days before harvest. Harvest when 85% grains turn golden straw color.',
                        'timing': 'October - November'
                    }
                ]
            },
            {
                'name': 'Hybrid Tomato (Tamatar)',
                'scientific_name': 'Solanum lycopersicum',
                'season': 'zaid',
                'crop_category': 'vegetable',
                'growth_duration_days': 110,
                'ideal_temp_min': 18.0,
                'ideal_temp_max': 30.0,
                'ideal_rainfall_min': 40.0,
                'ideal_rainfall_max': 100.0,
                'soil_type': 'Rich sandy loam with good organic matter',
                'ph_min': 6.0,
                'ph_max': 7.0,
                'hybrid_varieties': 'Syngenta Abhinav, Seminis US-440, NS-501, Arka Rakshak',
                'youtube_tutorial_id': 'b1hPjLhNlZc',
                'image_url': 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80',
                'estimated_yield_per_acre': '250 - 350 Quintals (High Yielding)',
                'market_price_range': '₹1,500 - ₹3,500 per Quintal',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Pro-Tray Nursery Raising',
                        'desc': 'Grow seeds in 98-cavity pro-trays with sterilized coco-peat and vermicompost inside insect-proof net house.',
                        'timing': 'January or August'
                    },
                    {
                        'step': 2,
                        'title': 'Raised Bed & Silver-Black Mulching',
                        'desc': 'Form 3-ft wide raised beds. Lay 25-micron silver-black plastic mulch with inline 16mm drip lateral irrigation lines.',
                        'timing': 'Day 25'
                    },
                    {
                        'step': 3,
                        'title': 'Transplanting & Drenching',
                        'desc': 'Plant at 50 cm intra-plant spacing. Drench root zone with Humic acid + Carbendazim to foster white roots.',
                        'timing': 'Day 30'
                    },
                    {
                        'step': 4,
                        'title': 'Trella / Bamboo Staking',
                        'desc': 'Support indeterminate tomato plants with nylon twine and bamboo poles to keep fruit off moist soil and improve airflow.',
                        'timing': 'Day 45'
                    },
                    {
                        'step': 5,
                        'title': 'Drip Fertigation & Calcium Spray',
                        'desc': 'Inject water-soluble 19:19:19 and Calcium Nitrate via venturi to prevent blossom end rot and produce firm fruit.',
                        'timing': 'Day 45 - 90'
                    },
                    {
                        'step': 6,
                        'title': 'Harvesting at Breaker Stage',
                        'desc': 'Pick fruit at breaker or pink stage for distant markets and red ripe for local mandis. Grade uniformly.',
                        'timing': 'Day 75 - 120'
                    }
                ]
            },
            {
                'name': 'Yellow Mustard (Sarson)',
                'scientific_name': 'Brassica juncea',
                'season': 'rabi',
                'crop_category': 'oilseed',
                'growth_duration_days': 115,
                'ideal_temp_min': 15.0,
                'ideal_temp_max': 25.0,
                'ideal_rainfall_min': 20.0,
                'ideal_rainfall_max': 60.0,
                'soil_type': 'Light to heavy sandy loam, tolerant to mild salinity',
                'ph_min': 6.5,
                'ph_max': 8.0,
                'hybrid_varieties': 'Pusa Bold, Pioneer 45S46, RH-749, Kranti, Giriraj',
                'youtube_tutorial_id': '8mCqN_vC51I',
                'image_url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=800&q=80',
                'estimated_yield_per_acre': '8 - 12 Quintals',
                'market_price_range': '₹5,450 - ₹6,000 per Quintal',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Conserving Residual Soil Moisture',
                        'desc': 'Field preparation immediately after Kharif crop harvest. Conserve sub-surface moisture with gentle planking.',
                        'timing': 'Early October'
                    },
                    {
                        'step': 2,
                        'title': 'Seed Rate & Spacing',
                        'desc': 'Sow 1.5 - 2.0 kg seed per acre at 30 cm row spacing. Thin seedlings to 10-15 cm within rows at 15-20 DAS.',
                        'timing': 'October 10 - 25'
                    },
                    {
                        'step': 3,
                        'title': 'Sulphur & Gypsum Application',
                        'desc': 'Mustard responds sharply to sulphur. Apply 20 kg elemental sulphur or 150 kg gypsum per acre at basal dose.',
                        'timing': 'Basal Dressing'
                    },
                    {
                        'step': 4,
                        'title': 'Flowering & Pod Filling Irrigation',
                        'desc': 'Mustard requires only 2 irrigations: 1st at flower initiation (30-35 DAS) and 2nd at pod filling (60-65 DAS).',
                        'timing': 'Day 35 & 65'
                    },
                    {
                        'step': 5,
                        'title': 'Aphid (Chetpa) Protection',
                        'desc': 'Install yellow sticky traps (15/acre). Spray Dimethoate 30 EC (1.5ml/L) or Neem oil at aphid threshold.',
                        'timing': 'December - January'
                    },
                    {
                        'step': 6,
                        'title': 'Morning Harvesting',
                        'desc': 'Harvest in early morning when pods are yellow to prevent seed shattering. Dry on threshing floor for 4 days.',
                        'timing': 'February - March'
                    }
                ]
            },
            {
                'name': 'Maize / Sweet Corn (Makka)',
                'scientific_name': 'Zea mays',
                'season': 'summer',
                'crop_category': 'cereal',
                'growth_duration_days': 105,
                'ideal_temp_min': 20.0,
                'ideal_temp_max': 32.0,
                'ideal_rainfall_min': 60.0,
                'ideal_rainfall_max': 120.0,
                'soil_type': 'Deep, fertile, well-drained loamy soil',
                'ph_min': 6.0,
                'ph_max': 7.5,
                'hybrid_varieties': 'DKC-9108, Pioneer P3396, Syngenta NK-6240, Sugar 75 (Sweet Corn)',
                'youtube_tutorial_id': '8mCqN_vC51I',
                'image_url': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=800&q=80',
                'estimated_yield_per_acre': '30 - 38 Quintals (Grain)',
                'market_price_range': '₹2,090 - ₹2,400 per Quintal',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Ridge & Furrow Sowing',
                        'desc': 'Sow seeds on the side of ridges at 60 cm row-to-row and 20 cm plant-to-plant spacing for superior drainage.',
                        'timing': 'February - March or June'
                    },
                    {
                        'step': 2,
                        'title': 'Fall Armyworm (FAW) Seed Guard',
                        'desc': 'Treat seed with Fortenza Duo (Cyantraniliprole) to guarantee 21 days systemic protection against Armyworm.',
                        'timing': 'Pre-sowing'
                    },
                    {
                        'step': 3,
                        'title': 'Critical Knee-High Fertigation',
                        'desc': 'Apply 2nd split of urea and zinc sulphate when plants reach knee-high stage (30 DAS).',
                        'timing': 'Day 30'
                    },
                    {
                        'step': 4,
                        'title': 'Tasseling & Silking Moisture Care',
                        'desc': 'Ensure uniform soil moisture during tasseling and silking to secure full kernel pollination and ear filling.',
                        'timing': 'Day 50 - 65'
                    },
                    {
                        'step': 5,
                        'title': 'Cob Harvesting at Black Layer',
                        'desc': 'Sweet corn is harvested at 75% silk drying (milky stage); grain maize when husk leaves dry completely.',
                        'timing': 'Day 90 - 105'
                    }
                ]
            }
        ]

        for c_dict in crops_data:
            steps = c_dict.pop('steps')
            crop = Crop(**c_dict)
            crop.workflow_steps = steps
            db.session.add(crop)
        db.session.commit()

    # 3. Seed Government Schemes
    if Scheme.query.count() == 0:
        print("  -> Seeding government schemes & Kisan credit portals...")
        schemes_data = [
    {
        'title': 'PM-KISAN Samman Nidhi Yojana',
        'category': 'central_gov',
        'provider_name': 'Ministry of Agriculture & Farmers Welfare, Govt. of India',
        'description': 'Central income-support scheme for eligible landholding farmer families across India.',
        'eligibility': 'Eligible landholding farmer families, subject to PM-KISAN exclusion criteria and verification.',
        'benefits': '₹6,000 per year paid directly to the beneficiary bank account in three installments.',
        'interest_rate_subsidy': 'Direct Benefit Transfer (DBT)',
        'application_url': 'https://pmkisan.gov.in/RegistrationFormupdated.aspx',
        'badge_label': '₹6,000 DBT'
    },
    {
        'title': 'Kisan Credit Card (KCC)',
        'category': 'bank_loan',
        'provider_name': 'Ministry of Agriculture & Farmers Welfare / Participating Banks',
        'description': 'Provides timely and flexible institutional credit for cultivation, post-harvest expenses, farm assets and allied agricultural activities.',
        'eligibility': 'Farmers and other eligible agricultural borrowers as per KCC and participating-bank guidelines.',
        'benefits': 'Provides short-term crop credit and other eligible agricultural credit requirements through participating banks.',
        'interest_rate_subsidy': 'Government interest subvention and prompt repayment incentive can reduce eligible short-term crop-loan interest to 4% p.a.',
        'application_url': 'https://www.myscheme.gov.in/schemes/kcc',
        'badge_label': 'Kisan Credit'
    },
    {
        'title': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
        'category': 'insurance',
        'provider_name': 'Ministry of Agriculture & Farmers Welfare',
        'description': 'Crop insurance scheme providing financial protection against eligible crop losses caused by notified natural risks.',
        'eligibility': 'Farmers growing notified crops in notified areas, subject to scheme and state implementation conditions.',
        'benefits': 'Insurance protection against eligible crop losses from notified risks during the crop season.',
        'interest_rate_subsidy': 'Farmer premium is generally capped at 2% for Kharif, 1.5% for Rabi and 5% for annual commercial/horticultural crops.',
        'application_url': 'https://pmfby.gov.in',
        'badge_label': 'Crop Insurance'
    },
    {
        'title': 'PM-KUSUM',
        'category': 'subsidy',
        'provider_name': 'Ministry of New and Renewable Energy (MNRE)',
        'description': 'Supports solar-powered agricultural pumps and solarisation of existing grid-connected agricultural pumps.',
        'eligibility': 'Farmers and other eligible agricultural beneficiaries under applicable PM-KUSUM components and state implementation rules.',
        'benefits': 'Financial assistance for eligible solar agricultural pump and solarisation projects.',
        'interest_rate_subsidy': 'Subsidy structure varies by PM-KUSUM component and state implementation.',
        'application_url': 'https://pmkusum.mnre.gov.in',
        'badge_label': 'Solar Farming'
    },
    {
        'title': 'Sub-Mission on Agricultural Mechanization (SMAM)',
        'category': 'subsidy',
        'provider_name': 'Department of Agriculture & Farmers Welfare',
        'description': 'Promotes farm mechanization and access to agricultural machinery, equipment and Custom Hiring Centres.',
        'eligibility': 'Farmers and eligible farmer groups subject to applicable machinery, subsidy and state implementation guidelines.',
        'benefits': 'Financial assistance may be available for eligible farm machinery and mechanization activities.',
        'interest_rate_subsidy': 'Subsidy level varies by machinery, beneficiary category and implementation guidelines.',
        'application_url': 'https://agrimachinery.nic.in',
        'badge_label': 'Farm Machinery'
    },
    {
        'title': 'Soil Health Card Scheme',
        'category': 'central_gov',
        'provider_name': 'Department of Agriculture & Farmers Welfare',
        'description': 'Provides soil-testing information to help farmers understand soil nutrient status and make better fertilizer and nutrient-management decisions.',
        'eligibility': 'Farmers can access soil-testing and Soil Health Card services through the programme and local agricultural authorities.',
        'benefits': 'Soil nutrient status, fertilizer recommendations and guidance for improving soil health.',
        'interest_rate_subsidy': 'Government-supported soil testing and advisory service.',
        'application_url': 'https://soilhealth.dac.gov.in',
        'badge_label': 'Soil Testing'
    },
    {
        'title': 'e-NAM - National Agriculture Market',
        'category': 'central_gov',
        'provider_name': 'Ministry of Agriculture & Farmers Welfare',
        'description': 'National electronic agricultural-market platform connecting participating mandis to improve market access and transparent price discovery.',
        'eligibility': 'Farmers can participate through registered e-NAM mandis and available farmer registration facilities.',
        'benefits': 'Access to electronic trading, wider market participation and improved price discovery for agricultural produce.',
        'interest_rate_subsidy': 'Digital agricultural marketing platform',
        'application_url': 'https://enam.gov.in/',
        'badge_label': 'Online Mandi'
    },
    {
        'title': 'Agriculture Infrastructure Fund (AIF)',
        'category': 'bank_loan',
        'provider_name': 'Ministry of Agriculture & Farmers Welfare',
        'description': 'Financing facility for eligible agriculture infrastructure and post-harvest management projects.',
        'eligibility': 'Eligible beneficiaries include farmers, farmer groups, FPOs, cooperatives and other approved entities depending on the proposed project.',
        'benefits': 'Eligible projects can receive financing support for agricultural infrastructure and post-harvest facilities.',
        'interest_rate_subsidy': 'Eligible loans can receive interest-subvention support subject to current AIF guidelines.',
        'application_url': 'https://agriinfra.dac.gov.in',
        'badge_label': 'Agri Infrastructure'
    }
]

        for s_dict in schemes_data:
            s = Scheme(**s_dict)
            db.session.add(s)
        db.session.commit()

    # 4. Seed Agricultural Machinery & Tools
    if AgriculturalTool.query.count() == 0:
        print("  -> Seeding agricultural machinery and high-tech tools...")
        tools_data = [
            {
                'name': 'AeroKisan Hexacopter Agri-Drone (10L)',
                'category': 'drone',
                'price_range': '₹4,50,000 - ₹6,00,000',
                'subsidy_available': '50% Subsidy under SMAM Scheme (Up to ₹5 Lakh)',
                'video_demo_url': 'https://www.youtube.com/watch?v=ScMzIvxBSi4',
                'image_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=800&q=80',
                'model_3d_identifier': 'drone_hex',
                'description': 'High-precision crop protection drone equipped with obstacle avoidance radar, RTK centimeter-level positioning, and ultra-low volume electrostatic spray nozzles.',
                'specs': {
                    'Tank Capacity': '10 Liters payload',
                    'Spray Speed': '1 Acre in 6 - 8 Minutes',
                    'Flight Time': '18-22 mins per battery pack',
                    'Nozzles': '4 Centrifugal Atomizing Sprayers',
                    'Coverage': '25-30 Acres per day'
                }
            },
            {
                'name': 'Trimble Dual-Axis Laser Land Leveler',
                'category': 'harvester',
                'price_range': '₹3,20,000 - ₹3,80,000',
                'subsidy_available': '40% State Mechanization Subsidy',
                'video_demo_url': 'https://www.youtube.com/watch?v=J---aiyznGQ',
                'image_url': 'https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=800&q=80',
                'model_3d_identifier': 'laser_leveler',
                'description': 'Precision hydraulic grade-controlled scraper blade paired with a 360-degree rotating laser transmitter. Produces an ultra-flat field surface.',
                'specs': {
                    'Working Width': '2.1 meters (7 ft bucket)',
                    'Leveling Accuracy': '± 2 mm gradient precision',
                    'Water Savings': 'Up to 25% - 30% irrigation saved',
                    'Yield Increment': '8% - 12% uniform germination gain',
                    'Operating Speed': '4 - 6 km/h with 45+ HP tractor'
                }
            },
            {
                'name': 'SmartKisan IoT Solar Drip Fertigation Controller',
                'category': 'irrigation',
                'price_range': '₹45,000 - ₹75,000',
                'subsidy_available': '55% under PMKSY Micro-Irrigation Fund',
                'video_demo_url': 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
                'image_url': 'https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80',
                'model_3d_identifier': 'iot_valves',
                'description': 'Cloud-connected cellular & LoRa controller for solenoid valves, fertilizer venturi injectors, and soil moisture matric tension sensors.',
                'specs': {
                    'Connectivity': '4G LTE + LoRaWAN 868MHz (5km Range)',
                    'Power Source': 'Integrated 20W Solar Panel + LiFePO4 Battery',
                    'Sensor Support': 'Soil VWC, EC, Temp, Pipe Flow Meter',
                    'Mobile App': 'Android / iOS remote valve schedule & alerts'
                }
            },
            {
                'name': 'Kubota Multi-Crop Rubber-Track Mini Combine',
                'category': 'tractor',
                'price_range': '₹14,00,000 - ₹18,50,000',
                'subsidy_available': 'Subsidized custom hiring financing available',
                'video_demo_url': 'https://www.youtube.com/watch?v=fJ9rUzIMcZQ',
                'image_url': 'https://images.unsplash.com/photo-1595246140625-573b715d11dc?auto=format&fit=crop&w=800&q=80',
                'model_3d_identifier': 'mini_combine',
                'description': 'Compact crawler-type combine harvester engineered specifically for wetland paddy fields and terrace farming where conventional wheeled harvesters sink.',
                'specs': {
                    'Engine': '68 HP Water-cooled 4-cylinder Diesel',
                    'Cutter Bar Width': '1.5 - 2.0 meters',
                    'Grain Tank': '1400 Liters with unloading auger',
                    'Ground Pressure': 'Ultra-low 0.18 kgf/cm² (does not bog down)'
                }
            }
        ]

        for t_dict in tools_data:
            specs = t_dict.pop('specs')
            tool = AgriculturalTool(**t_dict)
            tool.specs = specs
            db.session.add(tool)
        db.session.commit()

    # 5. Seed Community Posts
    if CommunityPost.query.count() == 0:
        print("  -> Seeding farmer community updates...")
        sample_author = User.query.filter_by(role='farmer').first()
        author_id = sample_author.id if sample_author else 1
        author_name = sample_author.name if sample_author else 'Sardar Gurpreet Singh'

        posts_data = [
            {
                'user_id': author_id,
                'author_name': author_name,
                'author_location': 'Ludhiana, Punjab',
                'title': 'Zero-Tillage Wheat after Basmati: 3rd Season Results',
                'content': 'We sowed HD-3086 directly using Happy Seeder into heavy rice straw residue without burning any stubble. Germination is extremely uniform and soil moisture was retained for 12 extra days! Highly recommend fellow farmers to stop residue burning.',
                'category': 'growth_update',
                'media_url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=800&q=80',
                'likes_count': 42,
                'comments_count': 11
            },
            {
                'user_id': author_id,
                'author_name': 'Rajendra Patidar',
                'author_location': 'Indore, Madhya Pradesh',
                'title': 'Yellow Mosaic in Soybean: Bio-spray formula that worked',
                'content': 'Noticed early whitefly infestation last week. Instead of harsh organophosphates, we sprayed 5% Neem seed kernel extract (NSKE) + yellow sticky traps (20 per acre). Infestation controlled by 85% within 4 days.',
                'category': 'query',
                'media_url': 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80',
                'likes_count': 28,
                'comments_count': 6
            },
            {
                'user_id': author_id,
                'author_name': 'Kavita Devi',
                'author_location': 'Varanasi, Uttar Pradesh',
                'title': 'Tomato Harvest Yield Update with Silver Mulch & Drip',
                'content': 'Completed our first major flush of Syngenta Abhinav tomatoes today. Yield touched 280 crates from 1.2 acres with pristine fruit quality. The silver mulch completely suppressed weeds and saved our labor costs.',
                'category': 'harvest',
                'media_url': 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80',
                'likes_count': 56,
                'comments_count': 14
            }
        ]

        for p_dict in posts_data:
            p = CommunityPost(**p_dict)
            db.session.add(p)
        db.session.commit()

    print("[OK] Kisan Web Project database successfully seeded!")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()
