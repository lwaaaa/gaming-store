// Gaming Store JavaScript

// Cart functionality
let cart = [];
let cartTotal = 0;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadCartFromStorage();
    updateCartDisplay();
});

// Initialize event listeners
function initializeEventListeners() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', handleAddToCart);
    });

    // Navigation smooth scrolling
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', handleSmoothScroll);
    });

    // Search functionality
    const searchIcon = document.querySelector('.fa-search');
    if (searchIcon) {
        searchIcon.addEventListener('click', handleSearch);
    }

    // Cart icon click
    const cartIcon = document.querySelector('.fa-shopping-cart');
    if (cartIcon) {
        cartIcon.addEventListener('click', showCart);
    }

    // User icon click
    const userIcon = document.querySelector('.fa-user');
    if (userIcon) {
        userIcon.addEventListener('click', handleUserLogin);
    }

    // CTA button
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', scrollToGames);
    }
}

// Handle add to cart
function handleAddToCart(event) {
    const button = event.target;
    const card = button.closest('.game-card, .accessory-card');
    
    if (card) {
        const name = card.querySelector('h3').textContent;
        const priceText = card.querySelector('.price').textContent;
        const price = parseInt(priceText.replace(/[^\d]/g, ''));
        
        const item = {
            id: Date.now(),
            name: name,
            price: price,
            quantity: 1
        };
        
        addToCart(item);
        showAddToCartAnimation(button);
    }
}

// Add item to cart
function addToCart(item) {
    // Check if item already exists
    const existingItem = cart.find(cartItem => cartItem.name === item.name);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push(item);
    }
    
    updateCartTotal();
    saveCartToStorage();
    updateCartDisplay();
    
    // Show success message
    showNotification(`تم إضافة ${item.name} إلى السلة!`, 'success');
}

// Update cart total
function updateCartTotal() {
    cartTotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

// Save cart to localStorage
function saveCartToStorage() {
    localStorage.setItem('gamingStoreCart', JSON.stringify(cart));
    localStorage.setItem('gamingStoreCartTotal', cartTotal.toString());
}

// Load cart from localStorage
function loadCartFromStorage() {
    const savedCart = localStorage.getItem('gamingStoreCart');
    const savedTotal = localStorage.getItem('gamingStoreCartTotal');
    
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
    
    if (savedTotal) {
        cartTotal = parseInt(savedTotal);
    }
}

// Update cart display
function updateCartDisplay() {
    const cartIcon = document.querySelector('.fa-shopping-cart');
    if (cartIcon && cart.length > 0) {
        // Add cart count badge
        let badge = cartIcon.nextElementSibling;
        if (!badge || !badge.classList.contains('cart-badge')) {
            badge = document.createElement('span');
            badge.classList.add('cart-badge');
            cartIcon.parentNode.insertBefore(badge, cartIcon.nextSibling);
        }
        badge.textContent = cart.length;
        badge.style.cssText = `
            position: absolute;
            top: -5px;
            right: -5px;
            background: #ff4757;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        `;
    }
}

// Show cart
function showCart() {
    if (cart.length === 0) {
        showNotification('السلة فارغة!', 'info');
        return;
    }
    
    let cartHTML = '<div style="background: white; padding: 20px; border-radius: 10px; max-width: 400px;">';
    cartHTML += '<h3 style="margin-bottom: 15px; color: #333;">سلة التسوق</h3>';
    
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
    cartHTML += '</div>';
    
    showModal(cartHTML);
}

// Checkout function
function checkout() {
    showNotification('شكراً لك! سيتم التواصل معك قريباً لإتمام الطلب.', 'success');
    cart = [];
    cartTotal = 0;
    saveCartToStorage();
    updateCartDisplay();
    closeModal();
}

// Handle smooth scrolling
function handleSmoothScroll(event) {
    event.preventDefault();
    const targetId = event.target.getAttribute('href');
    const targetSection = document.querySelector(targetId);
    
    if (targetSection) {
        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Handle search
function handleSearch() {
    const searchTerm = prompt('ابحث عن لعبة أو إكسسوار:');
    if (searchTerm) {
        showNotification(`البحث عن: ${searchTerm}`, 'info');
        // Here you would implement actual search functionality
    }
}

// Handle user login
function handleUserLogin() {
    showNotification('سيتم إضافة نظام تسجيل الدخول قريباً!', 'info');
}

// Scroll to games section
function scrollToGames() {
    const gamesSection = document.querySelector('#games');
    if (gamesSection) {
        gamesSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Show add to cart animation
function showAddToCartAnimation(button) {
    const originalText = button.textContent;
    button.textContent = 'تم الإضافة ✓';
    button.style.background = '#28a745';
    
    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
    }, 1500);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
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
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Show modal
function showModal(content) {
    const modal = document.createElement('div');
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
            <button onclick="closeModal()" style="position: absolute; top: -10px; right: -10px; background: #ff4757; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-weight: bold;">×</button>
            ${content}
        </div>
    `;
    
    modal.id = 'modal';
    document.body.appendChild(modal);
    
    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Close modal
function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        document.body.removeChild(modal);
    }
}

// Scroll animations
function animateOnScroll() {
    const elements = document.querySelectorAll('.game-card, .accessory-card');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// Initialize scroll animations
window.addEventListener('scroll', animateOnScroll);

// Initialize animations on load
window.addEventListener('load', () => {
    animateOnScroll();
});

// API Integration (for future backend connection)
const API_BASE_URL = window.location.origin.includes('localhost') 
    ? 'http://localhost:5000/api' 
    : 'https://gaming-store.onrender.com/api';

// Fetch games from backend
async function fetchGames() {
    try {
        const response = await fetch(`${API_BASE_URL}/games`);
        if (response.ok) {
            const games = await response.json();
            return games;
        }
    } catch (error) {
        console.log('Backend not available, using static data');
    }
    return null;
}

// Fetch accessories from backend
async function fetchAccessories() {
    try {
        const response = await fetch(`${API_BASE_URL}/accessories`);
        if (response.ok) {
            const accessories = await response.json();
            return accessories;
        }
    } catch (error) {
        console.log('Backend not available, using static data');
    }
    return null;
}

// Submit order to backend
async function submitOrder(orderData) {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        if (response.ok) {
            const result = await response.json();
            return result;
        }
    } catch (error) {
        console.log('Backend not available for order submission');
    }
    return null;
}

