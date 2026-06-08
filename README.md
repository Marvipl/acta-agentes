# acta-agentes

Repositório que serve de "casa" para os agentes de inteligência de mercado e prospecção da Acta Robotics, executados via **Claude Code Routines (modo Remote/nuvem)**.

## Para que serve

A cada execução da rotina, a nuvem da Anthropic **clona este repositório** e disponibiliza os arquivos abaixo ao agente. Eles contêm a identidade, as regras e os dados de referência que o agente usa para produzir o briefing diário.

## Estrutura

```
acta-agentes/
├── README.md          (este arquivo)
├── SKILL.md           (playbook do agente: papel + regras + ponteiros)
└── referencia/
    ├── icp_acta.md        (perfis-alvo: cliente, fornecedor, parceiro)
    ├── portfolio_acta.md  (produtos, serviços e disciplina de nomenclatura)
    └── guardrails.md      (regras de segurança e de não-invenção)
```

## Onde fica o prompt operacional

O **passo a passo que roda a cada execução** fica no campo de **instruções da rotina** (na interface do Claude Code Routines), não neste repositório. Este repositório guarda apenas o **conteúdo estável** (playbook e referências). Veja o documento de arquitetura (`Arquitetura_Agentes_Acta_v1.md`, seção 5) para o prompt completo.

## Regra de manutenção importante

Routines, por padrão, só fazem push para branches com prefixo `claude/` e clonam a branch padrão (main) a cada execução. **Não use este repositório como banco de dados que muda todo dia.** Os dados diários (rastreamento de contatos) vivem na planilha **"Tracking Acta"** no Google Drive. Aqui só entra conteúdo que muda raramente.

## Como atualizar

Edite os arquivos de `referencia/` quando o portfólio, o perfil-alvo ou as regras mudarem (ex.: novo produto, novo setor de foco, nova trava). As mudanças passam a valer na próxima execução da rotina.
