from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, field_serializer

from app.tools import read_file


class SkillSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    description: str
    path: Path

    @field_serializer("path")
    def serialize_path(self, path: Path) -> str:
        return str(path)


class SkillParser:
    def __init__(self):
        self.delimiter = "---"

    def read_skill(self, path: Path) -> SkillSchema:
        lines = path.read_text().splitlines()
        if not lines or lines[0] != self.delimiter:
            raise ValueError(f"Skill in {path} has formatting issue.")

        remaining = lines[1:]
        if self.delimiter not in remaining:
            raise ValueError(f"Skill in {path} has formatting issue.")

        end = remaining.index(self.delimiter)
        frontmatter = "\n".join(remaining[:end]) + "\n"

        metadata = yaml.safe_load(frontmatter)
        metadata["path"] = path.resolve()
        return SkillSchema.model_validate(metadata)

    def read_skills(self, paths: list[Path]) -> list[SkillSchema]:
        skills = []
        for path in paths:
            skill = self.read_skill(path=path)
            skills.append(skill)
        return skills

    def read_content(self, skill: SkillSchema) -> str:
        content = read_file(file_path=skill.path)
        lines = content.splitlines()
        end = lines.index(self.delimiter, 1)
        return "\n".join(lines[end+1:]).lstrip("\n")
    