// Mobile burger menu
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');

if(burger && nav){
  burger.addEventListener('click', () => {
    nav.classList.toggle('open');
    burger.classList.toggle('active');
  });
  // Close menu on link click
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });
}

// Sticky header shadow on scroll
const header = document.querySelector('.header');
window.addEventListener('scroll', () => {
  if(window.scrollY > 20){
    header.style.boxShadow = '0 6px 28px rgba(0,0,0,0.5)';
  } else {
    header.style.boxShadow = 'none';
  }
});

// Booking form handler — отправляет данные на локальный сервер
async function handleBooking(e){
  e.preventDefault();
  const form = e.target;
  const success = document.getElementById('success');
  const formData = Object.fromEntries(new FormData(form).entries());

  try{
    const resp = await fetch('http://localhost:5000/bookings', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(formData)
    });

    if(resp.ok){
      if(success){
        success.classList.add('show');
        form.reset();
        setTimeout(() => success.classList.remove('show'), 5000);
        success.scrollIntoView({behavior:'smooth', block:'center'});
      } else {
        alert('Booking sent.');
      }
    } else {
      const text = await resp.text();
      console.error('Server error:', resp.status, text);
      alert('Failed to send booking. Server returned ' + resp.status);
    }
  } catch(err){
    console.error('Network error:', err);
    alert('Не удалось отправить запрос. Убедитесь, что сервер запущен (python server.py).');
  }
}

// Simple fade-in on scroll for cards
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, {threshold:0.1});

document.querySelectorAll('.feature-card, .menu-card, .event-card, .gal-item, .insta-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity .6s ease, transform .6s ease';
  observer.observe(el);
});

// Floating CTA - show after scroll
const floatingCta = document.querySelector('.floating-cta');
if(floatingCta){
  window.addEventListener('scroll', () => {
    if(window.scrollY > 400){
      floatingCta.style.opacity = '1';
      floatingCta.style.pointerEvents = 'auto';
    } else {
      floatingCta.style.opacity = '0';
      floatingCta.style.pointerEvents = 'none';
    }
  });
  floatingCta.style.transition = 'opacity .3s ease, transform .25s ease';
}