# Continuity and edit design

Read before splitting a multi-clip story into final prompts. The goal is a comprehensible, emotionally continuous film, not invisible cuts at all costs.

## 1. Write across the cut

Build a causal spine: intention → visible action → consequence → reaction → next choice. Write the scene without provider duration limits first, then place generation boundaries at readable action phases, changes in attention, or dramatic turns. Keep each generated unit within 15 seconds; split or simplify a complicated action instead of speeding through it.

Avoid giving every segment a fresh establishing shot, repeated setup, musical intro, and closing pose. An outgoing shot can leave a purposeful action or question open. The incoming shot must continue or answer it before introducing unrelated information. Preserve emotional intensity and what each character knows; a frightened character does not reset to a neutral reference pose.

A cut must either continue something or make an intentional change legible. If changing time or place, establish a cue (departure/arrival, light, ambience, wardrobe, or requested post-production text). Do not hide a story gap behind a dissolve.

## 2. Choose the boundary by its job

| Situation | Preferred approach | Conditions to preserve |
|---|---|---|
| Same action, same camera trajectory | Actual-frame continuation when needed | Pose, contact, direction, action phase, subject and camera velocity; a still image constrains only appearance |
| Same action, useful new viewpoint | Match on action | Cut during a readable movement; incoming shot resumes its next phase without replaying it; preserve axis and prop hand |
| A person sees or hears something | Eyeline/reaction cut | Establish cue and gaze, reveal target at compatible screen direction, then a motivated reaction |
| Dialogue exchange | Shot/reverse shot or listener reaction | Stable geography, speaker ownership, breath and response timing; avoid resetting posture |
| Weak generated seam with valid story | Motivated detail or reaction insert | Insert supplies relevant information and covers an understood action; never invent an unrelated distraction |
| Time/place changes | Explicit ellipsis or motivated match cut | Explain the jump; shape/color matching is a visual rhyme, not proof of physical continuity |
| Scene begins before its picture or ends after it | J-cut / L-cut audio bridge | J: incoming sound precedes picture; L: outgoing sound continues after picture; specify actual timeline offsets |

Do not prescribe a dissolve by default: it can produce double faces, obscure causality, and read as elapsed time. Do not cross the action axis without an orienting view or a visible camera crossing. A small arbitrary viewpoint jump is usually less natural than staying in the shot or choosing a clearly informative new view.

## 3. Boundary contract

Create `02-continuity-plan.md` for N clips with exactly N−1 adjacent handoffs in timeline order. Use this compact record for each, omitting irrelevant details:

- **Pair and motivation:** clip IDs, what motivates the cut, and what the viewer expects next.
- **Story relation:** same moment / continuous elapsed action / intentional ellipsis; explain any time or location change.
- **Outgoing → incoming state:** character position, facing, eyeline, emotional state, costume, prop ownership/contact, action phase, screen direction, landmarks and light. Record intended changes as well as locks.
- **Motion:** subject direction and approximate speed, camera direction/speed, and whether either actually stops. Do not make an actor stop solely because the API clip ends.
- **Picture strategy:** selected technique, intended cut cue and opening behavior; include reference provenance (planned frame or extracted actual frame). For a new angle, design a new composition preserving world state instead of reusing the old frame literally.
- **Sound strategy:** ambience, dialogue, effects and music across the cut; absolute project timing for bridges, fades and speech. Use one score timeline when music is continuous. Do not ask each clip to restart the same track.
- **Execution:** generation dependency if actual footage is needed; planned source in/out points and any editing handles; required post-production operation.
- **Acceptance:** observable success condition, actual review status (`planned`, `needs_repair`, `verified`), and evidence paths/timecodes after rendering. Never mark an unrendered boundary verified.

For a continuing acted scene, add the **performance carryover**: the last stimulus, what each named actor now knows or refuses to admit, their active tactic, and the first behavior in the next clip. A matching face and costume cannot compensate for a wife becoming emotionally neutral after hearing her husband's farewell. Review runs of three adjacent clips as setup → changed tactic → consequence; this catches a middle clip that visually matches its neighbors but advances neither the story nor the emotion.

These are director/editor instructions, not automatically supported API fields. Put relevant visual/action/sound instructions inside each copyable model prompt; keep edit decisions and verification records outside it. Do not refer to an absent image as if uploaded.

## 4. Actual-frame continuation without propagating defects

Use this only where the story and geometry call for a continuous view:

1. Plan compatible outgoing and incoming states and a plausible physical path. Do not require a complicated transformation merely to reach a target frame.
2. Render upstream footage and watch its ending. Inspect identity, hands, prop contact, lighting, motion, blur, and camera movement. Choose the last **usable retained** frame, not blindly the final encoded frame. Record source file and timestamp/frame index.
   Compare the rendered face and body to the canonical identity anchor and the previous usable frames. A distorted tail must not become the next clip's identity seed.
3. If the tail is defective, trim to a valid handoff, repair/regenerate the failing segment within authorization, or redesign the cut. Do not cascade distorted anatomy into all later clips. A new paid retry needs authorization consistent with the existing cost scope; stop if that scope is unclear.
4. For a same-view continuation, save the actual boundary image in `assets/shots/`; use it as `first_frame` in frame mode, or as a composition reference in supported multimodal mode. Multimodal reference does not guarantee exact first-frame adherence. Preserve independent identity anchors where the mode permits them.
5. Tell the next prompt the ongoing motion and its next phase explicitly. A still frame cannot convey speed, acceleration, or which way a hand is moving. Do not repeat the action that has already happened.
6. Watch both clips together. Remove an actual duplicate frame or opening hold only when observed, at the correct frame rate; never apply a blind fixed trim. If an earlier frame was chosen, trim the upstream clip to that corresponding edit point. Recompute edited runtime.

Planned first/last conditioning can help where supported, but does not prove the model hit either target. Do not chain a change of scene or angle merely because the tool supports chaining.

### Current renderer limits and staged execution

`scripts/metaso_h3_video.py` currently supports `chain_from_previous: true` with exactly one `chain_boundary: true` reference of role `first_frame` or `reference_image`. It extracts the preceding downloaded clip's ending automatically and then submits the next job. It does **not** visually inspect that frame, choose a usable timestamp, pause for handoff review, or implement arbitrary dependency graphs. Preflight expects referenced files to exist; planned frame assets must be real and clearly recorded as planned until replaced.

For review-dependent chains, do not launch all dependent clips through that automatic loop. Prepare separate validated stage project directories with only the current job(s), existing assets and stage-local duration; run each with `--no-assemble`. Copy successful footage and approved extracted frames into the canonical project, update the next stage references, then validate and submit that stage. Preserve each stage's task records; the script does not safely resume a full project and rerunning it is now refused when saved task IDs exist; the guard does not implement task resume. Disable `chain_from_previous` when supplying an already approved extracted frame so it is not overwritten.

The stock assembler is a technical concat baseline with per-segment audio fades. It does not execute J/L cuts, selected in/out points, overlapped video, or `master_audio` mixing. When the edit plan needs those, use `--no-assemble` and an explicit FFmpeg/editor timeline, save the edit recipe in the project, and verify the rendered result. Do not describe an intended bridge as an implemented bridge.

## 5. Sound and duration

Prefer an independently managed continuous ambience/music bed over independently generated restarts. Retain useful synchronous effects. Avoid duplicated footsteps, interrupted breaths, clipped words, sudden noise-floor changes, and two copies of the same music. Overlap dialogue only when intentionally scripted. Micro fades prevent clicks; they do not repair a broken sound world.

Optional short editing handles must fit within each ≤15-second generated clip and within the spoken-content budget. Do not add arbitrary holds at every edge. Record source in/out points, output start times and overlaps in the continuity plan. Generated runtime is the sum of requested clip durations; edited runtime is the sum of retained durations minus video overlaps. Audio bridges alone do not shorten picture runtime. Preserve `total_duration_seconds` as the generated sum for the existing validator; report edited runtime separately in the plan and verify it against the final file. Do not use the stock full-duration assembler for a trimmed edit.

## 6. Example: hear a knock, open the door, reveal a visitor

Weak: A hears a knock and becomes still; B repeats the knock, re-establishes the room and reaches for the door; C starts with the person already outside. Tail-frame similarity cannot explain that missing action.

Better, using illustrative 8-second units:

- **A:** The knock interrupts writing. The character turns toward the door on screen right, rises, reaches it and depresses the handle with the right hand. End while the door begins opening, not in a posed freeze.
- **A → B:** Match on action. B starts from a closer interior angle on the same side of the axis. The door is already opening and continues at the same speed; the same right hand stays on the handle. The opening reveals the visitor. Keep the room tone and one continuous hinge sound in the edit; do not repeat the knock. This angle change calls for a matching newly composed opening, not literal tail-frame reuse.
- **B → C:** The visitor's expression motivates a reverse reaction shot of the resident. Preserve gaze, doorway geometry and the slightly open door. Carry exterior rain under the cut. A close reaction supplies new emotional information without replaying the reveal.

If B instead continues A's identical camera view, an approved actual end frame is appropriate; still specify that the door continues opening with existing velocity. If the next scene is the following morning outdoors, choose an explicit time/location transition and a fresh frame.

## 7. Review and repair in order

Watch 1–2 seconds on both sides of every cut at normal speed with sound; use slow/frame inspection to diagnose, not as the sole test. Review:

1. Causality and emotion: no missing motivation, repeated event, or emotional reset.
2. Geography and state: consistent direction, gaze, contact, identity, props and intentional changes.
3. Motion and rhythm: no duplicated action, velocity snap, camera reset, freeze or accidental pause.
4. Sound: no clipped speech, duplicated effects, restarted score or unexplained ambience break.
5. Technical output: no black/duplicate frames, size/fps mismatch, or incorrect edited duration.

Repair the earliest cause: rewrite the handoff for a story gap; redesign coverage for geometry; adjust an edit point for repeated motion; remix sound for an audio seam. Regenerate only the affected clip when needed, then recheck both neighboring cuts. Stop when the cut passes these observations; do not keep spending to chase imperceptible differences. Structural validators cannot certify these aesthetic properties. If inspection or editing is unavailable, report the boundary as unverified and state the concrete missing step.
