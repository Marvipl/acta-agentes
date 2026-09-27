(function(){
  var alvo='__TITULO__';
  function norm(s){return String(s||'').replace(/ /g,' ').replace(/\s*:\s*$/,'').trim().toUpperCase();}
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  var a=norm(alvo), ultimo=null, total=0;
  document.querySelectorAll('input,textarea').forEach(function(e){
    var r=e.getBoundingClientRect(); if(r.width===0&&r.height===0)return;
    if(e.readOnly||e.disabled)return;
    if(norm(e.title)!==a)return;
    total++;
    if(String(e.value||'').trim()==='') ultimo=e;
  });
  if(!ultimo) return 'NAOACHOU vazio "'+alvo+'" (total '+total+')';
  ultimo.setAttribute('data-alvo','1');
  return 'marcado vazio "'+alvo+'" id='+ultimo.id+' (total '+total+')';
})()
