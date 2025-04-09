# 半数黑金（Half Black Money）游戏项目

## 游戏概述

半数黑金是一款集换式卡牌游戏，结合策略、推理与角色扮演，通过人工智能生成的角色元素，让玩家体验多样化的游戏乐趣。

## 项目结构

### 文件结构
- [Readme.md](./Readme.md)：项目的整体简介和文件结构说明。
- [.env](./.env)：项目的配置文件，包含数据库连接信息。
- [generate_requirements.sh](./generate_requirements.sh)：生成项目依赖的脚本。
- [requirements.txt](./requirements.txt)：项目依赖的Python库列表。
- [LICENSE](./LICENSE)：项目的开源许可证。
- [docker-compose.yml](./docker-compose.yml)：容器编排配置
- [.gitattributes](./.gitattributes)：Git属性配置  
- [.gitignore](./.gitignore)：Git忽略规则
- [hbm-mysql.session.sql](./hbm-mysql.session.sql)：MySQL会话脚本

### 目录结构
- [backend](./backend)：后端代码
  - [app.py](./backend/app.py)：后端主应用文件，包含Flask应用及路由配置，数据库连接和业务逻辑实现
  - [api_ollama_by_local.py](./backend/api_ollama_by_local.py)：本地Ollama API接口
  - [api_ollama_by_remoto.py](./backend/api_ollama_by_remoto.py)：远程Ollama API接口 
  - [api_openai.py](./backend/api_openai.py)：OpenAI API接口
  - [get_remoto_api_url.py](./backend/get_remoto_api_url.py)：远程API URL获取工具
  - [login_or_register.py](./backend/login_or_register.py)：登录注册功能
  - [static.py](./backend/static.py)：静态文件服务
  - [api.py](./backend/api.py)：统一API路由入口
  - [server.py](./backend/server.py)：FastAPI备用服务
  - [save_images.py](./backend/save_images.py)：卡牌图像存储模块

- [frontend](./frontend)：前端代码
  - [index.html](./frontend/index.html)：游戏主页面
  - [game.html](./frontend/game.html)：游戏页面
  - [login.html](./frontend/login.html)：登录页面
  - [navbar.html](./frontend/navbar.html)：全局导航组件
  - [user.html](./frontend/user.html)：用户信息页面
  - [static](./frontend/static)：静态资源
    - [index.css](./frontend/static/index.css)：主样式表
    - [index.js](./frontend/static/index.js)：主JavaScript文件
    - [login.js](./frontend/static/login.js)：登录交互逻辑
    - [images](./frontend/static/images)：图片资源
      - [background.png](./frontend/static/images/background.png)：背景图片
      - [hbm.png](./frontend/static/images/hbm.png)：游戏Logo

- [db](./db)：数据库相关
  - [hbm_db_init.sql](./db/hbm_db_init.sql)：数据库初始化脚本
  - [hbm_db.py](./db/hbm_db.py)：数据库操作类
  - [hbm-mysql.session.sql](./db/hbm-mysql.session.sql)：MySQL会话脚本
  - [SQLite.sql](./db/SQLite.sql)：SQLite数据库脚本
- [参考](./参考)：参考代码和原型
  - [wolf_game.py](./参考/wolf_game.py)：狼人杀游戏逻辑
  - [server.py](./参考/server.py)：FastAPI服务器代码
  - [state.py](./参考/state.py)：游戏状态管理
## 主要功能

### 1. 主机控制
- **功能**：控制游戏进程。
- **责任**：指导玩家遵循游戏规则，确保游戏流程顺利进行。

### 2. 角色建立  
- **功能**：构建具体角色场景。
- **责任**：提供模板选择和实时生成角色的功能，确保角色场景的多样性和趣味性。

### 3. 角色身份
- **功能**：生成玩家的角色身份。
- **责任**：为角色生成独特的场景和技能，确保每个角色都有独特的体验。

### 4. 初始设定
- **功能**：在游戏开始前选择最多三张卡牌作为初始设定。
- **责任**：确保初始设定合理且不影响游戏平衡。

### 5. 行动生成
- **功能**：为每轮生成多种选择的行动。
- **责任**：根据游戏进程和场景动态调整可选项，确保行动的多样性和策略性。

### 6. 卡牌生成（AI增强版）

### 7. 分数和成绩管理
- **功能**：在游戏结束后生成玩家得分及成就记录。
- **实现**：通过 `hbm_db.py` 中的数据库操作类将玩家的得分和成就记录存储到 MySQL 数据库中，具体表结构在 `hbm_db_init.sql` 中定义。

### 8. 卡牌管理
- **功能**：允许玩家存储和管理卡牌信息。
- **责任**：支持查看游戏记录和进行分发卡牌，确保卡牌管理的便捷性和安全性。
- **实现**：通过 `save_images.py` 中的 `save_game` 函数将玩家的卡牌信息和游戏记录存储到数据库中，并通过 `hbm_db.py` 进行查询和管理。

### 9. 用户系统
- **功能**：完整的登录/注册流程
- **安全机制**：通过`login_or_register.py`实现密码哈希存储，确保用户数据的安全性。
- **会话管理**：基于Flask的session管理，确保用户会话的稳定性和安全性。

---

## 开发指南

### 开发准备

1. **AI服务配置**：
   ```bash
   # 本地Ollama服务
   docker run -d -p 11434:11434 ollama/ollama
   ollama pull llama2

   # OpenAI配置
   echo "OPENAI_API_KEY=sk-your-key" >> .env
   ```

2. **数据库初始化**： 通过docker  创建mysql 后在mysql 中执行hbm_db_init.sql
   

3. **前端热更新**：
   ```bash
   npx browser-sync start --server 'frontend' --files 'frontend/**/*.html, frontend/static/**/*.js'
   ```

4. **后端服务启动**：
   ```bash
   cd backend && python app.py
   ```

5. **前端服务启动**：
   ```bash
   cd frontend && npx http-server
   ```

---

## 技术栈

### 主要技术
- **语言**：Python 3.10, JavaScript
- **数据库**：MySQL 8.0.31, SQLite
- **Web框架**：Flask, FastAPI
- **前端**：HTML5, CSS3, JavaScript
- **容器化**：Docker, Docker Compose
- **ORM库**：mysql-connector-python, SQLAlchemy
- **AI服务**：Ollama, OpenAI
- **开发工具**：VSCode, Git

### 扩展技术
- **AI推理加速**：vLLM（通过Ollama集成）
- **前端框架**：Bootstrap 5（内置于navbar.html）
- **API文档**：Swagger（集成于FastAPI服务）
- **静态资源管理**：Flask-Static
- **会话管理**：Flask-Session

---

## 项目启动指南

1. **克隆项目**:
   ```bash
   git clone https://github.com/your-repo/half-black-money.git
   cd half-black-money
   ```

2. **配置环境变量**:
   - 复制`.env.example`为`.env`，并根据需要修改配置。

3. **启动服务**:
   ```bash
   docker-compose up --build
   ```

4. **访问应用**:
   - 打开浏览器，访问`http://localhost:5000`。

---