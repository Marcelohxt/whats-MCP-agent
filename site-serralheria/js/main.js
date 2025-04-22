// Arquivo principal de JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Site R.A Portões carregado!');

    // Header scroll effect
    const header = document.querySelector('.header');
    const logo = document.querySelector('.logo');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
            logo.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
            logo.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    const mobileMenu = document.querySelector('.mobile-menu');
    const nav = document.querySelector('.nav');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    if (mobileMenu && nav) {
        mobileMenu.addEventListener('click', () => {
            nav.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });

        // Fechar menu ao clicar em um link
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('active');
                mobileMenu.classList.remove('active');
            });
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

    // Inicializar Swiper
    const swiper = new Swiper('.portoes-carousel', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            },
        }
    });
}); 