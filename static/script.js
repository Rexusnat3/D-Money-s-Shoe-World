// Global state
let currentUser = null;
let authToken = null;
let cart = [];
let allShoes = [];

// API Base URL (relative to current origin, not hardcoded)
const API_BASE = '';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadAuthState();
    showSection('hero');
    
    // Add explicit event listeners for navigation buttons
    const authBtn = document.getElementById('auth-btn');
    const shopBtns = document.querySelectorAll('[onclick*="shop"]');
    const cartBtns = document.querySelectorAll('[onclick*="cart"]');
    
    if (authBtn) {
        authBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Login button clicked!');
            showSection('auth');
        });
    }
});

// Section Navigation
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section, .hero').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const section = document.getElementById(sectionName);
    if (section) {
        section.style.display = 'block';
    }
    
    // Load section-specific data
    if (sectionName === 'shop') {
        loadShoes();
    } else if (sectionName === 'cart') {
        renderCart();
    }
}

// Authentication Tab Switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Find and activate the clicked tab
    event.target.classList.add('active');
    
    // Show appropriate form
    if (tabName === 'login') {
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('register-form').style.display = 'none';
    } else {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    }
}

// Login Function
async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const messageDiv = document.getElementById('login-message');
    
    if (!username || !password) {
        showMessage(messageDiv, 'Please fill in all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.token;
            currentUser = data.user;
            
            // Save to localStorage
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
            showMessage(messageDiv, 'Login successful!', 'success');
            updateUIForLoggedInUser();
            
            setTimeout(() => {
                showSection('shop');
            }, 1000);
        } else {
            showMessage(messageDiv, data.message || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Connection error. Please try again.', 'error');
        console.error('Login error:', error);
    }
}

// Register Function
async function register() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const role = document.getElementById('register-role').value;
    const messageDiv = document.getElementById('register-message');
    
    if (!username || !email || !password) {
        showMessage(messageDiv, 'Please fill in all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password, role })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(messageDiv, 'Registration successful! Please login.', 'success');
            setTimeout(() => {
                switchTab('login');
            }, 1500);
        } else {
            showMessage(messageDiv, data.message || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Connection error. Please try again.', 'error');
        console.error('Registration error:', error);
    }
}

// Logout Function
function logout() {
    authToken = null;
    currentUser = null;
    cart = [];
    
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    
    updateUIForLoggedOutUser();
    showSection('hero');
}

// Load shoes from API
async function loadShoes() {
    try {
        const response = await fetch(`${API_BASE}/shoes`);
        const shoes = await response.json();
        
        allShoes = shoes;
        renderShoes(shoes);
    } catch (error) {
        console.error('Error loading shoes:', error);
        showEmptyState('products-grid', '❌', 'Failed to load products');
    }
}

// Render shoes in grid
function renderShoes(shoes) {
    const grid = document.getElementById('products-grid');
    
    if (!shoes || shoes.length === 0) {
        showEmptyState('products-grid', '👟', 'No shoes available yet');
        return;
    }
    
    grid.innerHTML = shoes.map(shoe => {
        const icon = getCategoryIcon(shoe.category);
        const inStock = shoe.stock > 0;
        const imageUrl = shoe.image || 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400';
        const cartItem = cart.find(item => item.id === shoe.id);
        
        let buttonHtml;
        if (!inStock) {
            buttonHtml = `<button class="add-to-cart-btn" disabled>Out of Stock</button>`;
        } else if (cartItem) {
            buttonHtml = `
                <div style="display: flex; gap: 8px; align-items: center;">
                    <button class="qty-btn" onclick="decreaseQuantity(${shoe.id})">−</button>
                    <span style="min-width: 30px; text-align: center; font-weight: 600;">${cartItem.quantity}</span>
                    <button class="qty-btn" onclick="increaseQuantity(${shoe.id})">+</button>
                </div>
            `;
        } else {
            buttonHtml = `<button class="add-to-cart-btn" onclick="addToCart(${shoe.id})">Add to Cart</button>`;
        }
        
        return `
            <div class="product-card" data-category="${shoe.category}">
                <div class="product-image" style="background-image: url('${imageUrl}')"></div>
                <h3 class="product-name">${shoe.name}</h3>
                <p class="product-brand">${shoe.brand}</p>
                <div class="product-details">
                    <span class="detail-badge">Size: ${shoe.size}</span>
                    <span class="detail-badge">${shoe.color}</span>
                    <span class="detail-badge">${shoe.category}</span>
                </div>
                <div class="product-price">$${parseFloat(shoe.price).toFixed(2)}</div>
                <p class="product-stock">${inStock ? `${shoe.stock} in stock` : 'Out of stock'}</p>
                ${buttonHtml}
            </div>
        `;
    }).join('');
}

// Filter shoes by category
function filterShoes(category) {
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter and render
    if (category === 'all') {
        renderShoes(allShoes);
    } else {
        const filtered = allShoes.filter(shoe => shoe.category === category);
        renderShoes(filtered);
    }
}

// Add shoe to cart
function addToCart(shoeId) {
    if (!authToken) {
        alert('Please login to add items to cart');
        showSection('auth');
        return;
    }
    
    const shoe = allShoes.find(s => s.id === shoeId);
    if (!shoe) return;
    
    // Check if already in cart
    const existing = cart.find(item => item.id === shoeId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...shoe, quantity: 1 });
    }
    
    updateCartCount();
    renderCart();
    renderShoes(allShoes);
}

// Increase quantity
function increaseQuantity(shoeId) {
    const cartItem = cart.find(item => item.id === shoeId);
    if (cartItem) {
        cartItem.quantity += 1;
        updateCartCount();
        renderCart();
        renderShoes(allShoes);
    }
}

// Decrease quantity
function decreaseQuantity(shoeId) {
    const cartItem = cart.find(item => item.id === shoeId);
    if (cartItem) {
        if (cartItem.quantity > 1) {
            cartItem.quantity -= 1;
        } else {
            const index = cart.findIndex(item => item.id === shoeId);
            cart.splice(index, 1);
        }
        updateCartCount();
        renderCart();
        renderShoes(allShoes);
    }
}

// Render cart
function renderCart() {
    const cartItemsDiv = document.getElementById('cart-items');
    
    if (cart.length === 0) {
        showEmptyState('cart-items', '🛒', 'Your cart is empty');
        document.getElementById('cart-subtotal').textContent = '$0.00';
        document.getElementById('cart-total').textContent = '$0.00';
        return;
    }
    
    let subtotal = 0;
    
    cartItemsDiv.innerHTML = cart.map((item, index) => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        return `
            <div class="cart-item">
                <div class="cart-item-info">
                    <h3>${item.name}</h3>
                    <p class="cart-item-details">
                        ${item.brand} | Size: ${item.size} | ${item.color}
                    </p>
                    <p style="margin-top: 8px; color: #9ca3af;">
                        $${parseFloat(item.price).toFixed(2)} × ${item.quantity} = $${itemTotal.toFixed(2)}
                    </p>
                </div>
                <div style="display: flex; flex-direction: column; gap: 10px; align-items: flex-end;">
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <button class="qty-btn" onclick="decreaseQuantityInCart(${item.id})">−</button>
                        <span style="min-width: 30px; text-align: center; font-weight: 600;">${item.quantity}</span>
                        <button class="qty-btn" onclick="increaseQuantityInCart(${item.id})">+</button>
                    </div>
                    <button class="remove-btn" onclick="removeFromCart(${index})">Remove</button>
                </div>
            </div>
        `;
    }).join('');
    
    document.getElementById('cart-subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('cart-total').textContent = `$${subtotal.toFixed(2)}`;
}

// Increase quantity in cart view
function increaseQuantityInCart(shoeId) {
    const cartItem = cart.find(item => item.id === shoeId);
    if (cartItem) {
        cartItem.quantity += 1;
        updateCartCount();
        renderCart();
        renderShoes(allShoes);
    }
}

// Decrease quantity in cart view
function decreaseQuantityInCart(shoeId) {
    const cartItem = cart.find(item => item.id === shoeId);
    if (cartItem) {
        if (cartItem.quantity > 1) {
            cartItem.quantity -= 1;
            updateCartCount();
            renderCart();
            renderShoes(allShoes);
        }
    }
}

// Remove from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartCount();
    renderCart();
}

// Update cart count badge
function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.length;
}

// Checkout
function checkout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    alert(`Checkout feature coming soon!\nTotal: $${total.toFixed(2)}\n\nThis would process your order of ${cart.length} item(s).`);
}

// Admin: Add new shoe
async function addShoe() {
    if (!authToken || currentUser.role !== 'admin') {
        alert('Admin access required');
        return;
    }
    
    const name = document.getElementById('shoe-name').value;
    const brand = document.getElementById('shoe-brand').value;
    const price = document.getElementById('shoe-price').value;
    const size = document.getElementById('shoe-size').value;
    const stock = document.getElementById('shoe-stock').value;
    const color = document.getElementById('shoe-color').value;
    const category = document.getElementById('shoe-category').value;
    const image = document.getElementById('shoe-image').value;
    
    const messageDiv = document.getElementById('admin-message');
    
    if (!name || !brand || !price) {
        showMessage(messageDiv, 'Please fill in required fields (Name, Brand, Price)', 'error');
        return;
    }
    
    const shoeData = {
        name, brand, price, size, stock, color, category
    };
    
    // Add image if provided
    if (image) {
        shoeData.image = image;
    }
    
    // Add category-specific fields
    if (category === 'casual') {
        shoeData.style = document.getElementById('shoe-style').value || 'sneaker';
    } else if (category === 'athletic') {
        shoeData.sport_type = document.getElementById('shoe-sport').value || 'running';
    } else if (category === 'formal') {
        shoeData.material = document.getElementById('shoe-material').value || 'leather';
    }
    
    try {
        const response = await fetch(`${API_BASE}/shoes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(shoeData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(messageDiv, 'Shoe added successfully!', 'success');
            // Clear form
            document.querySelectorAll('#admin input, #admin select').forEach(input => {
                if (input.type !== 'submit') input.value = '';
            });
            // Reload shoes
            loadShoes();
        } else {
            showMessage(messageDiv, data.message || 'Failed to add shoe', 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Connection error. Please try again.', 'error');
        console.error('Add shoe error:', error);
    }
}

// Update category-specific fields visibility
function updateCategoryFields() {
    const category = document.getElementById('shoe-category').value;
    
    document.getElementById('casual-fields').style.display = category === 'casual' ? 'block' : 'none';
    document.getElementById('athletic-fields').style.display = category === 'athletic' ? 'block' : 'none';
    document.getElementById('formal-fields').style.display = category === 'formal' ? 'block' : 'none';
}

// Utility: Show message
function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `message ${type}`;
    element.style.display = 'block';
}

// Utility: Show empty state
function showEmptyState(containerId, icon, text) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">${icon}</div>
            <p class="empty-state-text">${text}</p>
        </div>
    `;
}

// Utility: Get category icon
function getCategoryIcon(category) {
    const icons = {
        'athletic': '👟',
        'casual': '👞',
        'formal': '👔',
        'default': '👟'
    };
    return icons[category] || icons.default;
}

// Load authentication state from localStorage
function loadAuthState() {
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('currentUser');
    
    if (savedToken && savedUser) {
        authToken = savedToken;
        currentUser = JSON.parse(savedUser);
        updateUIForLoggedInUser();
    }
}

// Update UI for logged-in user
function updateUIForLoggedInUser() {
    document.getElementById('auth-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'block';
    document.getElementById('user-info').style.display = 'flex';
    document.getElementById('user-name').textContent = currentUser.username;
    document.getElementById('user-role').textContent = currentUser.role.toUpperCase();
    
    if (currentUser.role === 'admin') {
        document.getElementById('admin-btn').style.display = 'block';
    }
}

// Update UI for logged-out user
function updateUIForLoggedOutUser() {
    document.getElementById('auth-btn').style.display = 'block';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('admin-btn').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
    updateCartCount();
}
