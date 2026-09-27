(function(){
  var alvo='__RUBRICA__'.toUpperCase(), N=__N__;
  ['data-alvo','data-alvo2','data-alvo3','data-alvo4','data-alvo5'].forEach(function(a){
    document.querySelectorAll('['+a+']').forEach(function(e){e.removeAttribute(a);});
  });
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var marcos=[];
  document.querySelectorAll('*').forEach(function(e){
    if(e.children.length!==0)return;
    var t=(e.innerText||'').replace(/\s+/g,' ').trim();
    if(/^Rubrica:/.test(t)&&vis(e)) marcos.push({t:t,y:e.getBoundingClientRect().top+window.scrollY});
  });
  marcos.sort(function(a,b){return a.y-b.y;});
  var y1=null,y2=null;
  for(var i=0;i<marcos.length;i++){
    if(marcos[i].t.toUpperCase().indexOf(alvo)>=0){ y1=marcos[i].y; y2=(i+1<marcos.length)?marcos[i+1].y:Infinity; break; }
  }
  if(y1===null) return 'NAOACHOU rubrica "'+alvo+'"';
  // linhas ancoradas no textarea de descricao
  var linhas=[];
  document.querySelectorAll('textarea').forEach(function(e){
    if(!vis(e))return;
    var y=e.getBoundingClientRect().top+window.scrollY;
    if(y<=y1||y>=y2)return;
    linhas.push({y:y, el:e});
  });
  linhas.sort(function(a,b){return a.y-b.y;});
  if(linhas.length<N) return 'NAOACHOU linha '+N+' em "'+alvo+'" (existem '+linhas.length+')';
  var L=linhas[N-1];
  L.el.setAttribute('data-alvo','1');            // descricao
  var edits=[], fin=null, chk=null;
  document.querySelectorAll('input').forEach(function(e){
    if(!vis(e))return;
    var y=e.getBoundingClientRect().top+window.scrollY;
    if(Math.abs(y-L.y)>30)return;
    if(e.type==='checkbox'){ chk=e; return; }
    if(/-real$/.test(e.id)){ if(!fin) fin=e; return; }
    if(!e.readOnly&&!e.disabled) edits.push(e);
  });
  if(edits[0]) edits[0].setAttribute('data-alvo2','1');   // qtde
  if(edits[1]) edits[1].setAttribute('data-alvo3','1');   // valor unitario
  if(fin){
    var base=fin.id.replace(/-real$/,'');
    var b=document.getElementById(base+'-btn')||fin;
    b.setAttribute('data-alvo4','1');
  }
  if(chk) chk.setAttribute('data-alvo5','1');
  return 'rubrica "'+alvo+'" linha '+N+'/'+linhas.length+': desc='+L.el.id+' qtde='+(edits[0]?edits[0].id:'-')+' valor='+(edits[1]?edits[1].id:'-')+' fin='+(fin?fin.id:'-')+' chk='+(chk?chk.id:'-');
})()
