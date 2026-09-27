(function(){
  var N=__N__;
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  document.querySelectorAll('[data-alvo2]').forEach(function(e){e.removeAttribute('data-alvo2');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var marcos=[];
  document.querySelectorAll('*').forEach(function(e){
    if(e.children.length!==0)return;
    var t=(e.innerText||'').replace(/\s+/g,' ').trim();
    if(/^Rubrica:/.test(t)&&vis(e)) marcos.push({t:t,y:e.getBoundingClientRect().top+window.scrollY});
  });
  marcos.sort(function(a,b){return a.y-b.y;});
  var y1=null,y2=null;
  for(var i=0;i<marcos.length;i++) if(/Equipe Própria/.test(marcos[i].t)){ y1=marcos[i].y; y2=(i+1<marcos.length)?marcos[i+1].y:Infinity; }
  if(y1===null) return 'NAOACHOU rubrica';
  // linhas: ancoradas no textarea de descricao
  var linhas=[];
  document.querySelectorAll('textarea').forEach(function(e){
    if(!vis(e))return;
    var y=e.getBoundingClientRect().top+window.scrollY;
    if(y<=y1||y>=y2)return;
    linhas.push({y:y, desc:String(e.value||'')});
  });
  linhas.sort(function(a,b){return a.y-b.y;});
  if(linhas.length<N) return 'NAOACHOU linha '+N+' (existem '+linhas.length+')';
  var alvoY=linhas[N-1].y;
  // na mesma faixa vertical (+-30px): o input editavel = valor unitario; o -real = finalidade
  var valor=null, fin=null;
  document.querySelectorAll('input').forEach(function(e){
    if(!vis(e))return;
    var y=e.getBoundingClientRect().top+window.scrollY;
    if(Math.abs(y-alvoY)>30)return;
    if(e.type==='checkbox')return;
    if(!e.readOnly && !e.disabled && !valor) valor=e;
    if(/-real$/.test(e.id) && !fin) fin=e;
  });
  if(!valor) return 'NAOACHOU valor unitario da linha '+N;
  valor.setAttribute('data-alvo','1');
  var msg='linha '+N+' "'+linhas[N-1].desc.slice(0,34)+'" valor='+valor.id;
  if(fin){
    var base=fin.id.replace(/-real$/,'');
    var btn=document.getElementById(base+'-btn')||fin;
    btn.setAttribute('data-alvo2','1');
    msg+=' finalidade='+base+' (atual="'+fin.value.slice(0,20)+'")';
  }
  return msg;
})()
