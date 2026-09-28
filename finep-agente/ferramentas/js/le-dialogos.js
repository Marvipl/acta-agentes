(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  document.querySelectorAll('.z-window, .z-messagebox, .z-window-modal, .z-window-highlighted').forEach(function(w){
    if(!vis(w))return;
    out.push('>>> DIALOGO: '+(w.innerText||'').replace(/\n{2,}/g,NL).trim().slice(0,1200));
    var bs=[]; w.querySelectorAll('button,.z-button').forEach(function(b){if(vis(b)){var t=(b.innerText||b.value||'').trim(); if(t)bs.push(t);}});
    if(bs.length) out.push('    botoes: '+bs.join(' | '));
  });
  var errs=[];
  document.querySelectorAll('.z-errbox, .z-notification, [class*="errbox"]').forEach(function(e){
    if(!vis(e))return; errs.push((e.innerText||e.title||'').trim().slice(0,200));
  });
  if(errs.length) out.push('>>> ERRBOX: '+errs.join(' ;; '));
  if(!out.length) out.push('(nenhum dialogo aberto)');
  return out.join(NL);
})()
