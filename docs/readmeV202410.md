
游戏名称：半数黑金（Half Black Money）
游戏类型：本游戏为一款独具特色的集换式卡牌游戏，其核心机制依托于人工智能生成的随机事件，为玩家带来无尽的惊喜与挑战。
游戏机制概述：游戏伊始，玩家将扮演一个由众多权威机构共同组建的精英行动小组。该小组成员来自世界各地，具有不同的国籍和背景，展现出丰富的多样性。玩家在游戏过程中需通过抽取行动选项，进行四选一的决策。每一轮决策后，玩家将选定的行动转化为卡牌，从而推动游戏的整体进程。整个游戏的进程由主持人操控，确保游戏的顺利进行。
主持人Agent：该Agent在游戏过程中扮演着至关重要的角色。它负责调用其他Agent，以掌握每局游戏的总体流程，并引导玩家遵循既定的游戏规则。
故事背景Agent：为了增强游戏的沉浸感，故事背景Agent负责构建每局游戏的具体背景故事。房主(玩家)可以选择基础模板，或者根据需要让API即时生成一个独特的背景故事。这样，每局游戏都有其独特的背景，让玩家仿佛置身于一个真实的世界中。
角色身份Agent：在游戏开始前，玩家将从角色背景模板中选择一个角色。随后角色身份agent将在所选模板基础上生成本局游戏的角色身份。每个角色都有其独特的背景故事和技能，让玩家在游戏过程中体验到不同的角色扮演乐趣。
初始装备：为了增加游戏的策略性，玩家在游戏开始时可以从先前保存的最多三张卡牌中进行选择，作为自己的初始装备。这些卡牌可以是武器、防具或其他特殊道具，为玩家在游戏中的行动提供支持。
行动生成Agent：行动生成agent负责为每轮玩家行动生成四选一的行动选项。这些行动选项将根据游戏的进程和当前的背景故事进行动态调整，确保每一轮的决策都充满挑战和不确定性。
抽卡生图Agent：玩家根据所选行动的文字描述生成相应的行动卡牌。每张卡牌下方附有背景故事，上方展示卡牌效果数值。卡牌内容的最终生成将确保图文一致性，并符合游戏世界观，以控制实际效果。这样，玩家在游戏过程中不仅能体验到策略和决策的乐趣，还能享受到视觉上的享受。
分数和成就统计Agent：游戏结束后，agent将负责生成玩家的积分和成就统计。
卡片管理API：为了方便玩家保存和管理自己的游戏经历和卡牌信息，卡片管理API应运而生。玩家在每次游戏结束时，可以选择保存每局游戏中使用过的行动卡牌中的一张，并在游戏后在卡片管理页面进行管理。这样，玩家可以随时回顾自己的游戏经历，也可以与其他玩家分享自己的卡牌收藏。

二阶段开发内容
游戏内通讯Agent：为了加强玩家之间的互动和合作，游戏内通讯Agent提供实时的语音和文字通讯功能。玩家可以通过这个功能与队友进行沟通，制定战术和分享信息，从而提高团队协作的效率。
任务更新Agent：随着游戏进程的推进，任务更新Agent将根据玩家的行动和游戏背景故事，动态生成新的任务目标。这些任务目标将引导玩家进行下一步行动，同时为游戏带来更多的变数和挑战。
环境互动Agent：为了让游戏世界更加真实，环境互动Agent允许玩家与游戏中的环境进行互动。玩家可以利用环境中的道具或地形来帮助自己完成任务，或者在关键时刻改变局势。
成就解锁Agent：在游戏过程中，成就解锁Agent将记录玩家的行动和成就。每当玩家完成特定的任务或达到一定的里程碑时，成就解锁Agent将为玩家提供相应的奖励和解锁新的成就，激励玩家不断挑战自我。
游戏平衡Agent：为了确保游戏的公平性和可玩性，游戏平衡Agent会对游戏中的各种因素进行实时监控和调整。它将根据玩家的表现和游戏进程，动态调整卡牌效果数值和行动选项的难度，以保持游戏的平衡。
游戏存档Agent：为了方便玩家随时中断和继续游戏，游戏存档Agent将自动保存玩家的游戏进度。玩家可以在任何时候中断游戏，并在之后重新加载进度，继续未完成的游戏进程。
社交分享Agent：为了让玩家能够分享自己的游戏体验，社交分享Agent提供一键分享功能。玩家可以将游戏中的精彩瞬间或成就分享到社交媒体上，与朋友和家人分享自己的游戏乐趣。


数据库设计
-- 玩家基本信息表  
CREATE TABLE user_base_info (  
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户id',  
    username VARCHAR(32) NOT NULL UNIQUE COMMENT '用户名(登录用)',  
    password_hash VARCHAR(64) NOT NULL COMMENT '密码哈希',  
    email VARCHAR(32) UNIQUE COMMENT '电子邮箱(登录用)',  
    phone_number VARCHAR(15) UNIQUE COMMENT '电话号码(登录用)',  
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态: 1-激活, 0-未激活',  
    gender ENUM('m', 'f', 'o') DEFAULT 'o' COMMENT '性别: m=male, f=female, o=other',  
    birthdate DATE NULL COMMENT '出生日期',  
    country VARCHAR(100) NULL COMMENT '国家',  
    city VARCHAR(100) NULL COMMENT '城市',  
    invite_code VARCHAR(16) NULL COMMENT '邀请码(16位)',  
    is_verified TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否通过实名验证',  
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',  
    login_ip VARCHAR(45) NULL COMMENT '最后登录IP',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='玩家基本信息表';  
  
-- 玩家对外信息表  
CREATE TABLE user_out_info (  
    user_id INT PRIMARY KEY COMMENT '用户id',  
    score INT NOT NULL DEFAULT 0 COMMENT '分数',  
    game_count INT NOT NULL DEFAULT 0 COMMENT '游戏局数计数',  
    avatar_url VARCHAR(64) COMMENT '头像URL(64位)',  
    level INT NOT NULL DEFAULT 1 COMMENT '玩家等级',  
    rank INT NULL COMMENT '昨日积分排名',  
    last_game_uuid CHAR(36) NULL COMMENT '最近游戏uuid',  
    achievements VARCHAR(255) NULL COMMENT '玩家成就id(逗号分隔)',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' 
) COMMENT='玩家对外信息表';  
  
-- 玩家游戏记录表  
CREATE TABLE user_game_info (  
    user_id INT COMMENT '用户id',  
    game_uuid CHAR(36) COMMENT '游戏uuid 有序二进制uuid',  
    score INT NOT NULL DEFAULT 0 COMMENT '本局游戏给与本玩家的分数',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',  
    achievements VARCHAR(255) NULL COMMENT '本局游戏给与本玩家的成就id(逗号分隔的TEXT格式)',  
    game_type VARCHAR(100) NULL COMMENT '游戏类型',  
    story_id INT NULL COMMENT '本局游戏的故事背景模板id',  
    user_story_id INT NULL COMMENT '本局游戏的本玩家使用的角色背景模板id',  
    game_mode ENUM('s', 'm') DEFAULT 's' COMMENT '游戏模式: s=单人, m=多人',  
    duration INT NULL DEFAULT 0 COMMENT '游戏持续时间(秒)',  
    result ENUM('w', 'l', 'd') DEFAULT 'd' COMMENT '游戏结果: w=win, l=lose, d=draw(游戏未正常结束记为平局/流局)',  
    opponents VARCHAR(255) NULL COMMENT '对手用户名(逗号分割)',  
    game_version VARCHAR(50) NULL COMMENT '游戏数据版本',  
    player_count INT NOT NULL DEFAULT 1 COMMENT '玩家数量',  
    PRIMARY KEY (user_id, game_uuid)  
) COMMENT='玩家游戏记录表';  
  
-- 故事背景模板表  
CREATE TABLE story_template (  
    story_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '故事模板id',  
    story_name VARCHAR(255) NOT NULL COMMENT '故事模板名称',  
    story_details VARCHAR(500) NULL COMMENT '故事模板描述',  
    story_image_url VARCHAR(64) COMMENT '故事图像URL(64位)',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='故事背景模板表';  
  
-- 角色背景模板表  
CREATE TABLE character_template (  
    character_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '角色模板id',  
    character_name VARCHAR(255) NOT NULL COMMENT '角色模板名称',  
    character_details VARCHAR(500) NULL COMMENT '角色模板描述',  
    character_image_url VARCHAR(64) COMMENT '角色图像URL(64位)',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='角色背景模板表';  
  
-- 卡信息表  
CREATE TABLE card_info (  
    card_uuid CHAR(36) PRIMARY KEY COMMENT '卡片模板uuid 有序二进制uuid',  
    card_name VARCHAR(255) NOT NULL COMMENT '卡片名称',  
    card_details VARCHAR(500) NULL COMMENT '卡片描述',  
    card_image_url VARCHAR(64) COMMENT '卡片图像URL(64位)',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='卡信息表';  
  
-- 成就信息表  
CREATE TABLE achievements_info (  
    achievement_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '成就id',  
    achievement_name VARCHAR(255) NOT NULL COMMENT '成就名称',  
    achievement_details VARCHAR(500) NULL COMMENT '成就描述',  
    achievement_image_url VARCHAR(64) COMMENT '成就图像URL(64位)',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='成就信息表';

