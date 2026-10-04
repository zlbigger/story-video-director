# Image backends and art direction

## Choosing the generation route

Use built-in image generation when available. If it is unavailable, finish independent planning, state the specific missing capability and describe a compatible API alternative. Follow the installed imagegen skill's fallback rules. The user's request to use a named API, model or local gateway is evidence of provider choice; do not ask them to choose that same route again.

A local management page is not automatically the inference endpoint. Inspect the existing service documentation/model list, verify the requested model is present, and discover authentication through the user-authorized configuration or environment. Do not invent endpoints from a model name. Use an existing authenticated service without changing account, network or security settings.

For an OpenAI-compatible image interface, configure the existing imagegen CLI through `OPENAI_BASE_URL` and `OPENAI_API_KEY` in its process environment. Preserve `gpt-image-2` when requested; never downgrade silently. Never put credentials in command flags, scripts, prompt files, manifests, logs or Git. If reading an existing local configuration within the authorized task, extract the credential in memory, pass it only to the authorized process, and output model IDs or configuration-presence booleans rather than raw config. A model-list response alone does not prove generation/edit support; verify the documented route and first real asset result.

Keep authorization scopes separate: image generation approval is not video submission approval. Image jobs can incur provider charges too. On authentication or balance failure, stop; on timeout, resolve the original request state before retrying a billable operation.

## Carrying a style change through the project

When a user changes from live action to humorous 3D animation, update character silhouettes, head/body proportions, face/eyelid/eyebrow geometry, costume materials, hair volumes, environment shape language and lighting. Keep character identity, causal action and edit geography intact. Carry the change into every consuming prompt and exclude the former medium only where it is a plausible failure.

Four-view identity sheets still use front, strict side, strict back and portrait; each view depicts the same adult character model at consistent scale. A reference sheet is not a final scene. Exclude its studio background, repeated model views, seams and neutral pose in video prompts. Keyframes should be generated with approved character identity sheets and relevant location input when supported, rather than rebuilding faces from memory.

Inspect results before binding. Correct one failed property at a time, keep accepted properties stable, and preserve selected originals. Record any uncorrected difference that materially affects the story or QA. Do not certify animation or lip sync from still images.
