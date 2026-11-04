from pathlib import Path
p=Path(__file__).resolve().parents[1]/'website/app.js'
s=p.read_text(encoding='utf-8')
a='<section class="explanation-card supplement"><h3>03 ／ 教學補充・提醒</h3>${para(p.supplement)}</section>'
b='${p.supplement?`<section class="explanation-card supplement"><h3>03 ／ 教學補充・提醒</h3>${para(p.supplement)}</section>`:\'\'}'
assert a in s;s=s.replace(a,b)
a='<h3>教學補充／提醒</h3>${para(p.supplement)}'
b='${p.supplement?`<h3>教學補充／提醒</h3>${para(p.supplement)}`:\'\'}'
assert a in s;s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
