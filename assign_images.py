import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_configurator.settings")
django.setup()

from django.conf import settings
from django.core.files import File
from car_configurator.main.models.car_models import CarModel

media_path = os.path.join(settings.MEDIA_ROOT, 'car_images')
default_image_name = 'car_images/default.jpg'  # Change if your default image name/path is different

for car in CarModel.objects.all():
    current_image = str(car.image)
    image_exists = car.image and os.path.exists(car.image.path)

    # Skip only if it's a real custom image AND the file exists
    if image_exists and default_image_name not in current_image:
        print(f"⚠️ Skipping {car.model_name} (custom image already exists)")
        continue

    image_name = car.model_name.lower().replace(' ', '-') + '.jpg'
    image_path = os.path.join(media_path, image_name)

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            car.image.save(image_name, File(f), save=True)
            print(f"✅ Assigned image to {car.model_name}")
    else:
        print(f"❌ Image not found for {car.model_name} (expected: {image_name})")
