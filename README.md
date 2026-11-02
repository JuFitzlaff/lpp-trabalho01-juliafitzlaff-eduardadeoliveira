# Vila em Tempo Real — Vila 19: Floricultura

Aplicação web multiplayer em tempo real, feita para o Trabalho 01 de Linguagem de Programação e
Paradigmas (2026/2). Vários jogadores cuidam juntos da mesma floricultura: as **Estufas** colhem
flores sozinhas, os **floristas** constroem e, no **Ateliê**, transformam flores em **buquês**, que a
**Loja** vende automaticamente. As flores **murcham** se não forem usadas a tempo. O **Mestre** abre e
encerra a temporada. O servidor decide tudo e avisa todos os jogadores por eventos, sem recarregar a página.

## Integrantes

- Julia Fitzlaff — [@JuFitzlaff](https://github.com/JuFitzlaff) — servidor
- Eduarda de Oliveira — [@eduardadeoliveira1](https://github.com/eduardadeoliveira1) — tela e vila desenhada

## Tecnologias

| Parte | Tecnologia |
|---|---|
| Servidor | Python 3, [python-socketio](https://python-socketio.readthedocs.io/) e uvicorn |
| Comunicação em tempo real | Socket.IO |
| Tela | Vue 3 (por CDN) |
| Vila desenhada | Phaser 3 (por CDN), com o mapa do Kit Inicial |
| Estado | memória do servidor (sem banco de dados) |

## Como instalar e executar

Pré-requisitos: Python 3 e acesso à internet (Vue, Socket.IO e Phaser são carregados por CDN).

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
source .venv/bin/activate         # Linux ou macOS
pip install -r requirements.txt
uvicorn server:app --reload
```

Abra **http://localhost:8000** no navegador (não abra o arquivo direto pelo `file://`).
O estado fica na memória do servidor: ao reiniciar o servidor, a floricultura volta ao início.

## Documentação do projeto

| Arquivo | Conteúdo |
|---|---|
| [`docs/especificacao.md`](docs/especificacao.md) | regras, números, tabela completa de eventos e cenários de teste (escrita antes do código) |
| [`docs/equipe.md`](docs/equipe.md) | divisão do trabalho, milestones, responsáveis e commits |
| [`specs/001-floricultura/`](specs/001-floricultura/) | especificação, plano e tarefas no formato do GitHub Spec Kit |
| [`.specify/memory/constitution.md`](.specify/memory/constitution.md) | princípios do projeto (Spec Kit) |

## Regras da Floricultura (resumo)

| Item | Valor |
|---|---|
| Início | 100 flores, 0 buquês, 1 Estufa pronta, 3 floristas |
| Colheita | a cada 5 s, 10 flores por Estufa pronta (cada colheita é um lote) |
| Murcha | cada lote murcha 30 s depois da colheita; as flores mais antigas são usadas primeiro |
| Estufa / Ateliê / Loja | 30 flores / 50 flores / 40 flores + 2 buquês; 10 s de obra; 1 florista |
| Montagem no Ateliê | 5 flores → 1 buquê em 6 s, com 1 florista e 1 Ateliê livre |
| Vendas | a cada 10 s, cada Loja vende 1 buquê, se houver |

Detalhes e justificativas em [`docs/especificacao.md`](docs/especificacao.md).

## Eventos

Padrão de nomes: `objeto.acao_solicitada` para **pedidos** do cliente e `objeto.acao_no_passado` para
**fatos** confirmados pelo servidor.

### O cliente emite (pedidos) e o servidor escuta

| Evento | Quem pede | Tratador no servidor |
|---|---|---|
| `vila.abertura_solicitada` | Mestre | `abrir_vila` |
| `construcao.solicitada` (com `tipo`) | Jogador | `construir` |
| `buque.montagem_solicitada` | Jogador | `montar_buque` |
| `vila.encerramento_solicitado` | Mestre | `encerrar_vila` |

### O servidor emite (fatos e recusas) e o cliente escuta

| Evento | Para quem | Causa | Onde é emitido |
|---|---|---|---|
| `estado.sincronizado` | só quem entrou | conexão | `connect` |
| `vila.iniciada` | todos | `vila.abertura_solicitada` aceito | `abrir_vila` |
| `construcao.iniciada` | todos | `construcao.solicitada` aceito | `construir` |
| `operacao.recusada` | só quem pediu | qualquer pedido inválido | `recusar` |
| `recurso.produzido` | todos | temporizador da colheita | `colheita` |
| `construcao.concluida` | todos | temporizador da obra | `obra` |
| `buque.montagem_iniciada` | todos | `buque.montagem_solicitada` aceito | `montar_buque` |
| `buque.montado` | todos | temporizador da montagem | `montagem` |
| `buque.vendido` | todos | temporizador de vendas | `vendas` |
| `flores.murchadas` | todos | temporizador de validade do lote | `validade` |
| `vila.encerrada` | todos | `vila.encerramento_solicitado` aceito | `encerrar_vila` |

Os sete eventos mínimos do enunciado foram mantidos com o mesmo nome; os demais foram criados para a
transformação (buquês), a comercialização (Loja) e a expiração (flores murchas).

## Perguntas

### 1. Quais eventos o seu sistema emite e escuta?

O cliente emite quatro pedidos: `vila.abertura_solicitada`, `construcao.solicitada`,
`buque.montagem_solicitada` e `vila.encerramento_solicitado`. O servidor escuta esses pedidos e emite
onze eventos, que o cliente escuta: `estado.sincronizado`, `vila.iniciada`, `construcao.iniciada`,
`operacao.recusada`, `recurso.produzido`, `construcao.concluida`, `buque.montagem_iniciada`,
`buque.montado`, `buque.vendido`, `flores.murchadas` e `vila.encerrada`. As tabelas acima mostram
quem emite, quem recebe e a causa de cada um.

### 2. Como o sistema sabe quando deve atualizar os outros jogadores?

O cliente nunca muda o estado por conta própria nem pergunta ao servidor se algo mudou. Toda mudança
acontece no servidor, em dois momentos: quando ele **aceita um pedido** (depois de validar fase,
papel, recursos e floristas) ou quando um **temporizador** dispara (colheita, obra, montagem, vendas,
validade). Logo depois de alterar o estado, o servidor emite o fato com `sio.emit(evento, fato(...))`
**sem destinatário**, o que envia o fato a todos os jogadores conectados. Cada fato leva o retrato
completo da floricultura e a causa, e cada aba atualiza a tela ao escutá-lo. Os casos que só
interessam a uma pessoa usam `to=sid`: a recusa vai só para quem pediu, e o `estado.sincronizado` vai
só para quem acabou de entrar.

### 3. Que parte do código mostra claramente o uso do paradigma orientado a eventos?

- **`server.py`**: cada pedido tem um tratador registrado com `@sio.on("...")` (`abrir_vila`,
  `construir`, `montar_buque`, `encerrar_vila`), que valida e altera o estado sem pausa entre as duas
  etapas e então emite o fato ou a recusa. Os temporizadores (`colheita`, `vendas`, `obra`,
  `montagem`, `validade`) são tarefas em segundo plano ligadas por outros eventos (a abertura, o
  início de uma obra, uma colheita) e são fontes de eventos sem nenhum clique. A função `fato(causa,
  ...)` deixa explícita a causa de cada fato.
- **`client/index.html`**: dentro de `entrar()`, a região **ESCUTAS** liga cada evento do servidor a
  uma reação com `ouvir(evento, reação, função)`; a região **PEDIDOS** tem uma função por botão que só
  chama `pedir(evento)`. A cena Phaser tem um método por evento (`obraIniciada`, `obraConcluida`,
  `recursoProduzido`, `buqueMontado`, `floresMurcharam` ...).
- **Painel de eventos**: mostra em tempo real cada `⬆ emit` e `⬇ on`, com horário, dados, causa,
  reação e contadores por evento — o encadeamento pedido → fato → temporizador → fato aparece na tela.

## Como testar com duas abas (ou três)

Com o servidor rodando, abra **http://localhost:8000** em três abas lado a lado:

| Aba | Nome | Botão |
|---|---|---|
| 1 | Mestre (ex.: Mia) | Entrar como Mestre |
| 2 | Jogador A (ex.: Ana) | Entrar como Jogador |
| 3 | Jogador B (ex.: Bia) | Entrar como Jogador |

1. **Sincronização:** as três abas mostram 100 flores, 0 buquês, floristas 0/3 e 1 Estufa pronta.
   No painel de cada uma aparece `⬇ on estado.sincronizado` com causa `conexao`.
2. **Recusa antes da abertura:** na Ana, clique em **🌱 Estufa**. Só a aba da Ana mostra o aviso
   vermelho "A temporada não está aberta" e a vila treme; as outras abas não recebem nada.
3. **Abertura:** no Mestre, clique em **Abrir temporada**. As três abas passam para "Temporada aberta"
   sem recarregar. Só o Mestre vê o `⬆ emit vila.abertura_solicitada`.
4. **Colheita automática:** sem clicar em nada, as flores sobem 10 a cada 5 s em todas as abas e um
   "+10 🌷" sobe da Estufa. No painel, `recurso.produzido` aparece com causa "temporizador da colheita".
5. **Construção:** na Ana, clique em **✂️ Ateliê**. Todas as abas veem −50 flores, floristas 1/3 e o
   canteiro na vila. Uns 10 s depois a obra termina sozinha (`construcao.concluida`) e o florista é liberado.
6. **Transformação:** na Ana, clique em **💐 Montar buquê**: −5 flores e "1 em montagem" para todos.
   Se a Bia clicar antes de terminar, só ela recebe "Todos os ateliês estão ocupados". Depois de 6 s,
   todos veem +1 buquê (`buque.montado`).
7. **Loja e vendas:** a Loja é recusada enquanto faltam buquês ("Buquês insuficientes"). Com 2 buquês,
   construa a Loja; quando ela fica pronta, a cada 10 s um buquê é vendido e o placar "Vendidos" sobe
   em todas as abas (`buque.vendido`).
8. **Disputa pelo último florista:** com 2 de 3 floristas ocupados, clique em **🌱 Estufa** na Ana e na
   Bia quase ao mesmo tempo. Só uma consegue (3/3); a outra recebe "Nenhum florista livre". Os floristas
   nunca passam de 3/3 e as flores nunca ficam negativas.
9. **Flores murchas:** 30 s depois de cada colheita, o que sobrou do lote murcha. Todas as abas veem o
   aviso amarelo "🥀 N flores murcharam" e o estoque cai (`flores.murchadas`).
10. **Encerramento:** no Mestre, clique em **Encerrar temporada**. Todas as abas escurecem e mostram o
    placar final. A partir daí nada mais muda e qualquer pedido é recusado.
11. **Painel de eventos:** em cada aba confira `⬆ emit` (pedidos daquela aba) e `⬇ on` (fatos recebidos),
    com horário, dados, causa, reação e os **contadores por evento** no topo do painel.

Com duas abas (Mestre e um Jogador) os passos 1 a 7, 9 e 10 funcionam do mesmo jeito; a terceira aba
serve para ver as recusas individuais e a disputa.

## Uso de IA

Usamos IA para estruturar o que cada uma de nós deveria fazer e como fazer:

- **Claude (Anthropic)** serviu como co-programador do projeto: ajudou a organizar a divisão do
  trabalho, a planejar as milestones e a implementar e testar cada etapa.
- **GitHub Spec Kit** foi usado para organizar a especificação, o plano e as tarefas
  (`.specify/` e `specs/`), para que não houvesse erros durante o projeto.

Conforme requisitado no enunciado, criamos a especificação (`docs/especificacao.md`) antes de iniciar o
desenvolvimento e separamos o trabalho entre a equipe (`docs/equipe.md`): Julia no servidor e Eduarda
na tela.

## Extras

Feitos depois de todo o escopo obrigatório estar pronto e testado:

- **Placar e legenda dentro da tela do jogo:** os números da floricultura (flores, buquês, vendidos,
  floristas e construções) aparecem numa barra de status sobre a vila, e uma legenda recolhível (❔) no
  canto da tela explica o que são a Estufa, o Ateliê, a Loja, o Buquê, a murcha e as obras, usando os
  números enviados pelo servidor. O placar só reflete o retrato do último fato recebido; nada é calculado
  no cliente.

## Créditos

- Mapa, peças do cenário e sprites (`client/assets/`): Kit Inicial da disciplina — arte original de uso
  livre nos trabalhos da disciplina (ver `client/assets/LEIA-ME.txt`).
- Ícones da interface e da vila: emojis do sistema.
- Bibliotecas carregadas por CDN: Vue 3, Socket.IO e Phaser 3 (licenças MIT).

Nenhuma arte de terceiros fora do Kit Inicial foi usada.
