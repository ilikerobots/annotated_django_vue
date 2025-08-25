import os, re, yaml, sys

COMMENT_RE = re.compile(r"(?:#|//|<!--)\s*django-vue:\s*(.*?)(?:-->)?$", re.I)
TAG_RE = re.compile(r"([a-z0-9\-_]+)(?:@(\d+))?", re.I)

REPO = os.environ.get("GITHUB_REPOSITORY", "owner/repo")
REF = os.environ.get("GITHUB_SHA") or "main"

ANNOTATION_YML = "../annotations.yml"
SOURCE_ROOT = "../.."

def file_url(path, line):
    # return f"https://github.com/{REPO}/blob/{REF}/{path}#L{line}"
    return f"{path}#L{line}"

def load_catalog():
    with open(ANNOTATION_YML, "r", encoding="utf-8") as fh:
        items = yaml.safe_load(fh)
    # accept either `tag` or `id`
    return {e.get("tag") or e.get("id"): e for e in items}

def scan():
    hits = {}
    for root, _, files in os.walk(SOURCE_ROOT):
        if any(p in root for p in (".git", "node_modules", ".venv", "dist", "build")):
            continue
        for f in files:
            if not f.endswith((".py", ".html", ".js", ".ts", ".vue", ".scss")):
                continue
            path = os.path.join(root, f).lstrip("./")
            try:
                full_path = os.path.join(root, f)
                for i, line in enumerate(open(full_path, encoding="utf-8"), start=1):
                    m = COMMENT_RE.search(line)
                    if not m:
                        continue
                    for raw in m.group(1).split():
                        t = TAG_RE.match(raw)
                        if not t:
                            continue
                        tag, order = t.group(1), int(t.group(2) or 9999)
                        hits.setdefault(tag, []).append((order, path, i))
            except Exception as e:
                print(e)
                pass
    return hits

def render(catalog, hits):
    lines = ["## Annotated Code\n"]

    for tag, meta in catalog.items():
        title = meta.get("title", tag)
        desc = meta.get("description", "")

        lines.append(f"### {title}")
        lines.append("")

        if desc:
            lines.append(desc)
            lines.append("")

        # Add links as bullet points or numbered list if they exist
        tag_hits = sorted(hits.get(tag, []))
        if tag_hits:
            has_order_numbers = any(order != 9999 for order, _, _ in tag_hits)

            if has_order_numbers:
                for order, path, line in tag_hits:
                    lines.append(f"1. [{path}:{line}]({file_url(path, line)})")
            else:
                for order, path, line in tag_hits:
                    lines.append(f"* [{path}:{line}]({file_url(path, line)})")
            lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    catalog = load_catalog()
    hits = scan()
    out = render(catalog, hits)

    if len(sys.argv) > 1:
        output_file = sys.argv[1]
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"Documentation written to {output_file}")
        except Exception as e:
            print(f"Error writing to file {output_file}: {e}")
            sys.exit(1)
    else:
        print(out)