# System Architecture

## Overall Design

```mermaid
flowchart TB
    subgraph Frontend["Frontend (Vue 3)"]
        UI["Web UI<br/>Chat Interface"]
        NoVNC["NoVNC<br/>Remote Preview"]
    end

    subgraph Backend["Backend (FastAPI)"]
        API["REST API"]
        subgraph Agent["PlanAct Agent"]
            Planner["Planner Agent<br/>Task Planning"]
            Executor["Execution Agent<br/>Step Execution"]
        end
        Tools["Tool Services"]
    end

    subgraph Sandbox["Sandbox (Docker)"]
        Shell["Shell API"]
        File["File API"]
        Chrome["Chrome CDP"]
        VNC["VNC Server"]
    end

    subgraph Storage["Storage"]
        MongoDB[("MongoDB<br/>Sessions/Messages")]
        Redis[("Redis<br/>Cache")]
    end

    UI -->|"HTTP Request"| API
    API -->|"SSE Events"| UI
    NoVNC -->|"WebSocket"| VNC
    API --> Agent
    Planner <-->|"Collaboration"| Executor
    Executor --> Tools
    Tools -->|"HTTP/CDP"| Sandbox
    API --> Storage
```

## Core Components

### 1. Frontend

- **Tech Stack**: Vue 3 + TypeScript + Vite
- **Main Features**:
  - Chat Interface (ChatPage)
  - Remote Browser Preview (NoVNC)
  - Real-time Event Display (SSE)

### 2. Backend

- **Tech Stack**: FastAPI + Python
- **Architecture Pattern**: DDD (Domain-Driven Design)

```mermaid
flowchart TB
    subgraph Backend["Backend Architecture (DDD)"]
        subgraph Interfaces["Interface Layer interfaces/"]
            Routes["FastAPI Routes"]
        end

        subgraph Application["Application Layer application/"]
            Services["Orchestration Services"]
        end

        subgraph Domain["Domain Layer domain/"]
            Models["Domain Models<br/>Plan, Step, Message, Skill"]
            DomainServices["Domain Services"]
            subgraph Agents["agents/"]
                PlannerAgent["Planner Agent"]
                ExecAgent["Execution Agent"]
            end
            subgraph ToolServices["tools/"]
                BrowserTool["Browser"]
                ShellTool["Shell"]
                FileTool["File"]
                SearchTool["Search"]
            end
        end

        subgraph Infrastructure["Infrastructure Layer infrastructure/"]
            LLM["LLM Implementation<br/>OpenAI, Anthropic"]
            BrowserImpl["Browser Implementation<br/>Playwright"]
            SandboxImpl["Sandbox Implementation<br/>Docker"]
        end
    end

    Routes --> Services
    Services --> Domain
    Domain --> Infrastructure
```

### 3. Sandbox

- **Base Image**: Ubuntu 22.04
- **Process Manager**: Supervisor
- **Built-in Services**:

| Service | Port | Purpose |
|---------|------|---------|
| FastAPI | 8080 | Shell/File API |
| Chrome | 9222 | CDP Remote Debugging |
| VNC | 5900 | Remote Desktop |
| WebSockify | 5901 | VNC WebSocket Proxy |

```mermaid
flowchart LR
    subgraph Sandbox["Sandbox Container"]
        subgraph APIs["API Services"]
            ShellAPI["Shell API<br/>:8080"]
            FileAPI["File API<br/>:8080"]
        end
        subgraph Browser["Browser Service"]
            Chrome["Chrome<br/>:9222 CDP"]
        end
        subgraph Remote["Remote Desktop"]
            VNCServer["VNC Server<br/>:5900"]
            WebSockify["WebSockify<br/>:5901"]
        end
    end

    Backend["Backend"] -->|HTTP| APIs
    Backend -->|CDP| Browser
    Frontend["Frontend"] -->|WebSocket| WebSockify
    WebSockify --> VNCServer
```

## Request Processing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant P as Planner Agent
    participant E as Execution Agent
    participant S as Sandbox

    U->>F: Send Message
    F->>B: HTTP Request
    B->>S: Create Docker Container
    activate S
    B->>P: Analyze Task
    activate P
    P->>P: Generate Execution Plan

    loop Execute Each Step
        P->>E: Assign Step
        activate E
        E->>S: Call Tools (Browser/Shell/File)
        S-->>E: Return Result
        E-->>P: Report Progress
        deactivate E
        P-->>B: Update Plan Status
        B-->>F: SSE Event
        F-->>U: Real-time Update
    end

    P->>B: Task Complete
    deactivate P
    B-->>F: Completion Event
    F-->>U: Display Result
    deactivate S
```

## Tool System

### Available Tools

```mermaid
flowchart TB
    subgraph Tools["Tool System"]
        subgraph BrowserTools["Browser Tools"]
            navigate["browser_navigate<br/>Visit URL"]
            click["browser_click<br/>Click Element"]
            input["browser_input<br/>Input Text"]
            view["browser_view<br/>View Page"]
            scroll["browser_scroll<br/>Scroll Page"]
        end

        subgraph ShellTools["Shell Tools"]
            exec["shell_exec<br/>Execute Command"]
            shell_view["shell_view<br/>View Output"]
            write["shell_write<br/>Write Input"]
        end

        subgraph FileTools["File Tools"]
            read["file_read<br/>Read File"]
            file_write["file_write<br/>Write File"]
            search["file_search<br/>Search Files"]
        end

        subgraph OtherTools["Other Tools"]
            web_search["web_search<br/>Web Search"]
            ask_user["message_ask_user<br/>Ask User"]
        end
    end
```

| Category | Tool Name | Function |
|----------|-----------|----------|
| **Browser** | browser_navigate | Visit URL |
| | browser_click | Click Element |
| | browser_input | Input Text |
| | browser_view | View Page Content |
| | browser_scroll_up/down | Scroll Page |
| **Shell** | shell_exec | Execute Command |
| | shell_view | View Output |
| | shell_write | Write Input |
| **File** | file_read | Read File |
| | file_write | Write File |
| | file_search | Search Files |
| **Search** | web_search | Web Search |
| **Message** | message_ask_user | Ask User |

### Tool Invocation Flow

```mermaid
flowchart LR
    LLM["LLM Output<br/>Tool Call"] --> Parse["Parse Tool Call"]
    Parse --> Execute["Execute Tool Method<br/>BaseTool.execute()"]
    Execute --> Event["Send ToolEvent<br/>SSE Push"]
    Event --> Result["Return Result to LLM"]
```

## Data Storage

### Overall Architecture

```mermaid
flowchart TB
    subgraph Backend["⚙️ Backend"]
        API["REST API"]
        Agent["Agent"]
        TaskMgr["Task Manager"]
    end

    subgraph MongoDB["🍃 MongoDB - Persistent Storage"]
        Sessions[("Session Records")]
        Messages[("Message History")]
        Files[("File Metadata")]
        GridFS[("GridFS<br/>Large File Storage")]
    end

    subgraph Redis["⚡ Redis - High-Speed Cache & Real-time Communication"]
        subgraph Cache["Cache Layer"]
            SessionCache["Session Cache"]
            ResultCache["Result Cache"]
        end
        subgraph Realtime["Real-time Communication"]
            PubSub["Pub/Sub<br/>Event Broadcasting"]
            SSEChannel["SSE Channel"]
        end
        subgraph Queue["Task Queue"]
            TaskQueue["Background Tasks"]
            ScheduleQueue["Scheduled Tasks"]
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

### Redis Functionality Flow

```mermaid
flowchart LR
    subgraph Input["📥 Input"]
        Request["User Request"]
        Event["Agent Event"]
        Task["Background Task"]
    end

    subgraph RedisFlow["⚡ Redis Processing Flow"]
        direction TB
        subgraph CacheFlow["🔄 Cache Flow"]
            Check["Check Cache"] --> Hit{"Hit?"}
            Hit -->|"Yes"| Return["Return Cached"]
            Hit -->|"No"| Query["Query MongoDB"]
            Query --> Store["Write to Cache"]
            Store --> Return
        end

        subgraph PubSubFlow["📡 Pub/Sub Flow"]
            Publish["Publish Event"] --> Channel["Channel"]
            Channel --> Sub1["Subscriber 1"]
            Channel --> Sub2["Subscriber 2"]
            Channel --> SubN["Subscriber N"]
        end

        subgraph QueueFlow["📋 Queue Flow"]
            Push["Enqueue"] --> Queue["Task Queue"]
            Queue --> Pop["Dequeue"]
            Pop --> Worker["Worker Process"]
        end
    end

    Request --> CacheFlow
    Event --> PubSubFlow
    Task --> QueueFlow
```

### Redis Core Functions

| Function | Purpose | Data Structure |
|----------|---------|----------------|
| **Session Cache** | Accelerate session data reads | String/Hash |
| **Result Cache** | Cache tool execution results | String |
| **Pub/Sub** | SSE event real-time broadcasting | Channel |
| **Task Queue** | Background task scheduling | List/Sorted Set |
| **Scheduled Tasks** | Timed task execution | Sorted Set |
| **Distributed Lock** | Prevent concurrent conflicts | String + SETNX |

### Data Flow Sequence

```mermaid
sequenceDiagram
    participant C as 👤 Client
    participant A as ⚙️ API
    participant R as ⚡ Redis
    participant M as 🍃 MongoDB

    Note over R: Cache Read Flow
    C->>A: Request Session Data
    A->>R: GET session:123
    alt Cache Hit
        R-->>A: Return Cached Data
    else Cache Miss
        R-->>A: null
        A->>M: Query Database
        M-->>A: Return Data
        A->>R: SET session:123 (TTL)
    end
    A-->>C: Return Response

    Note over R: Pub/Sub Event Broadcasting
    A->>R: PUBLISH events:session:123
    R-->>C: SSE Push Event

    Note over R: Task Queue Processing
    A->>R: LPUSH task_queue
    R->>A: BRPOP task_queue
    A->>A: Execute Task
```

## Configuration

Key Environment Variables:

| Variable | Description |
|----------|-------------|
| `API_KEY` | LLM API Key |
| `API_BASE` | LLM API Base URL |
| `MODEL_NAME` | Model Name |
| `SANDBOX_IMAGE` | Sandbox Docker Image |
| `AUTH_PROVIDER` | Auth Mode (password/local/none) |
