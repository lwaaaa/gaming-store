from flask import Blueprint, jsonify, request
from datetime import datetime
from src.models.user import db

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
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'customer_phone', 'items', 'total_amount']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Validate items
        if not data['items'] or len(data['items']) == 0:
            return jsonify({
                'success': False,
                'message': 'Order must contain at least one item'
            }), 400
        
        # Create order
        order = {
            'id': ORDER_COUNTER,
            'order_number': f'GO-{ORDER_COUNTER:06d}',
            'customer_name': data['customer_name'],
            'customer_email': data['customer_email'],
            'customer_phone': data['customer_phone'],
            'customer_address': data.get('customer_address', ''),
            'items': data['items'],
            'total_amount': data['total_amount'],
            'status': 'pending',
            'payment_method': data.get('payment_method', 'cash_on_delivery'),
            'notes': data.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        ORDERS_DATA.append(order)
        ORDER_COUNTER += 1
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': order
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating order: {str(e)}'
        }), 500

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders (admin endpoint)"""
    status_filter = request.args.get('status')
    
    orders = ORDERS_DATA.copy()
    
    if status_filter:
        orders = [order for order in orders if order['status'] == status_filter]
    
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
            'message': 'Order not found'
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
                'message': 'Status is required'
            }), 400
        
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Valid statuses: {", ".join(valid_statuses)}'
            }), 400
        
        order = next((order for order in ORDERS_DATA if order['id'] == order_id), None)
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        order['status'] = new_status
        order['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Order status updated successfully',
            'order': order
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating order status: {str(e)}'
        }), 500

@orders_bp.route('/orders/search', methods=['GET'])
def search_orders():
    """Search orders by order number or customer name"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Search query is required'
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

@orders_bp.route('/orders/validate', methods=['POST'])
def validate_order():
    """Validate order data before submission"""
    try:
        data = request.get_json()
        
        errors = []
        
        # Validate customer info
        if not data.get('customer_name'):
            errors.append('Customer name is required')
        
        if not data.get('customer_email'):
            errors.append('Customer email is required')
        elif '@' not in data['customer_email']:
            errors.append('Invalid email format')
        
        if not data.get('customer_phone'):
            errors.append('Customer phone is required')
        
        # Validate items
        if not data.get('items') or len(data['items']) == 0:
            errors.append('Order must contain at least one item')
        
        # Validate total amount
        if not data.get('total_amount') or data['total_amount'] <= 0:
            errors.append('Total amount must be greater than 0')
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Order data is valid'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Validation error: {str(e)}'
        }), 500

