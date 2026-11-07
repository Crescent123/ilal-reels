const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const D=JSON.parse(fs.readFileSync('data.json'));const mode=process.argv[2];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/anim.html');await p.evaluate(d=>{D=d},D);await p.waitForTimeout(400);
if(mode==='test'){for(const t of JSON.parse(process.argv[3]||'[1]')){await p.evaluate(t=>render(t),t);await p.screenshot({path:`test_${t}.png`});}}
else{fs.mkdirSync('frames',{recursive:true});const fps=30,n=Math.ceil(D.dur*fps);
for(let i=0;i<n;i++){await p.evaluate(t=>render(t),i/fps);await p.screenshot({path:`frames/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:88});}}
await b.close();})();
