# P3.3｜Interior Huagong Target Source Binding V001

Status: **SOURCE BOUND / TARGET SUBSET ONLY / MASTER NOT YET AUTHORIZED**
Date: 2026-10-06

## Identity

- proposed component id: `CMP-FRAME-HUAGONG-INTERIOR-001`
- proposed master id: `CMP-FRAME-HUAGONG-INTERIOR-001_MASTER`
- canonical name: `华栱（梁架襻间进深）`
- system: `主体梁架 / 襻间承托`
- current target subset: East-Seam front/rear `上平槫下襻间`
- whole-hall count: UNKNOWN

This is a separate provenance/data-model family from the outer-eaves `CMP-GONG-HUAGONG-001_MASTER`.

The separation prevents unsupported inheritance. It does not assert that historical craftsmen used a different generic name.

## Direct source

Authority: `SRC-ZG-WF-001`

Appendix 1-9 / PDF p347 / printed p332 gives position-labelled target records:

### 东缝前上平槫下襻间
- component: `进深华栱`
- 广 = 221 mm
- 厚 = 153 mm
- 长 = `一端栱头，一端至托脚`

### 东缝后上平槫下襻间
- component: `进深华栱`
- 广 = 210 mm
- 厚 = 156 mm
- 长 = `一端栱头，一端至托脚`

## Bound facts

- target member identity = 华栱;
- target direction = 进深;
- target location = East-Seam front/rear upper-purlin Panjian node;
- target front/rear section values are position-specific direct observations;
- one end is gong-head; the other terminates at the Tuojiao according to the source description.

## Not bound

- numeric full length;
- exact endpoint coordinates;
- exact side profile;
- exact gong-head geometry;
- hidden overlap / slot / mortise / tenon;
- whole-hall count;
- equality with outer-eaves first/second-jump Huagong.

## Geometry authority boundary

Outer-eaves Huagong dimensions/profile may not be copied as target geometry authority.

Future target realization must be:
`DIRECT_SECTION + ASSEMBLY_ENDPOINT_DERIVED_LENGTH / REPLACEABLE`

until stronger direct length evidence is found.
