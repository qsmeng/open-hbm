以下是根据项目代码分析生成的包含架构图、类图和流程图的 Markdown 文档：
  - [wolf_game](https://github.com/hikariming/AIWolfGame)：AI狼人杀游戏

# AI 狼人杀模拟器项目架构分析

## 架构图
```mermaid
graph LR
    classDef process fill:#E5F6FF,stroke:#73A6FF,stroke-width:2px
    
    A(命令行界面):::process -->|参数输入| B(主程序 main.py):::process
    B -->|加载配置| C(config 目录):::process
    C -->|角色配置| B
    C -->|AI 配置| B
    B -->|初始化| D(日志系统 logger.py):::process
    B -->|创建实例| E(游戏控制器 game_controller.py):::process
    E -->|管理| F(AI 玩家 ai_players.py):::process
    E -->|调用| G(游戏工具 game_utils.py):::process
    F -->|使用| H(角色定义 roles.py):::process
    D -->|记录| I(logs 目录):::process
    E -->|保存统计| J(统计数据):::process
    B -->|导出分析| K(分析数据):::process
```
**说明**：
- 命令行界面通过参数输入启动主程序。
- 主程序加载配置文件，初始化日志系统，并创建游戏控制器实例。
- 游戏控制器管理 AI 玩家，调用游戏工具函数。
- AI 玩家使用角色定义。
- 日志系统记录游戏过程到日志目录。
- 游戏结束后，主程序导出分析数据。

## 类图
```mermaid
classDiagram
    class BaseRole {
        +is_wolf()
    }
    class BaseAIAgent {
        +__init__(config: Dict, role: BaseRole)
        +ask_ai(prompt: str, system_prompt: str)
        +_extract_target(response: str)
        +discuss(game_state: Dict)
        +vote(game_state: Dict)
        +last_words(game_state: Dict)
    }
    class WerewolfAgent {
        +__init__(config: Dict, role: BaseRole)
        +discuss(game_state: Dict)
        +vote(game_state: Dict)
    }
    class VillagerAgent {
        +__init__(config: Dict, role: BaseRole)
        +discuss(game_state: Dict)
        +vote(game_state: Dict)
    }
    class SeerAgent {
        +__init__(config: Dict, role: BaseRole)
        +check_player(game_state: Dict)
    }
    class WitchAgent {
        +__init__(config: Dict, role: BaseRole)
        +use_potion(game_state: Dict, victim_id: str)
    }
    class HunterAgent {
        +__init__(config: Dict, role: BaseRole)
        +shoot(game_state: Dict)
    }
    class GameController {
        +__init__(game_config: Dict)
        +run_game()
        +check_game_over()
    }
    class GameLogger {
        +__init__(debug: bool)
        +log_round(round_num: int, phase: str, events: List)
        +log_event(event_type: str, details: Dict)
        +log_game_over(winner: str, final_state: Dict)
        +save_game_record()
    }
    BaseAIAgent <|-- WerewolfAgent
    BaseAIAgent <|-- VillagerAgent
    BaseAIAgent <|-- SeerAgent
    BaseAIAgent <|-- WitchAgent
    BaseAIAgent <|-- HunterAgent
    GameController --> BaseAIAgent : 管理
    GameController --> GameLogger : 记录日志
```
**说明**：
- `BaseRole` 是角色的基类，定义了判断是否为狼人的方法。
- `BaseAIAgent` 是 AI 玩家的基类，定义了通用的方法。
- `WerewolfAgent`、`VillagerAgent`、`SeerAgent`、`WitchAgent` 和 `HunterAgent` 继承自 `BaseAIAgent`，并实现了各自的特殊方法。
- `GameController` 管理游戏流程，与 AI 玩家交互，并使用 `GameLogger` 记录日志。

## 流程图
```mermaid
graph TD
    classDef process fill:#E5F6FF,stroke:#73A6FF,stroke-width:2px
    
    A(开始):::process --> B(解析命令行参数):::process
    B --> C(加载配置文件):::process
    C --> D{配置验证}:::process
    D -- 失败 --> E(输出错误信息，退出):::process
    D -- 成功 --> F(初始化日志系统):::process
    F --> G{是否继续游戏}:::process
    G -- 是 --> H(加载断点数据):::process
    G -- 否 --> I(初始化统计数据):::process
    H --> I
    I --> J(开始游戏轮次循环):::process
    J --> K(分配模型到角色):::process
    K --> L(创建游戏实例):::process
    L --> M(运行游戏):::process
    M --> N{游戏是否结束}:::process
    N -- 否 --> M
    N -- 是 --> O(获取游戏结果):::process
    O --> P(更新统计数据):::process
    P --> Q(保存断点和导出分析):::process
    Q --> R{是否完成所有轮次}:::process
    R -- 否 --> J
    R -- 是 --> S(打印最终统计结果):::process
    S --> T(结束):::process
```
**说明**：
1. 程序开始后，解析命令行参数，加载配置文件并进行验证。
2. 初始化日志系统，根据用户选择决定是否从断点继续游戏。
3. 进入游戏轮次循环，分配模型到角色，创建游戏实例并运行游戏。
4. 游戏结束后，获取结果，更新统计数据，保存断点和导出分析。
5. 检查是否完成所有轮次，若未完成则继续循环，否则打印最终统计结果并结束程序。