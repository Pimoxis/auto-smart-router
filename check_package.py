"""Check this package's simple metadata, local links, and ZIP contents."""
from pathlib import Path
import re
import zipfile

root = Path(__file__).resolve().parent
skill = root / "codex-smart-router"
text = (skill / "SKILL.md").read_text(encoding="utf-8")
header, body = text.removeprefix("---\n").split("\n---\n", 1)
metadata = dict(line.split(": ", 1) for line in header.splitlines())
assert text.startswith("---\n")
assert set(metadata) == {"name", "description"}
assert metadata["name"] == skill.name
assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"])
assert len(metadata["name"]) <= 64
assert 0 < len(metadata["description"]) <= 1024
assert not any(char in metadata["description"] for char in "<>\n")
assert "TODO" not in text
for target in re.findall(r"\]\(([^)]+)\)", body):
    if "://" not in target:
        assert (skill / target).is_file(), target
ui = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
assert 'allow_implicit_invocation: true' in ui
assert '$codex-smart-router' in ui
description = re.search(r'short_description: "([^"]+)"', ui)[1]
assert 25 <= len(description) <= 64
files = {p.relative_to(root).as_posix(): p.read_bytes()
         for p in skill.rglob("*") if p.is_file()}
with zipfile.ZipFile(root / "codex-smart-router.zip") as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(files)
    for name, content in files.items():
        assert archive.read(name) == content, name
print(f"PASS: metadata, local links, and {len(files)} archived files match.")
