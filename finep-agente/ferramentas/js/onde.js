(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  // titulo do passo: o cabecalho acima das abas
  var h=document.querySelectorAll('.z-label,.z-caption,h1,h2,h3');
  var tit=[];
  h.forEach(function(e){ if(!vis(e))return; var t=(e.innerText||'').trim(); if(t.length>5&&t.length<80&&tit.length<12) tit.push(t); });
  out.push('--- primeiros rotulos da tela ---');
  out.push('  '+tit.slice(0,12).join(NL+'  '));
  out.push('--- botoes de navegacao ---');
  document.querySelectorAll('button,.z-button,.z-toolbarbutton').forEach(function(e){
    if(!vis(e))return; var t=(e.innerText||e.value||'').trim(); if(t) out.push('  "'+t+'"');
  });
  out.push('--- menu lateral / etapas ---');
  document.querySelectorAll('a,.z-treecell,.z-listcell').forEach(function(e){
    if(!vis(e))return; var t=(e.innerText||'').trim();
    if(t && t.length<70 && /passo|etapa|dados|custo|cronograma|projeto|altera/i.test(t)) out.push('  '+t);
  });
  return out.join(NL);
})()
