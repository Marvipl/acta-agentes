(function(){
  var alvo='__ALVO__'.toUpperCase(), mes=__MES__, dur=__DUR__;
  if(typeof window.gantt!=='object') return 'gantt ausente';
  var achou=null;
  gantt.eachTask(function(t){
    if(achou)return;
    if(String(t.text||'').toUpperCase().indexOf(alvo)>=0) achou=t;
  });
  if(!achou) return 'NAOACHOU tarefa "'+alvo+'"';
  // mes 1 = 01/01/2000; mes N = N-1 meses depois
  var ini=new Date(2000,0,1);
  ini.setMonth(ini.getMonth()+(mes-1));
  achou.start_date=ini;
  achou.duration=dur;
  achou.end_date=gantt.calculateEndDate(achou.start_date, dur);
  gantt.updateTask(achou.id);
  var f=gantt.date.date_to_str('%d/%m/%Y');
  return 'tarefa "'+String(achou.text).slice(0,35)+'" -> ini='+f(achou.start_date)+' fim='+f(achou.end_date)+' dur='+achou.duration;
})()
