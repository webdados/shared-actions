import os
import re
import json
from datetime import datetime, timezone

slug          = os.environ['GNCLJ_SLUG']
version       = os.environ['GNCLJ_VERSION']
plugin_id_raw = os.environ['GNCLJ_ID']
plugin_name   = os.environ['GNCLJ_NAME']
homepage      = os.environ['GNCLJ_HOMEPAGE']
link          = os.environ['GNCLJ_LINK']
changelog_f   = os.environ['GNCLJ_CHANGELOG_FILE']
plugin_f      = os.environ['GNCLJ_PLUGIN_FILE']
output_f      = os.environ['GNCLJ_OUTPUT_FILE']

# Parse plugin header for requires, tested, requires_php
requires = tested = requires_php = ''
with open(plugin_f, 'r', encoding='utf-8') as fh:
    for line in fh:
        if not requires:
            m = re.match(r'\s*\*\s*Requires at least:\s*(.+)', line)
            if m:
                requires = m.group(1).strip()
        if not tested:
            m = re.match(r'\s*\*\s*Tested up to:\s*(.+)', line)
            if m:
                tested = m.group(1).strip()
        if not requires_php:
            m = re.match(r'\s*\*\s*Requires PHP:\s*(.+)', line)
            if m:
                requires_php = m.group(1).strip()

# Read raw changelog
with open(changelog_f, 'r', encoding='utf-8') as fh:
    changelog_raw = fh.read()

# Type mapping - keys are lower-cased [TAG] values from changelog entries
TYPE_MAP = {
    'new':      'added',
    'fix':      'fixed',
    'dev':      'dev',
    'tweak':    'improved',
    'security': 'security',
    'added':    'added',
    'fixed':    'fixed',
    'improved': 'improved',
}

# Parse changelog: #### version headings and - [TYPE] item lines
entries = []
current_version = None
current_items = []

for line in changelog_raw.splitlines():
    heading = re.match(r'^(?:####\s+|=\s+)(.+?)(?:\s*=)?$', line)
    if heading:
        if current_version is not None:
            entries.append({'version': current_version, 'items': current_items})
        current_version = heading.group(1).strip()
        current_items = []
        continue
    item_m = re.match(r'^[-*]\s+\[([^\]]+)\]\s*(.*)', line)
    if item_m and current_version is not None:
        tag = item_m.group(1).strip()
        content_text = item_m.group(2).strip()
        item_type = TYPE_MAP.get(tag.lower(), 'improved')
        current_items.append({'content': content_text, 'type': item_type})
    else:
        plain_m = re.match(r'^[-*]\s+(.*)', line)
        if plain_m and current_version is not None:
            content_text = plain_m.group(1).strip()
            if content_text:
                current_items.append({'content': content_text, 'type': 'improved'})

if current_version is not None:
    entries.append({'version': current_version, 'items': current_items})

# Build the JSON payload
last_updated = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
first_id = int(plugin_id_raw.split()[0])

data = {
    'id':            first_id,
    'slug':          slug,
    'name':          plugin_name,
    'type':          'plugin',
    'version':       version,
    'tested':        tested,
    'requires':      requires,
    'requires_php':  requires_php,
    'homepage':      homepage,
    'last_updated':  last_updated,
    'link':          link,
    'changelog_raw': changelog_raw,
    'changelog':     entries,
}

with open(output_f, 'w', encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False, indent=4)

print('Generated', output_f)
