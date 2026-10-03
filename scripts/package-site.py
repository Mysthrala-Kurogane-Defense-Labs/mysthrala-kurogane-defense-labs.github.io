#!/usr/bin/env python3
"""Export and validate the public site for GitHub Pages or Cloudflare.

Requires Python 3.11+. Only the selected generated directory is recreated;
source files and the other hosting target are left intact.
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit


SOURCE = Path(__file__).resolve().parents[1]
OUTPUT_NAMES = {"github": "_site", "cloudflare": "_site-cloudflare"}
PUBLIC_FILES = (
    "index.html", "404.html", "aviso-legal.html", "privacidad.html",
    "cookies.html", "accesibilidad.html", "CNAME", "robots.txt",
    "sitemap.xml", "llms.txt", "index.md", "security.txt", ".nojekyll",
)
PUBLIC_DIRECTORIES = ("assets", ".well-known")
CLOUDFLARE_FILES = ("_headers", "_redirects")


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            require(attrs["id"] not in self.ids, f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        self.links.extend(attrs[key] for key in ("href", "src") if key in attrs)


def validate(output):
    require((output / "CNAME").read_text().strip() == "mkdl.jp", "CNAME must contain mkdl.jp")
    require(
        (output / "security.txt").read_bytes() == (output / ".well-known/security.txt").read_bytes(),
        "The two security.txt files must be identical",
    )
    require(not (output / ".git").exists(), "Git metadata must not be published")
    require(not (output / ".github").exists(), "GitHub workflows must not be published")
    require(not any(path.is_symlink() for path in output.rglob("*")), "Symlinks must not be published")

    pages = {}
    for path in output.glob("*.html"):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
    for source, page in pages.items():
        for link in page.links:
            target = urlsplit(link)
            if target.scheme or target.netloc:
                continue
            path = unquote(target.path)
            destination = (
                output / path.lstrip("/") if path.startswith("/")
                else source.parent / path if path else source
            ).resolve()
            label = f"{source.name}: {link}"
            require(destination.is_relative_to(output), f"Link escapes the public directory: {label}")
            if destination.is_dir():
                destination /= "index.html"
            require(destination.is_file(), f"Missing local link target: {label}")
            if target.fragment and destination in pages:
                require(unquote(target.fragment) in pages[destination].ids, f"Missing HTML fragment: {label}")
    return len(pages)


def package(target):
    # CLI choices and this fixed map prevent arbitrary output paths.
    output = SOURCE / OUTPUT_NAMES[target]
    inputs = [SOURCE / name for name in PUBLIC_FILES]
    for name in PUBLIC_DIRECTORIES:
        directory = SOURCE / name
        require(directory.is_dir() and not directory.is_symlink(), f"Invalid public directory: {name}")
        inputs.extend(directory.rglob("*"))
    if target == "cloudflare":
        hosting_directory = SOURCE / "cloudflare"
        require(hosting_directory.is_dir() and not hosting_directory.is_symlink(), "Invalid cloudflare directory")
        inputs.extend(SOURCE / "cloudflare" / name for name in CLOUDFLARE_FILES)
    for path in inputs:
        require(path.exists() and not path.is_symlink(), f"Missing file or forbidden symlink: {path}")

    require(not output.is_symlink(), f"Refusing to replace a symlink: {output}")
    if output.exists():
        require(output.is_dir(), f"Output path is not a directory: {output}")
        shutil.rmtree(output)
    output.mkdir()
    for name in PUBLIC_FILES:
        shutil.copy2(SOURCE / name, output / name)
    for name in PUBLIC_DIRECTORIES:
        shutil.copytree(SOURCE / name, output / name)
    if target == "cloudflare":
        for name in CLOUDFLARE_FILES:
            shutil.copy2(SOURCE / "cloudflare" / name, output / name)

    page_count = validate(output)
    public_assets = [
        path for path in output.rglob("*")
        if path.is_file() and path.name not in CLOUDFLARE_FILES
    ]
    print(f"Packaged {len(public_assets)} public files for {target} into {output}")
    print(f"Validated local links and fragments in {page_count} HTML pages")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=OUTPUT_NAMES, default="github")
    package(parser.parse_args().target)
