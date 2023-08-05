=====
Learning Log
=====

Learning Log is a Django app to track learning that provides users with action such as log in, register, create topic, and entries to that topic.\

Detailed documentation is in the 'docs' directory.

Quick start
-----------

1. Add 'learning_logs', 'users' and 'bootstrap4' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'learning_logs',
	    'users',
    ]

2. Include the learning_logs and users URLconf in your project urls.py like this::

    path('', include(\'learning_logs.urls')),
    path('users', include('users.urls')),

3. Add ``LOGIN_URL = 'users:login'`` in settings.py

3. Run ``python3 manage.py migrate`` to create the required models

4. Start the development server with ``python3 manage.py runserver`` and visit http://127.0.0.1:8000 to start your Learning Log!