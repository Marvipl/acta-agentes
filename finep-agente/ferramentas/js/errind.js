(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  var n=0;
  document.querySelectorAll('.err-ind').forEach(function(e){
    if(!vis(e))return;
    n++;
    var r=e.getBoundingClientRect();
    // sobe ate um container com rotulo util
    var ctx='', p=e.parentElement;
    for(var i=0;i<6&&p;i++){
      var t=(p.innerText||'').replace(/\s+/g,' ').trim();
      if(t.length>15){ ctx=t.slice(0,200); break; }
      p=p.parentElement;
    }
    out.push('ERR#'+n+' id='+e.id+' title="'+(e.title||'')+'" pos=('+Math.round(r.left)+','+Math.round(r.top)+') contexto="'+ctx+'"');
  });
  out.push('total de err-ind visiveis: '+n);
  return out.join(NL);
})()
