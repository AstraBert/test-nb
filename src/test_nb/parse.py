import re

from .models import CodeCell


def extract_bash(cell: CodeCell) -> str | None:
    lines = cell["source"]
    if (
        lines[0].strip().startswith("%%bash")
        or lines[0].strip().startswith("%%sh")
        or lines[0].strip().startswith("%%script bash")
    ):
        sanitized_lines = []
        for line in lines:
            if (
                sanitized_line := line.replace("%%bash", "")
                .replace("%%sh", "")
                .replace("%%script bash", "")
                .strip()
            ):
                sanitized_lines.append(sanitized_line)
        return " && ".join(sanitized_lines)
    script = ""
    for line in lines:
        l = line.strip()
        if l.startswith("!") or l.startswith("%"):
            script += l.replace("!", "").replace("%", "").strip() + " && "
    if script:
        return script.strip(" && ")
    return None


def extract_code(cell: CodeCell, exclude_env: bool = False) -> str | None:
    lines = cell["source"]
    if (
        lines[0].strip().startswith("%%bash")
        or lines[0].strip().startswith("%%sh")
        or lines[0].strip().startswith("%%script bash")
    ):
        return None
    code = ""
    for line in lines:
        if line.strip():
            if not line.startswith("!") and not line.startswith("%"):
                if exclude_env and re.search(
                    r"os\.environ\[['\"][^'\"]+['\"]\]\s*=", line
                ):
                    continue
                code += "\t" + line
    if code:
        return code
    return None
