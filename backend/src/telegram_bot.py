import requests
import json
from datetime import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, chat_id, text, parse_mode='HTML'):
        """Send a message to a Telegram chat"""
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def send_order_notification(self, chat_id, order_data):
        """Send order notification to Telegram"""
        customer_info = order_data.get('customer_info', {})
        items = order_data.get('items', [])
        total = order_data.get('total', 0)
        
        # Format order message
        message = f"""
🎮 <b>طلب جديد من متجر القيمنق!</b>

👤 <b>معلومات العميل:</b>
• الاسم: {customer_info.get('name', 'غير محدد')}
• البريد الإلكتروني: {customer_info.get('email', 'غير محدد')}
• رقم الهاتف: {customer_info.get('phone', 'غير محدد')}

🛒 <b>المنتجات المطلوبة:</b>
"""
        
        for item in items:
            message += f"• {item.get('name', 'منتج غير محدد')} - الكمية: {item.get('quantity', 1)} - السعر: {item.get('price', 0)} ريال\n"
        
        message += f"\n💰 <b>المجموع الكلي: {total} ريال</b>"
        message += f"\n📅 <b>وقت الطلب:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(chat_id, message)
    
    def send_contact_message(self, chat_id, contact_data):
        """Send contact form message to Telegram"""
        message = f"""
📞 <b>رسالة جديدة من موقع متجر القيمنق!</b>

👤 <b>معلومات المرسل:</b>
• الاسم: {contact_data.get('name', 'غير محدد')}
• البريد الإلكتروني: {contact_data.get('email', 'غير محدد')}
• رقم الهاتف: {contact_data.get('phone', 'غير محدد')}

💬 <b>الرسالة:</b>
{contact_data.get('message', 'لا توجد رسالة')}

📅 <b>وقت الإرسال:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(chat_id, message)
    
    def send_user_registration_notification(self, chat_id, user_data):
        """Send new user registration notification"""
        message = f"""
🆕 <b>مستخدم جديد في متجر القيمنق!</b>

👤 <b>معلومات المستخدم:</b>
• الاسم: {user_data.get('name', 'غير محدد')}
• البريد الإلكتروني: {user_data.get('email', 'غير محدد')}
• رقم الهاتف: {user_data.get('phone', 'غير محدد')}

📅 <b>تاريخ التسجيل:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(chat_id, message)

# Configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Replace with your chat ID

# Initialize bot instance
telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE" else None

