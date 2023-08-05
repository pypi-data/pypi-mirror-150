{\rtf1\ansi\ansicpg1252\cocoartf2638
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 =====\
Learning Log\
=====\
\
Learning Log is a Django app to track learning that provides users with action such as log in, register, create topic, and entries to that topic.\
\
Detailed documentation is in the \'93docs\'94 directory.\
\
Quick start\
-----------\
\
1. Add \'93learning_logs\'94 and  \'93users\'94 to your INSTALLED_APPS setting like this::\
\
    INSTALLED_APPS = [\
        ...\
        \'91learning_logs,\
	\'91users\'92,\
    ]\
\
2. Include the learning_logs and users URLconf in your project urls.py like this::\
\
    path('', include(\'91learning_logs.urls')),\
    path(\'91users\'92, include(\'91users.urls')),\
\
3. Run ``python3 manage.py migrate`` to create the required models\
\
4. Start the development server with ``python3 manage.py runserver`` and visit http://127.0.0.1:8000\
   to start your Learning Log!\
}