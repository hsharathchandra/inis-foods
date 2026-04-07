from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# ---------------- DB ----------------
engine = create_engine("sqlite:///data.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------- MODELS ----------------
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    price = Column(JSON)
    rating = Column(Integer)
    image = Column(String)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    items = Column(JSON)
    total = Column(Integer)
    status = Column(String)

Base.metadata.create_all(bind=engine)

# ---------------- SCHEMAS ----------------
class ProductIn(BaseModel):
    name: str
    category: str
    description: str
    price: Dict[str, int]
    rating: float
    image: str

class OrderIn(BaseModel):
    name: str
    phone: str
    items: List[dict]
    total: int

# ---------------- SEED ----------------
def seed_products():
    db = Session()

    if db.query(Product).count() == 0:
        products = [
            # ---------------- NON-VEG PICKLES ----------------
    {
        "name": "Chicken Pickle boneless",
        "category": "Non-Veg",
        "description": "Rich and spicy boneless chicken pickle with authentic Andhra flavors.",
        "price": {"250g": 350, "500g": 700, "1kg": 1400},
        "rating": 4.7,
        "image": "images/chicken_boneless.jpg"
    },
    {
        "name": "Chicken Pickle bone",
        "category": "Non-Veg",
        "description": "Traditional chicken pickle with bone for enhanced flavor.",
        "price": {"250g": 320, "500g": 640, "1kg": 1280},
        "rating": 4.6,
        "image": "images/Chicken-Bone.jpg"
    },
    {
        "name": "Chicken Tokku Pachadi",
        "category": "Non-Veg",
        "description": "Spicy shredded chicken tokku prepared in Andhra style.",
        "price": {"250g": 350, "500g": 700, "1kg": 1400},
        "rating": 4.6,
        "image": "images/chickenthokku.jpg"
    },
    {
        "name": "Chicken Gongura Pickle",
        "category": "Non-Veg",
        "description": "Tangy gongura blended with spicy chicken pickle.",
        "price": {"250g": 400, "500g": 800, "1kg": 1600},
        "rating": 4.8,
        "image": "images/Gongura-Chicken.jpg"
    },
    {
        "name": "Mutton Pickle boneless",
        "category": "Non-Veg",
        "description": "Premium boneless mutton pickle with rich spices.",
        "price": {"250g": 550, "500g": 1100, "1kg": 2200},
        "rating": 4.8,
        "image": "images/Mutton.jpg"
    },
    {
        "name": "Prawns Pickle",
        "category": "Non-Veg",
        "description": "Delicious prawn pickle with coastal Andhra flavors.",
        "price": {"250g": 500, "500g": 1000, "1kg": 2000},
        "rating": 4.7,
        "image": "images/Prawns.jpg"
    },

    # ---------------- VEG PICKLES ----------------
    {
        "name": "Mango Avakaya",
        "category": "Veg",
        "description": "Classic Andhra mango avakaya with bold spices.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.9,
        "image": "images/Avakaya.jpg"
    },
    {
        "name": "Usiri Kaaya Pickle",
        "category": "Veg",
        "description": "Healthy gooseberry pickle with tangy taste.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.5,
        "image": "images/usirikaya.jpg"
    },
    {
        "name": "Tomato Pickle",
        "category": "Veg",
        "description": "Spicy tomato pickle with rich masala blend.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.5,
        "image": "images/Tomato-Pickle.jpg"
    },
    {
        "name": "Gongura Pickle",
        "category": "Veg",
        "description": "Authentic tangy gongura leaf pickle.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.8,
        "image": "images/gongura.jpg"
    },
    {
        "name": "Gongura Pandu Mirchi Pickle",
        "category": "Veg",
        "description": "Spicy gongura with red chilli fusion.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.6,
        "image": "images/gpm.jpg"
    },
    {
        "name": "Dosakaya Pickle",
        "category": "Veg",
        "description": "Traditional yellow cucumber pickle.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.5,
        "image": "images/dosaka.jpg"
    },
    {
        "name": "Mullakaya Pickle",
        "category": "Veg",
        "description": "Drumstick pickle with unique earthy flavor.",
        "price": {"250g": 210, "500g": 420, "1kg": 840},
        "rating": 4.4,
        "image": "images/drums.png"
    },
    {
        "name": "Chikkudu kaya Pickle",
        "category": "Veg",
        "description": "Flat beans pickle with spicy seasoning.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.4,
        "image": "images/chikkudu.png"
    },
    {
        "name": "Kaakara Kaaya Pickle",
        "category": "Veg",
        "description": "Bitter gourd pickle with bold spices.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.3,
        "image": "images/Kakarakaya.jpg"
    },
    {
        "name": "Cauliflower Pickle",
        "category": "Veg",
        "description": "Spicy cauliflower pickle with rich masala.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.4,
        "image": "images/gobi.jpg"
    },
    {
        "name": "Lemon Pickle",
        "category": "Veg",
        "description": "Classic tangy lemon pickle.",
        "price": {"250g": 200, "500g": 400, "1kg": 800},
        "rating": 4.7,
        "image": "images/lemon.jpg"
    },
    {
        "name": "Green Chilli Pickle",
        "category": "Veg",
        "description": "Hot and spicy green chilli pickle.",
        "price": {"250g": 180, "500g": 360, "1kg": 720},
        "rating": 4.6,
        "image": "images/Green-Chilli-Pickle.jpg"
    },

    # ---------------- SPICE POWDERS ----------------
    {
        "name": "Vellulli Karam",
        "category": "Spices",
        "description": "Garlic spice powder with bold Andhra taste.",
        "price": {"250g": 60, "500g": 120, "1kg": 240},
        "rating": 4.7,
        "image": "images/VELLULLI-KARAM.jpg"
    },
    {
        "name": "Kobbari Karam Podi",
        "category": "Spices",
        "description": "Coconut spice powder with rich aroma.",
        "price": {"250g": 65, "500g": 130, "1kg": 260},
        "rating": 4.6,
        "image": "images/Kobbari.jpg"
    },
    {
        "name": "Palli Karam Podi",
        "category": "Spices",
        "description": "Peanut spice powder with crunchy flavor.",
        "price": {"250g": 60, "500g": 120, "1kg": 240},
        "rating": 4.7,
        "image": "images/PALLI-KARAM.jpg"
    },
    {
        "name": "Idli Karam Podi",
        "category": "Spices",
        "description": "Perfect podi for idli and dosa.",
        "price": {"250g": 60, "500g": 120, "1kg": 240},
        "rating": 4.8,
        "image": "images/Idli.jpg"
    },
    {
        "name": "Karvepaaku Podi",
        "category": "Spices",
        "description": "Curry leaf powder rich in aroma.",
        "price": {"250g": 70, "500g": 140, "1kg": 280},
        "rating": 4.6,
        "image": "images/Karvepaaku.jpg"
    },
    {
        "name": "Beetroot Podi",
        "category": "Spices",
        "description": "Healthy beetroot spice powder.",
        "price": {"250g": 100, "500g": 200, "1kg": 400},
        "rating": 4.5,
        "image": "images/beetroot.jpg"
    },
    {
        "name": "Carrot Podi",
        "category": "Spices",
        "description": "Nutritious carrot spice powder.",
        "price": {"250g": 100, "500g": 200, "1kg": 400},
        "rating": 4.5,
        "image": "images/carrot-powder.jpg"
    },
    {
        "name": "Putnalu Karam",
        "category": "Spices",
        "description": "Roasted gram spice powder.",
        "price": {"250g": 60, "500g": 120, "1kg": 240},
        "rating": 4.6,
        "image": "images/Putnala-Podi.jpg"
    },
    {
        "name": "Dry Prawns Podi",
        "category": "Non-Veg",
        "description": "Flavorful dry prawns spice powder.",
        "price": {"250g": 110, "500g": 220, "1kg": 440},
        "rating": 4.8,
        "image": "images/Prawnspodi.jpg"
    }

        ]

        for p in products:
            db.add(Product(**p))

        db.commit()

seed_products()

# ---------------- PRODUCTS ----------------
@app.get("/products")
def get_products():
    db = Session()
    products = db.query(Product).all()

    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "description": p.description,
            "price": p.price,
            "rating": p.rating,
            "image": p.image
        })

    return result

@app.post("/products")
def add_product(product: ProductIn):
    db = Session()

    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()

    return {"message": "Product added"}

# ---------------- ORDERS ----------------
@app.get("/orders")
def get_orders():
    db = Session()
    orders = db.query(Order).all()

    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "name": o.name,
            "phone": o.phone,
            "items": o.items,
            "total": o.total,
            "status": o.status
        })

    return result

@app.post("/orders")
def create_order(order: OrderIn):
    db = Session()

    new_order = Order(
        name=order.name,
        phone=order.phone,
        items=order.items,
        total=order.total,
        status="Pending"
    )

    db.add(new_order)
    db.commit()

    return {"message": "Order placed"}

@app.put("/orders/{order_id}")
def update_order(order_id: int, status: str):
    db = Session()

    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(404)

    order.status = status
    db.commit()

    return {"message": "Updated"}

