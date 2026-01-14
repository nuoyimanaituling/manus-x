# ManusX - Open Source General AI Agent

Project URL: <https://github.com/nuoyimanaituling/manus-x>

---

ManusX is a general-purpose AI Agent system that can be fully privately deployed and supports running various tools and operations in a sandbox environment.

The goal of ManusX project is to become a fully privately deployable enterprise-level Manus application. Vertical Manus applications have many repetitive engineering tasks, and this project hopes to unify this part, allowing everyone to build vertical Manus applications like building blocks.

Each service and tool in ManusX includes a Built-in version that can be fully privately deployed. Later, through A2A and MCP protocols, both Built-in Agents and Tools can be replaced. The underlying infrastructure can also be replaced by providing diverse provider configurations or simple development adaptations. ManusX supports distributed multi-instance deployment from the architectural design, facilitating horizontal scaling to meet enterprise-level deployment requirements.

---

## System Architecture Overview

```mermaid
flowchart TB
    subgraph User["User"]
        Browser["Browser"]
    end

    subgraph ManusX["ManusX System"]
        subgraph Frontend["Frontend"]
            WebUI["Web UI"]
            VNCViewer["VNC Viewer"]
        end

        subgraph Backend["Backend"]
            API["REST API"]
            Agent["Plan-Act Agent"]
            Tools["Tool Services"]
        end

        subgraph Sandbox["Sandbox"]
            Shell["Shell"]
            BrowserTool["Browser"]
            File["File"]
        end

        subgraph Storage["Storage"]
            MongoDB[("MongoDB")]
            Redis[("Redis")]
        end
    end

    Browser --> WebUI
    WebUI --> API
    API --> Agent
    Agent --> Tools
    Tools --> Sandbox
    API --> Storage
    VNCViewer --> Sandbox
```

## Demo

### Browser Automation

![Browser Automation](https://github.com/user-attachments/assets/d5574c2d-8228-41f5-a9ab-c4bb0f343e2b)

### Skill System

![Skill System](https://github.com/user-attachments/assets/25b897e5-27d1-40f8-97fa-17f56b4b5384)

## Core Features

```mermaid
flowchart LR
    subgraph Features["Core Features"]
        Deploy["Deployment<br/>Minimal Dependencies"]
        Tools["Tools<br/>Terminal/Browser/File"]
        Sandbox["Sandbox<br/>Docker Isolation"]
        Session["Sessions<br/>Task Management"]
        Dialog["Conversation<br/>Real-time Interaction"]
        i18n["Multi-language<br/>EN/ZH"]
        Auth["Authentication<br/>User Management"]
    end
```

| Feature | Description |
|---------|-------------|
| **Deployment** | Only requires one LLM service for deployment, no dependency on other external services |
| **Tools** | Supports Terminal, Browser, File, Web Search, message tools, with real-time viewing and takeover capabilities |
| **Sandbox** | Each Task is allocated a separate sandbox that runs in a local Docker environment |
| **Task Sessions** | Manages session history through Mongo/Redis, supports background tasks |
| **Conversations** | Supports stopping and interruption, supports file upload and download |
| **Multi-language** | Supports Chinese and English |
| **Authentication** | User login and authentication |

## Tech Stack

```mermaid
flowchart TB
    subgraph Tech["Tech Stack"]
        subgraph FE["Frontend"]
            Vue["Vue 3"]
            TS["TypeScript"]
            Tailwind["Tailwind CSS"]
        end

        subgraph BE["Backend"]
            FastAPI["FastAPI"]
            Python["Python"]
            DDD["DDD Architecture"]
        end

        subgraph Infra["Infrastructure"]
            Docker["Docker"]
            Mongo["MongoDB"]
            RedisDB["Redis"]
        end
    end
```

## Quick Start

```bash
# Clone the project
git clone https://github.com/nuoyimanaituling/manus-x.git
cd manus-x

# Configure environment variables
cp .env.example .env
# Edit .env file, configure API_KEY etc.

# Start services
./run.sh up -d

# Visit http://localhost:5173
```

For detailed deployment guide, see [Quick Start](quick_start.md).
