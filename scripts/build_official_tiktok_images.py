import io
import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

def create_cinematic_gradient(width, height):
    """
    Creates a cinematic gradient overlay that keeps the center imagery vivid
    while darkening top and bottom for flawless typography readability.
    """
    base = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    for y in range(height):
        ratio = y / height
        # Top header darkening (0 to 280px)
        if ratio < 0.22:
            alpha = int(170 - (ratio / 0.22) * 90) # from 170 down to 80
        # Center visual showcase (0.22 to 0.52) - keep very visible!
        elif ratio < 0.52:
            alpha = int(80 + ((ratio - 0.22) / 0.30) * 50) # 80 to 130
        # Bottom feature card & CTA (0.52 to 1.0)
        else:
            alpha = int(130 + ((ratio - 0.52) / 0.48) ** 1.2 * 105) # 130 to 235
            
        draw.line([(0, y), (width, y)], fill=(8, 18, 36, min(255, alpha)))
        
    return base

def draw_round_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_vector_check(draw, cx, cy, radius=22, circle_fill=(0, 168, 89)):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=circle_fill)
    # Checkmark lines
    draw.line([(cx - 9, cy), (cx - 2, cy + 8), (cx + 10, cy - 7)], fill=(255, 255, 255), width=4)

def draw_mini_star(draw, cx, cy, size=8, fill=(245, 158, 11)):
    # 4-point diamond star
    points = [(cx, cy - size), (cx + size * 0.4, cy - size * 0.4), (cx + size, cy),
              (cx + size * 0.4, cy + size * 0.4), (cx, cy + size), (cx - size * 0.4, cy + size * 0.4),
              (cx - size, cy), (cx - size * 0.4, cy - size * 0.4)]
    draw.polygon(points, fill=fill)


FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
FONT_FILES = {
    'jakarta': os.path.join(FONT_DIR, 'PlusJakartaSans.ttf'),
    'inter': os.path.join(FONT_DIR, 'Inter.ttf'),
}


def wide(text):
    """Elargit l'espace entre les mots.

    Plus Jakarta Sans a un espace tres etroit (0,17 em) : en capitales et en
    graisse lourde, les mots se collent et deviennent penibles a lire. On
    double l'espace pour revenir a une chasse normale.
    """
    return text.replace(' ', '  ')


def load_font(family, size, weight='Bold'):
    """Charge une graisse precise d'une police variable."""
    font = ImageFont.truetype(FONT_FILES[family], size)
    try:
        font.set_variation_by_name(weight)
    except Exception:
        pass  # graisse absente : on garde le reglage par defaut
    return font


def generate_tiktok_poster(
    bg_path,
    output_path,
    category_badge,
    badge_color,
    main_title,
    subtitle,
    bullets,
    tag_text,
    cta_text,
    cta_color,
    footer_left,
    footer_right,
    theme_accent=(37, 99, 235),
    gradient_stops=None
):
    target_w, target_h = 1080, 1920
    
    # 1. Fond : photo si disponible, sinon degrade thematique.
    # Toutes les affiches partagent ainsi la meme mise en page, qu'une photo
    # existe ou non pour ce visuel.
    if bg_path:
        bg = Image.open(bg_path).convert('RGB')
        bg_w, bg_h = bg.size

        scale = max(target_w / bg_w, target_h / bg_h)
        new_w, new_h = int(bg_w * scale), int(bg_h * scale)
        bg = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)

        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        bg = bg.crop((left, top, left + target_w, top + target_h))
    else:
        stops = gradient_stops or [(10, 25, 47), (14, 42, 77), (30, 58, 138)]
        bg = Image.new('RGB', (target_w, target_h))
        bg_draw = ImageDraw.Draw(bg)
        segments = len(stops) - 1
        for y in range(target_h):
            pos = y / (target_h - 1) * segments
            i = min(int(pos), segments - 1)
            t = pos - i
            c0, c1 = stops[i], stops[i + 1]
            bg_draw.line(
                [(0, y), (target_w, y)],
                fill=tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3))
            )
    
    # 2. Cinematic overlay
    overlay = create_cinematic_gradient(target_w, target_h)
    bg.paste(overlay, (0, 0), overlay)
    
    # 3. Canvas
    canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Fonts
    # Polices de la charte du site (Plus Jakarta Sans pour les titres, Inter
    # pour le texte courant) plutot que la police systeme de Windows : memes
    # fontes que ayegroupe.com, et dessinees pour la lecture a l'ecran.
    f_brand = load_font('jakarta', 46, 'ExtraBold')
    f_baseline = load_font('inter', 23, 'Medium')
    f_badge = load_font('jakarta', 25, 'Bold')
    f_sub = load_font('inter', 34, 'Medium')
    f_card_hdr = load_font('jakarta', 29, 'Bold')
    f_bullet = load_font('inter', 32, 'SemiBold')
    f_tag = load_font('inter', 28, 'Bold')
    f_cta = load_font('jakarta', 40, 'ExtraBold')
    f_footer = load_font('inter', 26, 'SemiBold')
    
    # 4. Top Header & Official Logo
    logo_path = 'public/logo/logo-transparent-white.png'
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        bbox = logo.getbbox()
        if bbox:
            logo = logo.crop(bbox)
        logo_h = 108
        logo_w = int(logo.width * (logo_h / logo.height))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        canvas.paste(logo, (70, 75), logo)
    
    # Brand typography
    draw.text((195, 78), wide("AYEGROUPE"), fill=(255, 255, 255), font=f_brand)
    draw.text((195, 134), "Technologie • Commerce • Logistique", fill=(148, 163, 184), font=f_baseline)
    
    # Top-right category badge pill
    badge_w = 380
    badge_h = 58
    badge_x = target_w - badge_w - 70
    badge_y = 96
    draw_round_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=29, fill=(10, 25, 47, 240), outline=badge_color, width=2)
    
    draw.text((badge_x + badge_w // 2, badge_y + 14), wide(category_badge), fill=badge_color, font=f_badge, anchor="mt")
    
    # Thin divider
    draw.line([(70, 205), (target_w - 70, 205)], fill=(255, 255, 255, 45), width=2)
    
    # 5. Accroche principale, en taille adaptative : une accroche longue doit
    # retrecir plutot que de deborder sur le bloc d'arguments (qui commence a
    # y=660).
    TITLE_TOP, TITLE_LIMIT = 240, 600
    for title_size in range(66, 39, -2):
        f_title = load_font('jakarta', title_size, 'ExtraBold')
        line_h = int(title_size * 1.22)
        lines, curr_line = [], ""
        for w in main_title.split(' '):
            test = (curr_line + " " + w).strip()
            probe = wide(test)
            if (f_title.getbbox(probe)[2] - f_title.getbbox(probe)[0]) > 940 and curr_line:
                lines.append(curr_line)
                curr_line = w
            else:
                curr_line = test
        if curr_line:
            lines.append(curr_line)
        if TITLE_TOP + len(lines) * line_h <= TITLE_LIMIT:
            break

    y_text = TITLE_TOP
    for l in lines:
        draw.text((70, y_text), wide(l), fill=(255, 255, 255), font=f_title)
        y_text += line_h
    
    # Subtitle
    y_text += 8
    draw.text((70, y_text), subtitle, fill=(203, 213, 225), font=f_sub)
    
    # 6. Center Feature Card (positioned so top 3D image remains nicely exposed)
    card_y = 660
    card_h = 750
    card_w = target_w - 140
    card_x = 70
    
    # Glassmorphism container
    draw_round_rect(draw, (card_x, card_y, card_x + card_w, card_y + card_h), radius=36, fill=(10, 25, 47, 230), outline=(255, 255, 255, 50), width=2)
    
    # Card Header
    hdr_y = card_y + 40
    draw_mini_star(draw, card_x + 60, hdr_y + 16, size=12, fill=badge_color)
    draw.text((card_x + 85, hdr_y), wide("CE QUE NOUS VOUS APPORTONS :"), fill=badge_color, font=f_card_hdr)
    
    draw.line([(card_x + 45, hdr_y + 48), (card_x + card_w - 45, hdr_y + 48)], fill=(255, 255, 255, 35), width=1)
    
    # Bullets
    b_y = hdr_y + 80
    for b in bullets:
        # Custom vector checkmark
        draw_vector_check(draw, card_x + 72, b_y + 24, radius=22, circle_fill=(0, 168, 89))
        
        # Multi-line wrap
        b_words = b.split(' ')
        b_lines = []
        b_cur = ""
        for w in b_words:
            test = (b_cur + " " + w).strip()
            bbox = f_bullet.getbbox(test)
            if (bbox[2] - bbox[0]) > 770:
                b_lines.append(b_cur)
                b_cur = w
            else:
                b_cur = test
        if b_cur:
            b_lines.append(b_cur)
        
        line_sub_y = b_y + 6
        for bl in b_lines:
            draw.text((card_x + 115, line_sub_y), bl, fill=(241, 245, 249), font=f_bullet)
            line_sub_y += 42
        
        b_y += max(88, len(b_lines) * 44 + 42)
    
    # 7. Trust Badge (below card)
    tag_y = card_y + card_h + 30
    tag_w = 660
    tag_h = 66
    tag_x = (target_w - tag_w) // 2
    draw_round_rect(draw, (tag_x, tag_y, tag_x + tag_w, tag_y + tag_h), radius=33, fill=(255, 255, 255, 25), outline=(255, 255, 255, 60), width=2)
    
    # Decorative star on left and right of tag
    draw_mini_star(draw, tag_x + 40, tag_y + 33, size=10, fill=(245, 158, 11))
    draw_mini_star(draw, tag_x + tag_w - 40, tag_y + 33, size=10, fill=(245, 158, 11))
    draw.text((tag_x + tag_w // 2, tag_y + 17), wide(tag_text), fill=(255, 255, 255), font=f_tag, anchor="mt")
    
    # 8. CTA Button
    cta_y = tag_y + tag_h + 35
    cta_w = target_w - 140
    cta_h = 135
    cta_x = 70
    draw_round_rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h), radius=35, fill=cta_color)
    draw.text((cta_x + cta_w // 2, cta_y + 44), wide(cta_text), fill=(255, 255, 255), font=f_cta, anchor="mt")
    
    # 9. Footer Info Bar
    footer_y = cta_y + cta_h + 52
    draw.line([(70, footer_y - 15), (target_w - 70, footer_y - 15)], fill=(255, 255, 255, 35), width=1)
    
    draw.text((70, footer_y), footer_left, fill=(148, 163, 184), font=f_footer)
    draw.text((target_w - 70, footer_y), footer_right, fill=(255, 255, 255), font=f_footer, anchor="rt")
    
    # Final Composite
    final_img = Image.alpha_composite(bg.convert('RGBA'), canvas)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.convert('RGB').save(output_path, quality=96)
    print(f"Generated: {output_path}")

brain_dir = "C:/Users/HP/.gemini/antigravity-ide/brain/85fa634b-7d53-4338-b68e-8e6f2a90fa64"

# Les 24 affiches sont generees depuis public/tiktok-visuals.json : meme source
# que le studio, pour que le texte publie corresponde toujours a ce qui est
# affiche a l'ecran. Les visuels sans photo recoivent un degrade thematique,
# afin que la serie reste homogene.

PHOTOS = {
    1:  f"{brain_dir}/bg_studio_creatif_clean_1790984870355.jpg",
    6:  f"{brain_dir}/bg_logistique_lome_clean_1790984885824.jpg",
    11: f"{brain_dir}/bg_import_export_clean_1790984900206.jpg",
    15: f"{brain_dir}/bg_it_bureautique_clean_1790984930525.jpg",
    20: f"{brain_dir}/bg_ayeprep_saas_clean_1790984980813.jpg",
}

SLUGS = {
    "creative": "studio-creatif", "logistics": "logistique", "trade": "import-export",
    "it_hardware": "it-bureautique", "saas_tech": "saas", "contact": "contact",
}


def hex_to_rgb(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def gradient_from_theme(theme):
    """Extrait les arrets de couleur de la classe Tailwind du visuel."""
    stops = [hex_to_rgb(m) for m in re.findall(r'#([0-9A-Fa-f]{6})', theme or '')]
    return stops if len(stops) >= 2 else None


with io.open('public/tiktok-visuals.json', encoding='utf-8') as fh:
    visuals = json.load(fh)

os.makedirs('public/images/tiktok', exist_ok=True)

for v in visuals:
    accent = hex_to_rgb(v.get('accentColor') or '#2563EB')
    slug = SLUGS.get(v['category'], 'visuel')
    out = f"public/images/tiktok/tiktok-{v['id']:02d}-{slug}.jpg"

    generate_tiktok_poster(
        bg_path=PHOTOS.get(v['id']),
        output_path=out,
        category_badge=(v.get('badge') or v['categoryName']).upper(),
        badge_color=accent,
        main_title=v['hook'].upper(),
        subtitle=v.get('subtitle', ''),
        bullets=v.get('points', []),
        tag_text=(v.get('tag') or '').upper(),
        cta_text=(v.get('ctaText') or '').upper(),
        # Vert de marque pour TOUS les appels a l'action : c'est la couleur
        # d'action sur l'ensemble du site, elle ne doit pas varier par theme.
        cta_color=(0, 168, 89),
        footer_left="Lomé, Togo & Surrey, Canada",
        footer_right=v.get('website', 'ayegroupe.com'),
        theme_accent=accent,
        gradient_stops=gradient_from_theme(v.get('themeGradient')),
    )

print(f"\n{len(visuals)} affiches generees.")
