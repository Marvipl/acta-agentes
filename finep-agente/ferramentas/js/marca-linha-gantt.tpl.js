(function(){
  var alvo='__ALVO__'.toUpperCase();
  document.querySelectorAll('[data-linha]').forEach(function(e){e.removeAttribute('data-linha');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var linha=null;
  document.querySelectorAll('.gantt_row').forEach(function(e){
    if(linha||!vis(e))return;
    var t=(e.innerText||'').replace(/\s+/g,' ').toUpperCase();
    if(t.indexOf(alvo)>=0) linha=e;
  });
  if(!linha) return 'NAOACHOU linha "'+alvo+'"';
  linha.setAttribute('data-linha','1');
  return 'linha marcada: "'+(linha.innerText||'').replace(/\s+/g,' ').trim().slice(0,40)+'"';
})()
