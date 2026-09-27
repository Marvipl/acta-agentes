(function(){
  var NL=String.fromCharCode(10), out=[];
  document.querySelectorAll('.z-combobox-popup, .z-comboboxpopup, [id$="-pp"]').forEach(function(pp){
    var r=pp.getBoundingClientRect();
    var aberto=!(r.width===0&&r.height===0);
    out.push('POPUP id='+pp.id+' aberto='+aberto+' itens:');
    pp.querySelectorAll('.z-comboitem, tr, li').forEach(function(it,i){
      var t=(it.innerText||'').replace(/\u00a0/g,' ').trim();
      if(t) out.push('  ['+i+'] '+t);
    });
  });
  if(!out.length) out.push('(nenhum popup no DOM)');
  return out.join(NL);
})()
