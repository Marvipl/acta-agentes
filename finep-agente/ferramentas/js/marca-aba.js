(function(){
  var alvo='INSTITUI';
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  var achou=null;
  document.querySelectorAll('.z-tab').forEach(function(e){
    var r=e.getBoundingClientRect(); if(r.width===0&&r.height===0)return;
    var t=(e.innerText||'').toUpperCase();
    if(t.indexOf(alvo)>=0 && !achou) achou=e;
  });
  if(!achou) return 'NAOACHOU';
  achou.setAttribute('data-alvo','1');
  var r=achou.getBoundingClientRect();
  return 'marcado: '+(achou.innerText||'').trim()+' em ('+Math.round(r.left+r.width/2)+','+Math.round(r.top+r.height/2)+')';
})()
