const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
const path=require('path');
const fs=require('fs');
const assert=require('assert');
(async()=>{
const browser=await chromium.launch({headless:true,channel:'chrome'});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
const url=pathToFileURL(path.resolve('website/index.html')).href;
await page.goto(url);await page.screenshot({path:'work/website-home.png',fullPage:true});
await page.getByRole('link',{name:/MATHEMATICS/}).click();
assert((await page.title()).includes('線性代數'));
await page.getByRole('link',{name:/LECTURE 5/}).click();
await page.waitForSelector('.explanation-card');
assert(await page.locator('.explanation-card').count()===3);
await page.locator('#page-select').selectOption('19');
await page.waitForFunction(()=>location.hash.endsWith('/19'));
assert((await page.locator('.translation').innerText()).includes('勘誤'));
await page.screenshot({path:'work/website-reader.png',fullPage:true});
await page.locator('#zoom-page').click();assert(await page.locator('dialog').evaluate(e=>e.open));await page.getByRole('button',{name:'關閉 ×'}).click();
await page.locator('#page-search').fill('Wronskian');
assert((await page.locator('.page-list a:visible').count())<87);
await page.locator('#page-search').fill('');
for(let i=1;i<=87;i++){
 await page.goto(url+'#/linear-algebra/lecture-5/pages/'+i);
 await page.waitForSelector('.source-panel img');
 assert(await page.locator('.source-panel img').evaluate(im=>im.complete&&im.naturalWidth>0),'image '+i);
 assert((await page.locator('.page-counter').innerText()).includes(String(i)));
 const lengths=await page.locator('.explanation-card p').evaluateAll(es=>es.map(e=>e.textContent.length));
 assert(lengths.length===3&&lengths.every(x=>x>=2),'content '+i);
}
await page.getByRole('link',{name:'精簡簡報',exact:true}).click();
for(let i=1;i<=15;i++){
 await page.locator('#slide-select').selectOption(String(i));
 await page.waitForFunction(n=>document.querySelector('#slide-select').value===String(n),i);
 assert((await page.locator('.speaker p').first().innerText()).length>20);
}
await page.locator('#slide-select').selectOption('9');
await page.screenshot({path:'work/website-slides.png',fullPage:true});
await page.locator('#fullscreen').click();assert(await page.evaluate(()=>!!document.fullscreenElement));
await page.locator('#slide-next').click();assert(await page.evaluate(()=>!!document.fullscreenElement));
await page.evaluate(()=>document.exitFullscreen());
await page.getByRole('link',{name:'完整筆記',exact:true}).click();assert(await page.locator('#notes-body section').count()===87);
await page.getByRole('button',{name:'查看 Markdown 原文'}).click();assert((await page.locator('#notes-body pre').innerText()).includes('PDF p. 87'));
await page.getByRole('button',{name:'回到閱讀版'}).click();await page.getByRole('link',{name:'基底與維度',exact:true}).click();assert(!page.url().includes('note-'));
await page.getByRole('link',{name:'圖解整理',exact:true}).click();await page.getByRole('button',{name:'設為共線：0°'}).click();assert((await page.locator('#vector-status').innerText()).includes('相依'));
await page.locator('#angle').fill('40');assert((await page.locator('#vector-status').innerText()).includes('獨立'));
await page.screenshot({path:'work/website-diagrams.png',fullPage:true});
await page.setViewportSize({width:390,height:844});await page.goto(url);await page.screenshot({path:'work/website-mobile-home.png',fullPage:true});
for(const mode of ['pages/38','slides/9','notes/','diagrams/','references/']){
 await page.goto(url+'#/linear-algebra/lecture-5/'+mode);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile overflow '+mode);
 if(mode==='pages/38')await page.screenshot({path:'work/website-mobile-reader.png',fullPage:true});
}
assert(!errors.length,errors.join('\n'));
fs.writeFileSync('work/website-checks.json',JSON.stringify({pages:87,slides:15,offline:true,mobileWidth:390,errors},null,2));
console.log('PASS: offline navigation, all 87 pages/images, 15 slides, fullscreen continuation, notes modes, search, zoom, vector interaction, mobile overflow, no browser errors.');
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
