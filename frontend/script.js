const API_BASE = "http://127.0.0.1:8000/api";

const pageInfo = {
 dashboard:["Dashboard","Your personal AI-powered study workspace"],
 documents:["Study Documents","Upload and process your learning material"],
 chat:["AI Document Chat","Ask questions grounded in your documents"],
 summary:["AI Summarizer","Create revision summaries"],
 quiz:["MCQ Generator","Practice with AI-generated questions"],
 questions:["Important Questions","Generate exam-oriented questions"],
 flashcards:["Flashcards","Learn concepts using active recall"],
 notes:["Study Notes","Generate structured revision notes"],
 simple:["Explain Simply","Convert difficult concepts into easy language"],
 planner:["Study Planner","Create a personalized preparation schedule"]
};

let filesSelected=[], quizData=[], cards=[], cardIndex=0;

document.querySelectorAll(".nav-btn").forEach(b=>b.onclick=()=>openPage(b.dataset.page));
function openPage(page){
 document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
 document.getElementById(page).classList.add("active");
 document.querySelectorAll(".nav-btn").forEach(b=>b.classList.toggle("active",b.dataset.page===page));
 document.getElementById("title").textContent=pageInfo[page][0];
 document.getElementById("subtitle").textContent=pageInfo[page][1];
 if(page==="documents") loadDocuments();
}

const input=document.getElementById("file-input"), drop=document.getElementById("dropzone"), upload=document.getElementById("upload-btn");
input.onchange=e=>{filesSelected=[...e.target.files];renderSelected();};
["dragenter","dragover"].forEach(x=>drop.addEventListener(x,e=>{e.preventDefault();drop.style.borderColor="#5b4bdb"}));
["dragleave","drop"].forEach(x=>drop.addEventListener(x,e=>{e.preventDefault();drop.style.borderColor="#cfd3df"}));
drop.addEventListener("drop",e=>{filesSelected=[...e.dataTransfer.files].filter(f=>/\.(pdf|docx|txt)$/i.test(f.name));renderSelected();});
function renderSelected(){
 document.getElementById("file-preview").innerHTML=filesSelected.map(f=>`<div class="file-row">📄 ${esc(f.name)} <span>${bytes(f.size)}</span></div>`).join("");
 upload.classList.toggle("hidden",filesSelected.length===0);
}
upload.onclick=async()=>{
 const fd=new FormData();filesSelected.forEach(f=>fd.append("files",f));
 setBtn(upload,true,"Processing...");
 try{const d=await request("/documents/upload",fd,true);document.getElementById("upload-result").innerHTML=`<p>✅ ${esc(d.message||"Documents processed.")}</p>`;updateStats(d.stats);loadDocuments();}
 catch(e){toast(e.message)}finally{setBtn(upload,false,"Process Documents")}
};

async function loadDocuments(){
 try{const d=await request("/documents");document.getElementById("documents-list").innerHTML=(d.documents||[]).map(x=>`<div class="doc-row">📄 ${esc(x.filename)} <span>${esc(x.status||"Processed")}</span></div>`).join("")||"<p class='muted'>No documents uploaded.</p>";updateStats(d.stats)}catch(e){}
}
document.getElementById("chat-form").onsubmit=async e=>{
 e.preventDefault();const inp=document.getElementById("chat-input"),q=inp.value.trim();if(!q)return;
 addBubble("user",q);inp.value="";const loading=addBubble("ai","Thinking...");
 try{const d=await request("/chat",{question:q});loading.querySelector("p").textContent=d.answer||"No answer.";if(d.sources?.length){const s=document.createElement("small");s.textContent="\nSources: "+d.sources.map(x=>`${x.filename||x.source} p.${x.page??"?"}`).join(", ");loading.appendChild(s)}updateStats(d.stats)}
 catch(e){loading.querySelector("p").textContent="Error: "+e.message}
};
function addBubble(type,text){const b=document.createElement("div");b.className=`bubble ${type}`;b.innerHTML=`<b>${type==="user"?"You":"AI Assistant"}</b><p>${esc(text)}</p>`;document.getElementById("chat-box").appendChild(b);document.getElementById("chat-box").scrollTop=999999;return b}
function clearChat(){document.getElementById("chat-box").innerHTML=`<div class="bubble ai"><b>AI Assistant</b><p>Chat cleared.</p></div>`}

async function generateSummary(){await generate("/generate/summary",{type:document.getElementById("summary-type").value},"summary-output")}
async function generateQuestions(){await generate("/generate/questions",{},"questions-output")}
async function generateNotes(){await generate("/generate/notes",{},"notes-output")}
async function explainSimply(){await generate("/generate/explain",{text:document.getElementById("simple-text").value,level:document.getElementById("simple-level").value},"simple-output")}
async function generatePlan(){await generate("/generate/plan",{subject:document.getElementById("plan-subject").value,units:+document.getElementById("plan-units").value,days:+document.getElementById("plan-days").value,hours:+document.getElementById("plan-hours").value,exam_date:document.getElementById("plan-date").value},"plan-output")}
async function generate(path,body,id){const o=document.getElementById(id);o.textContent="Generating...";try{const d=await request(path,body);o.textContent=d.result||d.answer||JSON.stringify(d,null,2);updateStats(d.stats)}catch(e){o.textContent="Error: "+e.message}}

async function generateQuiz(){
 const o=document.getElementById("quiz-output");o.innerHTML="Generating...";
 try{const d=await request("/generate/mcqs",{count:+document.getElementById("quiz-count").value,difficulty:document.getElementById("quiz-difficulty").value});quizData=d.questions||[];renderQuiz();updateStats(d.stats)}catch(e){o.textContent="Error: "+e.message}
}
function renderQuiz(){
 const o=document.getElementById("quiz-output");
 o.innerHTML=quizData.map((q,i)=>`<div class="quiz-question"><b>Q${i+1}. ${esc(q.question)}</b>${(q.options||[]).map(a=>`<label class="quiz-option"><input type="radio" name="q${i}" value="${attr(a)}"> ${esc(a)}</label>`).join("")}</div>`).join("")+`<button class="primary" onclick="submitQuiz()">Submit Quiz</button>`;
}
async function submitQuiz(){
 const answers=quizData.map((_,i)=>document.querySelector(`input[name=q${i}]:checked`)?.value||"");
 try{const d=await request("/quiz/submit",{answers});toast(`Score: ${d.score}/${d.total} (${d.percentage}%)`);updateStats(d.stats)}catch(e){toast(e.message)}
}
async function generateFlashcards(){
 const o=document.getElementById("flashcards-output");o.innerHTML='<div class="card">Generating...</div>';
 try{const d=await request("/generate/flashcards",{count:10});cards=d.flashcards||[];cardIndex=0;renderCard();}catch(e){o.innerHTML=`<div class="card">Error: ${esc(e.message)}</div>`}
}
function renderCard(){
 if(!cards.length)return;const c=cards[cardIndex];
 document.getElementById("flashcards-output").innerHTML=`<div><div class="card"><div><b>${esc(c.front)}</b><p id="card-answer" style="display:none">${esc(c.back)}</p></div></div><div style="margin-top:15px"><button class="secondary" onclick="document.getElementById('card-answer').style.display='block'">Show Answer</button> <button class="secondary" onclick="prevCard()">←</button> <button class="secondary" onclick="nextCard()">→</button></div><p class="muted">Card ${cardIndex+1} of ${cards.length}</p></div>`;
}
function prevCard(){if(cardIndex>0){cardIndex--;renderCard()}} function nextCard(){if(cardIndex<cards.length-1){cardIndex++;renderCard()}}

async function request(path,body=null,isForm=false){
 const opt={method:body?"POST":"GET"};
 if(body){if(isForm)opt.body=body;else{opt.headers={"Content-Type":"application/json"};opt.body=JSON.stringify(body)}}
 let r;try{r=await fetch(API_BASE+path,opt)}catch(e){throw new Error("Backend unavailable. Start FastAPI on port 8000.")}
 if(!r.ok){let x;try{x=await r.json()}catch(_){throw new Error(`${r.status} ${r.statusText}`)}throw new Error(x.detail||x.message||"Request failed")}
 return r.json()
}
async function updateDashboard(){try{updateStats(await request("/stats"))}catch(e){}}
function updateStats(s={}){if(s.documents!=null)document.getElementById("documents-stat").textContent=s.documents;if(s.questions!=null)document.getElementById("questions-stat").textContent=s.questions;if(s.quizzes!=null)document.getElementById("quizzes-stat").textContent=s.quizzes;if(s.avg_score!=null)document.getElementById("score-stat").textContent=Math.round(s.avg_score)+"%"}
function setBtn(b,on,t){b.disabled=on;b.textContent=t}
function toast(m){const t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2800)}
function bytes(n){return n<1024?n+" B":n<1048576?(n/1024).toFixed(1)+" KB":(n/1048576).toFixed(1)+" MB"}
function esc(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
function attr(s){return esc(s).replace(/`/g,"&#96;")}
updateDashboard();
