-- FICTÍCIO: missões com o modelo do robô e o período (dia/noite), dentro da faixa plausível do especialista
create table prep_missoes as
select m.*, r.modelo,
       case when m.turno = 'noite' then 'noite' else 'dia' end as periodo,
       strftime(cast(m.data as date), '%Y-%m') as mes
from base_missoes m left join base_robos r using (robo_id)
where m.duracao_min between 1 and 120;
