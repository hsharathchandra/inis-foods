import streamlit as st
import requests
import os
import urllib.parse

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "name" not in st.session_state:
    st.session_state.name = ""

# -----------------------------
# CONFIG
# -----------------------------
API = "https://inis-foods.onrender.com"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Ini's Pickle Jar", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.block-container { padding-top: 1rem !important; }

.product-card {
  background:white;
  padding:12px;
  border-radius:12px;
  box-shadow:0 4px 12px rgba(0,0,0,0.1);
  margin-bottom:15px;
}

.price { color:#A83232; font-weight:bold; }

.product-card img {
    height: 250px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 10px;
}

.cart-item {
    padding:8px;
    border-bottom:1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD PRODUCTS ----------------
def load_products():
    try:
        res = requests.get(f"{API}/products")
        if res.status_code != 200:
            return []
        data = res.json()
        return data if isinstance(data, list) else []
    except:
        return []

products = load_products()

# ---------------- STORE ----------------
st.title("🏺 Ini's Pickle Jar")

search = st.text_input("Search")

category = st.sidebar.multiselect(
    "Category",
    ["Veg","Non-Veg","Spices"],
    default=["Veg","Non-Veg","Spices"]
)

sort = st.sidebar.selectbox(
    "Sort By",
    ["None","Price Low","Price High","Rating"]
)

# ---------------- FILTER ----------------
filtered = []

for p in products:
    if not isinstance(p, dict):
        continue

    if p.get("category") in category and search.lower() in p.get("name","").lower():
        filtered.append(p)

# ---------------- SORT ----------------
if sort == "Price Low":
    filtered.sort(key=lambda x: min(x.get("price", {}).values()))
elif sort == "Price High":
    filtered.sort(key=lambda x: max(x.get("price", {}).values()), reverse=True)
elif sort == "Rating":
    filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)

# ---------------- PRODUCTS ----------------
cols = st.columns(3)

for i, p in enumerate(filtered):
    with cols[i % 3]:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        try:
            if p.get("image","").startswith("http"):
                st.image(p["image"])
            else:
                st.image(os.path.join(BASE_DIR, p.get("image","")))
        except:
            st.image("https://via.placeholder.com/300")

        st.subheader(p.get("name"))
        st.caption(p.get("description",""))
        st.write(f"⭐ {p.get('rating',0)}")

        price_dict = p.get("price", {})
        if not price_dict:
            continue

        weight = st.selectbox(
            "Weight",
            list(price_dict.keys()),
            key=f"w_{i}_{p.get('name')}"
        )

        price = price_dict[weight]

        qty = st.number_input(
            "Qty",
            min_value=1,
            max_value=10,
            value=1,
            key=f"q_{i}_{p.get('name')}"
        )

        st.markdown(f"<div class='price'>₹{price} × {qty} = ₹{price * qty}</div>", unsafe_allow_html=True)

        if st.button("🛒 Add to Cart", key=f"a_{i}_{p.get('name')}"):
            st.session_state.cart.append({
                "name": p.get("name"),
                "weight": weight,
                "price": price,
                "qty": qty
            })
            st.success("Added")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CART ----------------
st.sidebar.header("🛒 Cart")

total = 0
order_lines = []
remove_idx = None

for idx, item in enumerate(st.session_state.cart):

    item_total = item["price"] * item.get("qty", 1)
    total += item_total

    st.sidebar.markdown(f"""
    <div class="cart-item">
        <b>{item['name']}</b><br>
        {item['weight']} × {item['qty']} → ₹{item_total}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.sidebar.columns([1,1])

    if col1.button("➖ Remove", key=f"remove_{idx}"):
        remove_idx = idx

    order_lines.append(f"{item['name']} ({item['weight']}) × {item['qty']} = ₹{item_total}")

# SAFE REMOVE
if remove_idx is not None:
    st.session_state.cart.pop(remove_idx)
    st.rerun()

st.sidebar.write("---")
st.sidebar.write(f"**Total: ₹{total}**")

# ---------------- CLEAR CART ----------------
if st.sidebar.button("🧹 Clear Cart"):
    st.session_state.cart = []
    st.rerun()

# ---------------- CUSTOMER DETAILS ----------------
st.sidebar.text_input("Name", key="name")
st.sidebar.text_input("Phone", key="phone")

# ---------------- WHATSAPP (CLEAN FORMAT) ----------------
if total > 0:

    if not st.session_state.phone:
        st.sidebar.warning("Enter phone number to continue")
    else:
        message = "New Order\n\n"

        for line in order_lines:
            message += f"- {line}\n"

        message += f"\nTotal: ₹{total}\n\n"
        message += f"Name: {st.session_state.name}\n"
        message += f"Phone: {st.session_state.phone}\n\n"
        message += "Please share delivery address."

        encoded_message = urllib.parse.quote(message, safe='')

        whatsapp_url = f"https://wa.me/919618862474?text={encoded_message}"

        st.sidebar.markdown(f"[📲 Order via WhatsApp]({whatsapp_url})")