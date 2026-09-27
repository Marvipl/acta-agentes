(function(){
  var alvo='__ALVO__';
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  var achou=null;
  document.querySelectorAll('button, .z-button, .z-toolbarbutton, a').forEach(function(e){
    var r=e.getBoundingClientRect(); if(r.width===0&&r.height===0)return;
    var t=(e.innerText||e.value||'').replace(/\u00a0/g,' ').trim().toUpperCase();
    if(t===alvo && !achou) achou=e;
  });
  if(!achou) return 'NAOACHOU:'+alvo;
  achou.setAttribute('data-alvo','1');
  return 'botao marcado: '+(achou.innerText||'').trim()+' id='+achou.id;
})()
