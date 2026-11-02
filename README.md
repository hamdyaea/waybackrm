# WaybackRM — Local HTML URL Cleanup

**Developer:** Hamdy Abou El Anein  
**Contact:** info@daylightlinux.ch  
**License:** GPL v3 (see LICENSE).

A modern Python 3 tool that removes Wayback Machine URL wrappers from local HTML files. Unlike the original implementation, it **does not modify files by default** and does not reserialize entire HTML documents. The `--apply` mode creates a `.wayback-backup` file before replacing each modified HTML file.

```sh
python3 waybackrem.py ./site
python3 waybackrem.py ./site --apply
python3 -m unittest discover -s tests -v
```

Only matching URL wrappers are rewritten. The program deliberately does not attempt to remove entire Wayback toolbar DOM structures, which could alter unrelated page content. Existing backups prevent repeated overwrites; symlinks are skipped. Review the preview before applying changes.

Original code: [old branch](https://github.com/hamdyaea/waybackrm/tree/old).
