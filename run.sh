#!/bin/bash

exec python /code/manage.py runserver 0.0.0.0:8000 &
exec streamlit run streamlit/app.py