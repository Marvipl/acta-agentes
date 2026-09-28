(function(){
  var alvo='__ALVO__'.toUpperCase();
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  // acha a linha do gantt cujo texto casa
  var linha=null;
  document.querySelectorAll('.gantt_row,.gantt_task_row').forEach(function(e){
    if(linha||!vis(e))return;
    var t=(e.innerText||'').replace(/\s+/g,' ').toUpperCase();
    if(t.indexOf(alvo)>=0) linha=e;
  });
  if(!linha) return 'NAOACHOU linha "'+alvo+'"';
  var add=linha.querySelector('.gantt_add');
  if(!add) return 'NAOACHOU botao + na linha';
  add.setAttribute('data-alvo','1');
  var r=linha.getBoundingClientRect();
  return '+ marcado na linha "'+(linha.innerText||'').replace(/\s+/g,' ').trim().slice(0,45)+'"';
})()
