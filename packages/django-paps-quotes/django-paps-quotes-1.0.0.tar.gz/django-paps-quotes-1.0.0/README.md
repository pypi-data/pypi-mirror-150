 ## django-paps-quotes/README.rst

 =======
django-paps-quotes
 =======

 django-paps-deliveries is a simple Django app to to manage all delivery prices urls from paps.
 Detailed documentation is in the "docs" directory.

 Quick start
 -----------

 1. Add "quotes" to your INSTALLED_APPS setting like this::

     INSTALLED_APPS = [
         ...
         'quotes',
     ]

 2. Include the quotes URLconf in your project urls.py like this::

     path('quotes/', include('quotes.urls')),

 3. Run `**python manage.py migrate**` to create the quotes models.

 4. Visit http://127.0.0.1:8000/quotes/ to see all authentication urls.
