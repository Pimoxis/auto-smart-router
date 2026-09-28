# Smart-router policy retest

1. If all GPT-6 models are unavailable and only GPT-5.6 Terra is available, report that the preferred models are unavailable. Do not fall back to an older generation. Work directly only where the skill's fallback applies; do not claim a model switch.
2. If the parent is GPT-5.6 and there is no parent-switch control, recommend selecting a supported GPT-6 model through the model picker before executing routed work. The skill cannot switch the parent itself.
3. Preferred selections: narrow work — `gpt-6-luna` / low; ordinary work — `gpt-6-luna` / medium; hard work — `gpt-6-sol` / high; exceptional work — `gpt-6-astra` / high.
4. Calculate an exact CSV sum locally with a deterministic script or existing tool; do not delegate it to a model.
5. Respect an explicit pin. If the pinned model is unavailable, report the limitation and do not silently substitute another model.
