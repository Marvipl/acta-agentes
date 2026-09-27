(function(){
  var frag='__PERGUNTA__'.toUpperCase(), resp='__RESPOSTA__'.toUpperCase();
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  // acha o no de texto da pergunta
  var lab=null;
  document.querySelectorAll('*').forEach(function(e){
    if(lab)return;
    if(e.children.length>1)return;
    var t=(e.innerText||'').replace(/\s+/g,' ').toUpperCase();
    if(t.indexOf(frag)>=0) lab=e;
  });
  if(!lab) return 'NAOACHOU pergunta "'+frag.slice(0,40)+'"';
  // sobe ate um container que tenha radios
  var cont=lab.closest('tr')||lab.parentElement;
  for(var i=0;i<6&&cont;i++){
    if(cont.querySelectorAll('input[type=radio]').length>=2) break;
    cont=cont.parentElement;
  }
  if(!cont) return 'NAOACHOU container com radios';
  var alvo=null;
  cont.querySelectorAll('input[type=radio]').forEach(function(r){
    if(alvo)return;
    var w=r.closest('.z-radio')||r.parentElement;
    var t=(w?(w.innerText||''):'').replace(/\s+/g,' ').trim().toUpperCase();
    if(t===resp) alvo=r;
  });
  if(!alvo) return 'NAOACHOU opcao "'+resp+'" na pergunta';
  // no ZK o input real pode estar oculto; clicar no .z-radio visivel
  var clicavel=alvo.closest('.z-radio')||alvo;
  if(!vis(clicavel)) clicavel=alvo;
  clicavel.setAttribute('data-alvo','1');
  return 'marcado '+resp+' para "'+(lab.innerText||'').replace(/\s+/g,' ').trim().slice(0,60)+'" (input '+alvo.id+')';
})()
