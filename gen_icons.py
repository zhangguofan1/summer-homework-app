"""Generate PWA app icons (192x192 and 512x512)"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = r"C:/Users/Administrator/WorkBuddy/2026-07-27-10-57-34/summer-homework-workbench"

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Circular background with purple gradient
    margin = size // 16
    cx, cy = size // 2, size // 2
    r = size // 2 - margin

    # Draw gradient circle (purple to indigo)
    for y in range(cy - r, cy + r):
        for x in range(cx - r, cx + r):
            dx, dy = x - cx, y - cy
            if dx*dx + dy*dy <= r*r:
                t = (y - (cy - r)) / (2 * r)
                # Purple (#4f46e5) to darker indigo (#3730a3)
                R = int(79 - 30*t)
                G = int(70 - 30*t)
                B = int(229 - 50*t)
                img.putpixel((x, y), (R, G, B, 255))

    # White inner circle for contrast
    inner_r = r - size // 20
    draw.ellipse(
        [cx - inner_r + 2, cy - inner_r + 2, cx + inner_r - 2, cy + inner_r - 2],
        outline=(255, 255, 255, 60), width=max(2, size // 64)
    )

    # Draw a checkmark / book icon
    # Book shape
    book_w = size * 0.35
    book_h = size * 0.40
    book_l = cx - book_w / 2
    book_t = cy - book_h / 2

    # Left page
    draw.rounded_rectangle(
        [book_l, book_t, cx, book_t + book_h],
        radius=size//30, fill=(255, 255, 255, 230)
    )
    # Right page
    draw.rounded_rectangle(
        [cx, book_t, book_l + book_w, book_t + book_h],
        radius=size//30, fill=(255, 255, 255, 200)
    )
    # Spine line
    draw.line([cx, book_t + size//40, cx, book_t + book_h - size//40],
              fill=(79, 70, 229, 180), width=max(2, size // 48))

    # Checkmark on the book
    check_size = size * 0.14
    check_cx = cx
    check_cy = cy - size * 0.03

    # Checkmark circle
    draw.ellipse(
        [check_cx - check_size, check_cy - check_size,
         check_cx + check_size, check_cy + check_size],
        fill=(34, 197, 94, 255)
    )

    # Checkmark (✓)
    cw = check_size * 1.2
    ch = check_size * 0.8
    # Simple checkmark using lines
    p1 = (check_cx - cw * 0.35, check_cy)
    p2 = (check_cx - cw * 0.05, check_cy + ch * 0.55)
    p3 = (check_cx + cw * 0.45, check_cy - ch * 0.4)
    for pt_pair, thick in [((p1, p2), 3), ((p2, p3), 3)]:
        draw.line(pt_pair, fill=(255, 255, 255, 255),
                  width=max(3, size // 24))

    return img

# Generate both sizes
for size in [192, 512]:
    icon = draw_icon(size)
    path = os.path.join(OUT, f'icon-{size}.png')
    icon.save(path, 'PNG')
    print(f'Generated {path} ({size}x{size})')

print('Done!')
