#!/usr/bin/env python3
"""T-007: deterministic, evidence-aware medium-LOD structural skeleton.

Coordinates are millimetres: X=front width, Y=depth, Z=column-foot design
plane.  Box and line cross sections are diagrammatic module-derived envelopes,
not claims about exact member sections, joints, or corner carpentry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CASE = ROOT / "production/zhenguo_wanfo"
PARAMS = CASE / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
OVERRIDES = CASE / "params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json"
MATRIX = CASE / "dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json"
SCHEMA = CASE / "schema/evidence_aware_parameter_schema_v001.json"
DECISIONS = ROOT / "docs/project_control/decision_log.md"
OUTPUT = CASE / "output/P2_2_STRUCTURAL_SKELETON_V001.blend"
MANIFEST = CASE / "build/P2_2_BUILD_MANIFEST_V001.json"
REVIEW = CASE / "review"
PREFIX = "P2_2_STRUCTURAL_SKELETON_V001"

# Declared before inspecting geometry. All numeric comparisons use millimetres.
MACHINE_TOLERANCE_MM = 0.01
DETERMINISTIC_TOLERANCE_MM = 0.0001
ALLOWED_ROLES = {"DIRECT_GEOMETRY_INPUT", "DERIVED_GEOMETRY_RULE"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    return str(Path(path).resolve().relative_to(ROOT))


def read_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


class FormalInputs:
    """Read-only gateway; geometry can only request permitted dependency roles."""

    def __init__(self, params=PARAMS, overrides=OVERRIDES, matrix=MATRIX):
        self.paths = {"formal_parameter_set": Path(params), "approved_overrides": Path(overrides),
                      "geometry_dependency_matrix": Path(matrix), "evidence_schema": SCHEMA}
        self.formal = read_json(params)
        self.sidecar = read_json(overrides)
        self.matrix = read_json(matrix)
        self.schema = read_json(SCHEMA)
        self.parameters = self.formal["parameters"]
        self.entries = self.matrix["entries"]
        if len(self.parameters) != 85 or set(self.parameters) != set(self.entries):
            raise ValueError("Formal reader requires matching 85/85 parameter and dependency IDs")
        if self.formal["parameter_set_version"] != "V001" or self.matrix["matrix_version"] != "V001":
            raise ValueError("Unexpected formal input version")
        if self.parameters["Z-006"]["value"] is not None or self.parameters["Z-006"]["classification"] != "UNKNOWN" or self.parameters["Z-006"]["production_use"] != "DO_NOT_LOCK":
            raise ValueError("Z-006 historical UNKNOWN boundary changed")
        if self.entries["Z-006"]["unknown_dependency_status"] != "BLOCKS_P2_2_GEOMETRY":
            raise ValueError("Z-006 blocking dependency changed")
        if self.entries["DG-114"]["unknown_dependency_status"] != "BOUNDED_NON_BLOCKING" or self.entries["DG-114"]["geometry_dependency_role"] != "NOT_USED_IN_P2_2":
            raise ValueError("DG-114 boundary changed")
        if self.entries["HIS-002"]["geometry_dependency_role"] != "METADATA_ONLY":
            raise ValueError("HIS-002 boundary changed")
        decisions=DECISIONS.read_text(encoding="utf-8").splitlines()
        for ident,required in {"D-023":("Product Owner 批准","11 × MOD-006","REASONABLE_COMPLETION"),
                               "D-024":("P2.1","PASS"),
                               "D-025":("P2.2 Definition of Done","T-007")}.items():
            row=next((line for line in decisions if line.startswith("| "+ident+" |") or line.startswith("| **"+ident+"** |")),"")
            if not row or not all(token in row for token in required) or "ACTIVE" not in row:
                raise ValueError("Approval boundary missing/inconsistent: "+ident)
        self.resolution = self._validate_override()
        self.used = set()
        self.rules = {}

    def _validate_override(self):
        candidate = self.sidecar.get("overrides", {}).get("Z-006-RC-01")
        if self.sidecar.get("override_set_version") != "V001" or set(self.sidecar.get("overrides", {})) != {"Z-006-RC-01"} or not isinstance(candidate, dict):
            raise ValueError("Approved override identity/version changed")
        required = {"candidate_id":"Z-006-RC-01", "target_parameter_id":"Z-006",
                    "target_parameter_key":"column_height_963_design_mm", "classification":"REASONABLE_COMPLETION",
                    "time_layer":"reconstructed_963_candidate", "production_use":"DEFAULT_REPLACEABLE_CANDIDATE",
                    "formula":"11 * MOD-006", "depends_on":["MOD-006"], "unit":"mm",
                    "is_replaceable":True, "approval_decision_id":"D-023",
                    "status":"APPROVED_FOR_P2_2_CANDIDATE_USE", "multiplier":11}
        if any(candidate.get(key) != value for key,value in required.items()):
            raise ValueError("D-023 approved override fields changed")
        if not {"E-018","HR-01A","D-023"}.issubset(set(candidate.get("evidence_basis",[]))) or not candidate.get("historical_claim_boundary"):
            raise ValueError("D-023 evidence/claim boundary missing")
        mod = self.parameters["MOD-006"]["value"]
        from decimal import Decimal
        resolved = Decimal(str(candidate["multiplier"])) * Decimal(str(mod))
        if Decimal(str(candidate["current_resolved_value"])) != resolved:
            raise ValueError("Approved override cached resolution is stale")
        return {"resolved_value":float(resolved)}

    def value(self, ident):
        role = self.entries[ident]["geometry_dependency_role"]
        if role not in ALLOWED_ROLES:
            raise ValueError("Non-geometric role requested for geometry: " + ident + " / " + role)
        p = self.parameters[ident]
        value = p["value"]
        if value is None:
            raise ValueError("Null formal geometry parameter: " + ident)
        self.used.add(ident)
        return value

    def derived(self, name, value, formula, sources):
        self.rules[name] = {"formula": formula, "source_parameter_ids": list(sources), "resolved_value_mm": value}
        return value

    def snapshot(self):
        return {ident: {"value": self.parameters[ident]["value"], "unit": self.parameters[ident]["unit"],
                        "role": self.entries[ident]["geometry_dependency_role"]} for ident in sorted(self.used)}


def geometry_plan(inputs):
    v = inputs.value
    fen, chi = float(v("MOD-002")), float(v("MOD-001"))
    front_count, depth_count = int(v("PM-001")), int(v("PM-002"))
    if (front_count, depth_count) != (3, 3):
        raise ValueError("V001 topology mapping requires three front and three depth bays")
    front_center = inputs.derived("front_center_bay_mm", v("PM-008") * chi, "PM-008 * MOD-001", ["PM-008", "MOD-001"])
    depth_center = inputs.derived("depth_center_bay_mm", v("PM-009") * chi, "PM-009 * MOD-001", ["PM-009", "MOD-001"])
    side = inputs.derived("side_bay_mm", v("PM-010") * chi, "PM-010 * MOD-001", ["PM-010", "MOD-001"])
    width, depth = float(v("PM-011")), float(v("PM-012"))
    if abs(2 * side + front_center - width) > MACHINE_TOLERANCE_MM or abs(2 * side + depth_center - depth) > MACHINE_TOLERANCE_MM:
        raise ValueError("Design bay chain disagrees with formal overall dimensions")
    xs = [-width / 2, -front_center / 2, front_center / 2, width / 2]
    ys = [-depth / 2, -depth_center / 2, depth_center / 2, depth / 2]
    if int(v("PM-013")) != 2 * (len(xs) + len(ys)) - 4 or int(v("PM-014")) != 0:
        raise ValueError("Formal column counts disagree with perimeter grid topology")
    cai = float(v("MOD-006"))
    if abs(cai - float(v("MOD-005")) * fen) > MACHINE_TOLERANCE_MM:
        raise ValueError("Full-cai modular chain inconsistent")
    column_height = inputs.derived("Z-006-RC-01", self_float(inputs.resolution["resolved_value"]),
                                   "approved Z-006-RC-01.multiplier * MOD-006", ["MOD-006", "Z-006-RC-01"])
    diameter = float(v("Z-002"))
    corner_rise = float(v("Z-005"))
    datum = v("Z-007")
    match = re.fullmatch(r"Z\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)); abstract column-foot design plane", datum)
    if not match:
        raise ValueError("Unsupported Z datum rule")
    datum_z = float(match.group(1))
    if not math.isfinite(datum_z):
        raise ValueError("Nonfinite Z datum")
    # The sequence is an approved control chain, read in eave-to-ridge order.
    horizontal_fen = v("FR-007")
    rises_fen = [v("ROOF-007"), v("ROOF-008"), v("ROOF-009")]
    if len(horizontal_fen) != 3 or sum(rises_fen) != v("ROOF-010"):
        raise ValueError("Roof control chain inconsistent")
    roof_rise = float(v("ROOF-011"))
    if abs(roof_rise - sum(rises_fen) * fen) > MACHINE_TOLERANCE_MM:
        raise ValueError("Roof rise mm and fen conflict")
    frame_rises_fen = [v("ROOF-004"),v("ROOF-005"),v("ROOF-006")]
    # The two approved rise series are recorded separately; no silent merging.
    roof_sequence = [0.0]
    for item in horizontal_fen:
        roof_sequence.append(roof_sequence[-1] + item * fen)
    lower_ang_rise = inputs.derived("lower_ang_rise_mm", float(v("DG-113"))*fen,
                                    "DG-113 * MOD-002",["DG-113","MOD-002"])
    roof_z = [datum_z + column_height + lower_ang_rise]
    for item in rises_fen:
        roof_z.append(roof_z[-1] + item * fen)
    gable = inputs.derived("gable_projection_mm", v("OUT-003") * fen, "OUT-003 * MOD-002", ["OUT-003", "MOD-002"])
    frame_depths = [float(v("FR-004")), float(v("FR-005")), float(v("FR-006"))]
    if abs(sum(frame_depths) - depth / 2) > MACHINE_TOLERANCE_MM:
        raise ValueError("Primary frame depth chain does not reach column line")
    frame_y = [0.0, frame_depths[0], sum(frame_depths[:2]), sum(frame_depths)]
    frame_tier_z = [datum_z + column_height + lower_ang_rise + sum(frame_rises_fen[:3-k])*fen
                    for k in range(3)]
    if "双杪双下昂" not in v("DG-001") or "双杪" not in v("DG-002") or "六椽栿" not in v("RF-001"):
        raise ValueError("V001 topology vocabulary changed; review mapping")
    jump_a = inputs.derived("first_second_jump_total_mm",float(v("DG-110"))*fen,"DG-110 * MOD-002",["DG-110","MOD-002"])
    jump_b = inputs.derived("third_fourth_jump_total_mm",float(v("DG-111"))*fen,"DG-111 * MOD-002",["DG-111","MOD-002"])
    lower_ang_run = inputs.derived("lower_ang_run_mm",float(v("DG-112"))*fen,"DG-112 * MOD-002",["DG-112","MOD-002"])
    if abs(lower_ang_run - jump_b) > MACHINE_TOLERANCE_MM:
        raise ValueError("Lower-ang run and outer jump aggregate conflict")
    section_width = inputs.derived("diagrammatic_section_width_mm",float(v("MOD-003"))*fen,"MOD-003 * MOD-002",["MOD-003","MOD-002"])
    section_depth = inputs.derived("diagrammatic_section_depth_mm",float(v("MOD-004"))*fen,"MOD-004 * MOD-002",["MOD-004","MOD-002"])
    section_height = inputs.derived("diagrammatic_section_height_mm",float(v("MOD-005"))*fen,"MOD-005 * MOD-002",["MOD-005","MOD-002"])
    for k,ident in enumerate(("ROOF-007","ROOF-008","ROOF-009"),1):
        inputs.derived("roof_rise_interval_%d_mm" % k,rises_fen[k-1]*fen,ident+" * MOD-002",[ident,"MOD-002"])
    for k,ident in enumerate(("ROOF-004","ROOF-005","ROOF-006"),1):
        inputs.derived("frame_rise_interval_%d_mm" % k,frame_rises_fen[k-1]*fen,ident+" * MOD-002",[ident,"MOD-002"])
    inputs.derived("roof_half_run_mm",roof_sequence[-1],"sum(FR-007) * MOD-002",["FR-007","MOD-002"])
    return locals()


def self_float(value):
    return float(value)


def roof_height_at_y(plan, y):
    """Piecewise-linear diagrammatic interpolation of approved roof controls."""
    distance = abs(y)
    offsets = [plan["roof_sequence"][-1]-r for r in plan["roof_sequence"]]
    heights = plan["roof_z"]
    for k in range(len(offsets)-1):
        if offsets[k] >= distance >= offsets[k+1]:
            factor = (offsets[k]-distance)/(offsets[k]-offsets[k+1])
            return heights[k] + factor*(heights[k+1]-heights[k])
    if distance <= MACHINE_TOLERANCE_MM:
        return heights[-1]
    raise ValueError("Frame tier outside approved roof half-run")


def create_model(inputs, plan):
    import bpy
    from mathutils import Vector
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.name != "Collection" and collection.users == 0:
            bpy.data.collections.remove(collection)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    colors = {"GRID": (0.25, 0.25, 0.25, 1), "COLUMN": (0.52, 0.28, 0.12, 1),
              "FRAME": (0.20, 0.35, 0.52, 1), "BRACKET": (0.75, 0.42, 0.12, 1),
              "ROOF": (0.12, 0.45, 0.42, 1), "GABLE": (0.53, 0.25, 0.48, 1)}
    records = []
    counters = {}

    def coll(family):
        name = "P2_2_" + family
        if name not in bpy.data.collections:
            c = bpy.data.collections.new(name)
            scene.collection.children.link(c)
        return bpy.data.collections[name]

    def mark(obj, family, ids, *, boundary="candidate_control", subtype=""):
        for old in list(obj.users_collection):
            old.objects.unlink(obj)
        coll(family).objects.link(obj)
        obj.color = colors[family]
        source = [inputs.parameters[x] for x in ids if x in inputs.parameters]
        obj["historical_state_tag"] = "reconstructed_963_candidate"
        obj["evidence_class"] = "+".join(sorted(set(p["classification"] for p in source))) or "REASONABLE_COMPLETION"
        obj["source_layer"] = "+".join(sorted(set(p["source_layer"] for p in source))) or "D-023_APPROVED_OVERRIDE"
        obj["originality_status"] = "unknown"
        obj["parameter_ids"] = ",".join(ids)
        obj["override_ids"] = "Z-006-RC-01" if "Z-006-RC-01" in ids else ""
        obj["reasonable_completion_ids"] = ",".join(x for x in ids if x == "Z-006-RC-01" or x in inputs.parameters and inputs.parameters[x]["classification"] == "REASONABLE_COMPLETION")
        obj["bounded_placeholder"] = boundary == "bounded_placeholder"
        obj["topology_type"] = subtype
        records.append({"name": obj.name, "family": family, "parameter_ids": ids,
                        "historical_state_tag": obj["historical_state_tag"], "evidence_class": obj["evidence_class"],
                        "source_layer": obj["source_layer"], "originality_status": "unknown",
                        "override_ids": obj["override_ids"], "reasonable_completion_ids": obj["reasonable_completion_ids"],
                        "bounded_placeholder": obj["bounded_placeholder"], "topology_type": subtype})
        counters[family] = counters.get(family, 0) + 1

    def beam(name, a, b, w, h, family, ids, *, boundary="candidate_control", subtype=""):
        va, vb = Vector(a), Vector(b)
        delta = vb - va
        if delta.length <= 0:
            raise ValueError("Zero-length beam " + name)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(va + vb) / 2)
        ob = bpy.context.object
        ob.name = name
        ob.dimensions = (w, h, delta.length)
        ob.rotation_euler = delta.to_track_quat("Z", "Y").to_euler()
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        ob["endpoint_a_mm"] = list(a)
        ob["endpoint_b_mm"] = list(b)
        mark(ob, family, ids, boundary=boundary, subtype=subtype)
        return ob

    xs, ys = plan["xs"], plan["ys"]
    grid_w = plan["section_depth"] / 10  # graphic line weight, module derived
    for j, y in enumerate(ys):
        beam("GRID_Y%02d" % j, (xs[0], y, plan["datum_z"]), (xs[-1], y, plan["datum_z"]), grid_w, grid_w, "GRID", ["PM-001", "PM-008", "PM-010", "MOD-001", "Z-007"])
    for i, x in enumerate(xs):
        beam("GRID_X%02d" % i, (x, ys[0], plan["datum_z"]), (x, ys[-1], plan["datum_z"]), grid_w, grid_w, "GRID", ["PM-002", "PM-009", "PM-010", "MOD-001", "Z-007"])
    columns = []
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if i not in (0, len(xs)-1) and j not in (0, len(ys)-1):
                continue
            corner = i in (0, len(xs)-1) and j in (0, len(ys)-1)
            height = plan["column_height"] + (plan["corner_rise"] if corner else 0)
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=plan["diameter"]/2,
                                                depth=height, location=(x, y, plan["datum_z"]+height/2))
            ob = bpy.context.object
            ob.name = "COLUMN_X%02d_Y%02d" % (i,j)
            mark(ob, "COLUMN", ["PM-013", "PM-014", "Z-002", "Z-005" if corner else "Z-006-RC-01", "Z-006-RC-01"])
            columns.append((i,j,x,y,height))
    zframe = plan["datum_z"] + plan["column_height"] + plan["lower_ang_rise"]
    for i, x in enumerate(xs):
        beam("FRAME_DEPTH_X%02d" % i, (x,ys[0],zframe),(x,ys[-1],zframe),
             plan["section_width"],plan["section_height"],"FRAME",
             ["RF-001","PM-012","Z-006-RC-01","DG-113","MOD-002","MOD-003","MOD-005"],subtype="six_chuanfu_depth")
    for j, y in enumerate(ys):
        beam("FRAME_WIDTH_Y%02d" % j,(xs[0],y,zframe),(xs[-1],y,zframe),
             plan["section_width"],plan["section_depth"],"FRAME",
             ["PM-011","RF-001","Z-006-RC-01","MOD-003","MOD-004"],subtype="tie_beam")
    # Frame tiers are control members at the three approved half-depth spans.
    for side in (-1,1):
        for k, distance in enumerate(plan["frame_y"][1:], 1):
            y = side * distance
            z = plan["frame_tier_z"][k-1]
            beam("FRAME_TIER_%s_%02d" % ("N" if side < 0 else "S",k),
                 (xs[0],y,z),(xs[-1],y,z),plan["section_width"],plan["section_depth"],"FRAME",
                 ["FR-004","FR-005","FR-006","ROOF-004","ROOF-005","ROOF-006","PM-012","Z-006-RC-01","MOD-002","MOD-003","MOD-004"],
                 boundary="bounded_placeholder",subtype="frame_depth_control")
            for i,x in enumerate(xs):
                roof_at_y = roof_height_at_y(plan,y)
                if roof_at_y <= z:
                    raise ValueError("Frame tier exceeds roof control surface")
                base="FRAME_POST_%s_%02d_X%02d"%("N" if side<0 else "S",k,i)
                beam(base+"_LOW",(x,y,zframe),(x,y,z),plan["section_depth"],plan["section_depth"],"FRAME",
                     ["FR-004","FR-005","FR-006","ROOF-004","ROOF-005","ROOF-006","Z-006-RC-01","MOD-002","MOD-004"],
                     boundary="bounded_placeholder",subtype="frame_tier_support")
                beam(base+"_UP",(x,y,z),(x,y,roof_at_y),plan["section_depth"],plan["section_depth"],"FRAME",
                     ["FR-004","FR-005","FR-006","FR-007","ROOF-007","ROOF-008","ROOF-009","Z-006-RC-01","MOD-002","MOD-004"],
                     boundary="bounded_placeholder",subtype="roof_control_support")
    # Topological bracket arms: aggregate jump lengths are approved, equal subdivisions
    # are purely graphic markers of two steps, not individual historical jump sizes.
    bracket_sets = []
    for i,j,x,y,height in columns:
        normals = []
        if i == 0: normals.append((-1,0))
        if i == len(xs)-1: normals.append((1,0))
        if j == 0: normals.append((0,-1))
        if j == len(ys)-1: normals.append((0,1))
        for axis,(nx,ny) in enumerate(normals):
            bracket_sets.append(("HEAD_X%02d_Y%02d_A%d" % (i,j,axis),x,y,plan["datum_z"]+height,nx,ny,4,True))
    for j in (0,len(ys)-1):
        for i in range(len(xs)-1):
            bracket_sets.append(("INTER_Y%02d_B%02d" % (j,i),(xs[i]+xs[i+1])/2,ys[j],plan["datum_z"]+plan["column_height"],0,-1 if j==0 else 1,2,False))
    for i in (0,len(xs)-1):
        for j in range(len(ys)-1):
            bracket_sets.append(("INTER_X%02d_B%02d" % (i,j),xs[i],(ys[j]+ys[j+1])/2,plan["datum_z"]+plan["column_height"],-1 if i==0 else 1,0,2,False))
    for name,x,y,z,nx,ny,jumps,head in bracket_sets:
        ids = ["DG-001" if head else "DG-002","DG-110","MOD-002","MOD-003","MOD-004","Z-006-RC-01"]
        if head: ids += ["DG-111","DG-112","DG-113"]
        lengths = [plan["jump_a"] / 2] * 2 + ([plan["jump_b"] / 2] * 2 if head else [])
        previous = (x,y,z)
        for k, length in enumerate(lengths,1):
            total = sum(lengths[:k])
            end = (x+nx*total,y+ny*total,z+(plan["lower_ang_rise"]*k/jumps if head else 0))
            beam("BRACKET_%s_J%02d" % (name,k),previous,end,plan["section_width"],plan["section_depth"],"BRACKET",ids,
                 boundary="bounded_placeholder",subtype="head_4_jumps" if head else "intercolumn_2_jumps")
            previous=end
    roof_run = plan["roof_sequence"]
    roof_z = plan["roof_z"]
    roof_xs = [xs[0]-plan["gable"]] + xs + [xs[-1]+plan["gable"]]
    for side in (-1,1):
        for k, (run,z) in enumerate(zip(roof_run,roof_z)):
            if k == len(roof_run)-1 and side==1:
                continue
            y = side * (roof_run[-1]-run)
            beam("ROOF_PURLIN_%s_%02d" % ("N" if side < 0 else "S",k),
                 (roof_xs[0],y,z),(roof_xs[-1],y,z),plan["section_width"],plan["section_depth"],"ROOF",
                 ["FR-007","ROOF-007","ROOF-008","ROOF-009","ROOF-010","ROOF-011","OUT-003","Z-006-RC-01","MOD-002"],
                 subtype="roof_control_purlin")
        for i,x in enumerate(roof_xs):
            for k in range(len(roof_run)-1):
                y0 = side*(roof_run[-1]-roof_run[k])
                y1 = side*(roof_run[-1]-roof_run[k+1])
                beam("ROOF_RAFTER_%s_X%02d_S%02d" % ("N" if side<0 else "S",i,k),
                     (x,y0,roof_z[k]),(x,y1,roof_z[k+1]),plan["section_depth"],plan["section_depth"],"ROOF",
                     ["FR-007","ROOF-007","ROOF-008","ROOF-009","OUT-003","Z-006-RC-01","MOD-002"],
                     boundary="bounded_placeholder",subtype="roof_slope_control")
    for side,x in (("W",roof_xs[0]),("E",roof_xs[-1])):
        for sign in (-1,1):
            beam("GABLE_%s_%s" % (side,"N" if sign<0 else "S"),
                 (x,sign*roof_run[-1],roof_z[0]),(x,0,roof_z[-1]),
                 plan["section_depth"],plan["section_depth"],"GABLE",
                 ["OUT-003","FR-007","ROOF-010","ROOF-011","MOD-002","Z-006-RC-01"],
                 boundary="bounded_placeholder",subtype="gable_control")
    bpy.context.view_layer.update()
    return records,counters


def review_images(plan, directory):
    import bpy
    from mathutils import Vector
    directory.mkdir(parents=True,exist_ok=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.camera = None
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "P2_2_REVIEW_CAMERA"
    camera.data.type = "ORTHO"
    camera.data.clip_end = 1000000  # engineering view range in millimetre coordinates
    scene.camera = camera
    width = plan["width"]+2*plan["gable"]
    depth = 2*plan["roof_sequence"][-1]
    zmid = (plan["datum_z"]+plan["roof_z"][-1])/2
    views = {
        "PLAN": ((0,0,30000),(0,0,0),max(width,depth*scene.render.resolution_x/scene.render.resolution_y)*1.2),
        "ELEVATION": ((30000,0,zmid),(0,0,zmid),max(depth,plan["roof_z"][-1]*scene.render.resolution_x/scene.render.resolution_y)*1.3),
        "AXON": ((22000,-26000,21000),(0,0,zmid),max(width,depth)*1.65),
    }
    paths=[]
    for label,(position,target,scale) in views.items():
        camera.location = position
        direction = Vector(target)-camera.location
        camera.rotation_euler = direction.to_track_quat("-Z","Y").to_euler()
        camera.data.ortho_scale = scale
        path = directory / (PREFIX+"_"+label+".png")
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        paths.append(path)
    camera.hide_render = True
    return paths


def semantic_summary(plan, records, counters, inputs):
    return {"object_names": sorted(r["name"] for r in records),"object_count": len(records),
            "family_counts": dict(sorted(counters.items())),
            "key_dimensions_mm": {"width":plan["width"],"depth":plan["depth"],
                                  "front_bays":[plan["side"],plan["front_center"],plan["side"]],
                                  "depth_bays":[plan["side"],plan["depth_center"],plan["side"]],
                                  "column_height":plan["column_height"],"corner_rise":plan["corner_rise"],"datum_z":plan["datum_z"],
                                  "frame_half_depth_spans":plan["frame_depths"],
                                  "frame_tier_z":plan["frame_tier_z"],
                                  "bracket_two_jump_aggregate":plan["jump_a"],
                                  "bracket_outer_two_jump_aggregate":plan["jump_b"],
                                  "roof_half_run":plan["roof_sequence"][-1],
                                  "roof_control_z":plan["roof_z"],"gable_projection":plan["gable"]},
            "topology": {"front_bay_count":plan["front_count"],"depth_bay_count":plan["depth_count"],
                         "perimeter_columns":plan["front_count"]*2+plan["depth_count"]*2,
                         "interior_columns":0,"head_bracket_directions":16,
                         "intercolumn_bracket_sets":12,"head_jumps":4,"intercolumn_jumps":2,
                         "roof_half_control_intervals":3},
            "geometry_input_snapshot":inputs.snapshot()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=OUTPUT)
    parser.add_argument("--manifest",type=Path,default=MANIFEST)
    parser.add_argument("--summary",type=Path)
    parser.add_argument("--review-dir",type=Path,default=REVIEW)
    parser.add_argument("--no-review",action="store_true")
    parser.add_argument("--params",type=Path,default=PARAMS)
    parser.add_argument("--overrides",type=Path,default=OVERRIDES)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    inputs=FormalInputs(args.params,args.overrides,MATRIX)
    plan=geometry_plan(inputs)
    import bpy
    records,counters=create_model(inputs,plan)
    summary=semantic_summary(plan,records,counters,inputs)
    images=[] if args.no_review else review_images(plan,args.review_dir)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output))
    commit=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    manifest={"task":"T-007","version":"V001","machine_tolerance_mm":MACHINE_TOLERANCE_MM,
              "deterministic_tolerance_mm":DETERMINISTIC_TOLERANCE_MM,
              "inputs":{key:{"path":str(path.resolve()),"sha256":sha(path),
                             "version":(inputs.formal.get("parameter_set_version") if key=="formal_parameter_set" else
                                        inputs.sidecar.get("override_set_version") if key=="approved_overrides" else
                                        inputs.matrix.get("matrix_version") if key=="geometry_dependency_matrix" else
                                        inputs.formal.get("schema_version"))} for key,path in inputs.paths.items()},
              "approval_boundary":{"path":str(DECISIONS.resolve()),"sha256":sha(DECISIONS),
                                   "decision_ids":["D-023","D-024","D-025"]},
              "blender_version":bpy.app.version_string,"blender_python_version":sys.version.split()[0],
              "generation_script":{"path":rel(HERE),"sha256":sha(HERE),"source_commit":commit},
              "used_parameter_ids":sorted(inputs.used),"derived_geometry_rules":inputs.rules,
              "formal_derived_rule_inputs":{ident:{"formula":"identity(formal %s value)" % ident,
                 "source_parameter_ids":[ident],"value":inputs.parameters[ident]["value"],
                 "unit":inputs.parameters[ident]["unit"]} for ident in sorted(inputs.used)
                 if inputs.entries[ident]["geometry_dependency_role"]=="DERIVED_GEOMETRY_RULE"},
              "geometry_input_snapshot":inputs.snapshot(),
              "enabled_reasonable_completion":[{"id":ident,"value":inputs.parameters[ident]["value"],
                   "is_replaceable":inputs.parameters[ident]["is_replaceable"]} for ident in sorted(inputs.used)
                    if inputs.parameters[ident]["classification"]=="REASONABLE_COMPLETION"],
              "approved_override":{"id":"Z-006-RC-01","target_parameter_id":"Z-006",
                 "historical_Z_006":{"classification":"UNKNOWN","value":None,"production_use":"DO_NOT_LOCK",
                                      "dependency":"BLOCKS_P2_2_GEOMETRY"},
                 "classification":"REASONABLE_COMPLETION","approval_decision_id":"D-023",
                 "is_replaceable":True,"formula":inputs.sidecar["overrides"]["Z-006-RC-01"]["formula"],
                 "resolved_value_mm":plan["column_height"]},
              "bounded_unknowns":[{"id":"DG-114","status":"BOUNDED_NON_BLOCKING","use":"none"},
                                  {"id":"HIS-002","status":"METADATA_ONLY_BLOCK","originality_status":"unknown"},
                                  {"item":"45-degree corner joints / mortises / hidden-angle beam","status":"bounded medium-LOD topology only"}],
              "object_families":{family:{"count":count,"name_prefix":family+"_"} for family,count in sorted(counters.items())},
              "objects":records,"semantic_summary":summary,
              "output_blend":{"path":str(args.output.resolve()),"sha256":sha(args.output),"size_bytes":args.output.stat().st_size},
              "review_images":[{"path":str(p.resolve()),"sha256":sha(p)} for p in images]}
    args.manifest.parent.mkdir(parents=True,exist_ok=True)
    args.manifest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if args.summary:
        args.summary.parent.mkdir(parents=True,exist_ok=True)
        args.summary.write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("P2_2_BUILD_OK",json.dumps({"objects":len(records),"families":counters,"blend":str(args.output),
                                      "blend_sha256":manifest["output_blend"]["sha256"]}))


if __name__=="__main__":
    main()
