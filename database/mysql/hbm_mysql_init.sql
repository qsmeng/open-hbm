-- 删除表，如果表存在
-- DROP TABLE IF EXISTS hbm_db.user_base_info;
-- 玩家基本信息表
CREATE TABLE hbm_db.user_base_info (  
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

-- 删除表，如果表存在
-- DROP TABLE IF EXISTS hbm_db.user_out_info;
-- 玩家对外信息表
CREATE TABLE hbm_db.user_out_info (  
    user_id INT PRIMARY KEY COMMENT '用户id',
    score INT NOT NULL DEFAULT 0 COMMENT '分数',
    game_count INT NOT NULL DEFAULT 0 COMMENT '游戏局数计数',
    avatar_url VARCHAR(64) COMMENT '头像URL(64位)',
    level INT NOT NULL DEFAULT 1 COMMENT '玩家等级',
    yesterday_rank INT NULL COMMENT '昨日积分排名',
    last_game_uuid CHAR(36) NULL COMMENT '最近游戏uuid',
    achievements VARCHAR(255) NULL COMMENT '玩家成就id(逗号分隔)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' 
) COMMENT='玩家对外信息表';  

-- 删除表，如果表存在
-- DROP TABLE IF EXISTS hbm_db.user_game_info;
-- 玩家游戏记录表
CREATE TABLE hbm_db.user_game_info (  
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
-- 删除表，如果表存在
-- DROP TABLE IF EXISTS hbm_db.story_template;
-- 故事背景模板表
CREATE TABLE hbm_db.story_template (  
    story_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '故事模板id',
    story_name VARCHAR(255) NOT NULL COMMENT '故事模板名称',
    story_details VARCHAR(500) NULL COMMENT '故事模板描述',
    story_image_url VARCHAR(64) COMMENT '故事图像URL(64位)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='故事背景模板表';  
  
-- 删除表，如果表存在
-- DROP TABLE IF EXISTS hbm_db.card_info;
-- 卡信息表  
CREATE TABLE hbm_db.card_info (  
    card_uuid CHAR(36) PRIMARY KEY COMMENT '卡片模板uuid 有序二进制uuid',
    card_name VARCHAR(255) NOT NULL COMMENT '卡片名称',
    card_details VARCHAR(500) NULL COMMENT '卡片描述',
    card_image_url VARCHAR(64) COMMENT '卡片图像URL(64位)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='卡信息表';  
  
-- 删除表，如果表存在
-- DROP TABLE IF EXISTS hbm_db.achievements_info;
-- 成就信息表  
CREATE TABLE hbm_db.achievements_info (  
    achievement_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '成就id',
    achievement_name VARCHAR(255) NOT NULL COMMENT '成就名称',
    achievement_details VARCHAR(500) NULL COMMENT '成就描述',
    achievement_image_url VARCHAR(64) COMMENT '成就图像URL(64位)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'  
) COMMENT='成就信息表';