// 响应式导航菜单
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// 平滑滚动
const smoothScroll = (target) => {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
};

// 导航链接点击事件
const navItems = document.querySelectorAll('.nav-links a');
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const target = item.getAttribute('href');
        smoothScroll(target);
        navLinks.classList.remove('active');
    });
});

// CTA按钮点击事件
const ctaButtons = document.querySelectorAll('.cta-buttons a');
ctaButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        const target = button.getAttribute('href');
        smoothScroll(target);
    });
});

// 游戏卡片按钮点击事件
const gameButtons = document.querySelectorAll('.card-btn');
gameButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        // 这里可以添加游戏详情页的逻辑
        alert('游戏详情页开发中...');
    });
});

// 联系表单提交事件
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        if (name && email && message) {
            alert('消息已发送！我们会尽快回复您。');
            contactForm.reset();
        } else {
            alert('请填写所有必填字段。');
        }
    });
}

// 滚动时导航栏样式变化
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'rgba(26, 26, 26, 0.95)';
    } else {
        navbar.style.backgroundColor = '#1a1a1a';
    }
});

// 数字计数器动画
const animateCounter = (element, target, duration = 2000) => {
    let start = 0;
    const increment = target / (duration / 16);
    
    const updateCounter = () => {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start) + '+';
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + '+';
        }
    };
    
    updateCounter();
};

// 监听元素进入视口
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (entry.target.classList.contains('stat-number')) {
                const target = parseInt(entry.target.textContent);
                animateCounter(entry.target, target);
            }
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

// 观察统计数字元素
const statNumbers = document.querySelectorAll('.stat-number');
statNumbers.forEach(stat => {
    observer.observe(stat);
});

// 游戏卡片悬停效果
const gameCards = document.querySelectorAll('.game-card');
gameCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-10px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// 团队成员悬停效果
const teamMembers = document.querySelectorAll('.team-member');
teamMembers.forEach(member => {
    member.addEventListener('mouseenter', () => {
        member.querySelector('img').style.transform = 'scale(1.1)';
    });
    
    member.addEventListener('mouseleave', () => {
        member.querySelector('img').style.transform = 'scale(1)';
    });
});

// 开发流程步骤动画
const processSteps = document.querySelectorAll('.step');
const processObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, index * 200);
            processObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.3 });

processSteps.forEach(step => {
    step.style.opacity = '0';
    step.style.transform = 'translateY(30px)';
    step.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    processObserver.observe(step);
});