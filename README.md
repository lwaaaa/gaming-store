
# متجر القيمنق

هذا المشروع عبارة عن متجر إلكتروني للألعاب والإكسسوارات، مبني باستخدام Flask للواجهة الخلفية (Backend) و HTML/CSS/JavaScript للواجهة الأمامية (Frontend).

## هيكل المشروع

```
gaming_store_project/
├── backend/                # مجلد الواجهة الخلفية (Flask)
│   ├── src/
│   │   ├── main.py         # نقطة الدخول الرئيسية لتطبيق Flask
│   │   ├── models/         # ملفات نماذج قاعدة البيانات
│   │   ├── routes/         # ملفات الـ APIs (games, accessories, orders, user)
│   │   └── static/         # ملفات الواجهة الأمامية التي يتم تقديمها بواسطة Flask
│   ├── venv/               # البيئة الافتراضية
│   ├── requirements.txt    # متطلبات Python
│   └── Procfile            # لـ Render deployment
├── frontend/               # مجلد الواجهة الأمامية (HTML/CSS/JS)
│   ├── index.html          # الصفحة الرئيسية
│   ├── styles.css          # ملف الأنماط CSS
│   └── script.js           # ملف JavaScript
├── .env                    # متغيرات البيئة
└── render.yaml             # ملف إعدادات النشر على Render
```

## خطوات النشر على Render (تلقائي عبر GitHub Actions)

تم إعداد هذا المشروع للنشر التلقائي على Render باستخدام GitHub Actions. عند كل عملية `push` إلى الفرع الرئيسي (`main`) في GitHub، سيتم تشغيل سير عمل (workflow) يقوم بنشر التغييرات تلقائيًا.

### المتطلبات المسبقة

1.  **حساب GitHub**: يجب أن يكون لديك حساب GitHub.
2.  **حساب Render**: يجب أن يكون لديك حساب Render.
3.  **ربط GitHub بـ Render**: تأكد من ربط حساب GitHub الخاص بك بـ Render للسماح بالنشر التلقائي.

### الإعداد الأولي (مرة واحدة فقط)

1.  **إنشاء Repository على GitHub**: قم بإنشاء مستودع جديد على GitHub (إذا لم تكن قد فعلت ذلك بالفعل) وقم بربط هذا المشروع به.

    ```bash
    git init
    git add .
    git commit -m "Initial commit: Gaming Store Project"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/gaming-store.git # استبدل YOUR_USERNAME
    git push -u origin main
    ```

2.  **إعداد Render Web Service**: 
    *   اذهب إلى لوحة تحكم Render.
    *   انقر على `New Web Service`.
    *   اختر المستودع `gaming-store` من GitHub.
    *   قم بتكوين الخدمة كالتالي:
        *   **Name**: `gaming-store-backend`
        *   **Root Directory**: `backend`
        *   **Runtime**: `Python 3`
        *   **Build Command**: `pip install -r requirements.txt`
        *   **Start Command**: `gunicorn src.main:app`
        *   **Environment Variables**: أضف `SECRET_KEY` (يمكنك توليد قيمة عشوائية) و `FLASK_APP=src/main.py` و `FLASK_ENV=production`.
    *   انقر على `Create Web Service`.

3.  **إعداد Render Static Site**: 
    *   اذهب إلى لوحة تحكم Render.
    *   انقر على `New Static Site`.
    *   اختر المستودع `gaming-store` من GitHub.
    *   قم بتكوين الموقع كالتالي:
        *   **Name**: `gaming-store-frontend`
        *   **Root Directory**: `frontend`
        *   **Build Command**: `echo 'No build command for static site'`
        *   **Publish Directory**: `.` (أو `frontend` إذا كنت تستخدم مجلد فرعي)
    *   انقر على `Create Static Site`.

### النشر التلقائي

بعد الإعداد الأولي، كل ما عليك فعله هو دفع التغييرات إلى الفرع الرئيسي (`main`) في GitHub:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

سيقوم GitHub Actions تلقائيًا بتشغيل سير العمل المحدد في `.github/workflows/deploy.yml`، والذي بدوره سيقوم بتحديث ونشر الواجهة الخلفية والواجهة الأمامية على Render.

## التطوير المحلي

### الواجهة الخلفية (Backend)

1.  انتقل إلى مجلد `backend`:
    ```bash
    cd backend
    ```
2.  أنشئ بيئة افتراضية وقم بتنشيطها:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  ثبت المتطلبات:
    ```bash
    pip install -r requirements.txt
    ```
4.  شغل التطبيق:
    ```bash
    python src/main.py
    ```
    سيتم تشغيل التطبيق على `http://127.0.0.1:5000`.

### الواجهة الأمامية (Frontend)

الواجهة الأمامية هي ملفات HTML/CSS/JS ثابتة. يمكنك فتح `frontend/index.html` مباشرة في متصفحك أو استخدام خادم ويب بسيط (مثل `python3 -m http.server` من مجلد `frontend`) لعرضها.

## API Endpoints (الواجهة الخلفية)

*   `/api/health`: فحص حالة الـ API.
*   `/api/games`: جلب قائمة الألعاب.
*   `/api/games/<id>`: جلب تفاصيل لعبة معينة.
*   `/api/accessories`: جلب قائمة الإكسسوارات.
*   `/api/accessories/<id>`: جلب تفاصيل إكسسوار معين.
*   `/api/orders` (POST): إنشاء طلب جديد.
*   `/api/orders` (GET): جلب قائمة الطلبات (للاستخدام الإداري).
*   `/api/orders/<id>`: جلب تفاصيل طلب معين.
*   `/api/orders/<id>/status` (PUT): تحديث حالة الطلب.

## ملاحظات

*   تم استخدام قاعدة بيانات SQLite بسيطة للتطوير المحلي. للنشر على Render، يفضل استخدام قاعدة بيانات خارجية مثل PostgreSQL.
*   ملف `render.yaml` يحدد كيفية نشر كل من الواجهة الخلفية والواجهة الأمامية كخدمات منفصلة على Render.
*   ملف `.github/workflows/deploy.yml` (سيتم إنشاؤه لاحقًا) سيقوم بأتمتة عملية النشر.


