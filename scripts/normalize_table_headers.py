#!/usr/bin/env python3
"""
Normalize Markdown table headers across `content/posts/*.md`.

Behavior:
- Scans all markdown files under content/posts for Markdown tables.
- Detects header rows (a row with pipes) followed by a separator row (--- with pipes).
- Chooses the most common header row (by exact text of columns) as the canonical header.
- Rewrites tables whose column count matches the canonical header to use the canonical header and a normalized separator row.

This is conservative: tables with different column counts are left unchanged and reported so you can review manually.

Usage:
  python scripts/normalize_table_headers.py

Creates a small report on stdout and edits files in-place. Run with a git working tree so you can review and commit.
"""

import os
import re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
POSTS_DIR = os.path.join(ROOT, 'content', 'posts')

def find_tables_in_lines(lines):
    """Yield tuples (start_idx, header_idx, sep_idx, end_idx)
    where header_idx is the index of header line, sep_idx is the separator, start_idx first table line, end_idx exclusive."""
    i = 0
    n = len(lines)
    while i < n-1:
        line = lines[i]
        nxt = lines[i+1] if i+1<n else ''
        # header candidate: contains '|' and at least one alnum
        if '|' in line and re.search(r'[A-Za-z0-9]', line):
            # separator candidate: line of pipes, colons, dashes, spaces
            if re.match(r'^[\s|:>-]*[-:|\s]+$', nxt):
                # table found; find end
                start = i
                header = i
                sep = i+1
                j = i+2
                while j < n and ('|' in lines[j] or lines[j].strip()=='' or re.match(r'^\s*[:\-\|]+\s*$', lines[j])):
                    # stop when blank line followed by non-table
                    if lines[j].strip()=='' and (j+1>=n or '|' not in lines[j+1]):
                        break
                    j += 1
                end = j
                yield (start, header, sep, end)
                i = end
                continue
        i += 1

def split_cols(line):
    # remove outer pipes then split
    t = line.strip()
    if t.startswith('|') and t.endswith('|'):
        t = t[1:-1]
    cols = [c.strip() for c in t.split('|')]
    return cols

def make_header_line(cols):
    return '| ' + ' | '.join(cols) + ' |\n'

def make_sep_line(cols):
    # make a simple '---' separator for each column, centered
    return '| ' + ' | '.join(['---' for _ in cols]) + ' |\n'

def main():
    if not os.path.isdir(POSTS_DIR):
        print('No posts directory:', POSTS_DIR)
        return 1

    headers_counter = Counter()
    tables_found = []  # list of (path, header_cols, start, header_idx, sep_idx, end)

    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.lower().endswith('.md'):
            continue
        path = os.path.join(POSTS_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for start, header_idx, sep_idx, end in find_tables_in_lines(lines):
            header_line = lines[header_idx]
            cols = split_cols(header_line)
            headers_counter[tuple(cols)] += 1
            tables_found.append((path, cols, start, header_idx, sep_idx, end))

    if not headers_counter:
        print('No Markdown tables found in', POSTS_DIR)
        return 0

    # pick the most common header (by columns tuple)
    canonical_cols, cnt = headers_counter.most_common(1)[0]
    canonical_cols = list(canonical_cols)
    print('Canonical header chosen (occurrences={}):'.format(cnt))
    print(' | '.join(canonical_cols))

    # apply changes where column counts match canonical
    modified = defaultdict(list)  # path -> list of (old_header_line, new_header_line)

    for path, cols, start, header_idx, sep_idx, end in tables_found:
        if len(cols) != len(canonical_cols):
            # skip mismatched column counts
            continue
        # rewrite the header and sep
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        old_header = lines[header_idx]
        old_sep = lines[sep_idx]
        new_header = make_header_line(canonical_cols)
        new_sep = make_sep_line(canonical_cols)
        if old_header != new_header or old_sep != new_sep:
            lines[header_idx] = new_header
            lines[sep_idx] = new_sep
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            modified[path].append((old_header.rstrip('\n'), new_header.rstrip('\n')))

    # report
    if modified:
        print('\nModified tables:')
        for p, changes in modified.items():
            print(' -', os.path.relpath(p, ROOT))
            for old, new in changes:
                print('    ', 'OLD:', old)
                print('    ', 'NEW:', new)
    else:
        print('\nNo tables needed normalization (either none matched column count).')

    # list skipped tables (different column count)
    skipped = [ (p, cols) for (p, cols, *_ ) in tables_found if len(cols) != len(canonical_cols) ]
    if skipped:
        print('\nSkipped tables with different column counts:')
        for p, cols in skipped:
            print(' -', os.path.relpath(p, ROOT), 'columns=', len(cols))

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
