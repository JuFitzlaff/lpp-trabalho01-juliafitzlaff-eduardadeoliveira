# Especificação da funcionalidade: Floricultura em Tempo Real

**Branch**: `main` (sem branches de funcionalidade)

**Criada**: 2026-11-01

**Status**: Aprovada

**Fonte oficial**: [`docs/especificacao.md`](../../docs/especificacao.md) — regras, números da
temporada, tabela completa de eventos e cenários de teste. Este arquivo organiza a mesma
especificação em histórias de usuário; em caso de diferença, vale `docs/especificacao.md`.

## Cenários de usuário e testes

### História 1 — Entrar e ver a floricultura igual para todos (Prioridade: P1)

Um participante entra como Mestre ou Jogador e vê o retrato atual da floricultura: estoques,
floristas, construções e fase da temporada.

**Por que esta prioridade**: sem um estado compartilhado e sincronizado não existe jogo.

**Teste independente**: abrir duas abas, entrar nas duas e conferir que mostram os mesmos números.

**Cenários de aceitação**:

1. **Dado** que a floricultura tem 100 flores e 1 Estufa, **quando** um participante entra,
   **então** só ele recebe `estado.sincronizado` com causa `conexao` e vê esses números.
2. **Dado** que A já está dentro, **quando** B entra, **então** A não recebe nada.

---

### História 2 — O Mestre abre a temporada (Prioridade: P1)

**Por que esta prioridade**: nenhuma ação dos jogadores acontece antes da abertura.

**Teste independente**: Mestre e Jogador em abas separadas; o Mestre abre e as duas abas mudam.

**Cenários de aceitação**:

1. **Dado** a fase aguardando, **quando** o Mestre emite `vila.abertura_solicitada`, **então**
   todos recebem `vila.iniciada` e a fase passa a aberta.
2. **Dado** um Jogador ou a temporada já aberta, **quando** alguém pede a abertura, **então** só
   ele recebe `operacao.recusada`.

---

### História 3 — Construir e ser recusado quando não dá (Prioridade: P1)

Jogadores constroem Estufa, Ateliê e Loja pagando com flores (e buquês, no caso da Loja) e
ocupando um florista. Pedidos impossíveis são recusados só para quem pediu.

**Por que esta prioridade**: é o fluxo pedido → fato/recusa exigido pelo enunciado.

**Teste independente**: três abas; um Jogador constrói e todos veem o canteiro; pedidos sem
recurso, sem florista ou fora da temporada recebem a recusa só na aba de quem pediu.

**Cenários de aceitação**: Cenário 1 (recusa por falta de buquês), Cenário 3 (disputa pelo
último florista) e "Disputa pelas últimas flores" de `docs/especificacao.md`, seção 13.

---

### História 4 — O tempo passa sozinho: colheita e obras (Prioridade: P1)

As Estufas colhem flores a cada intervalo e as obras terminam sozinhas, liberando o florista.

**Por que esta prioridade**: temporizadores do servidor como fonte de eventos são obrigatórios.

**Teste independente**: abrir a temporada sem clicar em nada e ver as flores subirem em todas
as abas; construir e ver a obra terminar sozinha.

**Cenários de aceitação**: Cenário 2 (passagem do tempo) de `docs/especificacao.md`, até 25 s.

---

### História 5 — Montar buquês no Ateliê (Prioridade: P2)

Jogadores transformam 5 flores em 1 buquê no Ateliê, ocupando um florista e o Ateliê.

**Por que esta prioridade**: o recurso refinado precisa ter mecânica real.

**Teste independente**: com um Ateliê pronto, montar um buquê e ver flores caírem e o buquê
entrar no estoque de todos.

**Cenários de aceitação**: cenário complementar "Transformação" de `docs/especificacao.md`.

---

### História 6 — Vender buquês na Loja (Prioridade: P2)

Cada Loja pronta vende um buquê por ciclo, somando no placar de buquês vendidos.

**Teste independente**: com uma Loja pronta e buquês no estoque, ver o placar subir sozinho.

**Cenários de aceitação**: seção 7 de `docs/especificacao.md`.

---

### História 7 — Flores murcham (Prioridade: P2)

Cada lote de flores murcha depois do prazo se não for usado, e todos são avisados.

**Teste independente**: abrir a temporada, não usar as flores e ver o lote inicial murchar.

**Cenários de aceitação**: Cenário 2 completo (até 35 s) de `docs/especificacao.md`.

---

### História 8 — O Mestre encerra a temporada (Prioridade: P1)

**Teste independente**: encerrar com uma obra em andamento e verificar que nada mais muda.

**Cenários de aceitação**: cenário complementar "Encerramento" de `docs/especificacao.md`.

---

### História 9 — Painel de eventos com contadores (Prioridade: P1)

Cada aba mostra os eventos que emitiu e escutou, com nome, horário, dados, causa, reação e
contadores por evento.

**Teste independente**: executar o roteiro de três abas e conferir o painel de cada uma.

### Casos de borda

- Dois pedidos simultâneos pelo último florista ou pelas últimas flores: só um é aceito.
- Pedido com tipo de construção inexistente ou dados malformados: recusado.
- Lote de flores totalmente usado antes do prazo: some sem aviso de murcha.
- Participante que entra no meio da temporada: recebe o retrato atual.
- Pedidos depois do encerramento: recusados; temporizadores não alteram mais nada.

## Requisitos

### Requisitos funcionais

- **FR-001**: O sistema DEVE ter dois papéis: Mestre (abre e encerra) e Jogador (constrói e monta buquês).
- **FR-002**: O sistema DEVE manter um único estado compartilhado, decidido apenas pelo servidor.
- **FR-003**: O sistema DEVE separar pedidos dos jogadores e fatos do servidor, com a recusa como evento.
- **FR-004**: O sistema DEVE enviar recusas somente a quem fez o pedido.
- **FR-005**: O sistema DEVE produzir flores automaticamente a cada intervalo e avisar todos.
- **FR-006**: O sistema DEVE concluir obras e montagens sozinho após o tempo definido.
- **FR-007**: O sistema DEVE transformar flores em buquês e vender buquês na Loja.
- **FR-008**: O sistema DEVE fazer as flores murcharem ao fim do prazo de cada lote.
- **FR-009**: O sistema DEVE impedir que pedidos simultâneos consumam o mesmo recurso ou florista.
- **FR-010**: A tela DEVE mostrar estoques, floristas ocupados, construções, avisos, a vila desenhada
  e o painel de eventos com contadores, além dos nomes das desenvolvedoras no rodapé.

### Entidades principais

- **Temporada**: fase (aguardando, aberta, encerrada).
- **Lote de flores**: quantidade e prazo de validade; o estoque de flores é a soma dos lotes.
- **Construção**: tipo (Estufa, Ateliê, Loja), prontas e em obra.
- **Florista**: livre ou ocupado em uma obra ou montagem.
- **Participante**: nome e papel.

## Critérios de sucesso

- **SC-001**: Todas as abas mostram os mesmos números o tempo todo, sem recarregar a página.
- **SC-002**: Os três cenários obrigatórios da especificação passam com duas ou três abas.
- **SC-003**: Floristas nunca passam do limite e estoques nunca ficam negativos.
- **SC-004**: Todos os eventos da tabela aparecem no painel com causa e reação.

## Premissas

- Sem login, banco de dados ou publicação na internet (o enunciado dispensa).
- O estado volta ao início quando o servidor reinicia.
