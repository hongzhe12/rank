# 排行榜系统接口文档

## 1. 用户认证相关接口

### 1.1 用户注册
- **接口**: `/api/auth/register`
- **方法**: POST
- **请求参数**:
```json
{
    "name": "张三",
    "phone": "13800000001",
    "password": "123456",
    "avatar": "static/images/t1.jpg"  // 可选
}
```
- **响应示例**:
```json
{
    "status": "success",
    "message": "注册成功"
}
```

### 1.2 用户登录
- **接口**: `/api/auth/login`
- **方法**: POST
- **请求参数**:
```json
{
    "phone": "13800000001",
    "password": "123456"
}
```
- **响应示例**:
```json
{
    "status": "success",
    "message": "登录成功",
    "data": {
        "name": "张三",
        "phone": "13800000001",
        "avatar": "static/images/t1.jpg"
    }
}
```

### 1.3 用户登出
- **接口**: `/api/auth/logout`
- **方法**: GET
- **响应示例**:
```json
{
    "status": "success",
    "message": "登出成功"
}
```

## 2. 用户数据相关接口

### 2.1 获取用户统计数据
- **接口**: `/api/user/<name>/stats`
- **方法**: GET
- **需要登录**: 是
- **响应示例**:
```json
{
    "name": "张三",
    "chat_count": 128,
    "resume_count": 45,
    "interview_count": 12,
    "updated_at": "2024-02-22 10:30:00"
}
```

### 2.2 更新用户数据
- **接口**: `/api/user/<name>/update`
- **方法**: PUT
- **需要登录**: 是
- **请求参数**:
```json
{
    "chat_count": 150,
    "resume_count": 50,
    "interview_count": 15
}
```
- **响应示例**:
```json
{
    "status": "success",
    "message": "用户数据更新成功"
}
```

## 3. 榜单相关接口

### 3.1 获取特定榜单数据
- **接口**: `/api/rankings/<ranking_type>`
- **方法**: GET
- **需要登录**: 是
- **参数说明**: ranking_type可选值：chat/resume/interview
- **响应示例**:
```json
{
    "title": "沟通数量榜单",
    "list": [
        {
            "rank": 1,
            "name": "张三",
            "value": "128次",
            "avatar": "static/images/t1.jpg",
            "trend": 0
        }
    ]
}
```

### 3.2 刷新榜单
- **接口**: `/api/rankings/refresh`
- **方法**: POST
- **需要登录**: 是
- **响应示例**:
```json
{
    "status": "success",
    "message": "榜单刷新成功"
}
```

## 4. 错误码说明
- 200: 请求成功
- 400: 请求参数错误
- 401: 未登录或登录已过期
- 404: 资源不存在
- 500: 服务器内部错误

需要我添加更多接口说明或示例吗？