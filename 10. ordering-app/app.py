import os
import hashlib
from collections import defaultdict

import streamlit as st

from db import (
    get_customer_by_phone, get_cities, get_zones_by_city,
    get_menu_items, insert_customer, insert_order, insert_order_items,
    get_owner_by_username, get_monthly_stats,
)

# ── Constants ─────────────────────────────────────────────────────────────────
APP_DIR   = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, 'Logo2.png')

SSRS_REPORTS = [
    {'file': 'TOP Selling Items.png',              'title': 'TOP Selling Items'},
    {'file': 'Order & Customer Payment Details.png','title': 'Order & Customer Payment Details'},
    {'file': 'Platform Performance.png',           'title': 'Platform Performance'},
    {'file': 'Competitor Comparison.png',          'title': 'Competitor Comparison'},
    {'file': 'Zone Performance.png',               'title': 'Zone Performance'},
    {'file': 'Customer Profitability.png',         'title': 'Customer Profitability'},
]

DASHBOARDS = [
    {
        'key': 'exec',
        'title': 'EXEC',
        'subtitle': 'Executive & Operations',
        'icon': '📊',
        'url': 'https://app.powerbi.com/view?r=eyJrIjoiOWJkZjBiNmYtZWE2ZC00ZmNmLTk2YjAtZTU0NmU3OTUxMGVjIiwidCI6IjNmNGYyOGVkLTAwNWUtNGI5Ny1hNzJkLWFkNDQ4OWYzMTg1NyJ9',
    },
    {
        'key': 'cod',
        'title': 'COD',
        'subtitle': 'COD & Zones',
        'icon': '🚚',
        'url': 'https://app.powerbi.com/view?r=eyJrIjoiYWUwZDFkOTEtNTY4NC00NWI4LWEwMDctMzZlZDEzY2Q2NWUzIiwidCI6IjNmNGYyOGVkLTAwNWUtNGI5Ny1hNzJkLWFkNDQ4OWYzMTg1NyJ9',
    },
    {
        'key': 'menu',
        'title': 'MENU',
        'subtitle': 'Menu & Ingredients',
        'icon': '🍽️',
        'url': 'https://app.powerbi.com/view?r=eyJrIjoiNDhiYjkwZjQtN2FjOS00ZTRjLWFhZjUtMmIzYTg0MmFhY2VlIiwidCI6IjNmNGYyOGVkLTAwNWUtNGI5Ny1hNzJkLWFkNDQ4OWYzMTg1NyJ9',
    },
    {
        'key': 'customer',
        'title': 'CUSTOMER',
        'subtitle': 'Customers',
        'icon': '👥',
        'url': 'https://app.powerbi.com/view?r=eyJrIjoiMTdlODViZjUtNmIzZS00ZDY5LThiZDMtNDcwNTNmN2M3ZDNiIiwidCI6IjNmNGYyOGVkLTAwNWUtNGI5Ny1hNzJkLWFkNDQ4OWYzMTg1NyJ9',
    },
    {
        'key': 'platforms',
        'title': 'PLATFORMS',
        'subtitle': 'Platforms & Competitors',
        'icon': '📱',
        'url': 'https://public.tableau.com/app/profile/mazen.alasas/viz/Tableau_Dashboards_17794729154820/Dashboard2_PlatformCustomerInsights?publish=yes',  # ← paste the Tableau Public link here when available
    },
]

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FoodFlow",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ─────────────────────────── */
.stApp { background-color: #F8F5F2; direction: rtl; }
[data-testid="stAppViewContainer"] > .main { background-color: #F8F5F2; }

/* ── RTL text ───────────────────────── */
h1,h2,h3,h4,h5,h6,p,label,
.stMarkdown,div[data-testid="stText"] { direction:rtl; text-align:right; }

/* ── LTR inputs ─────────────────────── */
.stTextInput input,
input[type="text"],
input[type="password"] { direction:ltr; text-align:left; border-radius:10px!important; }

/* ── Sidebar ────────────────────────── */
[data-testid="stSidebar"] {
    background-color:#FFFFFF;
    border-left:3px solid #FDBA74;
    direction:rtl;
}
[data-testid="stSidebar"] * { direction:rtl; text-align:right; }

/* ── Primary button ─────────────────── */
.stButton>button[kind="primary"] {
    background:linear-gradient(135deg,#F97316 0%,#EA580C 100%);
    border:none; color:#FFFFFF; font-weight:700;
    border-radius:12px; padding:.65rem 1.5rem; font-size:1rem;
    width:100%; transition:all .25s ease;
    box-shadow:0 2px 8px rgba(249,115,22,.25);
}
.stButton>button[kind="primary"]:hover {
    background:linear-gradient(135deg,#EA580C 0%,#C2410C 100%);
    transform:translateY(-2px);
    box-shadow:0 6px 16px rgba(234,88,12,.4);
}

/* ── Secondary button ───────────────── */
.stButton>button:not([kind="primary"]) {
    border:2px solid #F97316!important; color:#F97316!important;
    border-radius:12px!important; background:transparent!important;
    font-weight:600!important; width:100%; transition:all .2s;
}
.stButton>button:not([kind="primary"]):hover { background:#FFF7ED!important; }

/* ── Link button ────────────────────── */
.stLinkButton a {
    background:linear-gradient(135deg,#F97316,#EA580C)!important;
    color:white!important; border-radius:12px!important;
    font-weight:700!important; border:none!important;
    display:block; text-align:center;
}

/* ── Metric cards ───────────────────── */
[data-testid="stMetric"] {
    background:#FFFFFF; border-radius:12px;
    padding:16px 20px; border:1px solid #FED7AA;
    box-shadow:0 1px 4px rgba(0,0,0,.06);
}
[data-testid="stMetricLabel"]  { color:#6B7280!important; font-size:.8rem!important; text-align:center!important; }
[data-testid="stMetricValue"]  { color:#111827!important; font-weight:700!important; text-align:center!important; }

/* ── Tabs ───────────────────────────── */
.stTabs [data-baseweb="tab-list"] { gap:4px; overflow-x:auto; }
.stTabs [data-baseweb="tab"]      { font-weight:600; color:#6B7280; }
.stTabs [aria-selected="true"]    { color:#F97316!important; border-bottom:3px solid #F97316!important; }

/* ── Number input ───────────────────── */
.stNumberInput { direction:ltr; }
.stNumberInput input { text-align:center; border-radius:8px!important; }

/* ── Divider ────────────────────────── */
hr { border-color:#FED7AA; }

/* ── Mobile ─────────────────────────── */
@media (max-width:768px) {
    section[data-testid="stSidebar"]    { display:none!important; }
    [data-testid="collapsedControl"]    { display:none!important; }
    .stTabs [data-baseweb="tab-list"]   { flex-wrap:nowrap; overflow-x:auto; -webkit-overflow-scrolling:touch; }
}
</style>
""", unsafe_allow_html=True)


# ── Session State Init ────────────────────────────────────────────────────────
def init_state():
    for key, val in {
        'screen': 0, 'phone': '', 'customer': None,
        'order_id': None, 'owner': None,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ── Utilities ─────────────────────────────────────────────────────────────────
def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def show_logo(width=180):
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=width)

@st.cache_data
def load_menu():    return get_menu_items()

@st.cache_data
def load_cities():  return get_cities()

@st.cache_data
def load_zones(city_id: int): return get_zones_by_city(city_id)

def build_cart(menu_items):
    cart = {}
    for item in menu_items:
        qty = st.session_state.get(f"qty_{item['ItemID']}", 0)
        if qty > 0:
            cart[item['ItemID']] = {
                'name_ar':   item['ItemName_AR'],
                'quantity':  qty,
                'price':     item['CurrentPrice_EGP'],
                'prep_time': item['PrepTimeMinutes'],
            }
    return cart

def cart_subtotal(cart):
    return sum(v['quantity'] * v['price'] for v in cart.values())

def estimated_time(cart, customer):
    return max(v['prep_time'] for v in cart.values()) + \
           round(customer['BaseDeliveryMinutes'] * customer['TrafficFactor'])


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 0 — Role Selection
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.screen == 0:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        _, lc, _ = st.columns([1, 2, 1])
        with lc:
            show_logo(width=230)

        st.markdown(
            "<h2 style='text-align:center;color:#111827;margin-top:8px;'>أهلاً بك في FoodFlow</h2>"
            "<p style='text-align:center;color:#6B7280;'>اختار نوع دخولك</p>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                "<div style='background:white;border-radius:18px;padding:30px 20px;"
                "text-align:center;border:2px solid #FED7AA;"
                "box-shadow:0 4px 12px rgba(0,0,0,.08);'>"
                "<div style='font-size:42px;'>🛍️</div>"
                "<div style='font-weight:700;font-size:18px;color:#111827;margin:8px 0 4px;'>أنا عميل</div>"
                "<div style='font-size:13px;color:#6B7280;'>اطلب طعامك</div>"
                "</div>", unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ابدأ الطلب", key="btn_customer", use_container_width=True, type="primary"):
                st.session_state.screen = 1
                st.rerun()

        with c2:
            st.markdown(
                "<div style='background:white;border-radius:18px;padding:30px 20px;"
                "text-align:center;border:2px solid #FED7AA;"
                "box-shadow:0 4px 12px rgba(0,0,0,.08);'>"
                "<div style='font-size:42px;'>📊</div>"
                "<div style='font-weight:700;font-size:18px;color:#111827;margin:8px 0 4px;'>أنا المدير</div>"
                "<div style='font-size:13px;color:#6B7280;'>لوحة التحكم</div>"
                "</div>", unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("دخول المدير", key="btn_owner", use_container_width=True):
                st.session_state.screen = 'owner_login'
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN owner_login — Owner Authentication
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == 'owner_login':
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        _, lc, _ = st.columns([1, 2, 1])
        with lc:
            show_logo(width=150)
        st.markdown("## 🔐 تسجيل دخول المدير")
        st.markdown("---")
        username = st.text_input("اسم المستخدم", placeholder="admin")
        password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← رجوع", use_container_width=True):
                st.session_state.screen = 0
                st.rerun()
        with c2:
            if st.button("دخول 🔓", use_container_width=True, type="primary"):
                if not username or not password:
                    st.error("ادخل اسم المستخدم وكلمة المرور")
                else:
                    owner = get_owner_by_username(username.strip())
                    if owner and owner['PasswordHash'] == hash_password(password):
                        st.session_state.owner = owner
                        st.session_state.screen = 'owner_home'
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غلط")


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN owner_home — Owner Dashboard
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == 'owner_home':
    owner = st.session_state.owner

    # Header
    c_logo, c_title, c_logout = st.columns([1, 5, 1])
    with c_logo:
        show_logo(width=85)
    with c_title:
        st.markdown(
            f"<h3 style='color:#111827;margin:0;padding-top:18px;'>"
            f"أهلاً، <span style='color:#F97316;'>{owner['FullName']}</span> 👋"
            f"<span style='font-size:14px;color:#6B7280;margin-right:12px;'>({owner['Role']})</span>"
            f"</h3>", unsafe_allow_html=True,
        )
    with c_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("خروج 🚪", use_container_width=True):
            st.session_state.owner  = None
            st.session_state.screen = 0
            st.rerun()

    st.markdown("---")

    # ── Monthly Stats ─────────────────────────────────────────────────────────
    with st.spinner("بنحمل الإحصائيات..."):
        stats = get_monthly_stats()

    st.markdown(
        f"<h4 style='color:#1E293B;'>📊 ملخص شهر {stats['Month']}</h4>",
        unsafe_allow_html=True,
    )

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1: st.metric("📦 إجمالي الطلبات",    f"{stats['TotalOrders']:,}")
    with r1c2: st.metric("💰 الإيرادات",          f"{stats['TotalRevenue']:,.0f} ج")
    with r1c3: st.metric("🚫 حالات رفض COD",      f"{stats['CODRefusals']:,}")

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1: st.metric("⚠️ نسبة الرفض",         f"{stats['CODRefusalRate']:.1f}%")
    with r2c2: st.metric("💸 خسائر COD",          f"{stats['TotalRefusedAmount']:,.0f} ج")
    with r2c3: st.metric("🏆 أكثر بلاتفورم",      stats['TopPlatform'])

    st.markdown("---")

    # ── Dashboards ────────────────────────────────────────────────────────────
    st.markdown(
        "<h4 style='color:#1E293B;'>📈 لوحات المعلومات</h4>",
        unsafe_allow_html=True,
    )

    row1 = st.columns(3)
    for i, dash in enumerate(DASHBOARDS[:3]):
        with row1[i]:
            st.markdown(
                f"<div style='background:white;border-radius:14px;padding:18px;"
                f"text-align:center;border:2px solid #FED7AA;"
                f"box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:8px;'>"
                f"<div style='font-size:26px;'>{dash['icon']}</div>"
                f"<div style='font-weight:700;color:#111827;font-size:15px;'>{dash['title']}</div>"
                f"<div style='font-size:11px;color:#6B7280;'>{dash['subtitle']}</div>"
                f"</div>", unsafe_allow_html=True,
            )
            if dash['url']:
                st.link_button("فتح الداشبورد ↗", dash['url'], use_container_width=True)
            else:
                st.button("قريباً ⏳", key=f"dash_{dash['key']}", use_container_width=True, disabled=True)

    row2_cols = st.columns(3)
    for i, dash in enumerate(DASHBOARDS[3:]):
        with row2_cols[i]:
            st.markdown(
                f"<div style='background:white;border-radius:14px;padding:18px;"
                f"text-align:center;border:2px solid #FED7AA;"
                f"box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:8px;'>"
                f"<div style='font-size:26px;'>{dash['icon']}</div>"
                f"<div style='font-weight:700;color:#111827;font-size:15px;'>{dash['title']}</div>"
                f"<div style='font-size:11px;color:#6B7280;'>{dash['subtitle']}</div>"
                f"</div>", unsafe_allow_html=True,
            )
            if dash['url']:
                st.link_button("فتح الداشبورد ↗", dash['url'], use_container_width=True)
            else:
                st.button("قريباً ⏳", key=f"dash_{dash['key']}", use_container_width=True, disabled=True)

    st.markdown("---")

    # ── SSRS Reports ──────────────────────────────────────────────────────────
    with st.expander("📋 تقارير SSRS — اضغط للعرض", expanded=False):
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        for idx, report in enumerate(SSRS_REPORTS):
            img_path = os.path.join(APP_DIR, report['file'])
            target   = col_a if idx % 2 == 0 else col_b
            with target:
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                    st.markdown(
                        f"<div style='background:#FFF7ED;border-radius:8px;"
                        f"padding:6px 10px;text-align:center;font-size:12px;"
                        f"font-weight:600;color:#1E293B;margin-bottom:20px;'>"
                        f"{report['title']}</div>", unsafe_allow_html=True,
                    )
                else:
                    st.warning(f"الصورة {report['file']} مش موجودة في مجلد التطبيق")


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — Phone Entry
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == 1:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        _, lc, _ = st.columns([1, 2, 1])
        with lc:
            show_logo(width=180)
        st.markdown("## 🍽️ أهلاً بك في FoodFlow")
        st.markdown("##### ادخل رقم تليفونك عشان نكمل")
        st.markdown("---")
        phone = st.text_input("رقم التليفون", placeholder="مثال: 01012345678", max_chars=11)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← رجوع", use_container_width=True):
                st.session_state.screen = 0
                st.rerun()
        with c2:
            if st.button("متابعة ←", use_container_width=True, type="primary"):
                phone = phone.strip()
                if len(phone) != 11 or not phone.isdigit():
                    st.error("⚠️ ادخل رقم تليفون صحيح مكون من 11 رقم")
                else:
                    st.session_state.phone    = phone
                    customer = get_customer_by_phone(phone)
                    if customer:
                        st.session_state.customer = customer
                        st.session_state.screen   = '2b'
                    else:
                        st.session_state.screen   = '2a'
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2A — New Customer Registration
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == '2a':
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("## 📋 تسجيل عميل جديد")
        st.info(f"الرقم **{st.session_state.phone}** مش موجود عندنا — ادخل بياناتك ونبدأ!")
        st.markdown("---")
        first_name = st.text_input("الاسم الأول (بالإنجليزي)", placeholder="Ahmed")
        last_name  = st.text_input("اسم العيلة (بالإنجليزي)",  placeholder="Mohamed")
        gender_map   = {"ذكر": "M", "أنثى": "F"}
        gender_label = st.radio("الجنس", list(gender_map.keys()), horizontal=True)
        st.markdown("---")
        cities       = load_cities()
        city_ar2id   = {c['CityName_AR']: c['CityID'] for c in cities}
        sel_city_ar  = st.selectbox("المدينة", list(city_ar2id.keys()))
        zones        = load_zones(city_ar2id[sel_city_ar])
        zone_ar2data = {z['ZoneName_AR']: z for z in zones}
        sel_zone_ar  = st.selectbox("المنطقة", list(zone_ar2data.keys()))
        sel_zone     = zone_ar2data[sel_zone_ar]
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← رجوع", use_container_width=True):
                st.session_state.screen = 1
                st.rerun()
        with c2:
            if st.button("سجّل وابدأ الطلب 🎉", use_container_width=True, type="primary"):
                if not first_name.strip() or not last_name.strip():
                    st.error("⚠️ ادخل الاسم الأول واسم العيلة")
                else:
                    full_name   = f"{first_name.strip()} {last_name.strip()}"
                    customer_id = insert_customer(
                        st.session_state.phone, full_name, full_name,
                        gender_map[gender_label], sel_zone['ZoneID'],
                    )
                    st.session_state.customer = {
                        'CustomerID':          customer_id,
                        'FullName_EN':         full_name,
                        'FullName_AR':         full_name,
                        'Gender':              gender_map[gender_label],
                        'ZoneID':              sel_zone['ZoneID'],
                        'ZoneName_AR':         sel_zone['ZoneName_AR'],
                        'ZoneName_EN':         sel_zone['ZoneName_EN'],
                        'DeliveryFee_EGP':     sel_zone['DeliveryFee_EGP'],
                        'BaseDeliveryMinutes': sel_zone['BaseDeliveryMinutes'],
                        'TrafficFactor':       sel_zone['TrafficFactor'],
                    }
                    st.session_state.screen = 3
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2B — Returning Customer
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == '2b':
    c = st.session_state.customer
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("## 👋 أهلاً بعودتك!")
        st.success(f"**{c['FullName_EN']}**")
        st.write(f"📍 منطقتك: **{c['ZoneName_AR']}**")
        st.write(f"🚚 رسوم التوصيل: **{c['DeliveryFee_EGP']:.2f} جنيه**")
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← رجوع", use_container_width=True):
                st.session_state.screen = 1
                st.rerun()
        with c2:
            if st.button("ابدأ طلبك 🍽️", use_container_width=True, type="primary"):
                st.session_state.screen = 3
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 3 — Menu Browser
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == 3:
    menu_items = load_menu()
    cart       = build_cart(menu_items)
    subtotal   = cart_subtotal(cart)
    c          = st.session_state.customer

    # ── Sidebar cart (desktop) ────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🛒 طلبك الحالي")
        st.markdown("---")
        if not cart:
            st.caption("لسه ما اخترتش حاجة")
        else:
            for item in cart.values():
                line = item['quantity'] * item['price']
                st.write(f"• {item['name_ar']}")
                st.caption(f"  {item['quantity']} × {item['price']:.2f} = **{line:.2f} ج**")
            st.markdown("---")
            st.metric("المجموع", f"{subtotal:.2f} جنيه")
            st.markdown("---")
            if st.button("مراجعة الطلب ✅", key="sidebar_review",
                         use_container_width=True, type="primary"):
                st.session_state['frozen_cart'] = cart
                st.session_state.screen = 4
                st.rerun()

    # ── Page header ───────────────────────────────────────────────────────────
    col_h, col_total = st.columns([3, 1])
    with col_h:
        st.markdown("## 🍽️ قائمة الطعام")
        st.caption(f"📍 {c['ZoneName_AR']}  |  🚚 رسوم التوصيل: {c['DeliveryFee_EGP']:.2f} جنيه")
    with col_total:
        if subtotal > 0:
            st.markdown(
                f"<div style='background:#FFF7ED;border:1px solid #FDBA74;"
                f"border-radius:12px;padding:12px;text-align:center;margin-top:10px;'>"
                f"<div style='font-size:11px;color:#6B7280;'>طلبك حتى الآن</div>"
                f"<div style='font-size:18px;font-weight:700;color:#EA580C;'>{subtotal:.2f} ج</div>"
                f"</div>", unsafe_allow_html=True,
            )

    # ── Mobile: always-visible cart bar + review button ───────────────────────
    if cart:
        st.markdown(
            f"<div style='background:#FFF7ED;border:1px solid #FDBA74;"
            f"border-radius:12px;padding:10px 16px;margin:8px 0;direction:rtl;'>"
            f"🛒 <strong>{sum(v['quantity'] for v in cart.values())} أيتم</strong> — "
            f"المجموع: <strong style='color:#EA580C;'>{subtotal:.2f} جنيه</strong>"
            f"</div>", unsafe_allow_html=True,
        )
        if st.button("مراجعة الطلب ✅", key="main_review",
                     use_container_width=True, type="primary"):
            st.session_state['frozen_cart'] = cart
            st.session_state.screen = 4
            st.rerun()

    st.markdown("---")

    # ── Category tabs ─────────────────────────────────────────────────────────
    categories = defaultdict(list)
    for item in menu_items:
        categories[item['CategoryName_AR']].append(item)

    tabs = st.tabs(list(categories.keys()))
    for tab, cat_name in zip(tabs, categories.keys()):
        with tab:
            for item in categories[cat_name]:
                iid = item['ItemID']
                cn, cp, cq = st.columns([4, 2, 2])
                with cn: st.write(f"**{item['ItemName_AR']}**")
                with cp: st.write(f"{item['CurrentPrice_EGP']:.2f} جنيه")
                with cq:
                    st.number_input(
                        label="الكمية", min_value=0, max_value=10, step=1,
                        key=f"qty_{iid}", label_visibility="collapsed",
                    )
                st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 4 — Order Confirmation
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == 4:
    cart         = st.session_state.get('frozen_cart', {})
    c            = st.session_state.customer
    delivery_fee = c['DeliveryFee_EGP']
    subtotal     = cart_subtotal(cart)
    total        = subtotal + delivery_fee

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown("## 🧾 تأكيد الطلب")
        st.markdown(f"📍 **{c['ZoneName_AR']}**")
        st.markdown("---")
        st.markdown("#### تفاصيل الطلب")
        for item in cart.values():
            line = item['quantity'] * item['price']
            ca, cb = st.columns([3, 1])
            with ca: st.write(f"• {item['name_ar']} × {item['quantity']}")
            with cb: st.write(f"**{line:.2f} ج**")
        st.markdown("---")
        ca, cb = st.columns(2)
        with ca:
            st.metric("المجموع",       f"{subtotal:.2f} جنيه")
            st.metric("رسوم التوصيل", f"{delivery_fee:.2f} جنيه")
        with cb:
            st.metric("💰 الإجمالي",  f"{total:.2f} جنيه")
            st.info("💵 الدفع: **كاش عند الاستلام**")
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← رجوع للمنيو", use_container_width=True):
                st.session_state.screen = 3
                st.rerun()
        with c2:
            if st.button("تأكيد الطلب 🎉", use_container_width=True, type="primary"):
                with st.spinner("بنحفظ طلبك..."):
                    order_id = insert_order(
                        c['CustomerID'], c['ZoneID'],
                        st.session_state.phone, subtotal, delivery_fee,
                    )
                    insert_order_items(order_id, cart)
                    st.session_state.order_id = order_id
                st.session_state.screen = 5
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 5 — Order Placed
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.screen == 5:
    cart     = st.session_state.get('frozen_cart', {})
    c        = st.session_state.customer
    order_id = st.session_state.get('order_id')
    max_prep      = max(v['prep_time'] for v in cart.values())
    delivery_mins = round(c['BaseDeliveryMinutes'] * c['TrafficFactor'])
    total_time    = max_prep + delivery_mins

    st.balloons()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("## ✅ تم استلام طلبك!")
        st.success(f"رقم الطلب: **#{order_id}**")
        st.markdown("---")
        st.metric("⏱️ وقت التوصيل المتوقع", f"{total_time} دقيقة")
        st.caption(f"وقت التحضير: {max_prep} دقيقة  +  وقت التوصيل: {delivery_mins} دقيقة")
        st.markdown("---")
        st.markdown("##### ملخص طلبك")
        for item in cart.values():
            st.write(f"• {item['name_ar']} × {item['quantity']}")
        st.markdown("---")
        if st.button("طلب جديد 🔄", use_container_width=True, type="primary"):
            keys = [k for k in st.session_state.keys() if k.startswith('qty_')]
            keys += ['screen', 'phone', 'customer', 'order_id', 'frozen_cart']
            for k in keys:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()
