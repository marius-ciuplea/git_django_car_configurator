🚗 Car Configurator – Django Web Application
📌 Overview

The Car Configurator is a full-stack Django web application that allows users to configure and customize a car before requesting a personalized offer.

Inspired by real-world vehicle configurators (e.g., volkswagen.ro), this project demonstrates skills in backend development, dynamic frontends, and database integration.

✨ Features

✅ Selectable car model, engine type, exterior color, and wheel style

💰 Real-time price calculation based on selected options

🎨 Dynamic image carousel that updates with the selected color

✉️ Send Offer functionality for personalized requests

🛠️ Admin interface to manage configurations and pricing

📱 Clean and responsive frontend



🛠️ Technologies

Backend: Python, Django

Frontend: HTML, CSS, JavaScript

Database: SQLite

<img width="1888" height="644" alt="image" src="https://github.com/user-attachments/assets/1f46fbff-8f1c-4049-9d4c-3ab6c942ad06" />

<img width="1901" height="901" alt="image" src="https://github.com/user-attachments/assets/2263387a-629d-4e91-bbf3-ad58574abd12" />

<img width="1385" height="891" alt="image" src="https://github.com/user-attachments/assets/c2ee42df-5072-4fb6-a6e8-f9d24f5127f5" />




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
