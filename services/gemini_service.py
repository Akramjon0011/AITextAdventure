import os
import logging
from google import genai
from google.genai import types

class GeminiService:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.available = True
            except Exception as e:
                logging.warning(f"Failed to initialize Gemini client: {e}")
                self.client = None
                self.available = False
        else:
            logging.warning("GEMINI_API_KEY not found. Gemini service will be disabled.")
            self.client = None
            self.available = False
        
        self.model = "gemini-2.5-flash"
        
        # Uzbek content prompts
        self.UZBEK_NEWS_PROMPT = """
        O'zbek auditoriya uchun {topic} mavzusida yangilik maqolasi yozing.
        
        TALABLAR:
        - Tili: O'zbek tili (lotin yozuvi)
        - Hajmi: 600-1000 so'z
        - Uslubi: Rasmiy yangilik uslubi
        - Mazmuni: O'zbekiston va Markaziy Osiyoga tegishli
        - SEO: Kalit so'zlar: {keywords}
        
        STRUKTURA:
        - Qiziqarli sarlavha (45-55 belgi)
        - Kirish qismi (lead paragraph)
        - Asosiy mazmun (3-4 paragraf)
        - Xulosa va kelgusi rejalar
        
        O'zbek mentaliteti va madaniyatini hisobga oling. Oilaviy va ma'rifiy kontent yarating.
        Javobni JSON formatida bering:
        {{
            "title": "Sarlavha",
            "content": "To'liq mazmun",
            "meta_title": "SEO sarlavha",
            "meta_description": "SEO tavsif",
            "keywords": "kalit so'zlar"
        }}
        """
        
        self.TELEGRAM_UZ_PROMPT = """
        {title} haqida qisqa Telegram posti yozing.
        
        FORMAT:
        - 150-250 so'z
        - O'zbek tilida
        - 2-3 emoji
        - #uzbekistan #yangiliklar kabi hashtag
        - "To'liq maqolani o'qish uchun: [link]"
        
        Mazmun: {content_preview}
        """
        
        self.RUSSIAN_TRANSLATION_PROMPT = """
        Quyidagi o'zbek tilidagi yangilik maqolasini rus tiliga tarjima qiling:
        
        Sarlavha: {title_uz}
        Mazmun: {content_uz}
        
        TALABLAR:
        - Tabiiy rus tili
        - Yangilik uslubi
        - Ma'noni to'liq saqlab qolish
        
        Javobni JSON formatida bering:
        {{
            "title_ru": "Rus tilidagi sarlavha",
            "content_ru": "Rus tilidagi mazmun"
        }}
        """
    
    def generate_uzbek_news(self, topic, keywords=""):
        """Generate news article in Uzbek language"""
        if not self.available:
            logging.error("Gemini service not available. Please set GEMINI_API_KEY environment variable.")
            return None
            
        try:
            prompt = self.UZBEK_NEWS_PROMPT.format(topic=topic, keywords=keywords)
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                import json
                return json.loads(response.text)
            else:
                raise Exception("Empty response from Gemini")
                
        except Exception as e:
            logging.error(f"Error generating Uzbek news: {e}")
            return None
    
    def generate_telegram_post(self, title, content_preview):
        """Generate Telegram post in Uzbek"""
        if not self.available:
            logging.error("Gemini service not available. Please set GEMINI_API_KEY environment variable.")
            return ""
            
        try:
            prompt = self.TELEGRAM_UZ_PROMPT.format(
                title=title,
                content_preview=content_preview[:200]
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text if response.text else ""
            
        except Exception as e:
            logging.error(f"Error generating Telegram post: {e}")
            return ""
    
    def translate_to_russian(self, title_uz, content_uz):
        """Translate Uzbek content to Russian"""
        if not self.available:
            logging.error("Gemini service not available. Please set GEMINI_API_KEY environment variable.")
            return None
            
        try:
            prompt = self.RUSSIAN_TRANSLATION_PROMPT.format(
                title_uz=title_uz,
                content_uz=content_uz
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                import json
                return json.loads(response.text)
            else:
                return {"title_ru": "", "content_ru": ""}
                
        except Exception as e:
            logging.error(f"Error translating to Russian: {e}")
            return {"title_ru": "", "content_ru": ""}
    
    def summarize_content(self, content, language="uz"):
        """Summarize content for preview"""
        if not self.available:
            logging.error("Gemini service not available. Please set GEMINI_API_KEY environment variable.")
            return content[:200]
            
        try:
            if language == "uz":
                prompt = f"Quyidagi matnni qisqacha xulosalang (100-150 so'z): {content[:500]}"
            else:
                prompt = f"Summarize the following text briefly (100-150 words): {content[:500]}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text if response.text else content[:200]
            
        except Exception as e:
            logging.error(f"Error summarizing content: {e}")
            return content[:200]
    
    def generate_news_content(self, topic, category, region):
        """Generate comprehensive news content based on topic"""
        if not self.available:
            logging.error("Gemini service not available. Please set GEMINI_API_KEY environment variable.")
            return None
            
        try:
            prompt = f"""
            Quyidagi mavzu bo'yicha haqiqiy va dolzarb yangilik maqolasi yarating:
            
            Mavzu: {topic}
            Kategoriya: {category}  
            Hudud: {region}
            
            TALABLAR:
            - Haqiqiy ma'lumotlarga asoslaning
            - Professional jurnalistik uslub
            - O'zbek va rus tillarida
            - SEO optimizatsiyasi
            
            JSON formatda javob bering:
            {{
                "title_uz": "Jozibali o'zbek tilidagi sarlavha",
                "title_ru": "Привлекательный заголовок на русском",  
                "content_uz": "To'liq o'zbek tilidagi matn (300-400 so'z)",
                "content_ru": "Полный текст на русском языке",
                "meta_title": "SEO uchun meta sarlavha",
                "meta_description": "Qisqa tavsif SEO uchun", 
                "keywords": "kalit so'zlar, vergul bilan"
            }}
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                import json
                return json.loads(response.text)
            return None
            
        except Exception as e:
            logging.error(f"Error generating news content: {e}")
            return None
