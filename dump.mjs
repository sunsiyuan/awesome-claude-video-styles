// read the one template table from the website (no copies): TEMPLATES, SECTIONS, STYLES → data/site.json
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
const js = readFileSync(new URL('../ultramotion.ai/site/assets/site.js', import.meta.url), 'utf8');
const grab = (name, close) => { const i = js.indexOf(`const ${name} = `) + `const ${name} = `.length, j = js.indexOf(`\n${close};`, i); return (0, eval)(`(${js.slice(i, j + 2)})`); };
mkdirSync(new URL('./data/', import.meta.url), { recursive: true });
writeFileSync(new URL('./data/site.json', import.meta.url), JSON.stringify({ templates: grab('TEMPLATES', ']'), sections: grab('SECTIONS', ']'), styles: grab('STYLES', ']') }, null, 1));
