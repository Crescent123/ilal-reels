// node render.js <epdir> test '[t1,t2]'  |  node render.js <epdir> full
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const E=path.resolve(process.argv[2]);const mode=process.argv[3];const D=JSON.parse(fs.readFileSync(E+'/data.json'));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/anim.html');await p.evaluate(d=>{D=d},D);await p.waitForTimeout(500);
if(mode==='test'){for(const t of JSON.parse(process.argv[4]||'[1]')){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${E}/test_${t}.png`});}}
else{fs.mkdirSync(E+'/frames',{recursive:true});const fps=30,n=Math.ceil(D.dur*fps);
for(let i=0;i<n;i++){await p.evaluate(t=>render(t),i/fps);await p.screenshot({path:`${E}/frames/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:88});}}
await b.close();})();
