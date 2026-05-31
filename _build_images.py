"""Build WebP images for anniversary site: full (max 1200px) + thumb (max 250px)."""
import os
from PIL import Image

SRC = '图片们'
FULL = os.path.join(SRC, 'full')
THUMB = os.path.join(SRC, 'thumb')

os.makedirs(FULL, exist_ok=True)
os.makedirs(THUMB, exist_ok=True)

SIZE_FULL = 1200
SIZE_THUMB = 250
QUALITY_FULL = 82
QUALITY_THUMB = 70

files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.jpg'))

for f in files:
    path = os.path.join(SRC, f)
    img = Image.open(path).convert('RGB')
    w, h = img.size

    # Full size
    ratio = min(SIZE_FULL / w, SIZE_FULL / h, 1.0)
    if ratio < 1:
        full_img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    else:
        full_img = img
    full_out = os.path.join(FULL, os.path.splitext(f)[0] + '.webp')
    full_img.save(full_out, 'WEBP', quality=QUALITY_FULL)
    full_sz = os.path.getsize(full_out)

    # Thumbnail
    ratio_t = min(SIZE_THUMB / w, SIZE_THUMB / h)
    thumb_img = img.resize((int(w * ratio_t), int(h * ratio_t)), Image.LANCZOS)
    thumb_out = os.path.join(THUMB, os.path.splitext(f)[0] + '.webp')
    thumb_img.save(thumb_out, 'WEBP', quality=QUALITY_THUMB)
    thumb_sz = os.path.getsize(thumb_out)

    print(f'{f}: {w}x{h} → full={full_sz//1024}KB thumb={thumb_sz//1024}KB')

# Summary
total_full = sum(os.path.getsize(os.path.join(FULL, x)) for x in os.listdir(FULL))
total_thumb = sum(os.path.getsize(os.path.join(THUMB, x)) for x in os.listdir(THUMB))
total_orig = sum(os.path.getsize(os.path.join(SRC, x)) for x in files)
print(f'\nOriginal: {total_orig/1024/1024:.1f}MB')
print(f'Full WebP: {total_full/1024:.0f}KB ({total_full*100/total_orig:.1f}%)')
print(f'Thumb WebP: {total_thumb/1024:.0f}KB ({total_thumb*100/total_orig:.1f}%)')
print('Done.')
