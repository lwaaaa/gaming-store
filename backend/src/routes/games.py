from flask import Blueprint, jsonify, request
from src.models.user import db

games_bp = Blueprint('games', __name__)

# Sample games data
GAMES_DATA = [
    {
        'id': 1,
        'name': 'FIFA 2024',
        'price': 299,
        'category': 'sports',
        'platform': ['PS5', 'Xbox', 'PC'],
        'description': 'أحدث إصدار من لعبة كرة القدم الشهيرة',
        'image': 'fifa2024.jpg',
        'rating': 4.8,
        'in_stock': True
    },
    {
        'id': 2,
        'name': 'Call of Duty',
        'price': 399,
        'category': 'action',
        'platform': ['PS5', 'Xbox', 'PC'],
        'description': 'لعبة الأكشن والحروب الأكثر شهرة',
        'image': 'cod.jpg',
        'rating': 4.7,
        'in_stock': True
    },
    {
        'id': 3,
        'name': 'Grand Theft Auto',
        'price': 249,
        'category': 'action',
        'platform': ['PS5', 'Xbox', 'PC'],
        'description': 'عالم مفتوح مليء بالمغامرات',
        'image': 'gta.jpg',
        'rating': 4.9,
        'in_stock': True
    },
    {
        'id': 4,
        'name': 'Elden Ring',
        'price': 349,
        'category': 'rpg',
        'platform': ['PS5', 'Xbox', 'PC'],
        'description': 'لعبة RPG ملحمية من صناع Dark Souls',
        'image': 'eldenring.jpg',
        'rating': 4.9,
        'in_stock': True
    },
    {
        'id': 5,
        'name': 'Spider-Man 2',
        'price': 379,
        'category': 'action',
        'platform': ['PS5'],
        'description': 'مغامرات الرجل العنكبوت الجديدة',
        'image': 'spiderman2.jpg',
        'rating': 4.8,
        'in_stock': True
    },
    {
        'id': 6,
        'name': 'Forza Horizon 5',
        'price': 299,
        'category': 'racing',
        'platform': ['Xbox', 'PC'],
        'description': 'أفضل لعبة سباقات في العالم المفتوح',
        'image': 'forza5.jpg',
        'rating': 4.7,
        'in_stock': True
    }
]

@games_bp.route('/games', methods=['GET'])
def get_games():
    """Get all games or filter by category/platform"""
    category = request.args.get('category')
    platform = request.args.get('platform')
    
    games = GAMES_DATA.copy()
    
    if category:
        games = [game for game in games if game['category'].lower() == category.lower()]
    
    if platform:
        games = [game for game in games if platform in game['platform']]
    
    return jsonify({
        'success': True,
        'games': games,
        'total': len(games)
    })

@games_bp.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """Get specific game by ID"""
    game = next((game for game in GAMES_DATA if game['id'] == game_id), None)
    
    if not game:
        return jsonify({
            'success': False,
            'message': 'Game not found'
        }), 404
    
    return jsonify({
        'success': True,
        'game': game
    })

@games_bp.route('/games/categories', methods=['GET'])
def get_categories():
    """Get all game categories"""
    categories = list(set(game['category'] for game in GAMES_DATA))
    
    return jsonify({
        'success': True,
        'categories': categories
    })

@games_bp.route('/games/platforms', methods=['GET'])
def get_platforms():
    """Get all available platforms"""
    platforms = set()
    for game in GAMES_DATA:
        platforms.update(game['platform'])
    
    return jsonify({
        'success': True,
        'platforms': list(platforms)
    })

@games_bp.route('/games/featured', methods=['GET'])
def get_featured_games():
    """Get featured games (highest rated)"""
    featured = sorted(GAMES_DATA, key=lambda x: x['rating'], reverse=True)[:4]
    
    return jsonify({
        'success': True,
        'featured_games': featured
    })

@games_bp.route('/games/search', methods=['GET'])
def search_games():
    """Search games by name"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Search query is required'
        }), 400
    
    results = [
        game for game in GAMES_DATA 
        if query in game['name'].lower() or query in game['description'].lower()
    ]
    
    return jsonify({
        'success': True,
        'results': results,
        'total': len(results)
    })

