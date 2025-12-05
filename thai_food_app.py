import streamlit as st
from datetime import datetime

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

# MENU DATABASE - Update this with actual menu items
MENU = {
    "1": {"name": "Pad Thai", "price": 9.50},
    "2": {"name": "Green Curry", "price": 10.90},
    "3": {"name": "Red Curry", "price": 10.90},
    "4": {"name": "Tom Yum Soup", "price": 8.50},
    "5": {"name": "Massaman Curry", "price": 11.50},
    "6": {"name": "Pad See Ew", "price": 9.50},
    "7": {"name": "Spring Rolls (4 pieces)", "price": 5.50},
    "8": {"name": "Som Tam (Papaya Salad)", "price": 7.90},
    "9": {"name": "Khao Pad (Fried Rice)", "price": 8.90},
    "10": {"name": "Tom Kha Gai", "price": 8.90},
    "11": {"name": "Panang Curry", "price": 10.90},
    "12": {"name": "Pho Bo", "price": 9.90},
    "13": {"name": "Satay Skewers (5 pieces)", "price": 7.50},
    "14": {"name": "Drunken Noodles", "price": 9.90},
    "15": {"name": "Thai Basil Chicken", "price": 10.50},
}

# Initialize session state for orders
if 'orders' not in st.session_state:
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

# Display menu in a nice format
with st.expander("📖 Quick Menu Reference", expanded=False):
    col_menu1, col_menu2, col_menu3 = st.columns(3)
    menu_items = list(MENU.items())
    
    for idx, (num, item) in enumerate(menu_items):
        if idx % 3 == 0:
            with col_menu1:
                st.markdown(f"**{num}.** {item['name']} - €{item['price']:.2f}")
        elif idx % 3 == 1:
            with col_menu2:
                st.markdown(f"**{num}.** {item['name']} - €{item['price']:.2f}")
        else:
            with col_menu3:
                st.markdown(f"**{num}.** {item['name']} - €{item['price']:.2f}")

# Main layout: Order form on left, Order summary on right
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Place Your Order")
    
    # Order form
    with st.form("order_form", clear_on_submit=True):
        name = st.text_input("Your Name 👤", placeholder="Who's hungry?")
        
        menu_number = st.text_input("Menu Number 🔢", placeholder="Enter number from menu (e.g., 1, 2, 3...)")
        
        # Show dish name and price if valid menu number
        if menu_number and menu_number in MENU:
            dish_info = MENU[menu_number]
            st.success(f"✨ {dish_info['name']} - €{dish_info['price']:.2f}")
        elif menu_number:
            st.warning("⚠️ Invalid menu number! Check the menu reference above.")
        
        col_spice, col_extra = st.columns(2)
        
        with col_spice:
            spice_level = st.select_slider(
                "Heat Level 🌶️",
                options=["😊 Mild", "🙂 Medium", "😅 Spicy", "🔥 Extra Hot", "☠️ Insane"],
                value="🙂 Medium"
            )
        
        with col_extra:
            extra_item = st.text_input("Extra Item? (optional)", placeholder="e.g., Rice, Drink")
            extra_price = st.number_input("Extra Price 💶", min_value=0.0, step=0.5, format="%.2f")
        
        special_requests = st.text_area(
            "Special Requests 💬",
            placeholder="Extra veggies? No peanuts? Make it your own!",
            height=80
        )
        
        submitted = st.form_submit_button("🚀 Add My Order!", use_container_width=True)
        
        if submitted:
            if name and menu_number and menu_number in MENU:
                dish_info = MENU[menu_number]
                total_price = dish_info['price'] + extra_price
                
                dish_display = dish_info['name']
                if extra_item:
                    dish_display += f" + {extra_item}"
                
                order = {
                    "name": name,
                    "dish": dish_display,
                    "spice": spice_level,
                    "requests": special_requests if special_requests else "No special requests",
                    "price": total_price,
                    "time": datetime.now().strftime("%H:%M")
                }
                st.session_state.orders.append(order)
                st.balloons()
                st.success(f"✨ Awesome! Added {name}'s order!")
            else:
                st.error("⚠️ Hold up! Fill in your name and a valid menu number!")

with col2:
    st.markdown("### 📋 The Squad's Orders")
    
    if st.session_state.orders:
        # Create dataframe for table display
        import pandas as pd
        
        df = pd.DataFrame(st.session_state.orders)
        df = df[['name', 'dish', 'spice', 'requests', 'price', 'time']]
        df.columns = ['Name', 'Dish', 'Heat', 'Notes', '€', 'Time']
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Total calculation with fun styling
        total = sum(order['price'] for order in st.session_state.orders)
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
            padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
                <h2 style='color: white; margin: 0;'>Total: €{total:.2f}</h2>
                <p style='color: white; margin: 0;'>💵 Cash to the delivery hero!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Remove order by selecting row number
        st.markdown("---")
        order_to_remove = st.number_input(
            "Remove order (row #)", 
            min_value=0, 
            max_value=len(st.session_state.orders)-1, 
            step=1
        )
        if st.button("🗑️ Remove Order"):
            st.session_state.orders.pop(order_to_remove)
            st.rerun()
        
        # Clear all orders button
        if st.button("💣 Clear Everything", use_container_width=True):
            st.session_state.orders = []
            st.rerun()
            
        # Export orders as text
        if st.button("📋 Copy Order List", use_container_width=True):
            summary = "🍜 THAI FOOD SQUAD ORDERS 🍜\n" + "="*35 + "\n\n"
            for idx, order in enumerate(st.session_state.orders, 1):
                summary += f"{idx}. {order['name']}\n"
                summary += f"   🍽️ {order['dish']}\n"
                summary += f"   🌶️ {order['spice']}\n"
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
st.markdown("<p style='text-align: center; color: #666;'>🚶 Your friendly office delivery service | 💶 Cash only vibes</p>", unsafe_allow_html=True)
