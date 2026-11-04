const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url'),path=require('path'),assert=require('assert'),fs=require('fs');
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});try{
 const p=await browser.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
 const base=pathToFileURL(path.resolve('index.html')).href;
 for(const n of [5,6]){
  await p.goto(base+`#/linear-algebra/lecture-${n}/pages/1`);await p.waitForSelector('#reader-stream');
  assert.equal(await p.locator('.page-section').count(),n===5?87:152);
  assert.equal(await p.locator('.supplement').count(),n===5?9:11);
  for(const [width,height] of [[1882,960],[1255,640],[768,900],[390,844]]){
   await p.setViewportSize({width,height});await p.waitForTimeout(80);
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow');
   const bad=await p.locator('.explanation-card').evaluateAll(es=>es.filter(e=>e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1).map(e=>e.closest('.page-section').id));
   assert(!bad.length,`${n}/${width} clipped text: ${bad}`);
   const target=n===5?53:144;await p.evaluate(v=>readerJump(v),target);await p.waitForTimeout(80);
   if(width===1882||width===390)await p.screenshot({path:`work/revised-lecture-${n}-${width}.png`,fullPage:true});
  }
  // No supplement content means no placeholder heading or blank card.
  assert.equal(await p.locator('#pdf-page-2 .explanation-card').count(),2);
  if(!await p.locator('.mode-tabs').isVisible())await p.locator('#reading-focus-toggle').click();await p.getByRole('link',{name:'完整筆記',exact:true}).click();
  assert.equal(await p.locator('#notes-body h3').filter({hasText:'教學補充／提醒'}).count(),n===5?9:11);
  assert.equal(await p.locator('#notes-body section').count(),n===5?87:152);
  await p.locator('#toggle-md').click();assert((await p.locator('#notes-body pre').innerText()).includes('補充'));
 }
 assert(!errors.length,errors.join('\n'));
 fs.writeFileSync('work/content-revision-layout-results.json',JSON.stringify({pages:239,supplements:[9,11],widths:[1882,1255,768,390],noClippedText:true,errors},null,2));
 console.log('PASS: all 239 revised pages at 4 viewport sizes, no clipped text or horizontal overflow; optional supplements and notes match; no JavaScript errors.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
