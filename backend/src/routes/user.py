from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.telegram_bot import telegram_bot, TELEGRAM_CHAT_ID
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_bp = Blueprint('user', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

@user_bp.route('/users/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'حقل {field} مطلوب'
                }), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        phone = data['phone'].strip()
        
        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'صيغة البريد الإلكتروني غير صحيحة'
            }), 400
        
        # Validate password strength
        if not validate_password(password):
            return jsonify({
                'success': False,
                'message': 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'البريد الإلكتروني مستخدم بالفعل'
            }), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user = User(
            username=name,
            email=email,
            password_hash=hashed_password,
            phone=phone
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Send Telegram notification for new user registration
        if telegram_bot and TELEGRAM_CHAT_ID != "YOUR_CHAT_ID_HERE":
            try:
                telegram_bot.send_user_registration_notification(TELEGRAM_CHAT_ID, {
                    'name': name,
                    'email': email,
                    'phone': phone
                })
            except Exception as e:
                print(f"Failed to send Telegram notification: {e}")
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء الحساب بنجاح',
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'phone': user.phone
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في إنشاء الحساب'
        }), 500

@user_bp.route('/users/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'البريد الإلكتروني وكلمة المرور مطلوبان'
            }), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({
                'success': False,
                'message': 'البريد الإلكتروني أو كلمة المرور غير صحيحة'
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'تم تسجيل الدخول بنجاح',
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'phone': user.phone
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في تسجيل الدخول'
        }), 500

@user_bp.route('/users/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'المستخدم غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'phone': user.phone,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في جلب بيانات المستخدم'
        }), 500

@user_bp.route('/users/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'المستخدم غير موجود'
            }), 404
        
        data = request.json
        
        # Update user fields
        if data.get('name'):
            user.username = data['name'].strip()
        
        if data.get('phone'):
            user.phone = data['phone'].strip()
        
        # Handle email update
        if data.get('email'):
            new_email = data['email'].strip().lower()
            if new_email != user.email:
                if not validate_email(new_email):
                    return jsonify({
                        'success': False,
                        'message': 'صيغة البريد الإلكتروني غير صحيحة'
                    }), 400
                
                # Check if email is already taken
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != user_id:
                    return jsonify({
                        'success': False,
                        'message': 'البريد الإلكتروني مستخدم بالفعل'
                    }), 400
                
                user.email = new_email
        
        # Handle password update
        if data.get('password'):
            new_password = data['password']
            if not validate_password(new_password):
                return jsonify({
                    'success': False,
                    'message': 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'
                }), 400
            
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم تحديث البيانات بنجاح',
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'phone': user.phone
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في تحديث البيانات'
        }), 500

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [{
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'phone': user.phone
            } for user in users]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في جلب المستخدمين'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'المستخدم غير موجود'
            }), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف المستخدم بنجاح'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في حذف المستخدم'
        }), 500

