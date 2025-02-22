from app import app, db
from models import User, RankingManager

def init_test_data():
    with app.app_context():
        # 清空现有用户数据
        User.query.delete()
        db.session.commit()
        
        # 创建测试用户数据
        test_users = [
            {
                'name': '张三',
                'avatar': 'static/images/t1.jpg',
                'chat_count': 128,
                'resume_count': 45,
                'interview_count': 12
            },
            {
                'name': '李四',
                'avatar': 'static/images/t1.jpg',
                'chat_count': 96,
                'resume_count': 38,
                'interview_count': 10
            },
            {
                'name': '王五',
                'avatar': 'static/images/t1.jpg',
                'chat_count': 87,
                'resume_count': 32,
                'interview_count': 8
            },
            {
                'name': '赵六',
                'avatar': 'static/images/t1.jpg',
                'chat_count': 75,
                'resume_count': 30,
                'interview_count': 7
            },
            {
                'name': '孙七',
                'avatar': 'static/images/t1.jpg',
                'chat_count': 150,
                'resume_count': 55,
                'interview_count': 15
            }
        ]
        
        # 添加用户数据
        for user_data in test_users:
            user = User(
                name=user_data['name'],
                avatar=user_data['avatar'],
                chat_count=user_data['chat_count'],
                resume_count=user_data['resume_count'],
                interview_count=user_data['interview_count']
            )
            db.session.add(user)
        
        db.session.commit()
        
        # 初始化并刷新榜单
        RankingManager.init_rankings()
        RankingManager.update_rankings()
        
        print("测试数据初始化完成！")

if __name__ == '__main__':
    init_test_data()