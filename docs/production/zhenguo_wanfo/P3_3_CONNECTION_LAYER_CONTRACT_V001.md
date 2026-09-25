# P3.3 Connection Layer Contract V001

Status: **PROOF-BOUND / PRODUCT OWNER DIRECTED / 2026-09-25**

## Purpose
A component assembly is not complete when two Master bodies merely touch.

P3.3 assembly success requires an explicit **Connection Layer** between participating Masters.

## Connection kinds
1. `PHYSICAL_CONNECTOR`
   - independent physical piece such as 散斗 / 木楔 / connector block;
   - must have its own connection identity;
   - may later be promoted to a full Component Master if evidence/registry coverage closes.

2. `JOINERY_FEATURE`
   - mortise / tenon / groove / notch or other parent-material cut;
   - belongs to one or more parent Masters at assembly realization;
   - does not require a separate physical component identity.

3. `CONTACT_INTERFACE`
   - bearing/contact relation with no separately modeled connector;
   - must still have explicit interface identity, contact faces and validation.

## Required fields
Every Connection Layer record must declare:
- connection_id
- connection_kind
- participants
- structural_semantic
- evidence_binding
- geometry_classification
- historical_claim
- replaceable
- lower_interface
- upper_interface
- resolver
- validation_tolerance
- prohibited_claims

## Evidence rule
Under RC-020 + RC-023:
- missing Northern-Song / 963 exact connector dimensions or joinery does not block assembly production;
- missing geometry may use explicit replaceable `RECONSTRUCTED_DESIGN` / `CONNECTOR_PROXY`;
- such proxy geometry must never be described as historical original geometry.

## Complete Assembly Success
A complete proof must validate:
1. all participating Master identities;
2. one explicit Connection Layer identity;
3. machine-readable lower/upper interfaces;
4. connector or joinery geometry is generated from the connection record;
5. both sides close within tolerance;
6. no unexplained interpenetration;
7. mutation of a connection parameter propagates automatically;
8. no manual Blender transform;
9. deterministic clean-state rebuild;
10. test geometry is not promoted to building/historical authority.

## T-032 proof instance
Evidence chain:
- 下层：上六椽栿
- Connection Layer：散斗 physical connector semantics
- 上层：四椽栿

Direct source states:
- 四椽栿位于上六椽栿之上；
- 二者之间设置隔架单栱一组；
- 四椽栿下不用栌斗；
- 由散斗承托。

For T-032:
- the **existence / role** of 散斗 is evidence-backed;
- exact 散斗 geometry/count/963 dimensions remain unresolved;
- generated 散斗 body is therefore `RECONSTRUCTED_DESIGN / PHYSICAL_CONNECTOR_PROXY / TEST_ONLY`;
- T-032 does not claim to close the full 隔架单栱 group geometry.
