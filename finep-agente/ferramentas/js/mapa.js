(function(){
  var NL=String.fromCharCode(10), out=[];
  var raiz=document.querySelector('.z-tabpanel:not([style*="display: none"])')||document.body;
  var it=document.createTreeWalker(raiz, NodeFilter.SHOW_ELEMENT, null, false);
  var n, ctrl=0, ultimoTexto='';
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  while((n=it.nextNode())){
    var tag=n.tagName;
    if(tag==='INPUT'||tag==='TEXTAREA'){
      if(n.type==='hidden')return;
      ctrl++;
      var tipo=(tag==='TEXTAREA')?'TEXTAREA':n.type.toUpperCase();
      var extra='';
      if(n.type==='radio'||n.type==='checkbox') extra=' checked='+n.checked;
      // rotulo do radio: texto do span/label mais proximo
      var rot='';
      if(n.type==='radio'||n.type==='checkbox'){
        var p=n.closest('.z-radio,.z-checkbox')||n.parentElement;
        if(p) rot=(p.innerText||'').replace(/\s+/g,' ').trim().slice(0,60);
        if(!rot && n.parentElement) rot=(n.parentElement.innerText||'').replace(/\s+/g,' ').trim().slice(0,60);
      }
      out.push('['+ctrl+'] '+tipo+' id='+n.id+' vis='+vis(n)+' ro='+(n.readOnly?1:0)+extra
               +(rot?' rotulo="'+rot+'"':'')
               +(n.title?' title="'+n.title+'"':'')
               +' val="'+String(n.value||'').slice(0,40)+'"');
    } else if(n.children.length===0){
      var t=(n.innerText||'').replace(/\s+/g,' ').trim();
      if(t.length>25 && t!==ultimoTexto){ ultimoTexto=t; out.push('    ~ '+t.slice(0,150)); }
    }
  }
  return out.join(NL);
})()
