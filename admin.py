from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, RankingList, RankingItem

admin = Admin(name='排行榜管理系统', template_mode='bootstrap4')

# 自定义 ModelView
class UserAdmin(ModelView):
    column_list = ['name', 'avatar', 'chat_count', 'resume_count', 'interview_count', 'created_at', 'updated_at']
    column_labels = {
        'name': '用户名',
        'avatar': '头像',
        'chat_count': '沟通数量',
        'resume_count': '简历数量',
        'interview_count': '面试数量',
        'created_at': '创建时间',
        'updated_at': '更新时间'
    }
    column_searchable_list = ['name']
    column_filters = ['created_at', 'updated_at']

class RankingListAdmin(ModelView):
    column_list = ['title', 'unit', 'last_update']
    column_labels = {
        'title': '榜单名称',
        'unit': '单位',
        'last_update': '最后更新时间'
    }

class RankingItemAdmin(ModelView):
    column_list = ['ranking_list', 'user', 'value', 'trend', 'rank', 'created_at']
    column_labels = {
        'ranking_list': '榜单',
        'user': '用户',
        'value': '数值',
        'trend': '趋势',
        'rank': '排名',
        'created_at': '创建时间'
    }
    column_filters = ['ranking_list', 'user', 'rank']

def init_admin(app):
    admin.init_app(app)
    # 添加模型视图
    admin.add_view(UserAdmin(User, db.session, name='用户管理'))
    admin.add_view(RankingListAdmin(RankingList, db.session, name='榜单管理'))
    admin.add_view(RankingItemAdmin(RankingItem, db.session, name='排名管理'))