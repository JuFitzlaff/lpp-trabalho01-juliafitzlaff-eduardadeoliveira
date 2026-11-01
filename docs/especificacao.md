# Especificação — Vila em Tempo Real

**Integrantes:**
- Julia Fitzlaff (@JuFitzlaff)
- Eduarda de Oliveira (@eduardadeoliveira1)

**Tipo de vila (sorteio):** Vila 19 — Floricultura

---

## 1. A Floricultura

Vários jogadores cuidam juntos da mesma floricultura durante uma **temporada**.
As **Estufas** colhem flores sozinhas, de tempos em tempos. Os **floristas** erguem novas
construções e, no **Ateliê**, transformam flores em **buquês**. A **Loja** vende os buquês
prontos. Flores são frágeis: cada colheita tem prazo e, se não for usada a tempo,
**murcha** e sai do estoque.

O **Mestre** abre e encerra a temporada. Os **Jogadores** constroem e montam buquês.
Quem decide tudo é o servidor: os jogadores apenas pedem e acompanham os fatos.

O objetivo cooperativo é **vender o maior número de buquês** até o Mestre encerrar a temporada.

## 2. Recursos

| Recurso | Tipo | Como entra no estoque | Como sai do estoque |
|---|---|---|---|
| 🌷 Flores | primário | colheita automática das Estufas | pagamento de construções, montagem de buquês, murcha |
| 💐 Buquês | refinado | montagem no Ateliê (5 flores → 1 buquê) | pagamento da Loja, venda automática na Loja |
| 🧾 Buquês vendidos | placar | venda automática na Loja | nunca diminui |

**Lotes de flores.** As flores do estoque são guardadas em **lotes**: cada colheita gera um
lote novo, com a quantidade colhida e o seu prazo de validade. O estoque de flores é a soma
dos lotes. Sempre que flores são gastas, **as mais antigas são usadas primeiro** (as que estão
mais perto de murchar).

## 3. Construções

| Construção | Para que serve | Efeito ao ficar pronta |
|---|---|---|
| 🌱 Estufa | colhe flores automaticamente | +10 flores por colheita |
| ✂️ Ateliê | local onde os floristas montam buquês | +1 montagem simultânea possível |
| 🏪 Loja | vende os buquês ao público | +1 buquê vendido por ciclo de vendas |

A floricultura **começa com 1 Estufa pronta**. Ateliês e Lojas precisam ser construídos.

## 4. Floristas (trabalhadores)

- A floricultura tem **3 floristas** (limite fixo durante toda a temporada).
- Cada **obra** ocupa 1 florista até terminar.
- Cada **montagem de buquê** ocupa 1 florista até terminar.
- A colheita e a venda são automáticas e **não** ocupam floristas.
- Um pedido que precise de florista quando os 3 estão ocupados é recusado.

## 5. Regras de produção (colheita)

- A colheita só acontece com a temporada **aberta**.
- A cada **5 segundos** o servidor colhe **10 flores por Estufa pronta**.
- Cada colheita cria um **lote novo** e começa a contar o prazo de validade desse lote.
- Com 1 Estufa: 10 flores a cada 5 s (120 por minuto). Cada Estufa nova soma +10 por colheita.
- Todos os jogadores são avisados de cada colheita.

## 6. Transformação: flores → buquês (Ateliê)

- Um Jogador pede a **montagem de um buquê**.
- Condições (todas verificadas pelo servidor):
  - temporada aberta;
  - quem pediu é Jogador;
  - existe pelo menos 1 Ateliê pronto;
  - há um Ateliê livre (montagens em andamento < Ateliês prontos);
  - há pelo menos **5 flores** no estoque;
  - há pelo menos 1 florista livre.
- Pedido aceito: saem **5 flores** (as mais antigas primeiro), **1 florista** e **1 Ateliê** ficam
  ocupados e a montagem começa. Todos são avisados.
- Após **6 segundos**, a montagem termina sozinha: entra **1 buquê** no estoque, o florista e o
  Ateliê ficam livres. Todos são avisados.

## 7. Comercialização (Loja)

- Com a temporada aberta, a cada **10 segundos** cada Loja pronta vende **1 buquê**, se houver.
- Vendas do mesmo ciclo são somadas: com 2 Lojas e 5 buquês, saem 2 buquês.
- Se nenhum buquê for vendido no ciclo (sem Loja ou sem buquê), nada é anunciado.
- Buquês vendidos saem do estoque e somam no placar **buquês vendidos**.

## 8. Expiração: flores murcham

- Cada lote de flores tem validade de **30 segundos** a partir da colheita.
- O lote inicial (100 flores) começa a contar o prazo **no momento em que a temporada é aberta**.
- Ao fim do prazo, as flores que **restarem** daquele lote murcham e saem do estoque.
  Todos os jogadores são avisados de quantas flores murcharam.
- Se o lote já tiver sido totalmente usado, ele apenas some, sem aviso.
- A murcha só acontece com a temporada aberta.

## 9. Temporada

| Fase | Como se chega | O que é permitido |
|---|---|---|
| aguardando | início do servidor | nada além de entrar e o Mestre abrir |
| aberta | Mestre abre a temporada | construir, montar buquês; colheita, vendas e murcha acontecem |
| encerrada | Mestre encerra a temporada | nada; todos os pedidos são recusados |

Ao encerrar:
- colheita, vendas e murcha **param**;
- obras e montagens em andamento **não terminam** (a floricultura fica congelada como está);
- o placar final de buquês vendidos é anunciado a todos.

## 10. Números da temporada

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Flores iniciais | 100 (1 lote) | permite as primeiras obras logo após a abertura |
| Buquês iniciais | 0 | buquês só existem depois do Ateliê |
| Estufas prontas no início | 1 | a colheita precisa existir desde a abertura |
| Limite de floristas | 3 | pequeno o bastante para testar o limite e a disputa com poucos cliques |
| Intervalo de colheita | 5 s | efeito visível rapidamente nos testes |
| Flores por Estufa por colheita | 10 | uma Estufa nova se paga em 3 colheitas (15 s) |
| Validade de um lote | 30 s | 6 colheitas: dá tempo de usar, mas pressiona os jogadores |
| Tempo de obra (todas as construções) | 10 s | tempo único: a primeira obra iniciada é sempre a primeira a terminar |
| Custo da Estufa | 30 flores | a mais barata: acelera a colheita |
| Custo do Ateliê | 50 flores | libera o recurso refinado |
| Custo da Loja | 40 flores + 2 buquês | exige o recurso refinado: só depois do Ateliê |
| Montagem de buquê | 5 flores → 1 buquê, 6 s, 1 florista, 1 Ateliê | transforma flores antes que murchem |
| Ciclo de vendas | 10 s, 1 buquê por Loja | a Loja consome buquês em ritmo menor do que o Ateliê produz |

## 11. Motivos de recusa

As verificações são feitas na ordem abaixo; o primeiro motivo encontrado é o informado.

**Construir:** temporada não aberta → não é Jogador → tipo de construção inválido →
flores insuficientes → buquês insuficientes → nenhum florista livre.

**Montar buquê:** temporada não aberta → não é Jogador → nenhum Ateliê pronto →
todos os Ateliês ocupados → flores insuficientes → nenhum florista livre.

**Abrir temporada:** não é Mestre → temporada já foi aberta.

**Encerrar temporada:** não é Mestre → temporada não está aberta.

| Motivo (texto mostrado) |
|---|
| A temporada não está aberta |
| A temporada já foi aberta |
| Só o Mestre pode abrir a temporada |
| Só o Mestre pode encerrar a temporada |
| Só jogadores podem construir |
| Só jogadores podem montar buquês |
| Tipo de construção inválido |
| Flores insuficientes |
| Buquês insuficientes |
| Nenhum florista livre |
| Nenhum ateliê pronto |
| Todos os ateliês estão ocupados |

Uma recusa **nunca** altera a floricultura e é enviada **somente** a quem fez o pedido.

## 12. Eventos

**Padrão de nomes:** `objeto.acao_solicitada` para pedidos dos jogadores e
`objeto.acao_no_passado` para fatos confirmados pelo servidor.

**Retrato da floricultura** (enviado em todos os fatos): fase, flores, buquês, buquês vendidos,
floristas ocupados e limite, construções prontas e em obra por tipo, montagens em andamento,
flores por colheita, além dos custos e tempos da tabela 10.

**Causa:** todo fato informa o que o gerou — o pedido aceito (por exemplo
`construcao.solicitada`) ou o temporizador (por exemplo `temporizador da colheita`).

| Evento | Emite | Recebe | Causa | Dados | O que acontece no servidor | O que muda na tela |
|---|---|---|---|---|---|---|
| `estado.sincronizado` | Servidor | Só quem entrou | entrada do participante | retrato, causa | registra o participante (nome e papel); a floricultura não muda | mostra o retrato atual: estoques, floristas, construções prontas e obras em andamento, faixa da fase |
| `vila.abertura_solicitada` | Mestre | Servidor | clique em "Abrir temporada" | — | é um pedido: verifica papel e fase | registra o pedido no painel |
| `vila.iniciada` | Servidor | Todos | `vila.abertura_solicitada` aceito | retrato, causa | fase passa a **aberta**; começam a colheita, as vendas e o prazo do lote inicial | faixa "Temporada aberta" e aviso de início |
| `construcao.solicitada` | Jogador | Servidor | clique em construir Estufa, Ateliê ou Loja | tipo | é um pedido: verifica fase, papel, tipo, flores, buquês e floristas | registra o pedido no painel |
| `construcao.iniciada` | Servidor | Todos | `construcao.solicitada` aceito | retrato, causa, tipo, quem pediu | debita o custo (flores mais antigas primeiro), ocupa 1 florista, soma 1 obra do tipo e marca o fim da obra para daqui a 10 s | canteiro com barra de progresso, "−N 🌷", aviso "Fulano iniciou uma Estufa" |
| `operacao.recusada` | Servidor | Só quem pediu | qualquer pedido que não passou nas verificações | motivo, causa (o pedido recusado) | nada muda | aviso vermelho com o motivo e a vila treme, só para quem pediu |
| `recurso.produzido` | Servidor | Todos | temporizador da colheita (a cada 5 s) | retrato, causa, quantidade colhida | cria um lote com 10 flores por Estufa pronta e marca o prazo desse lote para daqui a 30 s | flores sobem e "+N 🌷" sobe da Estufa |
| `construcao.concluida` | Servidor | Todos | temporizador da obra iniciado por `construcao.iniciada` | retrato, causa, tipo, quem pediu | tira 1 obra do tipo, soma 1 construção pronta, libera o florista e aplica o efeito do tipo (tabela 3) | canteiro vira a construção com o ícone do tipo e aviso de obra concluída |
| `buque.montagem_solicitada` | Jogador | Servidor | clique em "Montar buquê" | — | é um pedido: verifica fase, papel, Ateliê, flores e floristas | registra o pedido no painel |
| `buque.montagem_iniciada` | Servidor | Todos | `buque.montagem_solicitada` aceito | retrato, causa, quem pediu | debita 5 flores (mais antigas primeiro), ocupa 1 florista e 1 Ateliê e marca o fim da montagem para daqui a 6 s | "−5 🌷" no Ateliê e aviso "Fulano começou um buquê" |
| `buque.montado` | Servidor | Todos | temporizador da montagem iniciado por `buque.montagem_iniciada` | retrato, causa, quem pediu | soma 1 buquê, libera o florista e o Ateliê | "+1 💐" no Ateliê e aviso de buquê pronto |
| `buque.vendido` | Servidor | Todos | temporizador de vendas (a cada 10 s), só quando houve venda | retrato, causa, quantidade vendida | tira os buquês vendidos do estoque e soma no placar | "−N 💐" na Loja e placar de vendidos atualizado |
| `flores.murchadas` | Servidor | Todos | temporizador de validade de um lote (30 s após a colheita) | retrato, causa, quantidade murcha, lote | remove do estoque as flores que restaram do lote | flores caem, "🥀 −N" e aviso de flores murchas |
| `vila.encerramento_solicitado` | Mestre | Servidor | clique em "Encerrar temporada" | — | é um pedido: verifica papel e fase | registra o pedido no painel |
| `vila.encerrada` | Servidor | Todos | `vila.encerramento_solicitado` aceito | retrato, causa | fase passa a **encerrada**; colheita, vendas e murcha param; obras e montagens não terminam | faixa "Temporada encerrada", vila escurece, aviso com o total de buquês vendidos |

### Correspondência com os sete eventos mínimos

Os sete eventos mínimos do enunciado foram mantidos com o **mesmo nome**:
`vila.iniciada`, `construcao.solicitada`, `construcao.iniciada`, `operacao.recusada`,
`recurso.produzido` (o recurso é a flor), `construcao.concluida` e `vila.encerrada`.

Eventos acrescentados para a Floricultura: `estado.sincronizado`, `vila.abertura_solicitada`,
`vila.encerramento_solicitado` (pedidos do Mestre), `buque.montagem_solicitada`,
`buque.montagem_iniciada`, `buque.montado` (transformação), `buque.vendido` (comercialização)
e `flores.murchadas` (expiração).

## 13. Cenários de teste (Dado / Quando / Então)

### Cenário 1 — Recusa (falta do recurso refinado)

**Dado** que a temporada está aberta, há 100 flores, 0 buquês e 0 de 3 floristas ocupados,
**quando** o Jogador A emite `construcao.solicitada` com tipo Loja,
**então** o servidor emite `operacao.recusada` com motivo "Buquês insuficientes" e causa
`construcao.solicitada` **apenas para o Jogador A**; o estoque continua com 100 flores e 0 buquês,
os floristas continuam 0/3, e o Mestre e o Jogador B não recebem nenhum evento.

### Cenário 2 — Passagem do tempo (colheita, obra e murcha)

**Dado** que o Mestre emitiu `vila.abertura_solicitada` no instante 0 s, todos receberam
`vila.iniciada`, há 100 flores no lote 1, 1 Estufa pronta e ninguém mais age, exceto:
**quando** o Jogador A emite `construcao.solicitada` com tipo Estufa no instante 2 s,
**então**:

| Instante | Evento (para todos) | Causa | Flores |
|---|---|---|---|
| 2 s | `construcao.iniciada` (Estufa, −30 do lote 1) | `construcao.solicitada` | 70 |
| 5 s | `recurso.produzido` (+10, lote 2) | temporizador da colheita | 80 |
| 10 s | `recurso.produzido` (+10, lote 3) | temporizador da colheita | 90 |
| 12 s | `construcao.concluida` (Estufa; agora 2 Estufas, 20 por colheita; floristas 0/3) | temporizador da obra | 90 |
| 15 s | `recurso.produzido` (+20, lote 4) | temporizador da colheita | 110 |
| 20 s | `recurso.produzido` (+20, lote 5) | temporizador da colheita | 130 |
| 25 s | `recurso.produzido` (+20, lote 6) | temporizador da colheita | 150 |
| 30 s | `recurso.produzido` (+20, lote 7) | temporizador da colheita | 170 |
| 30 s | `flores.murchadas` (70 restantes do lote 1) | temporizador de validade | 100 |
| 35 s | `flores.murchadas` (10 do lote 2) e `recurso.produzido` (+20) | temporizadores | 110 |

Nenhum jogador clicou entre 2 s e 35 s: todos esses eventos foram gerados pelos temporizadores
do servidor e chegaram a todos ao mesmo tempo.

### Cenário 3 — Disputa pelo último florista

**Dado** que a temporada está aberta, há 100 flores e 2 de 3 floristas ocupados,
**quando** os Jogadores A e B emitem `construcao.solicitada` com tipo Estufa ao mesmo tempo,
**então** o servidor trata um pedido de cada vez: emite `construcao.iniciada` para todos com
o nome de quem chegou primeiro (floristas 3/3, flores 70) e `operacao.recusada` com motivo
"Nenhum florista livre" **apenas** para o outro jogador. Os floristas nunca passam de 3/3 e o
custo é debitado uma única vez.

### Cenários complementares

**Disputa pelas últimas flores.** Dado que a temporada está aberta, há 35 flores e 0 de 3 floristas
ocupados, quando A e B emitem `construcao.solicitada` com tipo Estufa ao mesmo tempo, então
apenas um recebe `construcao.iniciada` (flores 5) e o outro recebe `operacao.recusada` com
"Flores insuficientes". As flores nunca ficam negativas.

**Transformação.** Dado que a temporada está aberta, há 1 Ateliê pronto, 40 flores e 0 de 3
floristas ocupados, quando o Jogador A emite `buque.montagem_solicitada`, então todos recebem
`buque.montagem_iniciada` (flores 35, floristas 1/3); se o Jogador B emitir
`buque.montagem_solicitada` antes do fim, recebe sozinho `operacao.recusada` com "Todos os
ateliês estão ocupados"; 6 s depois todos recebem `buque.montado` (buquês 1, floristas 0/3).

**Encerramento.** Dado que a temporada está aberta com uma obra em andamento, quando o Mestre
emite `vila.encerramento_solicitado`, então todos recebem `vila.encerrada`; a partir daí nenhum
`recurso.produzido`, `buque.vendido`, `flores.murchadas` ou `construcao.concluida` é emitido, e
qualquer `construcao.solicitada` recebe `operacao.recusada` com "A temporada não está aberta".
