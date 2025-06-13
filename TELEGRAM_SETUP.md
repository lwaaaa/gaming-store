# إعداد Telegram Bot لمتجر القيمنق

## نظرة عامة

يستخدم متجر القيمنق Telegram Bot لإرسال إشعارات فورية عن:
- الطلبات الجديدة
- تسجيل المستخدمين الجدد
- رسائل التواصل من العملاء

## خطوات الإعداد

### 1. إنشاء البوت

1. **افتح تطبيق Telegram**
2. **ابحث عن BotFather**: `@BotFather`
3. **ابدأ محادثة** واضغط "Start"
4. **أرسل الأمر**: `/newbot`
5. **اختر اسم البوت**: مثل "متجر القيمنق"
6. **اختر معرف البوت**: مثل `gaming_store_notifications_bot`
7. **احفظ الرمز المميز** الذي سيرسله BotFather

### 2. الحصول على Chat ID

#### الطريقة الأولى: استخدام API
1. **أرسل رسالة للبوت** (أي رسالة)
2. **افتح الرابط التالي** في المتصفح:
   ```
   https://api.telegram.org/bot[YOUR_BOT_TOKEN]/getUpdates
   ```
   (استبدل `[YOUR_BOT_TOKEN]` برمز البوت الخاص بك)
3. **ابحث عن**: `"chat":{"id":`
4. **احفظ الرقم** الذي يأتي بعدها

#### الطريقة الثانية: استخدام بوت مساعد
1. **ابحث عن**: `@userinfobot`
2. **أرسل**: `/start`
3. **احفظ Chat ID** الذي سيظهر

### 3. تكوين المشروع

1. **افتح ملف**: `backend/src/telegram_bot.py`
2. **استبدل القيم**:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_ACTUAL_BOT_TOKEN_HERE"
   TELEGRAM_CHAT_ID = "YOUR_ACTUAL_CHAT_ID_HERE"
   ```

### 4. اختبار الإعداد

```python
# في terminal أو Python console
from src.telegram_bot import telegram_bot, TELEGRAM_CHAT_ID

# إرسال رسالة تجريبية
result = telegram_bot.send_message(TELEGRAM_CHAT_ID, "🎮 مرحباً من متجر القيمنق!")
print(result)
```

## أنواع الإشعارات

### 1. إشعار طلب جديد
```
🎮 طلب جديد من متجر القيمنق!

👤 معلومات العميل:
• الاسم: أحمد محمد
• البريد الإلكتروني: ahmed@example.com
• رقم الهاتف: +966501234567

🛒 المنتجات المطلوبة:
• FIFA 2024 - الكمية: 1 - السعر: 299 ريال
• يد تحكم PS5 - الكمية: 2 - السعر: 350 ريال

💰 المجموع الكلي: 999 ريال
📅 وقت الطلب: 2024-01-15 14:30:25
```

### 2. إشعار مستخدم جديد
```
🆕 مستخدم جديد في متجر القيمنق!

👤 معلومات المستخدم:
• الاسم: سارة أحمد
• البريد الإلكتروني: sara@example.com
• رقم الهاتف: +966507654321

📅 تاريخ التسجيل: 2024-01-15 14:25:10
```

### 3. إشعار رسالة تواصل
```
📞 رسالة جديدة من موقع متجر القيمنق!

👤 معلومات المرسل:
• الاسم: خالد عبدالله
• البريد الإلكتروني: khalid@example.com
• رقم الهاتف: +966509876543

💬 الرسالة:
أريد الاستفسار عن توفر لعبة Call of Duty الجديدة

📅 وقت الإرسال: 2024-01-15 15:45:30
```

## استكشاف الأخطاء

### مشكلة: البوت لا يرسل رسائل

**الحلول المحتملة:**

1. **تحقق من الرمز المميز**:
   ```python
   import requests
   token = "YOUR_BOT_TOKEN"
   url = f"https://api.telegram.org/bot{token}/getMe"
   response = requests.get(url)
   print(response.json())
   ```

2. **تحقق من Chat ID**:
   ```python
   import requests
   token = "YOUR_BOT_TOKEN"
   url = f"https://api.telegram.org/bot{token}/getUpdates"
   response = requests.get(url)
   print(response.json())
   ```

3. **تحقق من الاتصال**:
   ```python
   from src.telegram_bot import telegram_bot
   result = telegram_bot.send_message("YOUR_CHAT_ID", "اختبار")
   print(result)
   ```

### مشكلة: خطأ 401 Unauthorized

- **السبب**: رمز البوت غير صحيح
- **الحل**: تأكد من نسخ الرمز كاملاً من BotFather

### مشكلة: خطأ 400 Bad Request

- **السبب**: Chat ID غير صحيح
- **الحل**: تأكد من Chat ID وأنك أرسلت رسالة للبوت أولاً

## الأمان

### حماية الرموز المميزة

1. **لا تشارك** رمز البوت مع أحد
2. **استخدم متغيرات البيئة** في الإنتاج:
   ```python
   import os
   TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
   TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
   ```

3. **أضف إلى .gitignore**:
   ```
   .env
   config.py
   ```

### تقييد الوصول

1. **استخدم Chat ID محدد** بدلاً من السماح لأي شخص
2. **فعّل Privacy Mode** في إعدادات البوت
3. **راقب الرسائل** الواردة للبوت

## التطوير المتقدم

### إضافة أوامر للبوت

```python
def handle_commands(update):
    """معالجة أوامر البوت"""
    if update.get('message', {}).get('text') == '/stats':
        # إرسال إحصائيات المتجر
        stats = get_store_stats()
        send_stats_message(stats)
    
    elif update.get('message', {}).get('text') == '/orders':
        # إرسال آخر الطلبات
        recent_orders = get_recent_orders()
        send_orders_summary(recent_orders)
```

### تنسيق الرسائل المتقدم

```python
def format_order_message(order):
    """تنسيق رسالة الطلب مع تنسيق متقدم"""
    message = f"""
🎮 <b>طلب جديد #{order['id']}</b>

👤 <b>العميل:</b>
├ 📝 {order['customer_name']}
├ 📧 {order['customer_email']}
└ 📱 {order['customer_phone']}

🛒 <b>المنتجات:</b>
"""
    
    for item in order['items']:
        message += f"├ {item['name']} × {item['quantity']}\n"
        message += f"└ 💰 {item['price']} ريال\n\n"
    
    message += f"💳 <b>المجموع:</b> {order['total']} ريال"
    
    return message
```

## الدعم

إذا واجهت أي مشاكل في إعداد Telegram Bot:

1. **راجع الوثائق الرسمية**: [Telegram Bot API](https://core.telegram.org/bots/api)
2. **تحقق من الأمثلة**: في مجلد `examples/`
3. **اتصل بالدعم**: عبر GitHub Issues

---

*آخر تحديث: يناير 2024*

