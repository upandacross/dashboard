#!/usr/bin/env python3
"""
Test script to verify dashboard data generation
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dashboard_app import create_dash_app
    print("✅ Dashboard app imported successfully!")
    
    # Test creating the app
    app = create_dash_app()
    print("✅ Dashboard app created successfully!")
    
    # Test that we can access some basic properties
    print(f"✅ App URL base pathname: {app.config.url_base_pathname}")
    print("✅ Dashboard is ready to run!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()