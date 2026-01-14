from app.domain.services.tools.base import BaseTool, tool
from app.domain.models.tool_result import ToolResult
from app.domain.services.skill_loader import SkillLoader


class SkillTool(BaseTool):
    """Tool for loading specialized skills on demand"""

    name: str = "skill"

    def __init__(self, skill_loader: SkillLoader):
        super().__init__()
        self.skill_loader = skill_loader

    @tool(
        name="load_skill",
        description="Load a skill to gain specialized knowledge for a specific domain task. "
                    "Use this when the user's task matches one of the available skill descriptions. "
                    "The skill content will be injected into the conversation to guide task completion.",
        parameters={
            "skill": {
                "type": "string",
                "description": "The name of the skill to load (e.g., 'pdf', 'data-analysis')"
            }
        },
        required=["skill"]
    )
    async def load_skill(self, skill: str) -> ToolResult:
        """Load a skill by name

        Args:
            skill: Name of the skill to load

        Returns:
            ToolResult with skill content or error message
        """
        content = self.skill_loader.get_skill_content(skill)
        if content is None:
            available = ", ".join(self.skill_loader.list_skills()) or "none"
            return ToolResult(
                success=False,
                error=f"Unknown skill: '{skill}'. Available skills: {available}"
            )

        wrapped_content = f"""<skill-loaded name="{skill}">
{content}
</skill-loaded>

Follow the instructions in the skill above to complete the user's task."""

        return ToolResult(success=True, data=wrapped_content)
