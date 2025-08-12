# Overview

UzbekNews AI is a Flask-based news platform specifically designed for Uzbek audiences, featuring AI-powered content generation and automated Telegram distribution. The application provides bilingual support (Uzbek and Russian), integrates with Google's Gemini API for content creation, and includes a complete content management system for publishing news articles focused on Uzbekistan and Central Asia.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework
- **Flask Application**: Built with Flask web framework using SQLAlchemy ORM for database operations
- **Database Layer**: SQLAlchemy with support for both SQLite (development) and PostgreSQL (production) through environment configuration
- **Authentication**: Flask-Login for session management with admin-only access to dashboard and content creation

## Content Management System
- **Multi-language Support**: Dual language content storage (Uzbek and Russian) with automatic language switching based on user session
- **Post Model**: Comprehensive post structure including SEO fields, categories, regions, view tracking, and Telegram integration status
- **User Model**: Simple admin user system with password hashing and role-based permissions
- **Content Categories**: Pre-defined Uzbek news categories including technology, economy, sports, culture, education, health, and regional news

## AI Content Generation
- **Gemini Integration**: Google Generative AI (Gemini 2.5 Flash) service for automated content creation in Uzbek language
- **Content Templates**: Structured prompts for generating news articles and Telegram posts with specific formatting requirements
- **SEO Optimization**: AI-generated meta titles, descriptions, and keywords optimized for Uzbek search terms

## Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 for responsive design
- **Uzbek Design System**: Custom CSS with Uzbek national colors (blue, white, green) and culturally appropriate styling
- **Responsive Layout**: Mobile-first design optimized for Central Asian user preferences
- **Time Localization**: Tashkent timezone integration for accurate local time display

## Content Distribution
- **Telegram Bot Integration**: Automated news posting to Telegram channels with formatted messages
- **Multi-platform Publishing**: Simultaneous web and Telegram publication with different content formats
- **View Tracking**: Separate analytics for web views and Telegram engagement

## Configuration Management
- **Environment Variables**: Centralized configuration through environment files for API keys, database URLs, and site settings
- **Regional Customization**: Pre-configured Uzbek regions and categories for localized content categorization
- **Flexible Deployment**: Support for both development (SQLite) and production (PostgreSQL) environments

# External Dependencies

## AI Services
- **Google Generative AI (Gemini)**: Content generation service requiring GEMINI_API_KEY for automated article creation and translation
- **Content Generation Models**: Gemini 2.5 Flash model for Uzbek language content creation

## Social Media Integration
- **Python Telegram Bot**: Automated posting to Telegram channels requiring TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID
- **Telegram Channel Management**: Direct integration with Telegram channels for news distribution

## Database Systems
- **SQLAlchemy ORM**: Database abstraction layer supporting multiple database backends
- **PostgreSQL**: Production database (configurable via DATABASE_URL environment variable)
- **SQLite**: Development database with automatic fallback

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and components
- **Font Awesome**: Icon library for user interface elements
- **jQuery**: JavaScript library for enhanced user interactions

## Development Tools
- **Flask-WTF**: Form handling and CSRF protection for admin interfaces
- **Python-slugify**: URL slug generation for SEO-friendly post URLs
- **Pytz**: Timezone handling for accurate Tashkent time display

## Content Processing
- **Markdown Support**: Potential content formatting support for rich text editing
- **Image Handling**: Static file management for news images and media assets