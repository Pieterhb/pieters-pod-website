"""
Programmatic SEO (pSEO) Static Site Generator
Generates 54 high-quality, SEO-optimized landing pages for Pieter's POD Art website.
Each page targets a distinct long-tail keyword and contains unique editorial copy,
real product cards, schema.org JSON-LD, breadcrumbs, and balanced cross-links.

Run: python build_pseo.py
Output: subdirectories under public/ (built & deployed by Vite/Cloudflare Pages)
"""

import os
import json
import shutil
import urllib.parse
from datetime import datetime
from math import ceil

from site_config import (
    SITE_URL, SITE_NAME, SITE_TITLE_SUFFIX, SITE_TAGLINE,
    DEFAULT_DESCRIPTION, GA_ID, PUBLISHER_NAME, PUBLISHER_LOGO,
    DEFAULT_OG_IMAGE, STORE_RB1, STORE_RB2, STORE_TP
)

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# =====================================================
# Search URL builders — link to artist-filtered search
# instead of generic store homepage
# =====================================================
def rb_url(title: str, store: str = "RB2") -> str:
    """Returns Redbubble artist shop search URL for a given product title."""
    q = urllib.parse.quote(title)
    if store == "RB1":
        return f"{STORE_RB1}shop?query={q}"
    return f"{STORE_RB2}shop?query={q}"

def tp_url(title: str) -> str:
    """Returns TeePublic artist profile search URL for a given product title."""
    q = urllib.parse.quote(title)
    return f"{STORE_TP}?query={q}"

RB = STORE_RB2  # backward compatibility alias

# ===========================================================================
# PRODUCT DATA
# ===========================================================================
PRODUCTS = [   {   'id': 'w01',
        'img': '/images/scraped_image_001.png',
        'store': 'Redbubble',
        'tags': ['western', 'cowboy', 'sheriff', 'socks', 'accessories', 'gifts'],
        'title': 'Sheriff Badge Socks',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Sheriff%20Badge%20Socks'},
    {   'id': 'w02',
        'img': '/images/scraped_image_005.png',
        'store': 'Redbubble',
        'tags': ['western', 'cowboy', 'pillow', 'home-decor', 'wild-west', 'gifts'],
        'title': 'Wild West Covered Wagon Pillow',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Covered%20Wagon%20Pillow'},
    {   'id': 'w03',
        'img': '/images/scraped_image_016.png',
        'store': 'Redbubble',
        'tags': ['western', 'cowboy', 'apparel', 'dress', 'women', 'fashion'],
        'title': 'Wild West Cowboy Boot Dress',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Cowboy%20Boot%20Dress'},
    {   'id': 'w04',
        'img': '/images/scraped_image_018.png',
        'store': 'Redbubble',
        'tags': ['native-american', 'tapestry', 'wall-art', 'home-decor', 'western'],
        'title': 'Indian Tomahawk Tapestry',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Indian%20Tomahawk%20Tapestry'},
    {   'id': 'w05',
        'img': '/images/scraped_image_022.png',
        'store': 'Redbubble',
        'tags': ['western', 'native-american', 'wall-art', 'cowboy', 'gifts'],
        'title': 'Cowboy & Indian Teepee Art',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Cowboy%20Indian%20Teepee%20Art'},
    {   'id': 'w06',
        'img': '/images/scraped_image_004.png',
        'store': 'Redbubble',
        'tags': ['western', 'duvet', 'home-decor', 'bedroom', 'fantasy', 'women'],
        'title': 'Western Lady Duvet Cover',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Lady%20Duvet%20Cover'},
    {   'id': 'w07',
        'img': '/images/scraped_image_046.png',
        'store': 'Redbubble',
        'tags': ['western', 'train', 'bag', 'accessories', 'travel', 'gifts'],
        'title': 'Steam Train Drawstring Bag',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Steam%20Train%20Drawstring%20Bag'},
    {   'id': 'w08',
        'img': '/images/scraped_image_065.png',
        'store': 'Redbubble',
        'tags': ['western', 'shower-curtain', 'bathroom', 'home-decor', 'vintage'],
        'title': 'Western Era Whiskey Shower Curtain',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Era%20Whiskey%20Shower%20Curtain'},
    {   'id': 'w09',
        'img': '/images/scraped_image_042.png',
        'store': 'Redbubble',
        'tags': ['western', 'sheriff', 't-shirt', 'apparel', 'men', 'cowboy'],
        'title': 'Wild West Sheriff Badge T-Shirt',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Sheriff%20Badge%20T-Shirt'},
    {   'id': 'w10',
        'img': '/images/scraped_image_043.png',
        'store': 'Redbubble',
        'tags': ['western', 'phone-case', 'cowboy', 'horse', 'accessories', 'gifts'],
        'title': 'Western Horse Rider Phone Case',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Horse%20Rider%20Phone%20Case'},
    {   'id': 'w11',
        'img': '/images/scraped_image_068.png',
        'store': 'Redbubble',
        'tags': ['western', 'wall-art', 'cowboy', 'print', 'home-decor', 'vintage'],
        'title': 'Cowboy Hat Art Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Cowboy%20Hat%20Art%20Print'},
    {   'id': 'w12',
        'img': '/images/scraped_image_035.png',
        'store': 'Redbubble',
        'tags': ['western', 'leggings', 'apparel', 'women', 'cowboy', 'fashion'],
        'title': 'Wild West Boot Leggings',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Boot%20Leggings'},
    {   'id': 'w13',
        'img': '/images/scraped_image_032.png',
        'store': 'Redbubble',
        'tags': ['western', 'bandana', 'scarf', 'accessories', 'cowboy', 'fashion'],
        'title': 'Western Bandana Scarf',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Bandana%20Scarf'},
    {   'id': 'w14',
        'img': '/images/scraped_image_053.png',
        'store': 'Redbubble',
        'tags': ['native-american', 'eagle', 'wall-art', 'print', 'home-decor'],
        'title': 'Native American Eagle Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Native%20American%20Eagle%20Print'},
    {   'id': 'w15',
        'img': '/images/scraped_image_060.png',
        'store': 'Redbubble',
        'tags': ['western', 'duvet', 'bedroom', 'home-decor', 'buffalo', 'wild-west'],
        'title': 'Wild West Stampede Duvet',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Stampede%20Duvet'},
    {   'id': 'w16',
        'img': '/images/scraped_image_026.png',
        'store': 'Redbubble',
        'tags': ['western', 'rodeo', 'wall-art', 'cowboy', 'print', 'gifts'],
        'title': 'Cowboy Rodeo Art Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Cowboy%20Rodeo%20Art%20Print'},
    {   'id': 'w17',
        'img': '/images/scraped_image_041.png',
        'store': 'Redbubble',
        'tags': ['western', 'pillow', 'home-decor', 'ranch', 'cowboy', 'gifts'],
        'title': 'Western Ranch Throw Pillow',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Ranch%20Throw%20Pillow'},
    {   'id': 'w18',
        'img': '/images/scraped_image_027.png',
        'store': 'Redbubble',
        'tags': ['western', 'sheriff', 'wall-art', 'print', 'cowboy', 'home-decor'],
        'title': 'Sheriff Badge Wall Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Sheriff%20Badge%20Wall%20Print'},
    {   'id': 'w19',
        'img': '/images/scraped_image_031.png',
        'store': 'Redbubble',
        'tags': ['native-american', 'dreamcatcher', 'wall-art', 'gifts', 'home-decor'],
        'title': 'Native American Dreamcatcher',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Native%20American%20Dreamcatcher'},
    {   'id': 'w20',
        'img': '/images/scraped_image_064.png',
        'store': 'Redbubble',
        'tags': ['western', 'blanket', 'home-decor', 'cowboy', 'gifts', 'cozy'],
        'title': 'Wild West Throw Blanket',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Throw%20Blanket'},
    {   'id': 'w21',
        'img': '/images/scraped_image_038.png',
        'store': 'Redbubble',
        'tags': ['western', 'boot', 'wall-art', 'home-decor', 'cowboy', 'country'],
        'title': 'Western Boot Wall Decor',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Boot%20Wall%20Decor'},
    {   'id': 'w22',
        'img': '/images/scraped_image_041.png',
        'store': 'Redbubble',
        'tags': ['western', 'pillow', 'floor-pillow', 'cowboy', 'home-decor'],
        'title': 'Cowboy Rodeo Floor Pillow',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Cowboy%20Rodeo%20Floor%20Pillow'},
    {   'id': 'w23',
        'img': '/images/scraped_image_022.png',
        'store': 'Redbubble',
        'tags': ['western', 'tapestry', 'wall-art', 'buffalo', 'home-decor'],
        'title': 'Wild West Buffalo Tapestry',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Buffalo%20Tapestry'},
    {   'id': 'w24',
        'img': '/images/scraped_image_051.png',
        'store': 'Redbubble',
        'tags': ['western', 'poster', 'wall-art', 'heritage', 'vintage', 'cowboy'],
        'title': 'Western Heritage Poster',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Heritage%20Poster'},
    {   'id': 'w25',
        'img': '/images/scraped_image_026.png',
        'store': 'Redbubble',
        'tags': ['western', 'wall-art', 'cowboy', 'hanging', 'home-decor', 'gifts'],
        'title': 'Cowboy Legend Wall Hanging',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Cowboy%20Legend%20Wall%20Hanging'},
    {   'id': 'a01',
        'img': '/images/scraped_image_002.png',
        'store': 'TeePublic',
        'tags': ['yin-yang', 'mandala', 't-shirt', 'apparel', 'spiritual', 'men', 'women'],
        'title': 'Yin Yang Pink Mandala T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Yin%20Yang%20Pink%20Mandala'},
    {   'id': 'a02',
        'img': '/images/scraped_image_003.png',
        'store': 'TeePublic',
        'tags': ['chess', 'dragon', 't-shirt', 'apparel', 'fantasy', 'gifts'],
        'title': 'Chess Dragon Crest T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Chess%20Dragon%20Crest'},
    {   'id': 'a03',
        'img': '/images/scraped_image_007.png',
        'store': 'TeePublic',
        'tags': ['yin-yang', 't-shirt', 'apparel', 'spiritual', 'men', 'women', 'gifts'],
        'title': 'Yin Yang Red Circle T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Yin%20Yang%20Red%20Circle'},
    {   'id': 'a04',
        'img': '/images/scraped_image_009.png',
        'store': 'TeePublic',
        'tags': ['sci-fi', 't-shirt', 'apparel', 'retro', 'vintage', 'men', 'gifts'],
        'title': 'Captain Scarlet & Blue T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Captain%20Scarlet%20Blue'},
    {   'id': 'a05',
        'img': '/images/scraped_image_010.png',
        'store': 'TeePublic',
        'tags': ['alien', 'sci-fi', 't-shirt', 'apparel', 'men', 'gifts', 'funny'],
        'title': 'Red Alien T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Red%20Alien'},
    {   'id': 'a06',
        'img': '/images/scraped_image_011.png',
        'store': 'TeePublic',
        'tags': ['space', 'galaxy', 'planet', 't-shirt', 'apparel', 'sci-fi', 'men'],
        'title': 'Space Planet Galaxy T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Space%20Planet%20Galaxy'},
    {   'id': 'a07',
        'img': '/images/scraped_image_013.png',
        'store': 'TeePublic',
        'tags': ['psychedelic', 'swirl', 't-shirt', 'apparel', 'colorful', 'abstract'],
        'title': 'Colorful Swirl Vortex T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Colorful%20Swirl%20Vortex'},
    {   'id': 'a08',
        'img': '/images/scraped_image_019.png',
        'store': 'TeePublic',
        'tags': ['gothic', 'alphabet', 't-shirt', 'apparel', 'dark', 'men', 'unique'],
        'title': 'Gothic Alphabet T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Gothic%20Alphabet'},
    {   'id': 'a09',
        'img': '/images/scraped_image_021.png',
        'store': 'TeePublic',
        'tags': ['alien', 'funny', 't-shirt', 'apparel', 'sci-fi', 'gifts', 'novelty'],
        'title': 'Alien Newbies T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Alien%20Newbies'},
    {   'id': 'a10',
        'img': '/images/scraped_image_074.png',
        'store': 'TeePublic',
        'tags': ['graduation', 'class-of-2020', 't-shirt', 'apparel', 'vintage', 'gifts'],
        'title': 'Class of 2020 Vintage T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Class%20of%202020'},
    {   'id': 'a11',
        'img': '/images/scraped_image_020.png',
        'store': 'TeePublic',
        'tags': ['yin-yang', 't-shirt', 'apparel', 'spiritual', 'colorful', 'men'],
        'title': 'Yin Yang Yellow Ball Pattern',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Yin%20Yang%20Yellow%20Ball'},
    {   'id': 'a12',
        'img': '/images/scraped_image_008.jpg',
        'store': 'TeePublic',
        'tags': ['love', 'heart', 't-shirt', 'apparel', 'romantic', 'women', 'gifts'],
        'title': 'Love Heart Rings T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Love%20Heart%20Rings'},
    {   'id': 'a13',
        'img': '/images/scraped_image_015.jpg',
        'store': 'TeePublic',
        'tags': ['triquetra', 'celtic', 't-shirt', 'apparel', 'spiritual', 'gifts'],
        'title': 'Triquetra Spiral Art T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Triquetra%20Spiral'},
    {   'id': 'a14',
        'img': '/images/scraped_image_030.png',
        'store': 'TeePublic',
        'tags': ['yin-yang', 't-shirt', 'apparel', 'spiritual', 'pattern', 'men'],
        'title': 'Yin Yang Triple Ball T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Yin%20Yang%20Triple%20Ball'},
    {   'id': 'a15',
        'img': '/images/scraped_image_070.png',
        'store': 'TeePublic',
        'tags': ['fashion', 't-shirt', 'apparel', 'women', 'casual', 'blue'],
        'title': 'Sexy Light Blue T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Sexy%20Light%20Blue'},
    {   'id': 'a16',
        'img': '/images/scraped_image_012.jpg',
        'store': 'TeePublic',
        'tags': ['love', 'rainbow', 'heart', 't-shirt', 'apparel', 'pride', 'women'],
        'title': 'Love Rainbow Heart T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Love%20Rainbow%20Heart'},
    {   'id': 'a17',
        'img': '/images/scraped_image_063.png',
        'store': 'TeePublic',
        'tags': ['tennis', 'sports', 't-shirt', 'apparel', 'gifts', 'men', 'women'],
        'title': 'I Love Tennis T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=I%20Love%20Tennis'},
    {   'id': 'a18',
        'img': '/images/scraped_image_044.png',
        'store': 'TeePublic',
        'tags': ['political', 'face-mask', 'accessories', 'novelty', 'gifts'],
        'title': 'Trump 2020 Face Mask',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Trump%202020'},
    {   'id': 'a19',
        'img': '/images/scraped_image_057.png',
        'store': 'TeePublic',
        'tags': ['abstract', 'digital-art', 't-shirt', 'apparel', 'colorful', 'unique'],
        'title': 'Orange Glass Orb Globe T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Orange%20Glass%20Orb'},
    {   'id': 'a20',
        'img': '/images/scraped_image_072.png',
        'store': 'TeePublic',
        'tags': ['cyberpunk', 'robot', 'sci-fi', 't-shirt', 'apparel', 'men', 'tech'],
        'title': 'Cyber Punk Robot T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Cyber%20Punk%20Robot'},
    {   'id': 'a21',
        'img': '/images/scraped_image_036.png',
        'store': 'TeePublic',
        'tags': ['pop-art', 'neon', 't-shirt', 'apparel', 'colorful', 'abstract', 'men'],
        'title': 'Neon Pop Art T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Neon%20Pop%20Art'},
    {   'id': 'a22',
        'img': '/images/scraped_image_037.png',
        'store': 'TeePublic',
        'tags': ['abstract', 'digital-art', 't-shirt', 'apparel', 'colorful', 'unique'],
        'title': 'Abstract Digital Art T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Abstract%20Digital%20Art'},
    {   'id': 'a23',
        'img': '/images/scraped_image_077.png',
        'store': 'TeePublic',
        'tags': ['space', 'retro', 'shuttle', 't-shirt', 'apparel', 'sci-fi', 'men'],
        'title': 'Retro Space Shuttle T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Retro%20Space%20Shuttle'},
    {   'id': 'a24',
        'img': '/images/scraped_image_025.png',
        'store': 'TeePublic',
        'tags': ['birthday', 'vintage', 't-shirt', 'apparel', 'gifts', 'men', 'women'],
        'title': 'Birthday Vintage Year T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Birthday%20Vintage%20Year'},
    {   'id': 'a25',
        'img': '/images/scraped_image_039.jpg',
        'store': 'TeePublic',
        'tags': ['psychedelic', 'circle', 't-shirt', 'apparel', 'colorful', 'abstract'],
        'title': 'Psychedelic Circle T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Psychedelic%20Circle'},
    {   'id': 'a26',
        'img': '/images/scraped_image_055.png',
        'store': 'TeePublic',
        'tags': ['fractal', 'digital-art', 't-shirt', 'apparel', 'colorful', 'abstract'],
        'title': 'Colorful Fractal Art T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Colorful%20Fractal%20Art'},
    {   'id': 'a27',
        'img': '/images/scraped_image_061.png',
        'store': 'TeePublic',
        'tags': ['digital-art', 'wave', 't-shirt', 'apparel', 'abstract', 'colorful'],
        'title': 'Digital Wave Art T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Digital%20Wave%20Art'},
    {   'id': 'a28',
        'img': '/images/scraped_image_067.png',
        'store': 'TeePublic',
        'tags': ['floral', 'bright', 't-shirt', 'apparel', 'women', 'colorful', 'gifts'],
        'title': 'Bright Bloom T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Bright%20Bloom'},
    {   'id': 'a29',
        'img': '/images/scraped_image_045.png',
        'store': 'TeePublic',
        'tags': ['sci-fi', 'star', 'network', 't-shirt', 'apparel', 'abstract', 'men'],
        'title': 'Blue Star Network T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Blue%20Star%20Network'},
    {   'id': 'a30',
        'img': '/images/scraped_image_058.png',
        'store': 'TeePublic',
        'tags': ['dragon', 'fantasy', 't-shirt', 'apparel', 'men', 'gifts', 'art'],
        'title': 'Artistic Dragon T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Artistic%20Dragon'},
    {   'id': 'a31',
        'img': '/images/scraped_image_059.png',
        'store': 'TeePublic',
        'tags': ['tribal', 'pattern', 't-shirt', 'apparel', 'ethnic', 'men', 'women'],
        'title': 'Tribal Pattern T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Tribal%20Pattern'},
    {   'id': 'a32',
        'img': '/images/scraped_image_066.png',
        'store': 'TeePublic',
        'tags': ['geometric', 'abstract', 't-shirt', 'apparel', 'modern', 'men', 'women'],
        'title': 'Geometric Art T-Shirt',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Geometric%20Art'},
    {   'id': 'd01',
        'img': '/images/scraped_image_004.png',
        'store': 'Redbubble',
        'tags': ['western', 'duvet', 'bedroom', 'home-decor', 'fantasy', 'women'],
        'title': 'Western Lady Fantasy Duvet Cover',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Lady%20Fantasy%20Duvet%20Cover'},
    {   'id': 'd02',
        'img': '/images/scraped_image_018.png',
        'store': 'Redbubble',
        'tags': ['native-american', 'tapestry', 'wall-art', 'home-decor', 'western'],
        'title': 'Indian Tomahawk Wall Tapestry',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Indian%20Tomahawk%20Wall%20Tapestry'},
    {   'id': 'd03',
        'img': '/images/scraped_image_005.png',
        'store': 'Redbubble',
        'tags': ['western', 'floor-pillow', 'home-decor', 'cowboy', 'wild-west'],
        'title': 'Wild West Wagon Floor Pillow',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Wagon%20Floor%20Pillow'},
    {   'id': 'd04',
        'img': '/images/scraped_image_065.png',
        'store': 'Redbubble',
        'tags': ['western', 'shower-curtain', 'bathroom', 'home-decor', 'vintage'],
        'title': 'Western Era Shower Curtain',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Era%20Shower%20Curtain'},
    {   'id': 'd05',
        'img': '/images/scraped_image_076.png',
        'store': 'TeePublic',
        'tags': ['chess', 'poster', 'wall-art', 'home-decor', 'gifts', 'games'],
        'title': 'Chess Piece Art Poster',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Chess%20Piece%20Art%20Poster'},
    {   'id': 'd06',
        'img': '/images/scraped_image_057.png',
        'store': 'TeePublic',
        'tags': ['abstract', 'ornament', 'home-decor', 'colorful', 'gifts', 'unique'],
        'title': 'Orange Glass Globe Ornament',
        'url': 'https://www.teepublic.com/user/theblackpanther?query=Orange%20Glass%20Globe%20Ornament'},
    {   'id': 'd07',
        'img': '/images/scraped_image_041.png',
        'store': 'Redbubble',
        'tags': ['spiral', 'wall-art', 'home-decor', 'colorful', 'abstract', 'print'],
        'title': 'Colorful Spiral Wall Art',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Colorful%20Spiral%20Wall%20Art'},
    {   'id': 'd08',
        'img': '/images/scraped_image_078.png',
        'store': 'Redbubble',
        'tags': ['psychedelic', 'print', 'wall-art', 'home-decor', 'colorful', 'abstract'],
        'title': 'Psychedelic Home Decor Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Psychedelic%20Home%20Decor%20Print'},
    {   'id': 'd09',
        'img': '/images/scraped_image_050.png',
        'store': 'Redbubble',
        'tags': ['abstract', 'canvas', 'wall-art', 'home-decor', 'modern', 'print'],
        'title': 'Abstract Art Canvas Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Abstract%20Art%20Canvas%20Print'},
    {   'id': 'd10',
        'img': '/images/scraped_image_064.png',
        'store': 'Redbubble',
        'tags': ['western', 'blanket', 'home-decor', 'cowboy', 'cozy', 'gifts'],
        'title': 'Wild West Throw Blanket',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Wild%20West%20Throw%20Blanket'},
    {   'id': 'd11',
        'img': '/images/scraped_image_068.png',
        'store': 'Redbubble',
        'tags': ['western', 'vintage', 'poster', 'wall-art', 'cowboy', 'home-decor'],
        'title': 'Vintage Western Poster',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Vintage%20Western%20Poster'},
    {   'id': 'd12',
        'img': '/images/scraped_image_041.png',
        'store': 'Redbubble',
        'tags': ['western', 'floor-pillow', 'home-decor', 'ranch', 'cowboy'],
        'title': 'Western Ranch Floor Pillow',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Ranch%20Floor%20Pillow'},
    {   'id': 'd13',
        'img': '/images/scraped_image_022.png',
        'store': 'Redbubble',
        'tags': ['western', 'buffalo', 'wall-art', 'home-decor', 'wild-west', 'print'],
        'title': 'Buffalo Stampede Wall Art',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Buffalo%20Stampede%20Wall%20Art'},
    {   'id': 'd14',
        'img': '/images/scraped_image_079.png',
        'store': 'Redbubble',
        'tags': ['abstract', 'digital-art', 'canvas', 'wall-art', 'home-decor', 'modern'],
        'title': 'Abstract Digital Canvas',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Abstract%20Digital%20Canvas'},
    {   'id': 'd15',
        'img': '/images/scraped_image_053.png',
        'store': 'Redbubble',
        'tags': ['native-american', 'eagle', 'feather', 'print', 'wall-art', 'home-decor'],
        'title': 'Native Eagle Feather Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Native%20Eagle%20Feather%20Print'},
    {   'id': 'd16',
        'img': '/images/scraped_image_060.png',
        'store': 'Redbubble',
        'tags': ['western', 'rodeo', 'duvet', 'bedroom', 'home-decor', 'cowboy'],
        'title': 'Rodeo Art Duvet Cover',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Rodeo%20Art%20Duvet%20Cover'},
    {   'id': 'd17',
        'img': '/images/scraped_image_050.png',
        'store': 'Redbubble',
        'tags': ['geometric', 'wall-art', 'home-decor', 'modern', 'print', 'abstract'],
        'title': 'Geometric Wall Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Geometric%20Wall%20Print'},
    {   'id': 'd18',
        'img': '/images/scraped_image_041.png',
        'store': 'Redbubble',
        'tags': ['spiral', 'poster', 'wall-art', 'colorful', 'abstract', 'home-decor'],
        'title': 'Colorful Spiral Poster',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Colorful%20Spiral%20Poster'},
    {   'id': 'd19',
        'img': '/images/scraped_image_038.png',
        'store': 'Redbubble',
        'tags': ['western', 'boot', 'pillow', 'home-decor', 'cowboy', 'gifts'],
        'title': 'Western Boot Throw Pillow',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Boot%20Throw%20Pillow'},
    {   'id': 'd20',
        'img': '/images/scraped_image_051.png',
        'store': 'Redbubble',
        'tags': ['western', 'poster', 'wall-art', 'classic', 'home-decor', 'vintage'],
        'title': 'Classic Western Art Poster',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Classic%20Western%20Art%20Poster'},
    {   'id': 'd21',
        'img': '/images/scraped_image_026.png',
        'store': 'Redbubble',
        'tags': ['western', 'cowboy', 'rope', 'wall-art', 'print', 'home-decor'],
        'title': 'Cowboy Rope Art Print',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Cowboy%20Rope%20Art%20Print'},
    {   'id': 'd22',
        'img': '/images/scraped_image_031.png',
        'store': 'Redbubble',
        'tags': ['native-american', 'dreamcatcher', 'wall-hanging', 'home-decor', 'gifts'],
        'title': 'Dreamcatcher Wall Hanging',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Dreamcatcher%20Wall%20Hanging'},
    {   'id': 'd23',
        'img': '/images/scraped_image_018.png',
        'store': 'Redbubble',
        'tags': ['western', 'country', 'tapestry', 'wall-art', 'home-decor', 'large'],
        'title': 'Western Country Tapestry',
        'url': 'https://www.redbubble.com/people/Pieterhk/shop?query=Western%20Country%20Tapestry'}]

PAGES = [   {   'breadcrumb_label': 'Cowboy Art Gifts',
        'closing': "Whether you're buying for a Western enthusiast, decorating a ranch-style home, or simply love \n"
                   'the aesthetic of the Wild West, these cowboy art gifts offer something truly unique. Each design '
                   'is printed \n'
                   'on demand, so every order is freshly made just for you — no mass production, no compromises on '
                   'quality.',
        'h1': 'Cowboy Art Gifts: Unique Western Designs for True Fans',
        'intro': "If you're searching for cowboy art gifts that go beyond the generic, you've landed in the right "
                 'place. \n'
                 'These designs celebrate the raw beauty of the American West — dusty trails, rugged horses, vintage '
                 'sheriff badges, \n'
                 'and the timeless spirit of the cowboy. Every piece here is an original design by independent artist '
                 'Pieter, \n'
                 'available as wearables, home decor, accessories, and more through Redbubble and TeePublic.',
        'meta': 'Shop one-of-a-kind cowboy art gifts. From sheriff badge socks to rodeo prints, find the perfect '
                'western gift on Redbubble and TeePublic.',
        'products': ['w01', 'w09', 'w11', 'w16', 'w18', 'w25', 'd11', 'd20'],
        'related': [   'sheriff-badge-gifts',
                       'western-gifts-for-him',
                       'western-home-decor',
                       'cowboy-prints',
                       'phone-cases-western'],
        'section': 'designs',
        'slug': 'cowboy-art-gifts',
        'title': 'Cowboy Art Gifts & Western Designs'},
    {   'breadcrumb_label': 'Sheriff Badge Gifts',
        'closing': 'Perfect as gifts for western fans, law enforcement enthusiasts, or anyone who loves classic \n'
                   'Americana design. The sheriff badge motif translates beautifully onto a wide range of printed '
                   'products — \n'
                   'browse the selection and find the right gift for any occasion.',
        'h1': 'Sheriff Badge Gifts: Bold Western Law & Order Designs',
        'intro': "The sheriff's star has always been a symbol of authority, justice, and the golden era of the "
                 'American \n'
                 'West. These sheriff badge gifts capture that bold, iconic look in wearable and decorative formats. \n'
                 'From socks embroidered with a gleaming star to wall art prints that command attention, each design \n'
                 'brings a piece of frontier history into your everyday life.',
        'meta': 'Discover sheriff badge gifts and western law art. Unique printed gifts including socks, t-shirts, and '
                'wall prints. Shop on Redbubble.',
        'products': ['w01', 'w09', 'w18', 'w16', 'w11', 'w25', 'd11', 'd20'],
        'related': [   'cowboy-art-gifts',
                       'western-gifts-for-him',
                       'western-wall-art',
                       'cowboy-prints',
                       'kids-western-decor'],
        'section': 'designs',
        'slug': 'sheriff-badge-gifts',
        'title': 'Sheriff Badge Gifts & Western Art'},
    {   'breadcrumb_label': 'Yin Yang Art Shirts',
        'closing': 'Available in a wide range of sizes and colors on TeePublic, these shirts make thoughtful gifts \n'
                   'for yoga practitioners, philosophy students, spiritual seekers, or anyone who appreciates the art '
                   'of balance. \n'
                   'Print-on-demand means your shirt is made fresh — no dyes faded by sitting on a shelf for months.',
        'h1': 'Yin Yang Art T-Shirts: Spiritual Balance in Wearable Form',
        'intro': 'The yin yang symbol speaks of duality, balance, and harmony — concepts that resonate across '
                 'cultures \n'
                 'and centuries. These yin yang art t-shirts take that timeless symbol and reimagine it through vivid '
                 'digital \n'
                 'artistry: mandalas, bold color fields, layered circles, and intricate patterns. Each design is a '
                 'meditation \n'
                 'in visual balance, perfect for those drawn to spiritual or philosophical aesthetics.',
        'meta': 'Browse unique yin yang t-shirts with mandala and spiritual designs. Handcrafted digital art printed '
                'on premium quality shirts. Available on TeePublic.',
        'products': ['a01', 'a03', 'a11', 'a14', 'a25', 'a07', 'a26', 'a22'],
        'related': [   'spiritual-art-tees',
                       'mandala-art-prints',
                       'graphic-tees-for-men',
                       'psychedelic-art-shirts',
                       'spiritual-collection'],
        'section': 'designs',
        'slug': 'yin-yang-art-shirts',
        'title': 'Yin Yang T-Shirts & Spiritual Art'},
    {   'breadcrumb_label': 'Alien & Sci-Fi Tees',
        'closing': 'These shirts make the ultimate gift for sci-fi fans, gamers, stargazers, and anyone fascinated '
                   'by \n'
                   'extraterrestrial life. Available through TeePublic in classic tee, long sleeve, and hoodie formats '
                   '— because \n'
                   'space exploration calls for comfortable wear.',
        'h1': 'Alien & Sci-Fi T-Shirts: Out-of-This-World Graphic Designs',
        'intro': 'From wide-eyed alien newbies to red extraterrestrials and cyber punk robots, these alien and '
                 'sci-fi \n'
                 't-shirts celebrate the strange and wonderful universe beyond our own. Each design is crafted with a '
                 'playful \n'
                 'or awe-inspiring visual language — vivid colors, bold line work, and a healthy dose of cosmic '
                 'imagination. \n'
                 'If you believe the universe is bigger than we know, wear it proudly.',
        'meta': 'Shop alien and sci-fi graphic t-shirts with original extraterrestrial and space designs. Available on '
                'TeePublic in multiple styles and sizes.',
        'products': ['a05', 'a09', 'a06', 'a20', 'a23', 'a29', 'a04', 'a08'],
        'related': ['space-galaxy-art', 'graphic-tees-for-men', 'cyberpunk-tees', 'sci-fi-gifts', 'sci-fi-collection'],
        'section': 'designs',
        'slug': 'alien-sci-fi-tees',
        'title': 'Alien & Sci-Fi Graphic T-Shirts'},
    {   'breadcrumb_label': 'Psychedelic Art Shirts',
        'closing': 'Perfect for festival wear, casual everyday style, or as a conversation-starting gift. These \n'
                   'designs are printed on demand through TeePublic using high-quality direct-to-garment printing, '
                   'ensuring \n'
                   'the vivid colors stay true wash after wash.',
        'h1': 'Psychedelic Art T-Shirts: Vivid, Mind-Bending Designs',
        'intro': 'Color that vibrates. Shapes that swirl. Patterns that seem to move when you look at them long '
                 'enough. \n'
                 'These psychedelic art t-shirts are a celebration of digital art at its most expressive — vortices of '
                 'color, \n'
                 'fractal geometries, spiral mandalas, and abstract compositions that defy convention. Wear your inner '
                 'universe \n'
                 'on your sleeve, literally.',
        'meta': 'Explore psychedelic graphic t-shirts with swirling vortex, fractal, and abstract art designs. Unique '
                'prints on TeePublic.',
        'products': ['a07', 'a25', 'a26', 'a22', 'a21', 'a27', 'a19', 'a01'],
        'related': [   'yin-yang-art-shirts',
                       'abstract-art-prints',
                       'colorful-graphic-tees',
                       'spiritual-art-tees',
                       'wall-tapestries'],
        'section': 'designs',
        'slug': 'psychedelic-art-shirts',
        'title': 'Psychedelic Art & Trippy T-Shirts'},
    {   'breadcrumb_label': 'Dragon & Fantasy Art',
        'closing': 'Available as t-shirts, phone cases, posters, and more through TeePublic and Redbubble. These \n'
                   'make exceptional gifts for gamers, tabletop RPG players, fantasy novel readers, and anyone who '
                   'keeps \n'
                   'the magic of imagination alive.',
        'h1': 'Dragon & Fantasy Art: Bold Gifts for Fantasy Enthusiasts',
        'intro': 'Dragons have captured human imagination for millennia — creatures of fire, power, and ancient '
                 'magic. \n'
                 'These dragon and fantasy art designs bring that mythology to life through vivid digital artistry. '
                 'Whether \n'
                 "it's a chess-themed dragon crest or an artistic fire-breathing legend, these designs speak to the "
                 'fantasy \n'
                 'lover in everyone. Combined with western mythos and sci-fi themes, this collection bridges worlds.',
        'meta': 'Discover dragon and fantasy art gifts including t-shirts, prints, and accessories. Original designs '
                'available on TeePublic and Redbubble.',
        'products': ['a02', 'a30', 'a08', 'a29', 'w05', 'd05', 'a20', 'a04'],
        'related': ['alien-sci-fi-tees', 'chess-art-gifts', 'graphic-tees-for-men', 'sci-fi-gifts', 'game-room-art'],
        'section': 'designs',
        'slug': 'dragon-fantasy-art',
        'title': 'Dragon & Fantasy Art Gifts'},
    {   'breadcrumb_label': 'Native American Art',
        'closing': 'These Native American-inspired art gifts are printed on a variety of products through Redbubble '
                   '— \n'
                   'from large-format tapestries and throw pillows to framed wall prints. Each product is printed '
                   'fresh on \n'
                   'your order, using vibrant, long-lasting inks.',
        'h1': 'Native American Art Gifts: Inspired Designs Full of Cultural Beauty',
        'intro': 'With deep reverence for the rich visual heritage of Indigenous American cultures, these designs \n'
                 'draw inspiration from the symbols, patterns, and imagery of the Native American tradition — eagles '
                 'soaring \n'
                 'in painted skies, tomahawks etched with geometric detail, dreamcatchers woven with feathers and '
                 'beads, \n'
                 'and warrior art that speaks of honor and endurance.',
        'meta': 'Explore Native American-inspired art gifts: tapestries, prints, dreamcatchers, and wall art. Original '
                'designs on Redbubble.',
        'products': ['w04', 'w14', 'w19', 'd02', 'd15', 'd22', 'w05', 'd23'],
        'related': [   'cowboy-art-gifts',
                       'western-wall-art',
                       'western-home-decor',
                       'wall-tapestries',
                       'tribal-art-designs'],
        'section': 'designs',
        'slug': 'native-american-art',
        'title': 'Native American Art & Gifts'},
    {   'breadcrumb_label': 'Cyberpunk Tees',
        'closing': 'Available through TeePublic in multiple garment styles and dozens of colorways, these shirts are \n'
                   "as versatile as they are distinctive. Whether you're dressing for a gaming convention, a casual "
                   'Friday, \n'
                   'or a night out, cyberpunk art makes a statement.',
        'h1': 'Cyberpunk T-Shirts: Wear the Future with Bold Tech Art',
        'intro': 'In the neon-soaked alleys of the near future, style is everything. These cyberpunk t-shirts blend \n'
                 'technology, rebellion, and vivid visual design into wearable art. From chrome-plated robots and '
                 'glowing \n'
                 'network grids to pop-art explosions of color, these designs are for those who live at the '
                 'intersection \n'
                 'of tech and creativity.',
        'meta': 'Shop cyberpunk and futuristic art t-shirts with robot, neon, and digital designs. Unique sci-fi '
                'wearables on TeePublic.',
        'products': ['a20', 'a21', 'a22', 'a29', 'a08', 'a27', 'a06', 'a19'],
        'related': [   'alien-sci-fi-tees',
                       'sci-fi-gifts',
                       'retro-vintage-art-tees',
                       'game-room-art',
                       'sci-fi-collection'],
        'section': 'designs',
        'slug': 'cyberpunk-tees',
        'title': 'Cyberpunk T-Shirts & Sci-Fi Art'},
    {   'breadcrumb_label': 'Chess Art Gifts',
        'closing': 'Available as t-shirts and framed prints through TeePublic and Redbubble. Each item is printed \n'
                   'fresh on demand, ensuring crisp, gallery-quality images that the chess lover in your life will '
                   'cherish.',
        'h1': 'Chess Art Gifts: Unique Pieces for the Passionate Chess Player',
        'intro': "Chess is more than a game — it's a battlefield of the mind, a dance of strategy, and an art form \n"
                 'with centuries of history. These chess art gifts translate that intellectual passion into vivid '
                 'visual design. \n'
                 'The dragon crest shirt merges chess with fantasy mythology; the art poster presents chess pieces as '
                 'monumental \n'
                 'sculptures. Perfect gifts for club players, grandmasters in training, or chess lovers of all levels.',
        'meta': 'Find original chess art gifts including t-shirts, posters, and prints for chess enthusiasts. '
                'Available on TeePublic and Redbubble.',
        'products': ['a02', 'd05', 'a30', 'a08', 'd09', 'd14', 'd17', 'd07'],
        'related': ['dragon-fantasy-art', 'graphic-tees-for-men', 'unique-birthday-gifts', 'game-room-art'],
        'section': 'designs',
        'slug': 'chess-art-gifts',
        'title': 'Chess Art Gifts & Graphic Tees'},
    {   'breadcrumb_label': 'Abstract Art Prints',
        'closing': 'All prints are available through Redbubble in multiple formats and sizes — from small framed \n'
                   'prints for a bookshelf to large format canvas art that anchors an entire wall. These abstract '
                   'designs \n'
                   'suit modern, minimalist, and eclectic interiors with equal ease.',
        'h1': 'Abstract Art Prints: Modern Digital Wall Art for Contemporary Spaces',
        'intro': 'Abstract art has the remarkable ability to evoke emotion without depicting anything recognizable — \n'
                 'pure color, form, and movement. These abstract art prints use the latest digital tools to create '
                 'compositions \n'
                 'that feel alive: geometric grids that pulse with hidden energy, spirals that draw the eye inward, \n'
                 'and color explosions that bring warmth or drama to any room.',
        'meta': 'Discover abstract digital art prints for modern interiors. Geometric, spiral, and colorful abstract '
                'designs available on Redbubble.',
        'products': ['d07', 'd08', 'd09', 'd14', 'd17', 'd18', 'w04', 'd02'],
        'related': ['abstract-digital-collection', 'mandala-art-prints', 'wall-art-prints', 'home-office-wall-art'],
        'section': 'designs',
        'slug': 'abstract-art-prints',
        'title': 'Abstract Digital Art Prints'},
    {   'breadcrumb_label': 'Tribal Art Designs',
        'closing': 'Available in multiple shirt colors and styles on TeePublic. Tribal designs carry a timeless '
                   'strength that makes them stand out from standard graphic tees — bold, rhythmic, and unmistakably '
                   'distinct. Perfect for anyone drawn to global art traditions, spiritual iconography, and expressive '
                   'pattern design that elevates daily casual wear.',
        'h1': 'Tribal Art Designs: Bold Ethnic Patterns on Premium Apparel',
        'intro': 'Tribal art has existed as long as humanity itself — patterns that encode identity, story, and \n'
                 'spiritual meaning into bold geometric forms. These tribal art designs translate those ancient '
                 'visual \n'
                 'languages into modern graphic apparel. Bold lines, repeating patterns, and strong geometric '
                 'compositions \n'
                 'make each design visually compelling and culturally resonant.',
        'meta': 'Shop tribal and ethnic pattern t-shirts and art prints. Original digital designs inspired by global '
                'tribal traditions. Available on TeePublic.',
        'products': ['a31', 'a13', 'a32', 'a01', 'a07', 'a14', 'a22', 'a25'],
        'related': ['native-american-art', 'colorful-graphic-tees', 'yin-yang-art-shirts', 'graphic-tees-for-men'],
        'section': 'designs',
        'slug': 'tribal-art-designs',
        'title': 'Tribal Art Shirts & Patterns'},
    {   'breadcrumb_label': 'Spiritual Art Tees',
        'closing': 'Available through TeePublic in a full range of garment types and sizes. These make thoughtful \n'
                   'gifts for yoga teachers, meditation practitioners, spiritual students, and anyone who finds '
                   'beauty \n'
                   'in sacred symbolism.',
        'h1': 'Spiritual Art T-Shirts: Wear Your Sacred Symbols with Pride',
        'intro': 'For those who wear their spiritual journey outwardly, these spiritual art t-shirts offer a \n'
                 'meaningful selection. Yin yang symbols in multiple color interpretations, triquetra Celtic '
                 'spirals, \n'
                 'mandala patterns radiating perfect symmetry, and sacred geometry that speaks to the structure of \n'
                 'the universe — each design is a statement of inner values made visible.',
        'meta': 'Browse spiritual art t-shirts featuring yin yang, triquetra, mandala, and sacred geometry. Available '
                'on TeePublic in multiple styles.',
        'products': ['a01', 'a03', 'a11', 'a13', 'a14', 'a31', 'a07', 'a25'],
        'related': ['yin-yang-art-shirts', 'mandala-art-prints', 'spiritual-collection', 'psychedelic-art-shirts'],
        'section': 'designs',
        'slug': 'spiritual-art-tees',
        'title': 'Spiritual Art & Mandala Tees'},
    {   'breadcrumb_label': 'Retro & Vintage Tees',
        'closing': 'Available through TeePublic, these retro designs make perfect gifts for nostalgia fans, \n'
                   'classic car enthusiasts, vintage lovers, and anyone who appreciates art that references the '
                   'golden \n'
                   'age of graphic design.',
        'h1': 'Retro & Vintage Art T-Shirts: Celebrate the Golden Eras of Design',
        'intro': "There's something enduring about the visual language of bygone eras — the bold typographic \n"
                 'energy of the 1950s, the psychedelic explosion of the 1960s, the space-age optimism of the 1970s. \n'
                 'These retro and vintage art t-shirts capture that nostalgic aesthetic with modern printing '
                 'quality. \n'
                 'Captain Scarlet space age designs, retro shuttle graphics, vintage year typography — each design \n'
                 'is a loving tribute to classic era artistry.',
        'meta': 'Shop retro and vintage art t-shirts with classic 50s, 60s, and 70s inspired designs. Available on '
                'TeePublic.',
        'products': ['a04', 'a10', 'a23', 'a24', 'a08', 'a07', 'w08', 'd11'],
        'related': [   'top-graphic-tees',
                       'graphic-tees-for-men',
                       'sports-hobby-tees',
                       'colorful-graphic-tees',
                       'birthday-gift-tees'],
        'section': 'designs',
        'slug': 'retro-vintage-art-tees',
        'title': 'Retro & Vintage Graphic Tees'},
    {   'breadcrumb_label': 'Colorful Graphic Tees',
        'closing': 'Available through TeePublic in standard tee, fitted, long sleeve, and hoodie styles. The \n'
                   'vibrant colors are achieved through high-quality direct-to-garment printing, maintaining '
                   'brightness \n'
                   'through repeated washes.',
        'h1': 'Colorful Graphic T-Shirts: Bold, Vibrant Designs That Stand Out',
        'intro': 'Life is too short for dull clothes. These colorful graphic t-shirts inject energy and personality \n'
                 'into everyday wardrobes — bold color combinations, vivid digital art, and designs that catch the '
                 'eye \n'
                 'from across the room. From neon pop-art to floral bursts to swirling vortices, each shirt is a '
                 'canvas \n'
                 'of expression that makes a statement without needing a single word.',
        'meta': 'Discover colorful graphic t-shirts with vivid digital art. Abstract, psychedelic, and nature-inspired '
                'designs available on TeePublic.',
        'products': ['a07', 'a21', 'a26', 'a27', 'a28', 'a16', 'a19', 'a22'],
        'related': ['psychedelic-art-shirts', 'top-graphic-tees', 'graphic-tees-for-women', 'tribal-art-designs'],
        'section': 'designs',
        'slug': 'colorful-graphic-tees',
        'title': 'Colorful Graphic Art T-Shirts'},
    {   'breadcrumb_label': 'Sports & Hobby Tees',
        'closing': 'Available through TeePublic in multiple sizes and garment types, these activity shirts make \n'
                   "ideal birthday gifts, holiday gifts, and 'just because' presents. Show the people you love that \n"
                   'you really see who they are.',
        'h1': 'Sports & Hobby T-Shirts: The Perfect Gift for Active People',
        'intro': 'Passion deserves to be worn. These sports and hobby t-shirts let the active people in your life \n'
                 'show off what they love — from a sleek tennis-themed print for the court star in your family to \n'
                 'chess-themed designs for the strategic thinker. Each design is an original digital artwork that \n'
                 'elevates the humble t-shirt into a meaningful personal statement.',
        'meta': 'Find sports and hobby t-shirts including tennis, chess, and activity-themed designs. Unique printed '
                'gifts on TeePublic.',
        'products': ['a17', 'a02', 'd05', 'a10', 'a24', 'a15', 'a12', 'a16'],
        'related': ['retro-vintage-art-tees', 'graphic-tees-for-men', 'unique-birthday-gifts', 'drawstring-bags'],
        'section': 'designs',
        'slug': 'sports-hobby-tees',
        'title': 'Sports & Hobby Graphic Tees'},
    {   'breadcrumb_label': 'Western Throw Pillows',
        'closing': 'Available through Redbubble in multiple sizes, from small accent pillows to large floor \n'
                   'pillows. The covers feature vivid, fade-resistant prints and easy-zip removal for washing. \n'
                   'A perfect addition to any western, ranch, or rustic-themed interior.',
        'h1': 'Western Throw Pillows: Bring the Wild West Into Your Living Room',
        'intro': 'A throw pillow is a small but powerful design statement. These western throw pillows bring \n'
                 'the rugged charm of the American West to your sofa, armchair, or bedroom — wagon trains crossing \n'
                 'dusty plains, sheriff stars gleaming on aged leather, cowboy boots and lassos in rich earthy '
                 'palettes. \n'
                 "Each pillow features a full wraparound print of Pieter's original western digital art.",
        'meta': 'Shop western throw pillows with cowboy, ranch, and wild west designs. Available on Redbubble in '
                'multiple sizes.',
        'products': ['w02', 'w17', 'w22', 'd03', 'd12', 'd19', 'w07', 'w20'],
        'related': [   'western-home-decor',
                       'western-living-room',
                       'western-bedroom-decor',
                       'duvet-covers',
                       'kids-western-decor'],
        'section': 'products',
        'slug': 'western-throw-pillows',
        'title': 'Western Throw Pillows & Decor'},
    {   'breadcrumb_label': 'Graphic Tees for Men',
        'closing': 'Available in standard, fitted, and relaxed cuts across a broad range of sizes. These shirts \n'
                   'are ideal for everyday wear, weekend adventures, or as uniquely personal gifts for men who have \n'
                   'their own distinctive style.',
        'h1': 'Graphic T-Shirts for Men: Bold Designs That Define Your Style',
        'intro': 'The right t-shirt tells the world something about who you are before you say a word. These \n'
                 'graphic t-shirts for men span a wide range of themes — the rugged cool of the cowboy west, \n'
                 'the mind-bending dimension of alien sci-fi, the spiritual depth of yin yang symbolism, \n'
                 'and the bold edge of cyberpunk tech. Each design is an original digital artwork, printed fresh \n'
                 'on premium garments through TeePublic and Redbubble.',
        'meta': 'Browse graphic t-shirts for men with western, sci-fi, abstract, and artistic designs. Unique art '
                'prints available on TeePublic and Redbubble.',
        'products': ['w09', 'a05', 'a20', 'a08', 'a06', 'a02', 'a31', 'a30'],
        'related': ['top-graphic-tees', 'graphic-tees-for-women', 'retro-vintage-art-tees', 'alien-sci-fi-tees'],
        'section': 'products',
        'slug': 'graphic-tees-for-men',
        'title': 'Graphic T-Shirts for Men'},
    {   'breadcrumb_label': 'Graphic Tees for Women',
        'closing': 'Available through TeePublic in fitted, classic, and boyfriend-cut styles across a full size \n'
                   'range. These make wonderful gifts for birthdays, anniversaries, and any occasion when you want \n'
                   'to give something personal and beautifully made.',
        'h1': 'Graphic T-Shirts for Women: Wear Art That Speaks to You',
        'intro': 'Expression has no gender, but these graphic t-shirts for women are designed with a particular \n'
                 'attention to aesthetic beauty — floral bursts of bright bloom, love hearts in rainbow palettes, \n'
                 'yin yang mandalas that balance color and form, and western boot designs that channel frontier \n'
                 'independence. Each shirt offers a distinct visual personality that complements a wide range of \n'
                 'personal styles.',
        'meta': 'Shop graphic t-shirts for women with floral, spiritual, love, and artistic designs. Unique prints '
                'available on TeePublic in multiple sizes.',
        'products': ['a28', 'a12', 'a16', 'a01', 'a03', 'a15', 'a13', 'w03'],
        'related': ['top-graphic-tees', 'graphic-tees-for-men', 'western-fashion', 'colorful-graphic-tees'],
        'section': 'products',
        'slug': 'graphic-tees-for-women',
        'title': 'Graphic T-Shirts for Women'},
    {   'breadcrumb_label': 'Wall Tapestries',
        'closing': 'Available through Redbubble in small, medium, and large sizes. The woven fabric ensures \n'
                   "rich color reproduction and durability. Whether you're styling a bedroom, living room, dorm, \n"
                   'or creative studio, a tapestry makes a bold, artistic statement.',
        'h1': 'Wall Tapestries: Large Format Art That Transforms Any Space',
        'intro': 'Few things transform a space as dramatically as a large wall tapestry. These tapestries feature \n'
                 "Pieter's most striking original designs at their most expansive — Native American tomahawks and \n"
                 'eagle imagery, wild west wagon trains, and abstract art compositions that become the visual anchor \n'
                 'of an entire room. Lightweight and versatile, tapestries can hang from a rod, be draped over \n'
                 'furniture, or laid as a floor covering.',
        'meta': 'Shop large format wall tapestries with western, native American, and abstract art designs. Available '
                'on Redbubble in multiple sizes.',
        'products': ['w04', 'd02', 'd23', 'w23', 'd15', 'd07', 'd14', 'd08'],
        'related': [   'dorm-room-art',
                       'wall-art-prints',
                       'western-home-decor',
                       'psychedelic-art-shirts',
                       'native-american-art'],
        'section': 'products',
        'slug': 'wall-tapestries',
        'title': 'Art Wall Tapestries & Decor'},
    {   'breadcrumb_label': 'Wall Art Prints',
        'closing': 'Available through Redbubble with a satisfaction guarantee. Each print is produced on \n'
                   'archival-quality paper or canvas using high-fidelity inks that resist fading. Transform your \n'
                   "home, office, or studio with art that's as original as you are.",
        'h1': 'Wall Art Prints: Original Designs That Make Your Walls Come Alive',
        'intro': 'Your walls are a canvas waiting to be filled with meaning. These wall art prints offer \n'
                 'original digital designs ranging from vintage western posters and Native American eagle imagery \n'
                 'to vivid abstract art and geometric compositions. Each print is available in multiple sizes and \n'
                 'formats — framed art, unframed prints, canvas — to suit your space and budget.',
        'meta': 'Discover wall art prints with western, abstract, and digital art designs. Framed prints and posters '
                'available on Redbubble.',
        'products': ['w11', 'w16', 'w18', 'd09', 'd11', 'd13', 'd17', 'd20'],
        'related': ['abstract-art-prints', 'western-wall-art', 'home-office-wall-art', 'mandala-art-prints'],
        'section': 'products',
        'slug': 'wall-art-prints',
        'title': 'Original Wall Art Prints'},
    {   'breadcrumb_label': 'Duvet Covers',
        'closing': 'Available through Redbubble in twin, queen, and king sizes. The covers feature a full-print \n'
                   'exterior and a plain white interior, with convenient button closure. Machine washable and made \n'
                   'from soft, breathable fabric.',
        'h1': 'Duvet Covers: Transform Your Bedroom with Original Art',
        'intro': 'Your bedroom should be a sanctuary that reflects your personality — and nothing sets the tone \n'
                 "like a beautifully designed duvet cover. These duvet covers feature Pieter's original art across \n"
                 'the full surface, transforming your bed into a statement piece. Western lady fantasy art, buffalo \n'
                 'stampedes at dawn, and rodeo action under a big sky — each design tells a story as it shelters \n'
                 'you through the night.',
        'meta': 'Shop duvet covers with western, abstract, and rodeo art designs. Unique printed bedding available on '
                'Redbubble in queen and king sizes.',
        'products': ['w06', 'w15', 'd01', 'd16', 'd10', 'd23', 'd02', 'w04'],
        'related': ['western-bedroom-decor', 'western-bedroom-room', 'western-throw-pillows', 'wall-tapestries'],
        'section': 'products',
        'slug': 'duvet-covers',
        'title': 'Art Duvet Covers & Bedding'},
    {   'breadcrumb_label': 'Shower Curtains',
        'closing': 'Available through Redbubble in standard shower curtain dimensions with included rings. \n'
                   'The water-resistant fabric is woven for durability while maintaining beautiful color fidelity. \n'
                   'A uniquely personal home decor upgrade that guests will notice and remember.',
        'h1': 'Unique Shower Curtains: Bring Original Art Into Your Bathroom',
        'intro': "Why should the bathroom miss out on great art? These unique shower curtains bring Pieter's \n"
                 'original designs to one of the most functional objects in your home. The western whiskey bar \n'
                 'scene evokes the saloon era of the frontier; the vintage western designs transform a mundane \n'
                 'bathroom into a space with real character. Full-bleed print coverage means the design wraps \n'
                 'edge to edge for maximum visual impact.',
        'meta': 'Find unique shower curtains with western and vintage art designs. Original printed shower curtains '
                'available on Redbubble.',
        'products': ['w08', 'd04', 'd11', 'd08', 'd07', 'w04', 'd02', 'd13'],
        'related': ['western-bathroom-decor', 'western-home-decor', 'unique-gifts', 'home-decor-gifts'],
        'section': 'products',
        'slug': 'shower-curtains',
        'title': 'Unique Art Shower Curtains'},
    {   'breadcrumb_label': 'Western Phone Cases',
        'closing': 'Available through Redbubble for a wide range of iPhone and Samsung Galaxy models. \n'
                   'Cases are available in soft flexible, tough, and slim formats depending on your protection \n'
                   "preference. A stylish western gift idea that's both practical and personal.",
        'h1': 'Western Phone Cases: Protect Your Phone with Wild West Art',
        'intro': 'Your phone is always with you — so why not give it a design that tells your story? These \n'
                 "western phone cases feature Pieter's original wild west art, from a galloping horse rider in \n"
                 "full motion to the bold geometry of the sheriff's star. Each case offers both protection and \n"
                 'personality in a slim, precise-fit format for popular phone models.',
        'meta': 'Shop western and cowboy phone cases with horse rider, badge, and frontier art designs. Available on '
                'Redbubble.',
        'products': ['w10', 'w01', 'w09', 'w13', 'w11', 'w18', 'd11', 'd05'],
        'related': ['western-accessories', 'cowboy-art-gifts', 'western-gifts-for-him', 'unique-gifts'],
        'section': 'products',
        'slug': 'phone-cases-western',
        'title': 'Western Art Phone Cases'},
    {   'breadcrumb_label': 'Western Leggings',
        'closing': 'Available through Redbubble in multiple sizes with a comfortable high waist. The stretch \n'
                   'fabric is soft against the skin and designed to move with your body. A uniquely western take \n'
                   'on athleisure — equally at home at the ranch or the yoga studio.',
        'h1': 'Western Leggings: Wild West Style Meets Active Comfort',
        'intro': "The frontier spirit meets modern activewear. These western leggings feature Pieter's original \n"
                 'cowboy boot and wild west art wrapped around high-stretch, comfortable fabric — perfect for yoga, \n'
                 'gym sessions, casual weekends, or making a bold fashion statement. The all-over print technique \n'
                 'means every inch of the legging carries the design, creating a cohesive and striking look.',
        'meta': 'Shop western and cowboy leggings with boot and frontier art designs. Comfortable activewear available '
                'on Redbubble.',
        'products': ['w12', 'w03', 'w13', 'a15', 'a28', 'a16', 'a01', 'a31'],
        'related': ['western-fashion', 'western-gifts-for-her', 'western-accessories', 'graphic-tees-for-women'],
        'section': 'products',
        'slug': 'western-leggings',
        'title': 'Western & Cowboy Leggings'},
    {   'breadcrumb_label': 'Art Drawstring Bags',
        'closing': 'Available through Redbubble with adjustable drawstring straps and enough capacity for \n'
                   'your daily essentials. These bags make excellent gifts for students, outdoor adventurers, \n'
                   'and western art enthusiasts who want their accessories to say something.',
        'h1': 'Art Drawstring Bags: Carry Your Style Wherever You Go',
        'intro': 'Practical meets artistic. These art drawstring bags feature original designs on lightweight, \n'
                 'durable fabric — ideal for the gym, school, hiking, or as a stylish daily carry. The steam \n'
                 'train design evokes a romantic era of long-distance travel and frontier adventure, while \n'
                 'other western designs bring cowboy grit to your everyday essentials.',
        'meta': 'Find unique art drawstring bags with western and steam train designs. Lightweight printed bags '
                'available on Redbubble.',
        'products': ['w07', 'w13', 'w10', 'w01', 'd05', 'a17', 'a20', 'w09'],
        'related': ['western-accessories', 'sports-hobby-tees', 'unique-birthday-gifts', 'cowboy-art-gifts'],
        'section': 'products',
        'slug': 'drawstring-bags',
        'title': 'Art Drawstring Backpack Bags'},
    {   'breadcrumb_label': 'Mandala Art Prints',
        'closing': 'Available as wall art prints through Redbubble and as t-shirts through TeePublic. \n'
                   "Whether you're decorating a meditation space, yoga studio, or bedroom, mandala art brings \n"
                   'a sense of peace and intention to any environment.',
        'h1': 'Mandala Art Prints: Sacred Geometry That Radiates Peace',
        'intro': 'The mandala — a sacred circular form found in Hindu, Buddhist, and Indigenous traditions — \n'
                 'represents the universe, wholeness, and the infinite cycle of existence. These mandala art prints \n'
                 'translate the ancient form into modern digital art: yin yang mandalas in vivid pink and gold, \n'
                 'spiral mandalas with layered color depth, and geometric patterns that radiate outward in perfect \n'
                 'symmetry. Each design is a meditative visual experience.',
        'meta': 'Browse mandala and sacred geometry art prints and t-shirts. Digital mandala designs available on '
                'TeePublic and Redbubble.',
        'products': ['a01', 'a11', 'a14', 'a25', 'a07', 'd07', 'd08', 'a26'],
        'related': ['spiritual-collection', 'yin-yang-art-shirts', 'spiritual-art-tees', 'abstract-digital-collection'],
        'section': 'products',
        'slug': 'mandala-art-prints',
        'title': 'Mandala & Sacred Geometry Art'},
    {   'breadcrumb_label': 'Cowboy Gifts for Him',
        'closing': 'Browse the full selection above and find the western gift that matches his personality — \n'
                   "whether he's more sheriff-badge bold or vintage-poster nostalgic. All products ship directly \n"
                   'from Redbubble or TeePublic with worldwide delivery and easy returns.',
        'h1': "Cowboy Gifts for Him: Unique Western Art That He'll Actually Love",
        'intro': 'Finding a gift for the western art lover in your life just got easier. These cowboy gifts \n'
                 'for him celebrate everything that makes the American West iconic — the rugged sheriff with his \n'
                 'gleaming badge, the cowboy astride his horse at dusk, the steam train carving through frontier \n'
                 'country. Each product is an original digital design printed fresh on demand, making it a truly \n'
                 'unique gift that no department store can match.',
        'meta': 'Find the perfect cowboy gifts for him: western art t-shirts, phone cases, pillows, and more. Shop on '
                'Redbubble and TeePublic.',
        'products': ['w01', 'w09', 'w10', 'w07', 'w11', 'w13', 'd11', 'd05'],
        'related': ['western-gifts-for-him', 'cowboy-art-gifts', 'sheriff-badge-gifts', 'gift-guide-western-lover'],
        'section': 'gifts',
        'slug': 'cowboy-gifts-for-him',
        'title': 'Cowboy Gifts for Him'},
    {   'breadcrumb_label': 'Western Gifts for Him',
        'closing': 'These products are available on Redbubble and TeePublic with worldwide shipping. Gift-giving \n'
                   'for the western enthusiast has never been this authentic — and these prices are more affordable \n'
                   "than you'd expect for original art merchandise.",
        'h1': 'Western Gifts for Him: Wild West Art That Makes a Real Impression',
        'intro': "The man who loves the Wild West doesn't want a generic gift — he wants something with authentic \n"
                 'western character. These western gifts for him range from bold cowboy art prints ready to hang on \n'
                 "his workshop wall to sheriff badge accessories he'll use every day, and home decor that transforms \n"
                 'his space into a proper frontier retreat. Every item is an original design by artist Pieter.',
        'meta': 'Browse the best western gifts for men including art prints, home decor, and wearables. Original '
                'designs on Redbubble and TeePublic.',
        'products': ['w09', 'w10', 'w11', 'w16', 'w17', 'w20', 'd11', 'd20'],
        'related': ['cowboy-gifts-for-him', 'western-gifts-for-her', 'gift-guide-western-lover', 'phone-cases-western'],
        'section': 'gifts',
        'slug': 'western-gifts-for-him',
        'title': 'Western Gifts for Him'},
    {   'breadcrumb_label': 'Western Gifts for Her',
        'closing': 'All products available on Redbubble with easy international shipping. These gifts work \n'
                   'beautifully for birthdays, anniversaries, Christmas, or any occasion when you want to give \n'
                   'something personal and artistically meaningful.',
        'h1': "Western Gifts for Her: Beautiful Cowgirl Art She'll Treasure",
        'intro': 'The cowgirl spirit is timeless — independent, fierce, and beautifully creative. These western \n'
                 'gifts for her celebrate that spirit through original digital art: the western lady fantasy '
                 'portrait, \n'
                 'cowboy boot leggings for the active western woman, rustic bedroom duvet covers, and a western era \n'
                 'shower curtain that brings frontier style into her daily routine.',
        'meta': 'Discover western gifts for women including cowgirl art, leggings, and bedroom decor. Unique designs '
                'on Redbubble.',
        'products': ['w06', 'w12', 'w03', 'w13', 'd01', 'd16', 'd04', 'w15'],
        'related': ['western-gifts-for-him', 'western-fashion', 'western-leggings', 'phone-cases-western'],
        'section': 'gifts',
        'slug': 'western-gifts-for-her',
        'title': 'Western Gifts for Her'},
    {   'breadcrumb_label': 'Unique Birthday Gifts',
        'closing': 'Every product here is available through TeePublic and Redbubble and ships worldwide. \n'
                   'Print-on-demand means each gift is made fresh, ensuring the highest quality for a moment \n'
                   'that deserves the best.',
        'h1': "Unique Birthday Gifts: Original Art Presents They'll Never Forget",
        'intro': 'The best birthday gift is one that shows you really know the person — something personal, \n'
                 'original, and unexpectedly beautiful. These unique birthday gifts span a wide range of themes: \n'
                 'the vintage year birthday t-shirt captures a specific graduation or birth year in bold typography; \n'
                 'western art prints hang permanently as a reminder of a meaningful occasion; and graphic tees \n'
                 'celebrate specific interests that say "I really see who you are.".',
        'meta': 'Find unique birthday gifts including vintage year t-shirts, art prints, and western decor. '
                'One-of-a-kind presents on TeePublic and Redbubble.',
        'products': ['a24', 'a10', 'a17', 'a02', 'w09', 'd11', 'd05', 'a30'],
        'related': ['birthday-gift-tees', 'unique-gifts', 'sports-hobby-tees', 'chess-art-gifts'],
        'section': 'gifts',
        'slug': 'unique-birthday-gifts',
        'title': 'Unique Birthday Art Gifts'},
    {   'breadcrumb_label': 'Unique Art Gifts',
        'closing': "Browse through the full collection and find a gift that truly reflects the recipient's \n"
                   'personality. All products are available through Redbubble and TeePublic with satisfaction \n'
                   'guarantees and international shipping.',
        'h1': 'Unique Art Gifts: Original Print-on-Demand Designs for Every Occasion',
        'intro': 'Gift giving is an art form — and these unique art gifts are crafted to make the act of \n'
                 'giving as meaningful as the gift itself. Each product is an original design by independent \n'
                 'artist Pieter, produced on demand to guarantee freshness and quality. From western cowboy \n'
                 "art to alien sci-fi, spiritual mandalas to psychedelic abstracts, there's a design here \n"
                 'for every personality and interest.',
        'meta': 'Browse unique art gifts for any occasion. Original western, sci-fi, and abstract designs available on '
                'Redbubble and TeePublic.',
        'products': ['w09', 'a01', 'a05', 'd11', 'a17', 'w10', 'd05', 'a30'],
        'related': [   'unique-birthday-gifts',
                       'home-decor-gifts',
                       'sci-fi-gifts',
                       'shower-curtains',
                       'birthday-gift-tees'],
        'section': 'gifts',
        'slug': 'unique-gifts',
        'title': 'Unique Print on Demand Gifts'},
    {   'breadcrumb_label': 'Sci-Fi Gifts',
        'closing': 'All available through TeePublic with a broad selection of garment styles and sizes. \n'
                   'These make exceptional gifts for star wars fans, space lovers, gamers, and anyone who \n'
                   'finds the future more interesting than the present.',
        'h1': 'Sci-Fi Gifts: Space, Aliens & the Future in Wearable Art',
        'intro': "For the person who looks up at the night sky and wonders what's out there — these sci-fi \n"
                 'gifts bring the cosmos down to earth in wearable and displayable form. Alien characters with \n'
                 'their own strange charm, space planet prints that capture the scale of the universe, \n'
                 'cyberpunk robots that live in the electric city of the future, retro space shuttles \n'
                 'celebrating the golden age of exploration.',
        'meta': 'Find sci-fi gifts including alien t-shirts, space art, and cyberpunk designs. Original art available '
                'on TeePublic.',
        'products': ['a05', 'a09', 'a20', 'a06', 'a23', 'a29', 'a04', 'a22'],
        'related': [   'alien-sci-fi-tees',
                       'cyberpunk-tees',
                       'space-galaxy-art',
                       'sci-fi-collection',
                       'dragon-fantasy-art'],
        'section': 'gifts',
        'slug': 'sci-fi-gifts',
        'title': 'Sci-Fi & Space Art Gifts'},
    {   'breadcrumb_label': 'Birthday Gift Tees',
        'closing': 'Available through TeePublic in standard and fitted styles across a full size range. \n'
                   'These can be ordered last-minute since TeePublic ships quickly — and every shirt is \n'
                   'printed fresh to order to ensure maximum print quality.',
        'h1': 'Birthday Gift T-Shirts: Celebrate Their Year with Original Art',
        'intro': "A birthday t-shirt isn't just a shirt — it's a time capsule. The vintage year design \n"
                 'celebrates the year they were born or graduated in bold, nostalgic typography. The \n'
                 'Class of 2020 shirt captures a uniquely challenging graduation year with genuine historical \n'
                 'weight. These birthday gift t-shirts go beyond the generic to offer something genuinely \n'
                 'meaningful that the recipient will actually wear.',
        'meta': 'Shop birthday gift t-shirts with vintage year and graduation designs. Perfect personalized art gifts '
                'available on TeePublic.',
        'products': ['a24', 'a10', 'a17', 'a15', 'a12', 'a16', 'a28', 'a01'],
        'related': ['unique-birthday-gifts', 'retro-vintage-art-tees', 'graphic-tees-for-men', 'unique-gifts'],
        'section': 'gifts',
        'slug': 'birthday-gift-tees',
        'title': 'Birthday Gift Graphic Tees'},
    {   'breadcrumb_label': 'Home Decor Gifts',
        'closing': 'All products ship from Redbubble with satisfaction guarantee. Each piece is printed \n'
                   'fresh on demand, ensuring the quality that a meaningful home decor gift deserves. \n'
                   "Choose by room, by style, or by the personality of the person you're gifting.",
        'h1': 'Home Decor Gifts: Original Art for Every Room in the House',
        'intro': "When you give someone art for their home, you're giving them something they'll live with \n"
                 'and love for years. These home decor gifts cover every room — large tapestries for living \n'
                 'room walls, duvet covers that transform the bedroom, throw pillows that add western character \n'
                 'to a sofa, shower curtains that make the bathroom worth noticing, and art prints that bring \n'
                 'life to a blank wall.',
        'meta': 'Find home decor gifts including art prints, tapestries, pillows, and duvet covers. Unique printed '
                'gifts on Redbubble.',
        'products': ['d02', 'd09', 'w17', 'd01', 'd04', 'd10', 'd13', 'd07'],
        'related': [   'western-home-decor',
                       'western-throw-pillows',
                       'wall-art-prints',
                       'western-bathroom-decor',
                       'shower-curtains'],
        'section': 'gifts',
        'slug': 'home-decor-gifts',
        'title': 'Home Decor Art Gifts'},
    {   'breadcrumb_label': 'Western Home Decor',
        'closing': 'All western home decor items are available through Redbubble with worldwide shipping. \n'
                   "Whether you're decorating a room from scratch or adding western character to an existing \n"
                   'space, these original art pieces offer the perfect finishing touch.',
        'h1': 'Western Home Decor: Transform Your Space with Wild West Art',
        'intro': 'The American West has an interior design aesthetic all its own — warm earth tones, \n'
                 'rugged materials, and imagery that celebrates freedom, open skies, and frontier spirit. \n'
                 'These western home decor items bring that aesthetic into any home, from a ranch house \n'
                 'in Texas to an apartment in a modern city. Original digital art printed on quality \n'
                 'home goods creates an authentic western atmosphere wherever you place it.',
        'meta': 'Discover western home decor including throw pillows, tapestries, duvet covers, and wall art. Original '
                'designs available on Redbubble.',
        'products': ['w02', 'w17', 'd02', 'd03', 'd04', 'd11', 'd13', 'w20'],
        'related': [   'western-living-room',
                       'western-bedroom-decor',
                       'western-wall-art',
                       'kids-western-decor',
                       'western-bathroom-decor'],
        'section': 'themes',
        'slug': 'western-home-decor',
        'title': 'Western Home Decor & Art'},
    {   'breadcrumb_label': 'Western Bedroom Decor',
        'closing': 'All products available through Redbubble. Western bedroom decor makes an especially \n'
                   'meaningful gift for someone moving into a new home, redecorating their bedroom, or \n'
                   'celebrating a milestone. Pair a duvet with matching pillows for a complete western look.',
        'h1': 'Western Bedroom Decor: Create a Frontier Retreat in Your Bedroom',
        'intro': 'The bedroom is where your day begins and ends — and western bedroom decor turns that \n'
                 'space into a frontier retreat full of character and original art. Imagine a duvet cover \n'
                 'featuring the wide-open stampede of a buffalo herd at sunrise, accent pillows with covered \n'
                 'wagon designs, and a tapestry on the wall bringing the spirit of the American West into \n'
                 'your most personal space.',
        'meta': 'Shop western bedroom decor including duvet covers, throw pillows, and wall art. Transform your '
                'bedroom with original western designs on Redbubble.',
        'products': ['w06', 'w15', 'd01', 'd16', 'w02', 'd03', 'd10', 'd23'],
        'related': ['western-bedroom-room', 'duvet-covers', 'western-home-decor', 'western-throw-pillows'],
        'section': 'themes',
        'slug': 'western-bedroom-decor',
        'title': 'Western Bedroom Decor & Art'},
    {   'breadcrumb_label': 'Western Wall Art',
        'closing': 'Available through Redbubble in framed prints, unframed art prints, canvas, and \n'
                   'poster formats. Western wall art is appropriate for living rooms, home offices, \n'
                   'dens, or any space where you want to channel frontier energy and rugged beauty.',
        'h1': 'Western Wall Art: Original Frontier Art for Bold, Distinctive Walls',
        'intro': "The right wall art defines a room's personality — and western wall art makes that \n"
                 'statement with unmistakable confidence. Cowboy hat posters in earthy vintage palettes, \n'
                 'Native American eagle prints with the majesty of the great plains, sheriff star prints \n'
                 'in bold graphic style, and rodeo scenes captured in vivid digital paint. Every piece \n'
                 'is an original design by Pieter, produced on archival quality materials.',
        'meta': 'Browse western wall art prints, posters, and tapestries. Original cowboy and wild west designs for '
                'your walls. Available on Redbubble.',
        'products': ['w11', 'w16', 'w18', 'w14', 'd11', 'd13', 'd20', 'd21'],
        'related': ['western-living-room', 'wall-art-prints', 'cowboy-prints', 'native-american-art'],
        'section': 'themes',
        'slug': 'western-wall-art',
        'title': 'Western Wall Art & Prints'},
    {   'breadcrumb_label': 'Western Bathroom Decor',
        'closing': 'Available through Redbubble. A shower curtain is one of the easiest ways to dramatically \n'
                   "transform a bathroom's feel — and with a unique original design, it becomes a talking point \n"
                   'every time a guest visits. Western bathroom decor is a creative, affordable home upgrade.',
        'h1': 'Western Bathroom Decor: Bring Wild West Style to Your Bathroom',
        'intro': "The bathroom is often the last room to get a design upgrade — but it doesn't have to be. \n"
                 'These western bathroom decor items bring real character to the most utilitarian space in \n'
                 'your home. The western era whiskey shower curtain is a bold statement piece that anchors \n'
                 'the entire room, while complementary western prints and accessories complete the look. \n'
                 'Frontier style, executed with quality.',
        'meta': 'Shop western bathroom decor including unique shower curtains with frontier and vintage designs. '
                'Available on Redbubble.',
        'products': ['w08', 'd04', 'd11', 'd20', 'w18', 'd07', 'd08', 'd13'],
        'related': ['shower-curtains', 'western-home-decor', 'western-accessories', 'home-decor-gifts'],
        'section': 'themes',
        'slug': 'western-bathroom-decor',
        'title': 'Western Bathroom Decor & Art'},
    {   'breadcrumb_label': 'Space & Galaxy Art',
        'closing': 'Available through TeePublic in t-shirt, hoodie, and long-sleeve formats. Space art \n'
                   'makes perfect gifts for astronomers, sci-fi fans, physics students, and anyone who \n'
                   'finds the night sky endlessly fascinating.',
        'h1': 'Space & Galaxy Art: Wear and Display the Wonder of the Cosmos',
        'intro': 'The universe is unimaginably vast, filled with galaxies beyond counting and phenomena \n'
                 'beyond comprehension. These space and galaxy art designs capture that cosmic wonder in \n'
                 'vivid, wearable form. Planet systems orbit in saturated color fields; star networks \n'
                 'pulse with electric blue; retro space shuttles pay homage to the golden age of \n'
                 'exploration; and alien imagery reminds us that we may not be alone.',
        'meta': 'Browse space and galaxy art t-shirts and prints. Cosmic, planet, and space designs available on '
                'TeePublic.',
        'products': ['a06', 'a23', 'a29', 'a05', 'a09', 'a20', 'a04', 'a22'],
        'related': ['alien-sci-fi-tees', 'sci-fi-gifts', 'sci-fi-collection', 'abstract-digital-collection'],
        'section': 'themes',
        'slug': 'space-galaxy-art',
        'title': 'Space & Galaxy Art Prints'},
    {   'breadcrumb_label': 'Western Fashion',
        'closing': 'Available through Redbubble in a range of apparel styles and sizes. Western fashion \n'
                   'items make wonderful gifts for country music fans, rodeo enthusiasts, western art lovers, \n'
                   'and anyone with frontier style in their soul.',
        'h1': 'Western Fashion: Authentic Country Style in Modern Printed Apparel',
        'intro': "Western fashion has never gone out of style — it's evolved. From the classic cowboy boot \n"
                 'dress and bandana scarf to the all-over-print western leggings that bring frontier art \n'
                 'into modern activewear, these designs bridge the gap between authentic western heritage \n'
                 'and contemporary fashion. Each piece is an original design that brings genuine cowboy \n'
                 'character to your wardrobe.',
        'meta': 'Discover western fashion including cowboy boot dresses, leggings, bandanas, and graphic tees. Unique '
                'western apparel on Redbubble.',
        'products': ['w03', 'w12', 'w13', 'w01', 'w09', 'a15', 'a28', 'a31'],
        'related': ['western-leggings', 'western-gifts-for-her', 'graphic-tees-for-women', 'western-accessories'],
        'section': 'themes',
        'slug': 'western-fashion',
        'title': 'Western Fashion & Apparel'},
    {   'breadcrumb_label': 'Western Accessories',
        'closing': 'All western accessories are available through Redbubble and make ideal stocking stuffers, \n'
                   'birthday add-ons, or thoughtful small gifts for the western art enthusiast in your life. \n'
                   'Affordable prices, international shipping, and genuine original designs set these apart \n'
                   'from generic western merchandise.',
        'h1': 'Western Accessories: Carry the Wild West with You Every Day',
        'intro': "The best accessories tell a story. These western accessories take Pieter's original cowboy \n"
                 'and frontier art and translate it onto the objects you use every single day — your phone \n'
                 'case, your bag, your socks, your scarf. Each piece is a small but visible declaration \n'
                 'of western style, printed fresh on demand with fade-resistant inks and dyes.',
        'meta': 'Shop western accessories including phone cases, bags, socks, and scarves with original cowboy art. '
                'Available on Redbubble.',
        'products': ['w01', 'w10', 'w07', 'w13', 'w09', 'w12', 'd05', 'a17'],
        'related': ['phone-cases-western', 'drawstring-bags', 'western-fashion', 'western-gifts-for-him'],
        'section': 'themes',
        'slug': 'western-accessories',
        'title': 'Western Art Accessories'},
    {   'breadcrumb_label': 'Best Western Art',
        'closing': "All available on Redbubble. Bookmark this collection and return to it when you're \n"
                   'looking for western art gifts — it will be updated regularly as new designs are added \n'
                   'to the studio. These are the pieces that western art collectors and home decorators \n'
                   'come back to most.',
        'h1': 'Best Western Art: A Curated Collection of the Finest Frontier Designs',
        'intro': 'After browsing hundreds of designs, these are the standout western pieces — the ones that \n'
                 'combine the most compelling imagery with the strongest visual execution. From the dramatic \n'
                 'buffalo stampede duvet to the clean-lined sheriff badge wall print, from the richly detailed \n'
                 'Native American tapestry to the atmospheric cowboy hat poster, this curated collection \n'
                 'represents western digital art at its very best.',
        'meta': 'Explore the best western art designs by Pieter — curated collection of cowboy, native American, and '
                'wild west prints. Shop on Redbubble.',
        'products': ['w11', 'w15', 'w05', 'd02', 'd11', 'd13', 'w16', 'd20'],
        'related': ['cowboy-prints', 'western-wall-art', 'gift-guide-western-lover', 'western-home-decor'],
        'section': 'collections',
        'slug': 'best-western-art',
        'title': 'Best Western Art Collection'},
    {   'breadcrumb_label': 'Top Graphic Tees',
        'closing': 'Available through TeePublic with a wide range of garment options. These consistently \n'
                   "popular designs are a safe bet for gifts — they've proven their appeal to real customers \n"
                   'and continue to resonate with new audiences.',
        'h1': 'Top Graphic T-Shirts: The Best Selling Art Tees from the Collection',
        'intro': 'Not all graphic tees are created equal. These top graphic t-shirts rise above the rest \n'
                 'through bold design choices, careful color work, and imagery that resonates broadly — \n'
                 'the yin yang mandala that speaks to spiritual seekers, the red alien that delights \n'
                 'sci-fi fans, the colorful fractal that appeals to anyone who loves vivid art, \n'
                 'and the chess dragon that captures the imagination of fantasy lovers. These are \n'
                 'the shirts people come back to buy again and again.',
        'meta': "Browse the top selling graphic t-shirts from Pieter's POD collection. Art tees for men and women "
                'available on TeePublic.',
        'products': ['a01', 'a05', 'a26', 'a30', 'a07', 'a20', 'a22', 'a02'],
        'related': [   'graphic-tees-for-men',
                       'graphic-tees-for-women',
                       'colorful-graphic-tees',
                       'retro-vintage-art-tees'],
        'section': 'collections',
        'slug': 'top-graphic-tees',
        'title': 'Top Graphic Tees Collection'},
    {   'breadcrumb_label': 'Cowboy Prints',
        'closing': 'Perfect for a dedicated gallery wall in a western-themed room, or as individual \n'
                   'statement pieces in a variety of spaces. Cowboy prints make enduring gifts that \n'
                   'outlast trends — western art is timeless, and these original designs will look \n'
                   'as compelling in ten years as they do today.',
        'h1': 'Cowboy Prints: A Complete Wild West Art Print Collection',
        'intro': "This collection gathers every cowboy-themed print in Pieter's catalog into one curated \n"
                 'gallery. Cowboy hat posters with sepia-toned vintage character, rodeo action prints \n'
                 'that capture the dust and speed of the arena, sheriff badge wall prints in bold \n'
                 'graphic style, and atmospheric western landscape scenes. Each print is available \n'
                 'in multiple sizes and formats through Redbubble.',
        'meta': 'Browse the complete cowboy art print collection — posters, wall art, and framed prints with western '
                'designs. Available on Redbubble.',
        'products': ['w11', 'w16', 'w18', 'w25', 'd11', 'd20', 'd21', 'w14'],
        'related': ['best-western-art', 'cowboy-art-gifts', 'western-wall-art', 'western-living-room'],
        'section': 'collections',
        'slug': 'cowboy-prints',
        'title': 'Cowboy Prints & Wall Art'},
    {   'breadcrumb_label': 'Spiritual Collection',
        'closing': 'Available across multiple product types through TeePublic and Redbubble. These make \n'
                   'exceptionally meaningful gifts for people on a spiritual path — yoga teachers, \n'
                   'meditation practitioners, philosophy students, and anyone who finds depth \n'
                   'in sacred visual language.',
        'h1': 'Spiritual Art Collection: Sacred Symbols and Meditative Designs',
        'intro': 'This curated spiritual collection gathers all the designs that speak to inner life, \n'
                 'sacred symbolism, and meditative practice. Yin yang in multiple color expressions \n'
                 '— pink mandala, red circle, yellow ball, triple ball pattern. The triquetra spiral \n'
                 'bringing Celtic spirituality to modern garments. Mandala geometries radiating \n'
                 'perfect balance. Each design in this collection invites contemplation and carries \n'
                 'genuine spiritual resonance.',
        'meta': 'Explore the spiritual art collection with yin yang, mandala, triquetra, and sacred geometry. '
                'Available on TeePublic and Redbubble.',
        'products': ['a01', 'a03', 'a11', 'a14', 'a13', 'a25', 'a07', 'd07'],
        'related': ['spiritual-art-tees', 'yin-yang-art-shirts', 'mandala-art-prints', 'abstract-digital-collection'],
        'section': 'collections',
        'slug': 'spiritual-collection',
        'title': 'Spiritual Art Collection'},
    {   'breadcrumb_label': 'Sci-Fi Collection',
        'closing': 'Available through TeePublic in t-shirt, hoodie, and accessory formats. The sci-fi \n'
                   'collection makes an outstanding gift selection for anyone whose imagination extends \n'
                   "beyond our own world — which, if you're reading this, probably includes you.",
        'h1': 'Sci-Fi Art Collection: Space, Aliens, and the Technology of Tomorrow',
        'intro': 'From the outermost edges of the galaxy to the neon-lit streets of a cyberpunk metropolis, \n'
                 'this sci-fi art collection covers the full spectrum of speculative design. Alien characters \n'
                 'rendered in vivid red or green; a planet galaxy captured in swirling cosmic color; \n'
                 'a cyberpunk robot that belongs in a graphic novel; a retro space shuttle celebrating \n'
                 'the era of Apollo and beyond. Every design in this collection imagines a universe \n'
                 'beyond the ordinary.',
        'meta': 'Browse the complete sci-fi art collection including alien, space, cyberpunk, and robot designs. '
                'Available on TeePublic.',
        'products': ['a05', 'a06', 'a09', 'a20', 'a23', 'a29', 'a04', 'a22'],
        'related': ['alien-sci-fi-tees', 'cyberpunk-tees', 'space-galaxy-art', 'game-room-art', 'dragon-fantasy-art'],
        'section': 'collections',
        'slug': 'sci-fi-collection',
        'title': 'Sci-Fi Art Collection'},
    {   'breadcrumb_label': 'Abstract Digital Collection',
        'closing': 'Available as wall art prints and t-shirts through Redbubble and TeePublic. \n'
                   "Whether you're decorating a contemporary interior or expressing your taste in \n"
                   'avant-garde wearable art, this collection offers designs that stand apart from \n'
                   'everything in the mainstream market.',
        'h1': 'Abstract Digital Art Collection: Modern Art for the Digital Age',
        'intro': 'Digital art has unlocked creative possibilities that no traditional medium can match — \n'
                 'infinite color precision, perfect geometric construction, and forms that exist only \n'
                 'in the mathematical domain of the pixel. This abstract digital art collection showcases \n'
                 "Pieter's most experimental digital work: fractal color explosions, wave art that \n"
                 'seems to breathe, geometric grids that create optical movement, and pure abstraction \n'
                 'that resists simple description.',
        'meta': 'Browse the abstract digital art collection with colorful prints, t-shirts, and wall art. Original '
                'designs available on Redbubble and TeePublic.',
        'products': ['a26', 'a27', 'a22', 'a21', 'a07', 'd07', 'd09', 'd14'],
        'related': ['abstract-art-prints', 'mandala-art-prints', 'spiritual-collection', 'wall-art-prints'],
        'section': 'collections',
        'slug': 'abstract-digital-collection',
        'title': 'Abstract Digital Collection'},
    {   'breadcrumb_label': 'Home Office Wall Art',
        'closing': 'Available through Redbubble in sizes suited to any wall — from a small desk-side \n'
                   'print to a large canvas that anchors the room. All orders come with easy returns \n'
                   'and worldwide shipping.',
        'h1': 'Home Office Wall Art: Inspire Your Work Day with Original Art',
        'intro': 'The environment where you work shapes how you think and create. Home office wall art \n'
                 'can transform a blank functional space into an inspired creative studio — and the right \n'
                 'piece of original art can spark ideas, sustain focus, and remind you of what you value. \n'
                 'The clean boldness of the sheriff badge print; the meditative geometry of abstract \n'
                 'digital art; the timeless frontier ambition of a cowboy hat poster. Choose the art \n'
                 'that best represents your working self.',
        'meta': 'Find home office wall art with motivating western, abstract, and modern designs. Art prints and '
                'posters available on Redbubble.',
        'products': ['w18', 'd09', 'd17', 'd11', 'd14', 'w11', 'd07', 'd20'],
        'related': ['wall-art-prints', 'abstract-art-prints', 'western-wall-art', 'game-room-art'],
        'section': 'collections',
        'slug': 'home-office-wall-art',
        'title': 'Home Office Wall Art Prints'},
    {   'breadcrumb_label': 'Gift Guide: Western',
        'closing': 'All products available on Redbubble with worldwide shipping. Use this guide as a \n'
                   'starting point and browse individual product categories for even more options. \n'
                   'The western art lover in your life will appreciate the thoughtfulness of a gift \n'
                   'that reflects their genuine passion.',
        'h1': 'Gift Guide for Western Lovers: The Best Art Gifts for Wild West Fans',
        'intro': 'Put together the perfect gift bundle for the western art enthusiast in your life with \n'
                 'this comprehensive gift guide. Whether their passion is cowboy wall art, frontier home \n'
                 'decor, western fashion accessories, or graphic apparel celebrating the Wild West \n'
                 'aesthetic, this curated guide has something for every budget and every expression \n'
                 'of western passion. Each item is an original design — not mass-produced western \n'
                 'kitsch, but genuine digital art.',
        'meta': 'Complete gift guide for western lovers — art prints, home decor, apparel, and accessories. Original '
                'western designs on Redbubble.',
        'products': ['w11', 'w17', 'd02', 'd04', 'w09', 'w10', 'd11', 'w20'],
        'related': ['western-gifts-for-him', 'western-gifts-for-her', 'best-western-art', 'cowboy-gifts-for-him'],
        'section': 'collections',
        'slug': 'gift-guide-western-lover',
        'title': 'Western Lover Gift Guide'},
    {   'breadcrumb_label': 'Western Living Room',
        'closing': 'All products available through Redbubble with international shipping. Mix and match \n'
                   'individual pieces to build a cohesive western living room look — or start with one \n'
                   'statement piece and let the rest of the room grow around it.',
        'h1': 'Western Living Room Decor: Make Your Living Room a Frontier Statement',
        'intro': 'The living room is the most public space in your home — the room where you entertain, \n'
                 'relax, and express your personal taste to every guest. Western living room decor \n'
                 'transforms that space with frontier character and original art. A tapestry of the \n'
                 'Native American eagle on one wall, throw pillows with covered wagon designs on \n'
                 'the sofa, a large floor pillow featuring the buffalo stampede for the corner \n'
                 'by the fireplace — each element tells part of a cohesive western story.',
        'meta': 'Discover western living room decor including throw pillows, tapestries, and wall art. Transform your '
                'living room with original frontier art. Available on Redbubble.',
        'products': ['w02', 'w17', 'd02', 'd07', 'd13', 'w23', 'd03', 'w04'],
        'related': [   'western-home-decor',
                       'western-wall-art',
                       'western-throw-pillows',
                       'western-bedroom-room',
                       'cowboy-prints'],
        'section': 'rooms',
        'slug': 'western-living-room',
        'title': 'Western Living Room Decor'},
    {   'breadcrumb_label': 'Western Bedroom',
        'closing': 'All bedroom art products available through Redbubble. Mix sizes and print formats \n'
                   'to create visual interest — a large tapestry combined with a smaller framed print \n'
                   'creates a gallery wall effect that feels curated rather than catalog-standard.',
        'h1': 'Western Bedroom Art: Sleep Under the Stars of the Frontier',
        'intro': 'A bedroom decorated with western art is a sanctuary that reminds you of open skies, \n'
                 'rugged beauty, and frontier freedom every morning when you wake. The centerpiece \n'
                 'is the duvet cover — a full western art print that transforms the bed into \n'
                 'a statement piece. Pair it with matching throw pillows, a Native American \n'
                 'dreamcatcher wall print, and a rodeo art poster framed above the headboard \n'
                 'for a complete western bedroom look.',
        'meta': 'Shop western bedroom art including duvet covers, wall prints, and accent pillows. Create a frontier '
                'bedroom with original western designs on Redbubble.',
        'products': ['w06', 'w15', 'd01', 'w02', 'd16', 'w19', 'd23', 'd11'],
        'related': ['western-bedroom-decor', 'duvet-covers', 'western-living-room', 'western-home-decor'],
        'section': 'rooms',
        'slug': 'western-bedroom-room',
        'title': 'Western Bedroom Art & Decor'},
    {   'breadcrumb_label': 'Dorm Room Art',
        'closing': 'Available through Redbubble and TeePublic at accessible price points. These make \n'
                   'excellent move-in gifts, care packages, and start-of-semester treats for the student \n'
                   'who wants their space to reflect who they actually are.',
        'h1': 'Dorm Room Art: Bold, Affordable Art That Makes Your Space Yours',
        'intro': 'The dorm room is often the first space someone truly makes their own — and the right art \n'
                 'makes it a home rather than just a room. Tapestries are the perfect dorm room statement: \n'
                 'they cover a lot of wall space without needing picture hooks, come in vivid original \n'
                 "designs, and fold down to nothing when it's time to move. Graphic tees hang on walls \n"
                 'as art. Psychedelic abstract prints spark conversations. These dorm room art picks \n'
                 'are affordable, original, and genuinely cool.',
        'meta': 'Find perfect dorm room art including tapestries, posters, and graphic prints. Affordable original art '
                'for student spaces on Redbubble and TeePublic.',
        'products': ['d02', 'd23', 'a07', 'a26', 'a05', 'd08', 'w04', 'a22'],
        'related': ['wall-tapestries', 'game-room-art', 'alien-sci-fi-tees', 'top-graphic-tees'],
        'section': 'rooms',
        'slug': 'dorm-room-art',
        'title': 'Dorm Room Art & Tapestries'},
    {   'breadcrumb_label': 'Kids Western Decor',
        'closing': "All products available through Redbubble. When selecting for a child's room, consider \n"
                   'the scale of the space and whether a tapestry, framed print, or pillow best suits \n'
                   "the room's layout. These also make wonderful baby shower and birthday gifts.",
        'h1': "Kids Western Room Decor: Bring the Magic of the Wild West to Children's Spaces",
        'intro': "Children's imaginations run wild with western stories — cowboys and horses, sheriffs \n"
                 "and bandits, Native American legends and frontier adventures. These kids' western room \n"
                 'decor items bring that magic to life in the bedroom or playroom. A dreamcatcher \n'
                 'print brings peaceful dreams; covered wagon art sparks stories of adventure; \n'
                 'sheriff badge imagery inspires imaginative play. Real art, at kid-friendly scale.',
        'meta': 'Shop kids western room decor with cowboy art, native american designs, and dreamcatchers. Printed art '
                "for children's rooms on Redbubble.",
        'products': ['w19', 'w02', 'w04', 'd22', 'w14', 'w18', 'd11', 'w05'],
        'related': ['cowboy-art-gifts', 'western-home-decor', 'sheriff-badge-gifts', 'drawstring-bags'],
        'section': 'rooms',
        'slug': 'kids-western-decor',
        'title': 'Kids Western Room Decor'},
    {   'breadcrumb_label': 'Game Room Art',
        'closing': 'Available as framed art prints and posters through Redbubble and TeePublic. \n'
                   'Game room art works well in multiples — create a gallery wall that mixes \n'
                   'chess, dragon, and sci-fi themes for a layered, immersive aesthetic \n'
                   'that makes the space feel like a dedicated creative zone.',
        'h1': 'Game Room Art: Level Up Your Gaming Space with Original Art',
        'intro': 'The game room deserves art as bold as the games you play in it. Cyberpunk robot \n'
                 'prints that match the neon aesthetic of modern gaming; dragon fantasy art that \n'
                 "belongs in the world of tabletop RPGs; chess piece posters for the strategist's \n"
                 'wall; alien sci-fi prints that set the mood for space games. These game room art \n'
                 'picks are chosen specifically for the gamer, the tabletop player, and the \n'
                 'fantasy enthusiast who takes their space seriously.',
        'meta': 'Find game room art with sci-fi, cyberpunk, dragon, and chess designs. Original prints and posters for '
                'gaming spaces. Available on TeePublic and Redbubble.',
        'products': ['a20', 'a05', 'a02', 'd05', 'a30', 'a29', 'a22', 'd09'],
        'related': ['sci-fi-collection', 'cyberpunk-tees', 'chess-art-gifts', 'dorm-room-art', 'home-office-wall-art'],
        'section': 'rooms',
        'slug': 'game-room-art',
        'title': 'Game Room Art & Posters'}]

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
    page_title = f"{escape_html(page['title'])} {SITE_TITLE_SUFFIX}"
    meta_desc = escape_html(page['meta'])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {GA_SNIPPET}
  <title>{page_title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph / Facebook -->
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{og_img}">
  <meta property="og:site_name" content="{SITE_NAME}">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{og_img}">

  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Preconnect & Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/pseo.css">
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


def render_breadcrumbs(page, section, canonical_url):
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
      <link itemprop="item" href="{canonical_url}">
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
    return f"""<article class="product-card">
  <a href="{url}" target="_blank" rel="nofollow noopener noreferrer" class="card-img-link">
    <div class="card-img-wrap">
      <img src="{img_src}" alt="{alt}" width="400" height="400" loading="lazy">
      <span class="store-badge {badge_class}">{store_label}</span>
    </div>
  </a>
  <div class="card-body">
    <h3 class="card-title">{title}</h3>
    <p class="card-sub">Available exclusively on {store_label}</p>
    <a href="{url}" target="_blank" rel="nofollow noopener noreferrer" class="shop-btn btn-{badge_class}">
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
      <a href="{STORE_RB1}" target="_blank" rel="nofollow noopener noreferrer" class="footer-store-link">Redbubble Store 1</a>
      <a href="{STORE_RB2}" target="_blank" rel="nofollow noopener noreferrer" class="footer-store-link">Redbubble Store 2</a>
      <a href="{STORE_TP}" target="_blank" rel="nofollow noopener noreferrer" class="footer-store-link">TeePublic Store</a>
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
    section = page["section"]
    section_label = section.replace("-", " ").title()
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
                "@type": "WebSite",
                "@id": f"{SITE_URL}/#website",
                "url": f"{SITE_URL}/",
                "name": SITE_NAME,
                "description": DEFAULT_DESCRIPTION,
                "publisher": {
                    "@id": f"{SITE_URL}/#organization"
                }
            },
            {
                "@type": "Organization",
                "@id": f"{SITE_URL}/#organization",
                "name": PUBLISHER_NAME,
                "url": f"{SITE_URL}/",
                "logo": {
                    "@type": "ImageObject",
                    "url": PUBLISHER_LOGO
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{SITE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": section_label,
                        "item": f"{SITE_URL}/{section}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": page["breadcrumb_label"],
                        "item": canonical_url
                    }
                ]
            },
            {
                "@type": "CollectionPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": f"{page['title']} {SITE_TITLE_SUFFIX}",
                "description": page["meta"],
                "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
                "isPartOf": {"@id": f"{SITE_URL}/#website"},
                "publisher": {"@id": f"{SITE_URL}/#organization"}
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical_url}#itemlist",
                "name": page["h1"],
                "url": canonical_url,
                "numberOfItems": len(items),
                "itemListElement": items
            }
        ]
    }
    return f'<script type="application/ld+json">\n{json.dumps(structured, indent=2, ensure_ascii=False)}\n</script>'


# ===========================================================================
# SECTION INDEX PAGES
# ===========================================================================

def render_section_index(section, section_pages, output_dir):
    section_label = section.replace("-", " ").title()
    canonical_url = f"{SITE_URL}/{section}/"
    page_title = f"{section_label} Collection {SITE_TITLE_SUFFIX}"
    meta_desc = f"Browse all {section_label.lower()} in Pieter's POD Art collection — original print-on-demand designs available on Redbubble and TeePublic."
    og_img = DEFAULT_OG_IMAGE

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

    jsonld_structured = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE_URL}/#website",
                "url": f"{SITE_URL}/",
                "name": SITE_NAME,
                "description": DEFAULT_DESCRIPTION,
                "publisher": {"@id": f"{SITE_URL}/#organization"}
            },
            {
                "@type": "Organization",
                "@id": f"{SITE_URL}/#organization",
                "name": PUBLISHER_NAME,
                "url": f"{SITE_URL}/",
                "logo": {"@type": "ImageObject", "url": PUBLISHER_LOGO}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{SITE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": section_label,
                        "item": canonical_url
                    }
                ]
            },
            {
                "@type": "CollectionPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": page_title,
                "description": meta_desc,
                "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
                "isPartOf": {"@id": f"{SITE_URL}/#website"},
                "publisher": {"@id": f"{SITE_URL}/#organization"}
            }
        ]
    }
    jsonld_script = f'<script type="application/ld+json">\n{json.dumps(jsonld_structured, indent=2, ensure_ascii=False)}\n</script>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {GA_SNIPPET}
  <title>{page_title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph / Facebook -->
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{og_img}">
  <meta property="og:site_name" content="{SITE_NAME}">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{og_img}">

  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Preconnect & Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/pseo.css">
  {jsonld_script}
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
      <ol class="breadcrumb-list" itemscope itemtype="https://schema.org/BreadcrumbList">
        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <a href="/" itemprop="item"><span itemprop="name">Home</span></a>
          <meta itemprop="position" content="1">
        </li>
        <li class="breadcrumb-sep" aria-hidden="true">›</li>
        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <span itemprop="name">{section_label}</span>
          <link itemprop="item" href="{canonical_url}">
          <meta itemprop="position" content="2">
        </li>
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
        return None

    og_image = f"{SITE_URL}{products[0]['img']}" if products else DEFAULT_OG_IMAGE

    product_cards = "\n".join(render_product_card(p) for p in products)

    html = render_head(page, canonical_url, og_image) + "\n"
    html += render_nav(page, section) + "\n"
    html += "<main class=\"pseo-main\">\n"
    html += render_breadcrumbs(page, section, canonical_url) + "\n"

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
      <a href="{STORE_RB1}" target="_blank" rel="nofollow noopener noreferrer" class="store-btn rb-btn">Redbubble Store 1</a>
      <a href="{STORE_RB2}" target="_blank" rel="nofollow noopener noreferrer" class="store-btn rb-btn">Redbubble Store 2</a>
      <a href="{STORE_TP}" target="_blank" rel="nofollow noopener noreferrer" class="store-btn tp-btn">TeePublic Store</a>
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
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    # Add homepage
    lines.append(f"  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{CURRENT_DATE}</lastmod>\n  </url>")
    
    # Add section index URLs
    for section in ["designs","products","gifts","themes","collections","rooms"]:
        lines.append(f"  <url>\n    <loc>{SITE_URL}/{section}/</loc>\n    <lastmod>{CURRENT_DATE}</lastmod>\n  </url>")
        
    # Add all landing page URLs
    for url in sorted(urls):
        lines.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{CURRENT_DATE}</lastmod>\n  </url>")
        
    lines.append("</urlset>\n")
    sitemap_path = os.path.join(output_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nSitemap written -> {sitemap_path} ({len(urls) + 7} total URLs)")


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
    base_output_dir = os.path.join(os.path.dirname(__file__), "public")
    print(f"Output directory: {base_output_dir}")
    print(f"Total pages to generate: {len(PAGES)}\n")

    all_pages_map = {p["slug"]: p for p in PAGES}

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


if __name__ == "__main__":
    main()
