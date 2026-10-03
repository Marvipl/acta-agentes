# Verificação do orquestrador: regiões de origem e destino (2026-10-03)

Consulta agregada (sem colunas pessoais) sobre a tabela bruta, feita para responder Q04/Q05 do D0. Não é análise registrada: os números da oferta saem das análises do plano.

```sql
select "Região Origem", count(*) n from raw_prod_90dias_produtividade group by 1 order by n desc;
select "Região Destino", count(*) n from raw_prod_90dias_produtividade group by 1 order by n desc;
```

## Região Origem (tarefas)

| Região Origem | Tarefas |
|---|---|
| ROYAL CANIN - PICKING | 11380 |
| ESTRELA - PICKING | 7194 |
| ALFAPARF MILANO - PICKING | 6433 |
| VIC BEAUTE - PICKING  (B2C) | 5115 |
| HIVE - PICKING | 4540 |
| SR PRECO - PICKING | 3751 |
| COTY IT - PICKING | 2672 |
| IMBERA - PICKING | 838 |
| GOMES DA COSTA - PICKING | 578 |
| CONDOR - PICKING | 451 |
| PET TREATS - PALLET ALTO | 405 |
| RABBITOHS - PICKING | 91 |
| IMBERA - PALLET ALTO | 77 |
| VIC BEAUTE AG - PICKING | 69 |
| PHILIPS SIGNIFY B2C - PICKING | 68 |
| PHILIPS ILUMIN. B2B - PICKING | 41 |
| COTY IT - AVARIA | 36 |
| PET TREATS - PALLET ALTO,SR PRECO - PICKING | 28 |
| DEPYL ACTION - PICKING | 24 |
| JOHNSON B2B - PICKING | 24 |
| CONDOR - PICKING,COTY IT - PICKING | 22 |
| SHOP VINHO - PICKING | 20 |
| SEU GIN - PICKING | 20 |
| TEKBOND - AVARIA | 14 |
| LEGO - PICKING | 12 |
| OPEN DRINKS - PICKING | 11 |
| PHILIPS B2B - AVARIA | 9 |
| ESTRELA - AVARIA | 8 |
| PET MANIA - PICKING | 7 |
| COTY IT - PICKING,IMBERA - PICKING | 5 |
| CANCELADO | 4 |
| ISSVIVA - VENCIDOS | 4 |
| CANCELADO,ROYAL CANIN - PICKING | 4 |
| COTY IT - AVARIA,INSUMOS -GERAL | 2 |
| ALFAPARF MILANO - PICKING,VIC BEAUTE - PICKING  (B2C) | 2 |
| PET MANIA - AVARIA | 2 |
| ZERO FURO - PICKING | 2 |
| COTY IT - AVARIA,TEKBOND - PORTA PALET ALTO | 2 |
| JUVENTUS - PICKING | 1 |
| GOMES DA COSTA - AVARIA | 1 |
| VIC BEAUTE AG - AVARIA | 1 |
| CANCELADO,JOHNSON B2B - PICKING | 1 |
| IMBERA - PALLET ALTO,SHOP VINHO - PICKING | 1 |
| ROYAL CANIN - AVARIA | 1 |
| IMBERA - PALLET ALTO,IMBERA - PICKING | 1 |
| CONDOR - PICKING,IMBERA - PALLET ALTO | 1 |
| TEKBOND - PORTA PALET ALTO | 1 |
| PET FREE - PICKING,PET MANIA - PICKING | 1 |
| COTY IT - PICKING,COTY IT - PORTA PALLET ALTO | 1 |

## Região Destino (tarefas)

| Região Destino | Tarefas |
|---|---|
| PACKING | 27177 |
| PACKING ESPIRITO SANTO | 4540 |
| COLMEIA AMARELA | 1919 |
| COLMEIAS NUMERADAS | 1814 |
| COLMEIA AZUL | 1309 |
| COLMEIA TURQUESA | 1128 |
| COLMEIA BRONZE | 1070 |
| COLMEIA OURO | 998 |
| COLMEIA VERDE | 962 |
| COLMEIA ROXA | 924 |
| COLMEIA CHOCOLATE | 857 |
| COLMEIA VIOLETA | 622 |
| COLMEIA VERMELHA | 585 |
| PACKING ARMAZEM GERAL | 71 |

Leitura: o depositante é o prefixo de Região Origem antes de ' - ' (PICKING, AVARIA, PALLET ALTO etc.); há linhas com várias regiões separadas por vírgula e linhas CANCELADO. Região Destino separa colmeia (COLMEIA <cor>, COLMEIAS NUMERADAS) de packing (PACKING, PACKING ESPIRITO SANTO, PACKING ARMAZEM GERAL).
