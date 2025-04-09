# 半数黑金（Half Black Money）游戏项目

## 游戏概述

半数黑金是一款集换式卡牌游戏，结合策略、推理与角色扮演，通过人工智能生成的角色元素，让玩家体验多样化的游戏乐趣。

## 项目结构

### 文件结构
- [Readme.md](./Readme.md)：项目的整体简介和文件结构说明。
- [.env](./.env)：项目的配置文件，包含数据库连接信息。
- [create.sql](./db/create.sql)：创建数据库表的SQL脚本。
- [generate_requirements.sh](./generate_requirements.sh)：生成项目依赖的脚本。
- [requirements.txt](./requirements.txt)：项目依赖的Python库列表。
- [LICENSE](./LICENSE)：项目的开源许可证。

### [backend](./backend) 目录
- [app.py](./backend/app.py)：后端主应用文件，包含Flask应用及路由配置，数据库连接和业务逻辑实现。

### [frontend](./frontend) 目录
- [index.html](./frontend/index.html)：游戏的HTML主页。

## 主要功能

### 1. 主机控制
- **功能**：控制游戏进程。
- **责任**：指导玩家遵循游戏规则。

### 2. 角色建立
- **功能**：构建具体角色场景。
- **责任**：提供模板选择和实时生成角色的功能。

### 3. 角色身份
- **功能**：生成玩家的角色身份。
- **责任**：为角色生成独特的场景和技能。

### 4. 初始设定
- **功能**：在游戏开始前选择最多三张卡牌作为初始设定。

### 5. 行动生成
- **功能**：为每轮生成多种选择的行动。
- **责任**：根据游戏进程和场景动态调整可选项。

### 6. 卡牌生成
- **功能**：根据所选行动生成相应的卡牌。
- **责任**：确保卡牌内容符合世界观，符合玩家期望。

### 7. 分数和成绩管理
- **功能**：在游戏结束后生成玩家得分及成就记录。

### 8. 卡牌管理
- **功能**：允许玩家存储和管理卡牌信息。
- **责任**：支持查看游戏记录和进行分发卡牌。

## 技术栈
- 服务器: Python 3.10
- 数据库: MySQL 8.0.31
- 容器化: Docker-compose 3.8
- 开发环境: VSCode
- Web框架: Flask, FastAPI
- ORM库: mysql-connector-python
- 加密库: bcrypt
- 配置管理: dotenv, configparser
- 状态管理: langgraph
- 前端: HTML, CSS (通过index.html和page.html定义)

