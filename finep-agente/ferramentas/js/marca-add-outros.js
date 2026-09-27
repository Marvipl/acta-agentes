(function(){
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var lab=null;
  document.querySelectorAll('*').forEach(function(e){
    if(lab)return;
    if(e.children.length===0 && /Outros membros/i.test(e.innerText||'')) lab=e;
  });
  if(!lab) return 'NAOACHOU rotulo Outros membros';
  var y0=lab.getBoundingClientRect().top+window.scrollY;
  var alvo=null;
  document.querySelectorAll('.z-button,button').forEach(function(b){
    if(!vis(b))return;
    if(!/Adicionar/i.test(b.innerText||''))return;
    var y=b.getBoundingClientRect().top+window.scrollY;
    if(y>y0 && !alvo) alvo=b;
  });
  if(!alvo) return 'NAOACHOU Adicionar de Outros membros';
  alvo.setAttribute('data-alvo','1');
  return 'Adicionar (Outros membros) id='+alvo.id;
})()
