import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from compare_alpha import apply_cutoff, compare


class AlphaComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source.png"
        image = Image.new("RGBA", (4, 1))
        image.putdata([(10, 20, 30, alpha) for alpha in (0, 40, 96, 255)])
        image.save(self.source)
        self.metadata = {"asset_id": "test-asset", "alpha_editing": {
            "available": True, "processing": "binary_alpha_v1", "current_cutoff": 96,
            "source_layout": "image", "source_url": "https://example.com/?secret=example",
        }}

    def test_cutoff_restores_outline_preserves_rgb_and_uses_inclusive_boundary(self):
        with Image.open(self.source) as source:
            high = apply_cutoff(source, 96)
            low = apply_cutoff(source, 40)
            self.assertEqual(list(high.getchannel("A").getdata()), [0, 0, 255, 255])
            self.assertEqual(list(low.getchannel("A").getdata()), [0, 255, 255, 255])
            self.assertEqual(list(low.convert("RGB").getdata()), list(source.convert("RGB").getdata()))
            self.assertEqual(list(source.getchannel("A").getdata()), [0, 40, 96, 255])

    def test_report_and_candidates_keep_source_canvas_but_crop_preview(self):
        self.metadata["alpha_editing"]["preview_crop"] = {"left": 1, "top": 0, "right": 4, "bottom": 1}
        out = self.root / "output"
        report = compare(self.metadata, self.source, out, cutoffs=[40, 96], current_path=self.source)
        self.assertEqual(report["soft_alpha_pixels"], 2)
        self.assertTrue((out / "comparison.png").is_file())
        with Image.open(out / "cutoff-40.png") as image:
            self.assertEqual(image.size, (4, 1))
        text = (out / "comparison.json").read_text()
        self.assertNotIn("secret", text)
        self.assertNotIn(str(self.source), text)
        self.assertEqual(json.loads(text)["candidates"][0]["opaque_pixels"], 3)

    def test_animation_matches_layout_and_retains_every_frame(self):
        self.metadata["alpha_editing"].update(source_layout="horizontal_spritesheet", frame_count=2, frame_width=2, frame_height=1)
        compare(self.metadata, self.source, self.root / "frames", cutoffs=[40])
        with Image.open(self.root / "frames/cutoff-40.png") as image:
            self.assertEqual(list(image.getchannel("A").getdata()), [0, 255, 255, 255])
        self.metadata["alpha_editing"]["frame_width"] = 3
        with self.assertRaisesRegex(ValueError, "dimensions"):
            compare(self.metadata, self.source, self.root / "bad")

    def test_binary_source_warns_and_zero_matches_server_semantics(self):
        Image.new("RGBA", (1, 1), (10, 20, 30, 0)).save(self.source)
        report = compare(self.metadata, self.source, self.root / "binary", cutoffs=[0, 96])
        self.assertEqual(len(report["warnings"]), 2)
        self.assertEqual(report["candidates"][0]["opaque_pixels"], 1)
        self.assertEqual(report["candidates"][1]["opaque_pixels"], 0)

    def test_rejects_missing_source_other_algorithms_invalid_cutoffs_and_overwrites(self):
        for field, value in [("available", False), ("processing", "tileset_color_tolerance_v1")]:
            original = self.metadata["alpha_editing"][field]
            self.metadata["alpha_editing"][field] = value
            with self.assertRaises(ValueError):
                compare(self.metadata, self.source, self.root / "out")
            self.metadata["alpha_editing"][field] = original
        with self.assertRaises(ValueError):
            compare(self.metadata, self.source, self.root / "out", cutoffs=[256])
        compare(self.metadata, self.source, self.root / "out")
        with self.assertRaisesRegex(ValueError, "empty output"):
            compare(self.metadata, self.source, self.root / "out")


if __name__ == "__main__":
    unittest.main()
