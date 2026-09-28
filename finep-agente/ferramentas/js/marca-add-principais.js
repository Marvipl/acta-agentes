(function(){
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var lab=null;
  document.querySelectorAll('*').forEach(function(e){
    if(lab)return;
    if(e.children.length===0 && /Outros membros/i.test(e.innerText||'')) lab=e;
  });
  var y0=lab?lab.getBoundingClientRect().top+window.scrollY:Infinity;
  var alvo=null;
  document.querySelectorAll('.z-button,button').forEach(function(b){
    if(!vis(b))return;
    if(!/Adicionar/i.test(b.innerText||''))return;
    var y=b.getBoundingClientRect().top+window.scrollY;
    if(y<y0) alvo=b;   // o ultimo Adicionar ANTES de "Outros membros"
  });
  if(!alvo) return 'NAOACHOU Adicionar de Principais membros';
  alvo.setAttribute('data-alvo','1');
  return 'Adicionar (Principais) id='+alvo.id;
})()
