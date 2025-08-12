import os
import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime
import pytz

class TelegramService:
    def __init__(self):
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.environ.get('TELEGRAM_CHANNEL_ID')
        self.bot = Bot(token=self.bot_token) if self.bot_token else None
        self.tashkent_tz = pytz.timezone('Asia/Tashkent')
    
    async def send_news_post(self, post, base_url="http://localhost:5000"):
        """Send news post to Telegram channel"""
        if not self.bot or not self.channel_id:
            logging.error("Telegram bot or channel not configured")
            return False
        
        try:
            # Format message
            message = self._format_message(post, base_url)
            
            # Send message
            sent_message = await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
            logging.info(f"Message sent to Telegram: {sent_message.message_id}")
            return True
            
        except TelegramError as e:
            logging.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logging.error(f"Error sending to Telegram: {e}")
            return False
    
    def _format_message(self, post, base_url):
        """Format post for Telegram"""
        # Use Uzbek content
        title = post.title_uz
        
        # Get summary from content
        summary = post.content_uz[:200] + "..." if len(post.content_uz) > 200 else post.content_uz
        
        # Get current time in Tashkent
        now = datetime.now(self.tashkent_tz)
        time_str = now.strftime("%d-%B, %H:%M")
        
        # Format category
        category_emoji = self._get_category_emoji(post.category)
        
        # Create message
        message = f"""
{category_emoji} <b>{title}</b>

{summary}

📅 {time_str}
🏷️ #{post.category.replace(" ", "").replace("'", "")}

<a href="{base_url}{post.get_absolute_url()}">📖 To'liq maqolani o'qish uchun...</a>

#UzbekNews #Uzbekistan #Yangiliklar
        """.strip()
        
        return message
    
    def _get_category_emoji(self, category):
        """Get emoji for category"""
        emoji_map = {
            "O'zbekiston yangiliklar": "🇺🇿",
            "Texnologiya": "💻",
            "Iqtisodiyot": "📈",
            "Sport": "⚽",
            "Madaniyat": "🎭",
            "Ta'lim": "📚",
            "Sog'liqni saqlash": "🏥",
            "Markaziy Osiyodagi yangiliklar": "🌍",
            "Jahon yangiliklar": "🌐"
        }
        return emoji_map.get(category, "📰")
    
    def send_news_sync(self, post, base_url="http://localhost:5000"):
        """Synchronous wrapper for sending news"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an event loop, create a new thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.send_news_post(post, base_url))
                    return future.result()
            else:
                return asyncio.run(self.send_news_post(post, base_url))
        except Exception as e:
            logging.error(f"Error in sync telegram send: {e}")
            return False
    
    async def get_channel_info(self):
        """Get information about the Telegram channel"""
        if not self.bot or not self.channel_id:
            return None
        
        try:
            chat = await self.bot.get_chat(chat_id=self.channel_id)
            return {
                'title': chat.title,
                'username': chat.username,
                'member_count': await self.bot.get_chat_member_count(chat_id=self.channel_id)
            }
        except Exception as e:
            logging.error(f"Error getting channel info: {e}")
            return None
