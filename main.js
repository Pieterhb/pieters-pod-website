import './style.css'

// Store URLs
const RB1 = "https://www.redbubble.com/people/Pieterhb/"; // Redbubble Store 1 (Pieterhb)
const RB2 = "https://www.redbubble.com/people/Pieterhk/"; // Redbubble Store 2 (Pieterhk)
const RB  = RB2; // Default RB alias used by existing product cards
const TP  = "https://www.teepublic.com/user/theblackpanther";

// Navigation Logic
const navLinks = document.querySelectorAll('nav a, .nav-btn, .logo, .nav-btn-footer');
const views = document.querySelectorAll('.view');

function navigateTo(targetId) {
  views.forEach(view => {
    view.classList.toggle('active', view.id === targetId);
  });
  document.querySelectorAll('nav a').forEach(link => {
    link.classList.toggle('active', link.dataset.target === targetId);
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

// =====================================================
// WESTERN & COUNTRY ART - Redbubble Store
// =====================================================
const westernProducts = [
  { title: "Sheriff Badge Socks", img: "/images/scraped_image_001.png", store: "Redbubble", url: RB },
  { title: "Wild West Covered Wagon Pillow", img: "/images/scraped_image_005.png", store: "Redbubble", url: RB },
  { title: "Wild West Cowboy Boot Dress", img: "/images/scraped_image_016.png", store: "Redbubble", url: RB },
  { title: "Indian Tomahawk Tapestry", img: "/images/scraped_image_018.png", store: "Redbubble", url: RB },
  { title: "Cowboy & Indian Teepee Art", img: "/images/scraped_image_022.png", store: "Redbubble", url: RB },
  { title: "Western Lady Duvet Cover", img: "/images/scraped_image_004.png", store: "Redbubble", url: RB },
  { title: "Covered Wagon Throw Pillow", img: "/images/scraped_image_005.png", store: "Redbubble", url: RB },
  { title: "Steam Train Drawstring Bag", img: "/images/scraped_image_046.png", store: "Redbubble", url: RB },
  { title: "Western Era Whiskey Shower Curtain", img: "/images/scraped_image_065.png", store: "Redbubble", url: RB },
  { title: "Wild West Sheriff Badge T-Shirt", img: "/images/scraped_image_042.png", store: "Redbubble", url: RB },
  { title: "Western Horse Rider Phone Case", img: "/images/scraped_image_043.png", store: "Redbubble", url: RB },
  { title: "Cowboy Hat Art Print", img: "/images/scraped_image_068.png", store: "Redbubble", url: RB },
  { title: "Wild West Boot Leggings", img: "/images/scraped_image_035.png", store: "Redbubble", url: RB },
  { title: "Western Bandana Scarf", img: "/images/scraped_image_032.png", store: "Redbubble", url: RB },
  { title: "Native American Eagle Print", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Wild West Stampede Duvet", img: "/images/scraped_image_060.png", store: "Redbubble", url: RB },
  { title: "Cowboy Rodeo Art Print", img: "/images/scraped_image_026.png", store: "Redbubble", url: RB },
  { title: "Western Ranch Throw Pillow", img: "/images/scraped_image_041.png", store: "Redbubble", url: RB },
];

// =====================================================
// GRAPHIC T-SHIRTS & APPAREL - TeePublic Store
// =====================================================
const apparelProducts = [
  { title: "Yin Yang Pink Mandala T-Shirt", img: "/images/scraped_image_002.png", store: "TeePublic", url: TP },
  { title: "Chess Dragon Crest T-Shirt", img: "/images/scraped_image_003.png", store: "TeePublic", url: TP },
  { title: "Yin Yang Red Circle T-Shirt", img: "/images/scraped_image_007.png", store: "TeePublic", url: TP },
  { title: "Captain Scarlet & Blue T-Shirt", img: "/images/scraped_image_009.png", store: "TeePublic", url: TP },
  { title: "Red Alien T-Shirt", img: "/images/scraped_image_010.png", store: "TeePublic", url: TP },
  { title: "Space Planet Galaxy T-Shirt", img: "/images/scraped_image_011.png", store: "TeePublic", url: TP },
  { title: "Colorful Swirl Vortex T-Shirt", img: "/images/scraped_image_013.png", store: "TeePublic", url: TP },
  { title: "Gothic Alphabet T-Shirt", img: "/images/scraped_image_019.png", store: "TeePublic", url: TP },
  { title: "Alien Newbies T-Shirt", img: "/images/scraped_image_021.png", store: "TeePublic", url: TP },
  { title: "Class of 2020 Vintage T-Shirt", img: "/images/scraped_image_074.png", store: "TeePublic", url: TP },
  { title: "Yin Yang Yellow Ball Pattern", img: "/images/scraped_image_020.png", store: "TeePublic", url: TP },
  { title: "Love Heart Rings T-Shirt", img: "/images/scraped_image_008.jpg", store: "TeePublic", url: TP },
  { title: "Triquetra Spiral Art T-Shirt", img: "/images/scraped_image_015.jpg", store: "TeePublic", url: TP },
  { title: "Yin Yang Triple Ball T-Shirt", img: "/images/scraped_image_030.png", store: "TeePublic", url: TP },
  { title: "Sexy Light Blue T-Shirt", img: "/images/scraped_image_070.png", store: "TeePublic", url: TP },
  { title: "Love Rainbow Heart T-Shirt", img: "/images/scraped_image_012.jpg", store: "TeePublic", url: TP },
  { title: "I Love Tennis T-Shirt", img: "/images/scraped_image_063.png", store: "TeePublic", url: TP },
  { title: "Colorful Love Rings T-Shirt", img: "/images/scraped_image_008.jpg", store: "TeePublic", url: TP },
  { title: "Trump 2020 Face Mask", img: "/images/scraped_image_044.png", store: "TeePublic", url: TP },
  { title: "Orange Glass Orb Globe T-Shirt", img: "/images/scraped_image_057.png", store: "TeePublic", url: TP },
  { title: "Cyber Punk Robot T-Shirt", img: "/images/scraped_image_072.png", store: "TeePublic", url: TP },
  { title: "Neon Pop Art T-Shirt", img: "/images/scraped_image_036.png", store: "TeePublic", url: TP },
  { title: "Abstract Digital Art T-Shirt", img: "/images/scraped_image_037.png", store: "TeePublic", url: TP },
  { title: "Retro Space Shuttle T-Shirt", img: "/images/scraped_image_077.png", store: "TeePublic", url: TP },
  { title: "Birthday Vintage Year T-Shirt", img: "/images/scraped_image_025.png", store: "TeePublic", url: TP },
  { title: "Psychedelic Circle T-Shirt", img: "/images/scraped_image_039.jpg", store: "TeePublic", url: TP },
  { title: "Colorful Fractal Art T-Shirt", img: "/images/scraped_image_055.png", store: "TeePublic", url: TP },
  { title: "Digital Wave Art T-Shirt", img: "/images/scraped_image_061.png", store: "TeePublic", url: TP },
  { title: "Bright Bloom T-Shirt", img: "/images/scraped_image_067.png", store: "TeePublic", url: TP },
  { title: "Blue Star Network T-Shirt", img: "/images/scraped_image_045.png", store: "TeePublic", url: TP },
  { title: "Artistic Dragon T-Shirt", img: "/images/scraped_image_058.png", store: "TeePublic", url: TP },
  { title: "Tribal Pattern T-Shirt", img: "/images/scraped_image_059.png", store: "TeePublic", url: TP },
  { title: "Geometric Art T-Shirt", img: "/images/scraped_image_066.png", store: "TeePublic", url: TP },
];

// =====================================================
// WALL ART & HOME DECOR - Redbubble & TeePublic
// =====================================================
const decorProducts = [
  { title: "Western Lady Fantasy Duvet Cover", img: "/images/scraped_image_004.png", store: "Redbubble", url: RB },
  { title: "Indian Tomahawk Wall Tapestry", img: "/images/scraped_image_018.png", store: "Redbubble", url: RB },
  { title: "Wild West Wagon Floor Pillow", img: "/images/scraped_image_005.png", store: "Redbubble", url: RB },
  { title: "Western Era Shower Curtain", img: "/images/scraped_image_065.png", store: "Redbubble", url: RB },
  { title: "Chess Piece Art Poster", img: "/images/scraped_image_076.png", store: "TeePublic", url: TP },
  { title: "Orange Glass Globe Ornament", img: "/images/scraped_image_057.png", store: "TeePublic", url: TP },
  { title: "Colorful Spiral Wall Art", img: "/images/scraped_image_041.png", store: "Redbubble", url: RB },
  { title: "Sheriff Badge Wall Print", img: "/images/scraped_image_027.png", store: "Redbubble", url: RB },
  { title: "Psychedelic Home Decor Print", img: "/images/scraped_image_078.png", store: "Redbubble", url: RB },
  { title: "Abstract Art Canvas Print", img: "/images/scraped_image_050.png", store: "Redbubble", url: RB },
  { title: "Tomahawk Art Tapestry", img: "/images/scraped_image_018.png", store: "Redbubble", url: RB },
  { title: "Wild West Throw Blanket", img: "/images/scraped_image_064.png", store: "Redbubble", url: RB },
  { title: "Western Boot Wall Decor", img: "/images/scraped_image_038.png", store: "Redbubble", url: RB },
  { title: "Cowboy Art Framed Print", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Indian Eagle Tapestry", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Native Art Wall Hanging", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Western Mandala Art Print", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Vintage Western Poster", img: "/images/scraped_image_068.png", store: "Redbubble", url: RB },
  { title: "Western Ranch Floor Pillow", img: "/images/scraped_image_041.png", store: "Redbubble", url: RB },
  { title: "Buffalo Stampede Wall Art", img: "/images/scraped_image_022.png", store: "Redbubble", url: RB },
  { title: "Abstract Digital Canvas", img: "/images/scraped_image_079.png", store: "Redbubble", url: RB },
  { title: "Geometric Wall Print", img: "/images/scraped_image_050.png", store: "Redbubble", url: RB },
  { title: "Rodeo Art Duvet Cover", img: "/images/scraped_image_060.png", store: "Redbubble", url: RB },
  { title: "Colorful Spiral Poster", img: "/images/scraped_image_041.png", store: "Redbubble", url: RB },
  { title: "Western Boot Throw Pillow", img: "/images/scraped_image_022.png", store: "Redbubble", url: RB },
  { title: "Native American Dreamcatcher", img: "/images/scraped_image_031.png", store: "Redbubble", url: RB },
  { title: "Wild West Art Print", img: "/images/scraped_image_068.png", store: "Redbubble", url: RB },
  { title: "Cowboy Ranch Duvet", img: "/images/scraped_image_060.png", store: "Redbubble", url: RB },
  { title: "Western Emblem Wall Art", img: "/images/scraped_image_042.png", store: "Redbubble", url: RB },
  { title: "Sheriff Star Poster", img: "/images/scraped_image_042.png", store: "Redbubble", url: RB },
  { title: "Wild West Tapestry Large", img: "/images/scraped_image_018.png", store: "Redbubble", url: RB },
  { title: "Native Eagle Feather Print", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Western Country Wall Canvas", img: "/images/scraped_image_053.png", store: "Redbubble", url: RB },
  { title: "Classic Western Art Poster", img: "/images/scraped_image_051.png", store: "Redbubble", url: RB },
  { title: "Cowboy Legend Wall Hanging", img: "/images/scraped_image_026.png", store: "Redbubble", url: RB },
  { title: "Western Heritage Art Print", img: "/images/scraped_image_042.png", store: "Redbubble", url: RB },
];

// =====================================================
// Card Template
// =====================================================
function createCard(product) {
  const storeBadgeClass = product.store === 'Redbubble' ? 'badge-rb' : 'badge-tp';
  return `
    <article class="card">
      <div class="card-img-container">
        <img src="${product.img}" alt="${product.title}" loading="lazy">
        <span class="store-badge ${storeBadgeClass}">${product.store}</span>
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

// =====================================================
// Filter / Search Logic
// =====================================================
function setupFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const store = btn.dataset.store;
      const gridId = btn.closest('.filter-bar').dataset.grid;
      const allProducts = {
        'western-grid': westernProducts,
        'apparel-grid': apparelProducts,
        'decor-grid': decorProducts,
      };
      let products = allProducts[gridId];
      if (store !== 'all') {
        products = products.filter(p => p.store === store);
      }
      renderGrid(gridId, products);
    });
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  renderGrid('western-grid', westernProducts);
  renderGrid('apparel-grid', apparelProducts);
  renderGrid('decor-grid', decorProducts);
  setupFilters();
});
