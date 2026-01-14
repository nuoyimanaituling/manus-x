# Plan Agent Implementation

## Overview

Plan Agent is the core component of ManusX, implementing a **Plan-Act** pattern for task planning and execution. This pattern breaks down complex tasks into manageable steps and completes objectives through iterative execution and dynamic adjustment.

## Architecture Design

```mermaid
flowchart TB
    subgraph PlanAct["Plan-Act Execution Flow"]
        UserMsg["User Message"] --> Planner1["Planner Agent<br/>Create Plan"]
        Planner1 --> |"Plan { title, steps[], language }"| Executor["Execution Agent<br/>Execute Steps"]
        Executor --> |"Call Tools"| Tools["Browser / Shell / File / Search"]
        Tools --> |"Return Results"| Executor
        Executor --> |"Step Complete"| Planner2["Planner Agent<br/>Update Plan"]
        Planner2 --> |"Continue Execution"| Executor
        Planner2 --> |"All Complete"| Done["Task Complete"]
    end
```

### State Transitions

```mermaid
stateDiagram-v2
    [*] --> Planning: Receive User Message
    Planning --> Executing: Plan Ready
    Executing --> Updating: Step Complete
    Updating --> Executing: More Steps Pending
    Updating --> Completed: All Steps Complete
    Executing --> Failed: Execution Failed
    Planning --> Failed: Planning Failed
    Completed --> [*]
    Failed --> [*]
```

## Core Models

### Plan Model

```python
# backend/app/domain/models/plan.py

class Plan(BaseModel):
    title: str              # Plan title
    steps: List[Step]       # Execution steps list
    language: str = "en"    # Response language
```

### Step Model

```mermaid
flowchart LR
    subgraph Step["Step Model"]
        desc["description<br/>Step description"]
        status["status<br/>Execution status"]
        result["result<br/>Execution result"]
        success["success<br/>Success flag"]
        error["error<br/>Error message"]
        attach["attachments<br/>Attachment list"]
    end
```

```python
class Step(BaseModel):
    description: str                    # Step description
    status: ExecutionStatus = PENDING   # Execution status
    result: Optional[str] = None        # Execution result
    success: Optional[bool] = None      # Success flag
    error: Optional[str] = None         # Error message
    attachments: List[str] = []         # Attachment list

class ExecutionStatus(str, Enum):
    PENDING = "pending"       # Pending
    RUNNING = "running"       # Running
    COMPLETED = "completed"   # Completed
    FAILED = "failed"         # Failed
```

### Status Transitions

```mermaid
stateDiagram-v2
    [*] --> PENDING: Create Step
    PENDING --> RUNNING: Start Execution
    RUNNING --> COMPLETED: Execution Success
    RUNNING --> FAILED: Execution Failed
    COMPLETED --> [*]
    FAILED --> [*]
```

## Core Components

### 1. Planner Agent

**Responsibility**: Analyze user requirements, generate and update execution plans

**Key File**: `backend/app/domain/services/agents/planner.py`

```mermaid
flowchart TB
    subgraph PlannerAgent["Planner Agent"]
        Input["Input: User Message + Attachments"]
        Analyze["Analyze Task Requirements"]
        Generate["Generate Execution Plan"]
        Output["Output: Plan JSON"]
    end

    Input --> Analyze --> Generate --> Output
```

### 2. Execution Agent

**Responsibility**: Execute each step in the plan, call tools to complete specific tasks

**Key File**: `backend/app/domain/services/agents/execution.py`

```mermaid
flowchart TB
    subgraph ExecutionAgent["Execution Agent"]
        GetStep["Get Current Step"]
        Execute["Execute Step"]
        CallTool["Call Tools"]
        GetResult["Get Result"]
        Report["Report Status"]
    end

    GetStep --> Execute --> CallTool --> GetResult --> Report
```

### 3. Base Agent

**Responsibility**: Provide base Agent capabilities including LLM calls, tool execution, state management

**Key File**: `backend/app/domain/services/agents/base.py`

```mermaid
flowchart LR
    subgraph BaseAgent["Base Agent"]
        Build["Build Messages"]
        LLM["Call LLM"]
        Parse["Parse Response"]
        Tool["Execute Tools"]
        Return["Return Results"]
    end

    Build --> LLM --> Parse --> Tool --> Return
```

## Execution Flow Details

### Complete Execution Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant P as Planner Agent
    participant E as Execution Agent
    participant T as Tools
    participant F as Frontend

    U->>P: Send Task Request
    P->>P: Analyze Task
    P->>F: PlanEvent (CREATED)

    loop Execute Each Step
        P->>E: Assign Step
        E->>F: StepEvent (STARTED)
        E->>T: Call Tools
        T-->>E: Return Results
        E->>F: ToolEvent
        E->>F: StepEvent (COMPLETED)
        E->>P: Report Completion
        P->>P: Update Plan
        P->>F: PlanEvent (UPDATED)
    end

    P->>F: PlanEvent (COMPLETED)
    F->>U: Display Final Results
```

### 1. Plan Creation Phase

```mermaid
flowchart LR
    User["User: Search AI Agent on<br/>Baidu and summarize top 3 results"] --> Planner["Planner Agent"]
    Planner --> Plan["Plan:<br/>1. Open Baidu search page<br/>2. Input AI Agent and search<br/>3. Extract top 3 results<br/>4. Summarize content"]
```

### 2. Step Execution Phase

```mermaid
flowchart TB
    Step1["Step 1: Open Baidu search page"] --> Exec["Execution Agent"]
    Exec --> Tool["Tool: browser_navigate<br/>Args: { url: 'https://www.baidu.com' }"]
    Tool --> Result["Result: { success: true }"]
    Result --> Event["StepEvent: COMPLETED"]
```

### 3. Plan Update Phase

```mermaid
flowchart LR
    Result["Execution Result: Step 1 Complete"] --> Planner["Planner Agent"]
    Planner --> Updated["Updated Plan:<br/>1. [COMPLETED] Open Baidu<br/>2. [PENDING] Input search term<br/>3. [PENDING] Extract results<br/>4. [PENDING] Summarize content"]
```

## Event System

```mermaid
flowchart TB
    subgraph Events["Event System"]
        PlanEvent["PlanEvent<br/>Plan Create/Update"]
        StepEvent["StepEvent<br/>Step Status Change"]
        ToolEvent["ToolEvent<br/>Tool Invocation"]
        MessageEvent["MessageEvent<br/>Message Output"]
        ErrorEvent["ErrorEvent<br/>Error Occurred"]
    end

    subgraph SSE["SSE Stream"]
        Stream["Real-time Push"]
    end

    subgraph Frontend["Frontend"]
        UI["UI Update"]
    end

    Events --> Stream --> Frontend
```

| Event Type | Description | Data |
|------------|-------------|------|
| `PlanEvent` | Plan create/update | Plan object |
| `StepEvent` | Step status change | Step object |
| `ToolEvent` | Tool invocation | Tool name, args, result |
| `MessageEvent` | Message output | Text content |
| `ErrorEvent` | Error occurred | Error message |

## Key Files

| File Path | Function |
|-----------|----------|
| `domain/services/agents/planner.py` | Planner Agent implementation |
| `domain/services/agents/execution.py` | Execution Agent implementation |
| `domain/services/agents/base.py` | Agent base class |
| `domain/models/plan.py` | Plan/Step model definitions |
| `domain/services/prompts/planner.py` | Planner Prompt templates |
| `domain/services/prompts/execution.py` | Execution Prompt templates |
