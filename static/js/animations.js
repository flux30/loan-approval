/**
 * GSAP Animations & Scroll Triggers
 * Advanced animations for premium UI/UX experience
 */

// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

// Initialize animations on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initializeScrollAnimations();
    initializeElementAnimations();
});

/**
 * Initialize scroll-triggered animations
 */
function initializeScrollAnimations() {
    // Feature cards scroll animation
    gsap.utils.toArray('.feature-card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 80%',
                end: 'top 50%',
                scrub: 1,
                markers: false
            },
            opacity: 0,
            y: 50,
            duration: 0.8,
            delay: index * 0.1
        });
    });

    // Result cards scroll animation
    gsap.utils.toArray('.result-card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                end: 'top 55%',
                scrub: 0.5
            },
            opacity: 0,
            x: -50,
            duration: 0.6,
            delay: index * 0.05
        });
    });

    // Section titles scroll animation
    gsap.utils.toArray('.section-title').forEach(title => {
        gsap.from(title, {
            scrollTrigger: {
                trigger: title,
                start: 'top 90%',
                end: 'top 70%',
                scrub: 1
            },
            opacity: 0,
            scale: 0.8,
            duration: 0.6
        });
    });

    // Table scroll animation
    gsap.from('.applicants-table-wrapper', {
        scrollTrigger: {
            trigger: '.applicants-table-wrapper',
            start: 'top 85%',
            end: 'top 55%',
            scrub: 0.5
        },
        opacity: 0,
        y: 30,
        duration: 0.8
    });

    // Results grid scroll animation
    gsap.from('.results-grid', {
        scrollTrigger: {
            trigger: '.results-grid',
            start: 'top 85%',
            end: 'top 55%',
            scrub: 0.5
        },
        opacity: 0,
        y: 40,
        duration: 0.8
    });
}

/**
 * Initialize element-specific animations
 */
function initializeElementAnimations() {
    // Floating cards animation (hero section)
    const timeline = gsap.timeline();
    
    gsap.to('.card-1', {
        duration: 4,
        y: -30,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    gsap.to('.card-2', {
        duration: 5,
        y: -40,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: 0.5
    });

    gsap.to('.card-3', {
        duration: 6,
        y: -25,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: 1
    });

    // Subtle rotation on cards
    gsap.to('.card-1, .card-2, .card-3', {
        duration: 20,
        rotation: 360,
        repeat: -1,
        ease: 'none',
        transformOrigin: '50% 50%'
    });
}

/**
 * Modal open animation
 */
function openModalAnimation(modalElement) {
    gsap.fromTo(modalElement, 
        {
            opacity: 0,
            backdropFilter: 'blur(0px)'
        },
        {
            opacity: 1,
            backdropFilter: 'blur(5px)',
            duration: 0.3,
            ease: 'power2.out'
        }
    );

    const modalContent = modalElement.querySelector('.modal-content');
    gsap.fromTo(modalContent,
        {
            opacity: 0,
            y: 50,
            scale: 0.9
        },
        {
            opacity: 1,
            y: 0,
            scale: 1,
            duration: 0.4,
            ease: 'back.out'
        }
    );
}

/**
 * Modal close animation
 */
function closeModalAnimation(modalElement) {
    const modalContent = modalElement.querySelector('.modal-content');
    gsap.to(modalContent,
        {
            opacity: 0,
            y: 50,
            scale: 0.9,
            duration: 0.3,
            ease: 'back.in'
        }
    );

    gsap.to(modalElement,
        {
            opacity: 0,
            backdropFilter: 'blur(0px)',
            duration: 0.3,
            ease: 'power2.in',
            delay: 0.1,
            onComplete: () => {
                modalElement.classList.remove('active');
            }
        }
    );
}

/**
 * Result card appearance animation
 */
function animateResultCard(cardElement) {
    gsap.from(cardElement, {
        opacity: 0,
        y: 20,
        scale: 0.95,
        duration: 0.5,
        ease: 'back.out'
    });

    // Subtle hover effect
    cardElement.addEventListener('mouseenter', () => {
        gsap.to(cardElement, {
            duration: 0.3,
            boxShadow: '0 16px 48px rgba(102, 126, 234, 0.3)',
            ease: 'power2.out'
        });
    });

    cardElement.addEventListener('mouseleave', () => {
        gsap.to(cardElement, {
            duration: 0.3,
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
            ease: 'power2.out'
        });
    });
}

/**
 * Number counter animation
 */
function animateCounter(element, targetValue, duration = 1) {
    const currentValue = parseInt(element.textContent) || 0;
    
    gsap.to(element, {
        innerHTML: targetValue,
        duration: duration,
        snap: { innerHTML: 1 },
        ease: 'power2.out',
        onUpdate: function() {
            element.textContent = Math.round(this.targets()[0].innerHTML);
        }
    });
}

/**
 * Stagger animation for list items
 */
function staggerAnimateElements(elements, delay = 0.1) {
    gsap.from(elements, {
        opacity: 0,
        y: 20,
        duration: 0.5,
        stagger: delay,
        ease: 'back.out'
    });
}

/**
 * Pulse animation for emphasis
 */
function pulseElement(element, times = 2) {
    gsap.to(element, {
        boxShadow: '0 0 50px rgba(102, 126, 234, 0.8)',
        duration: 0.5,
        repeat: times * 2 - 1,
        yoyo: true,
        ease: 'sine.inOut'
    });
}

/**
 * Shake animation for errors
 */
function shakeElement(element) {
    gsap.to(element, {
        x: -10,
        duration: 0.1,
        repeat: 5,
        yoyo: true,
        ease: 'back.inOut'
    });
}

/**
 * Success animation
 */
function successAnimation(element) {
    gsap.timeline()
        .to(element, {
            scale: 1.05,
            duration: 0.2,
            ease: 'back.out'
        })
        .to(element, {
            rotation: 360,
            duration: 0.6,
            ease: 'circ.out'
        }, 0);
}

/**
 * Button click ripple effect
 */
function addRippleEffect(button) {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        this.appendChild(ripple);

        gsap.to(ripple, {
            opacity: 0,
            scale: 2,
            duration: 0.6,
            ease: 'power2.out',
            onComplete: () => ripple.remove()
        });
    });
}

/**
 * Fade in on page load
 */
function fadeInOnLoad() {
    const body = document.body;
    body.style.opacity = '0';
    
    gsap.to(body, {
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out'
    });
}

/**
 * Navbar active link animation
 */
function updateNavbarAnimation(activeLink) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

// Export functions for use in main.js
window.AnimationUtils = {
    openModalAnimation,
    closeModalAnimation,
    animateResultCard,
    animateCounter,
    staggerAnimateElements,
    pulseElement,
    shakeElement,
    successAnimation,
    addRippleEffect,
    fadeInOnLoad,
    updateNavbarAnimation
};
