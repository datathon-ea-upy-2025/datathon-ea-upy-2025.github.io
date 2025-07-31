/* =====================================================
   DATATHON UPY 2025 - JavaScript
   ===================================================== */

/* =====================================================
   1. FUNCIONES DE NAVEGACIÓN
   ===================================================== */

// Toggle del menú móvil
function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

/* =====================================================
   2. NAVEGACIÓN SUAVE (SMOOTH SCROLL)
   ===================================================== */

// Configurar navegación suave para los enlaces internos
document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los enlaces de navegación
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
});

// Manejar clicks en navegación
function handleNavClick(e) {
    const href = this.getAttribute('href');
    
    // Solo manejar enlaces internos (que empiezan con #)
    if (href.startsWith('#')) {
        e.preventDefault();
        
        const targetId = href.substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            // Calcular posición con offset para el header fijo
            const offsetTop = targetElement.offsetTop - 80;
            
            // Hacer scroll suave a la sección
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }
    
    // Cerrar menú móvil después de hacer click
    document.getElementById('navLinks').classList.remove('active');
}

/* =====================================================
   3. ANIMACIONES DE ENTRADA
   ===================================================== */

// Animación de entrada cuando carga la página
window.addEventListener('load', function() {
    animateMainContent();
});

// Animar elementos del contenido principal
function animateMainContent() {
    const elements = document.querySelectorAll('.main-content > *');
    
    elements.forEach((element, index) => {
        // Configurar estado inicial
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.8s ease';
        
        // Animar con delay escalonado
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

/* =====================================================
   4. EFECTOS INTERACTIVOS
   ===================================================== */

// Configurar efectos hover para el código QR
document.addEventListener('DOMContentLoaded', function() {
    const qrCode = document.querySelector('.qr-code');
    
    if (qrCode) {
        // Efecto hover - escalar y rotar
        qrCode.addEventListener('mouseenter', handleQRHover);
        qrCode.addEventListener('mouseleave', handleQRLeave);
    }
});

// Manejar hover en QR
function handleQRHover() {
    this.style.transform = 'scale(1.05) rotate(2deg)';
    this.style.transition = 'all 0.3s ease';
}

// Manejar mouse leave en QR
function handleQRLeave() {
    this.style.transform = 'scale(1) rotate(0deg)';
}

/* =====================================================
   5. OBSERVADOR DE INTERSECCIÓN (OPCIONAL)
   ===================================================== */

// Crear animaciones cuando los elementos entran en viewport
document.addEventListener('DOMContentLoaded', function() {
    setupIntersectionObserver();
});

// Configurar el observador de intersección
function setupIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(handleIntersection, observerOptions);
    
    // Observar bloques de información
    const infoBlocks = document.querySelectorAll('.info-block');
    infoBlocks.forEach(block => {
        observer.observe(block);
    });
}

// Manejar elementos que entran en viewport
function handleIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}

/* =====================================================
   6. UTILIDADES
   ===================================================== */

// Detectar si el usuario está en móvil
function isMobile() {
    return window.innerWidth <= 768;
}

// Cerrar menú móvil al hacer click fuera
document.addEventListener('click', function(e) {
    const navLinks = document.getElementById('navLinks');
    const menuToggle = document.querySelector('.menu-toggle');
    
    if (navLinks && menuToggle) {
        // Si el click no fue en el menú ni en el botón, cerrar el menú
        if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
            navLinks.classList.remove('active');
        }
    }
});

/* =====================================================
   7. ANIMACIONES CSS DINÁMICAS
   ===================================================== */

// Agregar animación fadeInUp si no existe
if (!document.querySelector('#dynamic-animations')) {
    const style = document.createElement('style');
    style.id = 'dynamic-animations';
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
}

/* =====================================================
   8. COUNTDOWN TIMER
   ===================================================== */

// Función para actualizar el countdown
function updateCountdown() {
    const targetDate = new Date('July 31, 2025 12:30:00').getTime();
    const now = new Date().getTime();
    const distance = targetDate - now;

    // Calcular días, horas, minutos y segundos
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Actualizar el HTML
    const daysElement = document.getElementById('days');
    const hoursElement = document.getElementById('hours');
    const minutesElement = document.getElementById('minutes');
    const secondsElement = document.getElementById('seconds');

    if (daysElement && hoursElement && minutesElement && secondsElement) {
        daysElement.textContent = String(days).padStart(2, '0');
        hoursElement.textContent = String(hours).padStart(2, '0');
        minutesElement.textContent = String(minutes).padStart(2, '0');
        secondsElement.textContent = String(seconds).padStart(2, '0');
    }

    // Si la fecha ya pasó
    if (distance < 0) {
        const countdownElement = document.getElementById('countdown');
        if (countdownElement) {
            countdownElement.innerHTML = '<div class="countdown-expired">¡EL DATATHON HA FINALIZADO!</div>';
        }
    }
}

// Iniciar el countdown cuando carga la página
document.addEventListener('DOMContentLoaded', function() {
    updateCountdown();
    // Actualizar cada segundo
    setInterval(updateCountdown, 1000);
});

/* =====================================================
   9. MANEJO DE SCROLL (OPCIONAL)
   ===================================================== */

// Variable para rastrear la posición anterior del scroll
let lastScrollTop = 0;

// Opción para hacer el header sticky con hide/show en scroll
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Solo aplicar en desktop
    if (!isMobile() && header) {
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling hacia abajo - ocultar header
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling hacia arriba - mostrar header
            header.style.transform = 'translateY(0)';
        }
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
}, false);