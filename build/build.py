import json,random,re,sys
sys.path.insert(0,'.')
from items_new import PR1,PR2,CESC,ENT
def setd(L,qstart,d):
  for k,x in enumerate(L):
    if x[2].startswith(qstart): L[k]=(x[0],d)+x[2:];return
  raise Exception(qstart)
setd(PR1,"Which title names","A");setd(PR2,"In 40 respondents","A");setd(CESC,"The Panay Bukidnon","A")
CESC[:]=[(("Self, Solidarity & Participation" if x[0] in("Self, Community & Marginalized Groups","Solidarity & Participation") else x[0]),)+x[1:] for x in CESC]
src=open('../index.html').read()
GM=json.loads(re.search(r'const ITEMS=(\[.*?\]);\n',src).group(1))
def mk(L,seed):
  rnd=random.Random(seed);topics=[];[topics.append(x[0]) for x in L if x[0] not in topics]
  L=sorted(L,key=lambda x:(topics.index(x[0]),"EAD".index(x[1])))
  pos=([0,1,2,3]*8)[:30];rnd.shuffle(pos)
  out=[]
  for x,p in zip(L,pos):
    w=list(x[4:7]);rnd.shuffle(w);c=w[:p]+[x[3]]+w[p:]
    out.append({"t":x[0],"d":x[1],"q":x[2],"c":c,"a":p})
  return out
S={"gm":{"g":"Grade 11","n":"General Mathematics","items":GM},
"pr1":{"g":"Grade 11","n":"Practical Research 1","items":mk(PR1,11)},
"cesc":{"g":"Grade 12","n":"Community Engagement, Solidarity and Citizenship (CESC)","items":mk(CESC,12)},
"pr2":{"g":"Grade 12","n":"Practical Research 2","items":mk(PR2,13)},
"ent":{"g":"Grade 12","n":"Entrepreneurship","items":mk(ENT,14)}}
from collections import Counter
for k,v in S.items(): print(k,len(v["items"]),Counter("ABCD"[i["a"]] for i in v["items"]),Counter(i.get("d") for i in v["items"]),list(dict.fromkeys(i["t"] for i in v["items"])))
json.dump(S,open('subjects.json','w'),ensure_ascii=False,indent=1)
head=src[:src.index('<header>')].replace('<title>Math Reviewer — Bago NHS</title>','<title>SHS Reviewer — Bago NHS</title>')
head=head.replace('</style>','select{width:100%;font-size:1rem;padding:12px;border:2px solid #d8d7d2;border-radius:12px;font-family:inherit;background:#fff}\n</style>')
body=r'''<header><div class="school">Bago National High School · Roxas City</div><h1>SHS Reviewer — Bago NHS</h1><p>Grade 11 &amp; 12 · Alternative Delivery Mode</p></header>
<main>
<div class="card"><label class="f" for="nm">Name</label><input type="text" id="nm" autocomplete="name">
<label class="f" for="gr">Grade Level</label><select id="gr"><option value="">— Choose grade level —</option><option>Grade 11</option><option>Grade 12</option></select>
<label class="f" for="sj">Subject</label><select id="sj" disabled><option value="">— Choose grade level first —</option></select>
<label class="f" for="sec">Section</label><input type="text" id="sec"><p class="note" id="info"></p></div>
<div id="result"></div><div id="qs"></div>
<div class="card" id="bar" style="display:none"><div id="msg" class="err"></div><button id="submit">Submit answers</button><button id="retake" style="display:none">Retake</button></div>
<p class="note">Reviewer by Sir Raymart Valbarez. When you submit, your score is sent to your teacher.<br>Take a screenshot of your result card and send it to your teacher.</p>
</main>
<script>
const SAVE_URL="__URL__";
const SUBJ=__S__;
const L="ABCD",qs=document.getElementById("qs"),gr=document.getElementById("gr"),sj=document.getElementById("sj");let ITEMS=[],SID="";
function esc(s){return String(s).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]))}
gr.onchange=()=>{const g=gr.value;sj.innerHTML='<option value="">'+(g?'— Choose subject —':'— Choose grade level first —')+'</option>'+Object.keys(SUBJ).filter(k=>SUBJ[k].g===g).map(k=>'<option value="'+k+'">'+esc(SUBJ[k].n)+'</option>').join("");sj.disabled=!g;load("")};
sj.onchange=()=>load(sj.value);
function load(id){SID=id;ITEMS=id?SUBJ[id].items:[];document.getElementById("result").innerHTML="";document.getElementById("bar").style.display=id?"block":"none";document.getElementById("submit").style.display="block";document.getElementById("retake").style.display="none";
document.getElementById("info").textContent=id?ITEMS.length+" items · "+new Set(ITEMS.map(x=>x.t)).size+" topics":"Choose your grade level and subject to start.";render()}
function render(){let h="",cur="";ITEMS.forEach((it,i)=>{if(it.t!==cur){cur=it.t;h+='<h2 class="sec">'+esc(cur)+'</h2>'}
h+='<div class="card" id="c'+i+'"><p class="q">'+(i+1)+'. '+esc(it.q)+'</p>'+it.c.map((c,j)=>'<label class="opt" id="o'+i+'_'+j+'"><input type="radio" name="q'+i+'" value="'+j+'"> <span><b>'+L[j]+'.</b> '+esc(c)+'</span></label>').join("")+'<div class="exp" id="e'+i+'"></div></div>'});qs.innerHTML=h}
load("");
document.getElementById("submit").onclick=()=>{const nm=document.getElementById("nm").value.trim(),sc=document.getElementById("sec").value.trim(),msg=document.getElementById("msg");
if(!nm||!sc||!gr.value||!SID){msg.textContent="Please enter your name, grade level, subject and section first.";window.scrollTo(0,0);return}
let un=[];ITEMS.forEach((it,i)=>{if(!document.querySelector('input[name=q'+i+']:checked'))un.push(i+1)});
if(un.length&&!confirm(un.length+" item(s) unanswered. Submit anyway?"))return;msg.textContent="";
let score=0,per={};ITEMS.forEach((it,i)=>{per[it.t]=per[it.t]||[0,0];per[it.t][1]++;const s=document.querySelector('input[name=q'+i+']:checked'),v=s?+s.value:-1,ok=v===it.a;if(ok){score++;per[it.t][0]++}
document.getElementById("o"+i+"_"+it.a).classList.add("right");if(v>=0&&!ok)document.getElementById("o"+i+"_"+v).classList.add("wrong");
document.querySelectorAll('input[name=q'+i+']').forEach(x=>x.disabled=true);
document.getElementById("e"+i).innerHTML=(ok?'<span class="tag ok">Correct</span>':'<span class="tag no">'+(v<0?'No answer':'Wrong')+'</span>')+' Correct answer: <b>'+L[it.a]+'. '+esc(it.c[it.a])+'</b>'});
gr.disabled=true;sj.disabled=true;
const sub=SUBJ[SID].n,d=new Date().toLocaleString("en-PH",{dateStyle:"medium",timeStyle:"short",timeZone:"Asia/Manila"}),pct=Math.round(score/ITEMS.length*100);
document.getElementById("result").innerHTML='<div class="card score"><div class="note">SHS REVIEWER — BAGO NHS · RESULT</div><div class="row"><b style="font-size:1rem;display:inline">'+esc(sub)+'</b></div><b>'+score+' / '+ITEMS.length+'</b><div class="row">'+pct+'%</div><div class="row"><b style="font-size:1.1rem;display:inline">'+esc(nm)+'</b></div><div class="row">'+esc(gr.value)+' · Section: '+esc(sc)+'</div><div class="row">'+d+'</div><table>'+Object.keys(per).map(k=>'<tr><td>'+esc(k)+'</td><td>'+per[k][0]+' / '+per[k][1]+'</td></tr>').join("")+'</table><p class="note">Screenshot this card and send it to your teacher. Scroll down to review each answer.</p></div>';
let ans="";ITEMS.forEach((it,i)=>{const s=document.querySelector('input[name=q'+i+']:checked');ans+=s?L[+s.value]:"-"});
const pm={};Object.keys(per).forEach(k=>pm[k]=per[k][0]);const tb=Object.keys(per).map(k=>k+": "+per[k][0]+"/"+per[k][1]).join("; ");
const res=document.getElementById("result").firstChild,st=document.createElement("p");st.className="note";res.appendChild(st);
if(SAVE_URL){st.textContent="Saving score…";fetch(SAVE_URL,{method:"POST",mode:"no-cors",headers:{"Content-Type":"text/plain;charset=utf-8"},body:JSON.stringify({name:nm,section:gr.value+" · "+sub+" · "+sc,sectionOnly:sc,grade:gr.value,subject:sub,score:score,total:ITEMS.length,percent:pct,topics:pm,topicBreakdown:tb,answers:ans,v:2})}).then(()=>{st.innerHTML="<b style='color:var(--ok);font-size:1rem;display:inline'>✓ Score saved</b>"}).catch(()=>{st.innerHTML="<b style='color:var(--no);font-size:1rem;display:inline'>Couldn't save — please screenshot this card</b>"})}
document.getElementById("submit").style.display="none";document.getElementById("retake").style.display="block";window.scrollTo(0,0)};
document.getElementById("retake").onclick=()=>{gr.disabled=false;sj.disabled=false;load(SID)};
</script></body></html>'''
url=re.search(r'const SAVE_URL="([^"]+)"',src).group(1)
open('../index.html','w').write(head+body.replace('__URL__',url).replace('__S__',json.dumps(S,ensure_ascii=False)))
