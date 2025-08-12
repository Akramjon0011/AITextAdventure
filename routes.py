from flask import render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length
from sqlalchemy import desc, func
import logging

from app import app, db
from models.user import User
from models.post import Post
from services.gemini_service import GeminiService
from services.telegram_service import TelegramService
from utils.helpers import format_uzbek_date, get_current_language, create_excerpt
from config import Config

# Initialize services
gemini_service = GeminiService()
telegram_service = TelegramService()

# Forms
class LoginForm(FlaskForm):
    username = StringField('Foydalanuvchi nomi', validators=[DataRequired()])
    password = PasswordField('Parol', validators=[DataRequired()])
    remember_me = BooleanField('Meni eslab qol')
    submit = SubmitField('Kirish')

class PostForm(FlaskForm):
    title_uz = StringField('Sarlavha (O\'zbek)', validators=[DataRequired(), Length(max=200)])
    title_ru = StringField('Sarlavha (Rus)', validators=[Length(max=200)])
    content_uz = TextAreaField('Mazmun (O\'zbek)', validators=[DataRequired()])
    content_ru = TextAreaField('Mazmun (Rus)')
    category = SelectField('Kategoriya', choices=[(cat, cat) for cat in Config.UZBEK_CATEGORIES])
    region = SelectField('Viloyat', choices=[('', 'Tanlang')] + [(region, region) for region in Config.UZBEK_REGIONS])
    keywords = StringField('Kalit so\'zlar')
    published = BooleanField('Nashr etish')
    featured = BooleanField('Asosiy yangilik')
    submit = SubmitField('Saqlash')

# Public Routes
@app.route('/')
def index():
    """Home page"""
    try:
        # Get featured posts
        featured_posts = Post.query.filter_by(published=True, featured=True).order_by(desc(Post.created_at)).limit(6).all()
        
        # Get recent posts
        recent_posts = Post.query.filter_by(published=True).order_by(desc(Post.created_at)).limit(8).all()
        
        # Get popular posts
        popular_posts = Post.query.filter_by(published=True).order_by(desc(Post.views)).limit(5).all()
        
        return render_template('index.html',
                             featured_posts=featured_posts,
                             recent_posts=recent_posts,
                             popular_posts=popular_posts,
                             config=Config)
    except Exception as e:
        logging.error(f"Error loading home page: {e}")
        return render_template('index.html',
                             featured_posts=[],
                             recent_posts=[],
                             popular_posts=[],
                             config=Config)

@app.route('/yangilik/<slug>')
def post_detail(slug):
    """Individual post page"""
    try:
        post = Post.query.filter_by(slug=slug, published=True).first_or_404()
        
        # Increment views
        post.increment_views()
        
        # Get related posts
        related_posts = Post.query.filter(
            Post.category == post.category,
            Post.id != post.id,
            Post.published == True
        ).order_by(desc(Post.created_at)).limit(4).all()
        
        # Get popular posts for sidebar
        popular_posts = Post.query.filter_by(published=True).order_by(desc(Post.views)).limit(5).all()
        
        # Get category posts for sidebar
        category_posts = Post.query.filter(
            Post.category == post.category,
            Post.id != post.id,
            Post.published == True
        ).order_by(desc(Post.created_at)).limit(3).all()
        
        # Handle language parameter
        lang = request.args.get('lang')
        if lang in ['uz', 'ru']:
            session['language'] = lang
        
        return render_template('post.html',
                             post=post,
                             related_posts=related_posts,
                             popular_posts=popular_posts,
                             category_posts=category_posts,
                             config=Config)
    except Exception as e:
        logging.error(f"Error loading post {slug}: {e}")
        abort(404)

@app.route('/kategoriya/<name>')
def category(name):
    """Category page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 12
        
        posts = Post.query.filter_by(category=name, published=True).order_by(desc(Post.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('category.html',
                             posts=posts,
                             category_name=name,
                             config=Config)
    except Exception as e:
        logging.error(f"Error loading category {name}: {e}")
        return redirect(url_for('index'))

@app.route('/viloyat/<region>')
def region_posts(region):
    """Regional news page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 12
        
        posts = Post.query.filter_by(region=region, published=True).order_by(desc(Post.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('region.html',
                             posts=posts,
                             region_name=region,
                             config=Config)
    except Exception as e:
        logging.error(f"Error loading region {region}: {e}")
        return redirect(url_for('index'))

@app.route('/qidiruv')
def search():
    """Search page"""
    try:
        query = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        if not query:
            return render_template('search.html', posts=None, query='', config=Config)
        
        # Search in title and content
        posts = Post.query.filter(
            Post.published == True,
            (Post.title_uz.contains(query) | 
             Post.content_uz.contains(query) |
             Post.title_ru.contains(query) |
             Post.content_ru.contains(query))
        ).order_by(desc(Post.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('search.html',
                             posts=posts,
                             query=query,
                             config=Config)
    except Exception as e:
        logging.error(f"Error in search: {e}")
        return render_template('search.html', posts=None, query=query, config=Config)

@app.route('/set-language/<language>')
def set_language(language):
    """Set language preference"""
    if language in ['uz', 'ru']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        flash('Noto\'g\'ri foydalanuvchi nomi yoki parol', 'error')
    
    return render_template('admin/login.html', form=form, config=Config)

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('Tizimdan chiqildi', 'info')
    return redirect(url_for('index'))

@app.route('/admin/')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin:
        abort(403)
    
    try:
        # Get statistics
        stats = {
            'total_posts': Post.query.count(),
            'published_posts': Post.query.filter_by(published=True).count(),
            'total_views': db.session.query(func.sum(Post.views)).scalar() or 0,
            'telegram_sent': Post.query.filter_by(telegram_posted=True).count()
        }
        
        # Get recent posts
        recent_posts = Post.query.order_by(desc(Post.created_at)).limit(10).all()
        
        # Check system status
        gemini_status = True
        telegram_status = True
        
        try:
            # Test Gemini
            test_response = gemini_service.summarize_content("Test content", "uz")
            gemini_status = bool(test_response)
        except:
            gemini_status = False
        
        try:
            # Test Telegram
            telegram_status = bool(telegram_service.bot_token and telegram_service.channel_id)
        except:
            telegram_status = False
        
        return render_template('admin/dashboard.html',
                             stats=stats,
                             recent_posts=recent_posts,
                             gemini_status=gemini_status,
                             telegram_status=telegram_status,
                             config=Config)
    except Exception as e:
        logging.error(f"Error in admin dashboard: {e}")
        return render_template('admin/dashboard.html',
                             stats={'total_posts': 0, 'published_posts': 0, 'total_views': 0, 'telegram_sent': 0},
                             recent_posts=[],
                             gemini_status=False,
                             telegram_status=False,
                             config=Config)

@app.route('/admin/posts')
@login_required
def admin_posts():
    """Admin posts list"""
    if not current_user.is_admin:
        abort(403)
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        posts = Post.query.order_by(desc(Post.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/posts.html', posts=posts, config=Config)
    except Exception as e:
        logging.error(f"Error loading admin posts: {e}")
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/post/create', methods=['GET', 'POST'])
@login_required
def admin_create_post():
    """Create new post"""
    if not current_user.is_admin:
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post()
            post.title_uz = form.title_uz.data
            post.title_ru = form.title_ru.data
            post.content_uz = form.content_uz.data
            post.content_ru = form.content_ru.data
            post.category = form.category.data
            post.region = form.region.data if form.region.data else None
            post.keywords = form.keywords.data
            post.published = form.published.data
            post.featured = form.featured.data
            post.author_id = current_user.id
            
            db.session.add(post)
            db.session.commit()
            
            flash('Maqola muvaffaqiyatli yaratildi!', 'success')
            
            # Send to Telegram if published
            if post.published:
                try:
                    telegram_service.send_news_sync(post)
                    post.telegram_posted = True
                    db.session.commit()
                    flash('Telegram kanaliga jo\'natildi!', 'info')
                except Exception as e:
                    logging.error(f"Failed to send to Telegram: {e}")
                    flash('Telegram jo\'natishda xatolik!', 'warning')
            
            return redirect(url_for('admin_posts'))
        except Exception as e:
            logging.error(f"Error creating post: {e}")
            flash('Maqola yaratishda xatolik!', 'error')
            db.session.rollback()
    
    return render_template('admin/create_post.html', form=form, config=Config)

@app.route('/admin/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_post(id):
    """Edit post"""
    if not current_user.is_admin:
        abort(403)
    
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(post)
            db.session.commit()
            flash('Maqola yangilandi!', 'success')
            return redirect(url_for('admin_posts'))
        except Exception as e:
            logging.error(f"Error updating post: {e}")
            flash('Yangilashda xatolik!', 'error')
            db.session.rollback()
    
    return render_template('admin/edit_post.html', form=form, post=post, config=Config)

@app.route('/admin/ai-generator')
@login_required
def admin_ai_generator():
    """AI content generator"""
    if not current_user.is_admin:
        abort(403)
    
    return render_template('admin/ai_generator.html', config=Config)

@app.route('/admin/generate-content', methods=['POST'])
@login_required
def admin_generate_content():
    """Generate content with AI"""
    if not current_user.is_admin:
        abort(403)
    
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        keywords = data.get('keywords', '')
        
        if not topic:
            return jsonify({'error': 'Mavzu kiritilmagan'}), 400
        
        # Generate content
        content = gemini_service.generate_uzbek_news(topic, keywords)
        
        if not content:
            return jsonify({'error': 'Kontent yaratib bo\'lmadi'}), 500
        
        # Generate Telegram post
        telegram_content = gemini_service.generate_telegram_post(
            content.get('title', ''), 
            content.get('content', '')[:200]
        )
        
        # Translate to Russian
        translation = gemini_service.translate_to_russian(
            content.get('title', ''), 
            content.get('content', '')
        )
        
        result = {
            'title_uz': content.get('title', ''),
            'content_uz': content.get('content', ''),
            'meta_title': content.get('meta_title', ''),
            'meta_description': content.get('meta_description', ''),
            'keywords': content.get('keywords', ''),
            'title_ru': translation.get('title_ru', ''),
            'content_ru': translation.get('content_ru', ''),
            'telegram_content': telegram_content
        }
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error generating content: {e}")
        return jsonify({'error': f'Xatolik: {str(e)}'}), 500

@app.route('/admin/telegram')
@login_required
def admin_telegram():
    """Telegram management"""
    if not current_user.is_admin:
        abort(403)
    
    return render_template('admin/telegram.html', config=Config)

# Context processors
@app.context_processor
def utility_processor():
    """Add utility functions to templates"""
    from datetime import datetime
    return {
        'moment': lambda: datetime.now(),  # Simple datetime function
        'config': Config,
        'current_language': get_current_language,
        'format_uzbek_date': format_uzbek_date,
        'create_excerpt': create_excerpt
    }

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', config=Config), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', config=Config), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', config=Config), 500

# Template filters
@app.template_filter('uzbek_date')
def uzbek_date_filter(date):
    return format_uzbek_date(date)

@app.template_filter('excerpt')
def excerpt_filter(content, length=150):
    return create_excerpt(content, length)