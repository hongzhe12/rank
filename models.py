from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(200), nullable=False)
    chat_count = db.Column(db.Integer, default=0)
    resume_count = db.Column(db.Integer, default=0)
    interview_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class RankingList(db.Model):
    __tablename__ = 'ranking_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.now)

class RankingItem(db.Model):
    __tablename__ = 'ranking_items'
    
    id = db.Column(db.Integer, primary_key=True)
    ranking_list_id = db.Column(db.Integer, db.ForeignKey('ranking_lists.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    value = db.Column(db.Integer, default=0)
    trend = db.Column(db.Integer, default=0)  # 1: 上升, 0: 不变, -1: 下降
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('ranking_items', lazy=True))
    ranking_list = db.relationship('RankingList', backref=db.backref('items', lazy=True))

class RankingManager:
    @staticmethod
    def init_rankings():
        # 初始化榜单
        rankings = {
            'chat': {'title': '沟通数量榜单', 'unit': '次'},
            'resume': {'title': '已投简历榜单', 'unit': '份'},
            'interview': {'title': '待面试榜单', 'unit': '场'}
        }
        
        for key, data in rankings.items():
            if not RankingList.query.filter_by(title=data['title']).first():
                ranking = RankingList(title=data['title'], unit=data['unit'])
                db.session.add(ranking)
        db.session.commit()

    @staticmethod
    def update_rankings():
        # 更新排名
        rankings = RankingList.query.all()
        for ranking in rankings:
            RankingItem.query.filter_by(ranking_list_id=ranking.id).delete()
            
            if ranking.title == '沟通数量榜单':
                users = User.query.order_by(User.chat_count.desc()).all()
                value_attr = 'chat_count'
            elif ranking.title == '已投简历榜单':
                users = User.query.order_by(User.resume_count.desc()).all()
                value_attr = 'resume_count'
            else:
                users = User.query.order_by(User.interview_count.desc()).all()
                value_attr = 'interview_count'

            for rank, user in enumerate(users, 1):
                item = RankingItem(
                    ranking_list_id=ranking.id,
                    user_id=user.id,
                    value=getattr(user, value_attr),
                    rank=rank
                )
                db.session.add(item)

        db.session.commit()

    @staticmethod
    def get_all_rankings():
        rankings = []
        for ranking_list in RankingList.query.all():
            items = []
            for item in RankingItem.query.filter_by(ranking_list_id=ranking_list.id).order_by(RankingItem.rank).all():
                items.append({
                    'rank': item.rank,
                    'name': item.user.name,
                    'value': f'{item.value}{ranking_list.unit}',
                    'avatar': item.user.avatar,
                    'trend': item.trend
                })
            rankings.append({
                'title': ranking_list.title,
                'list': items
            })
        return rankings