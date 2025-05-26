Car Configurator – Django Web Application

📌 Project Description
The Car Configurator is a Django web application that allows users to configure and customize a car before requesting a personalized offer.
Inspired by websites like volkswagen.ro, this app simulates a real-world vehicle configurator experience.

Users can select:

✅ Car model
⚙️ Engine type
🎨 Exterior color
🛞 Wheel style

The app dynamically updates:

💰 Total price based on selected option
📸 Image carousel based on selected color

🔧 Features

Dynamic car configuration system
Real-time price calculation
Image carousel that updates based on color selection
Clean and responsive frontend
Admin interface to manage configurations and pricing

🛠️ Technologies Used

Backend: Python, Django
Frontend: HTML, CSS, JavaScript
Database: SQLite 


Setup Instructions


1. Clone the repository
 ```bash
  https://github.com/marius-ciuplea/git_django_car_configurator.git
```

3. Install dependencies
  ```bash
  pip install -r requirements.txt
```

4. Apply database migrations
  ```bash
  python manage.py migrate
```

5. Load initial data fixtures
  ```bash
   python manage.py loaddata car_data.json
   python manage.py loaddata colors_and_images.json
```

6. Assign images to car models
  ```bash
  python manage.py assign_car_images
```

7. Optional
 Create a superuser if you want to access admin panel
```bash
   python manage.py createsuperuser
```

## 👤 Author
- **marius-ciuplea** - [GitHub](https://github.com/marius-ciuplea)
