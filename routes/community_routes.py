"""
Kisan Web Project - Community Platform Routes
Empowers farmers to share field updates, ask crop pathology questions, and interact with peers.
"""
import os
import uuid
from flask import Blueprint, request, jsonify, session, current_app
from extensions import db
from models import CommunityPost, User

community_bp = Blueprint('community', __name__, url_prefix='/api/community')

@community_bp.route('/posts', methods=['GET'])
def get_posts():
    """Retrieve community feed posts with category filtering."""
    category = request.args.get('category', '').strip().lower()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    query = CommunityPost.query
    if category and category != 'all':
        query = query.filter_by(category=category)

    posts_page = query.order_by(CommunityPost.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': posts_page.total,
        'pages': posts_page.pages,
        'current_page': posts_page.page,
        'posts': [p.to_dict() for p in posts_page.items]
    }), 200


@community_bp.route('/posts', methods=['POST'])
def create_post():
    """Create a new post in the farmer community feed."""
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None

    # Support both multipart/form-data (with file upload) and JSON
    if request.content_type and 'multipart/form-data' in request.content_type:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'growth_update').strip()
        author_name = request.form.get('author_name', '').strip()
        author_location = request.form.get('author_location', 'Punjab, India').strip()

        media_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'jpg'
                filename = f"post_{uuid.uuid4().hex[:10]}.{ext}"
                file.save(os.path.join(upload_dir, filename))
                media_url = f"/static/uploads/{filename}"
    else:
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', 'growth_update').strip()
        author_name = data.get('author_name', '').strip()
        author_location = data.get('author_location', 'Punjab, India').strip()
        media_url = data.get('media_url')

    if not title or not content:
        return jsonify({'error': 'Title and content are required.'}), 400

    if user:
        author_name = user.name
        author_location = f"{user.district}, {user.state}" if user.district else user.state or 'Local Farmer'
        post_user_id = user.id
    else:
        if not author_name:
            author_name = 'Progressive Farmer'
        # Default fallback system author
        admin_user = User.query.first()
        post_user_id = admin_user.id if admin_user else 1

    post = CommunityPost(
        user_id=post_user_id,
        author_name=author_name,
        author_location=author_location,
        title=title,
        content=content,
        category=category,
        media_url=media_url,
        likes_count=0,
        comments_count=0
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'message': 'Post published to the Kisan community feed!',
        'post': post.to_dict()
    }), 201


@community_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """Increment like/helpful counter on a community post."""
    post = CommunityPost.query.get_or_404(post_id)
    post.likes_count = (post.likes_count or 0) + 1
    db.session.commit()
    return jsonify({
        'status': 'success',
        'post_id': post.id,
        'likes_count': post.likes_count
    }), 200
