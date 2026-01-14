# 系统架构

## 整体设计

```mermaid
flowchart TB
    subgraph Frontend["🖥️ Frontend"]
        UI["💬 Web UI"]
        NoVNC["🖼️ NoVNC"]
    end

    subgraph Backend["⚙️ Backend"]
        API["🔌 REST API"]
        subgraph Agent["🤖 PlanAct Agent"]
            Planner["📋 Planner"]
            Executor["⚡ Executor"]
        end
        Tools["🔧 Tools"]
    end

    subgraph Sandbox["📦 Sandbox"]
        Shell["💻 Shell"]
        File["📁 File"]
        Chrome["🌐 Chrome"]
        VNC["🖥️ VNC"]
    end

    subgraph Storage["💾 Storage"]
        MongoDB[("🍃 MongoDB")]
        Redis[("⚡ Redis")]
    end

    UI -->|HTTP| API
    API -->|SSE| UI
    NoVNC -.->|WebSocket| VNC
    API --> Agent
    Planner <--> Executor
    Executor --> Tools
    Tools --> Sandbox
    API --> Storage
```

## 核心组件

### 1. Frontend (前端)

- **技术栈**: Vue 3 + TypeScript + Vite
- **主要功能**:
  - 聊天界面 (ChatPage)
  - 浏览器远程预览 (NoVNC)
  - 实时事件展示 (SSE)

### 2. Backend (后端)

- **技术栈**: FastAPI + Python
- **架构模式**: DDD (领域驱动设计)

```mermaid
flowchart TB
    subgraph Backend["🏗️ Backend DDD 架构"]
        subgraph Interfaces["📡 接口层"]
            Routes["FastAPI Routes"]
        end

        subgraph Application["📦 应用层"]
            Services["编排服务"]
        end

        subgraph Domain["💎 领域层"]
            Models["领域模型"]
            Agents["🤖 Agents"]
            ToolSvc["🔧 Tools"]
        end

        subgraph Infra["🔩 基础设施层"]
            LLM["LLM"]
            DB["Database"]
        end
    end

    Routes --> Services --> Domain --> Infra
```

### 3. Sandbox (沙箱)

- **基础镜像**: Ubuntu 22.04
- **进程管理**: Supervisor
- **内置服务**:

| 服务 | 端口 | 用途 |
|------|------|------|
| FastAPI | 8080 | Shell/File API |
| Chrome | 9222 | CDP 远程调试 |
| VNC | 5900 | 远程桌面 |
| WebSockify | 5901 | WebSocket 代理 |

```mermaid
flowchart LR
    subgraph Sandbox["📦 Sandbox 容器"]
        subgraph APIs["🔌 APIs"]
            ShellAPI["Shell"]
            FileAPI["File"]
        end
        Chrome["🌐 Chrome"]
        VNCServer["🖥️ VNC"]
    end

    BE["Backend"] --> APIs
    BE --> Chrome
    FE["Frontend"] -.-> VNCServer
```

## 请求处理流程

```mermaid
sequenceDiagram
    participant U as 👤 用户
    participant F as 🖥️ Frontend
    participant B as ⚙️ Backend
    participant P as 📋 Planner
    participant E as ⚡ Executor
    participant S as 📦 Sandbox

    U->>F: 发送消息
    F->>B: HTTP Request
    B->>S: 创建容器
    B->>P: 分析任务
    P->>P: 生成计划

    loop 执行步骤
        P->>E: 分配步骤
        E->>S: 调用工具
        S-->>E: 返回结果
        E-->>P: 报告进度
        B-->>F: SSE Event
    end

    P->>B: 完成
    B-->>F: 完成事件
```

## 工具系统

```mermaid
flowchart TB
    subgraph Tools["🔧 工具系统"]
        subgraph Browser["🌐 Browser"]
            nav["navigate"]
            click["click"]
            input["input"]
        end

        subgraph Shell["💻 Shell"]
            exec["exec"]
            view["view"]
        end

        subgraph File["📁 File"]
            read["read"]
            write["write"]
        end

        subgraph Other["🔍 Other"]
            search["search"]
            ask["ask_user"]
        end
    end
```

| 工具类别 | 工具名称 | 功能 |
|---------|---------|------|
| **Browser** | navigate | 访问 URL |
| | click | 点击元素 |
| | input | 输入文本 |
| | view | 查看页面 |
| **Shell** | exec | 执行命令 |
| | view | 查看输出 |
| **File** | read | 读取文件 |
| | write | 写入文件 |
| **Search** | web_search | 网络搜索 |

### 工具调用流程

```mermaid
flowchart LR
    A["🤖 LLM"] --> B["📝 解析"]
    B --> C["⚡ 执行"]
    C --> D["📡 事件"]
    D --> E["✅ 返回"]
```

## 数据存储

### 整体架构

```mermaid
flowchart TB
    subgraph Backend["⚙️ Backend"]
        API["REST API"]
        Agent["Agent"]
        TaskMgr["Task Manager"]
    end

    subgraph MongoDB["🍃 MongoDB - 持久化存储"]
        Sessions[("会话记录")]
        Messages[("消息历史")]
        Files[("文件元数据")]
        GridFS[("GridFS<br/>大文件存储")]
    end

    subgraph Redis["⚡ Redis - 高速缓存与实时通信"]
        subgraph Cache["缓存层"]
            SessionCache["会话缓存"]
            ResultCache["结果缓存"]
        end
        subgraph Realtime["实时通信"]
            PubSub["Pub/Sub<br/>事件广播"]
            SSEChannel["SSE 通道"]
        end
        subgraph Queue["任务队列"]
            TaskQueue["后台任务"]
            ScheduleQueue["定时任务"]
        end
    end

    API --> SessionCache
    API --> Sessions
    Agent --> ResultCache
    Agent --> Messages
    TaskMgr --> TaskQueue
    TaskMgr --> ScheduleQueue
    API --> PubSub
    PubSub --> SSEChannel
```

### 用户任务处理流程

```mermaid
flowchart LR
    subgraph Input["📥 输入"]
        Request["用户请求"]
        Event["Agent 事件"]
        Task["后台任务"]
    end

    subgraph RedisFlow["⚡ Redis 处理流程"]
        direction TB
        subgraph CacheFlow["🔄 缓存流程"]
            Check["检查缓存"] --> Hit{"命中?"}
            Hit -->|"Yes"| Return["返回缓存"]
            Hit -->|"No"| Query["查询 MongoDB"]
            Query --> Store["写入缓存"]
            Store --> Return
        end

        subgraph PubSubFlow["📡 Pub/Sub 流程"]
            Publish["发布事件"] --> Channel["频道"]
            Channel --> Sub1["订阅者 1"]
            Channel --> Sub2["订阅者 2"]
            Channel --> SubN["订阅者 N"]
        end

        subgraph QueueFlow["📋 队列流程"]
            Push["入队"] --> Queue["任务队列"]
            Queue --> Pop["出队"]
            Pop --> Worker["Worker 处理"]
        end
    end

    Request --> CacheFlow
    Event --> PubSubFlow
    Task --> QueueFlow
```

### 关键功能

| 功能 | 用途 | 数据结构 |
|------|------|----------|
| **会话缓存** | 加速会话数据读取 | String/Hash |
| **结果缓存** | 缓存工具执行结果 | String |
| **Pub/Sub** | SSE 事件实时广播 | Channel |
| **任务队列** | 后台任务调度 | List/Sorted Set |
| **定时任务** | 定时执行任务 | Sorted Set |
| **分布式锁** | 防止并发冲突 | String + SETNX |

### 数据流时序

```mermaid
sequenceDiagram
    participant C as 👤 客户端
    participant A as ⚙️ API
    participant R as ⚡ Redis
    participant M as 🍃 MongoDB

    Note over R: 缓存读取流程
    C->>A: 请求会话数据
    A->>R: GET session:123
    alt 缓存命中
        R-->>A: 返回缓存数据
    else 缓存未命中
        R-->>A: null
        A->>M: 查询数据库
        M-->>A: 返回数据
        A->>R: SET session:123 (TTL)
    end
    A-->>C: 返回响应

    Note over R: Pub/Sub 事件广播
    A->>R: PUBLISH events:session:123
    R-->>C: SSE 推送事件

    Note over R: 任务队列处理
    A->>R: LPUSH task_queue
    R->>A: BRPOP task_queue
    A->>A: 执行任务
```

## 配置说明

| 变量 | 说明 |
|------|------|
| `API_KEY` | LLM API 密钥 |
| `API_BASE` | LLM API 地址 |
| `MODEL_NAME` | 模型名称 |
| `SANDBOX_IMAGE` | Docker 镜像 |
| `AUTH_PROVIDER` | 认证方式 |
