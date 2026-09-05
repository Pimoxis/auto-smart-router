"""Read only this project's named test sessions; export token counts, not transcripts."""
import json
from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parent.parent
codex = Path.home() / ".codex"
names = {"/root/routing_trial", "/root/routing_trial/invoice_analysis",
         "/root/routing_trial/design_analysis", "/root/routing_retest", "/root/astra_trial"}
rows = []
with sqlite3.connect((codex / "state_5.sqlite").as_uri() + "?mode=ro", uri=True) as db:
    sessions = db.execute(
        "SELECT agent_path,model,reasoning_effort,rollout_path,cwd FROM threads "
        "WHERE agent_path IS NOT NULL").fetchall()
for name, model, effort, file, cwd in sessions:
    normalized_cwd = cwd.replace("\\\\", "\\").removeprefix("\\?\\")
    if name not in names or Path(normalized_cwd).resolve() != root:
        continue
    usage = None
    timestamps = []
    for line in Path(file).read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        payload = event.get("payload", {})
        if event.get("type") == "event_msg" and payload.get("type") == "token_count":
            info = payload.get("info")
            if info and info.get("total_token_usage"):
                usage = info["total_token_usage"]
                timestamps.append(event.get("timestamp"))
    if usage is None:
        continue
    assert 0 <= usage["cached_input_tokens"] <= usage["input_tokens"]
    assert usage["total_tokens"] == usage["input_tokens"] + usage["output_tokens"]
    assert 0 <= usage["reasoning_output_tokens"] <= usage["output_tokens"]
    rows.append({"agent": name, "model": model, "effort": effort,
                 "last_usage_timestamp": timestamps[-1],
                 "uncached_input_tokens": usage["input_tokens"] - usage["cached_input_tokens"],
                 **usage})
assert {row["agent"] for row in rows} == names, "Missing test-session usage"
(root / "routing-tests/usage-results.json").write_text(
    json.dumps(rows, indent=2) + "\n", encoding="utf-8")
print(json.dumps(rows, indent=2))
