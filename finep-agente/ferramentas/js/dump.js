(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var sel=document.querySelector('.z-tab-selected');
  out.push('### ABA ATIVA: '+(sel?(sel.innerText||'').trim():'(sem abas)'));
  out.push('--- ABAS ---');
  document.querySelectorAll('.z-tab').forEach(function(t){
    if(!vis(t))return;
    out.push('  '+(t.className.indexOf('selected')>=0?'[ativa] ':'        ')+(t.innerText||'').trim());
  });
  out.push('--- TEXTO ---');
  var main=document.querySelector('.z-tabpanel:not([style*="display: none"])')||document.body;
  out.push((main.innerText||'').replace(/\n{3,}/g,NL+NL).slice(0,4000));
  out.push('--- CAMPOS ---');
  document.querySelectorAll('input,textarea,select').forEach(function(e){
    if(!vis(e)||e.type==='hidden')return;
    var extra=(e.type==='radio'||e.type==='checkbox')?(' checked='+e.checked):'';
    out.push('  '+e.tagName+':'+(e.type||'')+' id='+e.id+' title="'+(e.title||'')+'" ro='+(e.readOnly?1:0)+extra+' val="'+String(e.value||'').slice(0,60)+'"');
  });
  out.push('--- BOTOES ---');
  document.querySelectorAll('button,.z-button,.z-toolbarbutton').forEach(function(e){
    if(!vis(e))return; var t=(e.innerText||e.value||'').trim(); if(t) out.push('  BTN "'+t+'"');
  });
  return out.join(NL);
})()
