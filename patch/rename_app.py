"""Give the rebuilt APK a distinct application id and launcher label.

Changing only the APK filename does NOT create a separate Android app.  The
manifest package/application id must be different from the old remote app.
"""
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])

# New application id: deliberately different from the original Remote app.
# Keep Java class packages unchanged; Android can run explicit activity class
# names from a different manifest/application package.
NEW_PACKAGE = "com.remote11.mirroring"

manifest = d / "AndroidManifest.xml"
s = manifest.read_text(encoding="utf-8")

# apktool decodes the manifest package as a normal XML attribute.
m = re.search(r'(<manifest\b[^>]*\bpackage=")([^"]+)(")', s)
if not m:
    raise SystemExit("manifest package attribute not found")
old_package = m.group(2)
if old_package == NEW_PACKAGE:
    pass
else:
    s = s[:m.start(2)] + NEW_PACKAGE + s[m.end(2):]
    manifest.write_text(s, encoding="utf-8")

# Launcher label.
strings = d / "res" / "values" / "strings.xml"
if strings.exists():
    ss = strings.read_text(encoding="utf-8")
    ss = re.sub(
        r'(<string\s+name="app_name">).*?(</string>)',
        r'\1MyRemote Mirror\2',
        ss,
        count=1,
    )
    strings.write_text(ss, encoding="utf-8")

print(f"Application id: {old_package} -> {NEW_PACKAGE}")
print("Launcher label: MyRemote Mirror")
