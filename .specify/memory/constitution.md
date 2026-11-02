# Constituição — Floricultura em Tempo Real

Trabalho 01 de Linguagem de Programação e Paradigmas (2026/2), "Vila em Tempo Real",
Vila 19 — Floricultura. Desenvolvido por Julia Fitzlaff e Eduarda de Oliveira.

## Princípios

### I. Orientação a eventos

- Toda comunicação entre cliente e servidor acontece por eventos com nome, emitidos (emit) e
  escutados por tratadores (on). Nada de chamadas diretas no lugar de eventos.
- Pedidos do cliente (`objeto.acao_solicitada`) são separados dos fatos confirmados pelo
  servidor (`objeto.acao_no_passado`). A recusa também é um evento.
- Temporizadores rodam no servidor e são fontes de eventos (colheita, obra, montagem, vendas,
  validade). O cliente nunca usa polling nem laços para descobrir se algo mudou.
- Todo evento emitido ou escutado está documentado em `docs/especificacao.md` e comentado no
  código explicando o porquê.

### II. Servidor como única fonte da verdade (INEGOCIÁVEL)

- O estado compartilhado vive na memória do servidor; o cliente nunca o altera por conta própria.
- Todas as validações acontecem no servidor; dados enviados pelo cliente nunca são confiáveis.
- Fase da temporada, recursos e floristas são verificados antes de qualquer alteração.
- Uma recusa vai somente para quem fez o pedido e não altera o estado.
- Validar e alterar o estado acontecem sem pausa assíncrona entre os dois passos: dois pedidos
  simultâneos nunca consomem o mesmo recurso ou florista.

### III. Painel de eventos completo (INEGOCIÁVEL)

O painel mostra, para cada evento: sentido (⬆ emit ou ⬇ on), nome, horário, dados, causa e a
reação do cliente, além de contadores de quantas vezes cada evento ocorreu (obrigatório para
dupla). Essas funcionalidades nunca são removidas nem simplificadas.

### IV. Mecânicas reais da Floricultura

- Recurso primário: flores. Recurso refinado: buquês. Construções: Estufa, Ateliê e Loja.
  Trabalhadores: floristas.
- A transformação de flores em buquês e a murcha das flores são mecânicas reais, controladas
  pelo servidor e comunicadas por eventos — nunca apenas visuais nem simuladas com dados fictícios.
- Regras, números, eventos e cenários seguem a especificação aprovada (`docs/especificacao.md`).

### V. Simplicidade e kit inicial

- Arquitetura do kit do professor: servidor em Python com python-socketio e uvicorn; tela em
  Vue 3 e vila desenhada em Phaser 3, por CDN; estado em memória.
- Tecnologias, bibliotecas e a estrutura do kit não são trocadas sem justificativa técnica e
  autorização; dependências desnecessárias não são adicionadas.
- O código é simples o bastante para que as duas desenvolvedoras expliquem qualquer evento:
  quem emite, quem escuta, a causa, o que muda no estado e como os outros jogadores são avisados.

## Restrições

- Nenhuma funcionalidade fora do escopo antes dos requisitos obrigatórios estarem prontos.
- Nenhum requisito inventado que não esteja no enunciado ou na especificação aprovada.
- O contrato de eventos não muda sem atualizar a especificação antes.
- Regras de negócio nunca ficam só no cliente.
- Nenhuma funcionalidade parcial é considerada concluída.

## Fluxo de desenvolvimento

1. Consultar esta constituição, a especificação e a divisão da equipe (`docs/equipe.md`).
2. Identificar a milestone atual, suas dependências e critérios de conclusão.
3. Implementar somente o escopo da milestone.
4. Testar com duas ou mais abas e verificar que as milestones anteriores continuam funcionando.
5. Resumir o que foi feito e os testes executados.
6. Fazer **um commit por milestone**, com mensagem padronizada (`docs:`, `feat:`, `chore:`),
   pela desenvolvedora responsável e com a própria identidade Git.
7. Atualizar o acompanhamento em `docs/equipe.md` e as tarefas em `specs/001-floricultura/tasks.md`.

Regras de Git: nada de squash nem reescrita de histórico; nenhum commit com código quebrado ou
sem teste; nenhuma mensagem genérica; nenhum arquivo temporário, ambiente virtual ou segredo
versionado; nenhuma autoria simulada.

## Divisão do trabalho

- Julia Fitzlaff: servidor (`server.py`) — estado, validações, fatos, temporizadores,
  transformação e expiração.
- Eduarda de Oliveira: tela (`client/`) — interface, pedidos e escutas, painel de eventos,
  contadores e reações na vila.
- As duas evitam alterar o mesmo arquivo ao mesmo tempo e conhecem a arquitetura completa.

## Governança

Em caso de conflito, a ordem de prioridade é: (1) o enunciado do trabalho; (2) esta
constituição e a especificação aprovada (`docs/especificacao.md`); (3) as decisões de
implementação. Mudanças nesta constituição são feitas em commit próprio (`docs:`) e
registradas em `docs/equipe.md`.

**Versão**: 1.0.0 | **Ratificada**: 2026-11-01 | **Última alteração**: 2026-11-01
