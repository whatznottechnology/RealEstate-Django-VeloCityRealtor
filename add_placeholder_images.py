#!/usr/bin/env python
"""
Add placeholder images to the Azure Heights Premium project
"""

import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Source.settings')
django.setup()

from Projects.models import Project, GalleryImage, FloorPlan, ConstructionUpdate

def create_placeholder_image(width, height, text, bg_color=(70, 130, 180), text_color=(255, 255, 255)):
    """Create a placeholder image with text"""
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", size=min(width, height) // 10)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", size=min(width, height) // 10)
        except:
            font = ImageFont.load_default()
    
    # Calculate text size and position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    return image

def add_project_images():
    """Add placeholder images to the Azure Heights Premium project"""
    print("🖼️ Adding placeholder images to Azure Heights Premium...")
    
    try:
        project = Project.objects.get(name='Azure Heights Premium')
        print(f"✅ Found project: {project.name}")
    except Project.DoesNotExist:
        print("❌ Azure Heights Premium project not found!")
        return
    
    # Add banner image
    if not project.banner_image:
        print("📸 Creating banner image...")
        banner_img = create_placeholder_image(1200, 600, "Azure Heights Premium\nLuxury Living in Bandra West", (30, 60, 120))
        banner_buffer = BytesIO()
        banner_img.save(banner_buffer, format='JPEG', quality=85)
        banner_buffer.seek(0)
        
        project.banner_image.save(
            'azure_heights_banner.jpg',
            ContentFile(banner_buffer.read()),
            save=True
        )
        print("✅ Banner image added")
    
    # Add logo
    if not project.logo:
        print("🏢 Creating logo...")
        logo_img = create_placeholder_image(300, 150, "PRESTIGE\nGROUP", (140, 69, 172))
        logo_buffer = BytesIO()
        logo_img.save(logo_buffer, format='PNG', quality=95)
        logo_buffer.seek(0)
        
        project.logo.save(
            'prestige_logo.png',
            ContentFile(logo_buffer.read()),
            save=True
        )
        print("✅ Logo added")
    
    # Add gallery images
    gallery_images_data = [
        ("Building Exterior", (800, 600), (52, 152, 219)),
        ("Lobby & Reception", (800, 600), (155, 89, 182)),
        ("Swimming Pool", (800, 600), (26, 188, 156)),
        ("Fitness Center", (800, 600), (241, 196, 15)),
        ("Clubhouse", (800, 600), (231, 76, 60)),
        ("Landscaped Gardens", (800, 600), (46, 125, 50)),
    ]
    
    existing_gallery_count = project.gallery_images.count()
    if existing_gallery_count == 0:
        print("🖼️ Creating gallery images...")
        for i, (name, (width, height), color) in enumerate(gallery_images_data):
            img = create_placeholder_image(width, height, f"Azure Heights\n{name}", color)
            img_buffer = BytesIO()
            img.save(img_buffer, format='JPEG', quality=85)
            img_buffer.seek(0)
            
            gallery_image = GalleryImage.objects.create(
                project=project,
                caption=name,
                order=i + 1,
                is_active=True
            )
            gallery_image.image.save(
                f'gallery_{i+1}_{name.lower().replace(" ", "_")}.jpg',
                ContentFile(img_buffer.read()),
                save=True
            )
            print(f"  ✅ Gallery image {i+1}: {name}")
    else:
        print(f"ℹ️ Gallery already has {existing_gallery_count} images")
    
    # Add floor plan images
    floor_plans = project.floor_plans.all()
    floor_plan_count = 0
    for plan in floor_plans:
        if not plan.image:
            print(f"📐 Creating floor plan image for: {plan.name}")
            plan_img = create_placeholder_image(800, 600, f"{plan.name}\n{plan.area}", (44, 62, 80))
            plan_buffer = BytesIO()
            plan_img.save(plan_buffer, format='JPEG', quality=85)
            plan_buffer.seek(0)
            
            plan.image.save(
                f'floor_plan_{plan.name.lower().replace(" ", "_")}.jpg',
                ContentFile(plan_buffer.read()),
                save=True
            )
            floor_plan_count += 1
    
    if floor_plan_count > 0:
        print(f"✅ Added {floor_plan_count} floor plan images")
    else:
        print("ℹ️ Floor plans already have images")
    
    # Add construction update images
    construction_updates = project.construction_updates.all()
    update_count = 0
    for update in construction_updates:
        if not update.image:
            print(f"🚧 Creating construction update image for: {update.title}")
            update_img = create_placeholder_image(600, 400, f"Construction Update\n{update.update_date.strftime('%B %Y')}", (52, 73, 94))
            update_buffer = BytesIO()
            update_img.save(update_buffer, format='JPEG', quality=85)
            update_buffer.seek(0)
            
            update.image.save(
                f'construction_update_{update.order}.jpg',
                ContentFile(update_buffer.read()),
                save=True
            )
            update_count += 1
    
    if update_count > 0:
        print(f"✅ Added {update_count} construction update images")
    else:
        print("ℹ️ Construction updates already have images")
    
    print("🎉 All placeholder images have been added successfully!")

def main():
    """Main function"""
    print("🚀 Adding Placeholder Images to Azure Heights Premium...")
    print("=" * 60)
    
    try:
        add_project_images()
        print("=" * 60)
        print("✅ PLACEHOLDER IMAGES ADDED SUCCESSFULLY!")
        print("🌐 Your project now has all required images!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error adding images: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
