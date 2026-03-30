import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Grandma's Pickles",
    layout="wide"
)

# -----------------------------
# STYLING (Vintage Feel)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #F7F3E9;
}
h1, h2, h3 {
    font-family: 'Georgia', serif;
    color: #5A3E2B;
}
.product-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    background-color: white;
    margin-bottom: 20px;
}
.add-btn {
    background-color: #A83232;
    color: white;
    padding: 8px;
    border-radius: 5px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SAMPLE DATA (EDITABLE)
# -----------------------------
products = [
    {
        "name": "Andhra Mango Pickle",
        "category": "Veg",
        "description": "Spicy mango pickle made with cold-pressed oil.",
        "price": { "250g": 199, "500g": 349, "1kg": 649 },
        "rating": 4.6
    },
    {
        "name": "Chicken Pickle",
        "category": "Non-Veg",
        "description": "Rich and spicy chicken pickle with authentic flavors.",
        "price": { "250g": 299, "500g": 549, "1kg": 999 },
        "rating": 4.7
    },
    {
        "name": "Gongura Pickle",
        "category": "Veg",
        "description": "Tangy Andhra-style gongura pickle.",
        "price": { "250g": 189, "500g": 329, "1kg": 599 },
        "rating": 4.5
    },
    {
        "name": "Spicy Chili Powder",
        "category": "Spices",
        "description": "Pure red chili powder with bold flavor.",
        "price": { "250g": 149, "500g": 279, "1kg": 499 },
        "rating": 4.4
    }
]

# -----------------------------
# HEADER
# -----------------------------
st.title("🏺 Ini's Pickle Jar")
search = st.text_input("🔍 Search Pickles & Spices")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    ["Veg", "Non-Veg", "Spices"],
    default=["Veg", "Non-Veg", "Spices"]
)

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["Popularity", "Price Low to High", "Price High to Low", "Rating"]
)

# -----------------------------
# FILTER FUNCTION
# -----------------------------
def filter_products(products):
    filtered = []

    for p in products:
        if p["category"] in category_filter:
            if search.lower() in p["name"].lower():
                filtered.append(p)

    return filtered

filtered_products = filter_products(products)

# -----------------------------
# SORTING
# -----------------------------
if sort_option == "Price Low to High":
    filtered_products.sort(key=lambda x: min(x["price"].values()))
elif sort_option == "Price High to Low":
    filtered_products.sort(key=lambda x: max(x["price"].values()), reverse=True)
elif sort_option == "Rating":
    filtered_products.sort(key=lambda x: x["rating"], reverse=True)

# -----------------------------
# CART STATE
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------------
# DISPLAY PRODUCTS
# -----------------------------
cols = st.columns(3)

for i, product in enumerate(filtered_products):
    with cols[i % 3]:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        # Placeholder image
        st.image("https://via.placeholder.com/300x200", use_container_width=True)

        st.subheader(product["name"])
        st.write(product["description"])
        st.write(f"⭐ {product['rating']}")

        weight = st.selectbox(
            f"Select Weight ({product['name']})",
            list(product["price"].keys()),
            key=f"weight_{i}"
        )

        st.write(f"Price: ₹{product['price'][weight]}")

        if st.button("Add to Cart", key=f"cart_{i}"):
            st.session_state.cart.append({
                "name": product["name"],
                "weight": weight,
                "price": product["price"][weight]
            })
            st.success(f"{product['name']} added!")

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# CART VIEW
# -----------------------------
st.sidebar.header("🛒 Cart")

total = 0
for item in st.session_state.cart:
    st.sidebar.write(f"{item['name']} ({item['weight']}) - ₹{item['price']}")
    total += item["price"]

st.sidebar.write("---")
st.sidebar.write(f"**Total: ₹{total}**")

if st.sidebar.button("Checkout"):
    st.sidebar.success("Order placed successfully! 🎉")
    st.session_state.cart = []