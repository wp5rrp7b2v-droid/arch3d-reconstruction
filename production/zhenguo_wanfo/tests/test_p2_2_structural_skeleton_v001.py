#!/usr/bin/env python3
"""Meaningful input-boundary and replacement tests for T-007."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts/generate_p2_2_structural_skeleton_v001.py"
sys.path.insert(0,str(SCRIPT.parent))
from generate_p2_2_structural_skeleton_v001 import FormalInputs, geometry_plan, PARAMS, OVERRIDES, MACHINE_TOLERANCE_MM


class StructuralSkeletonTests(unittest.TestCase):
    def test_formal_geometry_and_historical_boundary(self):
        inputs=FormalInputs()
        plan=geometry_plan(inputs)
        self.assertEqual(len(inputs.parameters),85)
        self.assertEqual(inputs.parameters["Z-006"]["value"],None)
        self.assertEqual(inputs.parameters["Z-006"]["classification"],"UNKNOWN")
        self.assertEqual(inputs.entries["Z-006"]["unknown_dependency_status"],"BLOCKS_P2_2_GEOMETRY")
        self.assertAlmostEqual(plan["column_height"],3534.3,places=6)
        self.assertEqual(plan["front_count"],3)
        self.assertEqual(plan["depth_count"],3)
        self.assertEqual(len(plan["xs"])*len(plan["ys"])-4,12)
        self.assertAlmostEqual(plan["roof_sequence"][-1]-plan["depth"]/2,plan["jump_a"]+plan["jump_b"],delta=MACHINE_TOLERANCE_MM)

    def test_reference_and_unknown_cannot_enter_geometry(self):
        inputs=FormalInputs()
        for ident in ("PM-003","DG-114","HIS-002","Z-006"):
            with self.assertRaises(ValueError):
                inputs.value(ident)

    def test_modular_mutation_recomputes_replaceable_candidate(self):
        original=geometry_plan(FormalInputs())
        formal=json.loads(PARAMS.read_text(encoding="utf-8"))
        sidecar=json.loads(OVERRIDES.read_text(encoding="utf-8"))
        formal["parameters"]["MOD-005"]["value"]+=1
        formal["parameters"]["MOD-006"]["value"]=formal["parameters"]["MOD-005"]["value"]*formal["parameters"]["MOD-002"]["value"]
        sidecar["overrides"]["Z-006-RC-01"]["current_resolved_value"]=round(sidecar["overrides"]["Z-006-RC-01"]["multiplier"]*formal["parameters"]["MOD-006"]["value"],4)
        with tempfile.TemporaryDirectory(prefix="T007_mutation_") as folder:
            params=Path(folder)/"params.json"; overrides=Path(folder)/"overrides.json"
            params.write_text(json.dumps(formal,ensure_ascii=False),encoding="utf-8")
            overrides.write_text(json.dumps(sidecar,ensure_ascii=False),encoding="utf-8")
            changed=geometry_plan(FormalInputs(params,overrides))
        self.assertGreater(changed["column_height"],original["column_height"])
        self.assertAlmostEqual(changed["column_height"]-original["column_height"],11*original["fen"],delta=MACHINE_TOLERANCE_MM)
        self.assertIsNone(formal["parameters"]["Z-006"]["value"])

    def test_other_reasonable_completions_remain_parameter_driven(self):
        original=geometry_plan(FormalInputs())
        formal=json.loads(PARAMS.read_text(encoding="utf-8"))
        formal["parameters"]["Z-005"]["value"]+=formal["parameters"]["MOD-002"]["value"]
        formal["parameters"]["Z-007"]["value"]="Z = 15.3; abstract column-foot design plane"
        formal["parameters"]["ROOF-009"]["value"]+=1
        formal["parameters"]["ROOF-010"]["value"]+=1
        formal["parameters"]["ROOF-011"]["value"]+=formal["parameters"]["MOD-002"]["value"]
        with tempfile.TemporaryDirectory(prefix="T007_other_rc_") as folder:
            params=Path(folder)/"params.json"
            params.write_text(json.dumps(formal,ensure_ascii=False),encoding="utf-8")
            changed=geometry_plan(FormalInputs(params,OVERRIDES))
        self.assertAlmostEqual(changed["corner_rise"]-original["corner_rise"],original["fen"],delta=MACHINE_TOLERANCE_MM)
        self.assertAlmostEqual(changed["datum_z"]-original["datum_z"],original["fen"],delta=MACHINE_TOLERANCE_MM)
        self.assertAlmostEqual(changed["roof_rise"]-original["roof_rise"],original["fen"],delta=MACHINE_TOLERANCE_MM)
        self.assertAlmostEqual(changed["roof_z"][-1]-original["roof_z"][-1],2*original["fen"],delta=MACHINE_TOLERANCE_MM)

    def test_no_formal_historical_dimension_literal(self):
        source=SCRIPT.read_text(encoding="utf-8")
        numeric=[n.value for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Constant) and type(n.value) in (int,float)]
        forbidden={306,321.3,3534.3,459,11475,10710,1759.5,1836,1407.6,231,92,48,47,21}
        self.assertFalse(forbidden.intersection(numeric),"Formal dimensions embedded as script numeric literals")


if __name__=="__main__":unittest.main()
