import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #fdf0ff 50%, #fff7f0 100%);
        color: #1a1a2e;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f5f0ff 100%);
        border-right: 2px solid #e0d4ff;
        box-shadow: 4px 0 20px rgba(124,58,237,0.08);
    }

    h1, h2, h3 {
        font-family: 'Nunito', sans-serif;
        color: #1a1a2e;
    }

    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        background-size: 200% auto;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.65rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(245,87,108,0.35);
        animation: gradientShift 3s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(245,87,108,0.5);
    }

    .card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #ede9fe;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(124,58,237,0.08);
    }

    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #f5576c 100%);
        border-radius: 24px;
        padding: 2.2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 12px 40px rgba(102,126,234,0.4);
        animation: pulseGlow 2s ease-in-out infinite;
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 12px 40px rgba(102,126,234,0.4); }
        50% { box-shadow: 0 16px 50px rgba(240,147,251,0.5); }
    }

    .price-amount {
        font-family: 'Nunito', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        text-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }

    .price-label {
        font-size: 0.95rem;
        opacity: 0.9;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.1rem;
        text-align: center;
        border: 2px solid #ede9fe;
        box-shadow: 0 4px 15px rgba(124,58,237,0.08);
        transition: transform 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(124,58,237,0.15);
    }

    .ai-advisor-box {
        background: linear-gradient(135deg, #ffffff 0%, #fdf4ff 100%);
        border-radius: 20px;
        padding: 1.8rem;
        border-left: 5px solid #f093fb;
        border-top: 1px solid #f3e8ff;
        border-right: 1px solid #f3e8ff;
        border-bottom: 1px solid #f3e8ff;
        line-height: 2;
        color: #2d1b69;
        font-size: 0.96rem;
        box-shadow: 0 4px 20px rgba(240,147,251,0.12);
    }

    .section-title {
        font-family: 'Nunito', sans-serif;
        font-size: 1.3rem;
        font-weight: 800;
        color: #4c1d95;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .future-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #f093fb);
        color: white;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        font-size: 0.82rem;
        font-weight: 700;
        margin: 0.25rem;
        box-shadow: 0 3px 10px rgba(102,126,234,0.3);
    }

    [data-testid="stNumberInput"] input {
        background: #faf5ff;
        color: #1a1a2e;
        border: 2px solid #e9d5ff;
        border-radius: 10px;
    }

    [data-testid="stNumberInput"] input:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 3px rgba(168,85,247,0.15);
    }

    .stSuccess > div {
        background: linear-gradient(135deg, #d1fae5, #ecfdf5);
        border: 1px solid #6ee7b7;
        border-radius: 12px;
        color: #065f46;
        font-weight: 500;
    }

    .stInfo > div {
        background: linear-gradient(135deg, #ede9fe, #f5f3ff);
        border: 1px solid #c4b5fd;
        border-radius: 12px;
        color: #4c1d95;
        font-weight: 500;
    }

    .stWarning > div {
        background: linear-gradient(135deg, #fef3c7, #fffbeb);
        border: 1px solid #fcd34d;
        border-radius: 12px;
        color: #92400e;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 16px;
        padding: 5px;
        gap: 4px;
        border: 2px solid #ede9fe;
        box-shadow: 0 2px 10px rgba(124,58,237,0.08);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: #6b21a8;
        font-weight: 600;
        font-family: 'Nunito', sans-serif;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(102,126,234,0.35) !important;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        border: 2px solid #ede9fe;
        box-shadow: 0 3px 12px rgba(124,58,237,0.07);
    }

    div[data-testid="stMetric"] label {
        color: #7c3aed !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    st.error("❌ Model not found! Run train.py first.")
    st.stop()

# ---------------- SESSION STATE ----------------
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "price_per_sqft" not in st.session_state:
    st.session_state.price_per_sqft = None
if "ai_advice" not in st.session_state:
    st.session_state.ai_advice = None
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

# ---------------- LOCATION DATA ----------------
CITY_DATA = {
    "Mumbai": {
        "areas": ["Andheri", "Bandra", "Powai", "Thane", "Navi Mumbai", "Borivali", "Dadar", "Juhu"],
        "base_multiplier": 2.5
    },
    "Delhi": {
        "areas": ["Dwarka", "Rohini", "Saket", "Lajpat Nagar", "Noida Sector 62", "Greater Noida", "Vasant Kunj", "Janakpuri"],
        "base_multiplier": 2.0
    },
    "Bangalore": {
        "areas": ["Whitefield", "Koramangala", "HSR Layout", "Indiranagar", "Electronic City", "Marathahalli", "BTM Layout", "Sarjapur"],
        "base_multiplier": 1.9
    },
    "Hyderabad": {
        "areas": ["Gachibowli", "Kondapur", "Madhapur", "Banjara Hills", "Jubilee Hills", "Miyapur", "Kukatpally", "LB Nagar"],
        "base_multiplier": 1.6
    },
    "Pune": {
        "areas": ["Hinjewadi", "Kothrud", "Wakad", "Baner", "Hadapsar", "Viman Nagar", "Kharadi", "Pimpri"],
        "base_multiplier": 1.5
    },
    "Chennai": {
        "areas": ["OMR", "Anna Nagar", "Velachery", "Porur", "Tambaram", "Sholinganallur", "Adyar", "T Nagar"],
        "base_multiplier": 1.4
    },
    "Kolkata": {
        "areas": ["Salt Lake", "New Town", "Jadavpur", "Ballygunge", "Park Street", "Dum Dum", "Behala", "Howrah"],
        "base_multiplier": 1.2
    },
    "Ahmedabad": {
        "areas": ["Satellite", "Prahlad Nagar", "Bopal", "Thaltej", "Maninagar", "Gota", "Vastrapur", "Navrangpura"],
        "base_multiplier": 1.1
    },
    "Jaipur": {
        "areas": ["Malviya Nagar", "Vaishali Nagar", "Mansarovar", "Jagatpura", "Tonk Road", "Ajmer Road", "C-Scheme", "Pratap Nagar"],
        "base_multiplier": 1.0
    },
    "Chandigarh": {
        "areas": ["Sector 17", "Sector 22", "Sector 35", "Mohali", "Panchkula", "Zirakpur", "Sector 43", "Sector 9"],
        "base_multiplier": 1.1
    },
    "Ludhiana": {
        "areas": ["Model Town", "BRS Nagar", "Sarabha Nagar", "Civil Lines", "Dugri", "Pakhowal Road", "Ferozepur Road", "Rajguru Nagar"],
        "base_multiplier": 0.9
    },
    "Lucknow": {
        "areas": ["Gomti Nagar", "Hazratganj", "Aliganj", "Indira Nagar", "Alambagh", "Chinhat", "Mahanagar", "Vibhuti Khand"],
        "base_multiplier": 0.95
    },
}

AMENITIES_DATA = {
    "Andheri": {"schools": ["Ryan International", "Bombay Scottish"], "hospitals": ["Kokilaben Hospital", "Criticare Asia"], "metro": ["Andheri Metro Station"], "malls": ["Infiniti Mall", "Mega Mall"], "parks": ["Joggers Park", "Millat Nagar Garden"]},
    "Bandra": {"schools": ["St. Stanislaus", "Holy Family"], "hospitals": ["Lilavati Hospital", "Holy Family Hospital"], "metro": ["Bandra Station"], "malls": ["Linking Road Market", "Hill Road Market"], "parks": ["Bandra Reclamation", "Carter Road Promenade"]},
    "Whitefield": {"schools": ["Inventure Academy", "DPS Whitefield"], "hospitals": ["Manipal Hospital", "Columbia Asia"], "metro": ["Whitefield Metro"], "malls": ["Phoenix Marketcity", "VR Bengaluru"], "parks": ["ITPL Park", "Whitefield Lake"]},
    "Koramangala": {"schools": ["DPS Koramangala", "Bishop Cotton"], "hospitals": ["Fortis Hospital", "Sakra World Hospital"], "metro": ["Silk Board Metro"], "malls": ["Forum Mall", "1 MG Mall"], "parks": ["Koramangala Park", "Sony World Signal Park"]},
    "Gachibowli": {"schools": ["Oakridge International", "DPS Miyapur"], "hospitals": ["KIMS Hospital", "Rainbow Hospital"], "metro": ["Raidurg Metro"], "malls": ["Inorbit Mall", "Sarath City Capital Mall"], "parks": ["Durgam Cheruvu", "KBR Park"]},
    "Hinjewadi": {"schools": ["Indus International", "Vibgyor High"], "hospitals": ["Sahyadri Hospital", "Lifepoint Hospital"], "metro": ["Hinjewadi Phase 1 Metro"], "malls": ["Xion Mall", "Westend Mall"], "parks": ["Hinjewadi Lake", "Pimpri Chinchwad Garden"]},
    "Salt Lake": {"schools": ["DPS Ruby Park", "South Point School"], "hospitals": ["Fortis Anandapur", "AMRI Hospital"], "metro": ["Salt Lake Sector V Metro"], "malls": ["City Centre 1", "City Centre 2"], "parks": ["Central Park Salt Lake", "Eco Park"]},
    "Model Town": {"schools": ["Sacred Heart Convent", "DAV Public School"], "hospitals": ["Dayanand Medical College", "Fortis Hospital"], "metro": ["N/A - Bus Rapid Transit"], "malls": ["MBD Neopolis Mall", "Westend Mall"], "parks": ["Rose Garden", "Model Town Park"]},
    "Gomti Nagar": {"schools": ["City Montessori School", "DPS Lucknow"], "hospitals": ["Medanta Hospital", "Sahara Hospital"], "metro": ["Gomti Nagar Metro"], "malls": ["Phoenix Palassio", "Fun Republic Mall"], "parks": ["Gomti Riverfront Park", "Janeshwar Mishra Park"]},
    "Sector 17": {"schools": ["St. John's High School", "Bhavan Vidyalaya"], "hospitals": ["PGI Chandigarh", "Fortis Hospital"], "metro": ["N/A - Bus network"], "malls": ["Elante Mall", "DLF City Centre"], "parks": ["Rose Garden", "Leisure Valley"]},
    "DEFAULT": {"schools": ["Local Government School", "Private School Nearby"], "hospitals": ["District Hospital", "Private Clinic"], "metro": ["Bus Stand Nearby"], "malls": ["Local Market"], "parks": ["Community Park"]},
}

def get_amenities(city, area):
    return AMENITIES_DATA.get(area, AMENITIES_DATA["DEFAULT"])

def get_locality_score(city, area, amenities):
    score = 0
    score += min(len(amenities.get("schools", [])) * 15, 20)
    score += min(len(amenities.get("hospitals", [])) * 15, 20)
    metro = amenities.get("metro", [])
    score += 20 if metro and "N/A" not in metro[0] else 8
    score += min(len(amenities.get("malls", [])) * 10, 20)
    score += min(len(amenities.get("parks", [])) * 10, 20)
    return min(score, 100)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<div style='font-family:Nunito,sans-serif;font-size:1.4rem;font-weight:900;color:#4c1d95;margin-bottom:0.3rem'>🏠 Price Predictor</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#7c3aed;font-size:0.85rem;margin-bottom:1rem;font-weight:500'>✨ Smart Real Estate Analysis</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📍 Location")
    selected_city = st.selectbox("🏙️ City", list(CITY_DATA.keys()), index=0)
    selected_area = st.selectbox("📌 Locality / Area", CITY_DATA[selected_city]["areas"])

    st.markdown("### 📥 Property Details")
    area = st.number_input("📏 Area (sq ft)", min_value=300, step=50, value=1000)
    bedrooms = st.number_input("🛏 Bedrooms", min_value=1, value=2)
    bath = st.number_input("🛁 Bathrooms", min_value=1, value=2)
    balcony = st.number_input("🌇 Balconies", min_value=0, value=1)

    st.markdown("---")

    if st.button("🚀 Predict Price", key="predict_btn"):
        try:
            features = np.array([[area, bath, balcony]])
            prediction = model.predict(features)
            st.session_state.prediction = round(abs(prediction[0]), 2)
            st.session_state.price_per_sqft = round(st.session_state.prediction * 100000 / area, 0)
            st.session_state.ai_advice = None  # reset AI advice on new prediction
            st.session_state.inputs = {
                "area": area, "bedrooms": bedrooms,
                "bath": bath, "balcony": balcony,
                "city": selected_city, "locality": selected_area
            }
        except Exception as e:
            st.error(f"❌ Error: {e}")

    st.markdown("---")
    st.markdown("### 📊 Property Summary")
    attached = min(bedrooms, bath)
    common = max(0, bedrooms - bath)
    st.info(f"🚿 Attached Bathrooms: {attached}")
    st.info(f"🚽 Common Bathrooms: {common}")
    if bath > bedrooms:
        st.warning("⚠️ Bathrooms > Bedrooms")
    st.success("✔ Model: Random Forest")
    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit + Claude AI")


# ---------------- RULE-BASED ADVISOR ----------------
def generate_rule_based_advice(area, bedrooms, bathrooms, balconies, price, price_per_sqft):
    tips = []

    # 1. Price Fairness
    tips.append("<b>💰 Price Fairness</b>")
    if price_per_sqft < 3000:
        tips.append("✅ Price per sq ft is <b>below ₹3,000</b> — this is quite affordable, likely a Tier-2/3 city or outskirts location. Great entry-level investment.")
    elif price_per_sqft < 6000:
        tips.append("✅ Price per sq ft is in the <b>₹3,000–₹6,000</b> range — fair for most Tier-2 cities like Jaipur, Lucknow, or Chandigarh.")
    elif price_per_sqft < 10000:
        tips.append("⚠️ Price per sq ft is <b>₹6,000–₹10,000</b> — typical for Tier-1 suburbs like Pune, Hyderabad outskirts, or Noida. Verify with local market rates.")
    else:
        tips.append("🔴 Price per sq ft exceeds <b>₹10,000</b> — premium segment. Suitable for metro prime areas (Mumbai, Bangalore, Delhi). Negotiate hard.")

    # 2. Configuration Pros
    tips.append("<br><b>🏡 Property Pros</b>")
    if bedrooms >= 3:
        tips.append("✅ <b>3+ BHK</b> — great for families, high resale demand.")
    if bathrooms >= bedrooms:
        tips.append("✅ Bathrooms match or exceed bedrooms — <b>attached baths</b> add daily comfort and resale value.")
    if balconies >= 2:
        tips.append("✅ Multiple balconies — adds <b>ventilation, light</b>, and lifestyle appeal.")
    if area > 1500:
        tips.append("✅ Spacious layout — <b>above 1500 sq ft</b> gives room to breathe and future flexibility.")
    if area < 800:
        tips.append("✅ Compact size — <b>lower maintenance cost</b> and easier to rent out.")

    # 3. Concerns
    tips.append("<br><b>⚠️ Things to Check Before Buying</b>")
    if bathrooms > bedrooms:
        tips.append("⚠️ More bathrooms than bedrooms — ensure layout isn't awkward. Ask for the floor plan.")
    if balconies == 0:
        tips.append("⚠️ No balcony — check for adequate <b>natural light and ventilation</b> in the unit.")
    if area < 600:
        tips.append("⚠️ Very small unit — verify <b>ceiling height and storage</b> space before finalising.")
    if price > 150:
        tips.append("⚠️ High-value property — get a <b>legal title check</b> and bank valuation done independently.")
    tips.append("⚠️ Always verify <b>RERA registration</b>, builder track record, and possession timeline.")

    # 4. Negotiation Tips
    tips.append("<br><b>💡 Negotiation Tips</b>")
    tips.append("💡 Ask for <b>free car parking, modular kitchen, or white goods</b> instead of price cut — easier for builder to agree.")
    if price > 80:
        tips.append("💡 For this budget, negotiate a <b>5–8% discount</b> on base price or stamp duty waiver.")
    tips.append("💡 Compare at least <b>3 similar properties</b> nearby before making an offer — use that data as leverage.")
    tips.append("💡 Check if GST is included in the quoted price — for under-construction homes it adds <b>5% extra</b>.")

    # 5. Ideal Buyer
    tips.append("<br><b>🌟 Ideal For</b>")
    if bedrooms == 1:
        tips.append("🌟 Best for <b>singles, young professionals, or investors</b> looking to rent out.")
    elif bedrooms == 2:
        tips.append("🌟 Perfect for <b>couples or small families</b> (2–3 members).")
    elif bedrooms == 3:
        tips.append("🌟 Ideal for <b>nuclear families of 4–5</b> — the sweet spot in Indian real estate.")
    else:
        tips.append("🌟 Suited for <b>large joint families or HNIs</b> wanting spacious living.")

    # EMI hint
    emi = round((price * 100000 * 0.009), 0)
    tips.append(f"<br>📊 <b>Rough EMI Estimate:</b> ₹{emi:,.0f}/month (20yr loan @ ~9% p.a. on full value)")

    return "<br>".join(tips)

# ---------------- FLOOR PLAN GENERATOR ----------------
def generate_floor_plan(area, bedrooms, bathrooms, balconies):
    W, H = 700, 500
    svg_parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="background:#faf5ff;border-radius:16px;border:2px solid #e9d5ff">']
    svg_parts.append('<defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e9d5ff" stroke-width="0.5"/></pattern></defs>')
    svg_parts.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

    # Title
    svg_parts.append(f'<text x="20" y="30" font-family="Syne,sans-serif" font-size="16" fill="#7c3aed" font-weight="700">Floor Plan — {area} sq ft | {bedrooms}BHK</text>')

    rooms = []
    # Living room — always large, bottom left
    rooms.append({"label": "Living Room", "x": 30, "y": 60, "w": 200, "h": 150, "color": "#ede9fe", "border": "#7c3aed"})
    # Kitchen — top left
    rooms.append({"label": "Kitchen", "x": 30, "y": 220, "w": 130, "h": 120, "color": "#dbeafe", "border": "#4f46e5"})

    # Bedrooms — right side
    bed_x = 250
    bed_y = 60
    bw = 180
    bh = max(80, min(140, int(300 / max(bedrooms, 1))))
    for i in range(bedrooms):
        label = "Master Bedroom" if i == 0 else f"Bedroom {i+1}"
        rooms.append({"label": label, "x": bed_x, "y": bed_y + i * (bh + 10), "w": bw, "h": bh, "color": "#d1fae5", "border": "#10b981"})

    # Bathrooms — beside kitchen
    bath_x = 170
    bath_y = 220
    for i in range(min(bathrooms, 3)):
        rooms.append({"label": f"Bath {i+1}", "x": bath_x, "y": bath_y + i * 60, "w": 70, "h": 50, "color": "#cffafe", "border": "#06b6d4"})

    # Balconies — far right
    for i in range(min(balconies, 2)):
        rooms.append({"label": f"Balcony {i+1}", "x": 450, "y": 60 + i * 90, "w": 100, "h": 70, "color": "#fef3c7", "border": "#f59e0b", "dashed": True})

    # Hallway
    rooms.append({"label": "Hallway", "x": 240, "y": 220, "w": 60, "h": 120, "color": "#f3f4f6", "border": "#9ca3af"})

    for r in rooms:
        dashed = r.get("dashed", False)
        dash_attr = 'stroke-dasharray="8,4"' if dashed else ''
        svg_parts.append(f'<rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" rx="6" fill="{r["color"]}" stroke="{r["border"]}" stroke-width="2" {dash_attr}/>')
        cx = r["x"] + r["w"] // 2
        cy = r["y"] + r["h"] // 2
        svg_parts.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" font-family="DM Sans,sans-serif" font-size="11" fill="#1e1b4b" font-weight="700">{r["label"]}</text>')

    # Legend
    svg_parts.append('<rect x="30" y="420" width="640" height="60" rx="10" fill="#ffffff" opacity="0.97"/>')
    legend = [("Bedroom", "#10b981"), ("Bathroom", "#06b6d4"), ("Living", "#7c3aed"), ("Kitchen", "#4f46e5"), ("Balcony", "#f59e0b")]
    for i, (lbl, clr) in enumerate(legend):
        lx = 50 + i * 130
        svg_parts.append(f'<rect x="{lx}" y="435" width="14" height="14" rx="3" fill="{clr}"/>')
        svg_parts.append(f'<text x="{lx+20}" y="447" font-family="DM Sans,sans-serif" font-size="11" fill="#4c1d95">{lbl}</text>')

    svg_parts.append("</svg>")
    return "".join(svg_parts)

# ---------------- FUTURE PRICE ----------------
def get_future_prices(base_price, years_list, annual_growth=0.08):
    return [round(base_price * ((1 + annual_growth) ** y), 2) for y in years_list]


# ---------------- MAIN ----------------
st.markdown("<h1 style='font-family:Nunito,sans-serif;font-size:2.4rem;margin-bottom:0;background:linear-gradient(135deg,#667eea,#f093fb,#f5576c);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>🏠 House Price Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b21a8;margin-bottom:1.5rem;font-weight:500'>Fill in property details in the sidebar and click <b>Predict Price</b> to get started.</p>", unsafe_allow_html=True)
st.markdown("---")

if st.session_state.prediction:
    pred = st.session_state.prediction
    inp = st.session_state.inputs

    # Price Card
    st.markdown(f"""
    <div class="price-card">
        <div class="price-label">Estimated Property Value</div>
        <div class="price-amount">₹ {pred} Lakhs</div>
        <div class="price-label">≈ ₹ {st.session_state.price_per_sqft:,.0f} per sq ft</div>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📏 Area", f"{inp['area']} sq ft")
    with col2:
        st.metric("🛏 Bedrooms", inp['bedrooms'])
    with col3:
        st.metric("🛁 Bathrooms", inp['bath'])
    with col4:
        st.metric("🌇 Balconies", inp['balcony'])

    st.markdown("---")

    # TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Price Analysis", "📸 Floor Plan", "🔮 Future Prices", "📍 Location & Amenities"])

    # ---------- TAB 1: PRICE ANALYSIS + AI ADVISOR ----------
    with tab1:
        st.markdown('<div class="section-title">📈 Price vs Area Chart</div>', unsafe_allow_html=True)
        areas = list(range(500, 5001, 250))
        prices = []
        for a in areas:
            f = np.array([[a, inp['bath'], inp['balcony']]])
            p = model.predict(f)
            prices.append(round(abs(p[0]), 2))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=areas, y=prices, mode='lines+markers', name='Predicted Price',
            line=dict(color='#667eea', width=3),
            marker=dict(size=5, color='#f093fb'),
            fill='tozeroy', fillcolor='rgba(102,126,234,0.12)'
        ))
        fig.add_trace(go.Scatter(
            x=[inp['area']], y=[pred], mode='markers', name='Your Property',
            marker=dict(size=14, color='#f59e0b', symbol='star')
        ))
        fig.update_layout(
            paper_bgcolor='white', plot_bgcolor='#faf5ff',
            xaxis=dict(title='Area (sq ft)', gridcolor='#e9d5ff', color='#4c1d95'),
            yaxis=dict(title='Price (Lakhs)', gridcolor='#e9d5ff', color='#4c1d95'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(color='#4c1d95')),
            height=380, margin=dict(l=20, r=20, t=40, b=20),
            font=dict(color='#4c1d95')
        )
        st.plotly_chart(fig, use_container_width=True)

        # Price Range
        st.markdown('<div class="section-title">💡 Price Range Estimate</div>', unsafe_allow_html=True)
        low = round(pred * 0.9, 2)
        high = round(pred * 1.1, 2)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div style="color:#ef4444;font-size:0.8rem;font-weight:700">LOW ESTIMATE</div><div style="font-size:1.5rem;font-weight:800;color:#1a1a2e;font-family:Nunito,sans-serif">₹ {low}L</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card" style="border-color:#7c3aed"><div style="color:#a78bfa;font-size:0.8rem;font-weight:700">PREDICTED</div><div style="font-size:1.5rem;font-weight:800;color:#1a1a2e;font-family:Nunito,sans-serif">₹ {pred}L</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div style="color:#10b981;font-size:0.8rem;font-weight:700">HIGH ESTIMATE</div><div style="font-size:1.5rem;font-weight:800;color:#1a1a2e;font-family:Nunito,sans-serif">₹ {high}L</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # 🧠 AI PROPERTY ADVISOR
        st.markdown('<div class="section-title">🧠 AI Property Advisor</div>', unsafe_allow_html=True)

        if st.button("✨ Get Property Analysis & Tips"):
            st.session_state.ai_advice = generate_rule_based_advice(
                inp['area'], inp['bedrooms'], inp['bath'], inp['balcony'], pred, st.session_state.price_per_sqft
            )

        if st.session_state.ai_advice:
            st.markdown(f'<div class="ai-advisor-box">{st.session_state.ai_advice}</div>', unsafe_allow_html=True)

    # ---------- TAB 2: FLOOR PLAN ----------
    with tab2:
        st.markdown('<div class="section-title">📸 Auto-Generated Floor Plan</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#6b21a8;font-size:0.9rem'>Schematic layout based on your inputs — {inp['area']} sq ft, {inp['bedrooms']}BHK, {inp['bath']} Bath, {inp['balcony']} Balcony</p>", unsafe_allow_html=True)

        floor_svg = generate_floor_plan(inp['area'], inp['bedrooms'], inp['bath'], inp['balcony'])
        st.markdown(floor_svg, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:1rem;padding:1rem;background:white;border-radius:12px;border:1px solid #e9d5ff;color:#6b21a8;font-size:0.85rem'>
        📌 <b style='color:#a78bfa'>Note:</b> This is a schematic representation for planning purposes. Actual layout may vary based on construction design.
        </div>
        """, unsafe_allow_html=True)

    # ---------- TAB 3: FUTURE PRICES ----------
    with tab3:
        st.markdown('<div class="section-title">🔮 Future Price Prediction</div>', unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([2, 1])
        with col_r2:
            growth_rate = st.slider("Annual Growth Rate (%)", min_value=3, max_value=15, value=8, step=1)

        years = list(range(0, 11))
        future_prices = get_future_prices(pred, years, annual_growth=growth_rate / 100)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=years, y=future_prices, mode='lines+markers',
            name='Projected Price',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=8, color='#f59e0b'),
            fill='tozeroy', fillcolor='rgba(245,158,11,0.08)'
        ))
        fig2.add_trace(go.Scatter(
            x=[5], y=[future_prices[5]], mode='markers',
            name='5-Year Mark',
            marker=dict(size=14, color='#10b981', symbol='diamond')
        ))
        fig2.add_trace(go.Scatter(
            x=[10], y=[future_prices[10]], mode='markers',
            name='10-Year Mark',
            marker=dict(size=14, color='#7c3aed', symbol='star')
        ))
        fig2.update_layout(
            paper_bgcolor='white', plot_bgcolor='#fff7f0',
            xaxis=dict(title='Years from Now', gridcolor='#fde8d8', color='#92400e', tickvals=list(range(11))),
            yaxis=dict(title='Price (Lakhs)', gridcolor='#fde8d8', color='#92400e'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(color='#92400e')),
            height=380, margin=dict(l=20, r=20, t=40, b=20),
            font=dict(color='#92400e')
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Milestone Cards
        milestones = [1, 3, 5, 7, 10]
        cols = st.columns(len(milestones))
        for i, y in enumerate(milestones):
            fp = future_prices[y]
            gain = round(fp - pred, 2)
            gain_pct = round((gain / pred) * 100, 1)
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card" style="border-color:#2a2a4a">
                    <div style="color:#7c3aed;font-size:0.75rem;font-weight:700">YEAR {y}</div>
                    <div style="font-size:1.2rem;font-weight:800;color:#1a1a2e;font-family:Nunito,sans-serif">₹{fp}L</div>
                    <div style="color:#059669;font-size:0.78rem;margin-top:0.3rem">+{gain_pct}% (₹{gain}L gain)</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='margin-top:1.5rem;padding:1rem 1.5rem;background:#1a1a24;border-radius:12px;border:1px solid #2a2a3a;color:#9090b0;font-size:0.85rem'>
        📌 <b style='color:#f59e0b'>Assumptions:</b> Compound annual growth rate of <b style='color:#f0f0ff'>{growth_rate}%</b> applied.
        India's average real estate appreciation is typically 7–12% p.a. in metro areas. Adjust the slider above to model different scenarios.
        </div>
        """, unsafe_allow_html=True)

    # ---------- TAB 4: LOCATION & AMENITIES ----------
    with tab4:
        city = inp.get("city", list(CITY_DATA.keys())[0])
        locality = inp.get("locality", CITY_DATA[city]["areas"][0])
        amenities = get_amenities(city, locality)
        loc_score = get_locality_score(city, locality, amenities)

        st.markdown(f'<div class="section-title">📍 {locality}, {city}</div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1, 2])
        with col_g1:
            if loc_score >= 80:
                score_color = "#10b981"; score_label = "Excellent! 🌟"
            elif loc_score >= 60:
                score_color = "#f59e0b"; score_label = "Good Area 👍"
            elif loc_score >= 40:
                score_color = "#f97316"; score_label = "Average 🙂"
            else:
                score_color = "#ef4444"; score_label = "Developing 🏗️"

            st.markdown(f"""
            <div style="background:white;border-radius:20px;padding:1.5rem;text-align:center;border:2px solid #ede9fe;box-shadow:0 4px 20px rgba(124,58,237,0.1)">
                <div style="font-size:0.85rem;color:#7c3aed;font-weight:700;margin-bottom:0.5rem">LOCALITY SCORE</div>
                <div style="font-size:4rem;font-weight:900;color:{score_color};font-family:Nunito,sans-serif;line-height:1">{loc_score}</div>
                <div style="font-size:0.75rem;color:#6b7280;margin-top:0.2rem">out of 100</div>
                <div style="background:{score_color}22;color:{score_color};border-radius:10px;padding:0.3rem 0.8rem;font-size:0.82rem;font-weight:700;margin-top:0.8rem;display:inline-block">{score_label}</div>
                <div style="background:#f3f4f6;border-radius:10px;height:10px;margin-top:1rem;overflow:hidden">
                    <div style="background:{score_color};width:{loc_score}%;height:100%;border-radius:10px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_g2:
            multiplier = CITY_DATA[city]["base_multiplier"]
            adj_price = round(inp["area"] * multiplier * 0.045, 2)
            tier = "Tier-1 Metro 🏙️" if multiplier >= 1.8 else "Tier-2 City 🌆" if multiplier >= 1.2 else "Tier-3 City 🏘️"
            appreciation = "10–14%" if multiplier >= 1.8 else "7–10%" if multiplier >= 1.2 else "5–8%"
            price_range = "₹8,000–20,000" if multiplier >= 1.8 else "₹4,000–8,000" if multiplier >= 1.2 else "₹2,500–5,000"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#667eea,#f093fb);border-radius:20px;padding:1.5rem;color:white;margin-bottom:1rem;box-shadow:0 6px 20px rgba(102,126,234,0.3)">
                <div style="font-size:0.85rem;opacity:0.9;font-weight:600">📊 Location-Adjusted Price</div>
                <div style="font-size:2.2rem;font-weight:900;font-family:Nunito,sans-serif">₹ {adj_price} Lakhs</div>
                <div style="font-size:0.8rem;opacity:0.8">Based on {city} market ({multiplier}x multiplier)</div>
            </div>
            <div style="background:white;border-radius:16px;padding:1.2rem;border:2px solid #ede9fe;font-size:0.88rem;color:#4c1d95;line-height:2">
                🏙️ <b>{city}</b> is a <b>{tier}</b><br>
                📈 Avg appreciation: <b>{appreciation}</b> per year<br>
                🏠 Avg price/sqft: <b>{price_range}</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">🏫 Nearby Amenities</div>', unsafe_allow_html=True)

        cat_config = {
            "schools":   ("🏫", "Schools",   "#dbeafe", "#3b82f6"),
            "hospitals": ("🏥", "Hospitals",  "#fce7f3", "#ec4899"),
            "metro":     ("🚇", "Transit",    "#fef3c7", "#f59e0b"),
            "malls":     ("🛍️", "Shopping",   "#ede9fe", "#7c3aed"),
            "parks":     ("🌳", "Parks",      "#d1fae5", "#10b981"),
        }

        cols = st.columns(5)
        for i, (cat, (icon, label, bg, fg)) in enumerate(cat_config.items()):
            items = amenities.get(cat, ["Not available nearby"])
            with cols[i]:
                items_html = "".join([
                    f'<div style="font-size:0.76rem;padding:0.25rem 0;border-bottom:1px solid {bg};color:#374151;word-break:break-word">• {item}</div>'
                    for item in items
                ])
                st.markdown(f"""
                <div style="background:{bg};border-radius:16px;padding:1rem;border:2px solid {fg}44;min-height:160px">
                    <div style="font-size:1.6rem;text-align:center">{icon}</div>
                    <div style="font-size:0.78rem;font-weight:800;color:{fg};text-align:center;margin-bottom:0.5rem">{label.upper()}</div>
                    {items_html}
                    <div style="background:{fg};color:white;border-radius:8px;padding:0.25rem;text-align:center;font-size:0.75rem;font-weight:700;margin-top:0.6rem">{len(items)} Nearby</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">💡 Location Insights</div>', unsafe_allow_html=True)

        has_metro = bool(amenities.get("metro")) and "N/A" not in amenities["metro"][0]
        insights = []
        if has_metro:
            insights.append(("✅", "#10b981", f"<b>Metro connected</b> — {amenities['metro'][0]} nearby. Boosts resale value by 15–20%."))
        else:
            insights.append(("⚠️", "#f59e0b", "<b>No metro nearby</b> — check bus/auto availability. May affect resale value slightly."))
        if len(amenities.get("schools", [])) >= 2:
            insights.append(("✅", "#3b82f6", f"<b>{len(amenities['schools'])} schools nearby</b> — great for families with children."))
        if amenities.get("hospitals"):
            insights.append(("✅", "#ec4899", f"<b>Hospital accessible</b> — {amenities['hospitals'][0]} is nearby. Important for emergencies."))
        if amenities.get("parks"):
            insights.append(("✅", "#10b981", "<b>Green spaces available</b> — adds to lifestyle quality and property appeal."))
        if loc_score >= 70:
            insights.append(("🌟", "#7c3aed", "<b>High-demand locality</b> — property likely to appreciate faster than city average."))
        elif loc_score < 50:
            insights.append(("🏗️", "#f97316", "<b>Developing area</b> — lower entry price. Watch for upcoming infrastructure projects."))

        for emoji, color, text in insights:
            st.markdown(f'<div style="background:white;border-radius:12px;padding:0.9rem 1.2rem;margin-bottom:0.5rem;border-left:4px solid {color};border-top:1px solid #ede9fe;border-right:1px solid #ede9fe;border-bottom:1px solid #ede9fe;color:#374151;font-size:0.9rem">{emoji} {text}</div>', unsafe_allow_html=True)


else:
    st.markdown("""
    <div style='text-align:center;padding:5rem 2rem;color:#3a3a5a'>
        <div style='font-size:5rem'>🏠</div>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;margin-top:1.2rem;font-weight:700;color:#4c1d95'>Enter property details in the sidebar</div>
        <div style='font-size:0.95rem;margin-top:0.5rem'>and click <b style="color:#f093fb">Predict Price</b> to unlock all features</div>
        <div style='margin-top:2rem;display:flex;justify-content:center;gap:0.5rem;flex-wrap:wrap'>
            <span class='future-badge'>🧠 AI Advisor</span>
            <span class='future-badge'>📸 Floor Plan</span>
            <span class='future-badge'>🔮 Future Prices</span>
            <span class='future-badge'>📈 Price Chart</span>
            <span class='future-badge'>📍 Location & Amenities</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("💡 Tip: Bigger area & better facilities increase price • Powered by Random Forest + Claude AI")