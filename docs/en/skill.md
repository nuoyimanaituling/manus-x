# Skill System Implementation

## Overview

The Skill system provides **domain expertise injection** capabilities for ManusX. Through Skills, Agents can gain professional operation guides and best practices in specific domains (such as PDF processing, data analysis, etc.).

## Design Philosophy

### Three-Layer Loading Architecture

```mermaid
flowchart TB
    subgraph Layer1["Layer 1: Metadata Layer"]
        Meta["Names and short descriptions of all Skills<br/>~100 tokens"]
    end

    subgraph Layer2["Layer 2: Full Content Layer"]
        Content["Complete operation guides, code examples<br/>~500-2000 tokens"]
    end

    subgraph Layer3["Layer 3: Resource File Layer"]
        Resources["Scripts, templates, reference docs<br/>On-demand loading"]
    end

    Meta -->|"LLM determines need"| Content
    Content -->|"Explicit request"| Resources

    style Layer1 fill:#e1f5fe
    style Layer2 fill:#fff3e0
    style Layer3 fill:#f3e5f5
```

```mermaid
flowchart LR
    subgraph Always["Always Loaded"]
        L1["Layer 1<br/>Metadata"]
    end

    subgraph OnDemand["On-Demand Loading"]
        L2["Layer 2<br/>Full Content"]
        L3["Layer 3<br/>Resource Files"]
    end

    L1 --> L2 --> L3
```

### Layer Details

| Layer | Load Timing | Content | Token Cost |
|-------|-------------|---------|------------|
| **Layer 1** | Always loaded | Skill names and short descriptions | ~100 |
| **Layer 2** | On-demand | Complete operation guides, code examples | ~500-2000 |
| **Layer 3** | Explicit request | Scripts, templates, reference docs | As needed |

## Directory Structure

```mermaid
flowchart TB
    subgraph SkillsDir["backend/skills/"]
        subgraph PDF["pdf/"]
            SKILL1["SKILL.md"]
            subgraph Scripts1["scripts/"]
                S1["extract_tables.py"]
            end
            subgraph Refs1["references/"]
                R1["pdf_spec.md"]
            end
            subgraph Assets1["assets/"]
                A1["template.html"]
            end
        end

        subgraph DataAnalysis["data-analysis/"]
            SKILL2["SKILL.md"]
            subgraph Scripts2["scripts/"]
                S2["analyze.py"]
            end
        end
    end
```

```
backend/skills/
├── pdf/
│   ├── SKILL.md              # Skill definition file
│   ├── scripts/              # Executable scripts
│   │   └── extract_tables.py
│   ├── references/           # Reference documents
│   │   └── pdf_spec.md
│   └── assets/               # Static assets
│       └── template.html
└── data-analysis/
    ├── SKILL.md
    └── scripts/
        └── analyze.py
```

## SKILL.md File Format

Each Skill is defined through a `SKILL.md` file using **YAML frontmatter + Markdown body** format:

```mermaid
flowchart TB
    subgraph SkillMD["SKILL.md File Structure"]
        subgraph YAML["YAML Frontmatter"]
            Name["name: pdf"]
            Desc["description: Process PDF files..."]
        end
        subgraph Body["Markdown Body"]
            Title["# PDF Processing Skill"]
            Section1["## Reading PDFs"]
            Code["```python...```"]
            Section2["## Key Libraries"]
        end
    end

    YAML --> Body
```

### Field Description

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique Skill identifier |
| `description` | Yes | Short description (~100 tokens) |
| `body` | Yes | Markdown body content |

## Core Implementation

### Skill Model

```mermaid
classDiagram
    class Skill {
        +str name
        +str description
        +str body
        +str path
        +str dir
        +List~str~ resources
    }
```

```python
# backend/app/domain/models/skill.py

class Skill(BaseModel):
    name: str              # Unique identifier
    description: str       # Short description
    body: str              # Full content
    path: str              # SKILL.md file path
    dir: str               # Skill directory path
    resources: List[str]   # Available resource files list
```

### SkillLoader Class

```mermaid
flowchart TB
    subgraph SkillLoader["SkillLoader"]
        Init["__init__<br/>Initialize"]
        Load["_load_skills<br/>Scan and Load"]
        Parse["_parse_skill_md<br/>Parse File"]
        GetDesc["get_descriptions<br/>Get Metadata"]
        GetContent["get_skill_content<br/>Get Full Content"]
    end

    Init --> Load --> Parse
    GetDesc --> |"Layer 1"| Return1["Return Description List"]
    GetContent --> |"Layer 2"| Return2["Return Full Content"]
```

## Usage Flow

### Complete Flow Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant L as SkillLoader
    participant F as File System

    Note over A: System Prompt contains Skill descriptions (Layer 1)

    U->>A: "Help me extract tables from this PDF"
    A->>A: Determine pdf skill needed
    A->>L: skill_request("pdf")
    L-->>A: Return full content (Layer 2)

    A->>F: file_read("scripts/extract_tables.py")
    F-->>A: Return script content (Layer 3)

    A->>A: Execute task
    A-->>U: Return extracted tables
```

## Execution Flow Diagram

```mermaid
flowchart TB
    User["User: Help me extract tables from this PDF"] --> SystemPrompt

    subgraph SystemPrompt["System Prompt"]
        Skills["Available Skills:<br/>- pdf: Process PDF files..."]
    end

    SystemPrompt --> LLMJudge["LLM determines: pdf skill needed"]

    LLMJudge --> SkillRequest["Call: skill_request('pdf')"]

    SkillRequest --> SkillContent["Return PDF Skill full content"]

    subgraph SkillContent
        Guide["# PDF Processing Skill<br/>## Reading PDFs<br/>..."]
        Resources["## Available Resources<br/>- scripts/extract_tables.py"]
    end

    SkillContent --> Execute["LLM executes according to guide"]

    subgraph Execute
        Exec1["shell_exec('pip install pdfplumber')"]
        Exec2["file_write('extract.py', ...)"]
        Exec3["shell_exec('python extract.py')"]
    end

    Execute --> Result["Return extracted table data"]
```

## Creating New Skills

```mermaid
flowchart LR
    Step1["1. Create Directory"] --> Step2["2. Write SKILL.md"]
    Step2 --> Step3["3. Add Resource Files"]
    Step3 --> Step4["4. Restart Service"]
```

### 1. Create Directory Structure

```bash
mkdir -p backend/skills/my-skill/{scripts,references,assets}
```

### 2. Write SKILL.md

```markdown
---
name: my-skill
description: Brief description of what this skill does (~100 tokens)
---

# My Skill Title

Detailed instructions for the LLM.

## Section 1

Instructions and code examples...

## Section 2

More instructions...
```

### 3. Add Resource Files (Optional)

```bash
# Scripts
echo "print('Hello')" > backend/skills/my-skill/scripts/helper.py

# Templates
echo "<html>...</html>" > backend/skills/my-skill/assets/template.html
```

### 4. Restart Service

Skills are automatically loaded when the service starts.

## Best Practices

```mermaid
flowchart TB
    subgraph BestPractices["Best Practices"]
        P1["Concise Description<br/>~100 tokens"]
        P2["Complete Examples<br/>Directly executable"]
        P3["Clear Organization<br/>Use Markdown headings"]
        P4["Independent Resources<br/>Minimize dependencies"]
        P5["Error Handling<br/>Include solutions"]
    end
```

1. **Concise Description**: Keep `description` field under 100 tokens
2. **Complete Examples**: Provide code examples that can be directly copied and executed
3. **Clear Organization**: Use Markdown headings to organize content
4. **Independent Resources**: Scripts should run independently with minimal dependencies
5. **Error Handling**: Include solutions for common errors

## Key Files

| File Path | Function |
|-----------|----------|
| `domain/models/skill.py` | Skill model definition |
| `domain/services/skill_loader.py` | Skill loader |
| `skills/*/SKILL.md` | Individual Skill definition files |
