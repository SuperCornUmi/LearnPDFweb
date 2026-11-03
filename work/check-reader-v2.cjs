const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');const path=require('path'),assert=require('assert'),fs=require('fs');
(async()=>{
const browser=await chromium.launch({headless:true,channel:'chrome'});
const page=await browser.newPage({viewport:{width:1905,height:910}}),errors=[];
page.on('pageerror',e=>errors.push(String(e)));
const url=pathToFileURL(path.resolve('index.html')).href,B='#/linear-algebra/lecture-5';
await page.goto(url+B+'/pages/1');
await page.waitForSelector('#reader-stream');
assert(await page.locator('.page-section').count()===87);
assert((await page.locator('#pdf-page-1 img').getAttribute('src')).endsWith('cover.svg'));
assert(!await page.locator('#page-directory').isVisible());
await page.screenshot({path:'work/reader-v2-cover.png',fullPage:true});
await page.evaluate(()=>readerJump(2));
await page.waitForFunction(()=>document.getElementById('page-select').value==='2');
const dims=await page.locator('#pdf-page-2 .source-panel').boundingBox();
assert(dims.width>1905/2,'PDF should exceed half desktop screen width: '+dims.width);
await page.screenshot({path:'work/reader-v2-desktop.png',fullPage:true});
const outer=await page.evaluate(()=>scrollY);
await page.locator('#reader-stream').hover();await page.mouse.wheel(0,1000);
await page.waitForTimeout(400);
assert(await page.evaluate(()=>scrollY)===outer,'wheel should stay inside reader');
assert(+(await page.locator('#page-select').inputValue())>2,'wheel should advance current page');
await page.getByRole('button',{name:'☰ 目錄／搜尋',exact:true}).click();
assert(await page.locator('#page-directory').isVisible());
await page.locator('#page-search').fill('Wronskian');
assert(await page.locator('[data-page]:visible').count()<87);
await page.getByRole('button',{name:'收起目錄',exact:true}).click();
for(const n of [19,38,60,86,87]){
 await page.locator('#page-select').selectOption(String(n));
 await page.waitForFunction(v=>document.getElementById('page-select').value===String(v)&&Math.abs(document.getElementById('reader-stream').scrollTop-document.getElementById('pdf-page-'+v).offsetTop)<3,n);
 assert(await page.locator('#pdf-page-'+n+' img').evaluate(im=>im.complete&&im.naturalWidth>0),'image '+n);
}
await page.getByRole('link',{name:'精簡簡報',exact:true}).click();
await page.locator('#slide-next').scrollIntoViewIfNeeded();
const before=await page.locator('#slide-next').boundingBox(),y=await page.evaluate(()=>scrollY);
for(let i=2;i<=15;i++){
 await page.getByRole('button',{name:'下一張簡報',exact:true}).click();
 await page.waitForFunction(v=>document.getElementById('slide-select').value===String(v),i);
 const after=await page.locator('#slide-next').boundingBox();
 assert(Math.abs(after.y-before.y)<2,'next button moves vertically');
 assert(Math.abs((await page.evaluate(()=>scrollY))-y)<2,'slide scroll resets');
}
await page.locator('#slide-select').selectOption('4');
await page.getByRole('button',{name:'全螢幕 ⛶',exact:true}).click();
await page.locator('#slide-next').click();
assert(await page.evaluate(()=>!!document.fullscreenElement));
await page.evaluate(()=>document.exitFullscreen());
await page.goto(url+B+'/pages/38');
await page.setViewportSize({width:390,height:844});
await page.waitForTimeout(300);
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
await page.screenshot({path:'work/reader-v2-mobile.png',fullPage:true});
await page.locator('#page-select').selectOption('60');
await page.waitForFunction(()=>Math.abs(document.getElementById('reader-stream').scrollTop-document.getElementById('pdf-page-60').offsetTop)<3);
for(const w of [768,1440]){
 await page.setViewportSize({width:w,height:1000});await page.waitForTimeout(100);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+w);
}
assert(!errors.length,errors.join('\n'));
fs.writeFileSync('work/reader-v2-results.json',JSON.stringify({pages:87,cover:'custom SVG',desktopPdfWidth:dims.width,wheel:'inner only',slides:'15 stable next clicks',mobile:'390/768/1440 widths',errors},null,2));
console.log('PASS: custom cover, 87 continuous pages, PDF >50% screen, collapsible search, isolated wheel, page jump incl last page, 15 stable slide clicks, fullscreen, mobile, no JS errors.');
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
