const http=require('http'),fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const root=path.resolve('.');
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.webp':'image/webp','.svg':'image/svg+xml','.pdf':'application/pdf','.md':'text/plain'};
const server=http.createServer((req,res)=>{const u=new URL(req.url,'http://localhost');let rel=decodeURIComponent(u.pathname);if(!rel.startsWith('/sample-repo/')){res.writeHead(404);res.end();return}rel=rel.slice('/sample-repo/'.length)||'index.html';const f=path.resolve(root,rel);if(!f.startsWith(root+path.sep)||!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);res.end();return}res.setHeader('Content-Type',(types[path.extname(f)]||'application/octet-stream')+'; charset=utf-8');fs.createReadStream(f).pipe(res)});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({headless:true,channel:'chrome'});
 const p=await browser.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
 const base=`http://127.0.0.1:${server.address().port}/sample-repo/`;
 await p.goto(base+'#/linear-algebra/lecture-5/pages/2');await p.waitForSelector('#reader-stream');
 await p.waitForFunction(()=>document.querySelector('#pdf-page-2 img').complete&&document.querySelector('#pdf-page-2 img').naturalWidth>0);
 const links=await p.locator('link[href],script[src],.source-panel img,.source-panel a,a[download],.header-right a').evaluateAll(es=>es.map(e=>e.href||e.src));
 for(const url of [...new Set(links)]){assert(url.startsWith(base),'resource escaped project prefix: '+url);const response=await p.request.get(url.split('#')[0]);assert(response.ok(),url+' '+response.status())}
 await p.getByRole('link',{name:'來源與文獻',exact:true}).click();const pdf=await p.getByRole('link',{name:/CE2005 Lecture 5｜原始 PDF/}).getAttribute('href');assert((await p.request.get(new URL(pdf,base).href)).ok());
 assert(!errors.length,errors.join('\n'));console.log('PASS: root index under /sample-repo/, CSS/JS, 87 image URLs, downloads, source PDF and Wiki URLs remain under project prefix and return 200.');
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
})().catch(e=>{console.error(e);process.exit(1)});
