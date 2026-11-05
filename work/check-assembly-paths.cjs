const http=require('http'),fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('C:/Users/miu99/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=process.cwd(),prefix='/sample-repo/';
const server=http.createServer((req,res)=>{let name;try{name=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400).end();return}if(!name.startsWith(prefix)){res.writeHead(404).end();return}const target=path.resolve(root,name.slice(prefix.length)||'index.html');if(!target.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(target,(e,data)=>{if(e){res.writeHead(404).end();return}const ext=path.extname(target),mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.md':'text/plain; charset=utf-8','.pdf':'application/pdf'};res.writeHead(200,{'Content-Type':mime[ext]||'application/octet-stream'});res.end(data)})});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const browser=await chromium.launch({headless:true,channel:'chrome'});try{
 const p=await browser.newPage({viewport:{width:1440,height:900}}),errors=[];p.on('pageerror',e=>errors.push(String(e)));
 const base=`http://127.0.0.1:${server.address().port}${prefix}index.html`;
 await p.goto(base+'#/assembly-language/chapter-8/pages/1');await p.waitForSelector('#reader-stream');
 const local=await p.evaluate(async()=>{const d=window.LESSONS['assembly-language/chapter-8'],m=d.meta,urls=[...document.querySelectorAll('script[src],link[rel=stylesheet]')].map(x=>x.getAttribute('src')||x.getAttribute('href'));urls.push(m.pdf,m.sourceWiki,m.downloads+'-notes.md',m.downloads+'-slides.md',m.downloads+'-speaker-notes.md',...d.pages.map(p=>m.assetBase+(p.page===1?'cover.svg':String(p.page).padStart(3,'0')+'.webp')));return Promise.all([...new Set(urls)].map(async u=>({url:u,status:(await fetch(u)).status})));});
 assert(local.every(x=>x.status===200),JSON.stringify(local.filter(x=>x.status!==200)));assert(await p.locator('.page-section').count()===51);
 // A fresh route resets the interactive sample for a clean visual record.
 await p.goto(base+'#/');await p.waitForSelector('.hero');await p.goto(base+'#/assembly-language/chapter-8/diagrams/');await p.waitForSelector('#match-result');
 assert((await p.locator('#match-result').innerText()).includes('基本題：2 筆；加分題：5 筆'));await p.evaluate(()=>scrollTo(0,0));
 await p.screenshot({path:'work/src-20261105-assembly-ch8/website-diagrams.png',fullPage:true});
 await p.goto(base+'#/assembly-language/chapter-8/pages/1');await p.waitForSelector('#reader-stream');await p.screenshot({path:'work/src-20261105-assembly-ch8/website-cover.png',fullPage:true});
 assert.deepStrictEqual(errors,[]);fs.writeFileSync('work/src-20261105-assembly-ch8/path-results.json',JSON.stringify({mount:prefix,local_resources:local.length,all_status_200:true,errors},null,2));console.log(JSON.stringify({mount:prefix,local_resources:local.length,all_status_200:true,errors}));
 }finally{await browser.close();await new Promise(r=>server.close(r))}
})().catch(e=>{console.error(e);server.close();process.exitCode=1});
