from app import db
from .database import BaseModel
from datetime import datetime
from slugify import slugify

class Post(BaseModel):
    __tablename__ = 'posts'
    
    # Multi-language titles
    title_uz = db.Column(db.String(200), nullable=False)
    title_ru = db.Column(db.String(200))
    
    # Multi-language content
    content_uz = db.Column(db.Text, nullable=False)
    content_ru = db.Column(db.Text)
    
    # Telegram content
    telegram_content_uz = db.Column(db.Text)
    telegram_content_ru = db.Column(db.Text)
    
    # SEO fields
    meta_title_uz = db.Column(db.String(60))
    meta_description_uz = db.Column(db.String(155))
    slug = db.Column(db.String(255), unique=True, nullable=False)
    
    # Categories and regions
    category = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50))
    keywords = db.Column(db.String(200))
    
    # Status and stats
    published = db.Column(db.Boolean, default=False)
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    telegram_views = db.Column(db.Integer, default=0)
    telegram_posted = db.Column(db.Boolean, default=False)
    
    # Relationships
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        if not self.slug and self.title_uz:
            self.slug = slugify(self.title_uz)
    
    def get_absolute_url(self):
        return f'/yangilik/{self.slug}'
    
    def increment_views(self):
        self.views += 1
        db.session.commit()
    
    def __repr__(self):
        return f'<Post {self.title_uz}>'
