#!/bin/bash

exec streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false 