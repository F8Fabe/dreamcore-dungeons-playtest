from pathlib import Path
import hashlib, json
root = Path(__file__).resolve().parent
site = root / "site"
for entry in json.loads((root / "manifest.json").read_text()):
    target = (site / entry["path"]).resolve()
    assert target.is_relative_to(site.resolve())
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with target.open("wb") as out:
        for part in entry["parts"]:
            p = (root / "parts" / part).resolve()
            assert p.is_relative_to((root / "parts").resolve())
            data = p.read_bytes()
            out.write(data)
            digest.update(data)
    assert target.stat().st_size == entry["bytes"]
    assert digest.hexdigest() == entry["sha256"]
assert sum(p.stat().st_size for p in site.rglob("*") if p.is_file()) < 1_000_000_000
print("Verified site ready")
