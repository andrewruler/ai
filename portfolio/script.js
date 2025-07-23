// Smooth scroll for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const section = document.querySelector(this.getAttribute('href'));
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Back-to-top button (optional if you add one)
const backToTop = document.createElement('button');
backToTop.innerText = '↑';
backToTop.id = 'backToTop';
document.body.appendChild(backToTop);

Object.assign(backToTop.style, {
  position: 'fixed',
  bottom: '30px',
  right: '30px',
  padding: '0.75rem 1rem',
  fontSize: '1.25rem',
  backgroundColor: '#3b82f6',
  color: 'white',
  border: 'none',
  borderRadius: '50%',
  cursor: 'pointer',
  display: 'none',
  zIndex: '1000',
});

backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    backToTop.style.display = 'block';
  } else {
    backToTop.style.display = 'none';
  }
});

// Placeholder: More dynamic features (e.g., filter projects, theme toggle)
