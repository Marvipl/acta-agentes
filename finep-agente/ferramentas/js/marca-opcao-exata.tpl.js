(function(){
  var alvo='__ALVO__';
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  function norm(s){return String(s||'').replace(/\u00a0/g,' ').replace(/\s+/g,' ').trim().toUpperCase();}
  var a=norm(alvo), achou=null, vistas=[];
  document.querySelectorAll('[id$="-pp"]').forEach(function(pp){
    if(!vis(pp))return;
    pp.querySelectorAll('.z-comboitem,.z-listitem').forEach(function(it){
      var t=norm(it.innerText);
      vistas.push(t);
      if(t===a && !achou) achou=it;
    });
  });
  if(!achou) return 'NAOACHOU exato "'+alvo+'" entre: '+vistas.slice(0,10).join(' | ');
  achou.setAttribute('data-alvo','1');
  return 'exato: '+norm(achou.innerText).slice(0,70);
})()
