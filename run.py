#!/usr/bin/env python3
"""
Run the Flask application with Waitress server
"""
from waitress import serve
from app import app

if __name__ == '__main__':
    print("Starting dashboard application with Waitress...")
    print("Dashboard will be available at:")
    print("- Main page: http://localhost:8080/")
    print("- Dashboard: http://localhost:8080/dashboard/")
    print("\nPress Ctrl+C to stop the server")
    
    serve(app, host='0.0.0.0', port=8080)