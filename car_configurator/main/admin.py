import os
from django.conf import settings
from django.core.files import File
from django.contrib import admin
from django.utils.html import format_html
from .models import CarModel, Engine, Color, Wheel, Configuration, ColorImage

# Inline models to allow adding options directly inside a car model
class EngineInline(admin.TabularInline):
    model = Engine
    extra = 0  # Number of blank rows for adding new items

class ColorInline(admin.TabularInline):
    model = Color
    extra = 0

class WheelInline(admin.TabularInline):
    model = Wheel
    extra = 0




class ColorImageInline(admin.TabularInline):
    model = ColorImage
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "No image"

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    inlines = [ColorImageInline]


# Admin for managing car models and linking them with options
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'model_name')  # Display fields
    search_fields = ('company_name', 'model_name')  # Enable search
    inlines = [EngineInline, ColorInline, WheelInline]  # Allow adding options inside the car model
    actions = ['assign_car_images', 'remove_car_images']  # Acțiune custom în admin

    def assign_car_images(self, request, queryset):
        import os
        from django.conf import settings
        from django.core.files import File

        media_path = os.path.join(settings.MEDIA_ROOT, 'car_images')
        default_image_name = 'car_images/default.jpg'
        updated = 0
        skipped = 0
        not_found = 0

        for car in queryset:
            current_image = str(car.image)
            image_exists = car.image and os.path.exists(car.image.path)

            if image_exists and default_image_name not in current_image:
                skipped += 1
                continue

            image_name = car.model_name.lower().replace(' ', '-') + '.jpg'
            image_path = os.path.join(media_path, image_name)

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    car.image.save(image_name, File(f), save=True)
                    updated += 1
            else:
                not_found += 1

        self.message_user(
            request,
            f"✅ Imagini actualizate: {updated}, ❌ Lipsă: {not_found}, ⚠️ Sărite: {skipped}"
        )

    assign_car_images.short_description = "Asignează automat imaginile lipsă pentru CarModel"

    def remove_car_images(self, request, queryset):
        deleted = 0

        for car in queryset:
            if car.image:
                car.image.delete(save=False)  # Delete the image from the model (but not from filesystem)
                deleted += 1

        self.message_user(
            request,
            f"✅ Imagini șterse: {deleted}"
        )

    remove_car_images.short_description = "Șterge toate imaginile de la modelele selectate"



# # Registering predefined options separately
# @admin.register(Engine)
# class EngineAdmin(admin.ModelAdmin):
#     list_display = ('name', 'types', 'power', 'car_model')  # Show car model
#     search_fields = ('name', 'types', 'car_model__model_name')

# @admin.register(Color)
# class ColorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'hex_code', 'car_model')
#     search_fields = ('name', 'car_model__model_name')

# @admin.register(Wheel)
# class WheelAdmin(admin.ModelAdmin):
#     list_display = ('style', 'size', 'car_model')
#     search_fields = ('style', 'car_model__model_name')
    

# Admin for viewing and managing user configurations
@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_model', 'engine', 'color', 'wheel', 'created_at', 'get_total_price', 'offered_config', 'get_total_price')
    search_fields = ('user__username', 'car_model__model_name','saved_config', 'offered_config')
    list_filter = ('car_model', 'engine', 'color', 'wheel')
    readonly_fields = ('get_total_price',)  # Optional: show in detail view

    def get_total_price(self, obj):
        return f"{obj.total_price():,.2f} €"
    get_total_price.short_description = 'Total Price'