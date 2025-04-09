# 半数黑金（Half Black Money）游戏项目

## 项目概述
半数黑金是一款集换式卡牌游戏，结合策略、推理与角色扮演，通过人工智能生成的角色元素，让玩家体验多样化的游戏乐趣。

## 项目结构
### 项目文件目录结构
- [Readme.md](./Readme.md)：项目的整体简介和文件结构说明。
- [.env](./.env)：项目的配置文件，包含数据库连接信息。
- [generate_requirements.sh](./generate_requirements.sh)：生成项目依赖的脚本。
- [requirements.txt](./requirements.txt)：项目依赖的Python库列表。
- [LICENSE](./LICENSE)：项目的开源许可证。
- [docker-compose.yml](./docker-compose.yml)：容器编排配置
- [.gitattributes](./.gitattributes)：Git属性配置  
- [.gitignore](./.gitignore)：Git忽略规则
- [db](./db)：数据库相关
  - [hbm_db_init.sql](./db/hbm_db_init.sql)：数据库初始化脚本
  - [hbm_db.py](./db/hbm_db.py)：数据库操作类
  - [hbm-mysql.session.sql](./db/hbm-mysql.session.sql)：MySQL会话脚本
  - [SQLite.sql](./db/SQLite.sql)：SQLite数据库脚本
- [backend](./backend)：后端代码
  - [app.py](./backend/app.py)：应用入口
  - [server.py](./backend/server.py)：FastAPI服务器代码
  - [static.py](./backend/static.py)：静态文件处理
  - [api](./backend/api)：API模块
    - [api_ollama_by_local.py](./backend/api/api_ollama_by_local.py)：本地Ollama API实现
    - [api_ollama_by_OpenAI.py](./backend/api/api_ollama_by_OpenAI.py)：OpenAI API实现
    - [api_ollama_by_remoto.py](./backend/api/api_ollama_by_remoto.py)：远程Ollama API实现
    - [api_openai.py](./backend/api/api_openai.py)：OpenAI API封装
    - [api.py](./backend/api/api.py)：通用API接口
  - [auth](./backend/auth)：认证模块
    - [login_or_register.py](./backend/auth/login_or_register.py)：登录和注册功能
  - [services](./backend/services)：服务模块
    - [get_remoto_api_url.py](./backend/services/get_remoto_api_url.py)：获取远程API URL
    - [save_images.py](./backend/services/save_images.py)：保存图片功能
  - [utils](./backend/utils)：工具模块
    - [utils.py](./backend/utils/utils.py)：通用工具函数
- [frontend](./frontend)：前端代码
  - [index.html](./frontend/index.html)：前端入口文件
  - [auth](./frontend/auth)：认证模块
    - [login.html](./frontend/auth/login.html)：登录页面
    - [login.js](./frontend/auth/login.js)：登录逻辑
  - [cards](./frontend/cards)：卡牌管理模块
    - [card-management.html](./frontend/cards/card-management.html)：卡牌管理页面
  - [components](./frontend/components)：组件模块
    - [common.js](./frontend/components/common.js)：通用JavaScript文件
    - [header.html](./frontend/components/header.html)：头部组件
    - [navbar.html](./frontend/components/narvar.html)：导航栏组件
    - [sidebar.html](./frontend/components/sidebar.html)：侧边栏组件
  - [game](./frontend/game)：游戏模块
    - [game.html](./frontend/game/game.html)：游戏页面
    - [game.css](./frontend/game/game.css)：游戏样式表
    - [game.js](./frontend/game/game.js)：游戏逻辑
  - [index](./frontend/index)：首页模块
    - [index.html](./frontend/index/index.html)：首页页面
    - [index.css](./frontend/index/index.css)：首页样式表
    - [index.js](./frontend/index/index.js)：首页逻辑
  - [static](./frontend/static)：静态资源
    - [images](./frontend/static/images)：图片资源
      - [background.png](./frontend/static/images/background.png)：背景图片
      - [hbm.png](./frontend/static/images/hbm.png)：项目Logo
  - [stats](./frontend/stats)：统计模块
    - [match-stats.html](./frontend/stats/match-stats.html)：比赛统计页面
    - [match-stats.js](./frontend/stats/match-stats.js)：比赛统计逻辑
  - [user](./frontend/user)：用户模块
    - [user.html](./frontend/user/user.html)：用户信息页面
    - [user.js](./frontend/user/user.js)：用户信息逻辑
- [参考](./参考)：参考代码和原型
  - [moments](https://github.com/greyli/moments)：一个基于Flask的社交网络项目
  - [langgraph-demo](https://github.com/q2wxec/langgraph-demo):LangGraph语言模型可视化Demo

## 主要功能
### 1. 主机控制
- **功能**：控制游戏进程。
- **责任**：指导玩家遵循游戏规则，确保游戏流程顺利进行。

### 2. 卡牌管理
- **功能**：允许玩家存储和管理卡牌信息。
- **责任**：提供卡牌的增删改查功能，确保玩家能够方便地管理自己的卡牌。

### 3. 角色建立  
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
- **功能**：利用AI生成卡牌内容，增加游戏的趣味性和可玩性。
- **责任**：确保生成的卡牌内容符合游戏规则和玩家期望。

### 7. 分数和成绩管理
- **功能**：在游戏结束后生成玩家得分及成就记录。
- **责任**：确保分数和成绩的准确性和可追溯性。

### 8. 用户系统
- **功能**：完整的登录/注册流程
- **安全机制**：实现密码哈希存储，确保用户数据的安全性。
- **会话管理**：支持用户会话管理，确保用户登录状态的持久性。

## 当前开发进度
### 已实现功能
1. **用户系统**：完成登录/注册功能，支持密码哈希存储和会话管理。
2. **卡牌管理**：实现卡牌信息的存储和管理，支持查看游戏记录和分发卡牌。
3. **分数和成绩管理**：完成玩家得分及成就记录的存储和查询功能。
4. **主机控制**：实现游戏进程的基本控制逻辑。
5. **角色建立**：完成角色场景的模板选择和实时生成功能。
6. **角色身份**：实现角色身份生成功能，支持为角色生成独特的场景和技能。
7. **初始设定**：完成游戏开始前的卡牌选择功能。
8. **行动生成**：实现每轮行动生成功能，支持动态调整可选项。
9. **卡牌生成（AI增强版）**：集成AI生成卡牌功能，支持自动生成卡牌内容。

### 未实现功能
1. **反向代理配置**：尚未配置Nginx反向代理

### 下一步计划
1. **行动生成**：开发每轮行动生成功能，确保行动的多样性和策略性。
2. **卡牌生成（AI增强版）**：集成AI生成卡牌功能，增强游戏体验。
3. **反向代理配置**：配置Nginx反向代理，优化服务部署。

## 技术栈
### 后端
- **语言**：Python 3.12.7
- **框架**：FastAPI
- **API文档**：Swagger/OpenAPI
- **数据库**：MySQL 8.0.31、SQLite
- **缓存**：Redis

### 容器化
- **工具**：Docker
- **配置文件**：`docker-compose.yml`

### AI服务
- **工具**：Ollama
- **端口**：11434

## 项目启动指南

1. **克隆项目**:
   ```bash
   git clone https://github.com/your-repo/half-black-money.git
   cd half-black-money
   ```

2. **配置环境变量**:
   - 复制 `.env.example` 为 `.env`，并根据需要修改配置。

3. **启动 Docker 服务**:
   ```bash
   docker-compose up --build
   ```
   注意：启动后，可以使用以下命令停止服务：
   ```bash
   docker-compose down
   ```

4. **开发环境下直接启动后端服务**:
   ```bash
   python backend/app.py
   ```
   注意：此方式适用于开发环境，默认监听 `5000` 端口。

5. **验证服务是否正常运行**:
   - 打开浏览器，访问 http://localhost:80，确认Nginx服务正常运行。
   - 访问 http://localhost:5001/docs，确认后端API服务正常运行。
   - 使用以下命令验证Ollama服务：
     ```bash
     curl http://localhost:11434
     ```
   - 使用以下命令验证Redis服务：
     ```bash
     redis-cli ping
     ```

6. **访问应用**:
   - 打开浏览器，访问 http://localhost:80。
   - 后端API服务默认映射到 `5001` 端口。
   - Ollama服务默认映射到 `11434` 端口。
   - Redis服务默认映射到 `6379` 端口。
