(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  // acha os titulos "Rubrica: X" e a posicao de cada um
  var marcos=[];
  document.querySelectorAll('*').forEach(function(e){
    if(e.children.length!==0)return;
    var t=(e.innerText||'').replace(/\s+/g,' ').trim();
    if(/^Rubrica:/.test(t) && vis(e)) marcos.push({t:t, y:e.getBoundingClientRect().top+window.scrollY});
  });
  marcos.sort(function(a,b){return a.y-b.y;});
  out.push('RUBRICAS: '+marcos.length);
  // para cada rubrica, conta linhas (inputs) ate a proxima
  marcos.forEach(function(m,i){
    var y1=m.y, y2=(i+1<marcos.length)?marcos[i+1].y:Infinity;
    var campos=0, editaveis=0, vazios=0;
    document.querySelectorAll('input').forEach(function(e){
      if(!vis(e))return;
      var y=e.getBoundingClientRect().top+window.scrollY;
      if(y<=y1||y>=y2)return;
      campos++;
      if(!e.readOnly&&!e.disabled){ editaveis++; if(String(e.value||'').trim()==='') vazios++; }
    });
    out.push('  '+m.t+'  -> campos='+campos+' editaveis='+editaveis+' vazios='+vazios+'  y='+Math.round(y1));
  });
  return out.join(NL);
})()
