# Public metadata only. GH_TOKEN is supplied to gh by GitHub Actions, never written here.
import json, subprocess
from pathlib import Path
raw=json.loads(subprocess.check_output(['gh','api','repos/largetomatoes/wenjian-software/releases?per_page=30']))
keys=('tag_name','html_url','body','published_at','draft','prerelease')
releases=[]
for value in raw:
    if value['draft'] or value['prerelease']: continue
    item={key:value.get(key) for key in keys}
    item['assets']=[{key:asset.get(key) for key in ('name','browser_download_url','state')} for asset in value['assets']]
    releases.append(item)
if not releases: raise SystemExit('No public release; refusing to replace the working index')
Path('updates').mkdir(exist_ok=True)
Path('updates/releases.json').write_text(json.dumps({'schema':1,'generatedAt':max(r['published_at'] for r in releases),'releases':releases},ensure_ascii=False,indent=2)+'\n')
print('Indexed',len(releases),'public releases; newest:',releases[0]['tag_name'])
