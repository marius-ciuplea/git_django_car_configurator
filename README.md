Car Configurator – Django Web Application

📌 Project Description

The Car Configurator is a full-stack Django web application that allows users to configure and customize a car before requesting a personalized offer. Inspired by websites like volkswagen.ro, this app simulates a real-world vehicle configurator experience.

Users can select:

✅ Car model

⚙️ Engine type

🎨 Exterior color

🛞 Wheel style

The app dynamically updates:

💰 Total price based on selected option

📸 Image carousel based on selected color

✉️ Ability to send an offer request

🔧 Features

Dynamic car configuration system

Real-time price calculation

Image carousel that updates based on color selection

Custom "Send Offer" functionality

Clean and responsive frontend

Admin interface to manage configurations and pricing

🛠️ Technologies Used

Backend: Python, Django

Frontend: HTML, CSS, JavaScript

Database: SQLite

Instructions:

1. Use
   ```bash
   git clone https://github.com/marius-ciuplea/git_django_car_configurator.git
   ```
2. Create a virtual env (Optionally)
   ```bash
   python -m virtualenv "name_env"
   ```
3. Run requirements.txt
   ```bash
   python manage.py -r requirements.txt
4. Make migrations
   ```bash
   python manage.py migrate
   ```
5. Load fixtures
   ```bash
   python manage.py loaddata car_data.json
   ```
   ```bash
   python manage.py loaddata colors_and_images.json
   ```
6. Assign images to models
   ```bash
   python manage.py assign_car_images
   ```


## 👤 Author
- **marius-ciuplea** - [GitHub](https://github.com/marius-ciuplea)
