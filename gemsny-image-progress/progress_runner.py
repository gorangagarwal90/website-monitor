import argparse
import os
import re
import subprocess
import sys
import time

PAGE_RE = re.compile(r"\[(\d+)/(\d+)\]\s+(.+?)\s+page\s+(\d+):\s+(\d+)\s+unique product images")
START_RE = re.compile(r"Auditor v[^—]+— shard (\d+)/(\d+): (\d+) categories")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--shard-index', type=int, required=True)
    p.add_argument('--shard-count', type=int, required=True)
    p.add_argument('--output-dir', required=True)
    args = p.parse_args()

    cmd = [
        sys.executable, 'audit.py',
        '--site', 'https://www.gemsny.com',
        '--sitemap', 'https://www.gemsny.com/sitemap',
        '--min-width', '500', '--min-height', '500',
        '--delay', '2', '--check-original',
        '--shard-index', str(args.shard_index),
        '--shard-count', str(args.shard_count),
        '--max-categories', '0', '--max-pages', '0',
        '--output-dir', args.output_dir,
    ]

    started = time.time()
    cumulative_images = 0
    pages = 0
    category_done = 0
    category_total = 0

    print(f"LIVE PROGRESS START | shard={args.shard_index}/{args.shard_count-1}", flush=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    for raw in proc.stdout:
        line = raw.rstrip()
        print(line, flush=True)

        m = START_RE.search(line)
        if m:
            category_total = int(m.group(3))
            print(f"PROGRESS | shard {args.shard_index} | categories assigned {category_total}", flush=True)
            continue

        m = PAGE_RE.search(line)
        if m:
            category_done = max(category_done, int(m.group(1)) - 1)
            category_total = int(m.group(2))
            category = m.group(3)
            page_no = int(m.group(4))
            images = int(m.group(5))
            cumulative_images += images
            pages += 1
            elapsed = int(time.time() - started)
            pct = round((category_done / category_total) * 100, 1) if category_total else 0
            print(
                f"PROGRESS | shard={args.shard_index} | category={category} | page={page_no} | "
                f"pages_checked={pages} | images_checked={cumulative_images} | "
                f"categories_completed={category_done}/{category_total} | approx_category_progress={pct}% | "
                f"elapsed_seconds={elapsed}",
                flush=True,
            )

    code = proc.wait()
    elapsed = int(time.time() - started)
    print(
        f"LIVE PROGRESS END | shard={args.shard_index} | exit_code={code} | "
        f"pages_checked={pages} | images_checked={cumulative_images} | elapsed_seconds={elapsed}",
        flush=True,
    )
    raise SystemExit(code)


if __name__ == '__main__':
    main()
