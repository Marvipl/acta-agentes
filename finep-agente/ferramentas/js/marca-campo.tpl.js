(function(){
  var alvo='__TITULO__', idx=__IDX__;
  function norm(s){ return String(s||'').replace(/ /g,' ').replace(/\s*:\s*$/,'').trim().toUpperCase(); }
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  var a=norm(alvo), achados=[];
  document.querySelectorAll('input,textarea').forEach(function(e){
    var r=e.getBoundingClientRect(); if(r.width===0&&r.height===0)return;
    if(e.readOnly||e.disabled)return;
    if(e.type==='radio'||e.type==='checkbox'||e.type==='hidden')return;
    if(norm(e.title)===a) achados.push(e);
  });
  if(achados.length<=idx) return 'NAOACHOU "'+alvo+'" idx='+idx+' (encontrados '+achados.length+')';
  achados[idx].setAttribute('data-alvo','1');
  return 'marcado "'+alvo+'"['+idx+'] id='+achados[idx].id+' de '+achados.length;
})()
