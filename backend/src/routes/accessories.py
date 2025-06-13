from flask import Blueprint, jsonify, request
from src.models.user import db

accessories_bp = Blueprint('accessories', __name__)

# Sample accessories data
ACCESSORIES_DATA = [
    {
        'id': 1,
        'name': 'سماعات قيمنق احترافية',
        'price': 199,
        'category': 'audio',
        'brand': 'HyperX',
        'description': 'سماعات عالية الجودة مع ميكروفون قابل للإزالة',
        'image': 'headset.jpg',
        'rating': 4.6,
        'in_stock': True,
        'features': ['صوت محيطي 7.1', 'ميكروفون قابل للإزالة', 'مريحة للاستخدام الطويل']
    },
    {
        'id': 2,
        'name': 'كيبورد ميكانيكي RGB',
        'price': 299,
        'category': 'input',
        'brand': 'Razer',
        'description': 'كيبورد ميكانيكي مع إضاءة RGB قابلة للتخصيص',
        'image': 'keyboard.jpg',
        'rating': 4.8,
        'in_stock': True,
        'features': ['مفاتيح ميكانيكية', 'إضاءة RGB', 'مقاوم للماء']
    },
    {
        'id': 3,
        'name': 'ماوس قيمنق دقيق',
        'price': 149,
        'category': 'input',
        'brand': 'Logitech',
        'description': 'ماوس عالي الدقة مع إعدادات قابلة للبرمجة',
        'image': 'mouse.jpg',
        'rating': 4.7,
        'in_stock': True,
        'features': ['12000 DPI', 'أزرار قابلة للبرمجة', 'تصميم مريح']
    },
    {
        'id': 4,
        'name': 'كرسي قيمنق مريح',
        'price': 899,
        'category': 'furniture',
        'brand': 'DXRacer',
        'description': 'كرسي قيمنق مريح مع دعم قطني',
        'image': 'chair.jpg',
        'rating': 4.5,
        'in_stock': True,
        'features': ['دعم قطني', 'قابل للتعديل', 'جلد عالي الجودة']
    },
    {
        'id': 5,
        'name': 'شاشة قيمنق منحنية',
        'price': 1299,
        'category': 'display',
        'brand': 'Samsung',
        'description': 'شاشة منحنية 27 بوصة بدقة 4K',
        'image': 'monitor.jpg',
        'rating': 4.9,
        'in_stock': True,
        'features': ['دقة 4K', 'معدل تحديث 144Hz', 'تصميم منحني']
    },
    {
        'id': 6,
        'name': 'يد تحكم لاسلكية',
        'price': 249,
        'category': 'controller',
        'brand': 'Xbox',
        'description': 'يد تحكم لاسلكية متوافقة مع PC و Xbox',
        'image': 'controller.jpg',
        'rating': 4.8,
        'in_stock': True,
        'features': ['اتصال لاسلكي', 'بطارية طويلة المدى', 'اهتزاز متقدم']
    },
    {
        'id': 7,
        'name': 'ميكروفون بث احترافي',
        'price': 399,
        'category': 'audio',
        'brand': 'Blue Yeti',
        'description': 'ميكروفون احترافي للبث والتسجيل',
        'image': 'microphone.jpg',
        'rating': 4.7,
        'in_stock': True,
        'features': ['جودة صوت احترافية', 'أنماط التقاط متعددة', 'سهل الاستخدام']
    },
    {
        'id': 8,
        'name': 'كاميرا ويب HD',
        'price': 179,
        'category': 'streaming',
        'brand': 'Logitech',
        'description': 'كاميرا ويب عالية الدقة للبث والمكالمات',
        'image': 'webcam.jpg',
        'rating': 4.4,
        'in_stock': True,
        'features': ['دقة 1080p', 'تركيز تلقائي', 'ميكروفون مدمج']
    }
]

@accessories_bp.route('/accessories', methods=['GET'])
def get_accessories():
    """Get all accessories or filter by category/brand"""
    category = request.args.get('category')
    brand = request.args.get('brand')
    
    accessories = ACCESSORIES_DATA.copy()
    
    if category:
        accessories = [acc for acc in accessories if acc['category'].lower() == category.lower()]
    
    if brand:
        accessories = [acc for acc in accessories if acc['brand'].lower() == brand.lower()]
    
    return jsonify({
        'success': True,
        'accessories': accessories,
        'total': len(accessories)
    })

@accessories_bp.route('/accessories/<int:accessory_id>', methods=['GET'])
def get_accessory(accessory_id):
    """Get specific accessory by ID"""
    accessory = next((acc for acc in ACCESSORIES_DATA if acc['id'] == accessory_id), None)
    
    if not accessory:
        return jsonify({
            'success': False,
            'message': 'Accessory not found'
        }), 404
    
    return jsonify({
        'success': True,
        'accessory': accessory
    })

@accessories_bp.route('/accessories/categories', methods=['GET'])
def get_accessory_categories():
    """Get all accessory categories"""
    categories = list(set(acc['category'] for acc in ACCESSORIES_DATA))
    
    return jsonify({
        'success': True,
        'categories': categories
    })

@accessories_bp.route('/accessories/brands', methods=['GET'])
def get_brands():
    """Get all available brands"""
    brands = list(set(acc['brand'] for acc in ACCESSORIES_DATA))
    
    return jsonify({
        'success': True,
        'brands': brands
    })

@accessories_bp.route('/accessories/featured', methods=['GET'])
def get_featured_accessories():
    """Get featured accessories (highest rated)"""
    featured = sorted(ACCESSORIES_DATA, key=lambda x: x['rating'], reverse=True)[:3]
    
    return jsonify({
        'success': True,
        'featured_accessories': featured
    })

@accessories_bp.route('/accessories/search', methods=['GET'])
def search_accessories():
    """Search accessories by name"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Search query is required'
        }), 400
    
    results = [
        acc for acc in ACCESSORIES_DATA 
        if query in acc['name'].lower() or query in acc['description'].lower()
    ]
    
    return jsonify({
        'success': True,
        'results': results,
        'total': len(results)
    })

@accessories_bp.route('/accessories/by-price', methods=['GET'])
def get_accessories_by_price():
    """Get accessories filtered by price range"""
    min_price = request.args.get('min_price', type=int, default=0)
    max_price = request.args.get('max_price', type=int, default=float('inf'))
    
    filtered = [
        acc for acc in ACCESSORIES_DATA 
        if min_price <= acc['price'] <= max_price
    ]
    
    return jsonify({
        'success': True,
        'accessories': filtered,
        'total': len(filtered)
    })

