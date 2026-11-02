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
proximo_lote = 2

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


async def recusar(sid, motivo, causa):
    """Recusa um pedido. Vai SÓ para quem pediu: os outros não têm nada a mudar."""
    await sio.emit("operacao.recusada", {"motivo": motivo, "causa": causa}, to=sid)


def papel_de(sid):
    return jogadores.get(sid, {}).get("papel")


@sio.on("vila.abertura_solicitada")
async def abrir_vila(sid, dados=None):
    # escuta o PEDIDO do Mestre; quem decide se a temporada abre é o servidor
    pedido = "vila.abertura_solicitada"
    if papel_de(sid) != "mestre":
        await recusar(sid, "Só o Mestre pode abrir a temporada", pedido)
        return
    if estado["fase"] != "aguardando":
        await recusar(sid, "A temporada já foi aberta", pedido)
        return
    estado["fase"] = "aberta"
    sio.start_background_task(colheita)     # a abertura liga o temporizador da colheita
    sio.start_background_task(vendas)       # e o temporizador de vendas da Loja
    for lote in lotes:                      # o prazo do lote inicial começa na abertura
        sio.start_background_task(validade, lote["id"])
    # servidor -> TODOS: o fato muda a fase para todos os jogadores ao mesmo tempo
    await sio.emit("vila.iniciada", fato(pedido))


def novo_lote(qtd):
    """Guarda uma colheita como lote novo e soma as flores ao estoque."""
    global proximo_lote
    lote = {"id": proximo_lote, "qtd": qtd}
    proximo_lote += 1
    lotes.append(lote)
    estado["flores"] += qtd
    return lote


async def colheita():
    """Temporizador da colheita: enquanto a temporada estiver aberta, colhe a cada INTERVALO_COLHEITA."""
    while estado["fase"] == "aberta":
        await sio.sleep(INTERVALO_COLHEITA)     # sio.sleep não trava o servidor (time.sleep travaria)
        if estado["fase"] != "aberta":
            break
        qtd = estado["producao"]                # 10 flores por Estufa pronta
        lote = novo_lote(qtd)
        sio.start_background_task(validade, lote["id"])     # cada colheita tem o seu prazo
        # servidor -> TODOS, sem ninguém pedir: a causa do fato é o temporizador
        await sio.emit("recurso.produzido", fato("temporizador da colheita", qtd=qtd))


async def validade(lote_id):
    """Temporizador de validade: VALIDADE_LOTE segundos depois da colheita, o que sobrou do lote murcha."""
    await sio.sleep(VALIDADE_LOTE)
    if estado["fase"] != "aberta":
        return                                  # temporada encerrada: nada mais murcha
    lote = next((l for l in lotes if l["id"] == lote_id), None)
    if lote is None:
        return                                  # lote já usado por inteiro: some sem aviso
    lotes.remove(lote)
    estado["flores"] -= lote["qtd"]
    # servidor -> TODOS, sem ninguém pedir: a causa do fato é o prazo do lote
    await sio.emit("flores.murchadas", fato("temporizador de validade", qtd=lote["qtd"], lote=lote_id))


async def vendas():
    """Temporizador de vendas: a cada INTERVALO_VENDAS, cada Loja pronta vende 1 buquê, se houver."""
    while estado["fase"] == "aberta":
        await sio.sleep(INTERVALO_VENDAS)
        if estado["fase"] != "aberta":
            break
        qtd = min(estado["construcoes"]["loja"]["prontas"], estado["buques"])
        if qtd == 0:
            continue                            # sem Loja ou sem buquê: nada a anunciar
        estado["buques"] -= qtd
        estado["vendidos"] += qtd               # placar cooperativo da temporada
        # servidor -> TODOS, sem ninguém pedir: a causa do fato é o temporizador de vendas
        await sio.emit("buque.vendido", fato("temporizador de vendas", qtd=qtd))


def gastar_flores(qtd):
    """Tira `qtd` flores do estoque, das mais antigas (mais perto de murchar) para as mais novas."""
    estado["flores"] -= qtd
    while qtd > 0 and lotes:
        usado = min(qtd, lotes[0]["qtd"])
        lotes[0]["qtd"] -= usado
        qtd -= usado
        if lotes[0]["qtd"] == 0:
            lotes.pop(0)            # lote usado por inteiro: some sem murchar


@sio.on("construcao.solicitada")
async def construir(sid, dados=None):
    # escuta o PEDIDO de um Jogador para construir uma Estufa, um Ateliê ou uma Loja
    pedido = "construcao.solicitada"
    tipo = dados.get("tipo") if isinstance(dados, dict) else None
    # Valide TUDO antes de alterar o estado e sem await no meio:
    # assim, dois pedidos simultâneos são decididos um de cada vez.
    if estado["fase"] != "aberta":
        motivo = "A temporada não está aberta"
    elif papel_de(sid) != "jogador":
        motivo = "Só jogadores podem construir"
    elif not isinstance(tipo, str) or tipo not in CUSTOS:
        motivo = "Tipo de construção inválido"
    elif estado["flores"] < CUSTOS[tipo]["flores"]:
        motivo = "Flores insuficientes"
    elif estado["buques"] < CUSTOS[tipo]["buques"]:
        motivo = "Buquês insuficientes"
    elif estado["floristas"] >= estado["limite"]:
        motivo = "Nenhum florista livre"
    else:
        motivo = None
    if motivo:
        await recusar(sid, motivo, pedido)      # só quem pediu recebe; nada muda
        return

    custo = CUSTOS[tipo]
    gastar_flores(custo["flores"])
    estado["buques"] -= custo["buques"]
    estado["floristas"] += 1
    estado["construcoes"][tipo]["em_obra"] += 1
    nome = jogadores[sid]["nome"]
    # servidor -> TODOS: todos veem o canteiro novo e o estoque debitado
    await sio.emit("construcao.iniciada", fato(pedido, tipo=tipo, por=nome))
    sio.start_background_task(obra, tipo, nome)     # o fato liga o temporizador desta obra


async def obra(tipo, nome):
    """Temporizador da obra: termina sozinha TEMPO_OBRA segundos depois de construcao.iniciada."""
    await sio.sleep(TEMPO_OBRA)
    if estado["fase"] != "aberta":
        return                                      # temporada encerrada: a obra fica congelada
    construcao = estado["construcoes"][tipo]
    construcao["em_obra"] -= 1
    construcao["prontas"] += 1
    estado["floristas"] -= 1                        # o florista volta a ficar livre
    if tipo == "estufa":
        estado["producao"] += FLORES_POR_ESTUFA     # cada Estufa nova colhe +10 por colheita
    # servidor -> TODOS, sem ninguém pedir: a causa é o temporizador ligado pela obra
    await sio.emit("construcao.concluida", fato("temporizador da obra", tipo=tipo, por=nome))


@sio.on("buque.montagem_solicitada")
async def montar_buque(sid, dados=None):
    # escuta o PEDIDO de um Jogador para transformar flores em um buquê no Ateliê
    pedido = "buque.montagem_solicitada"
    # Valide TUDO antes de alterar o estado e sem await no meio (mesma regra da construção).
    atelies = estado["construcoes"]["atelie"]["prontas"]
    if estado["fase"] != "aberta":
        motivo = "A temporada não está aberta"
    elif papel_de(sid) != "jogador":
        motivo = "Só jogadores podem montar buquês"
    elif atelies == 0:
        motivo = "Nenhum ateliê pronto"
    elif estado["montagens"] >= atelies:
        motivo = "Todos os ateliês estão ocupados"
    elif estado["flores"] < FLORES_POR_BUQUE:
        motivo = "Flores insuficientes"
    elif estado["floristas"] >= estado["limite"]:
        motivo = "Nenhum florista livre"
    else:
        motivo = None
    if motivo:
        await recusar(sid, motivo, pedido)      # só quem pediu recebe; nada muda
        return

    gastar_flores(FLORES_POR_BUQUE)             # as flores mais antigas viram buquê primeiro
    estado["floristas"] += 1
    estado["montagens"] += 1                    # ocupa um Ateliê
    nome = jogadores[sid]["nome"]
    # servidor -> TODOS: todos veem as flores saírem e o Ateliê ocupado
    await sio.emit("buque.montagem_iniciada", fato(pedido, por=nome))
    sio.start_background_task(montagem, nome)   # o fato liga o temporizador desta montagem


async def montagem(nome):
    """Temporizador da montagem: o buquê fica pronto TEMPO_MONTAGEM segundos depois."""
    await sio.sleep(TEMPO_MONTAGEM)
    if estado["fase"] != "aberta":
        return                                  # temporada encerrada: a montagem fica congelada
    estado["buques"] += 1
    estado["floristas"] -= 1                    # florista e Ateliê voltam a ficar livres
    estado["montagens"] -= 1
    # servidor -> TODOS, sem ninguém pedir: a causa é o temporizador ligado pela montagem
    await sio.emit("buque.montado", fato("temporizador da montagem", por=nome))
