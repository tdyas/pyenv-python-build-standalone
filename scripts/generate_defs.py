# Original license:
# Copyright 2023 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import sys
from pathlib import Path
import textwrap

import github
import requests
from github.GitReleaseAsset import GitReleaseAsset


DEFS_PATH = Path("./share/python-build-standalone")

ASSET_RE =  re.compile(r"cpython-([\d.]+)\+([\d.]+)-([\w\d]+)-([-_\w\d]+)-install_only")


def _github():
    # generate with `gh auth token`
    token = os.environ.get("GITHUB_TOKEN")
    if token is None:
        print(
            "WARNING: No GitHub token configured in GITHUB_TOKEN. Lower rate limits will apply!",
            file=sys.stderr,
        )
    return github.Github(auth=github.Auth.Token(token) if token else None)


def _compute_sha256(url):
    response = requests.get(url, stream=True)
    sha256_hash = hashlib.sha256()

    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def get_scraped_releases() -> frozenset[str]:
    return frozenset(DEFS_PATH.glob("*"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scrape-all-releases", dest="scrape_all_releases", action="store_true")
    parser.add_argument(
        "--scrape-release", metavar="RELEASE", dest="scrape_releases", action="append"
    )
    parser.add_argument("--overwrite-existing-defs", action="store_true")
    options = parser.parse_args()

    print("Starting to scrape GitHub PBS releases.")
    if not DEFS_PATH.exists():
        raise Exception("This helper script must be run from the root of the repository.")

    github = _github()
    pbs_repo = github.get_repo("indygreg/python-build-standalone")

    print("Downloading PBS release metadata.")
    releases = pbs_repo.get_releases()
    print("Downloaded PBS release metadata.")

    asset_map: dict[str, GitReleaseAsset] = {}
    sha256_map: dict[str, str] = {}
    existing_scraped_releases = get_scraped_releases()

    for release in releases.reversed:
        tag_name = release.tag_name

        if (
            options.scrape_all_releases
            or (options.scrape_releases and tag_name in options.scrape_releases)
            or (not options.scrape_releases and tag_name not in existing_scraped_releases)
        ):
            print(f"Scraping release tag `{tag_name}`.")
            assets = release.get_assets()
            for asset in assets:
                # NB: From https://python-build-standalone.readthedocs.io/en/latest/running.html#obtaining-distributions
                # > Casual users will likely want to use the install_only archive,
                # > as most users do not need the build artifacts present in the full archive.
                is_applicable = any(
                    f"{machine}-{osname}-install_only" in asset.name
                    for machine, osname in itertools.product(
                        ["aarch64", "x86_64"], ["apple-darwin", "unknown-linux-gnu"]
                    )
                )
                if not is_applicable:
                    continue

                is_checksum = asset.name.endswith(".sha256")
                if is_checksum:
                    shasum = requests.get(asset.browser_download_url).text.strip()
                    sha256_map[asset.name.removesuffix(".sha256")] = shasum
                else:
                    asset_map[asset.name] = asset

    print("Finished scraping releases.")

    for asset in asset_map.values():
        matched_versions = ASSET_RE.match(asset.name)
        if not matched_versions:
            print(f"Warning: Could not parse asset `{asset.name}`.")
            continue

        python_version, pbs_release_tag, machine, os = matched_versions.groups()

        sha256sum = sha256_map.get(asset.name)
        if not sha256sum:
            sha256sum = _compute_sha256(asset.browser_download_url)

        def_path = DEFS_PATH / python_version / pbs_release_tag / f"{machine}-{os}.def"
        def_path.parent.mkdir(parents=True, exist_ok=True)
        if not def_path.exists() or options.overwrite_existing_defs:
            def_path.write_text(textwrap.dedent(
                f"""\
                {asset.browser_download_url}
                {sha256sum}
                """
            ))


if __name__ == "__main__":
    main()
