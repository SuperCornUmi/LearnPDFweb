const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url'),path=require('path'),assert=require('assert'),fs=require('fs');
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});try{
const p=await browser.newPage({viewport:{width:1882,height:960}}),errors=[];p.on('pageerror',e=>errors.push(String(e)));p.on('requestfailed',r=>{if(r.url().startsWith('file:'))errors.push(r.url()+' '+r.failure()?.errorText)});
const base=pathToFileURL(path.resolve('index.html')).href;
await p.goto(base);assert((await p.locator('.hero-stats').innerText()).includes('239'));
await p.getByRole('link',{name:/MATHEMATICS/}).click();assert(await p.locator('.chapter-row').count()===2);
await p.screenshot({path:'work/two-unit-chapters.png',fullPage:true});
const expand=async()=>{if(await p.locator('#reading-focus-toggle').count()&&!(await p.locator('.mode-tabs').isVisible()))await p.locator('#reading-focus-toggle').click()};
for(const [n,count,slides] of [[5,87,15],[6,152,20]]){
 await p.goto(base+`#/linear-algebra/lecture-${n}/pages/1`);await p.waitForSelector('#reader-stream');
 assert(await p.locator('.page-section').count()===count);assert(await p.locator('#page-select option').count()===count);
 assert((await p.locator('#pdf-page-1 img').getAttribute('src')).includes(`lecture${n}/cover.svg`));
 for(let i=1;i<=count;i++){
  await p.evaluate(v=>readerJump(v),i);
  await p.waitForFunction(v=>{const im=document.querySelector('#pdf-page-'+v+' img');return im.complete&&im.naturalWidth>0},i);
  assert((await p.locator('#pdf-page-'+i+' .translation p').innerText()).length>1);
 }
 await p.evaluate(()=>readerJump(19));await p.waitForTimeout(60);await expand();
 await p.getByRole('link',{name:'精簡簡報',exact:true}).click();assert(await p.locator('#slide-select option').count()===slides);
 await p.locator('#slide-next').scrollIntoViewIfNeeded();let y=await p.locator('#slide-next').evaluate(e=>e.getBoundingClientRect().y);
 for(let i=2;i<=slides;i++){
  await p.locator('#slide-next').click();await p.waitForFunction(v=>document.getElementById('slide-select').value===String(v),i);
  assert(Math.abs(await p.locator('#slide-next').evaluate(e=>e.getBoundingClientRect().y)-y)<2);
 }
 await p.locator('#slide-select').selectOption('3');await p.locator('#fullscreen').click();await p.locator('#slide-next').click();assert(await p.evaluate(()=>!!document.fullscreenElement));await p.evaluate(()=>document.exitFullscreen());
 await p.getByRole('link',{name:'完整筆記',exact:true}).click();assert(await p.locator('#notes-body section').count()===count);await p.locator('#toggle-md').click();assert((await p.locator('#notes-body pre').innerText()).includes('PDF p. '+count));await p.locator('#toggle-md').click();
 await p.getByRole('link',{name:'圖解整理',exact:true}).click();
 if(n===6){for(const mode of ['rotate','scale','reflect','translate']){await p.locator('#shape-mode').selectOption(mode);assert((await p.locator('#shape-points').innerText()).includes('輸出頂點'));}await p.screenshot({path:'work/lecture6-diagrams.png',fullPage:true});}
 else{await p.locator('#collinear').click();assert((await p.locator('#vector-status').innerText()).includes('相依'));}
 await p.getByRole('link',{name:'來源與文獻',exact:true}).click();assert((await p.locator('.ref-card a').first().getAttribute('href')).includes('Lecture_'+n+'.pdf'));
}
// Direct unit-to-unit navigation must replace content even if both routes use pages.
await p.goto(base+'#/linear-algebra/lecture-5/pages/60');await p.waitForFunction(()=>document.getElementById('page-select').value==='60');
await p.evaluate(()=>location.hash='#/linear-algebra/lecture-6/pages/144');await p.waitForFunction(()=>document.querySelectorAll('.page-section').length===152&&document.getElementById('page-select').value==='144');
assert((await p.locator('#pdf-page-144 .translation').innerText()).includes('S⁻¹BS'));
await p.evaluate(()=>readerJump(18));await p.screenshot({path:'work/lecture6-reader.png',fullPage:true});
await p.goto(base+'#/linear-algebra');const saved=await p.locator('.chapter-row').evaluateAll(es=>es.map(e=>e.getAttribute('href')));assert(saved[0].endsWith('/60')&&saved[1].endsWith('/18'),saved.join(','));
for(const w of [390,768,1440]){
 await p.setViewportSize({width:w,height:900});
 for(const mode of ['pages/110','slides/19','notes/','diagrams/','references/']){
  await p.goto(base+'#/linear-algebra/lecture-6/'+mode);await p.waitForTimeout(40);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+w+' '+mode);
  if(w===390&&mode==='pages/110')await p.screenshot({path:'work/lecture6-mobile.png',fullPage:true});
 }
}
assert(!errors.length,errors.join('\n'));fs.writeFileSync('work/two-unit-results.json',JSON.stringify({units:2,totalPages:239,slides:[15,20],allPageImages:true,perUnitProgress:true,screenWidths:[390,768,1440,1882],errors},null,2));
console.log('PASS: 2 units, all 239 pages/images, 15+20 slides and stable next buttons/fullscreen, per-unit saved progress, unit-to-unit routes, notes/Markdown, both diagram modes, 4 viewport widths, no JS/resource errors.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
