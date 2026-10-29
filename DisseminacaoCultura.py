"""Disseminação de Cultura em um campus universitário
Inspirado em: Axelrod (1997), "The Dissemination of Culture".

Executar:  python DisseminacaoCultura.py   (requer Python 3.8+ com tkinter)

Regras resumidas
- Tabuleiro TAMANHO x TAMANHO (9x9 = 81 casas). Nº de agentes configurável (1 a 81).
- Cada agente tem 5 características: sexo, período, curso, religião e origem.
- Similaridade ponderada: religião e origem pesam mais; as demais pesam menos.
- A cada rodada, UM agente aleatório age:
        1) se move para a casa livre vizinha que mais o aproxima de agentes parecidos;
        2) (opcional) interação estilo Axelrod: com probabilidade = similaridade,
             copia uma característica diferente de um vizinho adjacente.
- Influenciadores:
        * Agente mais relevante do campus: 5% de chance por rodada de mudar CURSO ou
            RELIGIÃO dos agentes ao seu redor.
        * Líder de cada outro grupo: 1% de chance por rodada de aproximar culturalmente
            apenas os agentes adjacentes, copiando uma característica diferente.
"""

import random
import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------- Configuração
TAMANHO = 9                 # tabuleiro TAMANHO x TAMANHO
CELULA = 62                 # pixels por casa
PROB_INFLUENCIADOR = 0.05   # agente mais relevante do campus
PROB_LIDER_GRUPO = 0.01     # líderes dos demais grupos
LIMIAR_GRUPO = 0.70         # similaridade mínima para dois vizinhos formarem um grupo
RODADAS_POR_ANO = 12

# Pesos da similaridade (somam 1.0)
PESOS = {"religiao": 0.30, "origem": 0.30, "curso": 0.20, "periodo": 0.10, "sexo": 0.10}

SEXOS = ["Feminino", "Masculino"]
PERIODOS = list(range(1, 13))
CURSOS = [
    "Administração", "Arquitetura e Urbanismo", "Ciência da Computação",
    "Ciências Contábeis", "Ciências Econômicas", "Direito", "Enfermagem",
    "Engenharia Ambiental", "Engenharia Civil", "Engenharia de Alimentos",
    "Engenharia Elétrica", "Filosofia", "Inteligência Artificial", "Jornalismo",
    "Medicina", "Nutrição", "Pedagogia", "Psicologia", "Teatro",
]
RELIGIOES = ["Católica", "Evangélica", "Sem religião", "Espírita",
             "Umbanda", "Candomblé", "Budismo"]
ORIGENS = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

COR_CURSO = dict(zip(CURSOS, [
    "#80b1d3", "#fdb462", "#8dd3c7", "#fb8072", "#bebada",
    "#ccebc5", "#ffed6f", "#bc80bd", "#d9d9d9", "#fccde5",
    "#b3de69", "#c6e2ff", "#fdd0a2", "#9ed9a7", "#fcae91",
    "#d6c7e3", "#f5e6a8", "#92c5de", "#f4a582",
]))
COR_ORIGEM = {
    "Norte": "#1b7f3b", "Nordeste": "#d9480f", "Centro-Oeste": "#8d6e3f",
    "Sudeste": "#1c4e9c", "Sul": "#7a1fa2",
}

VIZ8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


# ------------------------------------------------------------------------ Agente
class Agente:
    def __init__(self, ident, pos):
        self.id = ident
        self.pos = pos  # (linha, coluna)
        self.sexo = random.choice(SEXOS)
        self.periodo = random.choice(PERIODOS)
        self.curso = random.choice(CURSOS)
        self.religiao = random.choice(RELIGIOES)
        self.origem = random.choice(ORIGENS)

    def similaridade(self, o):
        s = 0.0
        s += PESOS["religiao"] * (self.religiao == o.religiao)
        s += PESOS["origem"] * (self.origem == o.origem)
        s += PESOS["curso"] * (self.curso == o.curso)
        s += PESOS["sexo"] * (self.sexo == o.sexo)
        # período: quanto mais próximo, mais parecido
        s += PESOS["periodo"] * (1 - abs(self.periodo - o.periodo) / (len(PERIODOS) - 1))
        return s

    def tracos_diferentes(self, o):
        """Características em que os dois diferem (para a cópia estilo Axelrod)."""
        return [c for c in ("sexo", "periodo", "curso", "religiao", "origem")
                if getattr(self, c) != getattr(o, c)]


# --------------------------------------------------------------------- Simulação
class Simulacao:
    def __init__(self, n_agentes, axelrod=True):
        self.n = max(1, min(n_agentes, TAMANHO * TAMANHO))
        self.axelrod = axelrod
        self.rodada = 0
        self.ano = 0
        self.agentes = []
        self.grade = {}
        casas = [(r, c) for r in range(TAMANHO) for c in range(TAMANHO)]
        random.shuffle(casas)
        for i in range(self.n):
            a = Agente(i + 1, casas[i])
            self.agentes.append(a)
            self.grade[a.pos] = a
        self.distribuicao_inicial = [
            (a.id, a.pos, a.curso, a.origem) for a in self.agentes
        ]
        self.ativo = None
        self.ultimo_movimento = None
        self.eventos = []  # mensagens da última rodada
        self.historico_eventos = []
        self.influenciador = None
        self.lideres = []
        self.n_grupos = 0
        self.atualizar_relevancia()

    # ---- utilidades de grade
    @staticmethod
    def dentro(p):
        return 0 <= p[0] < TAMANHO and 0 <= p[1] < TAMANHO

    def vizinhos_adjacentes(self, a):
        res = []
        for dr, dc in VIZ8:
            p = (a.pos[0] + dr, a.pos[1] + dc)
            if p in self.grade:
                res.append(self.grade[p])
        return res

    @staticmethod
    def dist(p, q):
        return max(abs(p[0] - q[0]), abs(p[1] - q[1]))  # distância de Chebyshev

    # ---- relevância, grupos e líderes
    def atualizar_relevancia(self):
        """Relevância = soma da similaridade do agente com todos os outros."""
        if len(self.agentes) < 2:
            self.influenciador, self.lideres, self.n_grupos = self.agentes[0] if self.agentes else None, [], 0
            return
        relev = {a.id: sum(a.similaridade(o) for o in self.agentes if o is not a)
                 for a in self.agentes}
        self.influenciador = max(self.agentes, key=lambda a: relev[a.id])

        # grupos: componentes conexos (adjacência 8 vizinhos) com similaridade >= limiar
        visitados, grupos = set(), []
        for a in self.agentes:
            if a.id in visitados:
                continue
            pilha, grupo = [a], []
            visitados.add(a.id)
            while pilha:
                x = pilha.pop()
                grupo.append(x)
                for y in self.vizinhos_adjacentes(x):
                    if y.id not in visitados and x.similaridade(y) >= LIMIAR_GRUPO:
                        visitados.add(y.id)
                        pilha.append(y)
            if len(grupo) >= 2:
                grupos.append(grupo)
        self.n_grupos = len(grupos)
        self.lideres = []
        for g in grupos:
            if self.influenciador in g:
                continue
            lider = max(g, key=lambda x: sum(x.similaridade(o) for o in g if o is not x))
            self.lideres.append(lider)

    # ---- movimento
    def pontuacao_casa(self, agente, casa, ignorar=None):
        """Atração de uma casa: soma de similaridade/(1+distância) a todos os outros."""
        return sum(agente.similaridade(o) / (1 + self.dist(casa, o.pos))
                   for o in self.agentes if o is not agente and o is not ignorar)

    @staticmethod
    def formatar_posicao(posicao):
        return f"linha {posicao[0] + 1}, coluna {posicao[1] + 1}"

    def mover(self, a):
        melhor, melhor_p = a.pos, self.pontuacao_casa(a, a.pos)
        candidatos = []
        for dr, dc in VIZ8:
            p = (a.pos[0] + dr, a.pos[1] + dc)
            if not self.dentro(p):
                continue
            ocupante = self.grade.get(p)
            if ocupante is None or self.n == TAMANHO * TAMANHO:
                candidatos.append((p, ocupante))

        if self.n == TAMANHO * TAMANHO and candidatos:
            melhor, trocado = max(
                candidatos,
                key=lambda item: self.pontuacao_casa(a, item[0], item[1])
                + random.uniform(0, 0.01),
            )
        else:
            trocado = None
            for p, _ in candidatos:
                pt = self.pontuacao_casa(a, p) + random.uniform(0, 0.01)
                if pt > melhor_p:
                    melhor, melhor_p = p, pt
        if melhor != a.pos:
            origem = a.pos
            self.ultimo_movimento = (origem, melhor)
            del self.grade[origem]
            if trocado is not None:
                trocado.pos = origem
                self.grade[origem] = trocado
            a.pos = melhor
            self.grade[a.pos] = a
            self.eventos.append(
                f"Agente {a.id} mudou de {self.formatar_posicao(origem)} "
                f"para {self.formatar_posicao(melhor)}."
            )
            if trocado is not None:
                self.eventos.append(
                    f"Agente {trocado.id} mudou de {self.formatar_posicao(melhor)} "
                    f"para {self.formatar_posicao(origem)} (troca de posição)."
                )
        else:
            self.ultimo_movimento = None

    def mover_para_centro(self, agente):
        if agente is None:
            return
        centro = (TAMANHO // 2, TAMANHO // 2)
        distancia_atual = self.dist(agente.pos, centro)
        candidatos = [
            (agente.pos[0] + dr, agente.pos[1] + dc)
            for dr, dc in VIZ8
            if self.dentro((agente.pos[0] + dr, agente.pos[1] + dc))
            and self.dist((agente.pos[0] + dr, agente.pos[1] + dc), centro) < distancia_atual
        ]
        if not candidatos:
            return

        origem = agente.pos
        destino = min(candidatos, key=lambda pos: self.dist(pos, centro))
        trocado = self.grade.get(destino)
        del self.grade[origem]
        if trocado is not None:
            trocado.pos = origem
            self.grade[origem] = trocado
        agente.pos = destino
        self.grade[destino] = agente
        self.ultimo_movimento = (origem, destino)
        self.eventos.append(
            f"Agente mais relevante {agente.id} mudou de {self.formatar_posicao(origem)} "
            f"para {self.formatar_posicao(destino)} (em direção ao centro)."
        )
        if trocado is not None:
            self.eventos.append(
                f"Agente {trocado.id} mudou de {self.formatar_posicao(destino)} "
                f"para {self.formatar_posicao(origem)} (troca de posição)."
            )

    # ---- influência
    def influencia_axelrod(self, a):
        viz = self.vizinhos_adjacentes(a)
        if not viz:
            return
        o = random.choice(viz)
        if random.random() < a.similaridade(o):
            difs = a.tracos_diferentes(o)
            if difs:
                c = random.choice(difs)
                anterior = getattr(a, c)
                setattr(a, c, getattr(o, c))
                atual = getattr(a, c)
                self.eventos.append(
                    f"Agente {a.id}: {c} {anterior} -> {atual} "
                    f"(copiou do agente {o.id})."
                )

    def influencia_lider(self, lider, tipo):
        viz = self.vizinhos_adjacentes(lider)
        if not viz:
            return
        for v in viz:
            tracos = lider.tracos_diferentes(v)
            if tipo != "Líder de grupo":
                tracos = [c for c in tracos if c in ("curso", "religiao")]
            if not tracos:
                continue
            c = random.choice(tracos)
            anterior = getattr(v, c)
            atual = getattr(lider, c)
            setattr(v, c, getattr(lider, c))
            self.eventos.append(
                f"{tipo} {lider.id}: agente {v.id} em {self.formatar_posicao(v.pos)} "
                f"aproximou-se do líder: {c} {anterior} -> {atual}."
            )

    # ---- uma rodada
    def passo(self):
        self.rodada += 1
        self.eventos = []
        self.ativo = random.choice(self.agentes)
        self.mover(self.ativo)
        if self.axelrod:
            self.influencia_axelrod(self.ativo)

        if self.influenciador and random.random() < PROB_INFLUENCIADOR:
            self.influencia_lider(self.influenciador, "Mais relevante do campus")
        for lider in self.lideres:
            if random.random() < PROB_LIDER_GRUPO:
                self.influencia_lider(lider, "Líder de grupo")
        self.atualizar_relevancia()
        if self.rodada % RODADAS_POR_ANO == 0:
            self.ano += 1
            self.mover_para_centro(self.influenciador)
        if not self.eventos:
            self.eventos.append("Nenhuma mudança neste período.")
        self.historico_eventos.extend(
            f"Período {self.rodada}: {evento}" for evento in self.eventos
        )
        del self.historico_eventos[:-200]

    def similaridade_media_vizinhos(self):
        pares = []
        for a in self.agentes:
            for v in self.vizinhos_adjacentes(a):
                pares.append(a.similaridade(v))
        return sum(pares) / len(pares) if pares else 0.0


# ---------------------------------------------------------------------------- UI
class App:
    def __init__(self, root):
        self.root = root
        root.title("Disseminação de Cultura – Campus")
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()
        self.celula = max(32, min(
            CELULA,
            (largura_tela - 430) // TAMANHO,
            (altura_tela - 150) // TAMANHO,
        ))
        lado_tabuleiro = TAMANHO * self.celula
        largura_janela = min(largura_tela - 32, lado_tabuleiro + 430)
        altura_janela = min(altura_tela - 70, max(lado_tabuleiro + 100, 560))
        pos_x = max(0, (largura_tela - largura_janela) // 2)
        pos_y = max(0, (altura_tela - altura_janela) // 2)
        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        root.minsize(min(largura_janela, largura_tela - 20),
                     min(altura_janela, lado_tabuleiro + 90))
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.configure(background="#f1f4f1")
        estilo = ttk.Style(root)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f1f4f1")
        estilo.configure("TLabel", background="#f1f4f1", foreground="#25342f",
                         font=("Segoe UI", 9))
        estilo.configure("TLabelframe", background="#f1f4f1", bordercolor="#c6d2cc",
                         relief="solid")
        estilo.configure("TLabelframe.Label", background="#f1f4f1", foreground="#21483e",
                         font=("Segoe UI", 9, "bold"))
        estilo.configure("TCheckbutton", background="#f1f4f1", foreground="#25342f")
        estilo.configure("Header.TFrame", background="#21483e")
        estilo.configure("HeaderTitle.TLabel", background="#21483e", foreground="#ffffff",
                         font=("Segoe UI", 15, "bold"))
        estilo.configure("HeaderSubtitle.TLabel", background="#21483e", foreground="#d7e6df",
                         font=("Segoe UI", 9))
        estilo.configure("Primary.TButton", background="#19745f", foreground="#ffffff",
                         font=("Segoe UI", 9, "bold"), padding=(8, 7))
        estilo.map("Primary.TButton", background=[("active", "#145e4d")])
        estilo.configure("Secondary.TButton", background="#e2eae5", foreground="#21483e",
                         font=("Segoe UI", 9, "bold"), padding=(8, 7))
        estilo.map("Secondary.TButton", background=[("active", "#d1ded6")])
        estilo.configure("Muted.TLabel", foreground="#63736c", font=("Segoe UI", 8))
        self.sim = None
        self.rodando = False
        self.selecionado = None

        cabecalho = ttk.Frame(root, style="Header.TFrame", padding=(18, 12))
        cabecalho.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(cabecalho, text="DISSEMINAÇÃO DE CULTURA",
                  style="HeaderTitle.TLabel").pack(anchor="w")
        ttk.Label(cabecalho, text="Campus universitário  ·  modelo de Axelrod",
                  style="HeaderSubtitle.TLabel").pack(anchor="w", pady=(2, 0))

        # canvas do tabuleiro
        self.canvas = tk.Canvas(root, width=lado_tabuleiro, height=lado_tabuleiro,
                                bg="#ffffff", highlightthickness=1, highlightbackground="#c6d2cc")
        self.canvas.grid(row=1, column=0, padx=(18, 12), pady=18, sticky="n")
        self.canvas.bind("<Button-1>", self.clique)

        # Painel lateral rolável para manter todas as informações acessíveis.
        painel = ttk.Frame(root)
        painel.grid(row=1, column=1, sticky="nsew", padx=(0, 12), pady=10)
        self.canvas_lateral = tk.Canvas(painel, width=350, bg="#f1f4f1",
                                        highlightthickness=0, borderwidth=0)
        barra_lateral = ttk.Scrollbar(painel, orient="vertical",
                                      command=self.canvas_lateral.yview)
        self.canvas_lateral.configure(yscrollcommand=barra_lateral.set)
        self.canvas_lateral.grid(row=0, column=0, sticky="nsew")
        barra_lateral.grid(row=0, column=1, sticky="ns")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(0, weight=1)
        lado = ttk.Frame(self.canvas_lateral, padding=(0, 8, 14, 12))
        self.janela_lateral = self.canvas_lateral.create_window(
            (0, 0), window=lado, anchor="nw"
        )
        lado.bind("<Configure>", self.atualizar_area_lateral)
        self.canvas_lateral.bind("<Configure>", self.redimensionar_lateral)
        self.canvas_lateral.bind("<Enter>", self.ativar_rolagem_lateral)
        self.canvas_lateral.bind("<Leave>", self.desativar_rolagem_lateral)

        cfg = ttk.LabelFrame(lado, text="Configuração")
        cfg.pack(fill="x")
        ttk.Label(cfg, text="Agentes no campus:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.var_n = tk.IntVar(value=40)
        ttk.Spinbox(cfg, from_=2, to=TAMANHO * TAMANHO, textvariable=self.var_n,
                    width=6).grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(cfg, text="Velocidade:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.var_vel = tk.IntVar(value=5)
        ttk.Scale(cfg, from_=1, to=10, variable=self.var_vel, orient="horizontal",
                  length=120).grid(row=1, column=1, padx=6, pady=4)
        self.var_axl = tk.BooleanVar(value=True)
        ttk.Checkbutton(cfg, text="Interação cultural (Axelrod)",
                        variable=self.var_axl).grid(row=2, column=0, columnspan=2,
                                                    sticky="w", padx=6, pady=(4, 0))
        ttk.Label(cfg, text="Agentes próximos podem copiar características.",
                  style="Muted.TLabel").grid(row=3, column=0, columnspan=2,
                                             sticky="w", padx=6, pady=(0, 6))

        bt = ttk.Frame(lado)
        ttk.Button(lado, text="▶ Disseminar cultura · 1 período",
                   style="Primary.TButton", command=self.avancar_periodo).pack(fill="x", pady=(4, 2))
        ttk.Label(lado, text="Cada clique avança uma rodada e pausa.",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 4))

        bt.pack(fill="x", pady=4)
        for coluna in range(3):
            bt.grid_columnconfigure(coluna, weight=1, uniform="acoes")
        ttk.Button(bt, text="▶ Contínuo", style="Secondary.TButton",
                   command=self.iniciar).grid(row=0, column=0, sticky="ew", padx=(0, 3))
        ttk.Button(bt, text="Ⅱ Pausar", style="Secondary.TButton",
                   command=self.pausar).grid(row=0, column=1, sticky="ew", padx=3)
        ttk.Button(bt, text="↻ Reiniciar", style="Secondary.TButton",
                   command=self.reiniciar).grid(row=0, column=2, sticky="ew", padx=(3, 0))
        ttk.Button(lado, text="▦ Ver matriz inicial", style="Secondary.TButton",
                   command=self.visualizar_distribuicao_inicial).pack(fill="x", pady=(0, 4))
        ttk.Label(lado,
                  text=f"1 ano = {RODADAS_POR_ANO} rodadas. A cada ano, o indivíduo mais relevante avança uma casa em direção ao centro.",
                  style="Muted.TLabel", wraplength=300, justify="left").pack(anchor="w", pady=(0, 8))

        est = ttk.LabelFrame(lado, text="Resumo da simulação")
        est.pack(fill="x")
        self.lbl_stats = ttk.Label(est, justify="left")
        self.lbl_stats.pack(anchor="w", padx=6, pady=5)

        ag = ttk.LabelFrame(lado, text="Indivíduo")
        ag.pack(fill="x", pady=6)
        self.lbl_agente = ttk.Label(ag, justify="left", width=34, wraplength=290)
        self.lbl_agente.pack(anchor="w", padx=6, pady=5)

        ev = ttk.LabelFrame(lado, text="Eventos recentes")
        ev.pack(fill="x")
        area_eventos = ttk.Frame(ev)
        area_eventos.pack(fill="both", expand=True, padx=6, pady=5)
        self.txt_eventos = tk.Text(area_eventos, width=38, height=8, wrap="word",
                       state="disabled", font=("Segoe UI", 8),
                       bg="#ffffff", fg="#25342f", relief="solid",
                       borderwidth=1)
        barra_eventos = ttk.Scrollbar(area_eventos, orient="vertical",
                          command=self.txt_eventos.yview)
        self.txt_eventos.configure(yscrollcommand=barra_eventos.set)
        self.txt_eventos.grid(row=0, column=0, sticky="nsew")
        barra_eventos.grid(row=0, column=1, sticky="ns")
        area_eventos.grid_columnconfigure(0, weight=1)
        area_eventos.grid_rowconfigure(0, weight=1)

        leg = ttk.LabelFrame(lado, text="Legenda")
        leg.pack(fill="x", pady=6)
        lc = tk.Canvas(leg, width=340, height=340, bg="#f1f4f1", highlightthickness=0)
        lc.pack()
        lc.create_text(4, 9, text="Círculo: curso", anchor="w",
                       fill="#21483e", font=("Segoe UI", 8, "bold"))
        lc.create_text(188, 9, text="Contorno: origem", anchor="w",
                       fill="#21483e", font=("Segoe UI", 8, "bold"))
        for indice, (curso, cor) in enumerate(COR_CURSO.items()):
            y = 25 + indice * 14
            lc.create_oval(5, y - 5, 15, y + 5, fill=cor, outline="")
            lc.create_text(21, y, text=curso, anchor="w", fill="#25342f",
                           font=("Segoe UI", 7))
        for indice, (origem, cor) in enumerate(COR_ORIGEM.items()):
            y = 25 + indice * 15
            lc.create_rectangle(190, y - 5, 200, y + 5, outline=cor, width=3)
            lc.create_text(207, y, text=origem, anchor="w", fill="#25342f",
                           font=("Segoe UI", 8))
        lc.create_text(188, 115, text="★ Mais relevante", anchor="w",
                   fill="#25342f", font=("Segoe UI", 8))
        lc.create_text(188, 132, text="◆ Líder de grupo", anchor="w",
                   fill="#25342f", font=("Segoe UI", 8))
        lc.create_text(188, 149, text="Tracejado: centro", anchor="w",
                       fill="#25342f", font=("Segoe UI", 8))
        lc.create_text(188, 166, text="Anel vermelho: ativo", anchor="w",
                       fill="#25342f", font=("Segoe UI", 8))
        lc.create_text(188, 183, text="Moldura verde: selecionado",
                       anchor="w", fill="#25342f", font=("Segoe UI", 8))

        self.reiniciar()

    # ---- controle
    def atualizar_area_lateral(self, _evento=None):
        self.canvas_lateral.configure(scrollregion=self.canvas_lateral.bbox("all"))

    def redimensionar_lateral(self, evento):
        self.canvas_lateral.itemconfigure(self.janela_lateral, width=evento.width)

    def ativar_rolagem_lateral(self, _evento=None):
        self.root.bind_all("<MouseWheel>", self.rolar_lateral)

    def desativar_rolagem_lateral(self, _evento=None):
        self.root.unbind_all("<MouseWheel>")

    def rolar_lateral(self, evento):
        direcao = -1 if evento.delta > 0 else 1
        self.canvas_lateral.yview_scroll(direcao, "units")

    def iniciar(self):
        if not self.rodando:
            self.rodando = True
            self.loop()

    def avancar_periodo(self):
        self.rodando = False
        self.sim.axelrod = self.var_axl.get()
        self.sim.passo()
        self.desenhar()

    def pausar(self):
        self.rodando = False

    def reiniciar(self):
        self.rodando = False
        try:
            n = int(self.var_n.get())
        except (tk.TclError, ValueError):
            n = 40
        self.sim = Simulacao(n, self.var_axl.get())
        self.selecionado = None
        self.desenhar()

    def loop(self):
        if not self.rodando:
            return
        self.sim.axelrod = self.var_axl.get()
        self.sim.passo()
        self.desenhar()
        atraso = int(1050 - self.var_vel.get() * 100)  # 1 -> ~950ms, 10 -> ~50ms
        self.root.after(atraso, self.loop)

    def clique(self, ev):
        p = (ev.y // self.celula, ev.x // self.celula)
        self.selecionado = self.sim.grade.get(p)
        self.desenhar()

    def visualizar_distribuicao_inicial(self):
        janela = tk.Toplevel(self.root)
        janela.title("Distribuição inicial da matriz")
        cv = tk.Canvas(janela, width=TAMANHO * self.celula, height=TAMANHO * self.celula,
                       bg="#f4f4f4", highlightthickness=1, highlightbackground="#888")
        cv.pack(padx=10, pady=10)

        for i in range(TAMANHO + 1):
            cv.create_line(0, i * self.celula, TAMANHO * self.celula,
                           i * self.celula, fill="#d0d0d0")
            cv.create_line(i * self.celula, 0, i * self.celula,
                           TAMANHO * self.celula, fill="#d0d0d0")

        centro = TAMANHO // 2 * self.celula
        cv.create_rectangle(centro, centro, centro + self.celula, centro + self.celula,
                            outline="#19745f", width=2, dash=(4, 2))
        raio = self.celula * 0.36
        for ident, pos, curso, origem in self.sim.distribuicao_inicial:
            x, y = self.centro(pos)
            cv.create_oval(x - raio, y - raio, x + raio, y + raio,
                           fill=COR_CURSO[curso], outline=COR_ORIGEM[origem], width=4)
            cv.create_text(x, y, text=str(ident), font=("Arial", 9, "bold"))

    # ---- desenho
    def centro(self, p):
        return (p[1] * self.celula + self.celula / 2,
            p[0] * self.celula + self.celula / 2)

    def desenhar(self):
        s, cv = self.sim, self.canvas
        cv.delete("all")
        for i in range(TAMANHO + 1):
            cv.create_line(0, i * self.celula, TAMANHO * self.celula,
                           i * self.celula, fill="#d0d0d0")
            cv.create_line(i * self.celula, 0, i * self.celula,
                           TAMANHO * self.celula, fill="#d0d0d0")

        centro = TAMANHO // 2 * self.celula
        cv.create_rectangle(centro, centro, centro + self.celula, centro + self.celula,
                            outline="#19745f", width=2, dash=(4, 2))
        if s.ultimo_movimento:
            (x0, y0), (x1, y1) = self.centro(s.ultimo_movimento[0]), self.centro(s.ultimo_movimento[1])
            cv.create_line(x0, y0, x1, y1, fill="#444", dash=(3, 3), arrow=tk.LAST)

        raio = self.celula * 0.36
        for a in s.agentes:
            x, y = self.centro(a.pos)
            cv.create_oval(x - raio, y - raio, x + raio, y + raio,
                           fill=COR_CURSO[a.curso], outline=COR_ORIGEM[a.origem], width=4)
            cv.create_text(x, y, text=str(a.id), font=("Arial", 9, "bold"))
            if a is s.influenciador:
                cv.create_text(x + raio, y - raio, text="★", fill="#d4a000", font=("Arial", 14, "bold"))
            elif a in s.lideres:
                cv.create_text(x + raio, y - raio, text="◆", fill="#333", font=("Arial", 11, "bold"))

        if s.ativo:
            x, y = self.centro(s.ativo.pos)
            r = self.celula * 0.46
            cv.create_oval(x - r, y - r, x + r, y + r, outline="red", width=2)
        if self.selecionado and self.selecionado in s.agentes:
            x, y = self.centro(self.selecionado.pos)
            r = self.celula * 0.48
            cv.create_rectangle(x - r, y - r, x + r, y + r, outline="#0a0", width=2)

        self.atualizar_textos()

    def atualizar_textos(self):
        s = self.sim
        self.lbl_stats.config(text=(
            f"Agentes: {len(s.agentes)}\n"
            f"Ano: {s.ano}  |  Rodada: {s.rodada}\n"
            f"Grupos (≥2 agentes): {s.n_grupos}\n"
            f"Similaridade média entre vizinhos: {s.similaridade_media_vizinhos():.0%}"))

        a = self.selecionado or s.ativo
        if a:
            tag = "selecionado" if self.selecionado else "ativo na rodada"
            self.lbl_agente.config(text=(
                f"Agente {a.id} ({tag})\n"
                f"Sexo: {a.sexo}\nPeríodo: {a.periodo}º\nCurso: {a.curso}\n"
                f"Religião: {a.religiao}\nOrigem: {a.origem}\nPosição: {a.pos}"))
        else:
            self.lbl_agente.config(text="Clique em um agente ou inicie a simulação.")
        conteudo = "\n".join(s.historico_eventos[-80:]) or "Nenhum período executado."
        self.txt_eventos.configure(state="normal")
        self.txt_eventos.delete("1.0", "end")
        self.txt_eventos.insert("end", conteudo)
        self.txt_eventos.see("end")
        self.txt_eventos.configure(state="disabled")


if __name__ == "__main__":
    janela = tk.Tk()
    App(janela)
    janela.mainloop()