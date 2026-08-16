import './style.css'

// =====================================================
// Store Search URL helpers
// Uses artist-filtered search so clicks land on the
// artist's own results, not a generic store homepage.
// =====================================================
const RB1_BASE = "https://www.redbubble.com/people/Pieterhb/shop?query=";
const RB2_BASE = "https://www.redbubble.com/people/Pieterhk/shop?query=";
const TP_BASE  = "https://www.teepublic.com/user/theblackpanther?query=";

function rbUrl(title)  { return RB2_BASE + encodeURIComponent(title); }
function rbUrl1(title) { return RB1_BASE + encodeURIComponent(title); }
function tpUrl(title)  { return TP_BASE  + encodeURIComponent(title); }

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
    const target = link.dataset.target;
    if (target) {
      e.preventDefault();
      navigateTo(target);
    }
  });
});

// =====================================================
// WESTERN & COUNTRY ART - Redbubble Store
// =====================================================
const westernProducts = [
  { title: "Sheriff Badge Socks",               img: "/images/scraped_image_001.png", store: "Redbubble", url: rbUrl("Sheriff Badge Socks") },
  { title: "Wild West Covered Wagon Pillow",    img: "/images/scraped_image_005.png", store: "Redbubble", url: rbUrl("Wild West Covered Wagon") },
  { title: "Wild West Cowboy Boot Dress",       img: "/images/scraped_image_016.png", store: "Redbubble", url: rbUrl("Wild West Cowboy Boot") },
  { title: "Indian Tomahawk Tapestry",          img: "/images/scraped_image_018.png", store: "Redbubble", url: rbUrl("Indian Tomahawk Tapestry") },
  { title: "Cowboy & Indian Teepee Art",        img: "/images/scraped_image_022.png", store: "Redbubble", url: rbUrl("Cowboy Indian Teepee") },
  { title: "Western Lady Duvet Cover",          img: "/images/scraped_image_004.png", store: "Redbubble", url: rbUrl("Western Lady Duvet") },
  { title: "Covered Wagon Throw Pillow",        img: "/images/scraped_image_005.png", store: "Redbubble", url: rbUrl("Covered Wagon Pillow") },
  { title: "Steam Train Drawstring Bag",        img: "/images/scraped_image_046.png", store: "Redbubble", url: rbUrl("Steam Train Drawstring Bag") },
  { title: "Western Era Whiskey Shower Curtain",img: "/images/scraped_image_065.png", store: "Redbubble", url: rbUrl("Western Era Whiskey Shower Curtain") },
  { title: "Wild West Sheriff Badge T-Shirt",   img: "/images/scraped_image_042.png", store: "Redbubble", url: rbUrl("Wild West Sheriff Badge") },
  { title: "Western Horse Rider Phone Case",    img: "/images/scraped_image_043.png", store: "Redbubble", url: rbUrl("Western Horse Rider Phone Case") },
  { title: "Cowboy Hat Art Print",              img: "/images/scraped_image_068.png", store: "Redbubble", url: rbUrl("Cowboy Hat Art Print") },
  { title: "Wild West Boot Leggings",           img: "/images/scraped_image_035.png", store: "Redbubble", url: rbUrl("Wild West Boot Leggings") },
  { title: "Western Bandana Scarf",             img: "/images/scraped_image_032.png", store: "Redbubble", url: rbUrl("Western Bandana Scarf") },
  { title: "Native American Eagle Print",       img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Native American Eagle") },
  { title: "Wild West Stampede Duvet",          img: "/images/scraped_image_060.png", store: "Redbubble", url: rbUrl("Wild West Stampede Duvet") },
  { title: "Cowboy Rodeo Art Print",            img: "/images/scraped_image_026.png", store: "Redbubble", url: rbUrl("Cowboy Rodeo Art Print") },
  { title: "Western Ranch Throw Pillow",        img: "/images/scraped_image_041.png", store: "Redbubble", url: rbUrl("Western Ranch Throw Pillow") },
];

// =====================================================
// GRAPHIC T-SHIRTS & APPAREL - TeePublic Store
// =====================================================
const apparelProducts = [
  { title: "Yin Yang Pink Mandala T-Shirt",    img: "/images/scraped_image_002.png", store: "TeePublic", url: tpUrl("Yin Yang Pink Mandala") },
  { title: "Chess Dragon Crest T-Shirt",        img: "/images/scraped_image_003.png", store: "TeePublic", url: tpUrl("Chess Dragon Crest") },
  { title: "Yin Yang Red Circle T-Shirt",       img: "/images/scraped_image_007.png", store: "TeePublic", url: tpUrl("Yin Yang Red Circle") },
  { title: "Captain Scarlet & Blue T-Shirt",   img: "/images/scraped_image_009.png", store: "TeePublic", url: tpUrl("Captain Scarlet Blue") },
  { title: "Red Alien T-Shirt",                 img: "/images/scraped_image_010.png", store: "TeePublic", url: tpUrl("Red Alien") },
  { title: "Space Planet Galaxy T-Shirt",       img: "/images/scraped_image_011.png", store: "TeePublic", url: tpUrl("Space Planet Galaxy") },
  { title: "Colorful Swirl Vortex T-Shirt",    img: "/images/scraped_image_013.png", store: "TeePublic", url: tpUrl("Colorful Swirl Vortex") },
  { title: "Gothic Alphabet T-Shirt",           img: "/images/scraped_image_019.png", store: "TeePublic", url: tpUrl("Gothic Alphabet") },
  { title: "Alien Newbies T-Shirt",             img: "/images/scraped_image_021.png", store: "TeePublic", url: tpUrl("Alien Newbies") },
  { title: "Class of 2020 Vintage T-Shirt",    img: "/images/scraped_image_074.png", store: "TeePublic", url: tpUrl("Class of 2020") },
  { title: "Yin Yang Yellow Ball Pattern",      img: "/images/scraped_image_020.png", store: "TeePublic", url: tpUrl("Yin Yang Yellow Ball") },
  { title: "Love Heart Rings T-Shirt",          img: "/images/scraped_image_008.jpg", store: "TeePublic", url: tpUrl("Love Heart Rings") },
  { title: "Triquetra Spiral Art T-Shirt",      img: "/images/scraped_image_015.jpg", store: "TeePublic", url: tpUrl("Triquetra Spiral") },
  { title: "Yin Yang Triple Ball T-Shirt",      img: "/images/scraped_image_030.png", store: "TeePublic", url: tpUrl("Yin Yang Triple Ball") },
  { title: "Sexy Light Blue T-Shirt",           img: "/images/scraped_image_070.png", store: "TeePublic", url: tpUrl("Sexy Light Blue") },
  { title: "Love Rainbow Heart T-Shirt",        img: "/images/scraped_image_012.jpg", store: "TeePublic", url: tpUrl("Love Rainbow Heart") },
  { title: "I Love Tennis T-Shirt",             img: "/images/scraped_image_063.png", store: "TeePublic", url: tpUrl("I Love Tennis") },
  { title: "Colorful Love Rings T-Shirt",       img: "/images/scraped_image_008.jpg", store: "TeePublic", url: tpUrl("Colorful Love Rings") },
  { title: "Trump 2020 Face Mask",              img: "/images/scraped_image_044.png", store: "TeePublic", url: tpUrl("Trump 2020") },
  { title: "Orange Glass Orb Globe T-Shirt",   img: "/images/scraped_image_057.png", store: "TeePublic", url: tpUrl("Orange Glass Orb") },
  { title: "Cyber Punk Robot T-Shirt",          img: "/images/scraped_image_072.png", store: "TeePublic", url: tpUrl("Cyber Punk Robot") },
  { title: "Neon Pop Art T-Shirt",              img: "/images/scraped_image_036.png", store: "TeePublic", url: tpUrl("Neon Pop Art") },
  { title: "Abstract Digital Art T-Shirt",      img: "/images/scraped_image_037.png", store: "TeePublic", url: tpUrl("Abstract Digital Art") },
  { title: "Retro Space Shuttle T-Shirt",       img: "/images/scraped_image_077.png", store: "TeePublic", url: tpUrl("Retro Space Shuttle") },
  { title: "Birthday Vintage Year T-Shirt",     img: "/images/scraped_image_025.png", store: "TeePublic", url: tpUrl("Birthday Vintage") },
  { title: "Psychedelic Circle T-Shirt",        img: "/images/scraped_image_039.jpg", store: "TeePublic", url: tpUrl("Psychedelic Circle") },
  { title: "Colorful Fractal Art T-Shirt",      img: "/images/scraped_image_055.png", store: "TeePublic", url: tpUrl("Colorful Fractal Art") },
  { title: "Digital Wave Art T-Shirt",          img: "/images/scraped_image_061.png", store: "TeePublic", url: tpUrl("Digital Wave Art") },
  { title: "Bright Bloom T-Shirt",              img: "/images/scraped_image_067.png", store: "TeePublic", url: tpUrl("Bright Bloom") },
  { title: "Blue Star Network T-Shirt",         img: "/images/scraped_image_045.png", store: "TeePublic", url: tpUrl("Blue Star Network") },
  { title: "Artistic Dragon T-Shirt",           img: "/images/scraped_image_058.png", store: "TeePublic", url: tpUrl("Artistic Dragon") },
  { title: "Tribal Pattern T-Shirt",            img: "/images/scraped_image_059.png", store: "TeePublic", url: tpUrl("Tribal Pattern") },
  { title: "Geometric Art T-Shirt",             img: "/images/scraped_image_066.png", store: "TeePublic", url: tpUrl("Geometric Art") },
];

// =====================================================
// WALL ART & HOME DECOR - Redbubble & TeePublic
// =====================================================
const decorProducts = [
  { title: "Western Lady Fantasy Duvet Cover", img: "/images/scraped_image_004.png", store: "Redbubble", url: rbUrl("Western Lady Fantasy Duvet") },
  { title: "Indian Tomahawk Wall Tapestry",    img: "/images/scraped_image_018.png", store: "Redbubble", url: rbUrl("Indian Tomahawk Tapestry") },
  { title: "Wild West Wagon Floor Pillow",     img: "/images/scraped_image_005.png", store: "Redbubble", url: rbUrl("Wild West Wagon Floor Pillow") },
  { title: "Western Era Shower Curtain",       img: "/images/scraped_image_065.png", store: "Redbubble", url: rbUrl("Western Era Shower Curtain") },
  { title: "Chess Piece Art Poster",           img: "/images/scraped_image_076.png", store: "TeePublic", url: tpUrl("Chess Piece Art Poster") },
  { title: "Orange Glass Globe Ornament",      img: "/images/scraped_image_057.png", store: "TeePublic", url: tpUrl("Orange Glass Globe") },
  { title: "Colorful Spiral Wall Art",         img: "/images/scraped_image_041.png", store: "Redbubble", url: rbUrl("Colorful Spiral Wall Art") },
  { title: "Sheriff Badge Wall Print",         img: "/images/scraped_image_027.png", store: "Redbubble", url: rbUrl("Sheriff Badge Wall Print") },
  { title: "Psychedelic Home Decor Print",     img: "/images/scraped_image_078.png", store: "Redbubble", url: rbUrl("Psychedelic Home Decor") },
  { title: "Abstract Art Canvas Print",        img: "/images/scraped_image_050.png", store: "Redbubble", url: rbUrl("Abstract Art Canvas") },
  { title: "Tomahawk Art Tapestry",            img: "/images/scraped_image_018.png", store: "Redbubble", url: rbUrl("Tomahawk Art Tapestry") },
  { title: "Wild West Throw Blanket",          img: "/images/scraped_image_064.png", store: "Redbubble", url: rbUrl("Wild West Throw Blanket") },
  { title: "Western Boot Wall Decor",          img: "/images/scraped_image_038.png", store: "Redbubble", url: rbUrl("Western Boot Wall Decor") },
  { title: "Cowboy Art Framed Print",          img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Cowboy Art Framed Print") },
  { title: "Indian Eagle Tapestry",            img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Indian Eagle Tapestry") },
  { title: "Native Art Wall Hanging",          img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Native Art Wall Hanging") },
  { title: "Western Mandala Art Print",        img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Western Mandala Art") },
  { title: "Vintage Western Poster",           img: "/images/scraped_image_068.png", store: "Redbubble", url: rbUrl("Vintage Western Poster") },
  { title: "Western Ranch Floor Pillow",       img: "/images/scraped_image_041.png", store: "Redbubble", url: rbUrl("Western Ranch Floor Pillow") },
  { title: "Buffalo Stampede Wall Art",        img: "/images/scraped_image_022.png", store: "Redbubble", url: rbUrl("Buffalo Stampede Wall Art") },
  { title: "Abstract Digital Canvas",          img: "/images/scraped_image_079.png", store: "Redbubble", url: rbUrl("Abstract Digital Canvas") },
  { title: "Geometric Wall Print",             img: "/images/scraped_image_050.png", store: "Redbubble", url: rbUrl("Geometric Wall Print") },
  { title: "Rodeo Art Duvet Cover",            img: "/images/scraped_image_060.png", store: "Redbubble", url: rbUrl("Rodeo Art Duvet") },
  { title: "Colorful Spiral Poster",           img: "/images/scraped_image_041.png", store: "Redbubble", url: rbUrl("Colorful Spiral Poster") },
  { title: "Western Boot Throw Pillow",        img: "/images/scraped_image_022.png", store: "Redbubble", url: rbUrl("Western Boot Throw Pillow") },
  { title: "Native American Dreamcatcher",     img: "/images/scraped_image_031.png", store: "Redbubble", url: rbUrl("Native American Dreamcatcher") },
  { title: "Wild West Art Print",              img: "/images/scraped_image_068.png", store: "Redbubble", url: rbUrl("Wild West Art Print") },
  { title: "Cowboy Ranch Duvet",               img: "/images/scraped_image_060.png", store: "Redbubble", url: rbUrl("Cowboy Ranch Duvet") },
  { title: "Western Emblem Wall Art",          img: "/images/scraped_image_042.png", store: "Redbubble", url: rbUrl("Western Emblem Wall Art") },
  { title: "Sheriff Star Poster",              img: "/images/scraped_image_042.png", store: "Redbubble", url: rbUrl("Sheriff Star Poster") },
  { title: "Wild West Tapestry Large",         img: "/images/scraped_image_018.png", store: "Redbubble", url: rbUrl("Wild West Tapestry") },
  { title: "Native Eagle Feather Print",       img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Native Eagle Feather") },
  { title: "Western Country Wall Canvas",      img: "/images/scraped_image_053.png", store: "Redbubble", url: rbUrl("Western Country Wall") },
  { title: "Classic Western Art Poster",       img: "/images/scraped_image_051.png", store: "Redbubble", url: rbUrl("Classic Western Art Poster") },
  { title: "Cowboy Legend Wall Hanging",       img: "/images/scraped_image_026.png", store: "Redbubble", url: rbUrl("Cowboy Legend Wall Hanging") },
  { title: "Western Heritage Art Print",       img: "/images/scraped_image_042.png", store: "Redbubble", url: rbUrl("Western Heritage Art") },
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
