const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url'),path=require('path'),assert=require('assert');
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});try{
 const page=await browser.newPage({viewport:{width:1882,height:960}}),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 const unit=process.argv[2]||'5';
 const url=pathToFileURL(path.resolve('index.html')).href+`#/linear-algebra/lecture-${unit}/pages/2`;
 await page.goto(url);await page.waitForFunction(()=>document.getElementById('page-select').value==='2');
 assert(!await page.locator('.site-header').isVisible());assert(!await page.locator('.mode-tabs').isVisible());
 for(const [width,height] of [[1882,960],[1255,640],[1440,900]]){
  await page.setViewportSize({width,height});await page.waitForTimeout(100);
  await page.evaluate(()=>readerJump(2));
  const stream=await page.locator('#reader-stream').boundingBox(),image=await page.locator('#pdf-page-2 img').boundingBox();
  assert(stream.y<85,'header too tall '+stream.y);
  assert(image.y>=stream.y&&image.y+image.height<=stream.y+stream.height,'PDF not fully visible '+JSON.stringify({width,height,image,stream}));
  assert(await page.locator('#pdf-page-2 .page-explanations').isVisible());
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 }
 await page.setViewportSize({width:1882,height:960});await page.evaluate(()=>readerJump(2));
 await page.screenshot({path:'work/reading-focus-desktop.png',fullPage:true});
 await page.evaluate(()=>{document.getElementById('reader-stream').scrollTop+=100});await page.waitForTimeout(100);
 const before=await page.evaluate(()=>({page:document.getElementById('page-select').value,offset:document.getElementById('reader-stream').scrollTop-document.getElementById('pdf-page-'+document.getElementById('page-select').value).offsetTop}));
 await page.getByRole('button',{name:'展開導覽 ▾',exact:true}).click();
 assert(await page.locator('.mode-tabs').isVisible());
 const after=await page.evaluate(()=>({page:document.getElementById('page-select').value,offset:document.getElementById('reader-stream').scrollTop-document.getElementById('pdf-page-'+document.getElementById('page-select').value).offsetTop}));
 assert(before.page===after.page&&Math.abs(before.offset-after.offset)<2,'logical reading position changed');
 await page.reload();await page.waitForSelector('#reader-stream');assert(await page.locator('.mode-tabs').isVisible());
 await page.getByRole('button',{name:'收起上方 ▴',exact:true}).click();
 await page.reload();await page.waitForSelector('#reader-stream');assert(!await page.locator('.mode-tabs').isVisible());
 await page.setViewportSize({width:390,height:844});await page.waitForTimeout(100);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.screenshot({path:'work/reading-focus-mobile.png',fullPage:true});
 await page.getByRole('button',{name:'展開導覽 ▾',exact:true}).click();await page.getByRole('link',{name:'精簡簡報',exact:true}).click();
 assert(await page.locator('.site-header').isVisible());await page.locator('#slide-next').click();await page.waitForFunction(()=>document.getElementById('slide-select').value==='2');
 assert(!errors.length,errors.join('\n'));console.log('PASS: default focus, full PDF visible at 3 desktop sizes, both columns, toggle without losing position, saved preference after reload, mobile, mode switch and slide navigation.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
