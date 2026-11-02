---

description: "Tarefas da Floricultura em Tempo Real, organizadas pelas milestones de docs/equipe.md"
---

# Tarefas: Floricultura em Tempo Real

**Entrada**: `specs/001-floricultura/` e `docs/especificacao.md`

**Acompanhamento**: status, responsável e hash de cada milestone ficam em
[`docs/equipe.md`](../../docs/equipe.md). Aqui as tarefas são marcadas `[X]` no mesmo commit
da milestone que as conclui.

## Formato: `[ID] [Milestone] [História] Descrição`

- **Milestone**: ID em `docs/equipe.md` (A = servidor, Julia; B = tela, Eduarda).
- **História**: história de usuário em `spec.md` (US1 a US9).
- Partes A e B da mesma milestone mexem em arquivos diferentes e podem ser feitas em paralelo.

---

## Fase 1: Preparação

- [X] T001 [M0A] Especificação, divisão da equipe e `.gitignore` em `docs/`
- [X] T002 [M0B] Kit inicial do professor (`server.py`, `client/`, `requirements.txt`, `README.md`)
- [X] T003 [SK] Estrutura do Spec Kit: constituição, spec, plano e tarefas

---

## Fase 2: História 1 — Floricultura sincronizada (P1)

- [X] T004 [M1A] [US1] Constantes, estado inicial, lotes, `fato()`, `connect`/`disconnect` e `estado.sincronizado` em `server.py`
- [X] T005 [M1B] [US1] Escuta de `estado.sincronizado`, painel de estoques/floristas/construções e rodapé em `client/index.html`

## Fase 3: História 2 — Abertura da temporada (P1)

- [X] T006 [M2A] [US2] `recusar()` e tratador de `vila.abertura_solicitada` emitindo `vila.iniciada` em `server.py`
- [X] T007 [M2B] [US2] Pedido de abertura e escuta de `vila.iniciada` em `client/index.html`

## Fase 4: História 3 — Construções e recusas (P1)

- [X] T008 [M3A] [US3] Tratador de `construcao.solicitada` por tipo, débito pelos lotes mais antigos e `construcao.iniciada` em `server.py`
- [X] T009 [M3B] [US3] Botões Estufa/Ateliê/Loja, pedido com tipo e canteiro na vila em `client/index.html`
- [X] T010 [M4A] [US3] Validações na ordem da especificação e `operacao.recusada` só para quem pediu em `server.py`
- [X] T011 [M4B] [US3] Escuta de `operacao.recusada` com aviso vermelho e tremor em `client/index.html`

## Fase 5: História 4 — Passagem do tempo (P1)

- [X] T012 [M5A] [US4] Temporizador da colheita criando lotes e emitindo `recurso.produzido` em `server.py`
- [X] T013 [M5B] [US4] Escuta de `recurso.produzido` com "+N 🌷" na Estufa em `client/index.html`
- [X] T014 [M6A] [US4] Temporizador da obra emitindo `construcao.concluida`, liberando florista e aplicando o efeito do tipo em `server.py`
- [X] T015 [M6B] [US4] Escuta de `construcao.concluida` transformando o canteiro na construção em `client/index.html`

## Fase 6: História 5 — Montagem de buquês (P2)

- [X] T016 [M7A] [US5] Tratador de `buque.montagem_solicitada`, `buque.montagem_iniciada` e temporizador de `buque.montado` em `server.py`
- [X] T017 [M7B] [US5] Botão "Montar buquê" e escutas da montagem em `client/index.html`

## Fase 7: História 6 — Vendas na Loja (P2)

- [X] T018 [M8A] [US6] Temporizador de vendas emitindo `buque.vendido` em `server.py`
- [X] T019 [M8B] [US6] Escuta de `buque.vendido` e placar em `client/index.html`

## Fase 8: História 7 — Flores murcham (P2)

- [X] T020 [M9A] [US7] Temporizador de validade por lote emitindo `flores.murchadas` em `server.py`
- [X] T021 [M9B] [US7] Escuta de `flores.murchadas` com aviso e "🥀 −N" em `client/index.html`

## Fase 9: História 8 — Encerramento (P1)

- [X] T022 [M10A] [US8] Tratador de `vila.encerramento_solicitado`, `vila.encerrada` e revisão de concorrência em `server.py`
- [X] T023 [M10B] [US8] Pedido de encerramento e escuta de `vila.encerrada` em `client/index.html`

## Fase 10: História 9 e acabamento

- [X] T024 [M11] [US9] Contadores por evento, identidade visual e feedback revisado em `client/index.html`
- [X] T025 [M12A] README: instalação, eventos e respostas às perguntas
- [X] T026 [M12B] README: testes com três abas, declaração de uso de IA, créditos; teste final

## Fase 11: Extras (depois do escopo obrigatório)

- [X] T027 [M13] Placar (barra de status) e legenda dentro da tela do jogo em `client/index.html`

---

## Dependências e ordem

- Cada parte B depende da parte A da mesma milestone e da parte B anterior.
- Cada parte A depende da parte A anterior.
- A ordem completa e os critérios de conclusão estão em `docs/equipe.md`, seções 4 e 5.
