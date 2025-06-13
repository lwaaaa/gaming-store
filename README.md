# متجر القيمنق - Gaming Store

## 🎮 نظرة عامة

متجر القيمنق هو منصة تجارة إلكترونية احترافية مصممة خصيصاً لبيع الألعاب الإلكترونية وإكسسوارات الألعاب. يتميز بتصميم عصري وواجهة مستخدم سهلة الاستخدام مع دعم كامل للغة العربية.

## ✨ الميزات الرئيسية

- 🎯 **واجهة عربية كاملة** - دعم اتجاه النص من اليمين إلى اليسار
- 📱 **تصميم متجاوب** - يعمل على جميع الأجهزة
- 🔐 **نظام مستخدمين آمن** - تسجيل دخول وإنشاء حسابات
- 🛒 **سلة تسوق ذكية** - حفظ المنتجات محلياً
- 📦 **إدارة الطلبات** - تتبع حالة الطلبات
- 🤖 **تكامل Telegram** - إشعارات فورية للطلبات الجديدة
- 🎨 **صور منتجات عالية الجودة** - عرض جذاب للألعاب

## 🚀 الرابط المباشر

**الموقع متاح على:** [https://gaming-store-00fk.onrender.com](https://gaming-store-00fk.onrender.com)

## 🛠️ التقنيات المستخدمة

### Frontend
- HTML5 & CSS3
- JavaScript (Vanilla)
- Google Fonts (Cairo)
- Responsive Design

### Backend
- Python Flask
- SQLAlchemy (قاعدة البيانات)
- Flask-CORS
- Werkzeug (تشفير كلمات المرور)

### التكامل الخارجي
- Telegram Bot API
- Render (النشر السحابي)
- GitHub Actions (النشر التلقائي)

## 📁 هيكل المشروع

```
gaming-store/
├── backend/
│   ├── src/
│   │   ├── main.py              # الملف الرئيسي للخادم
│   │   ├── telegram_bot.py      # تكامل Telegram
│   │   ├── models/
│   │   │   └── user.py          # نموذج المستخدمين
│   │   ├── routes/
│   │   │   ├── user.py          # مسارات المستخدمين
│   │   │   ├── games.py         # مسارات الألعاب
│   │   │   ├── accessories.py   # مسارات الإكسسوارات
│   │   │   └── orders.py        # مسارات الطلبات
│   │   └── static/
│   │       ├── index.html       # الصفحة الرئيسية
│   │       ├── styles.css       # ملف التصميم
│   │       ├── script.js        # ملف JavaScript
│   │       └── *.jpg           # صور المنتجات
│   ├── requirements.txt         # متطلبات Python
│   └── Procfile                # إعدادات Render
├── frontend/                   # ملفات الواجهة الأمامية
├── .github/workflows/
│   └── deploy.yml              # GitHub Actions
├── render.yaml                 # إعدادات النشر
├── .env                       # متغيرات البيئة
├── README.md                  # هذا الملف
└── SETUP_GUIDE.md            # دليل الإعداد التفصيلي
```

## 🔧 التثبيت والتشغيل المحلي

### المتطلبات
- Python 3.8+
- pip
- Git

### خطوات التثبيت

1. **استنساخ المشروع**
```bash
git clone https://github.com/lwaaaa/gaming-store.git
cd gaming-store
```

2. **إعداد البيئة الافتراضية**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows
```

3. **تثبيت المتطلبات**
```bash
pip install -r requirements.txt
```

4. **تشغيل الخادم**
```bash
python src/main.py
```

5. **فتح المتصفح**
```
http://localhost:5000
```

## 🤖 إعداد Telegram Bot

### إنشاء البوت

1. ابحث عن `@BotFather` في Telegram
2. أرسل `/newbot`
3. اتبع التعليمات لإنشاء البوت
4. احفظ الرمز المميز (Token)

### الحصول على Chat ID

1. أرسل رسالة للبوت
2. زر الرابط: `https://api.telegram.org/bot[TOKEN]/getUpdates`
3. ابحث عن `"chat":{"id":` واحفظ الرقم

### تكوين المشروع

في ملف `backend/src/telegram_bot.py`:
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
```

## 🌐 النشر على Render

### الإعداد التلقائي

المشروع مُعد للنشر التلقائي على Render:

1. **إنشاء حساب** على [render.com](https://render.com)
2. **ربط GitHub** مع حسابك
3. **إنشاء Web Service** جديد
4. **اختيار المستودع** gaming-store
5. **تكوين الإعدادات**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.main:app`
   - Root Directory: `backend`

### GitHub Actions

يتم النشر تلقائياً عند كل `git push` إلى الفرع الرئيسي.

## 📊 واجهة برمجة التطبيقات (API)

### المستخدمين
- `POST /api/users/register` - تسجيل مستخدم جديد
- `POST /api/users/login` - تسجيل الدخول
- `GET /api/users/profile/<id>` - جلب الملف الشخصي
- `PUT /api/users/profile/<id>` - تحديث الملف الشخصي

### الألعاب
- `GET /api/games` - جلب جميع الألعاب
- `GET /api/games/<id>` - جلب لعبة محددة
- `GET /api/games/categories` - جلب التصنيفات
- `GET /api/games/search?q=<query>` - البحث في الألعاب

### الإكسسوارات
- `GET /api/accessories` - جلب جميع الإكسسوارات
- `GET /api/accessories/<id>` - جلب إكسسوار محدد
- `GET /api/accessories/categories` - جلب التصنيفات

### الطلبات
- `POST /api/orders` - إنشاء طلب جديد
- `GET /api/orders` - جلب جميع الطلبات
- `GET /api/orders/<id>` - جلب طلب محدد
- `PUT /api/orders/<id>/status` - تحديث حالة الطلب

## 🔒 الأمان

- تشفير كلمات المرور باستخدام Werkzeug
- التحقق من صحة البيانات المدخلة
- حماية من هجمات SQL Injection
- CORS مُفعل للتطوير الآمن

## 🐛 استكشاف الأخطاء

### مشاكل شائعة

1. **خطأ 500**: تحقق من سجلات الخادم
2. **مشاكل Telegram**: تأكد من صحة Token و Chat ID
3. **مشاكل قاعدة البيانات**: تأكد من إنشاء الجداول

### الحلول

```bash
# إعادة تشغيل الخادم
python src/main.py

# فحص السجلات
tail -f logs/app.log

# إعادة إنشاء قاعدة البيانات
rm database/app.db
python src/main.py
```

## 📈 الميزات المستقبلية

- [ ] نظام دفع إلكتروني
- [ ] تقييمات ومراجعات المنتجات
- [ ] نظام كوبونات الخصم
- [ ] تطبيق جوال
- [ ] لوحة تحكم إدارية متقدمة
- [ ] تكامل مع منصات التواصل الاجتماعي

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. عمل Fork للمشروع
2. إنشاء فرع جديد للميزة
3. إجراء التغييرات
4. إرسال Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 📞 التواصل

- **GitHub**: [lwaaaa/gaming-store](https://github.com/lwaaaa/gaming-store)
- **الموقع**: [https://gaming-store-00fk.onrender.com](https://gaming-store-00fk.onrender.com)
- **البريد الإلكتروني**: support@gaming-store.com

---

**تم تطوير هذا المشروع بواسطة فريق متجر القيمنق** 🎮

