from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
import json

class Command(BaseCommand):
    help = 'Load car model fixtures with dynamic created_by'

    def handle(self, *args, **kwargs):
        # Get the user (use the superuser or logged-in user)
        user = User.objects.filter(is_superuser=True).first()  # Or specify the user explicitly
        if not user:
            self.stderr.write("No superuser found. Please create a superuser.")
            return
        
        # Load the fixture manually
        fixture_path = 'C:\Users\flori\Desktop\carconfigurator\car_configurator\car_data.json'  # Update with your actual fixture path
        with open(fixture_path, 'r') as fixture_file:
            data = json.load(fixture_file)
        
        # Replace 'created_by' field with the current user ID (dynamically set)
        for obj in data:
            if obj['model'] == 'main.carmodel':  # Ensure you're targeting the correct model
                obj['fields']['created_by'] = user.id
        
        # Write the modified fixture to a temporary file
        with open('temp_fixture.json', 'w') as temp_fixture:
            json.dump(data, temp_fixture)

        # Call the loaddata command to load the modified fixture
        call_command('loaddata', 'temp_fixture.json')

        # Clean up the temporary fixture
        self.stdout.write("Fixture loaded successfully with dynamic user.")
