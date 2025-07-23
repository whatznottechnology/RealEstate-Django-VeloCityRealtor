import os
import shutil

"""
Script to copy all demo images from static/images/demoimages/ to media/project/banner/ and media/project/gallery/ etc.
This ensures images are available in MEDIA_ROOT for Django to serve as uploaded files.
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DEMO = os.path.join(BASE_DIR, 'static', 'images', 'demoimages')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Map of model upload_to folders
DESTS = [
    'project/banner/',
    'project/gallery/',
    'project/floor_plans/',
    'project/construction_updates/',
    'project/amenities/',
]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_demo_images():
    images = [f for f in os.listdir(STATIC_DEMO) if f.lower().endswith('.jpg')]
    if not images:
        print('No demo images found in static/images/demoimages')
        return
    for dest in DESTS:
        dest_dir = os.path.join(MEDIA_ROOT, dest)
        ensure_dir(dest_dir)
        for img in images:
            src = os.path.join(STATIC_DEMO, img)
            dst = os.path.join(dest_dir, img)
            shutil.copy2(src, dst)
            print(f'Copied {img} to {dest}')
    print('✅ All demo images copied to media folders.')

if __name__ == '__main__':
    copy_demo_images()
