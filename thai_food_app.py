import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Thai Food Order", page_icon="🍜", layout="wide")

# Initialize session state for orders
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Title and header
st.title("🍜 Thai Restaurant Office Orders")
st.markdown("### Order your lunch from our neighbor Thai restaurant!")

# Menu link section
st.info("📋 **Restaurant Menu**: [Click here to view the menu](https://example.com/menu) - Replace this link with your actual menu URL")

# Main layout: Order form on left, Order summary on right
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Place Your Order")
    
    # Order form
    with st.form("order_form", clear_on_submit=True):
        name = st.text_input("Your Name*", placeholder="Enter your name")
        
        dish = st.text_input("Dish Name*", placeholder="e.g., Pad Thai, Green Curry")
        
        spice_level = st.select_slider(
            "Spice Level",
            options=["No Spice", "Mild", "Medium", "Spicy", "Extra Spicy"],
            value="Medium"
        )
        
        special_requests = st.text_area(
            "Special Requests (optional)",
            placeholder="e.g., No peanuts, extra vegetables, no cilantro"
        )
        
        price = st.number_input("Price (€)*", min_value=0.0, step=0.5, format="%.2f")
        
        submitted = st.form_submit_button("Add to Orders", use_container_width=True)
        
        if submitted:
            if name and dish and price > 0:
                order = {
                    "name": name,
                    "dish": dish,
                    "spice": spice_level,
                    "requests": special_requests,
                    "price": price,
                    "time": datetime.now().strftime("%H:%M")
                }
                st.session_state.orders.append(order)
                st.success(f"✅ Order added for {name}!")
            else:
                st.error("Please fill in all required fields (Name, Dish, and Price)")

with col2:
    st.subheader("📝 Today's Orders")
    
    if st.session_state.orders:
        # Display all orders
        for idx, order in enumerate(st.session_state.orders):
            with st.container():
                st.markdown(f"**{order['name']}**")
                st.text(f"🍽️ {order['dish']}")
                st.text(f"🌶️ {order['spice']}")
                if order['requests']:
                    st.text(f"📝 {order['requests']}")
                st.text(f"💶 €{order['price']:.2f} | ⏰ {order['time']}")
                
                if st.button("Remove", key=f"remove_{idx}"):
                    st.session_state.orders.pop(idx)
                    st.rerun()
                
                st.divider()
        
        # Total calculation
        total = sum(order['price'] for order in st.session_state.orders)
        st.markdown(f"### Total: €{total:.2f}")
        st.info("💵 Payment: Cash only")
        
        # Clear all orders button
        if st.button("🗑️ Clear All Orders", use_container_width=True):
            st.session_state.orders = []
            st.rerun()
            
        # Export orders as text
        if st.button("📋 Copy Order Summary", use_container_width=True):
            summary = "THAI FOOD ORDERS\n" + "="*30 + "\n\n"
            for order in st.session_state.orders:
                summary += f"{order['name']}\n"
                summary += f"  Dish: {order['dish']}\n"
                summary += f"  Spice: {order['spice']}\n"
                if order['requests']:
                    summary += f"  Notes: {order['requests']}\n"
                summary += f"  Price: €{order['price']:.2f}\n\n"
            summary += f"TOTAL: €{total:.2f}\n"
            summary += "Payment: CASH"
            
            st.code(summary, language=None)
    else:
        st.info("No orders yet. Be the first to order!")

# Footer
st.markdown("---")
st.caption("🚶 Delivery by your friendly office colleague | 💶 Cash payment only")
