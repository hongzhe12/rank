import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_update_new_user():
    # 测试更新不存在的用户（应该自动创建）
    data = {
        "name": "测试新用户",
        "avatar": "static/images/t1.jpg",
        "chat_count": 88,
        "resume_count": 25,
        "interview_count": 6
    }
    response = requests.put(
        f'{BASE_URL}/api/user/测试新用户/update',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print("\n创建新用户:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    # 立即刷新榜单
    requests.post(f'{BASE_URL}/api/rankings/refresh')

def test_batch_create_users():
    # 批量创建测试用户
    test_users = [
        {
            "name": "测试用户A",
            "chat_count": 120,
            "resume_count": 40,
            "interview_count": 10
        },
        {
            "name": "测试用户B",
            "chat_count": 80,
            "resume_count": 30,
            "interview_count": 5
        }
    ]
    
    for user_data in test_users:
        response = requests.put(
            f'{BASE_URL}/api/user/{user_data["name"]}/update',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"\n创建用户 {user_data['name']}:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    # 批量创建后刷新榜单
    requests.post(f'{BASE_URL}/api/rankings/refresh')

def test_get_user_stats(name):
    # 获取用户统计数据
    response = requests.get(f'{BASE_URL}/api/user/{name}/stats')
    print(f"\n获取用户[{name}]统计:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_get_all_rankings():
    # 获取所有类型的榜单数据
    ranking_types = ['chat', 'resume', 'interview']
    for ranking_type in ranking_types:
        response = requests.get(f'{BASE_URL}/api/rankings/{ranking_type}')
        print(f"\n获取{ranking_type}榜单:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    print("开始测试API接口...")
    
    # 创建单个测试用户
    test_update_new_user()
    
    # 批量创建测试用户
    test_batch_create_users()
    
    # 验证所有用户数据
    test_get_user_stats("测试新用户")
    test_get_user_stats("测试用户A")
    test_get_user_stats("测试用户B")
    
    # 查看所有榜单
    test_get_all_rankings()