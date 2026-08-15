import streamlit as st
import requests

API_URL = "https://fakestoreapi.com/products"

st.set_page_config(
    page_title="Fake Store Products",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Fake Store Products")

with st.spinner("Loading products..."):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        products = response.json()
    except requests.RequestException:
        st.error("Failed to load products")
        st.stop()

categories = sorted(set(product["category"] for product in products))
categories.insert(0, "All")

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

max_price = max(product["price"] for product in products)

selected_price = st.sidebar.slider(
    "Maximum Price",
    min_value=0.0,
    max_value=float(max_price),
    value=float(max_price),
    step=1.0
)

search = st.sidebar.text_input(
    "Search"
)

filtered_products = products

if selected_category != "All":
    filtered_products = [
        product
        for product in filtered_products
        if product["category"] == selected_category
    ]

filtered_products = [
    product
    for product in filtered_products
    if product["price"] <= selected_price
]

if search:
    search = search.lower()

    filtered_products = [
        product
        for product in filtered_products
        if search in product["title"].lower()
        or search in product["description"].lower()
    ]

st.subheader(f"Products found: {len(filtered_products)}")

for product in filtered_products:
    st.image(
        product["image"],
        width=200
    )

    st.subheader(product["title"])

    st.write(f"**ID:** {product['id']}")
    st.write(f"**Price:** ${product['price']}")
    st.write(f"**Category:** {product['category']}")
    st.write(f"**Rating:** {product['rating']['rate']} ⭐")
    st.write(f"**Rating count:** {product['rating']['count']}")

    with st.expander("View details"):
        st.write(f"**Description:** {product['description']}")
        st.write(f"**Image URL:** {product['image']}")

    st.divider()