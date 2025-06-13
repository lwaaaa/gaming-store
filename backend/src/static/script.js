// Gaming Store JavaScript

// Cart functionality
let cart = [];
let cartTotal = 0;
let currentUser = null;

// Initialize the application
document.addEventListener("DOMContentLoaded", function() {
    initializeEventListeners();
    loadCartFromStorage();
    loadUserFromStorage();
    updateCartDisplay();
    updateUserDisplay();
    loadProducts(); // Load games and accessories on page load
});

// Initialize event listeners
function initializeEventListeners() {
    // Navigation smooth scrolling
    const navLinks = document.querySelectorAll("header nav ul li a");
    navLinks.forEach(link => {
        link.addEventListener("click", handleSmoothScroll);
    });

    // CTA button
    const ctaButton = document.querySelector(".hero .btn");
    if (ctaButton) {
        ctaButton.addEventListener("click", scrollToGames);
    }

    // Login/Register modals
    const loginBtn = document.getElementById("login-btn");
    const cartBtn = document.getElementById("cart-btn");
    const loginModal = document.getElementById("login-modal");
    const registerModal = document.getElementById("register-modal");
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const registerLink = document.getElementById("register-link");
    const loginLink = document.getElementById("login-link");

    // Modal event listeners
    loginBtn.addEventListener("click", () => {
        if (currentUser) {
            logout();
        } else {
            showModal(loginModal);
        }
    });

    cartBtn.addEventListener("click", showCart);

    registerLink.addEventListener("click", (e) => {
        e.preventDefault();
        hideModal(loginModal);
        showModal(registerModal);
    });

    loginLink.addEventListener("click", (e) => {
        e.preventDefault();
        hideModal(registerModal);
        showModal(loginModal);
    });

    // Close modals
    document.querySelectorAll(".close").forEach(closeBtn => {
        closeBtn.addEventListener("click", (e) => {
            hideModal(e.target.closest(".modal"));
        });
    });

    // Close modal on background click
    document.querySelectorAll(".modal").forEach(modal => {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                hideModal(modal);
            }
        });
    });

    // Form submissions
    loginForm.addEventListener("submit", handleLogin);
    registerForm.addEventListener("submit", handleRegister);
}

// User authentication functions
async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const loginData = {
        email: formData.get("email"),
        password: formData.get("password")
    };

    try {
        const response = await fetch("/api/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();

        if (result.success) {
            currentUser = result.user;
            saveUserToStorage();
            updateUserDisplay();
            hideModal(document.getElementById("login-modal"));
            showNotification("تم تسجيل الدخول بنجاح!", "success");
        } else {
            showNotification(result.message || "فشل في تسجيل الدخول", "error");
        }
    } catch (error) {
        showNotification("حدث خطأ في الاتصال", "error");
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const registerData = {
        name: formData.get("name"),
        email: formData.get("email"),
        password: formData.get("password"),
        phone: formData.get("phone")
    };

    try {
        const response = await fetch("/api/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(registerData)
        });

        const result = await response.json();

        if (result.success) {
            currentUser = result.user;
            saveUserToStorage();
            updateUserDisplay();
            hideModal(document.getElementById("register-modal"));
            showNotification("تم إنشاء الحساب بنجاح!", "success");
        } else {
            showNotification(result.message || "فشل في إنشاء الحساب", "error");
        }
    } catch (error) {
        showNotification("حدث خطأ في الاتصال", "error");
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem("gamingStoreUser");
    updateUserDisplay();
    showNotification("تم تسجيل الخروج بنجاح!", "success");
}

function saveUserToStorage() {
    localStorage.setItem("gamingStoreUser", JSON.stringify(currentUser));
}

function loadUserFromStorage() {
    const savedUser = localStorage.getItem("gamingStoreUser");
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
    }
}

function updateUserDisplay() {
    const loginBtn = document.getElementById("login-btn");
    if (currentUser) {
        loginBtn.textContent = `مرحباً ${currentUser.name} | تسجيل الخروج`;
        loginBtn.classList.add("logged-in");
    } else {
        loginBtn.textContent = "تسجيل الدخول";
        loginBtn.classList.remove("logged-in");
    }
}

// Modal functions
function showModal(modal) {
    modal.style.display = "flex";
}

function hideModal(modal) {
    modal.style.display = "none";
}

// Load products (games and accessories)
async function loadProducts() {
    const gamesContainer = document.getElementById("games-container");
    const accessoriesContainer = document.getElementById("accessories-container");

    // Fetch games
    try {
        const gamesResponse = await fetch("/api/games");
        if (gamesResponse.ok) {
            const gamesData = await gamesResponse.json();
            if (gamesData.success) {
                gamesData.games.forEach(game => {
                    gamesContainer.innerHTML += createProductCard(game, "game");
                });
            }
        }
    } catch (error) {
        console.error("Error loading games:", error);
    }

    // Fetch accessories
    try {
        const accessoriesResponse = await fetch("/api/accessories");
        if (accessoriesResponse.ok) {
            const accessoriesData = await accessoriesResponse.json();
            if (accessoriesData.success) {
                accessoriesData.accessories.forEach(accessory => {
                    accessoriesContainer.innerHTML += createProductCard(accessory, "accessory");
                });
            }
        }
    } catch (error) {
        console.error("Error loading accessories:", error);
    }

    // Add to cart buttons after products are loaded
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    addToCartButtons.forEach(button => {
        button.addEventListener("click", handleAddToCart);
    });

    // Animate products
    animateProducts();
}

// Create product card HTML
function createProductCard(product, type) {
    return `
        <div class="product-card ${type}-card">
            <img src="/static/${product.image}" alt="${product.name}" onerror="this.src='/static/placeholder.jpg'">
            <h3>${product.name}</h3>
            <p class="price">${product.price} ريال</p>
            <button class="add-to-cart" data-id="${product.id}" data-type="${type}">أضف إلى السلة</button>
        </div>
    `;
}

// Handle add to cart
function handleAddToCart(event) {
    const button = event.target;
    const card = button.closest(".product-card");
    
    if (card) {
        const name = card.querySelector("h3").textContent;
        const priceText = card.querySelector(".price").textContent;
        const price = parseInt(priceText.replace(/[^\d]/g, ""));
        const id = button.dataset.id;
        const type = button.dataset.type;
        
        const item = {
            id: id,
            name: name,
            price: price,
            quantity: 1,
            type: type
        };
        
        addToCart(item);
        showAddToCartAnimation(button);
    }
}

// Add item to cart
function addToCart(item) {
    // Check if item already exists
    const existingItem = cart.find(cartItem => cartItem.id === item.id && cartItem.type === item.type);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push(item);
    }
    
    updateCartTotal();
    saveCartToStorage();
    updateCartDisplay();
    
    // Show success message
    showNotification(`تم إضافة ${item.name} إلى السلة!`, "success");
}

// Update cart total
function updateCartTotal() {
    cartTotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

// Save cart to localStorage
function saveCartToStorage() {
    localStorage.setItem("gamingStoreCart", JSON.stringify(cart));
    localStorage.setItem("gamingStoreCartTotal", cartTotal.toString());
}

// Load cart from localStorage
function loadCartFromStorage() {
    const savedCart = localStorage.getItem("gamingStoreCart");
    const savedTotal = localStorage.getItem("gamingStoreCartTotal");
    
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
    
    if (savedTotal) {
        cartTotal = parseInt(savedTotal);
    }
}

// Update cart display
function updateCartDisplay() {
    const cartCount = document.getElementById("cart-count");
    cartCount.textContent = cart.length;
}

// Show cart
function showCart() {
    if (cart.length === 0) {
        showNotification("السلة فارغة!", "info");
        return;
    }
    
    let cartHTML = 
        `<div style="background: white; padding: 20px; border-radius: 10px; max-width: 400px;">
            <h3 style="margin-bottom: 15px; color: #333;">سلة التسوق</h3>`;
    
    cart.forEach(item => {
        cartHTML += `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding: 10px; border: 1px solid #eee; border-radius: 5px;">
                <div>
                    <strong>${item.name}</strong><br>
                    <small>الكمية: ${item.quantity}</small>
                </div>
                <div style="color: #667eea; font-weight: bold;">
                    ${item.price * item.quantity} ريال
                </div>
            </div>
        `;
    });
    
    cartHTML += `
        <div style="border-top: 2px solid #667eea; padding-top: 15px; margin-top: 15px;">
            <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: bold;">
                <span>المجموع:</span>
                <span style="color: #667eea;">${cartTotal} ريال</span>
            </div>
            <button onclick="checkout()" style="width: 100%; margin-top: 15px; background: #667eea; color: white; padding: 12px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">
                إتمام الشراء
            </button>
        </div>
    `;
    cartHTML += `</div>`;
    
    showModalContent(cartHTML);
}

// Checkout function
async function checkout() {
    if (!currentUser) {
        showNotification("يرجى تسجيل الدخول أولاً لإتمام الشراء", "error");
        closeModalContent();
        showModal(document.getElementById("login-modal"));
        return;
    }

    const orderData = {
        user_id: currentUser.id,
        items: cart,
        total: cartTotal,
        customer_info: {
            name: currentUser.name,
            email: currentUser.email,
            phone: currentUser.phone
        }
    };

    try {
        const response = await fetch("/api/orders", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(orderData)
        });

        const result = await response.json();

        if (result.success) {
            showNotification("تم إرسال طلبك بنجاح! سيتم التواصل معك قريباً.", "success");
            cart = [];
            cartTotal = 0;
            saveCartToStorage();
            updateCartDisplay();
            closeModalContent();
        } else {
            showNotification(result.message || "فشل في إرسال الطلب", "error");
        }
    } catch (error) {
        showNotification("حدث خطأ في الاتصال", "error");
    }
}

// Handle smooth scrolling
function handleSmoothScroll(event) {
    event.preventDefault();
    const targetId = event.target.getAttribute("href");
    const targetSection = document.querySelector(targetId);
    
    if (targetSection) {
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

// Scroll to games section
function scrollToGames() {
    const gamesSection = document.querySelector("#games");
    if (gamesSection) {
        gamesSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

// Show add to cart animation
function showAddToCartAnimation(button) {
    const originalText = button.textContent;
    button.textContent = "تم الإضافة ✓";
    button.style.background = "#28a745";
    
    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = "";
    }, 1500);
}

// Show notification
function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === "success" ? "#28a745" : type === "error" ? "#dc3545" : "#17a2b8"};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        z-index: 10000;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = "translateX(0)";
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = "translateX(100%)";
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Show modal content
function showModalContent(content) {
    const modal = document.createElement("div");
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;
    
    modal.innerHTML = `
        <div style="position: relative;">
            <button onclick="closeModalContent()" style="position: absolute; top: -10px; right: -10px; background: #ff4757; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-weight: bold;">×</button>
            ${content}
        </div>
    `;
    
    modal.id = "modal-content";
    document.body.appendChild(modal);
    
    // Close on background click
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            closeModalContent();
        }
    });
}

// Close modal content
function closeModalContent() {
    const modal = document.getElementById("modal-content");
    if (modal) {
        document.body.removeChild(modal);
    }
}

// Animate products
function animateProducts() {
    const products = document.querySelectorAll(".product-card");
    products.forEach((product, index) => {
        setTimeout(() => {
            product.classList.add("visible");
        }, index * 100);
    });
}

// Scroll animations
function animateOnScroll() {
    const elements = document.querySelectorAll(".product-card:not(.visible)");
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add("visible");
        }
    });
}

// Initialize scroll animations
window.addEventListener("scroll", animateOnScroll);

// Initialize animations on load
window.addEventListener("load", () => {
    animateOnScroll();
});


