(function(){
  var rot='__ROTULO__';
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  function norm(s){return String(s||'').replace(/\u00a0/g,' ').replace(/\s*:\s*$/,'').replace(/\s+/g,' ').trim().toUpperCase();}
  var a=norm(rot), cands=[];
  document.querySelectorAll('input[id$="-real"]').forEach(function(e){
    if(!vis(e))return; if(e.type==='radio'||e.type==='checkbox')return;
    var lab='', p=e.closest('tr')||e.parentElement;
    for(var i=0;i<4&&p;i++){ var t=(p.innerText||'').replace(/\s+/g,' ').trim(); if(t.length>2){lab=t;break;} p=p.parentElement; }
    if(norm(lab)===a) cands.push(e);
  });
  if(!cands.length) return 'NAOACHOU combo "'+rot+'"';
  // o ultimo vazio; se todos preenchidos, o ultimo
  var alvo=null;
  cands.forEach(function(e){ if(String(e.value||'').trim()==='') alvo=e; });
  if(!alvo) alvo=cands[cands.length-1];
  var base=alvo.id.replace(/-real$/,'');
  var btn=document.getElementById(base+'-btn')||alvo;
  btn.setAttribute('data-alvo','1');
  return 'combo "'+rot+'" -> '+base+' (de '+cands.length+' na tela)';
})()
