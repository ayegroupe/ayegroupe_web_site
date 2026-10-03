import os
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
    theme_accent=(37, 99, 235)
):
    target_w, target_h = 1080, 1920
    
    # 1. Load and scale background
    bg = Image.open(bg_path).convert('RGB')
    bg_w, bg_h = bg.size
    
    scale = max(target_w / bg_w, target_h / bg_h)
    new_w, new_h = int(bg_w * scale), int(bg_h * scale)
    bg = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    bg = bg.crop((left, top, left + target_w, top + target_h))
    
    # 2. Cinematic overlay
    overlay = create_cinematic_gradient(target_w, target_h)
    bg.paste(overlay, (0, 0), overlay)
    
    # 3. Canvas
    canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Fonts
    font_bold = "C:/Windows/Fonts/segoeuib.ttf"
    font_reg = "C:/Windows/Fonts/segoeui.ttf"
    font_mono = "C:/Windows/Fonts/tahomabd.ttf"
    
    f_brand = ImageFont.truetype(font_bold, 44)
    f_baseline = ImageFont.truetype(font_reg, 23)
    f_badge = ImageFont.truetype(font_bold, 24)
    f_title = ImageFont.truetype(font_bold, 54)
    f_sub = ImageFont.truetype(font_reg, 32)
    f_card_hdr = ImageFont.truetype(font_bold, 28)
    f_bullet = ImageFont.truetype(font_bold, 30)
    f_tag = ImageFont.truetype(font_bold, 27)
    f_cta = ImageFont.truetype(font_bold, 38)
    f_footer = ImageFont.truetype(font_bold, 25)
    
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
    draw.text((195, 78), "AYEGROUPE", fill=(255, 255, 255), font=f_brand)
    draw.text((195, 134), "Technologie • Commerce • Logistique", fill=(148, 163, 184), font=f_baseline)
    
    # Top-right category badge pill
    badge_w = 380
    badge_h = 58
    badge_x = target_w - badge_w - 70
    badge_y = 96
    draw_round_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=29, fill=(10, 25, 47, 240), outline=badge_color, width=2)
    
    draw.text((badge_x + badge_w // 2, badge_y + 14), category_badge, fill=badge_color, font=f_badge, anchor="mt")
    
    # Thin divider
    draw.line([(70, 205), (target_w - 70, 205)], fill=(255, 255, 255, 45), width=2)
    
    # 5. Main Hook Title
    title_words = main_title.split(' ')
    lines = []
    curr_line = ""
    for w in title_words:
        test = (curr_line + " " + w).strip()
        bbox = f_title.getbbox(test)
        if (bbox[2] - bbox[0]) > 940:
            lines.append(curr_line)
            curr_line = w
        else:
            curr_line = test
    if curr_line:
        lines.append(curr_line)
    
    y_text = 240
    for l in lines:
        draw.text((70, y_text), l, fill=(255, 255, 255), font=f_title)
        y_text += 68
    
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
    draw.text((card_x + 85, hdr_y), "CE QUE NOUS VOUS APPORTONS :", fill=badge_color, font=f_card_hdr)
    
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
    draw.text((tag_x + tag_w // 2, tag_y + 17), tag_text, fill=(255, 255, 255), font=f_tag, anchor="mt")
    
    # 8. CTA Button
    cta_y = tag_y + tag_h + 35
    cta_w = target_w - 140
    cta_h = 135
    cta_x = 70
    draw_round_rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h), radius=35, fill=cta_color)
    draw.text((cta_x + cta_w // 2, cta_y + 44), cta_text, fill=(255, 255, 255), font=f_cta, anchor="mt")
    
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

configs = [
    {
        "bg": f"{brain_dir}/bg_studio_creatif_clean_1790984870355.jpg",
        "out": "public/images/tiktok/tiktok-01-studio-creatif.jpg",
        "category": "STUDIO CRÉATIF",
        "badge_color": (37, 99, 235),
        "title": "CRÉATION DE SITES WEB & LOGOS PRO",
        "subtitle": "Propulsez l'image de marque de votre entreprise",
        "bullets": [
            "Sites vitrines & boutiques e-commerce ultra-rapides",
            "Paiement Mobile Money (T-Money, Flooz) & Carte bancaire",
            "Logos vectoriels uniques (SVG, AI, PDF haute résolution)",
            "Pack Corporate 360° clé en main en 7 jours ouvrés"
        ],
        "tag": "PACK PME & CRÉATION D'ENTREPRISE",
        "cta": "WHATSAPP DEVIS 15 MIN : +228 90 11 67 44",
        "cta_color": (0, 168, 89),
        "footer_left": "Lomé, Togo & Surrey, Canada",
        "footer_right": "ayegroupe.com/fr/services-creatifs"
    },
    {
        "bg": f"{brain_dir}/bg_logistique_lome_clean_1790984885824.jpg",
        "out": "public/images/tiktok/tiktok-06-logistique-lome.jpg",
        "category": "LOGISTIQUE & FRET",
        "badge_color": (245, 158, 11),
        "title": "TRANSIT PORT DE LOMÉ & ENTREPOSAGE",
        "subtitle": "Acheminement fiable et sécurisé de vos marchandises",
        "bullets": [
            "Enlèvement rapide de conteneurs & Zéro surestarie",
            "Flotte de camions porte-conteneurs géolocalisés GPS",
            "Espaces d'entreposage modernes & gardés 24h/24",
            "Corridors régionaux vers le Burkina, Mali et Niger"
        ],
        "tag": "PORT AUTONOME DE LOMÉ (PAL)",
        "cta": "COTATION EXPRESS WHATSAPP : +228 90 11 67 44",
        "cta_color": (217, 119, 6),
        "footer_left": "Port Autonome de Lomé, Togo",
        "footer_right": "ayegroupe.com/fr/togo/logistique"
    },
    {
        "bg": f"{brain_dir}/bg_import_export_clean_1790984900206.jpg",
        "out": "public/images/tiktok/tiktok-11-import-export.jpg",
        "category": "IMPORT-EXPORT",
        "badge_color": (245, 158, 11),
        "title": "SOURCING MONDIAL & DÉDOUANEMENT",
        "subtitle": "Votre passerelle d'affaires Chine, Dubaï et Europe",
        "bullets": [
            "Sourcing & audit d'usines certifiées (Chine, Turquie, Dubaï)",
            "Fret maritime conteneurs (FCL) & Groupage sécurisé (LCL)",
            "Dédouanement rapide sur le Guichet Unique (GUCE)",
            "Zéro risque fournisseur & conformité douanière totale"
        ],
        "tag": "0 RISQUE FOURNISSEUR • GUCE CONFORME",
        "cta": "CONTACTEZ NOS EXPERTS : +228 90 11 67 44",
        "cta_color": (217, 119, 6),
        "footer_left": "Hub Lomé, Togo & International",
        "footer_right": "ayegroupe.com/fr/togo/import-export"
    },
    {
        "bg": f"{brain_dir}/bg_it_bureautique_clean_1790984930525.jpg",
        "out": "public/images/tiktok/tiktok-15-it-bureautique.jpg",
        "category": "IT & BUREAUTIQUE",
        "badge_color": (37, 99, 235),
        "title": "MATÉRIEL INFORMATIQUE & MOBILIER PRO",
        "subtitle": "Équipez vos bureaux avec du matériel certifié",
        "bullets": [
            "PC Portables Dell, HP, Lenovo neufs sous garantie constructeur",
            "Câblage structuré réseau Cat6/Cat7, Baies & Wi-Fi pro",
            "Mobilier ergonomique de bureau & fauteuils de direction",
            "Contrat de maintenance informatique & infogérance PME"
        ],
        "tag": "MATÉRIEL GARANTI AVEC SAV À LOMÉ",
        "cta": "WHATSAPP CATALOGUE : +228 90 11 67 44",
        "cta_color": (0, 168, 89),
        "footer_left": "Sièges & Bureaux à Lomé, Togo",
        "footer_right": "ayegroupe.com/fr/togo/it-bureautique"
    },
    {
        "bg": f"{brain_dir}/bg_ayeprep_saas_clean_1790984980813.jpg",
        "out": "public/images/tiktok/tiktok-20-ayeprep-saas.jpg",
        "category": "EDTECH • AYEPREP.COM",
        "badge_color": (16, 185, 129),
        "title": "RÉUSSISSEZ LE TCF & TEF CANADA AVEC L'IA",
        "subtitle": "La 1ère plateforme EdTech d'entraînement par IA",
        "bullets": [
            "Simulateur d'expression orale avec IA vocale interactive",
            "Corrections instantanées de vos expressions écrites",
            "Des centaines d'examens blancs conformes aux vrais tests",
            "Atteignez le niveau C1/C2 (CLB 10) pour votre immigration"
        ],
        "tag": "PLATEFORME OFFICIELLE • 100% EN LIGNE",
        "cta": "TESTEZ GRATUITEMENT SUR AYEPREP.COM",
        "cta_color": (16, 185, 129),
        "footer_left": "Produit SaaS édité par AYEGROUPE",
        "footer_right": "ayeprep.com"
    }
]

for cfg in configs:
    generate_tiktok_poster(
        bg_path=cfg["bg"],
        output_path=cfg["out"],
        category_badge=cfg["category"],
        badge_color=cfg["badge_color"],
        main_title=cfg["title"],
        subtitle=cfg["subtitle"],
        bullets=cfg["bullets"],
        tag_text=cfg["tag"],
        cta_text=cfg["cta"],
        cta_color=cfg["cta_color"],
        footer_left=cfg["footer_left"],
        footer_right=cfg["footer_right"]
    )
    fname = os.path.basename(cfg["out"])
    brain_copy = f"{brain_dir}/{fname}"
    Image.open(cfg["out"]).save(brain_copy)
    print(f"Copied to brain: {brain_copy}")
