# Publishing a worked example

Use only when the user asks to publish/share the project to the stated repository or destination. Build and review the public artifact before committing or uploading it. Do not treat publication as approval to submit additional generation jobs.

## Public export

Create a separate copy using an allowlist: story source, director brief, screenplay, dialogue ledger, timing/continuity plan, image and video prompts, selected image assets, portable manifests, edit recipe, final video and any requested original clips. Do not copy the whole workspace or a raw archive that has not been inspected. Exclude credentials, authenticated examples, `.env`, provider responses/URLs, account/balance data, runtime logs, task IDs, temporary files and private absolute paths. Replace absolute links with project-relative paths; rebuild the gallery and validation report in the exported copy.

Disable paid submission in example manifests/jobs and explain how to adapt a private working copy deliberately. Keep the published original outputs available without requiring readers to run the paid renderer. Label source vs preview video, original resolution vs web preview, requested generation duration vs edited duration, model/backend choices, completed corrections and QA limitations. A preview transcode may change resolution/bitrate, but should preserve the full story and audio; do not call it the untouched source.

## Git and release assets

Keep a lightweight preview/poster and source documents in Git. Put large source videos or complete media archives in release assets when that keeps the repository usable. GitHub rejects individual Git blobs over 100 MiB; check sizes before commit, and prefer much smaller web previews. Use relative links inside archives and stable release URLs for large downloads.

Scan the exact staged Git content and every decompressed Release package, not only filenames. Detect live-token patterns (for example long `mk-`, `sk-`, `ghp_`/`gho_` tokens and private key blocks), authenticated URLs/headers, machine-specific paths and provider task records. When a secret is found, remove it from the public export and confirm it never entered committed history; never print the matching secret. Also inspect media metadata. Clearly labeled placeholders such as `mk-xxxxx` are examples, not live secrets.

The repository's license should state how original example source and generated media are intended to be used; distinguish them from external reference materials and avoid asserting provider ownership guarantees. Explain whether normal-speed audiovisual review and exact speech/lip-sync verification are still pending.

## Verification

Run the skill/project validators, any tests affected by executable changes, media probes and portable-link checks before publishing. After push and upload, verify the remote commit/tag, release asset names/sizes and linked resources. Report the repository and case/release links; do not claim a site was deployed unless it actually was.
