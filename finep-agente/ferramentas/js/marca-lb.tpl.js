(function(){
  var N=__N__;
  document.querySelectorAll('[data-alvo]').forEach(function(e){e.removeAttribute('data-alvo');});
  var lb=document.querySelector('.gantt_cal_light');
  if(!lb) return 'lightbox nao aberto';
  var tas=[];
  lb.querySelectorAll('textarea').forEach(function(e){
    var r=e.getBoundingClientRect();
    if(r.width===0&&r.height===0)return;
    tas.push(e);
  });
  if(tas.length<N) return 'NAOACHOU textarea '+N+' (existem '+tas.length+')';
  tas[N-1].setAttribute('data-alvo','1');
  return 'textarea '+N+' de '+tas.length+' marcada';
})()
