# Plano de implementação: Floricultura em Tempo Real

**Branch**: `main` | **Data**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Entrada**: especificação em `specs/001-floricultura/spec.md` e `docs/especificacao.md`.

## Resumo

Aplicação web multiplayer em tempo real sobre o Kit Inicial do professor. O servidor guarda o
estado da floricultura em memória, valida cada pedido, emite os fatos para todos (ou a recusa só
para quem pediu) e roda os temporizadores de colheita, obra, montagem, vendas e validade. A tela
apenas pede, escuta e reage, desenhando a vila e registrando cada evento no painel.

## Contexto técnico

**Linguagem/Versão**: Python 3 no servidor; JavaScript no navegador.

**Dependências principais**: python-socketio e uvicorn (servidor); Vue 3, Socket.IO client e
Phaser 3 carregados por CDN (tela).

**Armazenamento**: memória do servidor (sem banco de dados).

**Testes**: roteiro manual com duas ou três abas (Mestre, Jogador A, Jogador B) e teste de cada
parte do servidor pelo console do navegador, conforme `docs/equipe.md`.

**Plataforma**: navegador moderno em `http://localhost:8000`.

**Tipo de projeto**: aplicação web (servidor + página única).

**Escopo**: uma floricultura compartilhada por poucos participantes ao mesmo tempo.

## Verificação da constituição

| Princípio | Como o plano cumpre |
|---|---|
| I. Orientação a eventos | Todo o fluxo usa `emit`/`on`; temporizadores do servidor emitem fatos; a tela não faz polling. |
| II. Servidor como fonte da verdade | Validações no servidor, sem pausa entre validar e alterar; recusa com `to=` quem pediu. |
| III. Painel completo | `pedir()` e `ouvir()` do kit registram cada evento com causa e reação; contadores no painel. |
| IV. Mecânicas reais | Lotes com prazo, montagem com temporizador e vendas por ciclo implementados no servidor. |
| V. Simplicidade e kit | Mantém `server.py` e `client/index.html` do kit; nenhuma dependência nova. |

Sem violações.

## Estrutura do projeto

### Documentação

```text
docs/
├── especificacao.md        # especificação oficial (regras, eventos, cenários)
└── equipe.md               # divisão do trabalho e acompanhamento das milestones
specs/001-floricultura/
├── spec.md                 # histórias de usuário
├── plan.md                 # este arquivo
└── tasks.md                # tarefas por milestone
.specify/memory/constitution.md
```

### Código-fonte

```text
server.py                   # estado, tratadores dos pedidos, fatos e temporizadores (Julia)
client/
├── index.html              # tela Vue, pedidos/escutas, painel e cena Phaser (Eduarda)
└── assets/                 # mapa, tileset e sprites do kit
requirements.txt
```

**Decisão de estrutura**: manter a estrutura do kit. O servidor fica em um arquivo e a tela em
outro, o que também separa naturalmente o trabalho das duas desenvolvedoras.

## Acompanhamento da complexidade

Nenhum item: o plano não precisa de exceções à constituição.
