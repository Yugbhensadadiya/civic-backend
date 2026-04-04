#!/usr/bin/env python3
"""
Production Environment Setup Script
Sets up secure SECRET_KEY for production
"""

import os
import secrets
import sys

def generate_secret_key():
    """Generate a secure Django SECRET_KEY"""
    return secrets.token_urlsafe(50)

def check_environment():
    """Check current environment variables"""
    print("=== Environment Check ===")
    
    secret_key = os.getenv('SECRET_KEY')
    debug = os.getenv('DEBUG', 'False')
    database_url = os.getenv('DATABASE_URL')
    
    print(f"SECRET_KEY: {'✅ Set' if secret_key and secret_key != 'django-insecure-dev-key' else '❌ Missing or using default'}")
    print(f"DEBUG: {'❌ True (Production should be False)' if debug == 'True' else '✅ False'}")
    print(f"DATABASE_URL: {'✅ Set' if database_url else '❌ Using SQLite'}")
    
    return secret_key, debug, database_url

def setup_production():
    """Setup production environment"""
    print("\n=== Production Setup ===")
    
    secret_key, debug, database_url = check_environment()
    
    if not secret_key or secret_key == 'django-insecure-dev-key':
        new_key = generate_secret_key()
        print(f"\n🔑 New SECRET_KEY generated:")
        print(f"SECRET_KEY={new_key}")
        print("\n⚠️  Add this to your Render environment variables!")
    
    if debug == 'True':
        print("\n⚠️  DEBUG is True in production!")
        print("Set DEBUG=False in production environment")
    
    if not database_url:
        print("\n⚠️  No DATABASE_URL found")
        print("Using SQLite for development only")
    
    print("\n=== Render Environment Variables Required ===")
    print("1. SECRET_KEY (use the generated key above)")
    print("2. DEBUG=False")
    print("3. DATABASE_URL=postgresql://...")
    print("4. EMAIL_HOST_USER=your-email@gmail.com")
    print("5. EMAIL_HOST_PASSWORD=your-app-password")
    print("6. CLOUDINARY_CLOUD_NAME=your-cloud-name")
    print("7. CLOUDINARY_API_KEY=your-api-key")
    print("8. CLOUDINARY_API_SECRET=your-api-secret")

if __name__ == '__main__':
    setup_production()
