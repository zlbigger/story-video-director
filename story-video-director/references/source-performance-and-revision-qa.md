# Source adaptation, voice anchors and revision QA

Read for source-based adaptations or revision-heavy acted films. Use only the sections relevant to the current project.

## Source understanding before production

Record the source reading order explicitly; manga is not universally right-to-left. Distinguish file order, page order and panel order. Trace critical scenes with a compact ledger:

`source page/panel | observed event | interpretation/uncertainty | era/location | character age/costume | exact line | visible speaker or offscreen sound source | selected shot`

Resolve ambiguous spatial relationships, flashbacks and endings before dependent paid generation. A cramped drawing or overlapping silhouette does not establish that two people physically share a room. Inspect the source and distinguish observation from inference. For offscreen comfort, establish who is outside, who is listening inside, and which visible mouth remains closed. Character dialogue can be offscreen without becoming an external narrator.

Build identity variants by story era: a character can legitimately change age, hair or clothing across time. Compare a suspicious costume with the source and the same-era anchor before declaring drift. Keep character styling, architecture and props consistent with the source's cultural setting.

When corrected, supersede the affected screenplay, dialogue ledger, prompts and selected-shot metadata together. Label withdrawn interpretations and rejected assets explicitly; their presence in an archive does not make them valid references.

## Approved performance as a voice anchor

For a recurring voice that needs repair, generate a short representative candidate before replacing every line. Test age, timbre and a meaningful emotional turn. Older delivery needs believable breath, consonant onset, phrase endings and pauses; lowering pitch or slowing playback alone is insufficient.

After approval, extract the actual accepted generated audio as the voice reference, when the provider supports that reference mode. Specify inherited timbre/delivery and excluded reference words, incidental music and ambience. Do not promise exact voice cloning. Record the source clip, audio range, character/age variant and scope of user approval.

Before bulk submission, inspect whether that input mode preserves every visible character, including silent foreground listeners. A voice improvement can introduce visual identity drift. Use appropriate identity anchors and coverage, then inspect the actual output. Preserve satisfactory voices and footage during a local repair.

## Repair records and final edit clocks

Record each defect as:

`film version/time | native clip/time | observed fault | suspected cause | crop/edit recipe | replacement | selected/rejected | final-film verification`

Inspect the entire moving subject trajectory for headroom and face coverage. Maintain proportional scaling. Cropping cannot recover a head already absent from the native footage; regenerate with a wider/taller opening composition. If side fill is needed, derive it from the moving footage and distinguish it from the main proportional picture.

For long assemblies, avoid repeated per-piece AAC encoding/concatenation that can accumulate clock offsets. Align picture to fixed frame counts, assemble a continuous PCM master, then encode final audio once. Picture-only repairs may retain an unchanged audio stream. Derive speech edit windows from actual native audio with breathing margins; do not assume a fixed onset. After duration changes, rebuild absolute dialogue/subtitle times.

Compare source waveforms with the final encoded film to detect placement drift. Reliable correlation proves audio position only, not words, emotion or phonetic mouth accuracy. Treat weak/ambiguous matches as unverified. Verify visible mouths and audible speech together at normal speed through supported review or explicit user review.

Recheck repaired footage in the final film and both neighboring cuts. Keep rejected paid candidates labeled and excluded from active selection. Re-export only affected pieces and the final master where practical; repeat wider checks when changes or failures justify them.

## Review scope and stopping

Separate candidate approval, batch approval and whole-film acceptance. Store explicit user acceptance against the exact reviewed version; do not convert it into a claim that the agent independently heard or verified every phoneme. With appropriate technical checks and explicit whole-film acceptance, update the delivery state and stop pending-review loops. Silence does not count as approval.

Continue independent work while one grouped review question is pending. Poll existing live job handles without resubmitting. If truly input-bound, state the remaining decision once; repeated wait messages, counters and unchanged audits are not progress. Reuse already-authorized session credentials securely in memory when available, never in prompts, logs or archives.

## Local production archive

When requested, or useful for many revisions, make a local HTML archive connecting source/script, assets, full copyable prompts, uploaded references, generated clips, repairs and film versions. Include search/filter, image zoom, active/obsolete/rejected labels and real before/after descriptions. Distinguish historical versions from the accepted master.

For offline use, embed text metadata and use URL-encoded relative local media links; avoid fetching JSON from file://. Escape HTML and embedded JSON (including `<`), redact credentials and omit authenticated request dumps. Lazy-load images, preload only video metadata, and stop playback on tab/version changes. Keep navigation usable on small screens.

Validate local targets and JavaScript syntax. Report runtime or visual checks only if actually performed. Update the archive, review pages, timeline, subtitles, selected-shot map and delivery status together after a version change. Public publication remains a separate operation governed by public-showcase.md.
