django-popup_ds
==========

django-popup_ds is a Django app to use for stockanalyser. For each question,
visitors can choose between a fixed number of answers.

Quick start
------------

1. Add "fav_stock" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'popup',
    ]

2. Run below command to create the popup models.::

    python manage.py makemigrations popup
    python manage.py migrate
    python manage.py createsuperuser

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a popup (you'll need the Admin app enabled).

4. Usage in the template::

    {% load popup_tags %}
    {% make_popup %}

5. If you want to see appropriate html render, please use bootstrap 5.
