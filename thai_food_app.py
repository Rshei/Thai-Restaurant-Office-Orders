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

    # Rote Curry-Sauce (with Reis)
    "60": {"name": "Rotes Curry Vegetarisch mit Tofu", "price": 6.50},
    "61": {"name": "Rotes Curry Hühnerfleisch", "price": 7.50},
    "62": {"name": "Rotes Curry Rindfleisch", "price": 8.00},
    "63": {"name": "Rotes Curry Ente paniert kross gebacken", "price": 9.00},
    "64": {"name": "Rotes Curry Garnelen (8 Stück)", "price": 9.00},
    "65": {"name": "Rotes Curry Hühnerbrust kross gebacken", "price": 8.00},

    # Mango-Sauce (with Reis)
    "80": {"name": "Mango-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "81": {"name": "Mango-Sauce Hühnerfleisch", "price": 7.50},
    "83": {"name": "Mango-Sauce Ente paniert kross gebacken", "price": 9.00},
    "85": {"name": "Mango-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Knoblauch-Sauce (with Reis)
    "90": {"name": "Knoblauch-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "91": {"name": "Knoblauch-Sauce Hühnerfleisch", "price": 7.50},
    "92": {"name": "Knoblauch-Sauce Rindfleisch", "price": 8.00},
    "93": {"name": "Knoblauch-Sauce Ente paniert kross gebacken", "price": 9.00},
    "95": {"name": "Knoblauch-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Ingwer-Sauce (with Reis)
    "100": {"name": "Ingwer-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "101": {"name": "Ingwer-Sauce Hühnerfleisch", "price": 7.50},
    "102": {"name": "Ingwer-Sauce Rindfleisch", "price": 8.00},
    "103": {"name": "Ingwer-Sauce Ente paniert kross gebacken", "price": 9.00},
    "105": {"name": "Ingwer-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Zitronengras-Sauce (with Reis)
    "110": {"name": "Zitronengras-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "111": {"name": "Zitronengras-Sauce Hühnerfleisch", "price": 7.50},
    "112": {"name": "Zitronengras-Sauce Rindfleisch", "price": 8.00},
    "113": {"name": "Zitronengras-Sauce Ente paniert kross gebacken", "price": 9.00},
    "115": {"name": "Zitronengras-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},

    # Erdnuss-Sauce (with Reis)
    "120": {"name": "Erdnuss-Sauce Vegetarisch mit Tofu", "price": 6.50},
    "121": {"name": "Erdnuss-Sauce Hühnerfleisch", "price": 7.50},
    "123": {"name": "Erdnuss-Sauce Ente paniert kross gebacken", "price": 9.00},
    "124": {"name": "Erdnuss-Sauce Hühnerbrust paniert kross gebacken", "price": 8.00},
}

def sort_menu_key(key):
    """Properly sort menu keys including those with letters (51a, 51b, etc.)"""
    # Extract numeric part
    num_part = ''.join(filter(str.isdigit, key))
    # Extract letter part
    letter_part = ''.join(filter(str.isalpha, key))
    # Return tuple for proper sorting
    return (int(num_part) if num_part else 0, letter_part)

# Initialize session state for orders
if "orders" not in st.session_state:
    st.session_state.orders = []

# Fun header
st.markdown("<h1 style='text-align: center; color: #ff6b6b;'>🍜 Thai Lunch Squad 🔥</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>Thien Thai Bistro - Let's get this pad thai!</h3>", unsafe_allow_html=True)

# Function to add an item to the cart
def add_to_cart(item_code, item_name, price):
    st.session_state.orders.append({"Code": item_code, "Name": item_name, "Price": price})
    st.sidebar.success(f"Added {item_name} to cart!")

# Function to clear the cart
def clear_cart():
    st.session_state.orders = []
    st.sidebar.info("Cart cleared!")

# --- Main Application Layout ---

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Menu")
    
    # Dropdown for category selection
    selected_category_name = st.selectbox("Select a Category", list(MENU_CATEGORIES.keys()))
    
    # Get the item codes for the selected category
    item_codes = MENU_CATEGORIES[selected_category_name]
    
    # Sort item codes properly within category
    sorted_codes = sorted(item_codes, key=sort_menu_key)

    # Display items in the selected category
    for code in sorted_codes:
        item = MENU[code]
        item_name = item['name']
        price = item['price']

        # Use columns for layout within the menu
        menu_col1, menu_col2, menu_col3 = st.columns([0.5, 3, 1])
        with menu_col1:
            st.write(f"**{code}**")
        with menu_col2:
            st.write(item_name)
        with menu_col3:
            st.write(f"€{price:,.2f}")
            # Button to add to cart
            st.button("Add", key=f"add_{code}_{selected_category_name}", on_click=add_to_cart, args=(code, item_name, price))
        
        st.markdown("---") # Separator between items


with col2:
    st.header("Your Order Cart")

    if not st.session_state.orders:
        st.info("Your cart is empty.")
    else:
        # Convert orders list to a DataFrame for nice display
        df_orders = pd.DataFrame(st.session_state.orders)
        # Display the cart using a DataFrame
        st.dataframe(df_orders, use_container_width=True, hide_index=True)

        # Calculate total price
        total_price = df_orders['Price'].sum()
        st.markdown(f"### Total: €{total_price:,.2f}")

        # Clear cart button
        st.button("Clear Order", on_click=clear_cart)

        # Placeholder for final submission (e.g., this is where you'd send the order)
        st.success("Order ready! Copy the items above or integrate with a backend system.")
