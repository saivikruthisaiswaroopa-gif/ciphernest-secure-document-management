
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Smart Drone Food Delivery</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html {
                scroll-behavior: smooth;
            }

            body {
                font-family: Arial, sans-serif;
                background: #f5f7ff;
                color: #172554;
            }

            /* Navigation bar */
            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 20px;
                padding: 20px 7%;
                background: white;
                box-shadow: 0 3px 15px #17255412;
                position: sticky;
                top: 0;
                z-index: 10;
                flex-wrap: wrap;
            }

            .logo {
                font-size: 23px;
                font-weight: bold;
                color: #26358c;
            }

            .logo span {
                color: #ff6b1a;
            }

            nav a {
                color: #263454;
                text-decoration: none;
                font-weight: bold;
                margin: 5px 8px;
            }

            nav a:hover {
                color: #ff6b1a;
            }

            /* Hero background */
            .hero {
                min-height: 540px;
                display: flex;
                align-items: center;
                padding: 65px 7%;
                background-image:
                    linear-gradient(
                        90deg,
                        rgba(255,255,255,0.97) 0%,
                        rgba(255,255,255,0.87) 43%,
                        rgba(255,255,255,0.10) 100%
                    ),
                    url("https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=1800&q=85");
                background-size: cover;
                background-position: center;
            }

            .hero-content {
                max-width: 600px;
            }

            .tag {
                display: inline-block;
                padding: 9px 15px;
                background: #fff0e6;
                color: #e85c0d;
                border-radius: 25px;
                font-weight: bold;
                margin-bottom: 22px;
            }

            h1 {
                font-size: clamp(38px, 5vw, 62px);
                line-height: 1.12;
                margin-bottom: 20px;
            }

            h1 span {
                color: #ff6b1a;
            }

            .hero p {
                font-size: 18px;
                line-height: 1.8;
                color: #40506c;
                margin-bottom: 25px;
            }

            .btn {
                display: inline-block;
                background: #ff6b1a;
                color: white;
                padding: 15px 27px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                border: none;
                cursor: pointer;
                transition: 0.2s;
            }

            .btn:hover {
                background: #e95408;
                transform: translateY(-2px);
            }

            /* Features */
            .features {
                padding: 55px 7%;
                text-align: center;
            }

            .section-title {
                font-size: 32px;
                margin-bottom: 12px;
            }

            .subtitle {
                color: #64748b;
                margin-bottom: 32px;
                line-height: 1.7;
            }

            .feature-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
            }

            .feature-card {
                background: white;
                padding: 27px 18px;
                border-radius: 16px;
                box-shadow: 0 5px 22px #1725540c;
                transition: 0.2s;
            }

            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 28px #17255418;
            }

            .feature-icon {
                font-size: 36px;
                margin-bottom: 15px;
            }

            .feature-card h3 {
                margin-bottom: 10px;
            }

            .feature-card p {
                color: #64748b;
                line-height: 1.6;
                font-size: 14px;
            }

            /* Food showcase */
            .food-section {
                padding: 55px 7%;
                background: white;
                text-align: center;
            }

            .food-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 24px;
                margin-top: 30px;
            }

            .food-card {
                overflow: hidden;
                background: #fff;
                border: 1px solid #e8ebf3;
                border-radius: 16px;
                text-align: left;
                box-shadow: 0 5px 20px #1725540b;
            }

            .food-card img {
                display: block;
                width: 100%;
                height: 210px;
                object-fit: cover;
            }

            .food-info {
                padding: 20px;
            }

            .food-info p {
                color: #64748b;
                margin: 10px 0;
                line-height: 1.6;
            }

            .price {
                color: #e85c0d;
                font-size: 20px;
                font-weight: bold;
            }

            /* Footer */
            footer {
                background: #172554;
                color: white;
                text-align: center;
                padding: 28px 15px;
                line-height: 1.8;
            }

            footer span {
                color: #ff914d;
            }

           
            .add-cart {
                margin-top: 15px;
                font-size: 14px;
            }

            #cart-items {
                max-width: 600px;
                margin: 20px auto;
                text-align: left;
            }

            .cart-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                padding: 14px;
                margin-bottom: 10px;
                background: #f5f7ff;
                border-radius: 10px;
            }

            .cart-row button {
                padding: 5px 10px;
                border: 0;
                border-radius: 5px;
                cursor: pointer;
            }

            #order-form label {
                display: block;
                margin: 15px 0 7px;
                font-weight: bold;
            }

            #order-form input,
            #order-form textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #d7ddec;
                border-radius: 8px;
                font: inherit;
            }

            #order-form textarea {
                min-height: 85px;
                resize: vertical;
            }

            /* Restaurant cards use the existing food-card design */
            .restaurant-section {
                padding: 55px 7%;
                text-align: center;
            }

            .restaurant-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 24px;
                margin-top: 30px;
            }

            .restaurant-card {
                overflow: hidden;
                background: #fff;
                border: 1px solid #e8ebf3;
                border-radius: 16px;
                text-align: left;
                box-shadow: 0 5px 20px #1725540b;
            }

            .restaurant-card img {
                display: block;
                width: 100%;
                height: 210px;
                object-fit: cover;
            }

            .restaurant-info {
                padding: 20px;
            }

            .restaurant-info p {
                color: #64748b;
                margin: 10px 0;
                line-height: 1.6;
            }

            .restaurant-info .btn {
                margin-top: 8px;
            }

            .menu-notice {
                max-width: 900px;
                margin: 0 auto 18px;
                color: #64748b;
                font-size: 14px;
                line-height: 1.6;
            }

            @media (max-width: 800px) {
                .restaurant-grid {
                    grid-template-columns: 1fr;
                }
            }

            @media (max-width: 800px) {
                nav {
                    justify-content: center;
                }

                .feature-grid {
                    grid-template-columns: repeat(2, 1fr);
                }

                .food-grid {
                    grid-template-columns: 1fr;
                }

                .hero {
                    padding: 55px 6%;
                    background-position: 60% center;
                }
            }

            @media (max-width: 480px) {
                .feature-grid {
                    grid-template-columns: 1fr;
                }

                nav a {
                    font-size: 14px;
                }
            }
            .add-cart {
                display: inline-block;
                margin-top: 15px;
                background: #ff6b1a;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
            }

            .add-cart:hover {
                background: #e95408;
            }
        </style>
    </head>

    <body>

        <nav>
            <div class="logo">🚁 Smart<span>Drone Eats</span></div>

            <div>
                <a href="#home">Home</a>
                <a href="#features">Features</a>
                <a href="#restaurants">Restaurants</a>\n                <a href="#food">Food</a>
            </div>
        </nav>

        <section class="hero" id="home">
            <div class="hero-content">

                <div class="tag">🚀 THE FUTURE OF FOOD DELIVERY</div>

                <h1>
                    Smart Drone<br>
                    <span>Food Delivery</span>
                </h1>

                <p>
                    Your favorite food, delivered smarter!
                    Our intelligent system selects suitable drones,
                    checks delivery safety, and optimizes routes
                    using AI-based optimization algorithms.
                </p>

                <a class="btn" href="#food">Explore Food &rarr;</a>

            </div>
        </section>

        <section class="features" id="features">

            <h2 class="section-title">Why Choose Smart Drone Delivery?</h2>

            <p class="subtitle">
                Technology that makes food delivery smarter, safer,
                and more efficient.
            </p>

            <div class="feature-grid">

                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Fast Delivery</h3>
                    <p>Optimize delivery routes to reduce travel distance
                    and estimated delivery time.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <h3>AI Route Optimization</h3>
                    <p>Use Genetic Algorithm and Simulated Annealing
                    to find efficient delivery sequences.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <h3>Safety Checks</h3>
                    <p>Check package weight, drone payload capacity,
                    battery availability, and flight range.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">📍</div>
                    <h3>Smart Tracking</h3>
                    <p>Display delivery status and planned routes
                    through our website.</p>
                </div>

            </div>
        </section>

        <section class="restaurant-section" id="restaurants">
            <h2 class="section-title">Restaurants in Ongole 🍽️</h2>
            <p class="subtitle">
                Choose a restaurant to explore its menu and add food to your cart.
            </p>

            <div class="restaurant-grid">
                <div class="restaurant-card">
                    <img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80"
                         alt="Pizza and sides">
                    <div class="restaurant-info">
                        <h3>Pizza Hut</h3>
                        <p>Pizza, garlic bread and sides</p>
                        <p>Ongole, Andhra Pradesh 523001</p>
                        <button class="btn" type="button" onclick="selectRestaurant('Pizza Hut')">View Menu</button>
                    </div>
                </div>

                <div class="restaurant-card">
                    <img src="https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=800&q=80"
                         alt="Spiced rice platter">
                    <div class="restaurant-info">
                        <h3>Afzaan Mandi Restaurant</h3>
                        <p>Mandi, biryani and starters</p>
                        <p>Ongole, Andhra Pradesh 523001</p>
                        <button class="btn" type="button" onclick="selectRestaurant('Afzaan Mandi Restaurant')">View Menu</button>
                    </div>
                </div>

                <div class="restaurant-card">
                    <img src="https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=800&q=80"
                         alt="Biryani">
                    <div class="restaurant-info">
                        <h3>Biryanis and More</h3>
                        <p>Biryani, rice dishes and starters</p>
                        <p>Ongole, Andhra Pradesh 523001</p>
                        <button class="btn" type="button" onclick="selectRestaurant('Biryanis and More')">View Menu</button>
                    </div>
                </div>

                <div class="restaurant-card">
                    <img src="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80"
                         alt="Indian restaurant curry">
                    <div class="restaurant-info">
                        <h3>V Grand Family Restaurant</h3>
                        <p>Andhra dishes, biryani and Chinese food</p>
                        <p>Ongole, Andhra Pradesh 523001</p>
                        <button class="btn" type="button" onclick="selectRestaurant('V Grand Family Restaurant')">View Menu</button>
                    </div>
                </div>

                <div class="restaurant-card">
                    <img src="https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=800&q=80"
                         alt="Vegetable biryani">
                    <div class="restaurant-info">
                        <h3>Panthulu Gari Mess</h3>
                        <p>Traditional Andhra vegetarian meals</p>
                        <p>Ongole, Andhra Pradesh 523001</p>
                        <button class="btn" type="button" onclick="selectRestaurant('Panthulu Gari Mess')">View Menu</button>
                    </div>
                </div>
            </div>
        </section>

        <section class="food-section" id="food">
            <h2 class="section-title" id="menu-title">Popular Food Choices 🍔</h2>
            <p class="subtitle" id="menu-subtitle">
                Choose a restaurant above to see its food menu. The initial popular items are sample project items.
            </p>
            <p class="menu-notice">
                Project prototype: menu items and prices are sample data and are not confirmed live restaurant menus.
            </p>

            <div class="food-grid" id="food-grid">
                <div class="food-card">
                    <img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80"
                         alt="Burger">
                    <div class="food-info">
                        <h3>Classic Burger</h3>
                        <p>Fresh, delicious, and ready for delivery.</p>
                        <div class="price">₹149</div>
                        <button class="btn add-cart" onclick="addToCart('Classic Burger', 149)">Add to Cart</button>
                    </div>
                </div>

                <div class="food-card">
                    <img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80"
                         alt="Pizza">
                    <div class="food-info">
                        <h3>Cheese Pizza</h3>
                        <p>A tasty favorite from your local restaurant.</p>
                        <div class="price">₹249</div>
                        <button class="btn add-cart" onclick="addToCart('Cheese Pizza', 249)">Add to Cart</button>
                    </div>
                </div>

                <div class="food-card">
                    <img src="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80"
                         alt="Noodles">
                    <div class="food-info">
                        <h3>Delicious Noodles</h3>
                        <p>A satisfying meal packed for delivery.</p>
                        <div class="price">₹129</div>
                        <button class="btn add-cart" onclick="addToCart('Delicious Noodles', 129)">Add to Cart</button>
                    </div>
                </div>
            </div>
        </section>

        <section class="food-section" id="checkout">
                <h2 class="section-title">Your Food Cart 🛒</h2>
                <p class="subtitle">Review your order and enter delivery details.</p>

                <div id="cart-items">
                    <p>Your cart is empty. Add food items above!</p>
                </div>

                 <h3 id="cart-total">Total: ₹0</h3>

            <form id="order-form"
                    style="max-width:600px;margin:25px auto;text-align:left;">

                <label for="restaurant">Restaurant pickup location</label>
                <input id="restaurant" name="restaurant"
                    required placeholder="Restaurant name and address">

                <label for="customer">Customer name</label>
                <input id="customer" name="customer"
                    required placeholder="Enter your name">

                <label for="phone">Phone number</label>
                <input id="phone" name="phone" type="tel"
                    required placeholder="Enter your phone number">

                <label for="address">Delivery address</label>
                <textarea id="address" name="address"
                    required placeholder="Enter your complete delivery address"></textarea>

                <label for="notes">Delivery instructions (optional)</label>
                <textarea id="notes" name="notes"
                    placeholder="Landmark or other instructions"></textarea>

                <button class="btn" type="submit">Place Food Order</button>
                <p id="order-message" role="status"></p>
            </form>
        </section>
        <footer>
            <h3>🚁 Smart Drone Food Delivery</h3>
            <p>Smarter routes. Better delivery. A smarter future.</p>
            <p>Final-Year Project | AI-Based Route Optimization</p>
            <p>&copy; 2026 Smart Drone Food Delivery</p>
        </footer>

        <script>
        const cart = {};
        let selectedRestaurant = "Popular Menu";

        const restaurantMenus = {
            "Pizza Hut": [
                {name: "Margherita Pizza", price: 199, image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80", description: "Classic cheese and tomato pizza."},
                {name: "Farmhouse Pizza", price: 279, image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80", description: "Pizza topped with vegetables and cheese."},
                {name: "Cheese Pizza", price: 229, image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80", description: "Pizza topped with melted cheese."}
            ],
            "Afzaan Mandi Restaurant": [
                {name: "Chicken Biryani", price: 299, image: "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=800&q=80", description: "Spiced rice served with chicken."},
                {name: "Mutton Curry", price: 379, image: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80", description: "Rich Indian-style curry served as a meal option."},
                {name: "Chicken Starter", price: 199, image: "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80", description: "A sample starter item."}
            ],
            "Biryanis and More": [
                {name: "Chicken Biryani", price: 229, image: "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=800&q=80", description: "Aromatic rice with chicken."},
                {name: "Veg Biryani", price: 169, image: "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=800&q=80", description: "Spiced rice with vegetables."},
                {name: "Paneer Curry", price: 189, image: "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80", description: "Paneer cooked in a rich Indian-style curry."}
            ],
            "V Grand Family Restaurant": [
                {name: "Andhra Chicken Curry Meal", price: 249, image: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80", description: "Sample Andhra-style meal."},
                {name: "Chicken Fried Rice", price: 189, image: "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=800&q=80", description: "Fried rice with chicken."},
                {name: "Veg Noodles", price: 149, image: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80", description: "Noodles with vegetables."}
            ],
            "Panthulu Gari Mess": [
                {name: "Andhra Veg Meals", price: 120, image: "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80", description: "Sample traditional vegetarian meal."},
                {name: "Vegetable Biryani", price: 80, image: "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=800&q=80", description: "Rice cooked with vegetables and spices."},
                {name: "Veg Curry with Rice", price: 110, image: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80", description: "Vegetarian curry served with rice."}
            ]
        };

        function selectRestaurant(name) {
            if (Object.keys(cart).length > 0 && selectedRestaurant !== name) {
                const shouldSwitch = confirm(
                    "Your cart contains items from " + selectedRestaurant +
                    ". Switching restaurants will clear your current cart. Continue?"
                );
                if (!shouldSwitch) return;
                for (const key of Object.keys(cart)) delete cart[key];
                renderCart();
            }

            selectedRestaurant = name;
            document.getElementById("restaurant").value = name + ", Ongole, Andhra Pradesh 523001";
            document.getElementById("menu-title").textContent = name + " — Menu";
            document.getElementById("menu-subtitle").textContent =
                "Select food items from " + name + " and add them to your cart.";
            renderMenu(name);
            document.getElementById("food").scrollIntoView({behavior: "smooth"});
        }

        function renderMenu(restaurantName) {
            const menu = restaurantMenus[restaurantName] || [];
            const grid = document.getElementById("food-grid");
            grid.innerHTML = menu.map(item => `
                <div class="food-card">
                    <img src="${item.image}" alt="${item.name}">
                    <div class="food-info">
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                        <div class="price">₹${item.price}</div>
                        <button class="btn add-cart" type="button"
                            onclick="addToCart('${item.name.replace(/'/g, "\\'")}', ${item.price}, '${restaurantName.replace(/'/g, "\\'")}')">
                            Add to Cart
                        </button>
                    </div>
                </div>
            `).join("");
        }

        function addToCart(name, price, restaurantName) {
            const itemRestaurant = restaurantName || selectedRestaurant;
            if (Object.keys(cart).length > 0 && selectedRestaurant !== itemRestaurant) {
                alert("Please order from one restaurant at a time.");
                return;
            }
            selectedRestaurant = itemRestaurant;
            if (cart[name]) {
                cart[name].quantity += 1;
            } else {
                cart[name] = {price: price, quantity: 1, restaurant: itemRestaurant};
            }
            if (itemRestaurant !== "Popular Menu") {
                document.getElementById("restaurant").value =
                    itemRestaurant + ", Ongole, Andhra Pradesh 523001";
            }
            renderCart();
        }

        function changeQuantity(name, change) {
            if (!cart[name]) return;
            cart[name].quantity += change;
            if (cart[name].quantity <= 0) delete cart[name];
            renderCart();
        }

        function renderCart() {
            const container = document.getElementById("cart-items");
            const totalElement = document.getElementById("cart-total");
            const entries = Object.entries(cart);

            if (entries.length === 0) {
                container.innerHTML = "<p>Your cart is empty. Add food items above!</p>";
                totalElement.textContent = "Total: ₹0";
                return;
            }

            let total = 0;
            container.innerHTML = entries.map(([name, item]) => {
                const subtotal = item.price * item.quantity;
                total += subtotal;
                return `
                    <div class="cart-row">
                        <div>
                            <strong>${name}</strong><br>
                            ₹${item.price} × ${item.quantity} = ₹${subtotal}
                        </div>
                        <div>
                            <button type="button" onclick="changeQuantity('${name.replace(/'/g, "\\'")}', -1)">−</button>
                            <span>${item.quantity}</span>
                            <button type="button" onclick="changeQuantity('${name.replace(/'/g, "\\'")}', 1)">+</button>
                        </div>
                    </div>
                `;
            }).join("");
            totalElement.textContent = "Total: ₹" + total;
        }

        document.getElementById("order-form").addEventListener("submit", function(event) {
            event.preventDefault();
            const message = document.getElementById("order-message");

            if (Object.keys(cart).length === 0) {
                message.textContent = "Please add at least one food item to your cart.";
                return;
            }

            const form = new FormData(this);
            const items = Object.entries(cart).map(([name, item]) => ({
                name: name,
                price: item.price,
                quantity: item.quantity
            }));
            const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

            message.textContent = "Order details validated! Restaurant: " +
                (selectedRestaurant) + ". Total: ₹" + total +
                ". Database order placement will be connected in the next step.";
        });
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
