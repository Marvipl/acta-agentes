(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  out.push('=== ABAS / TABS ===');
  document.querySelectorAll('.z-tab, li[id$="-tab"], .z-tab-text').forEach(function(e){
    if(!vis(e))return; var t=(e.innerText||'').trim(); if(t) out.push('  TAB ['+(e.getAttribute('aria-selected')||'')+'] '+t);
  });
  out.push('=== CAMPOS ===');
  document.querySelectorAll('input,textarea,select').forEach(function(e){
    if(!vis(e))return; var r=e.getBoundingClientRect();
    out.push('  '+e.tagName+':'+(e.type||'')+' id='+e.id+' title="'+(e.title||'')+'" ro='+(e.readOnly?1:0)+' val="'+String(e.value||'').slice(0,50)+'" y='+Math.round(r.top+window.scrollY));
  });
  out.push('=== BOTOES ===');
  document.querySelectorAll('button, .z-button, a.z-toolbarbutton, .z-toolbarbutton').forEach(function(e){
    if(!vis(e))return; var t=(e.innerText||e.value||'').trim(); if(!t)return;
    var r=e.getBoundingClientRect();
    out.push('  BTN "'+t+'" id='+e.id+' y='+Math.round(r.top+window.scrollY));
  });
  return out.join(NL);
})()
