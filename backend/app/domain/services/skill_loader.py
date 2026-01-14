import re
import logging
from pathlib import Path
from typing import Dict, Optional, List

import yaml

from app.domain.models.skill import Skill

logger = logging.getLogger(__name__)


class SkillLoader:
    """Load and manage skills from SKILL.md files"""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skills: Dict[str, Skill] = {}
        self._load_skills()

    def _parse_skill_md(self, path: Path) -> Optional[Skill]:
        """Parse SKILL.md file (YAML frontmatter + Markdown body)

        Args:
            path: Path to SKILL.md file

        Returns:
            Skill object if parsing succeeds, None otherwise
        """
        try:
            content = path.read_text(encoding='utf-8')
            # Match YAML frontmatter between --- markers
            pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
            match = re.match(pattern, content, re.DOTALL)
            if not match:
                logger.warning(f"Invalid SKILL.md format: {path}")
                return None

            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2).strip()
            skill_dir = path.parent

            # Validate required fields
            if 'name' not in frontmatter or 'description' not in frontmatter:
                logger.warning(f"Missing required fields in SKILL.md: {path}")
                return None

            # List resource files in subdirectories
            resources = []
            for subdir in ['scripts', 'references', 'assets']:
                subdir_path = skill_dir / subdir
                if subdir_path.exists():
                    for f in subdir_path.rglob('*'):
                        if f.is_file():
                            resources.append(str(f.relative_to(skill_dir)))

            return Skill(
                name=frontmatter['name'],
                description=frontmatter['description'],
                body=body,
                path=str(path),
                dir=str(skill_dir),
                resources=resources
            )
        except Exception as e:
            logger.error(f"Error parsing SKILL.md at {path}: {e}")
            return None

    def _load_skills(self):
        """Scan and load all skills from skills directory"""
        if not self.skills_dir.exists():
            logger.info(f"Skills directory does not exist: {self.skills_dir}")
            return

        for skill_md in self.skills_dir.rglob('SKILL.md'):
            skill = self._parse_skill_md(skill_md)
            if skill:
                self.skills[skill.name] = skill
                logger.info(f"Loaded skill: {skill.name}")

        logger.info(f"Loaded {len(self.skills)} skills from {self.skills_dir}")

    def get_descriptions(self) -> str:
        """Get metadata descriptions of all skills (Layer 1)

        Returns:
            Formatted string of skill names and descriptions
        """
        if not self.skills:
            return ""
        return "\n".join(
            f"- {s.name}: {s.description}"
            for s in self.skills.values()
        )

    def get_skill_content(self, name: str) -> Optional[str]:
        """Get full skill content (Layer 2)

        Args:
            name: Skill name

        Returns:
            Full skill content with resource hints, or None if not found
        """
        skill = self.skills.get(name)
        if not skill:
            return None

        content = skill.body
        if skill.resources:
            content += f"\n\n## Available Resources\n"
            content += f"Directory: {skill.dir}\n"
            for r in skill.resources:
                content += f"- {r}\n"
        return content

    def list_skills(self) -> List[str]:
        """Get list of all skill names

        Returns:
            List of skill names
        """
        return list(self.skills.keys())

    def has_skills(self) -> bool:
        """Check if any skills are loaded

        Returns:
            True if skills are available
        """
        return len(self.skills) > 0
