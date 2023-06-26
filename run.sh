#!/bin/bash

exec gunicorn django_project.wsgi -b 0.0.0.0:8000 &
exec streamlit run streamlit/app.py