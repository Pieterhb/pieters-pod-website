import './style.css'

// Navigation Logic
const navLinks = document.querySelectorAll('nav a, .nav-btn, .logo');
const views = document.querySelectorAll('.view');

function navigateTo(targetId) {
  // Update views
  views.forEach(view => {
    if (view.id === targetId) {
      view.classList.add('active');
    } else {
      view.classList.remove('active');
    }
  });

  // Update nav links
  document.querySelectorAll('nav a').forEach(link => {
    if (link.dataset.target === targetId) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  window.scrollTo(0, 0);
}

navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const target = link.dataset.target;
    if (target) navigateTo(target);
  });
});


// Product Data (Derived from Scraping & Link Audit)
const westernProducts = [
  { title: "Cowboy and Indian Teepee Art", url: "https://www.redbubble.com/people/Pieterhk/", img: "/images/scraped_image_015.jpg", store: "Redbubble" },
  { title: "Steam Train Drawstring Bag", url: "https://tinyurl.com/y5e37wbx", img: "/images/scraped_image_020.png", store: "Redbubble" },
  { title: "Covered Wagon Throw Pillow", url: "https://tinyurl.com/y4c5fuu8", img: "/images/scraped_image_012.jpg", store: "Redbubble" },
  { title: "Sheriff Badge Socks", url: "https://tinyurl.com/y3doz7of", img: "/images/scraped_image_008.jpg", store: "Redbubble" }
];

const apparelProducts = [
  { title: "Class of 2020 T-Shirt", url: "https://www.teepublic.com/user/theblackpanther", img: "/images/scraped_image_025.png", store: "TeePublic" },
  { title: "I Love Tennis", url: "https://www.teepublic.com/user/theblackpanther", img: "/images/scraped_image_030.png", store: "TeePublic" },
  { title: "Trump 2020 T-Shirt", url: "https://www.teepublic.com/user/theblackpanther", img: "/images/scraped_image_032.png", store: "TeePublic" },
  { title: "Sexy in Light Blue", url: "https://www.teepublic.com/user/theblackpanther", img: "/images/scraped_image_028.png", store: "TeePublic" }
];

const decorProducts = [
  { title: "Indian Tomahawk Tapestry", url: "https://www.redbubble.com/people/Pieterhk/", img: "/images/scraped_image_035.png", store: "Redbubble" },
  { title: "Whiskey Bottle Shower Curtain", url: "https://tinyurl.com/y6csen7e", img: "/images/scraped_image_038.png", store: "Redbubble" },
  { title: "Orange Glass Orb", url: "https://www.teepublic.com/user/theblackpanther", img: "/images/scraped_image_045.png", store: "TeePublic" },
  { title: "Chess Piece Poster", url: "https://www.teepublic.com/user/theblackpanther", img: "/images/scraped_image_050.png", store: "TeePublic" }
];

function createCard(product) {
  return `
    <article class="card">
      <div class="card-img-container">
        <img src="${product.img}" alt="${product.title}" loading="lazy">
      </div>
      <div class="card-content">
        <h3>${product.title}</h3>
        <p>Available exclusively on ${product.store}. Click below to view sizing, colors, and pricing.</p>
        <a href="${product.url}" target="_blank" rel="noopener" class="btn">View on ${product.store}</a>
      </div>
    </article>
  `;
}

function renderGrid(containerId, products) {
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = products.map(createCard).join('');
  }
}

// Initialize Grids
document.addEventListener('DOMContentLoaded', () => {
  renderGrid('western-grid', westernProducts);
  renderGrid('apparel-grid', apparelProducts);
  renderGrid('decor-grid', decorProducts);
});
