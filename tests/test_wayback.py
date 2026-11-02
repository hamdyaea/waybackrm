# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from waybackrem import clean_html, plan, apply_changes

class WaybackTests(unittest.TestCase):
    def test_rewrites_wayback_url(self):
        value = '<a href="https://web.archive.org/web/20200101000000/https://example.org/a">Link</a>'
        self.assertEqual(clean_html(value), '<a href="https://example.org/a">Link</a>')
    def test_dry_run_and_backup(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "index.html"
            original = "https://web.archive.org/web/20200101000000/https://example.org"
            path.write_text(original)
            changes = plan(Path(folder))
            self.assertEqual(len(changes), 1)
            self.assertEqual(path.read_text(), original)
            self.assertEqual(apply_changes(changes), 1)
            self.assertEqual(path.read_text(), "https://example.org")
            self.assertEqual((Path(folder) / "index.html.wayback-backup").read_text(), original)
    def test_symlink_not_processed(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "source.html"
            path.write_text("https://web.archive.org/web/20200101000000/https://example.org")
            link = Path(folder) / "link.html"
            link.symlink_to(path)
            self.assertEqual(len(plan(Path(folder))), 1)

if __name__ == "__main__":
    unittest.main()
