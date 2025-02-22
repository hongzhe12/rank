from flask import Flask, render_template, jsonify, request
from models import db, RankingManager, RankingList, User
from admin import init_admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rankings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # 添加密钥，admin需要

db.init_app(app)
init_admin(app)  # 初始化管理后台

@app.route('/')
def index():
    from datetime import datetime
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rankings = RankingManager.get_all_rankings()
    return render_template('index.html', rankings=rankings, update_time=update_time)

# 用户数据更新接口
@app.route('/api/user/<string:name>/update', methods=['PUT'])
def update_user(name):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '无效的请求数据'}), 400
            
        user = User.query.filter_by(name=name).first()
        if not user:
            # 如果用户不存在，创建新用户
            user = User(
                name=name,
                avatar='static/images/t1.jpg',  # 使用默认头像
                chat_count=0,
                resume_count=0,
                interview_count=0
            )
            db.session.add(user)
            
        # 更新用户数据，使用 get 方法避免 KeyError
        if data.get('chat_count') is not None:
            user.chat_count = data['chat_count']
        if data.get('resume_count') is not None:
            user.resume_count = data['resume_count']
        if data.get('interview_count') is not None:
            user.interview_count = data['interview_count']
        if data.get('avatar'):
            user.avatar = data['avatar']
            
        db.session.commit()
        return jsonify({'status': 'success', 'message': '用户数据更新成功'})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")  # 添加错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 榜单刷新接口
@app.route('/api/rankings/refresh', methods=['POST'])
def refresh_rankings():
    try:
        RankingManager.update_rankings()
        return jsonify({'status': 'success', 'message': '榜单刷新成功'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 获取单个榜单数据接口
@app.route('/api/rankings/<string:ranking_type>')
def get_ranking(ranking_type):
    try:
        # 定义榜单类型映射
        ranking_titles = {
            'chat': '沟通数量榜单',
            'resume': '已投简历榜单',
            'interview': '待面试榜单'
        }
        
        if ranking_type not in ranking_titles:
            return jsonify({'status': 'error', 'message': '榜单类型不存在'}), 404
            
        rankings = RankingManager.get_all_rankings()
        for ranking in rankings:
            if ranking['title'] == ranking_titles[ranking_type]:
                return jsonify(ranking)
                
        return jsonify({'status': 'error', 'message': '榜单不存在'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 获取用户统计数据接口
@app.route('/api/user/<string:name>/stats')
def get_user_stats(name):
    try:
        user = User.query.filter_by(name=name).first()
        if user:
            return jsonify({
                'name': user.name,
                'chat_count': user.chat_count,
                'resume_count': user.resume_count,
                'interview_count': user.interview_count,
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 创建数据库表
with app.app_context():
    db.create_all()
    # 只在没有榜单数据时初始化
    if not RankingList.query.first():
        RankingManager.init_rankings()
        RankingManager.update_rankings()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)