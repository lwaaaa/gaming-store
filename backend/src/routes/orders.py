from flask import Blueprint, jsonify, request
from datetime import datetime
from src.models.user import db
from src.telegram_bot import telegram_bot, TELEGRAM_CHAT_ID

orders_bp = Blueprint('orders', __name__)

# In-memory storage for orders (in production, use database)
ORDERS_DATA = []
ORDER_COUNTER = 1

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    global ORDER_COUNTER
    
    try:
        data = request.get_json()
        
        # Extract customer info and items
        customer_info = data.get('customer_info', {})
        items = data.get('items', [])
        total = data.get('total', 0)
        user_id = data.get('user_id')
        
        # Validate required fields
        if not customer_info.get('name'):
            return jsonify({
                'success': False,
                'message': 'اسم العميل مطلوب'
            }), 400
        
        if not customer_info.get('email'):
            return jsonify({
                'success': False,
                'message': 'البريد الإلكتروني مطلوب'
            }), 400
        
        if not customer_info.get('phone'):
            return jsonify({
                'success': False,
                'message': 'رقم الهاتف مطلوب'
            }), 400
        
        if not items or len(items) == 0:
            return jsonify({
                'success': False,
                'message': 'يجب أن يحتوي الطلب على منتج واحد على الأقل'
            }), 400
        
        if total <= 0:
            return jsonify({
                'success': False,
                'message': 'المبلغ الإجمالي يجب أن يكون أكبر من صفر'
            }), 400
        
        # Create order
        order = {
            'id': ORDER_COUNTER,
            'order_number': f'GO-{ORDER_COUNTER:06d}',
            'user_id': user_id,
            'customer_name': customer_info['name'],
            'customer_email': customer_info['email'],
            'customer_phone': customer_info['phone'],
            'customer_address': customer_info.get('address', ''),
            'items': items,
            'total_amount': total,
            'status': 'pending',
            'payment_method': data.get('payment_method', 'cash_on_delivery'),
            'notes': data.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        ORDERS_DATA.append(order)
        ORDER_COUNTER += 1
        
        # Send Telegram notification
        if telegram_bot and TELEGRAM_CHAT_ID != "YOUR_CHAT_ID_HERE":
            try:
                telegram_bot.send_order_notification(TELEGRAM_CHAT_ID, {
                    'customer_info': customer_info,
                    'items': items,
                    'total': total,
                    'order_number': order['order_number']
                })
            except Exception as e:
                print(f"Failed to send Telegram notification: {e}")
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء الطلب بنجاح',
            'order': order
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في إنشاء الطلب: {str(e)}'
        }), 500

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders (admin endpoint)"""
    status_filter = request.args.get('status')
    user_id = request.args.get('user_id')
    
    orders = ORDERS_DATA.copy()
    
    if status_filter:
        orders = [order for order in orders if order['status'] == status_filter]
    
    if user_id:
        orders = [order for order in orders if order.get('user_id') == int(user_id)]
    
    # Sort by creation date (newest first)
    orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        'success': True,
        'orders': orders,
        'total': len(orders)
    })

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order by ID"""
    order = next((order for order in ORDERS_DATA if order['id'] == order_id), None)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'الطلب غير موجود'
        }), 404
    
    return jsonify({
        'success': True,
        'order': order
    })

@orders_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                'success': False,
                'message': 'حالة الطلب مطلوبة'
            }), 400
        
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'حالة غير صحيحة. الحالات المتاحة: {", ".join(valid_statuses)}'
            }), 400
        
        order = next((order for order in ORDERS_DATA if order['id'] == order_id), None)
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'الطلب غير موجود'
            }), 404
        
        order['status'] = new_status
        order['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'تم تحديث حالة الطلب بنجاح',
            'order': order
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في تحديث حالة الطلب: {str(e)}'
        }), 500

@orders_bp.route('/orders/search', methods=['GET'])
def search_orders():
    """Search orders by order number or customer name"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'استعلام البحث مطلوب'
        }), 400
    
    results = [
        order for order in ORDERS_DATA 
        if (query in order['order_number'].lower() or 
            query in order['customer_name'].lower() or
            query in order['customer_email'].lower())
    ]
    
    return jsonify({
        'success': True,
        'results': results,
        'total': len(results)
    })

@orders_bp.route('/orders/stats', methods=['GET'])
def get_order_stats():
    """Get order statistics"""
    total_orders = len(ORDERS_DATA)
    
    status_counts = {}
    total_revenue = 0
    
    for order in ORDERS_DATA:
        status = order['status']
        status_counts[status] = status_counts.get(status, 0) + 1
        
        if order['status'] in ['confirmed', 'processing', 'shipped', 'delivered']:
            total_revenue += order['total_amount']
    
    return jsonify({
        'success': True,
        'stats': {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'status_breakdown': status_counts,
            'average_order_value': total_revenue / max(total_orders, 1)
        }
    })

@orders_bp.route('/contact', methods=['POST'])
def contact_form():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'حقل {field} مطلوب'
                }), 400
        
        contact_data = {
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone', ''),
            'message': data['message'],
            'created_at': datetime.now().isoformat()
        }
        
        # Send Telegram notification
        if telegram_bot and TELEGRAM_CHAT_ID != "YOUR_CHAT_ID_HERE":
            try:
                telegram_bot.send_contact_message(TELEGRAM_CHAT_ID, contact_data)
            except Exception as e:
                print(f"Failed to send Telegram notification: {e}")
        
        return jsonify({
            'success': True,
            'message': 'تم إرسال رسالتك بنجاح. سنتواصل معك قريباً!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في إرسال الرسالة: {str(e)}'
        }), 500

