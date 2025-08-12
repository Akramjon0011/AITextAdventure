#!/usr/bin/env python3
from services.gemini_service import GeminiService
from models.post import Post
from models.user import User
from app import app, db

with app.app_context():
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@uzbeknews.ai')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin user yaratildi')
    
    gemini = GeminiService()
    
    # Technology news - Uzum unicorn success
    print("Texnologiya yangiligi yaratilmoqda...")
    tech_news = gemini.generate_news_content(
        topic='Ozbekiston texnologiya sohasi rivojlanishi - Uzum kompaniyasining 1 milliard dollar qiymatga erishishi',
        category='Texnologiya',
        region='Toshkent'
    )
    
    if tech_news:
        post = Post(
            title_uz=tech_news['title_uz'],
            title_ru=tech_news.get('title_ru', tech_news['title_uz']), 
            content_uz=tech_news['content_uz'],
            content_ru=tech_news.get('content_ru', tech_news['content_uz']),
            category='Texnologiya',
            region='Toshkent',
            author_id=admin.id,
            meta_title_uz=tech_news.get('meta_title', tech_news['title_uz']),
            meta_description_uz=tech_news.get('meta_description', ''),
            keywords=tech_news.get('keywords', ''),
            published=True
        )
        db.session.add(post)
        print(f'✓ Tech yangilik: {tech_news["title_uz"][:70]}')
        
    # Economy news - World Bank cooperation
    print("Iqtisodiyot yangiligi yaratilmoqda...")
    econ_news = gemini.generate_news_content(
        topic='Ozbekiston iqtisodiyoti 2025-yilda 5.9 foiz osish prognozi va Jahon Bank hamkorligi',
        category='Iqtisodiyot',
        region='Toshkent'
    )
    
    if econ_news:
        post = Post(
            title_uz=econ_news['title_uz'],
            title_ru=econ_news.get('title_ru', econ_news['title_uz']),
            content_uz=econ_news['content_uz'], 
            content_ru=econ_news.get('content_ru', econ_news['content_uz']),
            category='Iqtisodiyot',
            region='Toshkent',
            author_id=admin.id,
            meta_title_uz=econ_news.get('meta_title', econ_news['title_uz']),
            meta_description_uz=econ_news.get('meta_description', ''),
            keywords=econ_news.get('keywords', ''),
            published=True
        )
        db.session.add(post)
        print(f'✓ Iqtisod yangilik: {econ_news["title_uz"][:70]}')
    
    # Education success story
    print("Ta'lim yangiligi yaratilmoqda...")
    edu_news = gemini.generate_news_content(
        topic='Ozbekiston jamoasi Evropa Qizlar Informatika Olimpiadasida ikki bronza medal qolga kiritdi',
        category='Talim',
        region='Evropa'
    )
    
    if edu_news:
        post = Post(
            title_uz=edu_news['title_uz'],
            title_ru=edu_news.get('title_ru', edu_news['title_uz']),
            content_uz=edu_news['content_uz'],
            content_ru=edu_news.get('content_ru', edu_news['content_uz']),
            category='Talim',
            region='Evropa',
            author_id=admin.id,
            meta_title_uz=edu_news.get('meta_title', edu_news['title_uz']),
            meta_description_uz=edu_news.get('meta_description', ''),
            keywords=edu_news.get('keywords', ''),
            published=True
        )
        db.session.add(post)
        print(f'✓ Ta\'lim yangilik: {edu_news["title_uz"][:70]}')
    
    # Regional/Infrastructure news
    print("Hududiy yangilik yaratilmoqda...")
    infra_news = gemini.generate_news_content(
        topic='Ozbekiston-Afg\'oniston-Pokiston Trans-Afg\'on temir yol loyihasi va hududiy hamkorlik',
        category='Hududiy',
        region='Markaziy Osiyo'
    )
    
    if infra_news:
        post = Post(
            title_uz=infra_news['title_uz'],
            title_ru=infra_news.get('title_ru', infra_news['title_uz']),
            content_uz=infra_news['content_uz'],
            content_ru=infra_news.get('content_ru', infra_news['content_uz']),
            category='Hududiy',
            region='Markaziy Osiyo',
            author_id=admin.id,
            meta_title_uz=infra_news.get('meta_title', infra_news['title_uz']),
            meta_description_uz=infra_news.get('meta_description', ''),
            keywords=infra_news.get('keywords', ''),
            published=True
        )
        db.session.add(post)
        print(f'✓ Hududiy yangilik: {infra_news["title_uz"][:70]}')
    
    db.session.commit()
    posts_count = Post.query.count()
    print(f'\n🎉 Jami {posts_count} ta yangilik muvaffaqiyatli qo\'shildi!')
    
    # Show latest posts
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(4).all()
    print('\nSo\'nggi yangiliklar:')
    for i, post in enumerate(latest_posts, 1):
        print(f'{i}. {post.title_uz}')
        print(f'   Kategoriya: {post.category} | Hudud: {post.region}')
        print()