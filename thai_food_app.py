import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import json

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

# MENU DATABASE - updated to match restaurant menu
MENU = {
    # Suppen u. Vorspeisen
    "1":  {"name": "Eierblumensuppe (m. Hühnerfleisch)", "price": 3.50},
    "5":  {"name": "Tom Kha Gai Suppe (m. Hühnerfl. u. Kokosmilch)", "price": 4.00},
    "6":  {"name": "Tom Yam-Gung Thai-Suppe mit Garnelen", "price": 4.00},
    "7":  {"name": "Sauer-Scharf-Suppe (m. Hühnerfleisch)", "price": 3.50},
    "8":  {"name": "Wan-Tan-Suppe (m. Hühnerfleisch-Füllung)", "price": 3.50},
    "9":  {"name": "Glasnudeln-Suppe mit Hühnerfleisch", "price": 3.50},
    "18": {"name": "Frühlingsrollen vegetarisch (8 Stück)", "price": 3.50},
    "19": {"name": "Wan-Tan gebacken (6 Stück)", "price": 3.50},

    # Gebratene Nudeln
    "21": {"name": "Gebratene Nudeln m. Hühnerfleisch (klein)", "price": 6.00},
    "23": {"name": "Gebratene Nudeln vegetarisch", "price": 6.00},
    "24": {"name": "Gebratene Nudeln m. Hühnerfleisch (groß)", "price": 7.00},
    "25": {"name": "Gebratene Nudeln m. Rindfleisch", "price": 9.00},
    "26": {"name": "Gebratene Nudeln m. Ente paniert, kross u. Süß-Sauer-Sauce", "price": 10.00},
    "27": {"name": "Gebratene Nudeln m. Hühnerbrust kross u. Süß-Sauer-Sauce", "price": 9.00},
    "28": {"name": "Bami-Goreng (Hühner u. Shrimps, Curry, pikant)", "price": 8.50},
    "29": {"name": "Gebratene Nudeln m. Garnelen (8 Stück)", "price": 10.00},

    # Eierreis
    "31": {"name": "Eierreis m. Hühnerfleisch (klein)", "price": 6.00},
    "33": {"name": "Eierreis vegetarisch", "price": 6.00},
    "34": {"name": "Eierreis m. Hühnerfleisch (groß)", "price": 7.00},
    "35": {"name": "Eierreis m. Rindfleisch", "price": 9.00},
    "36": {"name": "Eierreis m. Ente paniert, kross u. Süß-Sauer-Sauce", "price": 10.00},
    "37": {"name": "Eierreis m. Hühnerbrust kross u. Süß-Sauer-Sauce", "price": 9.00},
    "38": {"name": "Nasi-Goreng (Hühner u. Shrimps, Curry, pikant)", "price": 8.50},
    "39": {"name": "Eierreis m. Garnelen (8 Stück)", "price": 10.00},

    # Glasnudeln & Reisbandnudeln
    "40": {"name": "Glasnudeln gebraten mit Gemüse und Tofu", "price": 7.50},
    "41": {"name": "Glasnudeln gebraten mit Gemüse und Hühnerfleisch", "price": 8.50},
    "42": {"name": "Glasnudeln gebraten mit Gemüse und Hühnerbrust doppelt gebacken", "price": 9.00},
    "43": {"name": "Glasnudeln gebraten mit Gemüse und Rindfleisch", "price": 9.00},
    "47": {"name": "Pad-Thai gebr. Reisbandnudeln m. Hühnerfleisch, Gemüse u. Erdnüsse (pikant)", "price": 8.50},

    # Chop Suey-Sauce (mit Reis)
    "50": {"name": "Chop Suey Vegetarisch mit Tofu", "price": 7.50},
    "51a": {"name": "Chop Suey Hühnerfleisch", "price": 7.50},
    "51b": {"name": "Chop Suey Hühnerbrust in Stück, doppelt gebacken", "price": 9.00},
    "52": {"name": "Chop Suey Rindfleisch", "price": 9.00},
    "53": {"name": "Chop Suey Ente paniert, kross gebacken", "price": 10.00},
    "54": {"name": "Chop Suey Garnelen (8 Stück)", "price": 10.00},
    "55": {"name": "Chop Suey Hühnerbrust in Scheiben, kross gebacken", "price": 9.00},

    # Süß-Sauer-Sauce (mit Reis)
    "56": {"name": "Süß-Sauer Tofu (pikant, nach Thai-Art)", "price": 7.50},
    "57a": {"name": "Süß-Sauer Hühnerfleisch (pikant, nach Thai-Art)", "price": 7.50},
    "57b": {"name": "Süß-Sauer Hühnerbrust in Stück, doppelt gebacken", "price": 9.00},
    "57c": {"name": "Süß-Sauer Hühnerbrust in Scheibe, kross gebacken", "price": 9.00},
    "58": {"name": "Süß-Sauer Garnelen (8 Stück), pikant, nach Thai-Art", "price": 10.00},
    "59": {"name": "Süß-Sauer Ente paniert, kross gebacken", "price": 10.00},

    # Rote Curry-Sauce (mit Reis)
    "60": {"name": "Rotes Curry Vegetarisch mit Tofu", "price": 7.50},
    "61": {"name": "Rotes Curry Hühnerfleisch", "price": 8.50},
    "62": {"name": "Rotes Curry Rindfleisch", "price": 9.00},
    "63": {"name": "Rotes Curry Ente paniert kross gebacken", "price": 10.00},
    "64": {"name": "Rotes Curry Garnelen (8 Stück)", "price": 10.00},
    "65": {"name": "Rotes Curry Hühnerbrust kross gebacken", "price": 9.00},

    # Mango-Sauce (mit Reis)
    "80": {"name": "Mango-Sauce Vegetarisch mit Tofu", "price": 7.50},
    "81": {"name": "Mango-Sauce Hühnerfleisch", "price": 8.50},
    "83": {"name": "Mango-Sauce Ente paniert kross gebacken", "price": 10.00},
    "85": {"name": "Mango-Sauce Hühnerbrust paniert kross gebacken", "price": 9.00},

    # Knoblauch-Sauce (mit Reis)
    "90": {"name": "Knoblauch-Sauce Vegetarisch mit Tofu", "price": 7.50},
    "91": {"name": "Knoblauch-Sauce Hühnerfleisch", "price": 8.50},
    "92": {"name": "Knoblauch-Sauce Rindfleisch", "price": 9.00},
    "93": {"name": "Knoblauch-Sauce Ente paniert kross gebacken", "price": 10.00},
    "95": {"name": "Knoblauch-Sauce Hühnerbrust paniert kross gebacken", "price": 9.00},

    # Ingwer-Sauce (mit Reis)
    "100": {"name": "Ingwer-Sauce Vegetarisch mit Tofu", "price": 7.50},
    "101": {"name": "Ingwer-Sauce Hühnerfleisch", "price": 8.50},
    "102": {"name": "Ingwer-Sauce Rindfleisch", "price": 9.00},
    "103": {"name": "Ingwer-Sauce Ente paniert kross gebacken", "price": 10.00},
    "105": {"name": "Ingwer-Sauce Hühnerbrust paniert kross gebacken", "price": 9.00},

    # Zitronengras-Sauce (mit Reis)
    "110": {"name": "Zitronengras-Sauce Vegetarisch mit Tofu", "price": 7.50},
    "111": {"name": "Zitronengras-Sauce Hühnerfleisch", "price": 8.50},
    "112": {"name": "Zitronengras-Sauce Rindfleisch", "price": 9.00},
    "113": {"name": "Zitronengras-Sauce Ente paniert kross gebacken", "price": 10.00},
    "115": {"name": "Zitronengras-Sauce Hühnerbrust paniert kross gebacken", "price": 9.00},

    # Erdnuss-Sauce (mit Reis)
    "120": {"name": "Erdnuss-Sauce Vegetarisch mit Tofu", "price": 7.50},
    "121": {"name": "Erdnuss-Sauce Hühnerfleisch", "price": 8.50},
    "123": {"name": "Erdnuss-Sauce Ente paniert kross gebacken", "price": 10.00},
    "124": {"name": "Erdnuss-Sauce Hühnerbrust paniert kross gebacken", "price": 9.00},
}

# Customer Reviews data (delivery-focused)
CUSTOMER_REVIEWS = [
    {
        "customer_name": "Laura W.",
        "rating": 5,
        "review_text": "Fast delivery and super friendly courier! Everything arrived warm and on time. Great service!"
    },
    {
        "customer_name": "Michael T.",
        "rating": 4,
        "review_text": "Delivery arrived earlier than expected. Smooth and professional handover. Would definitely order again."
    },
    {
        "customer_name": "Sven K.",
        "rating": 5,
        "review_text": "The delivery driver was really polite and called ahead when he arrived. Excellent experience!"
    },
    {
        "customer_name": "Julia R.",
        "rating": 4,
        "review_text": "Service was quick and organized. Appreciated the updates and the friendly attitude of the delivery person."
    },
    {
        "customer_name": "Daniel B.",
        "rating": 5,
        "review_text": "Super reliable! This is the third time I order, and every delivery has been perfectly on time."
    }
]

# ============ ORDER CLOSING TIME CONFIGURATION ============
# Set your order closing time here (24-hour format)
# Example: For 11:30 AM, use hour=11, minute=30
ORDER_CLOSING_HOUR = 14  # Hour (0-23)
ORDER_CLOSING_MINUTE = 00  # Minute (0-59)
# ==========================================================

# Function to calculate time remaining
def get_time_remaining():
    berlin_tz = ZoneInfo("Europe/Berlin")
    now = datetime.now(berlin_tz)
    
    # Create closing time for today
    closing_time = now.replace(hour=ORDER_CLOSING_HOUR, minute=ORDER_CLOSING_MINUTE, second=0, microsecond=0)
    
    # If closing time has passed today, show 0
    if now >= closing_time:
        return None, True  # None time remaining, orders closed
    
    time_remaining = closing_time - now
    return time_remaining, False

# --- Shared Order List using st.cache_resource ---
# This list will be initialized once and shared across all user sessions.
@st.cache_resource
def get_shared_orders():
    return []

# Initialize a global variable for shared orders
shared_orders = get_shared_orders()

# Fun header
st.markdown("<h1 style='text-align: center; color: #ff6b6b;'>🍜 Thai Lunch Squad 🔥</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>Thien Thai Bistro - Let's get this pad thai!</h3>", unsafe_allow_html=True)

# Countdown Timer
time_remaining, is_closed = get_time_remaining()

if is_closed:
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
        border-radius: 15px; margin-bottom: 2rem; border: 3px solid #ff0000;'>
            <h2 style='color: white; margin: 0;'>⏰ ORDERS CLOSED</h2>
            <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>Order deadline has passed. See you next time!</p>
        </div>
    """, unsafe_allow_html=True)
else:
    hours, remainder = divmod(int(time_remaining.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        time_display = f"{hours}h {minutes}m {seconds}s"
        bg_color = "#28a745"  # Green
    elif minutes > 30:
        time_display = f"{minutes}m {seconds}s"
        bg_color = "#28a745"  # Green
    elif minutes > 10:
        time_display = f"{minutes}m {seconds}s"
        bg_color = "#ffc107"  # Yellow/Orange
    else:
        time_display = f"{minutes}m {seconds}s"
        bg_color = "#ff6b6b"  # Red
    
    st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%); 
        border-radius: 15px; margin-bottom: 2rem; border: 3px solid {bg_color};'>
            <h2 style='color: white; margin: 0;'>⏰ Time Until Order Closes</h2>
            <h1 style='color: white; margin: 0.5rem 0; font-size: 3rem; font-family: monospace;'>{time_display}</h1>
            <p style='color: white; margin: 0; font-size: 1.1rem;'>Closing at {ORDER_CLOSING_HOUR:02d}:{ORDER_CLOSING_MINUTE:02d}</p>
        </div>
        <script>
            setTimeout(function(){{
                window.parent.location.reload();
            }}, 1000);
        </script>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #e6f7ff; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #007bff;'>Your Office Food Delivery Just Got Easier!</h4>
        <p style='color: #333;'>Simply choose your favorites from our delicious menu, place your order, and relax! We'll deliver fresh, hot food right to your office. Remember: cash payments only, and please show some love to our delivery heroes with a tip! 🛵💰</p>
    </div>
""", unsafe_allow_html=True)

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

# Quick Menu Reference
with st.expander("📖 Quick Menu Reference", expanded=False):
    col_menu1, col_menu2, col_menu3 = st.columns(3)
    # sort by numeric key
    menu_items = sorted(MENU.items(), key=lambda x: int(''.join(filter(str.isdigit, x[0])) or 0))

    for idx, (num, item) in enumerate(menu_items):
        col = [col_menu1, col_menu2, col_menu3][idx % 3]
        with col:
            st.markdown(f"**{num}.** {item['name']} - €{item['price']:.2f}")

# Build options for selectbox: "num - name (€price)"
dish_options = []
for key, value in sorted(MENU.items(), key=lambda x: int(''.join(filter(str.isdigit, x[0])) or 0)):
    label = f"{key}. {value['name']} - €{value['price']:.2f}"
    dish_options.append((label, key))

# Add a blank first option
dish_options = [(" ", None)] + dish_options
labels = [opt[0] for opt in dish_options]

# Main layout: Order form on left, Order summary on right
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Place Your Order")
    
    # Disable ordering if closed
    if is_closed:
        st.warning("⚠️ Ordering is closed for today. The deadline has passed.")
        st.info("📋 You can still view all orders in the summary panel on the right.")
    
    if not is_closed:
        with st.form("order_form", clear_on_submit=True):
            name = st.text_input("Your Name 👤", placeholder="Who's hungry?")

            # Select dish with blank default
            selected_label = st.selectbox(
                "Choose your dish 🍽️",
                options=labels,
                index=0
            )

            # Map back to menu number (None if blank)
            selected_key = next(
                (k for (label, k) in dish_options if label == selected_label),
                None
            )

            if selected_key is not None:
                dish_info = MENU[selected_key]
                st.info(f"✨ You chose: {selected_key}. {dish_info['name']} - €{dish_info['price']:.2f}")
            else:
                dish_info = None
                st.info("👉 Please choose a dish from the list.")

            special_requests = st.text_area(
                "Special Requests 💬",
                placeholder="Extra veggies? No peanuts? Make it your own!",
                height=80
            )

            submitted = st.form_submit_button("🚀 Add My Order!", use_container_width=True)

            if submitted:
                if not name:
                    st.error("⚠️ Hold up! Please fill in your name!")
                elif dish_info is None:
                    st.error("⚠️ Please choose a dish before adding the order!")
                else:
                    total_price = dish_info["price"]
                    dish_display = dish_info["name"]

                    order = {
                        "name": name,
                        "dish": f"{selected_key}. {dish_display}",
                        "requests": special_requests if special_requests else "No special requests",
                        "price": total_price,
                        "time": datetime.now(ZoneInfo("Europe/Berlin")).strftime("%H:%M"),
                    }
                    shared_orders.append(order)
                    st.success(f"✨ Awesome! Added {name}'s order!")

with col2:
    st.markdown("### 📋 The Squad's Orders")

    if shared_orders:
        df = pd.DataFrame(shared_orders)
        df = df[["name", "dish", "requests", "price", "time"]]
        df.columns = ["Name", "Dish", "Notes", "€", "Time"]

        st.dataframe(df, use_container_width=True, hide_index=True)

        total = sum(order["price"] for order in shared_orders)
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
            padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
                <h2 style='color: white; margin: 0;'>Total: €{total:.2f}</h2>
                <p style='color: white; margin: 0;'>💵 Cash to the delivery hero!</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        name_to_remove = st.text_input(
            "Enter name to remove order: ",
            key="remove_order_by_name_input"
        )

        if st.button("🗑️ Remove Order by Name"):
            if name_to_remove:
                original_len = len(shared_orders)
                # Find and remove the first order matching the name
                for i, order in enumerate(shared_orders):
                    if order["name"].lower() == name_to_remove.lower():
                        shared_orders.pop(i)
                        st.success(f"Removed {name_to_remove}'s order.")
                        break
                if len(shared_orders) == original_len:
                    st.warning(f"No order found for {name_to_remove}.")
            else:
                st.warning("Please enter a name to remove an order.")
            st.rerun()


        if st.button("📋 Copy Order List", use_container_width=True):
            summary = "🍜 THAI FOOD SQUAD ORDERS 🍜\n" + "=" * 35 + "\n\n"
            for idx, order in enumerate(shared_orders, 1):
                summary += f"{idx}. {order['name']}\n"
                summary += f"   🍽️ {order['dish']}\n"
                summary += f"   💬 {order['requests']}\n"
                summary += f"   💶 €{order['price']:.2f}\n\n"
            summary += f"💰 TOTAL: €{total:.2f}\n"
            summary += "💵 Payment: CASH to delivery hero"

            st.code(summary, language=None)
    else:
        st.markdown("No order yet!")

# Customer Reviews Section
st.markdown("--- ✨ What Our Customers Say! ✨ ---")

for review in CUSTOMER_REVIEWS:
    st.markdown(f"**{review['customer_name']}** - {'⭐' * review['rating']}")
    st.info(f"_{review['review_text']}_")
    st.markdown("\n")  # Add some spacing between reviews

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🚶This app built by Your friendly office delivery service | 💶 Cash only vibes</p>",
    unsafe_allow_html=True,
)
