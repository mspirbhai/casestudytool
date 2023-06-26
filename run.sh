#!/bin/bash

exec gunicorn django_project.wsgi -b 0.0.0.0:8000 --workers 2&
exec streamlit run streamlit/app.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false 