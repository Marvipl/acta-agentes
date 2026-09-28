(function(){
  var alvo='__ALVO__';
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var achou=null, vistos=0;
  document.querySelectorAll('[id$="-pp"]').forEach(function(pp){
    if(!vis(pp))return;
    pp.querySelectorAll('.z-comboitem,.z-listitem').forEach(function(it){
      vistos++;
      if(achou)return;
      var t=(it.innerText||'').replace(/\u00a0/g,' ').replace(/\s+/g,' ').toUpperCase();
      if(t.indexOf(alvo)>=0) achou=it;
    });
  });
  if(!achou) return 'NAOACHOU "'+alvo+'" (varridas '+vistos+' opcoes)';
  achou.setAttribute('data-alvo','1');
  return 'opcao marcada: '+(achou.innerText||'').replace(/\u00a0/g,' ').replace(/\s+/g,' ').trim().slice(0,90);
})()
