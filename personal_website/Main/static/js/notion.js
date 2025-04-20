document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.documentElement.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.documentElement.classList.contains('dark-mode'));
        });

        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.documentElement.classList.add('dark-mode');
        }
    }

    // Mobile sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.notion-sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Editable blocks
    document.querySelectorAll('.notion-block[contenteditable="true"]').forEach(block => {
        // Handle placeholder text
        block.addEventListener('focus', function() {
            if (this.textContent.trim() === this.getAttribute('data-placeholder')) {
                this.textContent = '';
            }
        });

        block.addEventListener('blur', function() {
            if (this.textContent.trim() === '') {
                this.textContent = this.getAttribute('data-placeholder');
            }
        });
    });

    // Collapsible blocks
    document.querySelectorAll('.notion-toggle').forEach(toggle => {
        const header = toggle.querySelector('.notion-toggle-header');
        const content = toggle.querySelector('.notion-toggle-content');

        if (header && content) {
            header.addEventListener('click', function() {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
                header.classList.toggle('collapsed');
            });
        }
    });

    // Table of contents generation
    function generateTOC() {
        const toc = document.getElementById('tableOfContents');
        if (!toc) return;

        const headings = document.querySelectorAll('h1, h2, h3');
        const tocList = document.createElement('ul');
        tocList.className = 'notion-list';

        headings.forEach(heading => {
            const li = document.createElement('li');
            li.className = 'notion-list-item';
            
            const a = document.createElement('a');
            a.textContent = heading.textContent;
            a.href = `#${heading.id}`;
            
            li.appendChild(a);
            tocList.appendChild(li);
        });

        toc.appendChild(tocList);
    }

    generateTOC();

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Page cover image parallax effect
    const pageCover = document.querySelector('.notion-page-cover');
    if (pageCover) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            pageCover.style.transform = `translateY(${scrolled * 0.4}px)`;
        });
    }

    // Code block syntax highlighting
    document.querySelectorAll('.notion-code').forEach(block => {
        if (window.Prism) {
            Prism.highlightElement(block);
        }
    });
}); 