import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from main.models import CarModel


class Command(BaseCommand):
    help = 'Assigns car images to CarModel instances if missing or using default image'

    def handle(self, *args, **kwargs):
        media_path = os.path.join(settings.MEDIA_ROOT, 'car_images')
        default_image_name = 'car_images/default.jpg'

        for car in CarModel.objects.all():
            current_image = str(car.image)
            image_exists = car.image and os.path.exists(car.image.path)

            # Skip if image exists and is not the default
            if image_exists and default_image_name not in current_image:
                self.stdout.write(f"⚠️ Skipping {car.model_name} (custom image already exists)")
                continue

            image_name = car.model_name.lower().replace(' ', '-') + '.jpg'
            image_path = os.path.join(media_path, image_name)

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    car.image.save(image_name, File(f), save=True)
                    self.stdout.write(f"✅ Assigned image to {car.model_name}")
            else:
                self.stdout.write(f"❌ Image not found for {car.model_name} (expected: {image_name})")
