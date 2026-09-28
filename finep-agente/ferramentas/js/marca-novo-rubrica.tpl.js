(function(){
  var alvo='__RUBRICA__'.toUpperCase();
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
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
  if(y1===null) return 'NAOACHOU rubrica "'+alvo+'" (existem: '+marcos.map(function(m){return m.t;}).join(' / ')+')';
  var alvoBtn=null;
  document.querySelectorAll('.z-button,button').forEach(function(b){
    if(!vis(b))return;
    if(!/Novo/i.test(b.innerText||''))return;
    var y=b.getBoundingClientRect().top+window.scrollY;
    if(y>y1&&y<y2&&!alvoBtn) alvoBtn=b;
  });
  if(!alvoBtn) return 'NAOACHOU botao Novo na rubrica';
  alvoBtn.setAttribute('data-alvo','1');
  return 'Novo de "'+alvo+'" id='+alvoBtn.id+' (faixa '+Math.round(y1)+'-'+(y2===Infinity?'fim':Math.round(y2))+')';
})()
