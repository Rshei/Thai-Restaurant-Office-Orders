import streamlit as st
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(page_title="Thai Food Order", page_icon="🍜", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff5252;
        transform: scale(1.05);
    }
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# MENU DATABASE with categories
MENU_CATEGORIES = {
    "Suppen & Vorspeisen": ["1", "3", "5", "6", "7", "8", "18", "19", "20"],
    "Gebratene Nudeln": ["21", "23", "24", "25", "26", "27", "28", "29"],
    "Eierreis": ["31", "33", "34", "35", "36", "37", "38", "39"],
    "Glasnudeln & Reisbandnudeln": ["40", "41", "42", "43", "47"],
    "Chop Suey-Sauce": ["50", "51a", "51b", "52", "53", "54", "55"],
    "Süß-Sauer-Sauce": ["56", "57a", "57b", "57c", "58", "59"],
    "Rote Curry-Sauce": ["60", "61", "62", "63", "64", "65"],
    "Mango-Sauce": ["80", "81", "83", "85"],
    "Knoblauch-Sauce": ["90", "91", "92", "93", "95"],
    "Ingwer-Sauce": ["100", "101", "102", "103", "105"],
    "Zitronengras-Sauce": ["110", "111", "112", "113", "115"],
    "Erdnuss-Sauce": ["120", "121", "123", "124"],
}

MENU = {
    # Suppen u. Vorspeisen
    "1":  {"name": "Eierblumensuppe (m. Hühnerfleisch)", "price": 3.00},
    "3":  {"name": "Glasnudeln-Suppe (mit Hühnerfleisch)", "price": 3.00},
    "5":  {"name": "Tom Kha-Gai Ram Suppe (m. Hühnerfleisch, Kokosmilch)", "price": 3.50},
    "6":  {"name": "Tom Yam-Gung Thai-Suppe (m. Garnelen)", "price": 3.60},
    "7":  {"name": "Sauer-Scharf-Suppe (m. Hühnerfleisch)", "price": 3.00},
    "8":  {"name": "Wan-Tan-Suppe (m. Hühnerfleisch-Füllung)", "price": 3.00},
    "18": {"name": "Frühlingsrollen vegetarisch (8 Stück)", "price": 3.00},
    "19": {"name": "Wantan gebacken (6 Stück)", "price": 3.00},
    "20": {"name": "Krupuk Garnelenchip", "price": 2.00},

    # Gebratene Nudeln
    "21": {"name": "Gebratene Nudeln m. Hühnerfleisch (klein)", "price": 5.00},
    "23": {"name": "Gebratene Nudeln vegetarisch", "price": 5.00},
    "24": {"name": "Gebratene Nudeln m. Hühnerfleisch (groß)", "price": 6.00},
    "25": {"name": "Gebratene Nudeln m. Rindfleisch", "price": 8.00},
    "26": {"name": "Gebratene Nudeln m. Ente paniert, kross u. Süß-Sauer-Sauce", "price": 9.00},
    "27": {"name": "Gebratene Nudeln m. Hühnerbrust kross u. Süß-Sauer-Sauce", "price": 8.00},
    "28": {"name": "Bami-Goreng (Hühner u. Shrimps, Curry, pikant)", "price": 7.50},
    "29": {"name": "Gebratene Nudeln m. Garnelen (8 Stück)", "price": 9.00},

    # Eierreis
    "31": {"name": "Eierreis m. Hühnerfleisch (klein)", "price": 5.00},
    "33": {"name": "Eierreis vegetarisch", "price": 5.00},
    "34": {"name": "Eierreis m. Hühnerfleisch (groß)", "price": 6.00},
    "35": {"name": "Eierreis m. Rindfleisch", "price": 8.00},
    "36": {"name": "Eierreis m. Ente paniert, kross u. Süß-Sauer-Sauce", "price": 9.00},
    "37": {"name": "Eierreis m. Hühnerbrust kross u. Süß-Sauer-Sauce", "price": 8.00},
    "38": {"name": "Nasi-Goreng (Hühner u. Shrimps, Curry, pikant)", "price": 7.50},
    "39": {"name": "Eierreis m. Garnelen (8 Stück)", "price": 9.00},

    # Glasnudeln & Reisbandnudeln
    "40": {"name": "Glasnudeln gebraten mit Gemüse und Tofu", "price": 6.50},
    "41": {"name": "Glasnudeln gebraten mit Gemüse und Hühnerfleisch", "price": 7.50},
    "42": {"name": "Glasnudeln gebraten mit Gemüse und Hühnerbrust doppelt gebacken", "price": 8.00},
    "43": {"name": "Glasnudeln gebraten mit Gemüse und Rindfleisch", "price": 8.00},
    "47": {"name": "Pad-Thai gebr. Reisbandnudeln m. Hühnerfleisch, Gemüse u. Erdnüsse (pikant)", "price": 7.50},

    # Chop Suey-Sauce (mit Reis)
    "50": {"name": "Chop Suey Vegetarisch mit Tofu", "price": 6.50},
    "51a": {"name": "Chop Suey Hühnerfleisch", "price": 6.50},
    "51b": {"name": "Chop Suey Hühnerbrust in Stück, doppelt gebacken", "price": 8.00},
    "52": {"name": "Chop Suey Rindfleisch", "price": 8.00},
    "53": {"name": "Chop Suey Ente paniert, kross gebacken", "price": 8.00},
    "54": {"name": "Chop Suey Garnelen (8 Stück)", "price": 9.00},
    "55": {"name": "Chop Suey Hühnerbrust in Scheiben, kross gebacken", "price": 9.00},

    # Süß-Sauer-Sauce (mit Reis)
    "56": {"name": "Süß-Sauer Tofu (pikant, nach Thai-Art)", "price": 6.50},
    "57a": {"name": "Süß-Sauer Hühnerfleisch (pikant, nach Thai-Art)", "price": 8.00},
    "57b": {"name": "Süß-Sauer Hühnerbrust in Stück, doppelt gebacken", "price": 8.00},
    "57c": {"name": "Süß-Sauer Hühnerbrust in Scheibe, kross gebacken", "price": 9.00},
    "58": {"name": "Süß-Sauer Garnelen (8 Stück), pikant, nach Thai-Art", "price": 9.00},
    "59": {"name": "Süß-Sauer Ente paniert, kross gebacken", "price": 9.00},

    # Rote Curry-Sauce (mit Reis)
    "60": {"name": "Rotes Curry Vegetarisch mit Tofu", "price": 6.50},
    "61": {"name": "Rotes Curry Hühnerfleisch", "price": 7.50},
    "62": {"name": "Rotes Curry Rindfleisch", "price": 8.00},
    "63": {"name": "Rotes Curry Ente paniert kross gebacken", "price": 9.00},
    "64": {"name": "Rotes Curry Garnelen (8 Stück)", "price": 9.00},
    "65": {"name": "Rotes Curry Hühnerbrust kross gebacken", "price": 8.00},

    # Mango-Sauce (mit Reis)
    "80": {"name": "Mango-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "81": {"name": "Mango-Sauce Hühnerfleisch", "price": 7.50},
    "83": {"name": "Mango-Sauce Ente paniert kross gebacken", "price": 9.00},
    "85": {"name": "Mango-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Knoblauch-Sauce (mit Reis)
    "90": {"name": "Knoblauch-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "91": {"name": "Knoblauch-Sauce Hühnerfleisch", "price": 7.50},
    "92": {"name": "Knoblauch-Sauce Rindfleisch", "price": 8.00},
    "93": {"name": "Knoblauch-Sauce Ente paniert kross gebacken", "price": 9.00},
    "95": {"name": "Knoblauch-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Ingwer-Sauce (mit Reis)
    "100": {"name": "Ingwer-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "101": {"name": "Ingwer-Sauce Hühnerfleisch", "price": 7.50},
    "102": {"name": "Ingwer-Sauce Rindfleisch", "price": 8.00},
    "103": {"name": "Ingwer-Sauce Ente paniert kross gebacken", "price": 9.00},
    "105": {"name": "Ingwer-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Zitronengras-Sauce (mit Reis)
    "110": {"name": "Zitronengras-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "111": {"name": "Zitronengras-Sauce Hühnerfleisch", "price": 7.50},
    "112": {"name": "Zitronengras-Sauce Rindfleisch", "price": 8.00},
    "113": {"name": "Zitronengras-Sauce Ente paniert kross gebacken", "price": 9.00},
    "115": {"name": "Zitronengras-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Erdnuss-Sauce (mit Reis)
    "120": {"name": "Erdnuss-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "121": {"name": "Erdnuss-Sauce Hühnerfleisch", "price": 7.50},
    "123": {"name": "Erdnuss-Sauce Ente paniert kross gebacken", "price": 9.00},
    "124": {"name": "Erdnuss-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},
}

# Initialize session state for orders
if "orders" not in st.session_state:
    st.session_state.orders = []

# Fun header
st.markdown("<h1 style='text-align: center; color: #ff6b6b;'>🍜 Thai Lunch Squad 🔥</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>Thien Thai Bistro - Let's get this pad thai!</h3>", unsafe_allow_html=True)

# Menu link section
MENU_URL = "https://www.google.com/maps/place/Thien+Thai+Bistro/@52.5364437,13.2723721,3a,75y,90t/data=!3m8!1e2!3m6!1sCIHM0ogKEICAgIDZruezGQ!2e10!3e12!6shttps:%2F%2Flh3.googleusercontent.com%2Fgps-cs-s%2FAG0ilSyjaUPfX_bg9cANspvtJgqf6qGUB3hTyNN8bkwRMCiCzpOZQn7hvozHQvIqqUefUHo5ywJ6ZYweysXOCSP05KNw_VqQlybBnJJgbh2Dn-3jtWL6ERtiGrE_n_geRKhC-eDcqPV7%3Dw146-h195-k-no!7i3000!8i4000!4m10!1m2!2m1!1ssiemens+damm!3m6!1s0x47a856c7885ec39d:0xe8d8c1bdc6419318!8m2!3d52.5362941!4d13.272357!10e9!16s%2Fg%2F11bxc5hddn?entry=ttu&g_ep=EgoyMDI1MTIwMi4wIKXMDSoASAFQAw%3D%3D"

st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 15px; margin-bottom: 2rem;'>
        <a href='{MENU_URL}' target='_blank' style='color: white; text-decoration: none; font-size: 1.2rem; font-weight: bold;'>
            📱 Check Out The Menu 🌶️
        </a>
    </div>
""", unsafe_allow_html=True)

# Quick Menu Reference - now with categories
with st.expander("📖 Quick Menu Reference", expanded=False):
    for category, item_ids in MENU_CATEGORIES.items():
        st.markdown(f"### {category}")
        col_menu1, col_menu2, col_menu3 = st.columns(3)
        for idx, item_id in enumerate(item_ids):
            item = MENU[item_id]
            col = [col_menu1, col_menu2, col_menu3][idx % 3]
            with col:
                st.markdown(f"**{item_id}.** {item['name']} - €{item['price']:.2f}")

# Category selector + dish selector
col_cat, col_dish = st.columns([1, 2])
with col_cat:
    selected_category = st.selectbox("Select Category 🍜", options=list(MENU_CATEGORIES.keys()))
with col_dish:
    category_items = MENU_CATEGORIES[selected_category]
    dish_options = [(f"{key}. {MENU[key]['name']} - €{MENU[key]['price']:.2f}", key) for key in category_items]
    selected_label = st.selectbox("Choose your dish", options=[opt[0] for opt in dish_options], index=0)
    selected_key = next(k for (label, k) in dish_options if label == selected_label)

# Main layout: Order form on left, Order summary on right
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Place Your Order")

    with st.form("order_form", clear_on_submit=True):
        name = st.text_input("Your Name 👤", placeholder="Who's hungry?")
        
        dish_info = MENU[selected_key]
        st.info(f"✨ You chose: **{selected_key}. {dish_info['name']}** - €{dish_info['price']:.2f}")

        special_requests = st.text_area(
            "Special Requests 💬",
            placeholder="Extra veggies? No peanuts? Make it your own!",
            height=80
        )

        submitted = st.form_submit_button("🚀 Add My Order!", use_container_width=True)

        if submitted:
            if name:
                total_price = dish_info["price"]
                dish_display = dish_info["name"]

                order = {
                    "name": name,
                    "dish": f"{selected_key}. {dish_display}",
                    "requests": special_requests if special_requests else "No special requests",
                    "price": total_price,
                    "time": datetime.now().strftime("%H:%M"),
                }
                st.session_state.orders.append(order)
                st.balloons()
                st.success(f"✨ Awesome! Added {name}'s order!")
            else:
                st.error("⚠️ Hold up! Please fill in your name!")

with col2:
    st.markdown("### 📋 The Squad's Orders")

    if st.session_state.orders:
        df = pd.DataFrame(st.session_state.orders)
        df = df[["name", "dish", "requests", "price", "time"]]
        df.columns = ["Name", "Dish", "Notes", "€", "Time"]

        st.dataframe(df, use_container_width=True, hide_index=True)

        total = sum(order["price"] for order in st.session_state.orders)
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
            padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
                <h2 style='color: white; margin: 0;'>Total: €{total:.2f}</h2>
                <p style='color: white; margin: 0;'>💵 Cash to the delivery hero!</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        order_to_remove = st.number_input(
            "Remove order (row #, starting at 0)",
            min_value=0,
            max_value=len(st.session_state.orders) - 1,
            step=1,
        )
        if st.button("🗑️ Remove Order"):
            st.session_state.orders.pop(order_to_remove)
            st.rerun()

        if st.button("💣 Clear Everything", use_container_width=True):
            st.session_state.orders = []
            st.rerun()

        if st.button("📋 Copy Order List", use_container_width=True):
            summary = "🍜 THAI FOOD SQUAD ORDERS 🍜\n" + "=" * 35 + "\n\n"
            for idx, order in enumerate(st.session_state.orders, 1):
                summary += f"{idx}. {order['name']}\n"
                summary += f"   🍽️ {order['dish']}\n"
                summary += f"   💬 {order['requests']}\n"
                summary += f"   💶 €{order['price']:.2f}\n\n"
            summary += f"💰 TOTAL: €{total:.2f}\n"
            summary += "💵 Payment: CASH to delivery hero"

            st.code(summary, language=None)
    else:
        st.markdown("""
            <div style='text-align: center; padding: 2rem; background-color: #fff3cd; 
            border-radius: 10px; border: 2px dashed #ffc107;'>
                <h3>🤔 No orders yet!</h3>
                <p>Be the first one to order! 🚀</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🚶 Your friendly office delivery service | 💶 Cash only vibes</p>",
    unsafe_allow_html=True,
)
