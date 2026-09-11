# 🌾 Kisan Web Project - 3D Smart Agricultural Operating System

A production-ready full-stack web application designed for the agricultural ecosystem, combining modern 3D WebGL UI visual elements, Tailwind CSS glassmorphism, Python Flask modular architecture, and PostgreSQL relational database persistence.

---

## 🏗️ Architecture & Technology Stack

- **Frontend & 3D Layer**:
  - **HTML5 & Vanilla ES6+ JavaScript**: Lightweight, reactive client execution without heavy framework bloat.
  - **Tailwind CSS (JIT/CDN)**: Responsive layouts, custom agricultural gradients, dark theme, and high-performance utilities.
  - **Three.js & WebGL**: Interactive 3D Earth globe with localized agricultural markers, glowing atmospheric Fresnel shaders, ambient floating golden bio-spores/wheat pollen particle cloud, and procedural swaying 3D crop stalks.
  - **CSS3D & Vanilla 3D Tilt Engine**: Card hover perspective rotation with dynamic specular glare highlights.
  - **Lucide Icons**: Crisp vector UI iconography.

- **Backend Layer (Python Flask)**:
  - **Modular Blueprint Structure**: Separation of concerns across Authentication, Seasonal Crops, Weather, AI Plant Pathology, Community, Agricultural Machinery, and Government Schemes.
  - **Flask-SQLAlchemy & Flask-Migrate**: Relational ORM supporting PostgreSQL in production and zero-config SQLite development fallback.
  - **Flask-JWT-Extended & Sessions**: Dual-mode stateless JWT bearer tokens for REST APIs and secure session cookies for web requests.
  - **Pillow (PIL)**: Server-side digital image processing and feature extraction for crop leaf scans.

- **Database (PostgreSQL)**:
  - Relational schema covering Users (Multi-role: Farmer, Buyer, Admin), Seasonal Crops, DiseaseLogs, WeatherCache, CommunityPosts, Schemes, and AgriculturalTools.

---

## 📁 File & Directory Structure

```
d:\Kisan\
├── app.py                      # Application factory, CLI commands (init-db, seed-db), server entry point
├── config.py                   # Configuration for PostgreSQL URI, JWT secrets, and file upload limits
├── extensions.py               # Extension instances (db, migrate, jwt)
├── models.py                   # Full SQLAlchemy PostgreSQL schema (Users, Crops, DiseaseLogs, etc.)
├── seed_data.py                # Database seeder with realistic Indian agricultural and scheme data
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment variables for PostgreSQL connection
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py          # User registration, login (JWT + session), verified farmer directory
│   ├── crop_routes.py          # Seasonal crop cycles, step-by-step workflows, smart geo-recommendation
│   ├── weather_routes.py       # Geolocation weather query, Open-Meteo integration, 7-day forecast cache
│   ├── ai_routes.py            # Crop image upload, pathology classification, remedies, YouTube fix tutorials
│   ├── community_routes.py     # Farmer social feed, posts with media upload, likes counter
│   ├── tools_routes.py         # Modern agricultural machinery specs, subsidy data, 3D video demos
│   └── schemes_routes.py       # Government schemes, Kisan loan portals, PM-KISAN, KCC, PM-KUSUM
├── static/
│   ├── css/
│   │   └── custom.css          # Glassmorphism, 3D card perspective, glow effects, laser scanner animation
│   ├── js/
│   │   ├── three_hero.js       # Three.js 3D Earth globe, agricultural pins, golden bio-spores & 3D crop model
│   │   ├── tilt3d.js           # 3D perspective mouse tilt engine with specular glare
│   │   ├── weather.js          # Auto-geolocation (HTML5 + IP fallback), Open-Meteo 7-day forecast
│   │   ├── ai_diagnostics.js   # Leaf image dropzone, scanner animation, diagnostic report & YouTube player
│   │   ├── carousel3d.js       # 3D cylindrical animated showcase carousel for machinery demos
│   │   ├── community.js        # Community feed interactions, new post modal, verified farmer directory
│   │   └── app.js              # Tab filters, crop lifecycle roadmap modal, smart recommendation engine, auth
│   └── uploads/                # User uploaded crop scans and community post attachments
└── templates/
    └── index.html              # Master single-page application interface
```

---

## 🗄️ PostgreSQL Database Schema (`models.py`)

1. **`User`**:
   - `id`, `name`, `email`, `password_hash`, `role` (`farmer`, `buyer`, `admin`), `phone`, `state`, `district`, `latitude`, `longitude`, `farm_size_acres`, `primary_crops`, `avatar_url`, `is_verified`, `created_at`.
2. **`Crop`**:
   - `id`, `name`, `scientific_name`, `season` (`summer`, `kharif`, `rabi`, `zaid`), `ideal_temp_min`, `ideal_temp_max`, `ideal_rainfall_min`, `ideal_rainfall_max`, `soil_type`, `growth_duration_days`, `workflow_steps_json`, `hybrid_varieties`, `youtube_tutorial_id`, `image_url`, `estimated_yield_per_acre`, `market_price_range`.
3. **`DiseaseLog`**:
   - `id`, `user_id`, `crop_name`, `image_path`, `disease_name`, `confidence`, `severity` (`Low`, `Medium`, `High`, `Critical`), `symptoms_json`, `organic_treatment`, `chemical_treatment`, `youtube_tutorial_id`, `created_at`.
4. **`WeatherCache`**:
   - `id`, `location_name`, `latitude`, `longitude`, `temperature`, `humidity`, `rainfall_probability`, `weather_condition`, `wind_speed_kmh`, `forecast_json`, `fetched_at`.
5. **`CommunityPost`**:
   - `id`, `user_id`, `author_name`, `author_location`, `title`, `content`, `category` (`growth_update`, `query`, `harvest`, `machinery`), `media_url`, `likes_count`, `comments_count`, `created_at`.
6. **`Scheme`**:
   - `id`, `title`, `category` (`central_gov`, `bank_loan`, `subsidy`, `insurance`), `provider_name`, `description`, `eligibility`, `benefits`, `interest_rate_subsidy`, `application_url`, `badge_label`.
7. **`AgriculturalTool`**:
   - `id`, `name`, `category` (`drone`, `harvester`, `irrigation`, `tractor`), `specs_json`, `price_range`, `subsidy_available`, `video_demo_url`, `image_url`, `model_3d_identifier`, `description`.

---

## 🌐 RESTful API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register user with multi-role support & profile data |
| `POST` | `/api/auth/login` | Authenticate user, issue JWT token & session |
| `GET` | `/api/auth/me` | Fetch currently logged-in user profile |
| `GET` | `/api/auth/farmers` | Public directory of verified local farmers with filters |
| `GET` | `/api/crops` | List seasonal crops (`?season=kharif\|rabi\|zaid\|summer`) |
| `GET` | `/api/crops/<id>` | Full crop details with step-by-step lifecycle workflow |
| `POST` | `/api/crops/recommend` | Geo/climate recommendation engine matching temp/soil |
| `GET` | `/api/weather/current` | Real-time weather & 7-day forecast via Open-Meteo |
| `POST` | `/api/ai/diagnose` | Multipart leaf image upload, AI pathology analysis, symptoms & remedy video |
| `GET` | `/api/ai/history` | Historical disease scan records |
| `GET` | `/api/community/posts` | Paginated social feed filtered by category |
| `POST` | `/api/community/posts` | Create new post with optional field photo attachment |
| `POST` | `/api/community/posts/<id>/like` | Increment like counter |
| `GET` | `/api/tools` | Modern machinery catalog with specs & video demos |
| `GET` | `/api/schemes` | Official government schemes & loan portals |

---

## 🚀 Quickstart & Setup Guide

### 1. Installation & Environment Setup
```powershell
cd d:\Kisan
pip install -r requirements.txt
```

### 2. Configure Database
- **SQLite (Default Zero-Config)**: The application automatically initializes `kisan.db` if `DATABASE_URL` is omitted.
- **PostgreSQL**: Set the environment variable in `.env` or your shell:
  ```powershell
  $env:DATABASE_URL="postgresql://postgres:password@localhost:5432/kisan_db"
  ```

### 3. Initialize & Seed Database
```powershell
python seed_data.py
```

### 4. Launch the Web Application
```powershell
python app.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🌟 Key User Experience Features
- **Interactive 3D Earth Globe**: Move the mouse across the hero to orbit the agricultural globe, inspect glowing regional breadbasket markers, and watch golden bio-spores drift with real-time parallax.
- **AI Leaf Scanner**: Drag and drop any crop photo to view laser scanning animation, confidence percentages, severity indicators, and curated YouTube remediation videos.
- **7-Day Weather**: Auto-detects GPS coordinates or regional IP and renders daily temperatures, rain probability bars, and farming advisories.
- **Seasonal Roadmap**: Click "View Step-by-Step Farming Roadmap" on any crop to open an interactive timeline from seed bed preparation to harvest storage.
- **Farmer Social Network**: Publish questions or yield reports with image attachments and connect directly with verified producers.
