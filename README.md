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

## Como testar com duas abas

(Passo a passo: quem entra como Mestre, quem entra como Jogador, o que clicar e o que deve aparecer.)

## Uso de IA

(O que usou e o que mudou. Se não usou: "Não utilizei IA".)

## Créditos

(Recursos visuais de terceiros, se houver.)
