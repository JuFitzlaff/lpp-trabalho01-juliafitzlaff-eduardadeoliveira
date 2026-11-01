import copy

import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio, static_files={
    "/": "client/index.html",
    "/assets": "client/assets",      # mapa, tileset e sprites da vila
})

# A partir da Etapa 1, adicione o seu código ABAIXO desta linha.

# ---------------------------------------------------------------------
# Regras da Floricultura (docs/especificacao.md, seção 10)
# ---------------------------------------------------------------------
LIMITE_FLORISTAS = 3        # floristas disponíveis durante toda a temporada
INTERVALO_COLHEITA = 5      # segundos entre duas colheitas
FLORES_POR_ESTUFA = 10      # flores colhidas por Estufa pronta, a cada colheita
VALIDADE_LOTE = 30          # segundos até as flores de um lote murcharem
TEMPO_OBRA = 10             # segundos de obra (igual para todas as construções)
FLORES_POR_BUQUE = 5        # flores gastas em uma montagem
TEMPO_MONTAGEM = 6          # segundos para montar um buquê
INTERVALO_VENDAS = 10       # segundos entre dois ciclos de vendas da Loja

CUSTOS = {                  # o que cada construção debita do estoque
    "estufa": {"flores": 30, "buques": 0},
    "atelie": {"flores": 50, "buques": 0},
    "loja":   {"flores": 40, "buques": 2},
}

# ---------------------------------------------------------------------
# Estado compartilhado: só o servidor altera. É o "retrato" enviado nos fatos.
# ---------------------------------------------------------------------
estado = {
    "fase": "aguardando",       # aguardando -> aberta -> encerrada
    "flores": 100,              # soma das flores de todos os lotes
    "buques": 0,
    "vendidos": 0,              # placar de buquês vendidos
    "floristas": 0,             # floristas ocupados agora
    "limite": LIMITE_FLORISTAS,
    "construcoes": {            # prontas e em obra, por tipo
        "estufa": {"prontas": 1, "em_obra": 0},   # a floricultura começa com 1 Estufa
        "atelie": {"prontas": 0, "em_obra": 0},
        "loja":   {"prontas": 0, "em_obra": 0},
    },
    "montagens": 0,             # buquês sendo montados agora
    "producao": FLORES_POR_ESTUFA,   # flores por colheita (10 x Estufas prontas)
    "intervalo": INTERVALO_COLHEITA,
    "validade": VALIDADE_LOTE,
    "tempo_obra": TEMPO_OBRA,
    "custos": CUSTOS,
    "flores_por_buque": FLORES_POR_BUQUE,
    "tempo_montagem": TEMPO_MONTAGEM,
    "intervalo_vendas": INTERVALO_VENDAS,
}

# Flores guardadas por lote (cada colheita vira um lote com prazo próprio).
# O total de flores fica em estado["flores"]; os lotes ficam só no servidor.
lotes = [{"id": 1, "qtd": 100}]     # lote inicial: o prazo começa na abertura

jogadores = {}                      # sid -> {"nome": ..., "papel": ...}


def fato(causa, **extras):
    """Monta o payload de um FATO: uma cópia do estado atual, a CAUSA (o pedido
    ou o temporizador que gerou o fato) e dados extras."""
    return {"estado": copy.deepcopy(estado), "causa": causa, **extras}


@sio.event
async def connect(sid, environ, auth):
    # Nunca confiar no cliente: papel desconhecido vira "jogador" e o nome é limitado.
    auth = auth if isinstance(auth, dict) else {}
    nome = str(auth.get("nome") or "Anônimo").strip()[:20] or "Anônimo"
    papel = auth.get("papel") if auth.get("papel") in ("mestre", "jogador") else "jogador"
    jogadores[sid] = {"nome": nome, "papel": papel}
    # servidor -> SÓ quem entrou: os outros já têm o estado, só o recém-chegado precisa dele
    await sio.emit("estado.sincronizado", fato("conexao"), to=sid)


@sio.event
async def disconnect(sid):
    # quem sai deixa de ser participante; a floricultura não muda
    jogadores.pop(sid, None)
