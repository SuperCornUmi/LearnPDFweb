const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url'),path=require('path'),fs=require('fs'),assert=require('assert');
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});try{
const p=await browser.newPage({viewport:{width:1882,height:960}}),errors=[],checks=[];
p.on('pageerror',e=>errors.push(String(e)));p.on('requestfailed',r=>errors.push(r.url()+' '+r.failure()?.errorText));
const base=pathToFileURL(path.resolve('index.html')).href,unit='#/assembly-language/chapter-8';
const go=async mode=>{await p.goto(base+unit+'/'+mode);await p.waitForTimeout(150);};
const expand=async()=>{if(await p.locator('#reading-focus-toggle').count()&&!(await p.locator('.mode-tabs').isVisible()))await p.locator('#reading-focus-toggle').click()};
const noOverflow=async tag=>assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+tag);
const waitAt=async n=>p.waitForFunction(n=>{const s=document.getElementById('reader-stream'),t=document.getElementById('pdf-page-'+n);return document.getElementById('page-select').value===String(n)&&Math.abs(s.scrollTop-Math.min(t.offsetTop,s.scrollHeight-s.clientHeight))<3},n);
await p.goto(base);assert((await p.locator('.hero-stats').innerText()).includes('290'));assert(await p.locator('.course-card').count()===2);
await p.getByRole('link',{name:/COMPUTER SYSTEMS/}).click();await p.waitForSelector('.chapter-row');assert(await p.locator('.chapter-row').count()===1);assert(!(await p.locator('.chapter-head').innerText()).includes('CE2005'));await p.screenshot({path:'work/src-20261105-assembly-ch8/website-course.png',fullPage:true});
await p.locator('.chapter-row').click();await p.waitForSelector('#reader-stream');assert(await p.locator('.page-section').count()===51);
assert(await p.locator('#page-select option').count()===51);assert(await p.locator('#pdf-page-4 pre').count()===1);assert(await p.locator('#pdf-page-1 img').getAttribute('src')==='website/assets/assembly-ch8/cover.svg');
for(let i=1;i<=51;i++){
 await p.evaluate(v=>readerJump(v),i);
 await p.waitForFunction(v=>{const im=document.querySelector('#pdf-page-'+v+' img');return im.complete&&im.naturalWidth>0},i);
 assert(await p.locator('#pdf-page-'+i+' .translation').count()===1);
 assert(await p.locator('#pdf-page-'+i+' .explanation-card').count()>=2);
}
checks.push('51 page images loaded, page sections/selector/code blocks present');
await p.evaluate(()=>readerJump(45));await p.waitForTimeout(150);
await p.locator('#reading-focus-toggle').click();await p.waitForTimeout(100);assert(await p.locator('#page-select').inputValue()==='45');await p.locator('#reading-focus-toggle').click();await p.reload();await p.waitForSelector('#reader-stream');assert(!(await p.locator('.mode-tabs').isVisible()));assert(await p.locator('#page-select').inputValue()==='45');
await p.evaluate(()=>readerJump(18));await p.screenshot({path:'work/src-20261105-assembly-ch8/website-reader.png',fullPage:true});
let stream=await p.locator('#reader-stream').evaluate(e=>({s:e.scrollTop,w:scrollY}));
await p.locator('#reader-stream').hover();await p.mouse.wheel(0,600);await p.waitForTimeout(200);
assert(await p.locator('#reader-stream').evaluate(e=>e.scrollTop)>stream.s);assert(await p.evaluate(()=>scrollY)===stream.w);
await p.evaluate(()=>readerJump(20));await p.locator('#directory-toggle').click();
await p.locator('#page-search').fill('Difference');assert(await p.locator('[data-page]:visible').count()>0);await p.locator('#page-search').fill('unfindableZZZZ');assert(await p.locator('#search-empty').isVisible());await p.locator('#page-search').fill('');
await p.locator('#directory-toggle').click();await p.waitForTimeout(100);await p.locator('#page-select').selectOption('51');await waitAt(51);
await p.locator('#reader-stream').focus();await p.keyboard.press('ArrowLeft');await waitAt(50);
await p.evaluate(()=>readerJump(18));
await p.locator('#pdf-page-18 [data-zoom]').click();assert(await p.locator('#image-dialog').isVisible());await p.locator('#image-dialog .close').click();
checks.push('focus preference/reload, page position, independent scroll, TOC search, jump and zoom');
await expand();await p.getByRole('link',{name:'精簡簡報',exact:true}).click();await p.waitForSelector('#slide-select');assert(await p.locator('#slide-select option').count()===16);
await p.locator('#slide-next').scrollIntoViewIfNeeded();let y=await p.locator('#slide-next').evaluate(e=>e.getBoundingClientRect().y),sy=await p.evaluate(()=>scrollY);
for(let i=2;i<=16;i++){await p.locator('#slide-next').click();await p.waitForFunction(v=>document.getElementById('slide-select').value===String(v),i);assert(Math.abs(await p.locator('#slide-next').evaluate(e=>e.getBoundingClientRect().y)-y)<2);assert(await p.evaluate(()=>scrollY)===sy);}
await p.locator('#slide-select').selectOption('3');await p.locator('#main').focus();await p.keyboard.press('ArrowRight');await p.waitForFunction(()=>document.getElementById('slide-select').value==='4');
await p.locator('#fullscreen').click();assert(await p.evaluate(()=>!!document.fullscreenElement));await p.locator('#slide-next').click();assert(await p.locator('#slide-select').inputValue()==='5');await p.evaluate(()=>document.exitFullscreen());
checks.push('16 slides sequential click stable scroll/buttons, keyboard and fullscreen');
await p.getByRole('link',{name:'完整筆記',exact:true}).click();await p.waitForSelector('#notes-body');assert(await p.locator('#notes-body section').count()===51);assert(await p.locator('#notes-body pre').count()>25);
await p.locator('#toggle-md').click();assert((await p.locator('#notes-body pre').innerText()).includes('PDF p. 51'));await p.locator('#toggle-md').click();
const download=await p.locator('.download-bar a[download]').getAttribute('href');assert(fs.existsSync(path.resolve(download)));
await p.emulateMedia({media:'print'});await noOverflow('print');await p.emulateMedia({media:'screen'});
checks.push('continuous notes, fenced code, Markdown toggle, download target and print layout');
await p.getByRole('link',{name:'圖解整理',exact:true}).click();assert((await p.locator('#match-result').innerText()).includes('基本題：2 筆；加分題：5 筆'));
for(let i=1;i<=7;i++)await p.locator('#stack-next').click();assert((await p.locator('#stack-registers').innerText()).includes('00100000h'));assert(await p.locator('#stack-next').isDisabled());
await p.locator('#stack-step').selectOption('4');assert((await p.locator('#stack-rows').innerText()).includes('EBP+8'));
await p.locator('#match-x').fill('');await p.locator('#match-y').fill('');await p.locator('#match-run').click();assert((await p.locator('#match-result').innerText()).includes('基本題：0 筆；加分題：0 筆'));
for(const [x,y,result] of [['-1,2','2,-1','基本題：0 筆；加分題：2 筆'],['1,1','1,2','無重複'],['1','1,2','共同長度'],['2147483648','1','32 位元']]){await p.locator('#match-x').fill(x);await p.locator('#match-y').fill(y);await p.locator('#match-run').click();assert((await p.locator('#match-result').innerText()).includes(result));}
await p.goto(base+unit+'/diagrams/');await p.waitForTimeout(100);await p.screenshot({path:'work/src-20261105-assembly-ch8/website-diagrams.png',fullPage:true});
checks.push('stack 8 stages, sample/empty/negative arrays and validation errors');
await p.getByRole('link',{name:'來源與文獻',exact:true}).click();await p.waitForSelector('.ref-card');assert(await p.locator('.ref-card').count()>=9);
for(const [width,height] of [[1882,960],[1255,640],[390,844],[768,900]]){
 await p.setViewportSize({width,height});
 for(const mode of ['pages/45','slides/12','notes/','diagrams/','references/']){await go(mode);await noOverflow(`${width} ${mode}`);}
 await go('pages/45');if(await p.locator('.mode-tabs').isVisible())await p.locator('#reading-focus-toggle').click();await p.waitForTimeout(100);
 if(width>=1000){const r=await p.locator('#pdf-page-45 img').evaluate(e=>{const r=e.getBoundingClientRect(),s=document.getElementById('reader-stream').getBoundingClientRect();return {h:r.height,available:s.height}});assert(r.h<=r.available+1,JSON.stringify(r));}
 if(width===1255)await p.screenshot({path:'work/src-20261105-assembly-ch8/website-short.png',fullPage:true});
 if(width===390)await p.screenshot({path:'work/src-20261105-assembly-ch8/website-mobile.png',fullPage:true});
}
checks.push('1882x960, 1255x640, 390x844, 768x900 all modes no page overflow; full source image height desktop');
await p.setViewportSize({width:1440,height:900});
for(const [n,count] of [[5,87],[6,152]]){await p.goto(base+`#/linear-algebra/lecture-${n}/pages/18`);await p.waitForTimeout(150);assert(await p.locator('.page-section').count()===count);await p.waitForFunction(()=>{const i=document.querySelector('#pdf-page-18 img');return i.complete&&i.naturalWidth>0});await p.goto(base+`#/linear-algebra/lecture-${n}/diagrams/`);assert(await p.locator('.diagram-card').count()>0);}
checks.push('both existing linear algebra units, original page assets and diagrams preserved');
assert.deepStrictEqual(errors,[]);
fs.writeFileSync('work/src-20261105-assembly-ch8/browser-results.json',JSON.stringify({date:'2026-11-05',checks,errors},null,2));console.log(JSON.stringify({checks,errors},null,2));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
