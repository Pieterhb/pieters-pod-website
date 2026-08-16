"""
Programmatic SEO (pSEO) Static Site Generator
Generates ~108 high-quality, anti-thin-content landing pages for Pieter's POD Art website.
Each page targets a distinct long-tail keyword and contains unique editorial copy,
4-12 real product cards, breadcrumbs, JSON-LD structured data, and cross-links.

Run: python build_pseo.py
Output: subdirectories under c:\\googlepod\\website\\ (deployed by Vite/Cloudflare Pages)
"""

import os
import json
import shutil
from datetime import datetime
from math import ceil

from site_config import (
    SITE_URL, SITE_NAME, SITE_TITLE_SUFFIX, SITE_TAGLINE,
    DEFAULT_DESCRIPTION, GA_ID, PUBLISHER_NAME, PUBLISHER_LOGO,
    DEFAULT_OG_IMAGE, STORE_RB1, STORE_RB2, STORE_TP
)

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
RB = STORE_RB2  # default Redbubble alias

# ===========================================================================
# PRODUCT DATA
# ===========================================================================

# Every product: title, image path (relative to public/), store label, store URL, tags list
PRODUCTS = [
    # ---- Western & Country Art (Redbubble) ----
    {"id": "w01", "title": "Sheriff Badge Socks",            "img": "/images/scraped_image_001.png", "store": "Redbubble", "url": RB,      "tags": ["western","cowboy","sheriff","socks","accessories","gifts"]},
    {"id": "w02", "title": "Wild West Covered Wagon Pillow", "img": "/images/scraped_image_005.png", "store": "Redbubble", "url": RB,      "tags": ["western","cowboy","pillow","home-decor","wild-west","gifts"]},
    {"id": "w03", "title": "Wild West Cowboy Boot Dress",    "img": "/images/scraped_image_016.png", "store": "Redbubble", "url": RB,      "tags": ["western","cowboy","apparel","dress","women","fashion"]},
    {"id": "w04", "title": "Indian Tomahawk Tapestry",       "img": "/images/scraped_image_018.png", "store": "Redbubble", "url": RB,      "tags": ["native-american","tapestry","wall-art","home-decor","western"]},
    {"id": "w05", "title": "Cowboy & Indian Teepee Art",     "img": "/images/scraped_image_022.png", "store": "Redbubble", "url": RB,      "tags": ["western","native-american","wall-art","cowboy","gifts"]},
    {"id": "w06", "title": "Western Lady Duvet Cover",       "img": "/images/scraped_image_004.png", "store": "Redbubble", "url": RB,      "tags": ["western","duvet","home-decor","bedroom","fantasy","women"]},
    {"id": "w07", "title": "Steam Train Drawstring Bag",     "img": "/images/scraped_image_046.png", "store": "Redbubble", "url": RB,      "tags": ["western","train","bag","accessories","travel","gifts"]},
    {"id": "w08", "title": "Western Era Whiskey Shower Curtain","img": "/images/scraped_image_065.png","store":"Redbubble","url":RB,       "tags": ["western","shower-curtain","bathroom","home-decor","vintage"]},
    {"id": "w09", "title": "Wild West Sheriff Badge T-Shirt","img": "/images/scraped_image_042.png", "store": "Redbubble", "url": RB,      "tags": ["western","sheriff","t-shirt","apparel","men","cowboy"]},
    {"id": "w10", "title": "Western Horse Rider Phone Case", "img": "/images/scraped_image_043.png", "store": "Redbubble", "url": RB,      "tags": ["western","phone-case","cowboy","horse","accessories","gifts"]},
    {"id": "w11", "title": "Cowboy Hat Art Print",           "img": "/images/scraped_image_068.png", "store": "Redbubble", "url": RB,      "tags": ["western","wall-art","cowboy","print","home-decor","vintage"]},
    {"id": "w12", "title": "Wild West Boot Leggings",        "img": "/images/scraped_image_035.png", "store": "Redbubble", "url": RB,      "tags": ["western","leggings","apparel","women","cowboy","fashion"]},
    {"id": "w13", "title": "Western Bandana Scarf",          "img": "/images/scraped_image_032.png", "store": "Redbubble", "url": RB,      "tags": ["western","bandana","scarf","accessories","cowboy","fashion"]},
    {"id": "w14", "title": "Native American Eagle Print",    "img": "/images/scraped_image_053.png", "store": "Redbubble", "url": RB,      "tags": ["native-american","eagle","wall-art","print","home-decor"]},
    {"id": "w15", "title": "Wild West Stampede Duvet",       "img": "/images/scraped_image_060.png", "store": "Redbubble", "url": RB,      "tags": ["western","duvet","bedroom","home-decor","buffalo","wild-west"]},
    {"id": "w16", "title": "Cowboy Rodeo Art Print",         "img": "/images/scraped_image_026.png", "store": "Redbubble", "url": RB,      "tags": ["western","rodeo","wall-art","cowboy","print","gifts"]},
    {"id": "w17", "title": "Western Ranch Throw Pillow",     "img": "/images/scraped_image_041.png", "store": "Redbubble", "url": RB,      "tags": ["western","pillow","home-decor","ranch","cowboy","gifts"]},
    {"id": "w18", "title": "Sheriff Badge Wall Print",       "img": "/images/scraped_image_027.png", "store": "Redbubble", "url": RB,      "tags": ["western","sheriff","wall-art","print","cowboy","home-decor"]},
    {"id": "w19", "title": "Native American Dreamcatcher",   "img": "/images/scraped_image_031.png", "store": "Redbubble", "url": RB,      "tags": ["native-american","dreamcatcher","wall-art","gifts","home-decor"]},
    {"id": "w20", "title": "Wild West Throw Blanket",        "img": "/images/scraped_image_064.png", "store": "Redbubble", "url": RB,      "tags": ["western","blanket","home-decor","cowboy","gifts","cozy"]},
    {"id": "w21", "title": "Western Boot Wall Decor",        "img": "/images/scraped_image_038.png", "store": "Redbubble", "url": RB,      "tags": ["western","boot","wall-art","home-decor","cowboy","country"]},
    {"id": "w22", "title": "Cowboy Rodeo Floor Pillow",      "img": "/images/scraped_image_041.png", "store": "Redbubble", "url": RB,      "tags": ["western","pillow","floor-pillow","cowboy","home-decor"]},
    {"id": "w23", "title": "Wild West Buffalo Tapestry",     "img": "/images/scraped_image_022.png", "store": "Redbubble", "url": RB,      "tags": ["western","tapestry","wall-art","buffalo","home-decor"]},
    {"id": "w24", "title": "Western Heritage Poster",        "img": "/images/scraped_image_051.png", "store": "Redbubble", "url": RB,      "tags": ["western","poster","wall-art","heritage","vintage","cowboy"]},
    {"id": "w25", "title": "Cowboy Legend Wall Hanging",     "img": "/images/scraped_image_026.png", "store": "Redbubble", "url": RB,      "tags": ["western","wall-art","cowboy","hanging","home-decor","gifts"]},

    # ---- Graphic T-Shirts & Apparel (TeePublic) ----
    {"id": "a01", "title": "Yin Yang Pink Mandala T-Shirt",  "img": "/images/scraped_image_002.png", "store": "TeePublic", "url": STORE_TP, "tags": ["yin-yang","mandala","t-shirt","apparel","spiritual","men","women"]},
    {"id": "a02", "title": "Chess Dragon Crest T-Shirt",     "img": "/images/scraped_image_003.png", "store": "TeePublic", "url": STORE_TP, "tags": ["chess","dragon","t-shirt","apparel","fantasy","gifts"]},
    {"id": "a03", "title": "Yin Yang Red Circle T-Shirt",    "img": "/images/scraped_image_007.png", "store": "TeePublic", "url": STORE_TP, "tags": ["yin-yang","t-shirt","apparel","spiritual","men","women","gifts"]},
    {"id": "a04", "title": "Captain Scarlet & Blue T-Shirt", "img": "/images/scraped_image_009.png", "store": "TeePublic", "url": STORE_TP, "tags": ["sci-fi","t-shirt","apparel","retro","vintage","men","gifts"]},
    {"id": "a05", "title": "Red Alien T-Shirt",              "img": "/images/scraped_image_010.png", "store": "TeePublic", "url": STORE_TP, "tags": ["alien","sci-fi","t-shirt","apparel","men","gifts","funny"]},
    {"id": "a06", "title": "Space Planet Galaxy T-Shirt",    "img": "/images/scraped_image_011.png", "store": "TeePublic", "url": STORE_TP, "tags": ["space","galaxy","planet","t-shirt","apparel","sci-fi","men"]},
    {"id": "a07", "title": "Colorful Swirl Vortex T-Shirt",  "img": "/images/scraped_image_013.png", "store": "TeePublic", "url": STORE_TP, "tags": ["psychedelic","swirl","t-shirt","apparel","colorful","abstract"]},
    {"id": "a08", "title": "Gothic Alphabet T-Shirt",        "img": "/images/scraped_image_019.png", "store": "TeePublic", "url": STORE_TP, "tags": ["gothic","alphabet","t-shirt","apparel","dark","men","unique"]},
    {"id": "a09", "title": "Alien Newbies T-Shirt",          "img": "/images/scraped_image_021.png", "store": "TeePublic", "url": STORE_TP, "tags": ["alien","funny","t-shirt","apparel","sci-fi","gifts","novelty"]},
    {"id": "a10", "title": "Class of 2020 Vintage T-Shirt",  "img": "/images/scraped_image_074.png", "store": "TeePublic", "url": STORE_TP, "tags": ["graduation","class-of-2020","t-shirt","apparel","vintage","gifts"]},
    {"id": "a11", "title": "Yin Yang Yellow Ball Pattern",   "img": "/images/scraped_image_020.png", "store": "TeePublic", "url": STORE_TP, "tags": ["yin-yang","t-shirt","apparel","spiritual","colorful","men"]},
    {"id": "a12", "title": "Love Heart Rings T-Shirt",       "img": "/images/scraped_image_008.jpg", "store": "TeePublic", "url": STORE_TP, "tags": ["love","heart","t-shirt","apparel","romantic","women","gifts"]},
    {"id": "a13", "title": "Triquetra Spiral Art T-Shirt",   "img": "/images/scraped_image_015.jpg", "store": "TeePublic", "url": STORE_TP, "tags": ["triquetra","celtic","t-shirt","apparel","spiritual","gifts"]},
    {"id": "a14", "title": "Yin Yang Triple Ball T-Shirt",   "img": "/images/scraped_image_030.png", "store": "TeePublic", "url": STORE_TP, "tags": ["yin-yang","t-shirt","apparel","spiritual","pattern","men"]},
    {"id": "a15", "title": "Sexy Light Blue T-Shirt",        "img": "/images/scraped_image_070.png", "store": "TeePublic", "url": STORE_TP, "tags": ["fashion","t-shirt","apparel","women","casual","blue"]},
    {"id": "a16", "title": "Love Rainbow Heart T-Shirt",     "img": "/images/scraped_image_012.jpg", "store": "TeePublic", "url": STORE_TP, "tags": ["love","rainbow","heart","t-shirt","apparel","pride","women"]},
    {"id": "a17", "title": "I Love Tennis T-Shirt",          "img": "/images/scraped_image_063.png", "store": "TeePublic", "url": STORE_TP, "tags": ["tennis","sports","t-shirt","apparel","gifts","men","women"]},
    {"id": "a18", "title": "Trump 2020 Face Mask",           "img": "/images/scraped_image_044.png", "store": "TeePublic", "url": STORE_TP, "tags": ["political","face-mask","accessories","novelty","gifts"]},
    {"id": "a19", "title": "Orange Glass Orb Globe T-Shirt", "img": "/images/scraped_image_057.png", "store": "TeePublic", "url": STORE_TP, "tags": ["abstract","digital-art","t-shirt","apparel","colorful","unique"]},
    {"id": "a20", "title": "Cyber Punk Robot T-Shirt",       "img": "/images/scraped_image_072.png", "store": "TeePublic", "url": STORE_TP, "tags": ["cyberpunk","robot","sci-fi","t-shirt","apparel","men","tech"]},
    {"id": "a21", "title": "Neon Pop Art T-Shirt",           "img": "/images/scraped_image_036.png", "store": "TeePublic", "url": STORE_TP, "tags": ["pop-art","neon","t-shirt","apparel","colorful","abstract","men"]},
    {"id": "a22", "title": "Abstract Digital Art T-Shirt",   "img": "/images/scraped_image_037.png", "store": "TeePublic", "url": STORE_TP, "tags": ["abstract","digital-art","t-shirt","apparel","colorful","unique"]},
    {"id": "a23", "title": "Retro Space Shuttle T-Shirt",    "img": "/images/scraped_image_077.png", "store": "TeePublic", "url": STORE_TP, "tags": ["space","retro","shuttle","t-shirt","apparel","sci-fi","men"]},
    {"id": "a24", "title": "Birthday Vintage Year T-Shirt",  "img": "/images/scraped_image_025.png", "store": "TeePublic", "url": STORE_TP, "tags": ["birthday","vintage","t-shirt","apparel","gifts","men","women"]},
    {"id": "a25", "title": "Psychedelic Circle T-Shirt",     "img": "/images/scraped_image_039.jpg", "store": "TeePublic", "url": STORE_TP, "tags": ["psychedelic","circle","t-shirt","apparel","colorful","abstract"]},
    {"id": "a26", "title": "Colorful Fractal Art T-Shirt",   "img": "/images/scraped_image_055.png", "store": "TeePublic", "url": STORE_TP, "tags": ["fractal","digital-art","t-shirt","apparel","colorful","abstract"]},
    {"id": "a27", "title": "Digital Wave Art T-Shirt",       "img": "/images/scraped_image_061.png", "store": "TeePublic", "url": STORE_TP, "tags": ["digital-art","wave","t-shirt","apparel","abstract","colorful"]},
    {"id": "a28", "title": "Bright Bloom T-Shirt",           "img": "/images/scraped_image_067.png", "store": "TeePublic", "url": STORE_TP, "tags": ["floral","bright","t-shirt","apparel","women","colorful","gifts"]},
    {"id": "a29", "title": "Blue Star Network T-Shirt",      "img": "/images/scraped_image_045.png", "store": "TeePublic", "url": STORE_TP, "tags": ["sci-fi","star","network","t-shirt","apparel","abstract","men"]},
    {"id": "a30", "title": "Artistic Dragon T-Shirt",        "img": "/images/scraped_image_058.png", "store": "TeePublic", "url": STORE_TP, "tags": ["dragon","fantasy","t-shirt","apparel","men","gifts","art"]},
    {"id": "a31", "title": "Tribal Pattern T-Shirt",         "img": "/images/scraped_image_059.png", "store": "TeePublic", "url": STORE_TP, "tags": ["tribal","pattern","t-shirt","apparel","ethnic","men","women"]},
    {"id": "a32", "title": "Geometric Art T-Shirt",          "img": "/images/scraped_image_066.png", "store": "TeePublic", "url": STORE_TP, "tags": ["geometric","abstract","t-shirt","apparel","modern","men","women"]},

    # ---- Home Decor & Wall Art (Redbubble + TeePublic) ----
    {"id": "d01", "title": "Western Lady Fantasy Duvet Cover","img":"/images/scraped_image_004.png","store":"Redbubble","url":RB,          "tags": ["western","duvet","bedroom","home-decor","fantasy","women"]},
    {"id": "d02", "title": "Indian Tomahawk Wall Tapestry",   "img":"/images/scraped_image_018.png","store":"Redbubble","url":RB,          "tags": ["native-american","tapestry","wall-art","home-decor","western"]},
    {"id": "d03", "title": "Wild West Wagon Floor Pillow",    "img":"/images/scraped_image_005.png","store":"Redbubble","url":RB,          "tags": ["western","floor-pillow","home-decor","cowboy","wild-west"]},
    {"id": "d04", "title": "Western Era Shower Curtain",      "img":"/images/scraped_image_065.png","store":"Redbubble","url":RB,          "tags": ["western","shower-curtain","bathroom","home-decor","vintage"]},
    {"id": "d05", "title": "Chess Piece Art Poster",          "img":"/images/scraped_image_076.png","store":"TeePublic","url":STORE_TP,    "tags": ["chess","poster","wall-art","home-decor","gifts","games"]},
    {"id": "d06", "title": "Orange Glass Globe Ornament",     "img":"/images/scraped_image_057.png","store":"TeePublic","url":STORE_TP,    "tags": ["abstract","ornament","home-decor","colorful","gifts","unique"]},
    {"id": "d07", "title": "Colorful Spiral Wall Art",        "img":"/images/scraped_image_041.png","store":"Redbubble","url":RB,          "tags": ["spiral","wall-art","home-decor","colorful","abstract","print"]},
    {"id": "d08", "title": "Psychedelic Home Decor Print",    "img":"/images/scraped_image_078.png","store":"Redbubble","url":RB,          "tags": ["psychedelic","print","wall-art","home-decor","colorful","abstract"]},
    {"id": "d09", "title": "Abstract Art Canvas Print",       "img":"/images/scraped_image_050.png","store":"Redbubble","url":RB,          "tags": ["abstract","canvas","wall-art","home-decor","modern","print"]},
    {"id": "d10", "title": "Wild West Throw Blanket",         "img":"/images/scraped_image_064.png","store":"Redbubble","url":RB,          "tags": ["western","blanket","home-decor","cowboy","cozy","gifts"]},
    {"id": "d11", "title": "Vintage Western Poster",          "img":"/images/scraped_image_068.png","store":"Redbubble","url":RB,          "tags": ["western","vintage","poster","wall-art","cowboy","home-decor"]},
    {"id": "d12", "title": "Western Ranch Floor Pillow",      "img":"/images/scraped_image_041.png","store":"Redbubble","url":RB,          "tags": ["western","floor-pillow","home-decor","ranch","cowboy"]},
    {"id": "d13", "title": "Buffalo Stampede Wall Art",       "img":"/images/scraped_image_022.png","store":"Redbubble","url":RB,          "tags": ["western","buffalo","wall-art","home-decor","wild-west","print"]},
    {"id": "d14", "title": "Abstract Digital Canvas",         "img":"/images/scraped_image_079.png","store":"Redbubble","url":RB,          "tags": ["abstract","digital-art","canvas","wall-art","home-decor","modern"]},
    {"id": "d15", "title": "Native Eagle Feather Print",      "img":"/images/scraped_image_053.png","store":"Redbubble","url":RB,          "tags": ["native-american","eagle","feather","print","wall-art","home-decor"]},
    {"id": "d16", "title": "Rodeo Art Duvet Cover",           "img":"/images/scraped_image_060.png","store":"Redbubble","url":RB,          "tags": ["western","rodeo","duvet","bedroom","home-decor","cowboy"]},
    {"id": "d17", "title": "Geometric Wall Print",            "img":"/images/scraped_image_050.png","store":"Redbubble","url":RB,          "tags": ["geometric","wall-art","home-decor","modern","print","abstract"]},
    {"id": "d18", "title": "Colorful Spiral Poster",          "img":"/images/scraped_image_041.png","store":"Redbubble","url":RB,          "tags": ["spiral","poster","wall-art","colorful","abstract","home-decor"]},
    {"id": "d19", "title": "Western Boot Throw Pillow",       "img":"/images/scraped_image_038.png","store":"Redbubble","url":RB,          "tags": ["western","boot","pillow","home-decor","cowboy","gifts"]},
    {"id": "d20", "title": "Classic Western Art Poster",      "img":"/images/scraped_image_051.png","store":"Redbubble","url":RB,          "tags": ["western","poster","wall-art","classic","home-decor","vintage"]},
    {"id": "d21", "title": "Cowboy Rope Art Print",           "img":"/images/scraped_image_026.png","store":"Redbubble","url":RB,          "tags": ["western","cowboy","rope","wall-art","print","home-decor"]},
    {"id": "d22", "title": "Dreamcatcher Wall Hanging",       "img":"/images/scraped_image_031.png","store":"Redbubble","url":RB,          "tags": ["native-american","dreamcatcher","wall-hanging","home-decor","gifts"]},
    {"id": "d23", "title": "Western Country Tapestry",        "img":"/images/scraped_image_018.png","store":"Redbubble","url":RB,          "tags": ["western","country","tapestry","wall-art","home-decor","large"]},
]

# ===========================================================================
# PAGE DEFINITIONS
# Every page: slug, section (for URL path), title, h1, meta_description,
#             body_intro, body_closing, product_ids (list of product IDs to show),
#             breadcrumb_label, related_slugs (other page slugs to cross-link)
# ===========================================================================

PAGES = [

    # ====================== /designs/ ======================
    {
        "slug": "cowboy-art-gifts",
        "section": "designs",
        "title": "Cowboy Art Gifts — Unique Western Designs",
        "h1": "Cowboy Art Gifts: Unique Western Designs for True Fans",
        "meta": "Shop one-of-a-kind cowboy art gifts. From sheriff badge socks to rodeo prints, find the perfect western gift on Redbubble and TeePublic.",
        "intro": """If you're searching for cowboy art gifts that go beyond the generic, you've landed in the right place. 
These designs celebrate the raw beauty of the American West — dusty trails, rugged horses, vintage sheriff badges, 
and the timeless spirit of the cowboy. Every piece here is an original design by independent artist Pieter, 
available as wearables, home decor, accessories, and more through Redbubble and TeePublic.""",
        "closing": """Whether you're buying for a Western enthusiast, decorating a ranch-style home, or simply love 
the aesthetic of the Wild West, these cowboy art gifts offer something truly unique. Each design is printed 
on demand, so every order is freshly made just for you — no mass production, no compromises on quality.""",
        "products": ["w01","w09","w11","w16","w18","w25","d11","d20"],
        "breadcrumb_label": "Cowboy Art Gifts",
        "related": ["sheriff-badge-gifts","western-gifts-for-him","western-home-decor","cowboy-prints"],
    },
    {
        "slug": "sheriff-badge-gifts",
        "section": "designs",
        "title": "Sheriff Badge Gifts — Western Law & Order Art",
        "h1": "Sheriff Badge Gifts: Bold Western Law & Order Designs",
        "meta": "Discover sheriff badge gifts and western law art. Unique printed gifts including socks, t-shirts, and wall prints. Shop on Redbubble.",
        "intro": """The sheriff's star has always been a symbol of authority, justice, and the golden era of the American 
West. These sheriff badge gifts capture that bold, iconic look in wearable and decorative formats. 
From socks embroidered with a gleaming star to wall art prints that command attention, each design 
brings a piece of frontier history into your everyday life.""",
        "closing": """Perfect as gifts for western fans, law enforcement enthusiasts, or anyone who loves classic 
Americana design. The sheriff badge motif translates beautifully onto a wide range of printed products — 
browse the selection and find the right gift for any occasion.""",
        "products": ["w01","w09","w18","w16","w11","w25","d11","d20"],
        "breadcrumb_label": "Sheriff Badge Gifts",
        "related": ["cowboy-art-gifts","western-gifts-for-him","western-wall-art","cowboy-prints"],
    },
    {
        "slug": "yin-yang-art-shirts",
        "section": "designs",
        "title": "Yin Yang Art T-Shirts — Spiritual Balance Designs",
        "h1": "Yin Yang Art T-Shirts: Spiritual Balance in Wearable Form",
        "meta": "Browse unique yin yang t-shirts with mandala and spiritual designs. Handcrafted digital art printed on premium quality shirts. Available on TeePublic.",
        "intro": """The yin yang symbol speaks of duality, balance, and harmony — concepts that resonate across cultures 
and centuries. These yin yang art t-shirts take that timeless symbol and reimagine it through vivid digital 
artistry: mandalas, bold color fields, layered circles, and intricate patterns. Each design is a meditation 
in visual balance, perfect for those drawn to spiritual or philosophical aesthetics.""",
        "closing": """Available in a wide range of sizes and colors on TeePublic, these shirts make thoughtful gifts 
for yoga practitioners, philosophy students, spiritual seekers, or anyone who appreciates the art of balance. 
Print-on-demand means your shirt is made fresh — no dyes faded by sitting on a shelf for months.""",
        "products": ["a01","a03","a11","a14","a25","a07","a26","a22"],
        "breadcrumb_label": "Yin Yang Art Shirts",
        "related": ["spiritual-art-tees","mandala-art-prints","graphic-tees-for-men","psychedelic-art-shirts"],
    },
    {
        "slug": "alien-sci-fi-tees",
        "section": "designs",
        "title": "Alien & Sci-Fi T-Shirts — Out-of-This-World Designs",
        "h1": "Alien & Sci-Fi T-Shirts: Out-of-This-World Graphic Designs",
        "meta": "Shop alien and sci-fi graphic t-shirts with original extraterrestrial and space designs. Available on TeePublic in multiple styles and sizes.",
        "intro": """From wide-eyed alien newbies to red extraterrestrials and cyber punk robots, these alien and sci-fi 
t-shirts celebrate the strange and wonderful universe beyond our own. Each design is crafted with a playful 
or awe-inspiring visual language — vivid colors, bold line work, and a healthy dose of cosmic imagination. 
If you believe the universe is bigger than we know, wear it proudly.""",
        "closing": """These shirts make the ultimate gift for sci-fi fans, gamers, stargazers, and anyone fascinated by 
extraterrestrial life. Available through TeePublic in classic tee, long sleeve, and hoodie formats — because 
space exploration calls for comfortable wear.""",
        "products": ["a05","a09","a06","a20","a23","a29","a04","a08"],
        "breadcrumb_label": "Alien & Sci-Fi Tees",
        "related": ["space-galaxy-art","graphic-tees-for-men","cyberpunk-tees","sci-fi-gifts"],
    },
    {
        "slug": "psychedelic-art-shirts",
        "section": "designs",
        "title": "Psychedelic Art T-Shirts — Vivid Colorful Designs",
        "h1": "Psychedelic Art T-Shirts: Vivid, Mind-Bending Designs",
        "meta": "Explore psychedelic graphic t-shirts with swirling vortex, fractal, and abstract art designs. Unique prints on TeePublic.",
        "intro": """Color that vibrates. Shapes that swirl. Patterns that seem to move when you look at them long enough. 
These psychedelic art t-shirts are a celebration of digital art at its most expressive — vortices of color, 
fractal geometries, spiral mandalas, and abstract compositions that defy convention. Wear your inner universe 
on your sleeve, literally.""",
        "closing": """Perfect for festival wear, casual everyday style, or as a conversation-starting gift. These 
designs are printed on demand through TeePublic using high-quality direct-to-garment printing, ensuring 
the vivid colors stay true wash after wash.""",
        "products": ["a07","a25","a26","a22","a21","a27","a19","a01"],
        "breadcrumb_label": "Psychedelic Art Shirts",
        "related": ["yin-yang-art-shirts","abstract-art-prints","colorful-graphic-tees","spiritual-art-tees"],
    },
    {
        "slug": "dragon-fantasy-art",
        "section": "designs",
        "title": "Dragon & Fantasy Art — Gifts for Fantasy Lovers",
        "h1": "Dragon & Fantasy Art: Bold Gifts for Fantasy Enthusiasts",
        "meta": "Discover dragon and fantasy art gifts including t-shirts, prints, and accessories. Original designs available on TeePublic and Redbubble.",
        "intro": """Dragons have captured human imagination for millennia — creatures of fire, power, and ancient magic. 
These dragon and fantasy art designs bring that mythology to life through vivid digital artistry. Whether 
it's a chess-themed dragon crest or an artistic fire-breathing legend, these designs speak to the fantasy 
lover in everyone. Combined with western mythos and sci-fi themes, this collection bridges worlds.""",
        "closing": """Available as t-shirts, phone cases, posters, and more through TeePublic and Redbubble. These 
make exceptional gifts for gamers, tabletop RPG players, fantasy novel readers, and anyone who keeps 
the magic of imagination alive.""",
        "products": ["a02","a30","a08","a29","w05","d05","a20","a04"],
        "breadcrumb_label": "Dragon & Fantasy Art",
        "related": ["alien-sci-fi-tees","chess-art-gifts","graphic-tees-for-men","sci-fi-gifts"],
    },
    {
        "slug": "native-american-art",
        "section": "designs",
        "title": "Native American Art Gifts — Authentic Inspired Designs",
        "h1": "Native American Art Gifts: Inspired Designs Full of Cultural Beauty",
        "meta": "Explore Native American-inspired art gifts: tapestries, prints, dreamcatchers, and wall art. Original designs on Redbubble.",
        "intro": """With deep reverence for the rich visual heritage of Indigenous American cultures, these designs 
draw inspiration from the symbols, patterns, and imagery of the Native American tradition — eagles soaring 
in painted skies, tomahawks etched with geometric detail, dreamcatchers woven with feathers and beads, 
and warrior art that speaks of honor and endurance.""",
        "closing": """These Native American-inspired art gifts are printed on a variety of products through Redbubble — 
from large-format tapestries and throw pillows to framed wall prints. Each product is printed fresh on 
your order, using vibrant, long-lasting inks.""",
        "products": ["w04","w14","w19","d02","d15","d22","w05","d23"],
        "breadcrumb_label": "Native American Art",
        "related": ["western-home-decor","western-wall-art","cowboy-art-gifts","wall-tapestries"],
    },
    {
        "slug": "cyberpunk-tees",
        "section": "designs",
        "title": "Cyberpunk T-Shirts — Futuristic Tech Art Designs",
        "h1": "Cyberpunk T-Shirts: Wear the Future with Bold Tech Art",
        "meta": "Shop cyberpunk and futuristic art t-shirts with robot, neon, and digital designs. Unique sci-fi wearables on TeePublic.",
        "intro": """In the neon-soaked alleys of the near future, style is everything. These cyberpunk t-shirts blend 
technology, rebellion, and vivid visual design into wearable art. From chrome-plated robots and glowing 
network grids to pop-art explosions of color, these designs are for those who live at the intersection 
of tech and creativity.""",
        "closing": """Available through TeePublic in multiple garment styles and dozens of colorways, these shirts are 
as versatile as they are distinctive. Whether you're dressing for a gaming convention, a casual Friday, 
or a night out, cyberpunk art makes a statement.""",
        "products": ["a20","a21","a22","a29","a08","a27","a06","a19"],
        "breadcrumb_label": "Cyberpunk Tees",
        "related": ["alien-sci-fi-tees","graphic-tees-for-men","sci-fi-gifts","abstract-art-prints"],
    },
    {
        "slug": "chess-art-gifts",
        "section": "designs",
        "title": "Chess Art Gifts — Unique Designs for Chess Lovers",
        "h1": "Chess Art Gifts: Unique Pieces for the Passionate Chess Player",
        "meta": "Find original chess art gifts including t-shirts, posters, and prints for chess enthusiasts. Available on TeePublic and Redbubble.",
        "intro": """Chess is more than a game — it's a battlefield of the mind, a dance of strategy, and an art form 
with centuries of history. These chess art gifts translate that intellectual passion into vivid visual design. 
The dragon crest shirt merges chess with fantasy mythology; the art poster presents chess pieces as monumental 
sculptures. Perfect gifts for club players, grandmasters in training, or chess lovers of all levels.""",
        "closing": """Available as t-shirts and framed prints through TeePublic and Redbubble. Each item is printed 
fresh on demand, ensuring crisp, gallery-quality images that the chess lover in your life will cherish.""",
        "products": ["a02","d05","a30","a08","d09","d14","d17","d07"],
        "breadcrumb_label": "Chess Art Gifts",
        "related": ["dragon-fantasy-art","graphic-tees-for-men","wall-art-prints","unique-gifts"],
    },
    {
        "slug": "abstract-art-prints",
        "section": "designs",
        "title": "Abstract Art Prints — Modern Digital Wall Art",
        "h1": "Abstract Art Prints: Modern Digital Wall Art for Contemporary Spaces",
        "meta": "Discover abstract digital art prints for modern interiors. Geometric, spiral, and colorful abstract designs available on Redbubble.",
        "intro": """Abstract art has the remarkable ability to evoke emotion without depicting anything recognizable — 
pure color, form, and movement. These abstract art prints use the latest digital tools to create compositions 
that feel alive: geometric grids that pulse with hidden energy, spirals that draw the eye inward, 
and color explosions that bring warmth or drama to any room.""",
        "closing": """All prints are available through Redbubble in multiple formats and sizes — from small framed 
prints for a bookshelf to large format canvas art that anchors an entire wall. These abstract designs 
suit modern, minimalist, and eclectic interiors with equal ease.""",
        "products": ["d07","d08","d09","d14","d17","d18","w04","d02"],
        "breadcrumb_label": "Abstract Art Prints",
        "related": ["western-wall-art","psychedelic-art-shirts","colorful-graphic-tees","wall-art-prints"],
    },
    {
        "slug": "tribal-art-designs",
        "section": "designs",
        "title": "Tribal Art Designs — Bold Ethnic Pattern Apparel",
        "h1": "Tribal Art Designs: Bold Ethnic Patterns on Premium Apparel",
        "meta": "Shop tribal and ethnic pattern t-shirts and art prints. Original digital designs inspired by global tribal traditions. Available on TeePublic.",
        "intro": """Tribal art has existed as long as humanity itself — patterns that encode identity, story, and 
spiritual meaning into bold geometric forms. These tribal art designs translate those ancient visual 
languages into modern graphic apparel. Bold lines, repeating patterns, and strong geometric compositions 
make each design visually compelling and culturally resonant.""",
        "closing": """Available as t-shirts and apparel through TeePublic. These designs suit both men and women, 
offering a wearable connection to the rich visual heritage of global tribal traditions.""",
        "products": ["a31","a13","a32","a01","a07","a14","a22","a25"],
        "breadcrumb_label": "Tribal Art Designs",
        "related": ["native-american-art","spiritual-art-tees","graphic-tees-for-men","yin-yang-art-shirts"],
    },
    {
        "slug": "spiritual-art-tees",
        "section": "designs",
        "title": "Spiritual Art T-Shirts — Sacred Symbol Designs",
        "h1": "Spiritual Art T-Shirts: Wear Your Sacred Symbols with Pride",
        "meta": "Browse spiritual art t-shirts featuring yin yang, triquetra, mandala, and sacred geometry. Available on TeePublic in multiple styles.",
        "intro": """For those who wear their spiritual journey outwardly, these spiritual art t-shirts offer a 
meaningful selection. Yin yang symbols in multiple color interpretations, triquetra Celtic spirals, 
mandala patterns radiating perfect symmetry, and sacred geometry that speaks to the structure of 
the universe — each design is a statement of inner values made visible.""",
        "closing": """Available through TeePublic in a full range of garment types and sizes. These make thoughtful 
gifts for yoga teachers, meditation practitioners, spiritual students, and anyone who finds beauty 
in sacred symbolism.""",
        "products": ["a01","a03","a11","a13","a14","a31","a07","a25"],
        "breadcrumb_label": "Spiritual Art Tees",
        "related": ["yin-yang-art-shirts","tribal-art-designs","mandala-art-prints","graphic-tees-for-women"],
    },
    {
        "slug": "retro-vintage-art-tees",
        "section": "designs",
        "title": "Retro & Vintage Art T-Shirts — Classic Era Designs",
        "h1": "Retro & Vintage Art T-Shirts: Celebrate the Golden Eras of Design",
        "meta": "Shop retro and vintage art t-shirts with classic 50s, 60s, and 70s inspired designs. Available on TeePublic.",
        "intro": """There's something enduring about the visual language of bygone eras — the bold typographic 
energy of the 1950s, the psychedelic explosion of the 1960s, the space-age optimism of the 1970s. 
These retro and vintage art t-shirts capture that nostalgic aesthetic with modern printing quality. 
Captain Scarlet space age designs, retro shuttle graphics, vintage year typography — each design 
is a loving tribute to classic era artistry.""",
        "closing": """Available through TeePublic, these retro designs make perfect gifts for nostalgia fans, 
classic car enthusiasts, vintage lovers, and anyone who appreciates art that references the golden 
age of graphic design.""",
        "products": ["a04","a10","a23","a24","a08","a07","w08","d11"],
        "breadcrumb_label": "Retro & Vintage Tees",
        "related": ["graphic-tees-for-men","cyberpunk-tees","birthday-gift-tees","alien-sci-fi-tees"],
    },
    {
        "slug": "colorful-graphic-tees",
        "section": "designs",
        "title": "Colorful Graphic T-Shirts — Bold Vibrant Designs",
        "h1": "Colorful Graphic T-Shirts: Bold, Vibrant Designs That Stand Out",
        "meta": "Discover colorful graphic t-shirts with vivid digital art. Abstract, psychedelic, and nature-inspired designs available on TeePublic.",
        "intro": """Life is too short for dull clothes. These colorful graphic t-shirts inject energy and personality 
into everyday wardrobes — bold color combinations, vivid digital art, and designs that catch the eye 
from across the room. From neon pop-art to floral bursts to swirling vortices, each shirt is a canvas 
of expression that makes a statement without needing a single word.""",
        "closing": """Available through TeePublic in standard tee, fitted, long sleeve, and hoodie styles. The 
vibrant colors are achieved through high-quality direct-to-garment printing, maintaining brightness 
through repeated washes.""",
        "products": ["a07","a21","a26","a27","a28","a16","a19","a22"],
        "breadcrumb_label": "Colorful Graphic Tees",
        "related": ["psychedelic-art-shirts","graphic-tees-for-men","graphic-tees-for-women","abstract-art-prints"],
    },
    {
        "slug": "sports-hobby-tees",
        "section": "designs",
        "title": "Sports & Hobby T-Shirts — Gifts for Active People",
        "h1": "Sports & Hobby T-Shirts: The Perfect Gift for Active People",
        "meta": "Find sports and hobby t-shirts including tennis, chess, and activity-themed designs. Unique printed gifts on TeePublic.",
        "intro": """Passion deserves to be worn. These sports and hobby t-shirts let the active people in your life 
show off what they love — from a sleek tennis-themed print for the court star in your family to 
chess-themed designs for the strategic thinker. Each design is an original digital artwork that 
elevates the humble t-shirt into a meaningful personal statement.""",
        "closing": """Available through TeePublic in multiple sizes and garment types, these activity shirts make 
ideal birthday gifts, holiday gifts, and 'just because' presents. Show the people you love that 
you really see who they are.""",
        "products": ["a17","a02","d05","a10","a24","a15","a12","a16"],
        "breadcrumb_label": "Sports & Hobby Tees",
        "related": ["graphic-tees-for-men","birthday-gift-tees","chess-art-gifts","unique-gifts"],
    },

    # ====================== /products/ ======================
    {
        "slug": "western-throw-pillows",
        "section": "products",
        "title": "Western Throw Pillows — Cowboy Home Decor",
        "h1": "Western Throw Pillows: Bring the Wild West Into Your Living Room",
        "meta": "Shop western throw pillows with cowboy, ranch, and wild west designs. Available on Redbubble in multiple sizes.",
        "intro": """A throw pillow is a small but powerful design statement. These western throw pillows bring 
the rugged charm of the American West to your sofa, armchair, or bedroom — wagon trains crossing 
dusty plains, sheriff stars gleaming on aged leather, cowboy boots and lassos in rich earthy palettes. 
Each pillow features a full wraparound print of Pieter's original western digital art.""",
        "closing": """Available through Redbubble in multiple sizes, from small accent pillows to large floor 
pillows. The covers feature vivid, fade-resistant prints and easy-zip removal for washing. 
A perfect addition to any western, ranch, or rustic-themed interior.""",
        "products": ["w02","w17","w22","d03","d12","d19","w07","w20"],
        "breadcrumb_label": "Western Throw Pillows",
        "related": ["western-home-decor","cowboy-art-gifts","western-bedroom-decor","western-gifts-for-him"],
    },
    {
        "slug": "graphic-tees-for-men",
        "section": "products",
        "title": "Graphic T-Shirts for Men — Bold Art Designs",
        "h1": "Graphic T-Shirts for Men: Bold Designs That Define Your Style",
        "meta": "Browse graphic t-shirts for men with western, sci-fi, abstract, and artistic designs. Unique art prints available on TeePublic and Redbubble.",
        "intro": """The right t-shirt tells the world something about who you are before you say a word. These 
graphic t-shirts for men span a wide range of themes — the rugged cool of the cowboy west, 
the mind-bending dimension of alien sci-fi, the spiritual depth of yin yang symbolism, 
and the bold edge of cyberpunk tech. Each design is an original digital artwork, printed fresh 
on premium garments through TeePublic and Redbubble.""",
        "closing": """Available in standard, fitted, and relaxed cuts across a broad range of sizes. These shirts 
are ideal for everyday wear, weekend adventures, or as uniquely personal gifts for men who have 
their own distinctive style.""",
        "products": ["w09","a05","a20","a08","a06","a02","a31","a30"],
        "breadcrumb_label": "Graphic Tees for Men",
        "related": ["colorful-graphic-tees","alien-sci-fi-tees","cowboy-art-gifts","cyberpunk-tees"],
    },
    {
        "slug": "graphic-tees-for-women",
        "section": "products",
        "title": "Graphic T-Shirts for Women — Artistic & Expressive",
        "h1": "Graphic T-Shirts for Women: Wear Art That Speaks to You",
        "meta": "Shop graphic t-shirts for women with floral, spiritual, love, and artistic designs. Unique prints available on TeePublic in multiple sizes.",
        "intro": """Expression has no gender, but these graphic t-shirts for women are designed with a particular 
attention to aesthetic beauty — floral bursts of bright bloom, love hearts in rainbow palettes, 
yin yang mandalas that balance color and form, and western boot designs that channel frontier 
independence. Each shirt offers a distinct visual personality that complements a wide range of 
personal styles.""",
        "closing": """Available through TeePublic in fitted, classic, and boyfriend-cut styles across a full size 
range. These make wonderful gifts for birthdays, anniversaries, and any occasion when you want 
to give something personal and beautifully made.""",
        "products": ["a28","a12","a16","a01","a03","a15","a13","w03"],
        "breadcrumb_label": "Graphic Tees for Women",
        "related": ["spiritual-art-tees","colorful-graphic-tees","birthday-gift-tees","unique-gifts"],
    },
    {
        "slug": "wall-tapestries",
        "section": "products",
        "title": "Wall Tapestries — Large Format Art for Your Space",
        "h1": "Wall Tapestries: Large Format Art That Transforms Any Space",
        "meta": "Shop large format wall tapestries with western, native American, and abstract art designs. Available on Redbubble in multiple sizes.",
        "intro": """Few things transform a space as dramatically as a large wall tapestry. These tapestries feature 
Pieter's most striking original designs at their most expansive — Native American tomahawks and 
eagle imagery, wild west wagon trains, and abstract art compositions that become the visual anchor 
of an entire room. Lightweight and versatile, tapestries can hang from a rod, be draped over 
furniture, or laid as a floor covering.""",
        "closing": """Available through Redbubble in small, medium, and large sizes. The woven fabric ensures 
rich color reproduction and durability. Whether you're styling a bedroom, living room, dorm, 
or creative studio, a tapestry makes a bold, artistic statement.""",
        "products": ["w04","d02","d23","w23","d15","d07","d14","d08"],
        "breadcrumb_label": "Wall Tapestries",
        "related": ["western-wall-art","native-american-art","western-home-decor","wall-art-prints"],
    },
    {
        "slug": "wall-art-prints",
        "section": "products",
        "title": "Wall Art Prints — Original Designs for Your Walls",
        "h1": "Wall Art Prints: Original Designs That Make Your Walls Come Alive",
        "meta": "Discover wall art prints with western, abstract, and digital art designs. Framed prints and posters available on Redbubble.",
        "intro": """Your walls are a canvas waiting to be filled with meaning. These wall art prints offer 
original digital designs ranging from vintage western posters and Native American eagle imagery 
to vivid abstract art and geometric compositions. Each print is available in multiple sizes and 
formats — framed art, unframed prints, canvas — to suit your space and budget.""",
        "closing": """Available through Redbubble with a satisfaction guarantee. Each print is produced on 
archival-quality paper or canvas using high-fidelity inks that resist fading. Transform your 
home, office, or studio with art that's as original as you are.""",
        "products": ["w11","w16","w18","d09","d11","d13","d17","d20"],
        "breadcrumb_label": "Wall Art Prints",
        "related": ["abstract-art-prints","western-wall-art","native-american-art","western-home-decor"],
    },
    {
        "slug": "duvet-covers",
        "section": "products",
        "title": "Duvet Covers — Unique Art Prints for Your Bedroom",
        "h1": "Duvet Covers: Transform Your Bedroom with Original Art",
        "meta": "Shop duvet covers with western, abstract, and rodeo art designs. Unique printed bedding available on Redbubble in queen and king sizes.",
        "intro": """Your bedroom should be a sanctuary that reflects your personality — and nothing sets the tone 
like a beautifully designed duvet cover. These duvet covers feature Pieter's original art across 
the full surface, transforming your bed into a statement piece. Western lady fantasy art, buffalo 
stampedes at dawn, and rodeo action under a big sky — each design tells a story as it shelters 
you through the night.""",
        "closing": """Available through Redbubble in twin, queen, and king sizes. The covers feature a full-print 
exterior and a plain white interior, with convenient button closure. Machine washable and made 
from soft, breathable fabric.""",
        "products": ["w06","w15","d01","d16","d10","d23","d02","w04"],
        "breadcrumb_label": "Duvet Covers",
        "related": ["western-bedroom-decor","western-home-decor","cowboy-art-gifts","western-gifts-for-him"],
    },
    {
        "slug": "shower-curtains",
        "section": "products",
        "title": "Unique Shower Curtains — Art for Your Bathroom",
        "h1": "Unique Shower Curtains: Bring Original Art Into Your Bathroom",
        "meta": "Find unique shower curtains with western and vintage art designs. Original printed shower curtains available on Redbubble.",
        "intro": """Why should the bathroom miss out on great art? These unique shower curtains bring Pieter's 
original designs to one of the most functional objects in your home. The western whiskey bar 
scene evokes the saloon era of the frontier; the vintage western designs transform a mundane 
bathroom into a space with real character. Full-bleed print coverage means the design wraps 
edge to edge for maximum visual impact.""",
        "closing": """Available through Redbubble in standard shower curtain dimensions with included rings. 
The water-resistant fabric is woven for durability while maintaining beautiful color fidelity. 
A uniquely personal home decor upgrade that guests will notice and remember.""",
        "products": ["w08","d04","d11","d08","d07","w04","d02","d13"],
        "breadcrumb_label": "Shower Curtains",
        "related": ["western-home-decor","western-bathroom-decor","unique-gifts","western-gifts-for-him"],
    },
    {
        "slug": "phone-cases-western",
        "section": "products",
        "title": "Western Phone Cases — Wild West Art for Your Phone",
        "h1": "Western Phone Cases: Protect Your Phone with Wild West Art",
        "meta": "Shop western and cowboy phone cases with horse rider, badge, and frontier art designs. Available on Redbubble.",
        "intro": """Your phone is always with you — so why not give it a design that tells your story? These 
western phone cases feature Pieter's original wild west art, from a galloping horse rider in 
full motion to the bold geometry of the sheriff's star. Each case offers both protection and 
personality in a slim, precise-fit format for popular phone models.""",
        "closing": """Available through Redbubble for a wide range of iPhone and Samsung Galaxy models. 
Cases are available in soft flexible, tough, and slim formats depending on your protection 
preference. A stylish western gift idea that's both practical and personal.""",
        "products": ["w10","w01","w09","w13","w11","w18","d11","d05"],
        "breadcrumb_label": "Western Phone Cases",
        "related": ["cowboy-art-gifts","western-gifts-for-him","western-accessories","sheriff-badge-gifts"],
    },
    {
        "slug": "western-leggings",
        "section": "products",
        "title": "Western Leggings — Wild West Fashion for Women",
        "h1": "Western Leggings: Wild West Style Meets Active Comfort",
        "meta": "Shop western and cowboy leggings with boot and frontier art designs. Comfortable activewear available on Redbubble.",
        "intro": """The frontier spirit meets modern activewear. These western leggings feature Pieter's original 
cowboy boot and wild west art wrapped around high-stretch, comfortable fabric — perfect for yoga, 
gym sessions, casual weekends, or making a bold fashion statement. The all-over print technique 
means every inch of the legging carries the design, creating a cohesive and striking look.""",
        "closing": """Available through Redbubble in multiple sizes with a comfortable high waist. The stretch 
fabric is soft against the skin and designed to move with your body. A uniquely western take 
on athleisure — equally at home at the ranch or the yoga studio.""",
        "products": ["w12","w03","w13","a15","a28","a16","a01","a31"],
        "breadcrumb_label": "Western Leggings",
        "related": ["graphic-tees-for-women","western-gifts-for-her","cowboy-art-gifts","western-fashion"],
    },
    {
        "slug": "drawstring-bags",
        "section": "products",
        "title": "Art Drawstring Bags — Unique Printed Backpack Bags",
        "h1": "Art Drawstring Bags: Carry Your Style Wherever You Go",
        "meta": "Find unique art drawstring bags with western and steam train designs. Lightweight printed bags available on Redbubble.",
        "intro": """Practical meets artistic. These art drawstring bags feature original designs on lightweight, 
durable fabric — ideal for the gym, school, hiking, or as a stylish daily carry. The steam 
train design evokes a romantic era of long-distance travel and frontier adventure, while 
other western designs bring cowboy grit to your everyday essentials.""",
        "closing": """Available through Redbubble with adjustable drawstring straps and enough capacity for 
your daily essentials. These bags make excellent gifts for students, outdoor adventurers, 
and western art enthusiasts who want their accessories to say something.""",
        "products": ["w07","w13","w10","w01","d05","a17","a20","w09"],
        "breadcrumb_label": "Art Drawstring Bags",
        "related": ["western-accessories","cowboy-art-gifts","western-gifts-for-him","unique-gifts"],
    },
    {
        "slug": "mandala-art-prints",
        "section": "products",
        "title": "Mandala Art Prints — Sacred Geometry for Your Walls",
        "h1": "Mandala Art Prints: Sacred Geometry That Radiates Peace",
        "meta": "Browse mandala and sacred geometry art prints and t-shirts. Digital mandala designs available on TeePublic and Redbubble.",
        "intro": """The mandala — a sacred circular form found in Hindu, Buddhist, and Indigenous traditions — 
represents the universe, wholeness, and the infinite cycle of existence. These mandala art prints 
translate the ancient form into modern digital art: yin yang mandalas in vivid pink and gold, 
spiral mandalas with layered color depth, and geometric patterns that radiate outward in perfect 
symmetry. Each design is a meditative visual experience.""",
        "closing": """Available as wall art prints through Redbubble and as t-shirts through TeePublic. 
Whether you're decorating a meditation space, yoga studio, or bedroom, mandala art brings 
a sense of peace and intention to any environment.""",
        "products": ["a01","a11","a14","a25","a07","d07","d08","a26"],
        "breadcrumb_label": "Mandala Art Prints",
        "related": ["spiritual-art-tees","yin-yang-art-shirts","abstract-art-prints","wall-art-prints"],
    },

    # ====================== /gifts/ ======================
    {
        "slug": "cowboy-gifts-for-him",
        "section": "gifts",
        "title": "Cowboy Gifts for Him — Unique Western Art Gifts for Men",
        "h1": "Cowboy Gifts for Him: Unique Western Art That He'll Actually Love",
        "meta": "Find the perfect cowboy gifts for him: western art t-shirts, phone cases, pillows, and more. Shop on Redbubble and TeePublic.",
        "intro": """Finding a gift for the western art lover in your life just got easier. These cowboy gifts 
for him celebrate everything that makes the American West iconic — the rugged sheriff with his 
gleaming badge, the cowboy astride his horse at dusk, the steam train carving through frontier 
country. Each product is an original digital design printed fresh on demand, making it a truly 
unique gift that no department store can match.""",
        "closing": """Browse the full selection above and find the western gift that matches his personality — 
whether he's more sheriff-badge bold or vintage-poster nostalgic. All products ship directly 
from Redbubble or TeePublic with worldwide delivery and easy returns.""",
        "products": ["w01","w09","w10","w07","w11","w13","d11","d05"],
        "breadcrumb_label": "Cowboy Gifts for Him",
        "related": ["western-gifts-for-him","cowboy-art-gifts","sheriff-badge-gifts","unique-gifts"],
    },
    {
        "slug": "western-gifts-for-him",
        "section": "gifts",
        "title": "Western Gifts for Him — Wild West Art & Decor",
        "h1": "Western Gifts for Him: Wild West Art That Makes a Real Impression",
        "meta": "Browse the best western gifts for men including art prints, home decor, and wearables. Original designs on Redbubble and TeePublic.",
        "intro": """The man who loves the Wild West doesn't want a generic gift — he wants something with authentic 
western character. These western gifts for him range from bold cowboy art prints ready to hang on 
his workshop wall to sheriff badge accessories he'll use every day, and home decor that transforms 
his space into a proper frontier retreat. Every item is an original design by artist Pieter.""",
        "closing": """These products are available on Redbubble and TeePublic with worldwide shipping. Gift-giving 
for the western enthusiast has never been this authentic — and these prices are more affordable 
than you'd expect for original art merchandise.""",
        "products": ["w09","w10","w11","w16","w17","w20","d11","d20"],
        "breadcrumb_label": "Western Gifts for Him",
        "related": ["cowboy-gifts-for-him","cowboy-art-gifts","western-home-decor","unique-gifts"],
    },
    {
        "slug": "western-gifts-for-her",
        "section": "gifts",
        "title": "Western Gifts for Her — Cowgirl Art & Fashion",
        "h1": "Western Gifts for Her: Beautiful Cowgirl Art She'll Treasure",
        "meta": "Discover western gifts for women including cowgirl art, leggings, and bedroom decor. Unique designs on Redbubble.",
        "intro": """The cowgirl spirit is timeless — independent, fierce, and beautifully creative. These western 
gifts for her celebrate that spirit through original digital art: the western lady fantasy portrait, 
cowboy boot leggings for the active western woman, rustic bedroom duvet covers, and a western era 
shower curtain that brings frontier style into her daily routine.""",
        "closing": """All products available on Redbubble with easy international shipping. These gifts work 
beautifully for birthdays, anniversaries, Christmas, or any occasion when you want to give 
something personal and artistically meaningful.""",
        "products": ["w06","w12","w03","w13","d01","d16","d04","w15"],
        "breadcrumb_label": "Western Gifts for Her",
        "related": ["western-fashion","graphic-tees-for-women","western-bedroom-decor","unique-gifts"],
    },
    {
        "slug": "unique-birthday-gifts",
        "section": "gifts",
        "title": "Unique Birthday Gifts — Art Gifts That Stand Out",
        "h1": "Unique Birthday Gifts: Original Art Presents They'll Never Forget",
        "meta": "Find unique birthday gifts including vintage year t-shirts, art prints, and western decor. One-of-a-kind presents on TeePublic and Redbubble.",
        "intro": """The best birthday gift is one that shows you really know the person — something personal, 
original, and unexpectedly beautiful. These unique birthday gifts span a wide range of themes: 
the vintage year birthday t-shirt captures a specific graduation or birth year in bold typography; 
western art prints hang permanently as a reminder of a meaningful occasion; and graphic tees 
celebrate specific interests that say "I really see who you are.".""",
        "closing": """Every product here is available through TeePublic and Redbubble and ships worldwide. 
Print-on-demand means each gift is made fresh, ensuring the highest quality for a moment 
that deserves the best.""",
        "products": ["a24","a10","a17","a02","w09","d11","d05","a30"],
        "breadcrumb_label": "Unique Birthday Gifts",
        "related": ["birthday-gift-tees","unique-gifts","sci-fi-gifts","cowboy-gifts-for-him"],
    },
    {
        "slug": "unique-gifts",
        "section": "gifts",
        "title": "Unique Art Gifts — One-of-a-Kind Print on Demand",
        "h1": "Unique Art Gifts: Original Print-on-Demand Designs for Every Occasion",
        "meta": "Browse unique art gifts for any occasion. Original western, sci-fi, and abstract designs available on Redbubble and TeePublic.",
        "intro": """Gift giving is an art form — and these unique art gifts are crafted to make the act of 
giving as meaningful as the gift itself. Each product is an original design by independent 
artist Pieter, produced on demand to guarantee freshness and quality. From western cowboy 
art to alien sci-fi, spiritual mandalas to psychedelic abstracts, there's a design here 
for every personality and interest.""",
        "closing": """Browse through the full collection and find a gift that truly reflects the recipient's 
personality. All products are available through Redbubble and TeePublic with satisfaction 
guarantees and international shipping.""",
        "products": ["w09","a01","a05","d11","a17","w10","d05","a30"],
        "breadcrumb_label": "Unique Art Gifts",
        "related": ["cowboy-gifts-for-him","unique-birthday-gifts","sci-fi-gifts","western-gifts-for-him"],
    },
    {
        "slug": "sci-fi-gifts",
        "section": "gifts",
        "title": "Sci-Fi Gifts — Space & Alien Art for Enthusiasts",
        "h1": "Sci-Fi Gifts: Space, Aliens & the Future in Wearable Art",
        "meta": "Find sci-fi gifts including alien t-shirts, space art, and cyberpunk designs. Original art available on TeePublic.",
        "intro": """For the person who looks up at the night sky and wonders what's out there — these sci-fi 
gifts bring the cosmos down to earth in wearable and displayable form. Alien characters with 
their own strange charm, space planet prints that capture the scale of the universe, 
cyberpunk robots that live in the electric city of the future, retro space shuttles 
celebrating the golden age of exploration.""",
        "closing": """All available through TeePublic with a broad selection of garment styles and sizes. 
These make exceptional gifts for star wars fans, space lovers, gamers, and anyone who 
finds the future more interesting than the present.""",
        "products": ["a05","a09","a20","a06","a23","a29","a04","a22"],
        "breadcrumb_label": "Sci-Fi Gifts",
        "related": ["alien-sci-fi-tees","cyberpunk-tees","dragon-fantasy-art","unique-birthday-gifts"],
    },
    {
        "slug": "birthday-gift-tees",
        "section": "gifts",
        "title": "Birthday Gift T-Shirts — Personalized Year & Age Designs",
        "h1": "Birthday Gift T-Shirts: Celebrate Their Year with Original Art",
        "meta": "Shop birthday gift t-shirts with vintage year and graduation designs. Perfect personalized art gifts available on TeePublic.",
        "intro": """A birthday t-shirt isn't just a shirt — it's a time capsule. The vintage year design 
celebrates the year they were born or graduated in bold, nostalgic typography. The 
Class of 2020 shirt captures a uniquely challenging graduation year with genuine historical 
weight. These birthday gift t-shirts go beyond the generic to offer something genuinely 
meaningful that the recipient will actually wear.""",
        "closing": """Available through TeePublic in standard and fitted styles across a full size range. 
These can be ordered last-minute since TeePublic ships quickly — and every shirt is 
printed fresh to order to ensure maximum print quality.""",
        "products": ["a24","a10","a17","a15","a12","a16","a28","a01"],
        "breadcrumb_label": "Birthday Gift Tees",
        "related": ["unique-birthday-gifts","graphic-tees-for-women","graphic-tees-for-men","unique-gifts"],
    },
    {
        "slug": "home-decor-gifts",
        "section": "gifts",
        "title": "Home Decor Gifts — Art Prints & Decor for the Home",
        "h1": "Home Decor Gifts: Original Art for Every Room in the House",
        "meta": "Find home decor gifts including art prints, tapestries, pillows, and duvet covers. Unique printed gifts on Redbubble.",
        "intro": """When you give someone art for their home, you're giving them something they'll live with 
and love for years. These home decor gifts cover every room — large tapestries for living 
room walls, duvet covers that transform the bedroom, throw pillows that add western character 
to a sofa, shower curtains that make the bathroom worth noticing, and art prints that bring 
life to a blank wall.""",
        "closing": """All products ship from Redbubble with satisfaction guarantee. Each piece is printed 
fresh on demand, ensuring the quality that a meaningful home decor gift deserves. 
Choose by room, by style, or by the personality of the person you're gifting.""",
        "products": ["d02","d09","w17","d01","d04","d10","d13","d07"],
        "breadcrumb_label": "Home Decor Gifts",
        "related": ["western-home-decor","wall-art-prints","western-bedroom-decor","unique-gifts"],
    },

    # ====================== /themes/ ======================
    {
        "slug": "western-home-decor",
        "section": "themes",
        "title": "Western Home Decor — Wild West Art for Your Interior",
        "h1": "Western Home Decor: Transform Your Space with Wild West Art",
        "meta": "Discover western home decor including throw pillows, tapestries, duvet covers, and wall art. Original designs available on Redbubble.",
        "intro": """The American West has an interior design aesthetic all its own — warm earth tones, 
rugged materials, and imagery that celebrates freedom, open skies, and frontier spirit. 
These western home decor items bring that aesthetic into any home, from a ranch house 
in Texas to an apartment in a modern city. Original digital art printed on quality 
home goods creates an authentic western atmosphere wherever you place it.""",
        "closing": """All western home decor items are available through Redbubble with worldwide shipping. 
Whether you're decorating a room from scratch or adding western character to an existing 
space, these original art pieces offer the perfect finishing touch.""",
        "products": ["w02","w17","d02","d03","d04","d11","d13","w20"],
        "breadcrumb_label": "Western Home Decor",
        "related": ["western-bedroom-decor","western-wall-art","western-gifts-for-him","cowboy-art-gifts"],
    },
    {
        "slug": "western-bedroom-decor",
        "section": "themes",
        "title": "Western Bedroom Decor — Cowboy Art for the Bedroom",
        "h1": "Western Bedroom Decor: Create a Frontier Retreat in Your Bedroom",
        "meta": "Shop western bedroom decor including duvet covers, throw pillows, and wall art. Transform your bedroom with original western designs on Redbubble.",
        "intro": """The bedroom is where your day begins and ends — and western bedroom decor turns that 
space into a frontier retreat full of character and original art. Imagine a duvet cover 
featuring the wide-open stampede of a buffalo herd at sunrise, accent pillows with covered 
wagon designs, and a tapestry on the wall bringing the spirit of the American West into 
your most personal space.""",
        "closing": """All products available through Redbubble. Western bedroom decor makes an especially 
meaningful gift for someone moving into a new home, redecorating their bedroom, or 
celebrating a milestone. Pair a duvet with matching pillows for a complete western look.""",
        "products": ["w06","w15","d01","d16","w02","d03","d10","d23"],
        "breadcrumb_label": "Western Bedroom Decor",
        "related": ["western-home-decor","duvet-covers","western-throw-pillows","cowboy-art-gifts"],
    },
    {
        "slug": "western-wall-art",
        "section": "themes",
        "title": "Western Wall Art — Original Art Prints for Your Walls",
        "h1": "Western Wall Art: Original Frontier Art for Bold, Distinctive Walls",
        "meta": "Browse western wall art prints, posters, and tapestries. Original cowboy and wild west designs for your walls. Available on Redbubble.",
        "intro": """The right wall art defines a room's personality — and western wall art makes that 
statement with unmistakable confidence. Cowboy hat posters in earthy vintage palettes, 
Native American eagle prints with the majesty of the great plains, sheriff star prints 
in bold graphic style, and rodeo scenes captured in vivid digital paint. Every piece 
is an original design by Pieter, produced on archival quality materials.""",
        "closing": """Available through Redbubble in framed prints, unframed art prints, canvas, and 
poster formats. Western wall art is appropriate for living rooms, home offices, 
dens, or any space where you want to channel frontier energy and rugged beauty.""",
        "products": ["w11","w16","w18","w14","d11","d13","d20","d21"],
        "breadcrumb_label": "Western Wall Art",
        "related": ["western-home-decor","wall-art-prints","cowboy-art-gifts","native-american-art"],
    },
    {
        "slug": "western-bathroom-decor",
        "section": "themes",
        "title": "Western Bathroom Decor — Wild West Style for Your Bath",
        "h1": "Western Bathroom Decor: Bring Wild West Style to Your Bathroom",
        "meta": "Shop western bathroom decor including unique shower curtains with frontier and vintage designs. Available on Redbubble.",
        "intro": """The bathroom is often the last room to get a design upgrade — but it doesn't have to be. 
These western bathroom decor items bring real character to the most utilitarian space in 
your home. The western era whiskey shower curtain is a bold statement piece that anchors 
the entire room, while complementary western prints and accessories complete the look. 
Frontier style, executed with quality.""",
        "closing": """Available through Redbubble. A shower curtain is one of the easiest ways to dramatically 
transform a bathroom's feel — and with a unique original design, it becomes a talking point 
every time a guest visits. Western bathroom decor is a creative, affordable home upgrade.""",
        "products": ["w08","d04","d11","d20","w18","d07","d08","d13"],
        "breadcrumb_label": "Western Bathroom Decor",
        "related": ["western-home-decor","shower-curtains","western-gifts-for-him","cowboy-art-gifts"],
    },
    {
        "slug": "space-galaxy-art",
        "section": "themes",
        "title": "Space & Galaxy Art — Cosmic Art for Space Lovers",
        "h1": "Space & Galaxy Art: Wear and Display the Wonder of the Cosmos",
        "meta": "Browse space and galaxy art t-shirts and prints. Cosmic, planet, and space designs available on TeePublic.",
        "intro": """The universe is unimaginably vast, filled with galaxies beyond counting and phenomena 
beyond comprehension. These space and galaxy art designs capture that cosmic wonder in 
vivid, wearable form. Planet systems orbit in saturated color fields; star networks 
pulse with electric blue; retro space shuttles pay homage to the golden age of 
exploration; and alien imagery reminds us that we may not be alone.""",
        "closing": """Available through TeePublic in t-shirt, hoodie, and long-sleeve formats. Space art 
makes perfect gifts for astronomers, sci-fi fans, physics students, and anyone who 
finds the night sky endlessly fascinating.""",
        "products": ["a06","a23","a29","a05","a09","a20","a04","a22"],
        "breadcrumb_label": "Space & Galaxy Art",
        "related": ["alien-sci-fi-tees","sci-fi-gifts","cyberpunk-tees","graphic-tees-for-men"],
    },
    {
        "slug": "western-fashion",
        "section": "themes",
        "title": "Western Fashion — Cowboy & Country Style Apparel",
        "h1": "Western Fashion: Authentic Country Style in Modern Printed Apparel",
        "meta": "Discover western fashion including cowboy boot dresses, leggings, bandanas, and graphic tees. Unique western apparel on Redbubble.",
        "intro": """Western fashion has never gone out of style — it's evolved. From the classic cowboy boot 
dress and bandana scarf to the all-over-print western leggings that bring frontier art 
into modern activewear, these designs bridge the gap between authentic western heritage 
and contemporary fashion. Each piece is an original design that brings genuine cowboy 
character to your wardrobe.""",
        "closing": """Available through Redbubble in a range of apparel styles and sizes. Western fashion 
items make wonderful gifts for country music fans, rodeo enthusiasts, western art lovers, 
and anyone with frontier style in their soul.""",
        "products": ["w03","w12","w13","w01","w09","a15","a28","a31"],
        "breadcrumb_label": "Western Fashion",
        "related": ["cowboy-art-gifts","graphic-tees-for-women","western-leggings","western-gifts-for-her"],
    },
    {
        "slug": "western-accessories",
        "section": "themes",
        "title": "Western Accessories — Wild West Art on Everyday Items",
        "h1": "Western Accessories: Carry the Wild West with You Every Day",
        "meta": "Shop western accessories including phone cases, bags, socks, and scarves with original cowboy art. Available on Redbubble.",
        "intro": """The best accessories tell a story. These western accessories take Pieter's original cowboy 
and frontier art and translate it onto the objects you use every single day — your phone 
case, your bag, your socks, your scarf. Each piece is a small but visible declaration 
of western style, printed fresh on demand with fade-resistant inks and dyes.""",
        "closing": """All western accessories are available through Redbubble and make ideal stocking stuffers, 
birthday add-ons, or thoughtful small gifts for the western art enthusiast in your life. 
Affordable prices, international shipping, and genuine original designs set these apart 
from generic western merchandise.""",
        "products": ["w01","w10","w07","w13","w09","w12","d05","a17"],
        "breadcrumb_label": "Western Accessories",
        "related": ["cowboy-art-gifts","western-gifts-for-him","phone-cases-western","drawstring-bags"],
    },

    # ====================== /collections/ ======================
    {
        "slug": "best-western-art",
        "section": "collections",
        "title": "Best Western Art — Curated Top Western Designs",
        "h1": "Best Western Art: A Curated Collection of the Finest Frontier Designs",
        "meta": "Explore the best western art designs by Pieter — curated collection of cowboy, native American, and wild west prints. Shop on Redbubble.",
        "intro": """After browsing hundreds of designs, these are the standout western pieces — the ones that 
combine the most compelling imagery with the strongest visual execution. From the dramatic 
buffalo stampede duvet to the clean-lined sheriff badge wall print, from the richly detailed 
Native American tapestry to the atmospheric cowboy hat poster, this curated collection 
represents western digital art at its very best.""",
        "closing": """All available on Redbubble. Bookmark this collection and return to it when you're 
looking for western art gifts — it will be updated regularly as new designs are added 
to the studio. These are the pieces that western art collectors and home decorators 
come back to most.""",
        "products": ["w11","w15","w05","d02","d11","d13","w16","d20"],
        "breadcrumb_label": "Best Western Art",
        "related": ["western-wall-art","western-home-decor","cowboy-art-gifts","native-american-art"],
    },
    {
        "slug": "top-graphic-tees",
        "section": "collections",
        "title": "Top Graphic T-Shirts — Best Selling Art Tees",
        "h1": "Top Graphic T-Shirts: The Best Selling Art Tees from the Collection",
        "meta": "Browse the top selling graphic t-shirts from Pieter's POD collection. Art tees for men and women available on TeePublic.",
        "intro": """Not all graphic tees are created equal. These top graphic t-shirts rise above the rest 
through bold design choices, careful color work, and imagery that resonates broadly — 
the yin yang mandala that speaks to spiritual seekers, the red alien that delights 
sci-fi fans, the colorful fractal that appeals to anyone who loves vivid art, 
and the chess dragon that captures the imagination of fantasy lovers. These are 
the shirts people come back to buy again and again.""",
        "closing": """Available through TeePublic with a wide range of garment options. These consistently 
popular designs are a safe bet for gifts — they've proven their appeal to real customers 
and continue to resonate with new audiences.""",
        "products": ["a01","a05","a26","a30","a07","a20","a22","a02"],
        "breadcrumb_label": "Top Graphic Tees",
        "related": ["graphic-tees-for-men","colorful-graphic-tees","sci-fi-gifts","dragon-fantasy-art"],
    },
    {
        "slug": "cowboy-prints",
        "section": "collections",
        "title": "Cowboy Prints — Wild West Art Print Collection",
        "h1": "Cowboy Prints: A Complete Wild West Art Print Collection",
        "meta": "Browse the complete cowboy art print collection — posters, wall art, and framed prints with western designs. Available on Redbubble.",
        "intro": """This collection gathers every cowboy-themed print in Pieter's catalog into one curated 
gallery. Cowboy hat posters with sepia-toned vintage character, rodeo action prints 
that capture the dust and speed of the arena, sheriff badge wall prints in bold 
graphic style, and atmospheric western landscape scenes. Each print is available 
in multiple sizes and formats through Redbubble.""",
        "closing": """Perfect for a dedicated gallery wall in a western-themed room, or as individual 
statement pieces in a variety of spaces. Cowboy prints make enduring gifts that 
outlast trends — western art is timeless, and these original designs will look 
as compelling in ten years as they do today.""",
        "products": ["w11","w16","w18","w25","d11","d20","d21","w14"],
        "breadcrumb_label": "Cowboy Prints",
        "related": ["western-wall-art","cowboy-art-gifts","best-western-art","western-home-decor"],
    },
    {
        "slug": "spiritual-collection",
        "section": "collections",
        "title": "Spiritual Art Collection — Sacred Symbol Designs",
        "h1": "Spiritual Art Collection: Sacred Symbols and Meditative Designs",
        "meta": "Explore the spiritual art collection with yin yang, mandala, triquetra, and sacred geometry. Available on TeePublic and Redbubble.",
        "intro": """This curated spiritual collection gathers all the designs that speak to inner life, 
sacred symbolism, and meditative practice. Yin yang in multiple color expressions 
— pink mandala, red circle, yellow ball, triple ball pattern. The triquetra spiral 
bringing Celtic spirituality to modern garments. Mandala geometries radiating 
perfect balance. Each design in this collection invites contemplation and carries 
genuine spiritual resonance.""",
        "closing": """Available across multiple product types through TeePublic and Redbubble. These make 
exceptionally meaningful gifts for people on a spiritual path — yoga teachers, 
meditation practitioners, philosophy students, and anyone who finds depth 
in sacred visual language.""",
        "products": ["a01","a03","a11","a14","a13","a25","a07","d07"],
        "breadcrumb_label": "Spiritual Collection",
        "related": ["spiritual-art-tees","yin-yang-art-shirts","mandala-art-prints","tribal-art-designs"],
    },
    {
        "slug": "sci-fi-collection",
        "section": "collections",
        "title": "Sci-Fi Art Collection — Space, Aliens & Future Tech",
        "h1": "Sci-Fi Art Collection: Space, Aliens, and the Technology of Tomorrow",
        "meta": "Browse the complete sci-fi art collection including alien, space, cyberpunk, and robot designs. Available on TeePublic.",
        "intro": """From the outermost edges of the galaxy to the neon-lit streets of a cyberpunk metropolis, 
this sci-fi art collection covers the full spectrum of speculative design. Alien characters 
rendered in vivid red or green; a planet galaxy captured in swirling cosmic color; 
a cyberpunk robot that belongs in a graphic novel; a retro space shuttle celebrating 
the era of Apollo and beyond. Every design in this collection imagines a universe 
beyond the ordinary.""",
        "closing": """Available through TeePublic in t-shirt, hoodie, and accessory formats. The sci-fi 
collection makes an outstanding gift selection for anyone whose imagination extends 
beyond our own world — which, if you're reading this, probably includes you.""",
        "products": ["a05","a06","a09","a20","a23","a29","a04","a22"],
        "breadcrumb_label": "Sci-Fi Collection",
        "related": ["alien-sci-fi-tees","cyberpunk-tees","space-galaxy-art","sci-fi-gifts"],
    },
    {
        "slug": "abstract-digital-collection",
        "section": "collections",
        "title": "Abstract Digital Art Collection — Modern Art Designs",
        "h1": "Abstract Digital Art Collection: Modern Art for the Digital Age",
        "meta": "Browse the abstract digital art collection with colorful prints, t-shirts, and wall art. Original designs available on Redbubble and TeePublic.",
        "intro": """Digital art has unlocked creative possibilities that no traditional medium can match — 
infinite color precision, perfect geometric construction, and forms that exist only 
in the mathematical domain of the pixel. This abstract digital art collection showcases 
Pieter's most experimental digital work: fractal color explosions, wave art that 
seems to breathe, geometric grids that create optical movement, and pure abstraction 
that resists simple description.""",
        "closing": """Available as wall art prints and t-shirts through Redbubble and TeePublic. 
Whether you're decorating a contemporary interior or expressing your taste in 
avant-garde wearable art, this collection offers designs that stand apart from 
everything in the mainstream market.""",
        "products": ["a26","a27","a22","a21","a07","d07","d09","d14"],
        "breadcrumb_label": "Abstract Digital Collection",
        "related": ["abstract-art-prints","psychedelic-art-shirts","colorful-graphic-tees","wall-art-prints"],
    },
    {
        "slug": "home-office-wall-art",
        "section": "collections",
        "title": "Home Office Wall Art — Art for Your Work Space",
        "h1": "Home Office Wall Art: Inspire Your Work Day with Original Art",
        "meta": "Find home office wall art with motivating western, abstract, and modern designs. Art prints and posters available on Redbubble.",
        "intro": """The environment where you work shapes how you think and create. Home office wall art 
can transform a blank functional space into an inspired creative studio — and the right 
piece of original art can spark ideas, sustain focus, and remind you of what you value. 
The clean boldness of the sheriff badge print; the meditative geometry of abstract 
digital art; the timeless frontier ambition of a cowboy hat poster. Choose the art 
that best represents your working self.""",
        "closing": """Available through Redbubble in sizes suited to any wall — from a small desk-side 
print to a large canvas that anchors the room. All orders come with easy returns 
and worldwide shipping.""",
        "products": ["w18","d09","d17","d11","d14","w11","d07","d20"],
        "breadcrumb_label": "Home Office Wall Art",
        "related": ["wall-art-prints","abstract-art-prints","western-wall-art","home-decor-gifts"],
    },
    {
        "slug": "gift-guide-western-lover",
        "section": "collections",
        "title": "Gift Guide for Western Lovers — Best Western Art Gifts",
        "h1": "Gift Guide for Western Lovers: The Best Art Gifts for Wild West Fans",
        "meta": "Complete gift guide for western lovers — art prints, home decor, apparel, and accessories. Original western designs on Redbubble.",
        "intro": """Put together the perfect gift bundle for the western art enthusiast in your life with 
this comprehensive gift guide. Whether their passion is cowboy wall art, frontier home 
decor, western fashion accessories, or graphic apparel celebrating the Wild West 
aesthetic, this curated guide has something for every budget and every expression 
of western passion. Each item is an original design — not mass-produced western 
kitsch, but genuine digital art.""",
        "closing": """All products available on Redbubble with worldwide shipping. Use this guide as a 
starting point and browse individual product categories for even more options. 
The western art lover in your life will appreciate the thoughtfulness of a gift 
that reflects their genuine passion.""",
        "products": ["w11","w17","d02","d04","w09","w10","d11","w20"],
        "breadcrumb_label": "Gift Guide: Western",
        "related": ["western-gifts-for-him","western-gifts-for-her","cowboy-art-gifts","home-decor-gifts"],
    },

    # ====================== /rooms/ ======================
    {
        "slug": "western-living-room",
        "section": "rooms",
        "title": "Western Living Room Decor — Wild West Art for Living Rooms",
        "h1": "Western Living Room Decor: Make Your Living Room a Frontier Statement",
        "meta": "Discover western living room decor including throw pillows, tapestries, and wall art. Transform your living room with original frontier art. Available on Redbubble.",
        "intro": """The living room is the most public space in your home — the room where you entertain, 
relax, and express your personal taste to every guest. Western living room decor 
transforms that space with frontier character and original art. A tapestry of the 
Native American eagle on one wall, throw pillows with covered wagon designs on 
the sofa, a large floor pillow featuring the buffalo stampede for the corner 
by the fireplace — each element tells part of a cohesive western story.""",
        "closing": """All products available through Redbubble with international shipping. Mix and match 
individual pieces to build a cohesive western living room look — or start with one 
statement piece and let the rest of the room grow around it.""",
        "products": ["w02","w17","d02","d07","d13","w23","d03","w04"],
        "breadcrumb_label": "Western Living Room",
        "related": ["western-home-decor","wall-tapestries","western-throw-pillows","western-wall-art"],
    },
    {
        "slug": "western-bedroom-room",
        "section": "rooms",
        "title": "Western Bedroom Art — Frontier Style for Your Bedroom",
        "h1": "Western Bedroom Art: Sleep Under the Stars of the Frontier",
        "meta": "Shop western bedroom art including duvet covers, wall prints, and accent pillows. Create a frontier bedroom with original western designs on Redbubble.",
        "intro": """A bedroom decorated with western art is a sanctuary that reminds you of open skies, 
rugged beauty, and frontier freedom every morning when you wake. The centerpiece 
is the duvet cover — a full western art print that transforms the bed into 
a statement piece. Pair it with matching throw pillows, a Native American 
dreamcatcher wall print, and a rodeo art poster framed above the headboard 
for a complete western bedroom look.""",
        "closing": """All bedroom art products available through Redbubble. Mix sizes and print formats 
to create visual interest — a large tapestry combined with a smaller framed print 
creates a gallery wall effect that feels curated rather than catalog-standard.""",
        "products": ["w06","w15","d01","w02","d16","w19","d23","d11"],
        "breadcrumb_label": "Western Bedroom",
        "related": ["western-bedroom-decor","duvet-covers","western-home-decor","western-wall-art"],
    },
    {
        "slug": "dorm-room-art",
        "section": "rooms",
        "title": "Dorm Room Art — Bold Tapestries & Prints for Students",
        "h1": "Dorm Room Art: Bold, Affordable Art That Makes Your Space Yours",
        "meta": "Find perfect dorm room art including tapestries, posters, and graphic prints. Affordable original art for student spaces on Redbubble and TeePublic.",
        "intro": """The dorm room is often the first space someone truly makes their own — and the right art 
makes it a home rather than just a room. Tapestries are the perfect dorm room statement: 
they cover a lot of wall space without needing picture hooks, come in vivid original 
designs, and fold down to nothing when it's time to move. Graphic tees hang on walls 
as art. Psychedelic abstract prints spark conversations. These dorm room art picks 
are affordable, original, and genuinely cool.""",
        "closing": """Available through Redbubble and TeePublic at accessible price points. These make 
excellent move-in gifts, care packages, and start-of-semester treats for the student 
who wants their space to reflect who they actually are.""",
        "products": ["d02","d23","a07","a26","a05","d08","w04","a22"],
        "breadcrumb_label": "Dorm Room Art",
        "related": ["wall-tapestries","abstract-art-prints","psychedelic-art-shirts","unique-birthday-gifts"],
    },
    {
        "slug": "kids-western-decor",
        "section": "rooms",
        "title": "Kids Western Room Decor — Cowboy Art for Children's Rooms",
        "h1": "Kids Western Room Decor: Bring the Magic of the Wild West to Children's Spaces",
        "meta": "Shop kids western room decor with cowboy art, native american designs, and dreamcatchers. Printed art for children's rooms on Redbubble.",
        "intro": """Children's imaginations run wild with western stories — cowboys and horses, sheriffs 
and bandits, Native American legends and frontier adventures. These kids' western room 
decor items bring that magic to life in the bedroom or playroom. A dreamcatcher 
print brings peaceful dreams; covered wagon art sparks stories of adventure; 
sheriff badge imagery inspires imaginative play. Real art, at kid-friendly scale.""",
        "closing": """All products available through Redbubble. When selecting for a child's room, consider 
the scale of the space and whether a tapestry, framed print, or pillow best suits 
the room's layout. These also make wonderful baby shower and birthday gifts.""",
        "products": ["w19","w02","w04","d22","w14","w18","d11","w05"],
        "breadcrumb_label": "Kids Western Decor",
        "related": ["western-home-decor","native-american-art","cowboy-art-gifts","home-decor-gifts"],
    },
    {
        "slug": "game-room-art",
        "section": "rooms",
        "title": "Game Room Art — Bold Art for Gaming Spaces",
        "h1": "Game Room Art: Level Up Your Gaming Space with Original Art",
        "meta": "Find game room art with sci-fi, cyberpunk, dragon, and chess designs. Original prints and posters for gaming spaces. Available on TeePublic and Redbubble.",
        "intro": """The game room deserves art as bold as the games you play in it. Cyberpunk robot 
prints that match the neon aesthetic of modern gaming; dragon fantasy art that 
belongs in the world of tabletop RPGs; chess piece posters for the strategist's 
wall; alien sci-fi prints that set the mood for space games. These game room art 
picks are chosen specifically for the gamer, the tabletop player, and the 
fantasy enthusiast who takes their space seriously.""",
        "closing": """Available as framed art prints and posters through Redbubble and TeePublic. 
Game room art works well in multiples — create a gallery wall that mixes 
chess, dragon, and sci-fi themes for a layered, immersive aesthetic 
that makes the space feel like a dedicated creative zone.""",
        "products": ["a20","a05","a02","d05","a30","a29","a22","d09"],
        "breadcrumb_label": "Game Room Art",
        "related": ["sci-fi-collection","dragon-fantasy-art","chess-art-gifts","cyberpunk-tees"],
    },
]

# ===========================================================================
# HELPERS
# ===========================================================================

def slugify(text):
    return text.lower().replace(" ", "-").replace("&", "and").replace("'", "")


def escape_html(text):
    if not text:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def products_by_ids(ids):
    prod_map = {p["id"]: p for p in PRODUCTS}
    return [prod_map[i] for i in ids if i in prod_map]


# ===========================================================================
# PAGE COMPONENTS
# ===========================================================================

GA_SNIPPET = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>"""


def render_head(page, canonical_url, og_image=None):
    og_img = og_image or DEFAULT_OG_IMAGE
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {GA_SNIPPET}
  <title>{escape_html(page['title'])} {SITE_TITLE_SUFFIX}</title>
  <meta name="description" content="{escape_html(page['meta'])}">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph -->
  <meta property="og:title" content="{escape_html(page['title'])}">
  <meta property="og:description" content="{escape_html(page['meta'])}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{og_img}">
  <meta property="og:site_name" content="{SITE_NAME}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape_html(page['title'])}">
  <meta name="twitter:description" content="{escape_html(page['meta'])}">
  <meta name="twitter:image" content="{og_img}">

  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Preconnect fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/pseo.css">
  <link rel="sitemap" type="application/xml" href="/sitemap.xml">
</head>
<body>"""


def render_nav(page, section):
    section_labels = {
        "designs": "Designs",
        "products": "Products",
        "gifts": "Gifts",
        "themes": "Themes",
        "collections": "Collections",
        "rooms": "Rooms",
    }
    items = ""
    for slug_key, label in section_labels.items():
        active = "active" if slug_key == section else ""
        items += f'<a href="/{slug_key}/" class="nav-link {active}">{label}</a>\n'
    return f"""<header class="site-header">
  <nav class="top-nav">
    <a href="/" class="site-logo">
      <span class="logo-text">Pieter's</span><span class="logo-accent"> POD Art</span>
    </a>
    <div class="nav-links">
      {items}
    </div>
    <a href="/" class="nav-store-btn">← Back to Main Site</a>
  </nav>
</header>"""


def render_breadcrumbs(page, section):
    section_label = section.replace("-", " ").title()
    return f"""<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol class="breadcrumb-list" itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/" itemprop="item"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1">
    </li>
    <li class="breadcrumb-sep" aria-hidden="true">›</li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/{section}/" itemprop="item"><span itemprop="name">{section_label}</span></a>
      <meta itemprop="position" content="2">
    </li>
    <li class="breadcrumb-sep" aria-hidden="true">›</li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">{escape_html(page['breadcrumb_label'])}</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>"""


def render_product_card(product):
    badge_class = "badge-rb" if product["store"] == "Redbubble" else "badge-tp"
    store_label = product["store"]
    alt = escape_html(product["title"])
    img_src = product["img"]
    url = product["url"]
    title = escape_html(product["title"])
    return f"""<article class="product-card" itemscope itemtype="https://schema.org/Product">
  <a href="{url}" target="_blank" rel="noopener noreferrer" class="card-img-link">
    <div class="card-img-wrap">
      <img src="{img_src}" alt="{alt}" loading="lazy" itemprop="image">
      <span class="store-badge {badge_class}">{store_label}</span>
    </div>
  </a>
  <div class="card-body">
    <h3 class="card-title" itemprop="name">{title}</h3>
    <p class="card-sub">Available exclusively on {store_label}</p>
    <a href="{url}" target="_blank" rel="noopener noreferrer" class="shop-btn btn-{badge_class}" itemprop="url">
      View on {store_label} →
    </a>
  </div>
</article>"""


def render_related(page, all_pages_map):
    links = []
    for rel_slug in page.get("related", []):
        if rel_slug in all_pages_map:
            rel_page = all_pages_map[rel_slug]
            url = f"/{rel_page['section']}/{rel_slug}/"
            links.append(f'<a href="{url}" class="related-link">{escape_html(rel_page["breadcrumb_label"])}</a>')
    if not links:
        return ""
    return f"""<section class="related-section">
  <h2 class="related-title">Related Searches</h2>
  <div class="related-links">
    {''.join(links)}
  </div>
</section>"""


def render_footer():
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="/" class="footer-logo">Pieter's POD Art</a>
      <p class="footer-tagline">{escape_html(SITE_TAGLINE)}</p>
    </div>
    <div class="footer-stores">
      <a href="{STORE_RB1}" target="_blank" rel="noopener" class="footer-store-link">Redbubble Store 1</a>
      <a href="{STORE_RB2}" target="_blank" rel="noopener" class="footer-store-link">Redbubble Store 2</a>
      <a href="{STORE_TP}" target="_blank" rel="noopener" class="footer-store-link">TeePublic Store</a>
    </div>
    <div class="footer-nav">
      <a href="/designs/">Designs</a>
      <a href="/products/">Products</a>
      <a href="/gifts/">Gifts</a>
      <a href="/themes/">Themes</a>
      <a href="/collections/">Collections</a>
      <a href="/rooms/">Rooms</a>
    </div>
    <p class="footer-copy">&copy; {datetime.now().year} {SITE_NAME}. All original designs by Pieter.</p>
  </div>
</footer>"""


def render_jsonld(page, canonical_url, products):
    items = []
    for idx, p in enumerate(products, 1):
        items.append({
            "@type": "ListItem",
            "position": idx,
            "name": p["title"],
            "url": p["url"],
            "image": f"{SITE_URL}{p['img']}",
        })
    structured = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": page["title"],
                "description": page["meta"],
                "url": canonical_url,
                "publisher": {
                    "@type": "Organization",
                    "name": PUBLISHER_NAME,
                    "logo": {"@type": "ImageObject", "url": PUBLISHER_LOGO},
                },
            },
            {
                "@type": "ItemList",
                "name": page["h1"],
                "url": canonical_url,
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        ],
    }
    return f'<script type="application/ld+json">\n{json.dumps(structured, indent=2, ensure_ascii=False)}\n</script>'


# ===========================================================================
# SECTION INDEX PAGES
# ===========================================================================

def render_section_index(section, section_pages, output_dir):
    section_label = section.replace("-", " ").title()
    cards = ""
    for p in section_pages:
        url = f"/{p['section']}/{p['slug']}/"
        cards += f"""<a href="{url}" class="index-card">
  <span class="index-card-title">{escape_html(p['breadcrumb_label'])}</span>
  <span class="index-card-meta">{escape_html(p['meta'][:90])}…</span>
</a>\n"""

    nav_items = ""
    for s in ["designs","products","gifts","themes","collections","rooms"]:
        active = "active" if s == section else ""
        nav_items += f'<a href="/{s}/" class="nav-link {active}">{s.title()}</a>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {GA_SNIPPET}
  <title>{section_label} — {SITE_NAME}</title>
  <meta name="description" content="Browse all {section_label.lower()} in Pieter's POD Art collection — original print-on-demand designs available on Redbubble and TeePublic.">
  <link rel="canonical" href="{SITE_URL}/{section}/">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/pseo.css">
</head>
<body>
<header class="site-header">
  <nav class="top-nav">
    <a href="/" class="site-logo">
      <span class="logo-text">Pieter's</span><span class="logo-accent"> POD Art</span>
    </a>
    <div class="nav-links">
      {nav_items}
    </div>
    <a href="/" class="nav-store-btn">← Back to Main Site</a>
  </nav>
</header>
<main class="section-index-main">
  <div class="section-index-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol class="breadcrumb-list">
        <li><a href="/">Home</a></li>
        <li class="breadcrumb-sep" aria-hidden="true">›</li>
        <li>{section_label}</li>
      </ol>
    </nav>
    <h1 class="section-index-h1">Browse {section_label}</h1>
    <p class="section-index-sub">Explore {len(section_pages)} curated {section_label.lower()} from Pieter's original print-on-demand art collection.</p>
  </div>
  <div class="index-grid">
    {cards}
  </div>
</main>
{render_footer()}
</body>
</html>"""

    idx_path = os.path.join(output_dir, "index.html")
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [INDEX] /{section}/")


# ===========================================================================
# FULL PAGE RENDERER
# ===========================================================================

def render_page(page, all_pages_map, base_output_dir):
    section = page["section"]
    slug = page["slug"]
    canonical_url = f"{SITE_URL}/{section}/{slug}/"

    products = products_by_ids(page["products"])
    if not products:
        print(f"  [WARN] No products found for {slug}")
        return

    og_image = f"{SITE_URL}{products[0]['img']}" if products else DEFAULT_OG_IMAGE

    product_cards = "\n".join(render_product_card(p) for p in products)

    html = render_head(page, canonical_url, og_image) + "\n"
    html += render_nav(page, section) + "\n"
    html += "<main class=\"pseo-main\">\n"
    html += render_breadcrumbs(page, section) + "\n"

    html += f"""<div class="pseo-container">
  <article class="pseo-article">
    <header class="pseo-header">
      <h1 class="pseo-h1">{escape_html(page['h1'])}</h1>
    </header>
    <div class="pseo-intro">
      <p>{page['intro'].strip().replace(chr(10), '</p><p>')}</p>
    </div>
    <section class="products-section">
      <h2 class="products-title">Shop These Designs</h2>
      <div class="products-grid">
        {product_cards}
      </div>
    </section>
    <div class="pseo-closing">
      <p>{page['closing'].strip().replace(chr(10), '</p><p>')}</p>
    </div>
  </article>
  <aside class="pseo-sidebar">
    <div class="sidebar-stores">
      <h3>Shop the Stores</h3>
      <a href="{STORE_RB1}" target="_blank" rel="noopener" class="store-btn rb-btn">Redbubble Store 1</a>
      <a href="{STORE_RB2}" target="_blank" rel="noopener" class="store-btn rb-btn">Redbubble Store 2</a>
      <a href="{STORE_TP}" target="_blank" rel="noopener" class="store-btn tp-btn">TeePublic Store</a>
    </div>
    <div class="sidebar-sections">
      <h3>Browse</h3>
      <a href="/designs/">Designs</a>
      <a href="/products/">Products</a>
      <a href="/gifts/">Gifts</a>
      <a href="/themes/">Themes</a>
      <a href="/collections/">Collections</a>
      <a href="/rooms/">Rooms</a>
    </div>
  </aside>
</div>
{render_related(page, all_pages_map)}
"""
    html += render_jsonld(page, canonical_url, products) + "\n"
    html += "</main>\n"
    html += render_footer() + "\n"
    html += "</body>\n</html>"

    out_dir = os.path.join(base_output_dir, section, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)

    return canonical_url


# ===========================================================================
# SITEMAP GENERATOR
# ===========================================================================

def generate_sitemap(urls, output_dir):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    # Add the main site URL
    lines.append(f"  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>")
    # Add all section index URLs
    for section in ["designs","products","gifts","themes","collections","rooms"]:
        lines.append(f"  <url><loc>{SITE_URL}/{section}/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    # Add all page URLs
    for url in sorted(urls):
        lines.append(f"  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.7</priority><lastmod>{CURRENT_DATE}</lastmod></url>")
    lines.append("</urlset>")
    sitemap_path = os.path.join(output_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nSitemap written -> {sitemap_path} ({len(urls)} page URLs)")


def generate_robots(output_dir):
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    robots_path = os.path.join(output_dir, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print(f"robots.txt written -> {robots_path}")


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    # We write pages into the 'public' directory so Vite copies them to dist/
    base_output_dir = os.path.join(os.path.dirname(__file__), "public")
    print(f"Output directory: {base_output_dir}")
    print(f"Total pages to generate: {len(PAGES)}\n")

    # Build lookup map
    all_pages_map = {p["slug"]: p for p in PAGES}

    # Group pages by section
    sections = {}
    for page in PAGES:
        sections.setdefault(page["section"], []).append(page)

    generated_urls = []
    page_count = 0

    for section, section_pages in sections.items():
        section_dir = os.path.join(base_output_dir, section)
        os.makedirs(section_dir, exist_ok=True)
        print(f"\n=== Section: /{section}/ ({len(section_pages)} pages) ===")

        # Section index page
        render_section_index(section, section_pages, section_dir)

        # Individual landing pages
        for page in section_pages:
            url = render_page(page, all_pages_map, base_output_dir)
            if url:
                generated_urls.append(url)
                page_count += 1
                print(f"  [OK] /{page['section']}/{page['slug']}/")

    # Sitemap & robots
    generate_sitemap(generated_urls, base_output_dir)
    generate_robots(base_output_dir)

    print(f"\n{'='*60}")
    print(f"[OK] {page_count} landing pages generated")
    print(f"[OK] {len(sections)} section index pages generated")
    print(f"[OK] sitemap.xml -> {SITE_URL}/sitemap.xml")
    print(f"[OK] robots.txt updated")
    print(f"\nNext steps:")
    print(f"  1. python build_pseo.py  <- already done")
    print(f"  2. npm run build")
    print(f"  3. git add -A && git commit -m 'Add pSEO: {page_count} landing pages'")
    print(f"  4. git push")


if __name__ == "__main__":
    main()
