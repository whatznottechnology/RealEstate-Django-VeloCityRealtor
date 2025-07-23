# Django + Tailwind Starter

A modern Django project with Tailwind CSS, dark mode support, and a clean project structure. All templates and static files (including favicon and images) are organized under the `theme` app for easy management.

## Features
- Django 5.x
- Tailwind CSS (with dark mode toggle)
- All static files and templates under `theme/`
- Ready for deployment or local development

---

## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a virtual environment and activate it
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Install Django (if not in requirements.txt)
```bash
pip install django
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start Tailwind CSS (in a separate terminal)
```bash
python manage.py tailwind install  # Only needed once, on first setup
python manage.py tailwind start
```

### 7. Run the Django development server
```bash
python manage.py runserver
```

---

## Project Structure
```
theme/
    static/           # All static files (css, favicon, images, etc.)
    templates/        # All templates (base, home, components, etc.)
    ...
manage.py
requirements.txt
```

---

## Notes
- All static files (CSS, JS, images, videos, favicon, etc.) should be placed in `theme/static/`.
- All templates should be placed in `theme/templates/`.
- For user-uploaded files (media), they will be stored in the `media/` folder at the project root. Use `MEDIA_URL` and `MEDIA_ROOT` in Django settings for access.
- Tailwind CSS is fully integrated. Use `python manage.py tailwind start` to watch for changes.
- Dark mode is supported out of the box with a toggle in the UI.

---

## Static & Media Setup

- **Static files:**
    - Place all static assets (CSS, JS, images, videos, etc.) in `theme/static/`.
    - Django will collect these into `staticfiles/` when you run `python manage.py collectstatic` (for production).
    - Access in templates using `{% static 'path/to/file' %}`.

- **Media files:**
    - User-uploaded files are stored in the `media/` folder at the project root.
    - Make sure `MEDIA_URL` and `MEDIA_ROOT` are set in `settings.py` (already configured).
    - In development, serve media files by adding this to your `urls.py`:
      ```python
      from django.conf import settings
      from django.conf.urls.static import static
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
      ```
    - Access media in templates using `{{ object.image.url }}` or similar.

## Troubleshooting
- If Tailwind styles are not updating, make sure `python manage.py tailwind start` is running.
- If you add new template paths, update `tailwind.config.js` accordingly.

---

## License
MIT
