"""
GESNER DESLANDES REAL ESTATE PLATFORM
Listing Aggregator · Built by Gesner Deslandes

IMPORTANT LEGAL NOTICE:
This platform is an information aggregator only. Gesner Deslandes is NOT a
licensed real estate broker and does NOT collect commissions or referral fees
for real estate transactions. All property listings are sourced from public
data providers. Users must contact property owners or licensed agents directly.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gesner Deslandes Real Estate Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CONTACT & LEGAL CONSTANTS
# ─────────────────────────────────────────────────────────────
CONTACT_PHONE = "(509)-47385663"
CONTACT_EMAIL = "deslandes78@gmail.com"
TAPTAP_LINK   = "http://bit.ly/TTSBrazil"

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: #0a0f1a;
        color: #eaf1ff;
    }
    h1, h2, h3 { color: #ffd93b !important; }
    .main-title {
        font-family: Georgia, serif;
        font-size: 2.4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ffd93b, #ff9f00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #8fa9d1;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.85rem;
        margin-bottom: 4px;
    }
    .contact-bar {
        text-align: center;
        padding: 12px;
        background: rgba(255,217,59,0.10);
        border: 2px solid rgba(255,217,59,0.45);
        border-radius: 14px;
        margin-bottom: 18px;
        font-weight: 900;
        color: #ffe680;
    }
    .contact-bar a {
        color: #ffd93b;
        text-decoration: none;
        border-bottom: 1px dotted #ffd93b;
        margin: 0 10px;
    }
    .legal-box {
        padding: 16px 20px;
        border-radius: 12px;
        background: rgba(255,95,86,0.08);
        border: 2px solid rgba(255,95,86,0.45);
        color: #ffbcb8;
        font-size: 0.82rem;
        line-height: 1.6;
        margin-bottom: 18px;
    }
    .legal-box b { color: #ff5f56; }
    .listing-card {
        border-radius: 14px;
        padding: 18px 16px;
        background: linear-gradient(180deg, rgba(20,30,52,0.95), rgba(12,18,32,0.95));
        border: 2px solid rgba(148,163,255,0.22);
        margin-bottom: 14px;
    }
    .listing-price {
        font-family: 'Courier New', monospace;
        font-size: 1.4rem;
        font-weight: 900;
        color: #ffd93b;
    }
    .listing-addr {
        font-size: 1rem;
        font-weight: 800;
        color: #eaf1ff;
        margin: 6px 0;
    }
    .listing-detail {
        font-size: 0.82rem;
        color: #8fa9d1;
        font-weight: 700;
    }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        background: rgba(58,160,255,0.14);
        border: 1px solid rgba(58,160,255,0.45);
        color: #bcd9ff;
        font-size: 0.66rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 2px;
    }
    .tag-rent { background: rgba(61,220,132,0.14); border-color: rgba(61,220,132,0.5); color: #a8f5c9; }
    .tag-sale { background: rgba(255,159,67,0.14); border-color: rgba(255,159,67,0.5); color: #ffc98e; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="subtitle">Rentals · Purchases · Live US Listings</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">GESNER DESLANDES REAL ESTATE PLATFORM</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="contact-bar">'
    f'📞 <a href="tel:+50947385663">{CONTACT_PHONE}</a>'
    f'&nbsp;&nbsp;✉️ <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
    f'</div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# LEGAL DISCLAIMER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="legal-box">
<b>⚖️ LEGAL NOTICE — PLEASE READ</b><br><br>
This platform is an <b>information aggregator only</b>. Gesner Deslandes is
<b>NOT</b> a licensed real estate broker or agent. This platform does
<b>NOT</b> collect commissions, referral fees, or any form of compensation
from property owners or buyers for real estate transactions.<br><br>
All property listings are sourced from publicly available data providers.
Users must contact property owners or licensed agents directly. Any
financial support sent via the Tap Tap Send link below is a
<b>voluntary tip</b> and is not a condition of viewing or contacting any
property owner.<br><br>
If you are a licensed broker and wish to enter into a formal referral
agreement, please contact us directly to discuss a compliant arrangement.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR — SEARCH FILTERS
# ─────────────────────────────────────────────────────────────
st.sidebar.markdown("### 🔎 Search Filters")

listing_type = st.sidebar.radio(
    "Listing type",
    ["For Rent", "For Sale"],
    index=0,
)

city = st.sidebar.text_input("City", value="Miami")
state = st.sidebar.text_input("State (2-letter code)", value="FL")

col1, col2 = st.sidebar.columns(2)
with col1:
    price_min = st.number_input("Min price ($)", min_value=0, value=0, step=10000)
with col2:
    price_max = st.number_input("Max price ($)", min_value=0, value=2000000, step=10000)

col3, col4 = st.sidebar.columns(2)
with col3:
    beds_min = st.number_input("Min beds", min_value=0, value=1, step=1)
with col4:
    baths_min = st.number_input("Min baths", min_value=0, value=1, step=1)

radius = st.sidebar.slider("Search radius (miles)", 1, 50, 10)

st.sidebar.markdown("---")

use_live = st.sidebar.checkbox(
    "Fetch live listings (requires API key)",
    value=False,
    help="If unchecked, the app shows demo listings so you can test the interface.",
)

# ─────────────────────────────────────────────────────────────
# DATA FETCHING
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_rentcast(listing_type, city, state, price_min, price_max, beds_min, baths_min):
    """Fetch listings from RentCast API."""
    api_key = st.secrets.get("RENTCAST_API_KEY", None)
    if not api_key:
        return None

    endpoint = (
        "https://api.rentcast.io/v1/listings/rental/long-term"
        if listing_type == "For Rent"
        else "https://api.rentcast.io/v1/listings/sale"
    )

    headers = {"X-Api-Key": api_key, "Accept": "application/json"}
    params = {
        "city": city,
        "state": state,
        "limit": 50,
        "status": "Active",
    }
    if listing_type == "For Sale":
        params["priceMin"] = price_min
        params["priceMax"] = price_max
    params["bedroomsMin"] = beds_min
    params["bathroomsMin"] = baths_min

    try:
        r = requests.get(endpoint, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def demo_listings(listing_type, city, state):
    """Demo data so the app works without an API key."""
    if listing_type == "For Rent":
        return [
            {"addressLine1": f"1200 Brickell Ave #{i}", "city": city, "state": state,
             "zipCode": "33131", "price": p, "bedrooms": b, "bathrooms": ba,
             "squareFootage": sf, "propertyType": "Apartment",
             "listingType": "For Rent", "listedDate": "2025-09-01", "id": f"R{i}"}
            for i, (p, b, ba, sf) in enumerate([
                (2200, 1, 1, 720), (2900, 2, 2, 1050),
                (3400, 2, 2, 1180), (4200, 3, 2, 1420),
                (5100, 3, 3, 1750), (6800, 4, 3, 2100),
            ])
        ]
    else:
        return [
            {"addressLine1": f"88 Ocean Drive #{i}", "city": city, "state": state,
             "zipCode": "33139", "price": p, "bedrooms": b, "bathrooms": ba,
             "squareFootage": sf, "propertyType": "Single Family",
             "listingType": "For Sale", "listedDate": "2025-09-01", "id": f"S{i}"}
            for i, (p, b, ba, sf) in enumerate([
                (285000, 2, 2, 1100), (420000, 3, 2, 1450),
                (575000, 3, 3, 1800), (720000, 4, 3, 2200),
                (950000, 4, 4, 2800), (1250000, 5, 4, 3400),
            ])
        ]


if use_live:
    with st.spinner("Fetching live listings…"):
        raw = fetch_rentcast(listing_type, city, state, price_min, price_max, beds_min, baths_min)
    if raw is None:
        st.warning("⚠️ No API key found. Add `RENTCAST_API_KEY` to Streamlit secrets, or uncheck 'Fetch live listings'.")
        listings = demo_listings(listing_type, city, state)
    else:
        listings = raw
else:
    listings = demo_listings(listing_type, city, state)

# ─────────────────────────────────────────────────────────────
# DISPLAY LISTINGS
# ─────────────────────────────────────────────────────────────
st.markdown(f"### 🏘️ {len(listings)} {listing_type.lower()} listings in {city}, {state}")

if not listings:
    st.info("No listings found. Try widening your search.")
else:
    for i, listing in enumerate(listings):
        addr = listing.get("addressLine1", "Address unavailable")
        price = listing.get("price", 0)
        beds = listing.get("bedrooms", "—")
        baths = listing.get("bathrooms", "—")
        sqft = listing.get("squareFootage", "—")
        ptype = listing.get("propertyType", "Property")
        zipc = listing.get("zipCode", "")
        cityn = listing.get("city", city)
        staten = listing.get("state", state)
        listed = listing.get("listedDate", "—")

        price_fmt = f"${price:,.0f}" + ("/mo" if listing_type == "For Rent" else "")

        with st.container():
            st.markdown(f"""
            <div class="listing-card">
                <span class="tag {'tag-rent' if listing_type == 'For Rent' else 'tag-sale'}">{ptype}</span>
                <span class="tag">{listing_type}</span>
                <div class="listing-price">{price_fmt}</div>
                <div class="listing-addr">📍 {addr}, {cityn}, {staten} {zipc}</div>
                <div class="listing-detail">
                    🛏️ {beds} beds &nbsp;·&nbsp; 🛁 {baths} baths &nbsp;·&nbsp;
                    📐 {sqft} sqft &nbsp;·&nbsp; 📅 Listed {listed}
                </div>
                <div style="margin-top:10px;">
                    <a href="sms:?&body=Hi,%20I%20saw%20your%20listing%20on%20Gesner%20Deslandes%20Real%20Estate%20Platform.%20I%20am%20interested%20in%20{addr.replace(' ', '%20')}.%20Please%20contact%20me%20at%20{CONTACT_PHONE}."
                       style="display:inline-block;padding:10px 18px;border-radius:10px;
                              background:linear-gradient(135deg,#ffd93b,#ff9f00);color:#1a1000;
                              font-weight:900;text-decoration:none;font-size:0.8rem;
                              letter-spacing:1px;text-transform:uppercase;">
                       📱 Contact Owner
                    </a>
                    <a href="mailto:{CONTACT_EMAIL}?subject=Interest%20in%20{addr.replace(' ', '%20')}"
                       style="display:inline-block;padding:10px 18px;border-radius:10px;
                              background:rgba(58,160,255,0.14);color:#bcd9ff;
                              border:2px solid rgba(58,160,255,0.45);
                              font-weight:900;text-decoration:none;font-size:0.8rem;
                              letter-spacing:1px;text-transform:uppercase;margin-left:6px;">
                       ✉️ Email
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SUMMARY CHART
# ─────────────────────────────────────────────────────────────
if listings:
    st.markdown("---")
    st.markdown("### 📊 Price Distribution")
    df = pd.DataFrame(listings)
    if "price" in df.columns:
        fig = px.histogram(
            df, x="price", nbins=12,
            color_discrete_sequence=["#ffd93b"],
            labels={"price": "Price ($)"},
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#eaf1ff",
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# SUPPORT SECTION (voluntary, disclosed)
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💛 Support This Platform (Optional)")
st.markdown("""
This platform is **free to use**. If you found it helpful and would like to
support its continued development, you may send a **voluntary contribution**
via Tap Tap Send. This is **not** a commission, referral fee, or condition
of any property transaction.
""")
st.markdown(
    f'<a href="{TAPTAP_LINK}" target="_blank" '
    f'style="display:inline-block;padding:14px 28px;border-radius:12px;'
    f'background:linear-gradient(135deg,#3ddc84,#1a8a4a);color:#fff;'
    f'font-weight:900;text-decoration:none;font-size:0.9rem;'
    f'letter-spacing:1.5px;text-transform:uppercase;">'
    f'💚 Send a Voluntary Tip via Tap Tap Send</a>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#8fa9d1;font-size:0.8rem;line-height:1.8;">
    <b style="color:#ffd93b;">GESNER DESLANDES REAL ESTATE PLATFORM</b><br>
    Built by Gesner Deslandes · Software Engineer<br>
    📞 {CONTACT_PHONE} &nbsp;·&nbsp; ✉️ {CONTACT_EMAIL}<br>
    <span style="font-size:0.7rem;">
    This platform is an information aggregator. Not a licensed real estate brokerage.
    No commissions or referral fees are collected. All listings are sourced from
    public data providers and are subject to change without notice.
    </span>
</div>
""", unsafe_allow_html=True)
