from pydantic import BaseModel
from typing import List


class Skill(BaseModel):
    """Skill model for domain expertise injection"""
    name: str                    # Unique skill identifier
    description: str             # Brief description (~100 tokens)
    body: str                    # Full skill content
    path: str                    # SKILL.md file path
    dir: str                     # Skill directory path
    resources: List[str] = []    # Available resource files
