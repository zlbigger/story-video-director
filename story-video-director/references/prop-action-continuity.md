# Prop actions and illustrated handoffs

Read before clip splitting for manipulation, repeated attempts, transfers, breakage, ignition, eating/smoking, or persistent scattered objects. These scenes require a physical screenplay, not just a list of verbs. More references help only when they encode consistent states; images do not guarantee motion or object permanence.

## 1. Write the physical screenplay first

For each action specify: visible stimulus → source → anatomical hand and grip → support/contact → trajectory → material/state change → release/destination → reaction. Distinguish anatomical left/right from screen left/right. Explain contact even when off camera; decide which causal contacts must be visible.

Example: paper rests across both hands, left fingers support its underside, right fingers fold its near edge around the tobacco. The paper never spreads unsupported in the air. The finished single cigarette stays pinched in the right hand, travels tip-first to one mouth corner, and only transfers when the lips grip it and fingers release. No second cigarette appears during that transfer.

Treat an introduction, transfer, break, disappearance, or ignition as a visible event with a cause. Do not hide several of these in “he lights a cigarette.” Split the action or use a motivated hand/prop insert if it cannot fit at readable speed. Simplify before increasing prompt length. An intricate 9-second action may need two shorter units; recalculate total duration and estimated cost before submission.

## 2. Maintain a prop state ledger

Create `prop-state-ledger.json` for these scenes. Track stable object IDs (including individual repeated consumables), container position, hand/owner, support, integrity, ignition, and destination at critical beats and every boundary. Track only story-visible counts; do not invent an exact inventory of unseen items inside a closed box.

Suggested structure:

```json
{
  "version": 1,
  "objects": [{"id": "cigarette-01", "kind": "single rolled cigarette"}],
  "snapshots": [{
    "id": "clip-01-end",
    "clip_id": "clip-01",
    "time_seconds": 9,
    "states": [{"object_id": "cigarette-01", "location": "right mouth corner", "holder": "man:lips", "support": "lips", "integrity": "whole", "ignition": "unlit", "visible": true}]
  }],
  "events": [{"clip_id": "clip-01", "time_seconds": 7, "object_id": "cigarette-01", "action": "transfer", "from": "man:right_hand", "to": "man:lips", "cause": "lips grip before fingers release"}]
}
```

Use this as the source for screenplay, image specs, prompts, and handoffs. A broken match retains its ID as named fragments; one stick cannot become several intact sticks. Unlit → lit requires an explicitly planned ignition event; a failed ignition stays unlit. A container never relocates without a carry/drop event. New matches originate from the fixed box, not a shoe, empty fist, or floor. Cigarettes remain singular unless the screenplay introduces another.

For debris continuity, make a reusable floor-layout detail reference with stable landmarks and named zones (e.g. beside the chair's front-left leg). Specify piece counts and approximate spatial order. Compose each consuming frame from this same state. Do not use a floor layout from a future beat in an earlier opening. A changed viewpoint must preserve world coordinates, not identical screen coordinates.

## 3. Generate enough individual keyframes

Create `keyframe-plan.md`: frame ID, exact beat time, role (opening/action checkpoint/outgoing/incoming/detail), required object IDs/state, consuming clips, and image QA status.

- A simple reaction can use one opening frame plus identity/location references.
- A fragile manipulation normally needs an opening, a readable contact checkpoint, and an outgoing frame. Add a second checkpoint when a transfer or break changes ownership or geometry. Select the actual count from the failure risk and provider limits.
- For critical boundaries, illustrate both outgoing and incoming compositions. Same viewpoint can share an approved boundary; a changed viewpoint needs a new composition derived from the same ledger state.
- Generate individual scene frames, not a collage as the primary motion reference. A contact sheet is for human review; upload it only if the provider explicitly supports ordered storyboard conditioning.
- A prop appearance sheet does not replace a contact checkpoint or floor-layout reference.

Before selecting assets, inspect source, contact, grip, singularity, state and debris. If a checkpoint already has a duplicate cigarette, wrong hand, flame, or unsupported paper, repair it before submission. Do not accept it just because the face looks consistent.

## 4. Bind images to time and authority

Every uploaded image needs a filename, slot alias, temporal role, state to inherit and exclusions inside the prompt. Example:

```text
卷烟接触检查@rolling-contact.png（@3）：仅约3秒采用此双手支撑和纸边接触；不作为首帧，不增加第二支烟，不继承静止姿势。
本段尾态@rolled-end.png（@4）：仅约8秒达到此单支烟夹于右嘴角的状态；不提前跳到该动作，不重演转移。
```

Declare precedence: identity anchor owns face/costume, location owns geometry/light, ledger owns count/hand/state, timed action frame owns the specified contact only. Fix contradictory images before prompting; prose cannot reliably override a visibly conflicting reference. Do not upload irrelevant weapon/prop groups to earlier scenes.

Respect the actual provider media ceiling. Keep identity and essential contact references; remove redundant style plates. Split a complex clip if essential states cannot fit the reference budget. Multimodal reference images are guidance, not guaranteed keyframe interpolation. Use first/last-frame conditioning only when supported, in its separate mode; never claim the reference-only adapter schedules exact frame constraints.

## 5. Inspect before committing dependent clips

For a critical state handoff, render upstream first and inspect the retained tail and transition, then choose a clean actual frame. Update the ledger with actual usable state. If it contradicts the story (e.g. ignition despite a scripted failure), repair the upstream unit rather than adopting the error as the new story. Generate the downstream angle from the accepted state and canonical identity. Never automatically seed from a defective last encoded frame.

Use staged projects with the current renderer as described in `continuity-and-edit-design.md`. Review-dependent downstream jobs remain unsent until upstream acceptance. A newly composed view is not an extracted actual frame; record provenance honestly.

## 6. Acceptance and repairs

Watch complete actions at normal speed, then slow down transfer, ignition, breakage and each boundary to check:

- one object stays one object through occlusion and mouth/hand transfer;
- every acquisition has a source; every disappearance has a release/destination;
- fingers/paper/wood have support and contact, with no unsupported reconstruction;
- failed ignition does not produce flame, smoke, ember or another ignition tool;
- fragments and fixed containers match ledger and adjacent frames;
- outgoing/incoming views agree on hand, mouth, floor state and unfinished phase;
- trigger precedes reaction, without a repeated attempt or unexplained reset.

Treat violations as action/state failures, even when overall style is attractive. Record timecodes and evidence; still-frame checks cannot certify the whole event. When motion/audio inspection is unavailable, mark it unverified and deliver a clearly labelled trial only. Repair the earliest cause: simplify screenplay, add missing contact frame, repair asset, change coverage, trim an observed duplicated phase, or regenerate the smallest failing unit within authorized spend. Never replace a failure with undisclosed still motion.

## 7. Regression example: matchstick short

Observed trial errors: airborne cigarette assembly and duplicate mouth cigarette; a flame on acquisition; changing match identity; matches appearing from shoe/floor; an unexplained box/lighter; inconsistent floor debris. A robust revision separates rolling, single cigarette transfer, box acquisition, one failed strike, discard, reacquisition, and reaction into readable actions. It uses a supported-paper checkpoint, single-cigarette transfer checkpoint, unlit-match grip detail, break/discard detail, and a shared floor-layout state across late shots. It does not merely append “no deformation” to the original prompt.
