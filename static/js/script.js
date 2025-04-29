// Sample book data
const books = [
    {
        id: 1,
        title: "The Midnight Library",
        author: "Matt Haig",
        price: 399,
        originalPrice: 499,
        image: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "fiction",
        bestseller: true,
        newRelease: false,
        rating: 4.5,
        reviews: 128
    },
    {
        id: 2,
        title: "Atomic Habits",
        author: "James Clear",
        price: 349,
        originalPrice: 499,
        image: "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "non-fiction",
        bestseller: true,
        newRelease: false,
        rating: 4.7,
        reviews: 215
    },
    {
        id: 3,
        title: "Where the Crawdads Sing",
        author: "Delia Owens",
        price: 459,
        originalPrice: 599,
        image: "https://images.unsplash.com/photo-1589998059171-988d887df646?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "fiction",
        bestseller: true,
        newRelease: false,
        rating: 4.6,
        reviews: 178
    },
    {
        id: 4,
        title: "The Psychology of Money",
        author: "Morgan Housel",
        price: 299,
        originalPrice: 399,
        image: "https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "non-fiction",
        bestseller: false,
        newRelease: true,
        rating: 4.4,
        reviews: 92
    },
    {
        id: 5,
        title: "Ikigai: The Japanese Secret to a Long and Happy Life",
        author: "Héctor García",
        price: 279,
        originalPrice: 399,
        image: "https://images.unsplash.com/photo-1531346878377-a5be20888e57?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "non-fiction",
        bestseller: false,
        newRelease: true,
        rating: 4.3,
        reviews: 156
    },
    {
        id: 6,
        title: "The Alchemist",
        author: "Paulo Coelho",
        price: 249,
        originalPrice: 299,
        image: "https://images.unsplash.com/photo-1532012197267-da84d127e765?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "fiction",
        bestseller: false,
        newRelease: true,
        rating: 4.2,
        reviews: 203
    },
    {
        id: 7,
        title: "Educated: A Memoir",
        author: "Tara Westover",
        price: 389,
        originalPrice: 499,
        image: "https://images.unsplash.com/photo-1589998059171-988d887df646?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "non-fiction",
        bestseller: true,
        newRelease: false,
        rating: 4.8,
        reviews: 187
    },
    {
        id: 8,
        title: "The Silent Patient",
        author: "Alex Michaelides",
        price: 319,
        originalPrice: 399,
        image: "https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        category: "fiction",
        bestseller: false,
        newRelease: true,
        rating: 4.1,
        reviews: 134
    }
];

// DOM Elements
const bestsellersGrid = document.getElementById('bestsellersGrid');
const newReleasesGrid = document.getElementById('newReleasesGrid');
const cartButton = document.getElementById('cartButton');
const cartSidebar = document.getElementById('cartSidebar');
const cartOverlay = document.getElementById('cartOverlay');
const closeCart = document.getElementById('closeCart');
const cartItems = document.getElementById('cartItems');
const cartCount = document.querySelector('.cart-count');
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const newsletterForm = document.getElementById('newsletterForm');

// Shopping cart
let cart = [];

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    displayBooks();
    setupEventListeners();
});

// Display books in their respective sections
function displayBooks() {
    // Display bestsellers
    const bestsellers = books.filter(book => book.bestseller);
    bestsellersGrid.innerHTML = bestsellers.map(book => createBookCard(book)).join('');
    
    // Display new releases
    const newReleases = books.filter(book => book.newRelease);
    newReleasesGrid.innerHTML = newReleases.map(book => createBookCard(book)).join('');
}

// Create HTML for a book card
function createBookCard(book) {
    const discount = Math.round(((book.originalPrice - book.price) / book.originalPrice) * 100);
    
    return `
        <div class="book-card" data-id="${book.id}">
            ${book.newRelease ? '<span class="book-badge">New</span>' : ''}
            <div class="book-image">
                <img src="${book.image}" alt="${book.title}">
            </div>
            <div class="book-info">
                <h3 class="book-title">${book.title}</h3>
                <p class="book-author">${book.author}</p>
                <div class="book-price">
                    <span class="current-price">₹${book.price}</span>
                    ${book.originalPrice > book.price ? 
                        `<span class="original-price">₹${book.originalPrice}</span>
                         <span class="discount">${discount}% OFF</span>` : ''
                    }
                </div>
                <button class="add-to-cart" data-id="${book.id}">Add to Cart</button>
            </div>
        </div>
    `;
}

// Set up event listeners
function setupEventListeners() {
    // Cart toggle
    cartButton.addEventListener('click', (e) => {
        e.preventDefault();
        cartSidebar.classList.add('active');
        cartOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    // Close cart
    closeCart.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
        cartOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });
    
    cartOverlay.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
        cartOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });
    
    // Add to cart buttons
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-to-cart')) {
            const bookId = parseInt(e.target.getAttribute('data-id'));
            const book = books.find(b => b.id === bookId);
            
            if (book) {
                addToCart(book);
            }
        }
        
        // Quantity controls in cart
        if (e.target.classList.contains('quantity-btn')) {
            const bookId = parseInt(e.target.closest('.cart-item').getAttribute('data-id'));
            const isIncrease = e.target.textContent === '+';
            updateCartItem(bookId, isIncrease ? 1 : -1);
        }
        
        // Remove item from cart
        if (e.target.classList.contains('remove-item')) {
            const bookId = parseInt(e.target.closest('.cart-item').getAttribute('data-id'));
            removeFromCart(bookId);
        }
    });
    
    // Search form
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const searchTerm = searchInput.value.trim().toLowerCase();
        
        if (searchTerm) {
            const results = books.filter(book => 
                book.title.toLowerCase().includes(searchTerm) || 
                book.author.toLowerCase().includes(searchTerm)
            );
            
            if (results.length > 0) {
                bestsellersGrid.innerHTML = results.map(book => createBookCard(book)).join('');
                document.querySelector('.bestsellers-section .section-title').textContent = 'Search Results';
                newReleasesGrid.innerHTML = '';
            } else {
                alert('No books found matching your search');
            }
        }
    });
    
    // Newsletter form
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input').value;
        
        if (email) {
            alert(`Thank you for subscribing with ${email}!`);
            newsletterForm.reset();
        }
    });
}

// Add item to cart
function addToCart(book) {
    const existingItem = cart.find(item => item.id === book.id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            ...book,
            quantity: 1
        });
    }
    
    updateCartUI();
    showNotification(`${book.title} added to cart!`);
}

// Update cart item quantity
function updateCartItem(bookId, change) {
    const itemIndex = cart.findIndex(item => item.id === bookId);
    
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += change;
        
        if (cart[itemIndex].quantity <= 0) {
            cart.splice(itemIndex, 1);
        }
        
        updateCartUI();
    }
}

// Remove item from cart
function removeFromCart(bookId) {
    cart = cart.filter(item => item.id !== bookId);
    updateCartUI();
}

// Update cart UI
function updateCartUI() {
    // Update cart count
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Update cart items
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item" data-id="${item.id}">
                <img src="${item.image}" alt="${item.title}" class="cart-item-img">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.title}</h4>
                    <p class="cart-item-author">${item.author}</p>
                    <p class="cart-item-price">₹${item.price}</p>
                    <div class="cart-item-actions">
                        <div class="quantity-control">
                            <button class="quantity-btn">-</button>
                            <span class="quantity">${item.quantity}</span>
                            <button class="quantity-btn">+</button>
                        </div>
                        <button class="remove-item">Remove</button>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    // Update cart total
    const totalAmount = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    document.querySelector('.total-amount').textContent = `₹${totalAmount.toFixed(2)}`;
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add notification styles dynamically
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: var(--primary);
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 3000;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .notification.show {
        opacity: 1;
    }
`;
document.head.appendChild(notificationStyles);