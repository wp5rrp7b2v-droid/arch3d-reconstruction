# P3.3 Stage2-C｜Batch 03 Review

- Batch: **Deferred Primary-Frame Groove / Ridge-Counterpart Attachment Classes**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Authority: **D-280**
- Batch 01: **LOCKED / D-277**
- Batch 02: **LOCKED / D-279**
- Engineering execution: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Evidence-bounded result

### A. JOINERY_FEATURE records materialized

1. `CONN-S2C-B03-DINGFU-BRACKET-GROOVE-FAMILY-001`
   - Dingfu → gable column-head bracket-set role
   - direct historical claim is limited to: **groove / bracket-entry feature exists**
   - exact width / depth / length / contour: **UNKNOWN**
   - exact counterpart Master: **UNKNOWN**
   - exact mortise-tenon closure: **NOT CLAIMED**

2. `CONN-S2C-B03-RUFU-BRACKET-GROOVE-FAMILY-001`
   - Rufu → bracket-set role
   - direct historical claim is limited to: **groove / bracket-entry feature exists**
   - same-building photo supports the intersection/entry semantic
   - exact width / depth / length / contour: **UNKNOWN**
   - exact counterpart Master: **UNKNOWN**
   - fixed 45° assumption: **PROHIBITED**

### B. Upper ridge counterpart interfaces recorded but not bound

3. Shuzhu upper ridge-support endpoint:
   `IF-S2C-B03-SHUZHU-UPPER-RIDGE-REGION`

4. Chashou upper ridge-support endpoint:
   `IF-S2C-B03-CHASHOU-UPPER-RIDGE-REGION`

Current evidence establishes the **ridge-support region / endpoint role** but does not yet prove the exact approved Master counterpart.

Therefore:
- counterpart_master_id = **null**
- Connection Layer record = **NOT MATERIALIZED**
- exact historical contact geometry = **UNKNOWN**

This prevents silently converting “ridge region” into “ridge purlin” or another specific Master.

## Candidate counts

- New interfaces: **6**
- New JOINERY_FEATURE records: **2**
- Deferred ridge-counterpart requirements: **2**
- Fabricated exact groove geometry: **0**
- Fabricated exact bracket counterpart Master binding: **0**
- Fabricated ridge counterpart Master binding: **0**

## Candidate consistency check

- Required Connection Layer fields: **12 / 12 on both records**
- Interface references: **4 / 4 resolve**
- Connection kinds: **2 × JOINERY_FEATURE**
- Dingfu exact groove dimensions: **null / UNKNOWN**
- Rufu exact groove dimensions: **null / UNKNOWN**
- historical claim scope: **feature existence only**
- world-coordinate authority: **false**
- instance-generation authority: **false**
- ridge counterpart connection records: **0**
- Shuzhu counterpart Master: **null**
- Chashou counterpart Master: **null**

## Review decision requested

Approve or reject **Stage2-C Batch 03 Candidate**.

Approval would lock:
- the two direct groove-existence JOINERY_FEATURE records;
- the two upper ridge endpoint requirements as explicitly deferred/unresolved.

It would not authorize:
- exact groove geometry;
- exact bracket-set counterpart Masters;
- Shuzhu/Chashou upper-ridge Master bindings;
- Blender engineering;
- Stage3;
- world-coordinate placement;
- T-018 restart.
