"""Check links to RSD source in the guides and optionally update their version."""

import argparse
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, unquote


DOCS = Path(__file__).resolve().parents[1]
SOURCE_LINK = re.compile(
    r"(?<=\]\()(?P<base>https://github\.com/rsd-devel/rsd/(?P<kind>blob|tree)/)"
    r"(?P<target>[^\s)#?]+)"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="local RSD source repository")
    parser.add_argument("tag", help="target release tag in RSD")
    parser.add_argument("--from-ref", help="also rewrite links from this tag or branch")
    args = parser.parse_args()

    # Read the tagged tree even when the working checkout is on another branch.
    tree = subprocess.run(
        ["git", "-C", args.repo, "ls-tree", "-rtz", "refs/tags/" + args.tag],
        capture_output=True,
    )
    if tree.returncode:
        parser.exit(1, tree.stderr.decode(errors="replace"))
    entries = {}
    for entry in tree.stdout.split(b"\0"):
        if entry:
            header, path = entry.split(b"\t", 1)
            entries[path] = header.split()[1].decode()

    tag = quote(args.tag, safe="/")
    refs = [tag]
    if args.from_ref:
        refs.append(quote(args.from_ref, safe="/"))
        refs.sort(key=len, reverse=True)

    changes = {}
    errors = []
    checked = 0
    pages = [DOCS / "README.md"]
    for language in ("en", "jp"):
        pages.extend(sorted((DOCS / language).rglob("*.md")))
    for page in pages:
        original = page.read_bytes().decode("utf-8")  # Preserve each page's line endings.

        def update(match):
            nonlocal checked
            checked += 1
            for ref in refs:
                if match["target"].startswith(ref + "/"):
                    path = match["target"][len(ref) + 1:]
                    if entries.get(unquote(path).encode()) == match["kind"]:
                        return match["base"] + tag + "/" + path
                    break
            errors.append(f"{page.relative_to(DOCS)}: check ref and path in {match[0]}")
            return match[0]

        updated = SOURCE_LINK.sub(update, original)
        if updated != original:
            changes[page] = updated

    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    for page, updated in changes.items():
        page.write_bytes(updated.encode("utf-8"))
    print(f"{args.tag}: checked {checked} source links, updated {len(changes)} pages")


if __name__ == "__main__":
    main()
