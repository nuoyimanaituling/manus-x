# ManusX 与 OpenManus Sandbox 实现对比分析

## 1. 概述

### 1.1 什么是 Sandbox？

在 AI Agent 系统中，Sandbox（沙箱）是一个**隔离的执行环境**，用于安全地运行 Agent 生成的代码和命令。它提供了：
- Shell 命令执行能力
- 文件系统操作
- 浏览器自动化（可选）
- 与宿主机隔离的安全边界

### 1.2 两个项目的定位

| 项目 | 定位 | Sandbox 设计理念 |
|------|------|------------------|
| **ManusX** | 企业级 AI Agent 平台 | **服务化架构**：Sandbox 作为独立服务，通过 HTTP API 通信 |
| **OpenManus** | 开源 AI Agent 框架 | **灵活架构**：支持本地 Docker SDK 和云端 Daytona 双模式 |

---

## 2. ManusX Sandbox 实现

### 2.1 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                        ManusX 架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         HTTP API          ┌────────────────┐  │
│  │   Backend    │ ◄──────────────────────►  │    Sandbox     │  │
│  │   Container  │    POST /api/v1/shell     │   Container    │  │
│  │              │    POST /api/v1/file      │                │  │
│  │  ┌────────┐  │                           │  ┌──────────┐  │  │
│  │  │Docker  │  │    容器动态创建/销毁        │  │ FastAPI  │  │  │
│  │  │Sandbox │──┼───────────────────────────┼─►│  Server  │  │  │
│  │  │ Class  │  │                           │  └──────────┘  │  │
│  │  └────────┘  │                           │       │        │  │
│  └──────────────┘                           │       ▼        │  │
│                                             │  ┌──────────┐  │  │
│                                             │  │Supervisor│  │  │
│                                             │  │ (进程管理)│  │  │
│                                             │  └──────────┘  │  │
│                                             │       │        │  │
│                                             │       ▼        │  │
│                                             │  ┌──────────┐  │  │
│                                             │  │ Services │  │  │
│                                             │  │ - Shell  │  │  │
│                                             │  │ - File   │  │  │
│                                             │  │ - Chrome │  │  │
│                                             │  └──────────┘  │  │
│                                             └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件

#### 2.2.1 Sandbox 容器（独立 Docker 服务）

**基础环境**：
- 操作系统：Ubuntu 22.04
- Python：3.10
- Node.js：20.18.0
- 浏览器：Chromium

**进程管理**（Supervisor）：
```
[program:xvfb]       # 虚拟显示器 :1
[program:chrome]     # Chromium 浏览器
[program:socat]      # 端口转发 9222
[program:x11vnc]     # VNC 远程桌面
[program:websockify] # WebSocket 代理
[program:app]        # FastAPI 服务
```

#### 2.2.2 Backend 交互层

```python
# backend/app/infrastructure/external/sandbox/docker_sandbox.py

class DockerSandbox(Sandbox):
    """通过 HTTP API 与 Sandbox 容器通信"""

    def __init__(self, ip: str, container_name: str):
        self.client = httpx.AsyncClient(timeout=600)
        self.base_url = f"http://{ip}:8080"

    async def exec_command(self, session_id, exec_dir, command):
        """执行 Shell 命令"""
        response = await self.client.post(
            f"{self.base_url}/api/v1/shell/exec",
            json={"id": session_id, "exec_dir": exec_dir, "command": command}
        )
        return ToolResult(**response.json())

    async def file_write(self, file, content, ...):
        """写入文件"""
        response = await self.client.post(
            f"{self.base_url}/api/v1/file/write",
            json={"file": file, "content": content, ...}
        )
        return ToolResult(**response.json())
```

### 2.3 核心文件清单

| 文件路径 | 功能 |
|---------|------|
| `sandbox/app/main.py` | FastAPI 应用入口 |
| `sandbox/app/services/shell.py` | Shell 会话管理（内存存储活跃会话） |
| `sandbox/app/services/file.py` | 文件读写、搜索、替换 |
| `sandbox/app/services/supervisor.py` | 进程生命周期 + 超时管理 |
| `sandbox/Dockerfile` | 容器镜像定义 |
| `sandbox/supervisord.conf` | 进程启动配置 |
| `backend/.../docker_sandbox.py` | Docker 容器管理 + HTTP 客户端 |
| `backend/app/domain/external/sandbox.py` | Sandbox 抽象接口（Protocol） |

### 2.4 Shell 命令执行流程

```python
# sandbox/app/services/shell.py

class ShellService:
    active_shells: Dict[str, Dict] = {}  # 内存中的活跃会话

    async def exec_command(self, session_id, exec_dir, command):
        # 1. 检查会话是否存在
        if session_id in self.active_shells:
            shell = self.active_shells[session_id]
        else:
            # 2. 创建新的异步子进程
            process = await asyncio.create_subprocess_shell(
                f"cd {exec_dir} && {command}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            shell = {"process": process, "output": "", ...}
            self.active_shells[session_id] = shell

        # 3. 启动后台输出读取器
        asyncio.create_task(self._read_output(session_id))

        # 4. 等待命令完成或超时
        await asyncio.wait_for(process.wait(), timeout=5)

        return ShellExecResult(
            session_id=session_id,
            status="completed" if process.returncode else "running",
            output=shell["output"]
        )
```

### 2.5 容器生命周期

```python
# backend/.../docker_sandbox.py

class DockerSandbox:
    @staticmethod
    async def create():
        """创建新容器"""
        docker_client = docker.from_env()
        container_name = f"sandbox-{uuid.uuid4()[:8]}"

        container = docker_client.containers.run(
            image=settings.sandbox_image,
            name=container_name,
            detach=True,
            remove=True,  # 停止时自动删除
            environment={
                "SERVICE_TIMEOUT_MINUTES": settings.sandbox_ttl_minutes
            },
            network=settings.sandbox_network
        )

        ip = DockerSandbox._get_container_ip(container)
        return DockerSandbox(ip=ip, container_name=container_name)

    async def destroy(self):
        """销毁容器"""
        docker_client = docker.from_env()
        container = docker_client.containers.get(self.container_name)
        container.remove(force=True)
```

### 2.6 超时保护机制

```python
# sandbox/app/services/supervisor.py

class SupervisorService:
    def __init__(self):
        if settings.SERVICE_TIMEOUT_MINUTES:
            # 设置自动关闭定时器
            self.shutdown_time = datetime.now() + timedelta(
                minutes=settings.SERVICE_TIMEOUT_MINUTES
            )
            self._setup_timer(settings.SERVICE_TIMEOUT_MINUTES)

    async def extend_timeout(self):
        """延长超时时间（每次 API 调用自动触发）"""
        self.shutdown_time = datetime.now() + timedelta(
            minutes=settings.SERVICE_TIMEOUT_MINUTES
        )

# sandbox/app/core/middleware.py
async def auto_extend_timeout_middleware(request, call_next):
    """中间件：自动延长超时"""
    if supervisor_service.auto_expand_enabled:
        await supervisor_service.extend_timeout()
    return await call_next(request)
```

---

## 3. OpenManus Sandbox 实现

### 3.1 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenManus 架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      应用层                                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ ShellTool    │  │ FilesTool    │  │ BrowserTool  │    │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │   │
│  └─────────┼─────────────────┼─────────────────┼────────────┘   │
│            │                 │                 │                 │
│            ▼                 ▼                 ▼                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Sandbox 抽象层                          │   │
│  │  ┌─────────────────────┐  ┌─────────────────────┐        │   │
│  │  │  LocalSandboxClient │  │  DaytonaSandbox     │        │   │
│  │  │  (Docker SDK)       │  │  (Cloud API)        │        │   │
│  │  └──────────┬──────────┘  └──────────┬──────────┘        │   │
│  └─────────────┼─────────────────────────┼──────────────────┘   │
│                │                         │                       │
│       ┌────────▼────────┐       ┌────────▼────────┐             │
│       │  Docker Engine  │       │  Daytona Cloud  │             │
│       │  (本地容器)      │       │  (远程服务)      │             │
│       └─────────────────┘       └─────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 双模式支持

#### 模式一：本地 Docker Sandbox

```python
# app/sandbox/core/sandbox.py

class DockerSandbox:
    """基于 Docker SDK 的本地沙箱"""

    async def create(self):
        """创建容器"""
        self.container = self.docker_client.containers.run(
            image=self.config.image,
            name=f"sandbox_{uuid.uuid4()}",
            detach=True,
            tty=True,
            environment={"PYTHONUNBUFFERED": "1"},
            mem_limit=self.config.memory_limit,
            cpu_period=100000,
            cpu_quota=int(self.config.cpu_limit * 100000),
            network_mode="none" if not self.config.network_enabled else "bridge"
        )

        # 初始化交互式终端
        self.terminal = AsyncDockerizedTerminal(self.container)
        await self.terminal.create()

    async def run_command(self, command: str, timeout: int = 300):
        """执行命令"""
        return await self.terminal.execute(command, timeout)
```

#### 模式二：Daytona 云 Sandbox

```python
# app/daytona/sandbox.py

async def get_or_start_sandbox(sandbox_id: str):
    """获取或启动 Daytona 沙箱"""
    daytona = Daytona(
        config=DaytonaConfig(
            api_key=settings.daytona_api_key,
            server_url=settings.daytona_server_url,
            target=settings.daytona_target
        )
    )

    sandbox = daytona.get(sandbox_id)
    if sandbox.state != "running":
        daytona.start(sandbox)

    # 启动 supervisor 会话
    await start_supervisord_session(sandbox)
    return sandbox
```

### 3.3 核心文件清单

| 文件路径 | 功能 |
|---------|------|
| `app/sandbox/core/sandbox.py` | DockerSandbox 主类 |
| `app/sandbox/core/terminal.py` | AsyncDockerizedTerminal（Socket 通信） |
| `app/sandbox/core/manager.py` | SandboxManager（多沙箱池化管理） |
| `app/sandbox/client.py` | BaseSandboxClient / LocalSandboxClient |
| `app/daytona/sandbox.py` | Daytona 云集成 |
| `app/daytona/tool_base.py` | SandboxToolsBase 基类 |
| `app/tool/sandbox/sb_shell_tool.py` | Shell 工具（tmux 会话） |
| `app/tool/sandbox/sb_files_tool.py` | 文件操作工具 |
| `app/tool/sandbox/sb_browser_tool.py` | 浏览器自动化工具 |

### 3.4 异步终端实现

```python
# app/sandbox/core/terminal.py

class AsyncDockerizedTerminal:
    """通过 Docker exec + Socket 实现异步终端"""

    async def create(self):
        """创建交互式终端"""
        exec_instance = self.container.client.api.exec_create(
            self.container.id,
            cmd="/bin/bash",
            stdin=True, tty=True, stdout=True, stderr=True,
            environment={"TERM": "dumb", "PS1": "$ "}
        )

        # 获取 socket 连接
        self.socket = self.container.client.api.exec_start(
            exec_instance["Id"],
            socket=True
        )
        self.socket._sock.setblocking(False)

    async def execute(self, command: str, timeout: int):
        """执行命令"""
        # 1. 安全检查
        self._check_dangerous_commands(command)

        # 2. 发送命令
        self.socket._sock.sendall(f"{command}\n".encode())

        # 3. 读取输出直到提示符
        output = ""
        while "$ " not in output:
            chunk = await asyncio.wait_for(
                self._read_chunk(), timeout=timeout
            )
            output += chunk

        return self._clean_output(output)
```

### 3.5 多沙箱管理器

```python
# app/sandbox/core/manager.py

class SandboxManager:
    """管理多个沙箱实例"""

    def __init__(self):
        self.sandboxes: Dict[str, SandboxInfo] = {}
        self.max_sandboxes = 100
        self.idle_timeout = 3600  # 1小时空闲超时
        self.cleanup_interval = 300  # 5分钟清理一次

        # 启动清理任务
        asyncio.create_task(self._cleanup_loop())

    async def create_sandbox(self, config: SandboxSettings) -> str:
        """创建新沙箱"""
        if len(self.sandboxes) >= self.max_sandboxes:
            raise SandboxResourceError("Max sandboxes reached")

        sandbox = DockerSandbox(config)
        await sandbox.create()

        sandbox_id = str(uuid.uuid4())
        self.sandboxes[sandbox_id] = SandboxInfo(
            sandbox=sandbox,
            last_used=datetime.now()
        )
        return sandbox_id

    async def _cleanup_idle_sandboxes(self):
        """清理空闲沙箱"""
        now = datetime.now()
        for sandbox_id, info in list(self.sandboxes.items()):
            if (now - info.last_used).seconds > self.idle_timeout:
                await info.sandbox.cleanup()
                del self.sandboxes[sandbox_id]
```

### 3.6 文件操作（tar 流传输）

```python
# app/sandbox/core/sandbox.py

class DockerSandbox:
    async def read_file(self, path: str) -> str:
        """通过 tar 流读取文件"""
        stream, stat = self.container.get_archive(path)

        # 解包 tar
        tar_bytes = b"".join(chunk for chunk in stream)
        with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tar:
            member = tar.getmembers()[0]
            f = tar.extractfile(member)
            return f.read().decode()

    async def write_file(self, path: str, content: str):
        """通过 tar 流写入文件"""
        # 创建 tar 归档
        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            data = content.encode()
            tarinfo = tarfile.TarInfo(name=os.path.basename(path))
            tarinfo.size = len(data)
            tar.addfile(tarinfo, io.BytesIO(data))

        tar_stream.seek(0)
        self.container.put_archive(os.path.dirname(path), tar_stream)
```

---

## 4. 核心差异对比

### 4.1 通信方式

| 维度 | ManusX | OpenManus |
|------|----------|-----------|
| **协议** | HTTP/REST API | Docker SDK (Unix Socket) |
| **数据格式** | JSON | Binary (tar, socket stream) |
| **连接方式** | 无状态请求 | 持久化 Socket 连接 |
| **延迟** | 较高（HTTP 开销） | 较低（直接调用） |

### 4.2 进程管理

| 维度 | ManusX | OpenManus |
|------|----------|-----------|
| **工具** | Supervisor | tmux |
| **会话持久化** | 内存字典 | tmux 会话 |
| **多进程** | 多 program 配置 | tmux 多窗口 |
| **进程监控** | Supervisor API | 手动管理 |

### 4.3 文件传输

| 维度 | ManusX | OpenManus |
|------|----------|-----------|
| **上传** | HTTP multipart/form-data | tar 归档流 |
| **下载** | HTTP 响应流 | tar 归档流 |
| **大文件** | 分片支持 | 需自行处理 |

### 4.4 浏览器集成

| 维度 | ManusX | OpenManus |
|------|----------|-----------|
| **实现** | 容器内置 Chromium | 依赖 Daytona 或外部 |
| **协议** | CDP (Chrome DevTools Protocol) | CDP |
| **远程访问** | VNC over WebSocket | Daytona Preview Link |

### 4.5 多租户/扩展性

| 维度 | ManusX | OpenManus |
|------|----------|-----------|
| **隔离** | 每会话独立容器 | SandboxManager 池化 |
| **并发** | Docker 网络隔离 | asyncio.Lock |
| **云支持** | 无 | Daytona 平台 |

---

## 5. 优缺点分析

### 5.1 ManusX

#### 优势

| 优势 | 说明 |
|------|------|
| **服务解耦** | Sandbox 作为独立服务，可单独扩展、部署、监控 |
| **标准接口** | HTTP API 易于调试、测试、对接其他系统 |
| **完整环境** | 内置浏览器、VNC，开箱即用 |
| **自动保护** | Supervisor 进程监控 + 超时自动清理 |
| **易于替换** | Protocol 抽象，可切换不同实现 |

#### 劣势

| 劣势 | 说明 |
|------|------|
| **HTTP 开销** | 每次调用都有网络往返延迟 |
| **启动延迟** | 容器创建 + 服务就绪需要时间（~10-30s） |
| **资源占用** | 每个容器都运行完整服务栈 |
| **无云原生** | 缺少 Kubernetes/云平台集成 |

### 5.2 OpenManus

#### 优势

| 优势 | 说明 |
|------|------|
| **性能优越** | Docker SDK 直连，无 HTTP 开销 |
| **实时通信** | Socket 连接，支持流式输出 |
| **云支持** | Daytona 平台，无需自建基础设施 |
| **池化管理** | SandboxManager 复用沙箱，减少创建开销 |
| **灵活部署** | 本地/云端双模式切换 |

#### 劣势

| 劣势 | 说明 |
|------|------|
| **Docker 依赖** | 必须有 Docker 守护进程 |
| **架构复杂** | 双模式增加维护成本 |
| **浏览器外置** | 需额外配置浏览器环境 |
| **调试困难** | Socket 通信不如 HTTP 直观 |

---

## 6. 适用场景建议

### 6.1 选择 ManusX 架构

- **企业私有部署**：需要完整控制、审计日志
- **多租户 SaaS**：每个用户独立容器隔离
- **需要浏览器**：网页自动化、截图、爬虫
- **团队协作**：标准 API，易于前后端分工

### 6.2 选择 OpenManus 架构

- **高性能场景**：大量命令执行、低延迟要求
- **云原生部署**：已有 Daytona 或类似平台
- **资源受限**：需要沙箱复用，减少容器数量
- **开发测试**：本地快速迭代，灵活切换

### 6.3 混合方案

可以结合两者优势：
1. 使用 OpenManus 的 Docker SDK 方式提升性能
2. 借鉴 ManusX 的 Supervisor 进行进程管理
3. 通过 Protocol 抽象支持多种后端

---

## 7. 总结

### 7.1 核心差异总结

```
┌─────────────────────────────────────────────────────────────────┐
│                        设计理念对比                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ManusX                          OpenManus                   │
│   ─────────                         ─────────                   │
│   服务化架构                         SDK 直连架构                 │
│   HTTP API 通信                      Socket 通信                 │
│   Supervisor 进程管理                 tmux 会话管理              │
│   容器内置浏览器                      外部/云端浏览器             │
│   每会话独立容器                      沙箱池化复用                │
│                                                                  │
│   适合：企业部署、多租户              适合：高性能、云原生        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 选型建议

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 企业级 AI Agent 平台 | ManusX | 服务解耦、审计友好、易于监控 |
| 高性能执行引擎 | OpenManus | SDK 直连、低延迟、资源复用 |
| 云端 SaaS 产品 | OpenManus + Daytona | 免运维、弹性伸缩 |
| 本地开发工具 | OpenManus 本地模式 | 快速启动、无外部依赖 |

### 7.3 演进方向

两个项目都在持续演进，可以相互借鉴：
- ManusX 可引入 Docker SDK 直连模式提升性能
- OpenManus 可借鉴 Supervisor 增强进程管理
- 两者都可增加 Kubernetes 原生支持

---

## 附录：关键文件路径

### ManusX

```
ManusX/
├── sandbox/
│   ├── app/
│   │   ├── main.py                    # FastAPI 入口
│   │   ├── services/
│   │   │   ├── shell.py               # Shell 服务
│   │   │   ├── file.py                # 文件服务
│   │   │   └── supervisor.py          # 进程管理
│   │   └── api/v1/
│   │       ├── shell.py               # Shell API
│   │       └── file.py                # File API
│   ├── Dockerfile
│   └── supervisord.conf
└── backend/
    └── app/
        ├── domain/external/sandbox.py           # Protocol 定义
        └── infrastructure/external/sandbox/
            └── docker_sandbox.py                # 实现
```

### OpenManus

```
OpenManus/
├── app/
│   ├── sandbox/
│   │   ├── core/
│   │   │   ├── sandbox.py             # DockerSandbox
│   │   │   ├── terminal.py            # AsyncDockerizedTerminal
│   │   │   └── manager.py             # SandboxManager
│   │   └── client.py                  # 客户端接口
│   ├── daytona/
│   │   ├── sandbox.py                 # Daytona 集成
│   │   └── tool_base.py               # 工具基类
│   └── tool/sandbox/
│       ├── sb_shell_tool.py           # Shell 工具
│       ├── sb_files_tool.py           # 文件工具
│       └── sb_browser_tool.py         # 浏览器工具
└── Dockerfile
```
