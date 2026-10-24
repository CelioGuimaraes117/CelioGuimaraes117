#!/usr/bin/env python3
"""Profile repository checks (standard library only).

  python3 scripts/validate_profile.py            # structure, assets, SVG safety, privacy, data schema
  python3 scripts/validate_profile.py --links    # also checks external links over the network

Privacy: the denylist below holds truncated SHA-256 hashes of confidential tokens (client
and private-repository names, non-public e-mails), so the check works without publishing
the very names it protects.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ["README.md", "README.pt-BR.md"]
DENY = set("""
ca75da6440157fbde152a87b 73e6154f5c80baf95e012453 e763d2a097597014d37688bf 84c7497f72a364dbd11636dd
cd8bbe178dfb278ae17ec0d2 ae849dec36ce103cf4a4778f fa822a2a83e4843af71df104 09813a4dd3a2015cbff51aeb
fd1f9e69bcdb990ecd863ba0 fefd803478453a08192966a3 4da787e1cb2fa9ac1aab7af2 023eb7a1a55f23973b5e9eb9
456f45fddc2e725c2948d033 67da1db97f78e350a2b23d19 b0c0200933fecc6a93c2cbdb 6925cb9e108fcfb8378ab10e
776cb326ab0cd5f0a974c1b9 5ef56002e3c48db595323879 88e6b3e27725c438ef790b7b 897d65e31dc0f6df22fdfd2a
deee4fcb39cfe227d9b6ad5c 9db523aa308909163bded93a edc5407dbc7e0632fd7ddaa0 5d19b2623e4cbd826d956674
f6b3bb0784a70bfa33a6cd4f a6889f844f744f2f83bf3d59
""".split())
SVG_FORBIDDEN = re.compile(r"<script|<foreignObject|\son[a-z]+\s*=|javascript:|xlink:href|\shref=|<image|@import|url\(", re.I)
MAX_ASSET_BYTES = 400_000
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def tokens(text: str) -> set[str]:
    words = set(re.findall(r"[a-z0-9][a-z0-9._@+-]*[a-z0-9]", text.lower()))
    parts = {p for w in words for p in re.split(r"[._/-]", w) if p}
    return words | parts


def check_privacy(name: str, text: str) -> None:
    for tok in tokens(text):
        if hashlib.sha256(tok.encode()).hexdigest()[:24] in DENY:
            err(f"{name}: contains a confidential token (hash {hashlib.sha256(tok.encode()).hexdigest()[:8]}…)")


def check_docs() -> list[str]:
    links = []
    for doc in DOCS:
        p = ROOT / doc
        if not p.exists():
            err(f"missing {doc}")
            continue
        text = p.read_text()
        check_privacy(doc, text)
        for tag in re.findall(r"<img\b[^>]*>", text):
            if not re.search(r'\salt="[^"]{3,}"', tag):
                err(f"{doc}: <img> without meaningful alt: {tag[:80]}")
        refs = re.findall(r'(?:src|srcset)="([^"]+)"', text) + re.findall(r"\]\(([^)]+)\)", text)
        for ref in refs:
            if ref.startswith(("http://", "https://", "mailto:")):
                if ref.startswith("http://"):
                    err(f"{doc}: insecure link {ref}")
                links.append(ref)
            elif not (ROOT / ref.split("#")[0]).exists():
                err(f"{doc}: broken relative reference {ref}")
        for dark in re.findall(r'srcset="([^"]+-dark\.svg)"', text):
            if not (ROOT / dark.replace("-dark.svg", "-light.svg")).exists():
                err(f"{doc}: {dark} has no light variant")
    return links


def check_assets() -> None:
    for p in sorted((ROOT / "assets").rglob("*")):
        if p.is_dir():
            continue
        if p.suffix not in {".svg", ".png"}:
            err(f"unexpected asset type: {p.relative_to(ROOT)}")
        if p.stat().st_size > MAX_ASSET_BYTES:
            err(f"asset too large: {p.relative_to(ROOT)}")
        if p.suffix == ".svg":
            s = p.read_text()
            if SVG_FORBIDDEN.search(s):
                err(f"unsafe SVG construct: {p.relative_to(ROOT)}")
            if not re.search(r"<title[^>]*>[^<]{3,}</title>", s):
                err(f"SVG without <title>: {p.relative_to(ROOT)}")
            check_privacy(str(p.relative_to(ROOT)), s)


def check_data() -> None:
    p = ROOT / "data" / "public-metrics.json"
    d = json.loads(p.read_text())
    expected = {"schema", "generated_on", "window", "commits", "monthly", "pull_requests", "languages"}
    if set(d) != expected or d.get("schema") != "cea.public/v1":
        err("data/public-metrics.json: unexpected top-level shape")
    allowed_str = re.compile(r"^(cea\.public/v1|\d{4}-\d{2}(-\d{2})?|[A-Za-z0-9+#. -]{1,24})$")

    def walk(v, path="$"):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x, f"{path}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{path}[{i}]")
        elif isinstance(v, str) and not allowed_str.match(v):
            err(f"data/public-metrics.json: unexpected string at {path}")
        elif isinstance(v, bool) or (isinstance(v, (int, float)) and v < 0):
            err(f"data/public-metrics.json: invalid value at {path}")
    walk(d)
    check_privacy("data/public-metrics.json", p.read_text())


V2_KEYS = {"schema", "generated_on", "collection", "periods", "monthly", "languages", "definitions"}
V2_PERIODS = {"7d", "30d", "12m", "all"}
V2_TEXT = re.compile(r"^[A-Za-z0-9_ ,.;:()+/'-]{1,300}$")      # reviewed prose in definitions/collection


def check_data_v2() -> None:
    """cea.public/v2 (optional until the V2 dashboard is integrated): shape, counts, invariants, privacy."""
    p = ROOT / "data" / "public-metrics-v2.json"
    if not p.exists():
        return
    d = json.loads(p.read_text())
    if set(d) != V2_KEYS or d.get("schema") != "cea.public/v2" or set(d.get("periods", {})) != V2_PERIODS:
        err("data/public-metrics-v2.json: unexpected top-level shape")
        return
    allowed_str = re.compile(r"^(cea\.public/v2|\d{4}-\d{2}(-\d{2})?|[A-Za-z0-9+#. -]{1,24})$")

    def walk(v, path="$"):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x, f"{path}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{path}[{i}]")
        elif isinstance(v, str):
            prose = path.startswith(("$.definitions.", "$.collection."))
            if not (V2_TEXT.match(v) if prose else allowed_str.match(v)):
                err(f"data/public-metrics-v2.json: unexpected string at {path}")
        elif isinstance(v, bool) or (isinstance(v, (int, float)) and v < 0):
            err(f"data/public-metrics-v2.json: invalid value at {path}")
    walk(d)
    for name, per in d["periods"].items():
        s = per["sources"]
        if s["consolidated"] != s["github_only"] + s["azure_devops_only"] + s["both"] \
                or per["git"]["owner_authored_shas"] != s["consolidated"]:
            err(f"data/public-metrics-v2.json: {name} sources do not add up")
        con, g = per["contributions"], per["git"]
        if set(con) != {"official_total", "eligible_mirrored_commits", "calendar_upper_bound", "pending_on_calendar"} \
                or con["calendar_upper_bound"] > con["eligible_mirrored_commits"] \
                or con["pending_on_calendar"] != con["eligible_mirrored_commits"] - con["calendar_upper_bound"]:
            err(f"data/public-metrics-v2.json: {name} contribution figures inconsistent")
        if g["default_branch_shas"] + g["other_live_branch_only_shas"] + g["deleted_branch_recovered_shas"] \
                != g["owner_authored_shas"]:
            err(f"data/public-metrics-v2.json: {name} reachability classes do not partition the population")
    check_privacy("data/public-metrics-v2.json", p.read_text())


def check_links(links: list[str]) -> None:
    for url in sorted(set(links)):
        if url.startswith("mailto:"):
            continue
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 profile-link-check"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
                status = r.status
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:  # network errors are reported, not hidden
            err(f"link unreachable: {url} ({type(e).__name__})")
            continue
        if status in (429, 999):      # LinkedIn and rate limits refuse bots; reported as a warning
            print(f"warning: {url} answered {status} (bot protection), not verifiable automatically")
        elif status >= 400:
            err(f"broken link: {url} ({status})")


def main() -> int:
    links = check_docs()
    check_assets()
    check_data()
    check_data_v2()
    if "--links" in sys.argv:
        check_links(links)
    for e in errors:
        print(f"error: {e}")
    print("profile validation:", "FAILED" if errors else "OK", f"({len(errors)} errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
