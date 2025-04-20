// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Navbar script loaded');
    
    // Get all required elements using IDs
    const hamburger = document.getElementById('hamburgerBtn');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');
    
    console.log('Elements found:', {
        hamburger: hamburger !== null,
        navMenu: navMenu !== null,
        navOverlay: navOverlay !== null
    });

    // Exit if any required element is missing
    if (!hamburger || !navMenu || !navOverlay) {
        console.error('Required elements not found');
        return;
    }

    let isMenuOpen = false;

    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
        console.log('Toggling menu:', isMenuOpen ? 'opening' : 'closing');
        
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        navOverlay.classList.toggle('active');
        
        // Update aria-expanded for accessibility
        hamburger.setAttribute('aria-expanded', isMenuOpen);

        // Prevent body scroll when menu is open
        document.body.style.overflow = isMenuOpen ? 'hidden' : '';
    }

    // Toggle menu when hamburger is clicked
    hamburger.addEventListener('click', function(e) {
        console.log('Hamburger clicked');
        e.preventDefault(); // Prevent any default button behavior
        e.stopPropagation();
        toggleMenu();
    });

    // Close menu when clicking overlay
    navOverlay.addEventListener('click', function() {
        console.log('Overlay clicked');
        if (isMenuOpen) {
            toggleMenu();
        }
    });

    // Close menu when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isMenuOpen) {
            console.log('Escape key pressed');
            toggleMenu();
        }
    });

    // Close menu when clicking a nav item
    const navItems = navMenu.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            console.log('Nav item clicked');
            if (isMenuOpen) {
                toggleMenu();
            }
        });
    });

    // Log initial state
    console.log('Navbar initialization complete');
}); 