# Equipe e acompanhamento — Vila 19: Floricultura

## 1. Integrantes

| Nome | GitHub | Foco principal |
|---|---|---|
| Julia Fitzlaff | @JuFitzlaff | Servidor (backend) |
| Eduarda de Oliveira | @eduardadeoliveira1 | Tela e vila desenhada (frontend) |

## 2. Responsabilidades

**Julia Fitzlaff — servidor (`server.py`)**
- Estado compartilhado da floricultura (lotes de flores, buquês, construções, floristas).
- Tratadores dos pedidos e todas as validações.
- Emissão dos fatos e das recusas (só para quem pediu).
- Temporizadores: colheita, obra, montagem, vendas e validade dos lotes.
- Transformação de flores em buquês e expiração das flores.
- Comentários em cada ponto de emissão e escuta no servidor.

**Eduarda de Oliveira — tela (`client/index.html` e `client/assets/`)**
- Interface Vue: estoques, floristas, construções, botões e avisos.
- Pedidos (`pedir`) e escutas (`ouvir`) de cada evento, com a frase de reação.
- Painel de eventos e contadores por evento (obrigatório para dupla).
- Reações visuais na vila desenhada (Phaser), incluindo novos métodos da cena.
- Identidade visual da Floricultura e rodapé com os nomes.
- Comentários em cada ponto de emissão e escuta no cliente.

**Ambas**
- Conhecem a arquitetura completa e sabem explicar qualquer evento: quem emite, quem escuta,
  a causa e o que muda.
- Revisam a milestone da colega antes de começar a própria parte da milestone seguinte.

## 3. Regras de trabalho

1. **Arquivos por responsável.** Julia altera `server.py`; Eduarda altera `client/`. Nenhuma das duas
   altera o arquivo da outra sem combinar antes.
2. **Contrato de eventos.** Nomes, dados e causas seguem `docs/especificacao.md`. Mudou o contrato?
   Primeiro atualiza a especificação (em commit próprio `docs:`), depois o código.
3. **Um commit por milestone**, feito por quem é responsável por ela, com a própria identidade Git.
   Antes de cada commit, a responsável confere `git config user.name` e `git config user.email`
   neste repositório. Nada de squash, reescrita de histórico ou autoria trocada.
4. **Parte A e parte B.** Milestones com servidor e tela são divididas em **A (Julia)** e **B (Eduarda)**.
   Como os arquivos são diferentes, A e B podem ser feitas em paralelo seguindo o contrato; o commit
   B é feito depois do A, porque é testado com o servidor real.
5. **Hash do commit.** Um commit não conhece o próprio hash. Cada desenvolvedora preenche o hash da
   sua milestone anterior no commit da milestone seguinte (as últimas são preenchidas em M12).
6. **Status:** `pendente` → `em andamento` → `concluída`. Cada uma atualiza apenas as suas linhas.
7. **Spec Kit.** Os princípios do projeto estão em `.specify/memory/constitution.md` e as tarefas em
   `specs/001-floricultura/tasks.md`. No commit de cada milestone, a responsável também marca `[X]`
   nas tarefas que concluiu.

### Como testar uma parte A (só servidor) antes da tela existir

Com o servidor rodando, abra `http://localhost:8000`, abra o console do navegador (F12) e rode:

```js
const s = io({ auth: { nome: "Teste", papel: "jogador" } });   // ou papel: "mestre"
s.onAny((evento, dados) => console.log(evento, dados));         // mostra todo fato recebido
s.emit("construcao.solicitada", { tipo: "estufa" });            // envia um pedido
```

Abrindo duas abas com esse roteiro dá para verificar quem recebe cada evento (todos ou só quem pediu).

## 4. Milestones

| ID | Milestone | Responsável | Depende de | Status | Commit |
|---|---|---|---|---|---|
| M0A | Especificação e divisão da equipe | Julia | — | concluída | `370fd2c` |
| M0B | Kit inicial do professor (sem alterações) | Eduarda | M0A | concluída | `68b3932` |
| M1A | Estado inicial e `estado.sincronizado` no servidor | Julia | M0B | concluída | `2c7e1ad` |
| M1B | Tela da floricultura sincronizada + rodapé | Eduarda | M1A | concluída | `b1438b7` |
| M2A | Abertura da temporada no servidor | Julia | M1A | concluída | `01c563d` |
| M2B | Botão do Mestre e reação a `vila.iniciada` | Eduarda | M2A, M1B | concluída | `7db04e9` |
| M3A | Construção das três construções no servidor | Julia | M2A | concluída | `3ee2dc9` |
| M3B | Botões de construção e canteiro na vila | Eduarda | M3A, M2B | concluída | `f3c4019` |
| M4A | Validações e `operacao.recusada` | Julia | M3A | concluída | `854d3a9` |
| M4B | Reação à recusa (aviso e tremor) | Eduarda | M4A, M3B | concluída | `70ac610` |
| M5A | Colheita automática por temporizador | Julia | M4A | concluída | `d0d26cb` |
| M5B | Reação à colheita | Eduarda | M5A, M4B | concluída | `b9f95ee` |
| SK | Estrutura do Spec Kit (constituição, spec, plano, tarefas) | Julia | M5B | concluída | `6bff7ef` |
| M6A | Conclusão das obras por temporizador | Julia | M5A | concluída | `8411495` |
| M6B | Construção pronta na vila | Eduarda | M6A, M5B | concluída | `4e9897e` |
| M7A | Montagem de buquês no Ateliê | Julia | M6A | concluída | `981e3a7` |
| M7B | Botão e reações da montagem | Eduarda | M7A, M6B | concluída | `b939a90` |
| M8A | Vendas automáticas na Loja | Julia | M7A | concluída | `47a07f0` |
| M8B | Reação às vendas e placar | Eduarda | M8A, M7B | concluída | `39f9d33` |
| M9A | Validade dos lotes e murcha | Julia | M8A | concluída | `177bf81` |
| M9B | Reação às flores murchas | Eduarda | M9A, M8B | concluída | `3b0ac7c` |
| M10A | Encerramento e revisão de concorrência | Julia | M9A | concluída | `6350b8b` |
| M10B | Botão de encerrar e vila encerrada | Eduarda | M10A, M9B | concluída | `c0fe25e` |
| M11 | Identidade visual, contadores e painel completo | Eduarda | M10B | concluída | `92aa5c8` |
| M12A | README: instalação, eventos e respostas | Julia | M11 | concluída | `0197204` |
| M12B | README: testes, IA e créditos + teste final com 3 abas | Eduarda | M12A | concluída | último commit do histórico |

## 5. Detalhamento

### M0A — Especificação e divisão da equipe · Julia
- **Escopo:** `docs/especificacao.md`, `docs/equipe.md` e `.gitignore` (do kit, acrescido de
  `docs/implementacao/`, materiais de apoio que não entram no repositório). Nenhum código.
- **Conclusão:** primeiro commit do repositório; contém regras, números, tabela de eventos e cenários.
- **Commit:** `docs: define especificacao da floricultura`

### M0B — Kit inicial · Eduarda
- **Escopo:** `server.py`, `client/`, `requirements.txt`, `README.md` exatamente como vieram no kit
  (o `.gitignore` já entrou em M0A).
- **Teste:** `uvicorn server:app --reload`, abrir `http://localhost:8000`, entrar como Jogador: vila vazia,
  faixa "Aguardando o Mestre", painel sem eventos.
- **Commit:** `chore: adiciona kit inicial e esqueleto do servidor`

### M1A — Estado inicial e sincronização · Julia
- **Escopo:** constantes da tabela 10, estado (com lote inicial de 100 flores e 1 Estufa pronta),
  registro de participantes, função `fato(causa, ...)`, `connect`/`disconnect`, emissão de
  `estado.sincronizado` só para quem entrou.
- **Conclusão:** duas abas conectadas recebem `estado.sincronizado` com causa `conexao`; a primeira
  aba não recebe nada quando a segunda entra.
- **Teste:** roteiro do console em duas abas.
- **Commit:** `feat: implementa estado inicial e sincronizacao no servidor`

### M1B — Tela sincronizada · Eduarda
- **Escopo:** `ouvir("estado.sincronizado")`; painel com flores, buquês, vendidos, floristas x/3 com barra,
  construções por tipo; vila desenha a Estufa inicial; nomes das desenvolvedoras no rodapé.
- **Conclusão:** duas abas mostram os mesmos números; painel mostra `⬇ on estado.sincronizado` com causa e reação.
- **Commit:** `feat: exibe estado sincronizado da floricultura`

### M2A — Abertura da temporada · Julia
- **Escopo:** `recusar(sid, motivo, causa)`; tratador de `vila.abertura_solicitada` (papel e fase);
  emissão de `vila.iniciada` para todos.
- **Conclusão:** Mestre abre → todos recebem `vila.iniciada`; Jogador tentando abrir e segunda abertura
  recebem `operacao.recusada` só para si (visível no console).
- **Commit:** `feat: implementa abertura da temporada no servidor`

### M2B — Abertura na tela · Eduarda
- **Escopo:** `pedir("vila.abertura_solicitada")`; `ouvir("vila.iniciada")` → aviso e `jogo.vilaIniciada()`.
- **Conclusão:** com Mestre e Jogador abertos, a faixa muda nas duas abas sem recarregar; só o Mestre vê o `⬆ emit`.
- **Commit:** `feat: implementa abertura da temporada na tela`

### M3A — Construções · Julia
- **Escopo:** tratador de `construcao.solicitada` com `tipo` (estufa, atelie, loja); débito do custo
  (flores mais antigas primeiro, e buquês da Loja); ocupa florista; soma obra do tipo;
  emite `construcao.iniciada` com tipo e quem pediu.
- **Fora do escopo:** validações (M4A) e fim da obra (M6A). Sem validação, os números podem ficar
  negativos — comportamento esperado nesta etapa, como no guia.
- **Conclusão:** cada tipo debita o custo correto e todos recebem o fato.
- **Commit:** `feat: implementa construcoes da floricultura no servidor`

### M3B — Construções na tela · Eduarda
- **Escopo:** três botões (Estufa, Ateliê, Loja) com custo; `pedir("construcao.solicitada", { tipo })`;
  `ouvir("construcao.iniciada")` → aviso e canteiro na vila com o ícone do tipo.
- **Conclusão:** o clique de um Jogador atualiza flores e floristas em todas as abas e aparece o canteiro.
- **Commit:** `feat: implementa pedido de construcao na tela`

### M4A — Validações · Julia
- **Escopo:** ordem de verificações da seção 11 da especificação para construir; validação do `tipo`
  recebido; papel Jogador; tudo validado e alterado **sem pausa (await) entre verificar e alterar**.
- **Conclusão:** cada motivo de recusa reproduzido; recusa só para quem pediu; nunca passa de 3/3
  floristas nem fica com estoque negativo.
- **Commit:** `feat: implementa validacao de recursos e floristas`

### M4B — Recusa na tela · Eduarda
- **Escopo:** `ouvir("operacao.recusada")` → aviso vermelho e `jogo.recusado(motivo)`.
- **Conclusão:** recusa aparece em vermelho no painel e a vila treme só na aba de quem pediu.
- **Commit:** `feat: exibe recusas para quem fez o pedido`

### M5A — Colheita automática · Julia
- **Escopo:** temporizador de colheita iniciado na abertura; a cada 5 s cria lote de 10 × Estufas;
  emite `recurso.produzido` com causa `temporizador da colheita`.
- **Conclusão:** flores sobem sozinhas em todas as abas; colheita só com temporada aberta.
- **Commit:** `feat: implementa producao automatica de flores`

### M5B — Colheita na tela · Eduarda
- **Escopo:** `ouvir("recurso.produzido")` → atualiza e `jogo.recursoProduzido(...)` com "+N 🌷"; filtro
  "ocultar recurso.produzido" continua funcionando.
- **Commit:** `feat: exibe colheita automatica de flores`

### SK — Estrutura do Spec Kit · Julia
- **Escopo:** `.specify/` (constituição com os princípios do projeto, templates e scripts oficiais do
  GitHub Spec Kit) e `specs/001-floricultura/` (`spec.md`, `plan.md`, `tasks.md`). A especificação
  oficial continua sendo `docs/especificacao.md`; os arquivos do Spec Kit apontam para ela.
- **Conclusão:** constituição sem placeholders; spec, plano e tarefas coerentes com a especificação
  e com esta tabela; tarefas das milestones já concluídas marcadas.
- **Commit:** `docs: adiciona estrutura do spec kit`

### M6A — Conclusão das obras · Julia
- **Escopo:** temporizador de obra (10 s) iniciado junto com `construcao.iniciada`; emite
  `construcao.concluida`; libera florista; aplica efeito do tipo (Estufa +10 por colheita).
- **Conclusão:** cenário 2 da especificação reproduzido até o instante 25 s.
- **Commit:** `feat: implementa conclusao das obras por temporizador`

### M6B — Construção pronta na tela · Eduarda
- **Escopo:** `ouvir("construcao.concluida")` → aviso e canteiro vira construção com ícone do tipo.
- **Commit:** `feat: exibe construcoes concluidas na vila`

### M7A — Montagem de buquês · Julia
- **Escopo:** tratador de `buque.montagem_solicitada` com as verificações da seção 6; emite
  `buque.montagem_iniciada`; temporizador de 6 s emite `buque.montado`.
- **Conclusão:** cenário complementar "Transformação" reproduzido; Loja passa a poder ser construída.
- **Commit:** `feat: implementa transformacao de flores em buques`

### M7B — Montagem na tela · Eduarda
- **Escopo:** botão "Montar buquê (5 🌷)"; escutas de `buque.montagem_iniciada` e `buque.montado`;
  novos métodos na cena para "−5 🌷" e "+1 💐" no Ateliê.
- **Commit:** `feat: exibe montagem de buques na tela`

### M8A — Vendas na Loja · Julia
- **Escopo:** temporizador de vendas (10 s) iniciado na abertura; vende 1 buquê por Loja pronta;
  emite `buque.vendido` só quando há venda.
- **Conclusão:** com Loja pronta e buquês no estoque, buquês caem e vendidos sobem em todas as abas.
- **Commit:** `feat: implementa vendas de buques na loja`

### M8B — Vendas na tela · Eduarda
- **Escopo:** `ouvir("buque.vendido")`; placar de buquês vendidos; reação na vila.
- **Commit:** `feat: exibe vendas e placar de buques`

### M9A — Murcha das flores · Julia
- **Escopo:** temporizador de validade por lote (30 s; o lote inicial começa na abertura); remove o
  restante do lote; emite `flores.murchadas` só quando restou flor.
- **Conclusão:** cenário 2 completo (até 35 s) reproduzido.
- **Commit:** `feat: implementa expiracao de flores`

### M9B — Murcha na tela · Eduarda
- **Escopo:** `ouvir("flores.murchadas")` → aviso e "🥀 −N" na vila; opção de ocultar eventos frequentes.
- **Commit:** `feat: exibe flores murchas para todos`

### M10A — Encerramento · Julia
- **Escopo:** tratador de `vila.encerramento_solicitado`; emite `vila.encerrada`; todos os temporizadores
  conferem a fase antes de alterar o estado; revisão de que nenhum tratador tem pausa entre validar e alterar.
- **Conclusão:** cenários 3 e "Encerramento" reproduzidos com três abas.
- **Commit:** `feat: implementa encerramento da temporada`

### M10B — Encerramento na tela · Eduarda
- **Escopo:** `pedir("vila.encerramento_solicitado")`; `ouvir("vila.encerrada")` → aviso com total vendido e
  `jogo.vilaEncerrada()`.
- **Commit:** `feat: exibe encerramento da temporada`

### M11 — Interface e painel · Eduarda
- **Escopo:** contadores por evento no painel; identidade visual da Floricultura (textos, emojis, cores);
  feedback de sucesso, recusa, conclusão e murcha revisados; mapa adaptado no Tiled (opcional).
- **Conclusão:** todos os 15 eventos aparecem no painel com emit/on, causa, dados e reação, e com contador.
- **Commit:** `feat: finaliza interface e contadores do painel`

### M12A — README (parte 1) · Julia
- **Escopo:** descrição, integrantes com @, tecnologias, instalação e execução, eventos emitidos e escutados,
  respostas às três perguntas.
- **Commit:** `docs: documenta instalacao e eventos no readme`

### M12B — README (parte 2) e teste final · Eduarda
- **Escopo:** como testar com três abas (Mestre, Jogador A, Jogador B), declaração de uso de IA, créditos;
  checklist de entrega conferido.
- **Commit:** `docs: documenta testes e uso de ia no readme`

## 6. Roteiro do teste final (três abas)

Aba 1 Mestre · Aba 2 Jogador A · Aba 3 Jogador B.

- [X] Sincronização: as três abas mostram os mesmos números o tempo todo.
- [X] Recusas individuais antes da abertura e com a temporada aberta.
- [X] Colheita automática a cada 5 s.
- [X] Construção simultânea por A e B.
- [X] Limite de 3 floristas e disputa pelo último florista.
- [X] Disputa pelas últimas flores.
- [X] Transformação de flores em buquês e Ateliê ocupado.
- [X] Construção da Loja e vendas automáticas.
- [X] Murcha de flores após 30 s.
- [X] Encerramento: nada mais muda e todo pedido é recusado.
- [X] Contadores por evento e rodapé com os nomes.
