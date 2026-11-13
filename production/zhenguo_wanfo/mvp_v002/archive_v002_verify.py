#!/usr/bin/env python3
"""Read-only archival audit of the already-built Wanfo Whole Hall MVP V002.
Do NOT rebuild / alter any model, source Master or approved snapshot.
Only produce a candidate archive verification record in mvp_v002/.
"""
import hashlib
import json
import os
import pathlib
import struct
from datetime import datetime, timezone

ROOT = pathlib.Path.cwd()
BASE = ROOT / "production/zhenguo_wanfo/mvp_v002"
OUTPUT = BASE / "V002_CANDIDATE_ARCHIVE_VERIFIED.json"
SHA_APPROVED_63 = "fbcc8f4e025da9325fa5bf0d7b76f7c6267e796650eb19e651f0f27a58f70802"
REQUIRED = {
  "proof": [
    "WANFO_PROOF_V002.blend", "WANFO_PROOF_V002.glb",
    "WANFO_PROOF_AXON.png", "WANFO_PROOF_EXTERIOR.png",
    "BUILD_REPORT.json", "BLEND_REOPEN_CHECK.json", "GLB_REOPEN_CHECK.json"
  ],
  "full": [
    "WANFO_FULL_V002.blend", "WANFO_FULL_V002.glb",
    "WANFO_FULL_AXON.png", "WANFO_FULL_EXTERIOR.png",
    "WANFO_FULL_INTERIOR.png", "WANFO_FULL_ROOF.png",
    "WANFO_FULL_FRONT_ELEVATION.png", "WANFO_FULL_SIDE_ELEVATION.png",
    "BUILD_REPORT.json", "BLEND_REOPEN_CHECK.json", "GLB_REOPEN_CHECK.json"
  ]
}
EXPECTED_COUNTS = {"proof": (76, 63, 13), "full": (473, 63, 410)}

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()

def check_binary_header(path):
    with path.open("rb") as f:
        h=f.read(12)
    if path.suffix == ".blend":
        assert (h.startswith(b"BLENDER") or h.startswith(bytes([0x28,0xB5,0x2F,0xFD]))), f"BLEND_HEADER_BAD: {path}"
    elif path.suffix == ".glb":
        assert h[0:4] == b"glTF", f"GLB_HEADER_BAD: {path}"
        assert struct.unpack("<I",h[4:8])[0] == 2, f"GLB_VERSION_BAD: {path}"
        assert struct.unpack("<I",h[8:12])[0] == path.stat().st_size, f"GLB_LENGTH_BAD: {path}"
    elif path.suffix == ".png":
        assert h.startswith(b"\x89PNG\r\n\x1a\n"), f"PNG_HEADER_BAD: {path}"

def check_stage(stage):
    folder=BASE / stage
    report=json.loads((folder/"BUILD_REPORT.json").read_text(encoding="utf-8"))
    blend=json.loads((folder/"BLEND_REOPEN_CHECK.json").read_text(encoding="utf-8"))
    glb=json.loads((folder/"GLB_REOPEN_CHECK.json").read_text(encoding="utf-8"))
    total, approved, temporary = EXPECTED_COUNTS[stage]
    assert report["stage"]==stage
    assert report["approved_geometry_modified"] is False
    assert report["source_sha256"] == SHA_APPROVED_63
    assert report["source_count"]==approved
    assert report["component_counts"]=={"mesh_objects":total,"temporary_meshes":temporary}
    assert report["column_count"]==12
    assert report["candidate_design_dimensions_mm"]=={"width":11475,"depth":10710}
    assert report["roof_seam_check"]["status"]=="PASS"
    assert report["roof_seam_check"]["unintended_open_internal_seams"]==0
    assert report["roof_seam_check"]["eave_boundary_edges"]==80
    assert abs(report["datum"]["column_foot_z_mm"])<=0.001
    assert report["visual_design_controls"]["temporary_override"] is True
    assert report["visual_proxy_policy"]["formal_assets_untouched"] is True
    assert (blend["status"],glb["status"])==("PASS","PASS")
    assert (blend["source_meshes"], blend["temporary_meshes"])==(approved,temporary)
    assert (glb["approved_mesh_count"],glb["temporary_mesh_count"])==(approved,temporary)
    assert glb["mesh_count"]==total
    inventory={}
    for name in REQUIRED[stage]:
        p=folder/name
        assert p.is_file(),f"FILE_MISSING {p}"
        assert p.stat().st_size>100
        check_binary_header(p)
        inventory[str(p.relative_to(ROOT))]={"bytes":p.stat().st_size,"sha256":digest(p)}
    for format in ("blend","glb"):
        p=folder/f"WANFO_{stage.upper()}_V002.{format}"
        assert report["hashes"][format] == inventory[str(p.relative_to(ROOT))]["sha256"], f"HASH_MISMATCH {p}"
    for image in report["deliverables"]["review_images"]:
        assert image in inventory, f"REVIEW_IMAGE_UNARCHIVED {image}"
    return {
      "status":"PASS",
      "technical_roundtrip_report":"PASS (checked independent BLEND/GLB reopen records)",
      "approved_source_geometry_hash":SHA_APPROVED_63,
      "full_mesh_count":total,
      "approved_source_meshes":approved,
      "temporary_meshes":temporary,
      "roof_topology_check":"PASS, NOT historic structural certification",
      "files":inventory
    }

def main():
    assert os.environ.get("GITHUB_REF_NAME","") == "feature/wanfo-whole-hall-mvp-v002-20261110", "WRONG_BRANCH"
    stages={name:check_stage(name) for name in ("proof","full")}
    script=BASE/"wanfo_mvp_blender_v002.py"
    assert script.is_file()
    manifest={
      "artifact_id":"WANFO_WHOLE_HALL_MVP_V002_CANDIDATE_ARCHIVE",
      "archive_verified_at_utc":datetime.now(timezone.utc).isoformat(),
      "status":"CANDIDATE_ARCHIVED_TECHNICAL_PASS_VISUAL_UNAPPROVED",
      "approval":{"product_owner_visual_approved":False,
                  "approved_master_registry_updated":False,
                  "main_merge_authorized":False,
                  "main_merged":False},
      "source":{"github_repository":"wp5rrp7b2v-droid/arch3d-reconstruction",
                "branch":"feature/wanfo-whole-hall-mvp-v002-20261110",
                "pre_archive_checkout_sha":os.environ.get("GITHUB_SHA"),
                "draft_pr":91,"technical_generation_run":42754853528,
                "builder_script":str(script.relative_to(ROOT)),
                "builder_sha256":digest(script)},
      "scope":"WHOLE_HALL_MVP_VISUAL_CANDIDATE_NOT_HISTORIC_RECONSTRUCTION_APPROVAL",
      "stages":stages,
      "validation_limits":[
          "Review images exist and have PNG headers, but no source A1 silhouette overlay passed",
          "Model reopens and object count pass; visible bearing contacts, load and joinery NOT proved",
          "V002 candidate eave and ridge heights are temporary visual controls, not promoted measurements",
          "No replacements or changes to approved Master assets, approved East/West snapshots",
          "Existing PR #92 focused connection failure is separate and remains FAIL"
      ]
    }
    OUTPUT.write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("V002_ARCHIVE_VERIFICATION_PASS",len(stages["full"]["files"]),len(stages["proof"]["files"]))
    print("V002_CURRENT_NOT_APPROVED")
    print("V002_ARCHIVE_JSON",OUTPUT)

if __name__=="__main__":
    main()
