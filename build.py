"""Build README.md / README.zh.md and previews/ from the website's template table.
    node dump.mjs && python3 build.py
data/site.json comes from ../ultramotion.ai/site/assets/site.js (dump.mjs) — the one table; nothing is typed here twice.
Previews: a 3-second GIF per template, cut from the sample's card video on media.ultramotion.ai, made once (delete one to remake it).
"""
import json, os, subprocess, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(f'{H}/data/site.json'))
T = {t['id']: t for t in D['templates']}
SITE = 'https://ultramotion.ai'
UTM = 'utm_source=github&utm_medium=readme&utm_campaign=awesome-claude-video-styles'
NOPROXY = {k: v for k, v in os.environ.items() if k.lower() not in ('https_proxy', 'http_proxy', 'all_proxy')}

def preview(t):
    out = f'{H}/previews/{t["id"]}.gif'
    if os.path.exists(out): return True
    key, _, ratio, *rest = t['clips'][0]; t0 = max(0, (rest[0] if rest and isinstance(rest[0], (int, float)) else 1) - .5)
    src = f'/tmp/awesome-src/{key}.mp4'; os.makedirs(os.path.dirname(src), exist_ok=True); os.makedirs(f'{H}/previews', exist_ok=True)
    if not os.path.exists(src):
        r = subprocess.run(['curl', '-sfL', '-o', src, f'https://media.ultramotion.ai/card/{key}.mp4'], env=NOPROXY)
        if r.returncode: r = subprocess.run(['curl', '-sfL', '-o', src, f'https://media.ultramotion.ai/{key}.mp4'], env=NOPROXY)
        if r.returncode: print('no video for', t['id']); return False
    w = 200 if ratio == '9:16' else 320
    vf = f'fps=8,scale={w}:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4'
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t0), '-t', '3', '-i', src, '-vf', vf, '-loop', '0', out])
    return r.returncode == 0

def cell(t, lang):
    url = f'{SITE}/templates/{t["id"]}/' + ('' if lang == 'en' else '?lang=zh') + ('&' if lang != 'en' else '?') + UTM
    name, use = t['name'][lang], t['use'][lang]
    img = f'<a href="{url}"><img src="previews/{t["id"]}.gif" width="{200 if t["clips"][0][2] == "9:16" else 260}" alt="{name}"></a><br>' if os.path.exists(f'{H}/previews/{t["id"]}.gif') else ''
    by = next((c[4]['by'] for c in t['clips'] if len(c) > 4 and isinstance(c[4], dict) and c[4].get('by')), None)
    credit = (f'<br><sub>{"sample by" if lang == "en" else "样片作者"} {by}</sub>' if by else '')
    return f'<td valign="top" width="33%">{img}<a href="{url}"><b>{name}</b></a><br><sub>{use}</sub>{credit}</td>'

def table(ids, lang):
    rows = [ids[i:i + 3] for i in range(0, len(ids), 3)]
    return '<table>\n' + '\n'.join('<tr>' + ''.join(cell(T[i], lang) for i in r) + '</tr>' for r in rows) + '\n</table>\n'

for t in D['templates']: preview(t)
on_home = [i for s in D['sections'] for i in s['ids'] if i in T]
rest = [t['id'] for t in D['templates'] if t['id'] not in set(on_home)]
groups = [(s['name'], s['line'], [i for i in s['ids'] if i in T]) for s in D['sections']] + ([({'en': 'More', 'zh': '更多'}, {'en': 'Everything else on the site.', 'zh': '网站上的其他模板。'}, rest)] if rest else [])
anchor = lambda s: s.lower().replace('&', '').replace(' ', '-').replace('--', '-')

TEXT = {
 'en': dict(title='Awesome Claude Video Styles', other='[English](README.md) · [中文](README.zh.md)',
    intro=f'**{len(T)} video styles** you can make with Claude (or any coding agent) — launch films, explainers, title sequences, memes, music videos — each with a sample and a long prompt you can copy. Named after the look they match: Linear-style launches, Kurzgesagt-style explainers, Star Wars-style crawls, Windows XP error memes.',
    how=f'Click any style for its sample and the prompt. Paste the prompt into Claude Code (or Codex, Cursor…) with your own content; optional: `npx skills add sunsiyuan/ultramotion` for the renderer and sound. All styles: **[ultramotion.ai/templates]({SITE}/templates/?{UTM})**.',
    contents='Contents', also='Also: [Awesome Claude 3D Videos](https://github.com/sunsiyuan/awesome-claude-3d-videos) — 500+ 3D scenes, worlds and games made by Claude, from the original posts.',
    contrib='## Contributing\n\nMade a video in one of these styles, or know a style people keep copying that is missing? Open an issue or a pull request with the link.\n',
    lic='## License\n\n[CC BY 4.0](LICENSE). Samples credited where they are not ours.\n'),
 'zh': dict(title='Awesome Claude Video Styles', other='[English](README.md) · [中文](README.zh.md)',
    intro=f'**{len(T)} 种视频风格**，用 Claude（或任何会写代码的 agent）就能做——发布片、讲解、片头、梗、歌词视频——每种都有样片和可以直接复制的长提示词。按它像谁起名：Linear 式发布片、Kurzgesagt 式科普、星球大战式开场字幕、Windows XP 报错梗。',
    how=f'点任意一个风格看样片和提示词。把提示词连同你自己的内容贴进 Claude Code（或 Codex、Cursor……）就行；想要渲染和配乐工具可以先 `npx skills add sunsiyuan/ultramotion`。全部风格：**[ultramotion.ai/templates]({SITE}/templates/?lang=zh&{UTM})**。',
    contents='目录', also='另见：[Awesome Claude 3D Videos](https://github.com/sunsiyuan/awesome-claude-3d-videos)——Claude 做的 500+ 个 3D 场景、世界和游戏，都链到原帖。',
    contrib='## 参与\n\n用这些风格做了视频，或者知道一种大家都在模仿、这里还没有的风格？开个 issue 或 PR 附上链接。\n',
    lic='## 许可\n\n[CC BY 4.0](LICENSE)。不是我们做的样片都标了作者。\n'),
}
for lang, fn in (('en', 'README.md'), ('zh', 'README.zh.md')):
    x = TEXT[lang]
    md = [f'# {x["title"]} [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)\n', x['other'] + '\n', x['intro'] + '\n', x['how'] + '\n',
          f'## {x["contents"]}\n', '\n'.join(f'- [{n[lang]}](#{anchor(n["en"])}) ({len(ids)})' for n, _, ids in groups) + '\n']
    for n, line, ids in groups:
        md += [f'<a id="{anchor(n["en"])}"></a>\n## {n[lang]}\n', line[lang] + '\n', table(ids, lang)]
    md += [x['also'] + '\n', x['contrib'], x['lic']]
    open(f'{H}/{fn}', 'w').write('\n'.join(md))
print(len(T), 'styles,', len(os.listdir(f'{H}/previews')), 'previews')
