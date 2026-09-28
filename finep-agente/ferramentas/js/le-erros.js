(function(){
  var NL=String.fromCharCode(10), out=[];
  function vis(e){var r=e.getBoundingClientRect();return !(r.width===0&&r.height===0);}
  // 1) errboxes visiveis e o campo a que se ancoram
  var n=0;
  document.querySelectorAll('[class*="errbox"]').forEach(function(eb){
    n++;
    var r=eb.getBoundingClientRect();
    var msg=(eb.innerText||eb.title||eb.getAttribute('aria-label')||'').trim();
    // o id do errbox no ZK costuma ser <idDoCampo>-errbox / ou guarda o alvo em .z-errbox
    var base=eb.id ? eb.id.replace(/-errbox.*$/,'') : '';
    var campo=base?document.getElementById(base):null;
    var titulo=campo?(campo.title||campo.id):'';
    // procura tambem por um irmao/ancestral com title
    if(!titulo){
      var p=eb.parentElement, t='';
      for(var i=0;i<5&&p;i++){ var c=p.querySelector('[title]'); if(c&&c.title){t=c.title;break;} p=p.parentElement; }
      titulo=t;
    }
    out.push('ERR#'+n+' vis='+vis(eb)+' id='+eb.id+' msg="'+msg.slice(0,200)+'" campo="'+titulo+'" pos=('+Math.round(r.left)+','+Math.round(r.top)+')');
  });
  // 2) aba em que cada erro esta: lista abas e se tem marca de erro
  out.push('--- ABAS ---');
  document.querySelectorAll('.z-tab').forEach(function(t){
    if(!vis(t))return;
    out.push('  '+(t.className.indexOf('selected')>=0?'[ativa] ':'        ')+(t.innerText||'').trim());
  });
  // 3) campos obrigatorios vazios nas 3 abas (varre tudo, inclusive oculto)
  out.push('--- CAMPOS VAZIOS (todos, inclusive de abas ocultas) ---');
  document.querySelectorAll('input,textarea').forEach(function(e){
    if(e.type==='hidden')return;
    var v=String(e.value||'').trim();
    var marca=(e.type==='checkbox')?('checked='+e.checked):('vazio='+(v===''));
    if((e.type==='checkbox'&&!e.checked)||(e.type!=='checkbox'&&v===''))
      out.push('  '+e.tagName+':'+e.type+' id='+e.id+' title="'+(e.title||'')+'" '+marca+' visivel='+vis(e));
  });
  if(n===0) out.unshift('(nenhum errbox no DOM)');
  return out.join(NL);
})()
