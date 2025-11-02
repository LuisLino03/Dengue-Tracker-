import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import Database

class TelaVisualizacao:
    def __init__(self, parent, db, app_instance):
        self.parent = parent
        self.db = db
        self.app_instance = app_instance
        self.janela = tk.Toplevel(parent)
        self.janela.title("Visualizar Ocorrências - Detalhes Completos")
        self.janela.geometry("1400x700")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Configurar estilo
        self.configurar_estilo()
        
        self.ocorrencia_selecionada = None
        self.criar_widgets()
        self.carregar_ocorrencias()
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'))
    
    def criar_widgets(self):
        # Notebook (abas) para organizar a visualização
        notebook = ttk.Notebook(self.janela)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba 1: Lista de Ocorrências
        frame_lista = ttk.Frame(notebook)
        notebook.add(frame_lista, text="Lista de Ocorrências")
        
        # Aba 2: Detalhes da Ocorrência
        frame_detalhes = ttk.Frame(notebook)
        notebook.add(frame_detalhes, text="Detalhes da Ocorrência")
        
        self.criar_aba_lista(frame_lista)
        self.criar_aba_detalhes(frame_detalhes)
    
    def criar_aba_lista(self, parent):
        # Frame para filtros
        frame_filtros = ttk.LabelFrame(parent, text="Filtrar Ocorrências", padding=15)
        frame_filtros.pack(fill="x", padx=10, pady=5)
        
        # Linha 1 de filtros
        frame_filtros_linha1 = ttk.Frame(frame_filtros)
        frame_filtros_linha1.pack(fill="x", pady=5)
        
        ttk.Label(frame_filtros_linha1, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_filtro_nome = ttk.Entry(frame_filtros_linha1, width=20)
        self.entry_filtro_nome.grid(row=0, column=1, padx=5, pady=2)
        self.entry_filtro_nome.bind('<KeyRelease>', lambda e: self.aplicar_filtros())
        
        ttk.Label(frame_filtros_linha1, text="Bairro:").grid(row=0, column=2, sticky="w", padx=15, pady=2)
        self.entry_filtro_bairro = ttk.Entry(frame_filtros_linha1, width=15)
        self.entry_filtro_bairro.grid(row=0, column=3, padx=5, pady=2)
        self.entry_filtro_bairro.bind('<KeyRelease>', lambda e: self.aplicar_filtros())
        
        ttk.Label(frame_filtros_linha1, text="Quarterão:").grid(row=0, column=4, sticky="w", padx=15, pady=2)
        self.entry_filtro_quarterao = ttk.Entry(frame_filtros_linha1, width=10)
        self.entry_filtro_quarterao.grid(row=0, column=5, padx=5, pady=2)
        self.entry_filtro_quarterao.bind('<KeyRelease>', lambda e: self.aplicar_filtros())
        
        # Linha 2 de filtros
        frame_filtros_linha2 = ttk.Frame(frame_filtros)
        frame_filtros_linha2.pack(fill="x", pady=5)
        
        ttk.Label(frame_filtros_linha2, text="SINAN:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_filtro_sinan = ttk.Entry(frame_filtros_linha2, width=15)
        self.entry_filtro_sinan.grid(row=0, column=1, padx=5, pady=2)
        self.entry_filtro_sinan.bind('<KeyRelease>', lambda e: self.aplicar_filtros())
        
        ttk.Label(frame_filtros_linha2, text="Doença:").grid(row=0, column=2, sticky="w", padx=15, pady=2)
        self.combo_filtro_doenca = ttk.Combobox(frame_filtros_linha2, width=15, 
                                              values=["", "Dengue", "Zika", "Chikungunya"])
        self.combo_filtro_doenca.grid(row=0, column=3, padx=5, pady=2)
        self.combo_filtro_doenca.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())
        
        # Botões de filtro
        frame_botoes_filtro = ttk.Frame(frame_filtros)
        frame_botoes_filtro.pack(pady=10)
        
        btn_limpar_filtros = ttk.Button(frame_botoes_filtro, text="Limpar Filtros", command=self.limpar_filtros)
        btn_limpar_filtros.pack(side="left", padx=5)
        
        btn_atualizar = ttk.Button(frame_botoes_filtro, text="Atualizar Lista", command=self.carregar_ocorrencias)
        btn_atualizar.pack(side="left", padx=5)
        
        # Frame para listagem
        frame_lista_ocorrencias = ttk.LabelFrame(parent, text="Ocorrências Cadastradas", padding=10)
        frame_lista_ocorrencias.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview para exibir as ocorrências
        columns = ('id', 'sinan', 'nome', 'data_nascimento', 'bairro', 'tipo_doenca', 'resultado', 'classificacao', 'data_criacao')
        self.tree = ttk.Treeview(frame_lista_ocorrencias, columns=columns, show='headings', height=15)
        
        # Definindo cabeçalhos
        self.tree.heading('id', text='ID')
        self.tree.heading('sinan', text='SINAN')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('data_nascimento', text='Data Nasc.')
        self.tree.heading('bairro', text='Bairro')
        self.tree.heading('tipo_doenca', text='Tipo Doença')
        self.tree.heading('resultado', text='Resultado')
        self.tree.heading('classificacao', text='Classificação')
        self.tree.heading('data_criacao', text='Data Criação')
        
        # Definindo largura das colunas
        self.tree.column('id', width=40, anchor='center')
        self.tree.column('sinan', width=80, anchor='center')
        self.tree.column('nome', width=150, anchor='w')
        self.tree.column('data_nascimento', width=90, anchor='center')
        self.tree.column('bairro', width=120, anchor='w')
        self.tree.column('tipo_doenca', width=100, anchor='center')
        self.tree.column('resultado', width=90, anchor='center')
        self.tree.column('classificacao', width=100, anchor='center')
        self.tree.column('data_criacao', width=110, anchor='center')
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_lista_ocorrencias, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_lista_ocorrencias, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Configurar weights para expansão
        frame_lista_ocorrencias.grid_rowconfigure(0, weight=1)
        frame_lista_ocorrencias.grid_columnconfigure(0, weight=1)
        
        # Frame para botões de ação
        frame_botoes = ttk.Frame(frame_lista_ocorrencias)
        frame_botoes.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botões de ação
        btn_ver_detalhes = ttk.Button(frame_botoes, text="Ver Detalhes", command=self.ver_detalhes)
        btn_ver_detalhes.pack(side="left", padx=5)
        
        btn_editar = ttk.Button(frame_botoes, text="Editar Selecionada", command=self.editar_ocorrencia)
        btn_editar.pack(side="left", padx=5)
        
        btn_excluir = ttk.Button(frame_botoes, text="Excluir Selecionada", command=self.excluir_ocorrencia)
        btn_excluir.pack(side="left", padx=5)
        
        btn_fechar = ttk.Button(frame_botoes, text="Fechar", command=self.janela.destroy)
        btn_fechar.pack(side="left", padx=5)
        
        # Bind duplo clique para ver detalhes
        self.tree.bind("<Double-1>", lambda event: self.ver_detalhes())
    
    def criar_aba_detalhes(self, parent):
        # Frame principal para detalhes
        frame_detalhes = ttk.Frame(parent)
        frame_detalhes.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas com scrollbar para os detalhes
        canvas = tk.Canvas(frame_detalhes)
        scrollbar = ttk.Scrollbar(frame_detalhes, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        self.label_titulo_detalhes = ttk.Label(scrollable_frame, text="Selecione uma ocorrência para ver os detalhes", 
                                              style='Title.TLabel')
        self.label_titulo_detalhes.pack(pady=15)
        
        # Frame para dados epidemiológicos
        frame_dados_epidemiologicos = ttk.LabelFrame(scrollable_frame, text="Dados Epidemiológicos", padding=15)
        frame_dados_epidemiologicos.pack(fill="x", padx=10, pady=5)
        
        # Grid para dados epidemiológicos
        labels_epidemiologicos = [
            ("SINAN:", "label_sinan"), ("Data Notificação:", "label_data_notificacao"),
            ("Início Sintoma:", "label_inicio_sintoma"), ("Data Exame:", "label_data_exame"),
            ("Tipo Exame:", "label_tipo_exame"), ("Resultado:", "label_resultado"),
            ("Tipo Doença:", "label_tipo_doenca"), ("Classificação:", "label_classificacao"),
            ("Data Resultado:", "label_data_resultado"), ("CC:", "label_cc"), 
            ("NP:", "label_np"), ("Sinais de Alerta:", "label_sinais_alerta")
        ]
        
        for i, (texto, attr_name) in enumerate(labels_epidemiologicos):
            ttk.Label(frame_dados_epidemiologicos, text=texto, style='Header.TLabel').grid(
                row=i//2, column=(i%2)*2, sticky="w", padx=10, pady=3)
            label = ttk.Label(frame_dados_epidemiologicos, text="", wraplength=300)
            label.grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=10, pady=3)
            setattr(self, attr_name, label)
        
        # Frame para dados pessoais
        frame_dados_pessoais = ttk.LabelFrame(scrollable_frame, text="Dados Pessoais", padding=15)
        frame_dados_pessoais.pack(fill="x", padx=10, pady=10)
        
        # Labels para dados pessoais
        labels_pessoais = [
            ("Nome:", "label_nome"), ("Data Nascimento:", "label_data_nascimento"),
            ("Logradouro:", "label_logradouro"), ("Número:", "label_numero"),
            ("Bairro:", "label_bairro"), ("Quarterão:", "label_quarterao")
        ]
        
        for i, (texto, attr_name) in enumerate(labels_pessoais):
            ttk.Label(frame_dados_pessoais, text=texto, style='Header.TLabel').grid(
                row=i//2, column=(i%2)*2, sticky="w", padx=10, pady=3)
            label = ttk.Label(frame_dados_pessoais, text="", wraplength=300)
            label.grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=10, pady=3)
            setattr(self, attr_name, label)
        
        # Frame para dados do sistema
        frame_dados_sistema = ttk.LabelFrame(scrollable_frame, text="Dados do Sistema", padding=15)
        frame_dados_sistema.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_dados_sistema, text="Data de Criação:", style='Header.TLabel').grid(
            row=0, column=0, sticky="w", padx=10, pady=3)
        self.label_data_criacao = ttk.Label(frame_dados_sistema, text="")
        self.label_data_criacao.grid(row=0, column=1, sticky="w", padx=10, pady=3)
        
        # Botão para voltar à lista
        btn_voltar = ttk.Button(scrollable_frame, text="Voltar à Lista", command=self.voltar_lista)
        btn_voltar.pack(pady=15)
    
    def voltar_lista(self):
        # Voltar para a aba de lista
        notebook = self.janela.winfo_children()[0]
        notebook.select(0)
    
    def ver_detalhes(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione uma ocorrência para ver os detalhes!")
            return
        
        item = selecionado[0]
        id_ocorrencia = self.tree.item(item, 'values')[0]
        
        # Buscar dados completos da ocorrência
        ocorrencia_completa = self.db.buscar_ocorrencia_por_id(id_ocorrencia)
        
        if ocorrencia_completa:
            self.ocorrencia_selecionada = ocorrencia_completa
            self.mostrar_detalhes(ocorrencia_completa)
            
            # Mudar para a aba de detalhes
            notebook = self.janela.winfo_children()[0]
            notebook.select(1)
    
    def mostrar_detalhes(self, ocorrencia):
        (id_ocorrencia, sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
         tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
         nome, data_nascimento, logradouro, numero, bairro, quarterao, data_criacao) = ocorrencia
        
        # Atualizar título
        self.label_titulo_detalhes.config(text=f"Detalhes da Ocorrência - ID: {id_ocorrencia}")
        
        # Dados epidemiológicos
        self.label_sinan.config(text=sinan or "Não informado")
        self.label_data_notificacao.config(text=data_notificacao or "Não informado")
        self.label_inicio_sintoma.config(text=inicio_sintoma or "Não informado")
        self.label_data_exame.config(text=data_exame or "Não informado")
        self.label_tipo_exame.config(text=tipo_exame or "Não informado")
        self.label_resultado.config(text=resultado or "Não informado")
        self.label_tipo_doenca.config(text=tipo_doenca or "Não informado")
        self.label_classificacao.config(text=classificacao or "Não informado")
        self.label_data_resultado.config(text=data_resultado or "Não informado")
        self.label_cc.config(text=cc or "Não informado")
        self.label_np.config(text=np or "Não informado")
        self.label_sinais_alerta.config(text=sinais_alerta or "Não informado")
        
        # Dados pessoais
        self.label_nome.config(text=nome or "Não informado")
        self.label_data_nascimento.config(text=data_nascimento or "Não informado")
        self.label_logradouro.config(text=logradouro or "Não informado")
        self.label_numero.config(text=numero or "Não informado")
        self.label_bairro.config(text=bairro or "Não informado")
        self.label_quarterao.config(text=quarterao or "Não informado")
        
        # Dados do sistema
        self.label_data_criacao.config(text=data_criacao or "Não informado")
    
    def aplicar_filtros(self):
        filtro_nome = self.entry_filtro_nome.get().strip()
        filtro_bairro = self.entry_filtro_bairro.get().strip()
        filtro_quarterao = self.entry_filtro_quarterao.get().strip()
        filtro_sinan = self.entry_filtro_sinan.get().strip()
        filtro_doenca = self.combo_filtro_doenca.get().strip()
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aplicar filtros
        ocorrencias = self.db.buscar_ocorrencias()
        
        for ocorrencia in ocorrencias:
            (id_ocorrencia, sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
             tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
             nome, data_nascimento, logradouro, numero, bairro, quarterao, data_criacao) = ocorrencia
            
            # Verificar se a ocorrência atende aos filtros
            match_nome = not filtro_nome or filtro_nome.lower() in (nome or '').lower()
            match_bairro = not filtro_bairro or filtro_bairro.lower() in (bairro or '').lower()
            match_quarterao = not filtro_quarterao or filtro_quarterao.lower() in (quarterao or '').lower()
            match_sinan = not filtro_sinan or filtro_sinan.lower() in (sinan or '').lower()
            match_doenca = not filtro_doenca or filtro_doenca.lower() in (tipo_doenca or '').lower()
            
            if match_nome and match_bairro and match_quarterao and match_sinan and match_doenca:
                self.tree.insert('', 'end', values=(
                    id_ocorrencia, sinan, nome, data_nascimento, bairro,
                    tipo_doenca, resultado, classificacao, data_criacao
                ))
    
    def limpar_filtros(self):
        self.entry_filtro_nome.delete(0, tk.END)
        self.entry_filtro_bairro.delete(0, tk.END)
        self.entry_filtro_quarterao.delete(0, tk.END)
        self.entry_filtro_sinan.delete(0, tk.END)
        self.combo_filtro_doenca.set("")
        self.carregar_ocorrencias()
    
    def carregar_ocorrencias(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar ocorrências do banco
        ocorrencias = self.db.buscar_ocorrencias()
        
        # Adicionar à treeview
        for ocorrencia in ocorrencias:
            (id_ocorrencia, sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
             tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
             nome, data_nascimento, logradouro, numero, bairro, quarterao, data_criacao) = ocorrencia
            
            self.tree.insert('', 'end', values=(
                id_ocorrencia, sinan, nome, data_nascimento, bairro,
                tipo_doenca, resultado, classificacao, data_criacao
            ))
    
    def editar_ocorrencia(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione uma ocorrência para editar!")
            return
        
        item = selecionado[0]
        id_ocorrencia = self.tree.item(item, 'values')[0]
        
        # Buscar dados completos da ocorrência
        ocorrencia_completa = self.db.buscar_ocorrencia_por_id(id_ocorrencia)
        
        if ocorrencia_completa:
            # Fechar janela de visualização e abrir edição na janela principal
            self.janela.destroy()
            self.app_instance.editar_ocorrencia_direto(*ocorrencia_completa)
    
    def excluir_ocorrencia(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione uma ocorrência para excluir!")
            return
        
        item = selecionado[0]
        id_ocorrencia = self.tree.item(item, 'values')[0]
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta ocorrência?"):
            try:
                self.db.excluir_ocorrencia(id_ocorrencia)
                messagebox.showinfo("Sucesso", "Ocorrência excluída com sucesso!")
                self.carregar_ocorrencias()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir ocorrência: {str(e)}")

class OcorrenciasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Notificação Epidemiológica")
        self.root.geometry("1100x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo
        self.configurar_estilo()
        
        self.db = Database()
        self.ocorrencia_editando = None
        
        self.criar_widgets()
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores e fontes
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'), foreground='#2c3e50')
        style.configure('Section.TLabelframe.Label', font=('Arial', 12, 'bold'), foreground='#34495e')
        
        # Configurar Labelframes
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', background='#f0f0f0')
    
    def criar_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Notificação Epidemiológica", 
                          style='Title.TLabel')
        titulo.pack(pady=(0, 20))
        
        # Container principal com grid para melhor organização
        container = ttk.Frame(main_frame)
        container.pack(fill="both", expand=True)
        
        # Frame para dados epidemiológicos
        frame_epidemiologicos = ttk.LabelFrame(container, text="Dados Epidemiológicos", 
                                             padding=20, style='Section.TLabelframe')
        frame_epidemiologicos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Grid para dados epidemiológicos - 4 colunas
        # Linha 1
        ttk.Label(frame_epidemiologicos, text="SINAN *", style='Header.TLabel').grid(
            row=0, column=0, sticky="w", padx=10, pady=8)
        self.entry_sinan = ttk.Entry(frame_epidemiologicos, width=20, font=('Arial', 10))
        self.entry_sinan.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_epidemiologicos, text="Data Notificação *", style='Header.TLabel').grid(
            row=0, column=2, sticky="w", padx=10, pady=8)
        self.entry_data_notificacao = ttk.Entry(frame_epidemiologicos, width=15, font=('Arial', 10))
        self.entry_data_notificacao.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        self.entry_data_notificacao.insert(0, datetime.now().strftime('%d/%m/%Y'))
        
        # Linha 2
        ttk.Label(frame_epidemiologicos, text="Início Sintoma", style='Header.TLabel').grid(
            row=1, column=0, sticky="w", padx=10, pady=8)
        self.entry_inicio_sintoma = ttk.Entry(frame_epidemiologicos, width=15, font=('Arial', 10))
        self.entry_inicio_sintoma.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_epidemiologicos, text="Data Exame", style='Header.TLabel').grid(
            row=1, column=2, sticky="w", padx=10, pady=8)
        self.entry_data_exame = ttk.Entry(frame_epidemiologicos, width=15, font=('Arial', 10))
        self.entry_data_exame.grid(row=1, column=3, padx=10, pady=8, sticky="w")
        
        # Linha 3
        ttk.Label(frame_epidemiologicos, text="Tipo de Exame", style='Header.TLabel').grid(
            row=2, column=0, sticky="w", padx=10, pady=8)
        self.combo_tipo_exame = ttk.Combobox(frame_epidemiologicos, width=18, 
                                           values=["", "NS1", "Sorologia", "PCR"],
                                           state="readonly", font=('Arial', 10))
        self.combo_tipo_exame.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_epidemiologicos, text="Resultado", style='Header.TLabel').grid(
            row=2, column=2, sticky="w", padx=10, pady=8)
        self.combo_resultado = ttk.Combobox(frame_epidemiologicos, width=18, 
                                          values=["", "Positivo", "Negativo", "Inconclusivo"],
                                          state="readonly", font=('Arial', 10))
        self.combo_resultado.grid(row=2, column=3, padx=10, pady=8, sticky="w")
        
        # Linha 4
        ttk.Label(frame_epidemiologicos, text="Tipo de Doença", style='Header.TLabel').grid(
            row=3, column=0, sticky="w", padx=10, pady=8)
        self.combo_tipo_doenca = ttk.Combobox(frame_epidemiologicos, width=18, 
                                            values=["", "Dengue", "Zika", "Chikungunya"],
                                            state="readonly", font=('Arial', 10))
        self.combo_tipo_doenca.grid(row=3, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_epidemiologicos, text="Classificação", style='Header.TLabel').grid(
            row=3, column=2, sticky="w", padx=10, pady=8)
        self.combo_classificacao = ttk.Combobox(frame_epidemiologicos, width=18, 
                                              values=["", "Autóctone", "Importada"],
                                              state="readonly", font=('Arial', 10))
        self.combo_classificacao.grid(row=3, column=3, padx=10, pady=8, sticky="w")
        
        # Linha 5
        ttk.Label(frame_epidemiologicos, text="Data Resultado", style='Header.TLabel').grid(
            row=4, column=0, sticky="w", padx=10, pady=8)
        self.entry_data_resultado = ttk.Entry(frame_epidemiologicos, width=15, font=('Arial', 10))
        self.entry_data_resultado.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_epidemiologicos, text="Sinais de Alerta", style='Header.TLabel').grid(
            row=4, column=2, sticky="w", padx=10, pady=8)
        self.combo_sinais_alerta = ttk.Combobox(frame_epidemiologicos, width=18, 
                                              values=["", "Leve", "Moderado", "Grave", "Óbito"],
                                              state="readonly", font=('Arial', 10))
        self.combo_sinais_alerta.grid(row=4, column=3, padx=10, pady=8, sticky="w")
        
        # Linha 6
        ttk.Label(frame_epidemiologicos, text="CC", style='Header.TLabel').grid(
            row=5, column=0, sticky="w", padx=10, pady=8)
        self.entry_cc = ttk.Entry(frame_epidemiologicos, width=15, font=('Arial', 10))
        self.entry_cc.grid(row=5, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_epidemiologicos, text="NP", style='Header.TLabel').grid(
            row=5, column=2, sticky="w", padx=10, pady=8)
        self.entry_np = ttk.Entry(frame_epidemiologicos, width=15, font=('Arial', 10))
        self.entry_np.grid(row=5, column=3, padx=10, pady=8, sticky="w")
        
        # Frame para dados pessoais
        frame_pessoais = ttk.LabelFrame(container, text="Dados Pessoais", 
                                      padding=20, style='Section.TLabelframe')
        frame_pessoais.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Grid para dados pessoais - 4 colunas
        # Linha 1
        ttk.Label(frame_pessoais, text="Nome *", style='Header.TLabel').grid(
            row=0, column=0, sticky="w", padx=10, pady=8)
        self.entry_nome = ttk.Entry(frame_pessoais, width=30, font=('Arial', 10))
        self.entry_nome.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_pessoais, text="Data Nascimento *", style='Header.TLabel').grid(
            row=0, column=2, sticky="w", padx=10, pady=8)
        self.entry_data_nascimento = ttk.Entry(frame_pessoais, width=15, font=('Arial', 10))
        self.entry_data_nascimento.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        self.entry_data_nascimento.insert(0, datetime.now().strftime('%d/%m/%Y'))
        
        # Linha 2
        ttk.Label(frame_pessoais, text="Logradouro *", style='Header.TLabel').grid(
            row=1, column=0, sticky="w", padx=10, pady=8)
        self.entry_logradouro = ttk.Entry(frame_pessoais, width=30, font=('Arial', 10))
        self.entry_logradouro.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_pessoais, text="Número *", style='Header.TLabel').grid(
            row=1, column=2, sticky="w", padx=10, pady=8)
        self.entry_numero = ttk.Entry(frame_pessoais, width=15, font=('Arial', 10))
        self.entry_numero.grid(row=1, column=3, padx=10, pady=8, sticky="w")
        
        # Linha 3
        ttk.Label(frame_pessoais, text="Bairro *", style='Header.TLabel').grid(
            row=2, column=0, sticky="w", padx=10, pady=8)
        self.entry_bairro = ttk.Entry(frame_pessoais, width=30, font=('Arial', 10))
        self.entry_bairro.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        
        ttk.Label(frame_pessoais, text="Quarterão *", style='Header.TLabel').grid(
            row=2, column=2, sticky="w", padx=10, pady=8)
        self.entry_quarterao = ttk.Entry(frame_pessoais, width=15, font=('Arial', 10))
        self.entry_quarterao.grid(row=2, column=3, padx=10, pady=8, sticky="w")
        
        # Frame para botões
        frame_botoes = ttk.Frame(container)
        frame_botoes.grid(row=2, column=0, sticky="ew", pady=20)
        
        # Botões centralizados
        btn_frame = ttk.Frame(frame_botoes)
        btn_frame.pack(expand=True)
        
        self.btn_cadastrar = ttk.Button(btn_frame, text="Cadastrar Ocorrência", 
                                      command=self.cadastrar_ocorrencia, width=20)
        self.btn_cadastrar.pack(side="left", padx=10)
        
        self.btn_cancelar_edicao = ttk.Button(btn_frame, text="Cancelar Edição", 
                                            command=self.cancelar_edicao, state="disabled", width=15)
        self.btn_cancelar_edicao.pack(side="left", padx=10)
        
        btn_visualizar = ttk.Button(btn_frame, text="Visualizar Ocorrências", 
                                  command=self.abrir_visualizacao, width=20)
        btn_visualizar.pack(side="left", padx=10)
        
        # Configurar weights para responsividade
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
    
    def abrir_visualizacao(self):
        TelaVisualizacao(self.root, self.db, self)
    
    def editar_ocorrencia_direto(self, id_ocorrencia, sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
                               tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
                               nome, data_nascimento, logradouro, numero, bairro, quarterao, data_criacao):
        """Método chamado pela tela de visualização para editar uma ocorrência"""
        # Campos epidemiológicos
        self.entry_sinan.delete(0, tk.END)
        self.entry_sinan.insert(0, sinan or "")
        
        self.entry_data_notificacao.delete(0, tk.END)
        self.entry_data_notificacao.insert(0, data_notificacao or "")
        
        self.entry_inicio_sintoma.delete(0, tk.END)
        self.entry_inicio_sintoma.insert(0, inicio_sintoma or "")
        
        self.entry_data_exame.delete(0, tk.END)
        self.entry_data_exame.insert(0, data_exame or "")
        
        self.combo_tipo_exame.set(tipo_exame or "")
        
        self.combo_resultado.set(resultado or "")
        
        self.combo_tipo_doenca.set(tipo_doenca or "")
        
        self.combo_classificacao.set(classificacao or "")
        
        self.entry_data_resultado.delete(0, tk.END)
        self.entry_data_resultado.insert(0, data_resultado or "")
        
        self.entry_cc.delete(0, tk.END)
        self.entry_cc.insert(0, cc or "")
        
        self.entry_np.delete(0, tk.END)
        self.entry_np.insert(0, np or "")
        
        self.combo_sinais_alerta.set(sinais_alerta or "")
        
        # Dados pessoais
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        
        self.entry_data_nascimento.delete(0, tk.END)
        self.entry_data_nascimento.insert(0, data_nascimento)
        
        self.entry_logradouro.delete(0, tk.END)
        self.entry_logradouro.insert(0, logradouro)
        
        self.entry_numero.delete(0, tk.END)
        self.entry_numero.insert(0, numero)
        
        self.entry_bairro.delete(0, tk.END)
        self.entry_bairro.insert(0, bairro)
        
        self.entry_quarterao.delete(0, tk.END)
        self.entry_quarterao.insert(0, quarterao)
        
        # Configurar modo de edição
        self.ocorrencia_editando = id_ocorrencia
        self.btn_cadastrar.config(text="Atualizar Ocorrência")
        self.btn_cancelar_edicao.config(state="enabled")
    
    def cadastrar_ocorrencia(self):
        # Dados epidemiológicos
        sinan = self.entry_sinan.get().strip()
        data_notificacao = self.entry_data_notificacao.get().strip()
        inicio_sintoma = self.entry_inicio_sintoma.get().strip()
        data_exame = self.entry_data_exame.get().strip()
        tipo_exame = self.combo_tipo_exame.get().strip()
        resultado = self.combo_resultado.get().strip()
        tipo_doenca = self.combo_tipo_doenca.get().strip()
        classificacao = self.combo_classificacao.get().strip()
        data_resultado = self.entry_data_resultado.get().strip()
        cc = self.entry_cc.get().strip()
        np = self.entry_np.get().strip()
        sinais_alerta = self.combo_sinais_alerta.get().strip()
        
        # Dados pessoais
        nome = self.entry_nome.get().strip()
        data_nascimento = self.entry_data_nascimento.get().strip()
        logradouro = self.entry_logradouro.get().strip()
        numero = self.entry_numero.get().strip()
        bairro = self.entry_bairro.get().strip()
        quarterao = self.entry_quarterao.get().strip()
        
        # Validar campos obrigatórios
        if not all([sinan, data_notificacao, nome, data_nascimento, logradouro, numero, bairro, quarterao]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios (*)!")
            return
        
        try:
            if self.ocorrencia_editando:
                # Modo edição
                self.db.atualizar_ocorrencia(self.ocorrencia_editando, sinan, data_notificacao, inicio_sintoma,
                                           data_exame, tipo_exame, resultado, tipo_doenca, classificacao,
                                           data_resultado, cc, np, sinais_alerta, nome, data_nascimento,
                                           logradouro, numero, bairro, quarterao)
                messagebox.showinfo("Sucesso", "Ocorrência atualizada com sucesso!")
                self.cancelar_edicao()
            else:
                # Modo cadastro
                self.db.inserir_ocorrencia(sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame,
                                         resultado, tipo_doenca, classificacao, data_resultado, cc, np,
                                         sinais_alerta, nome, data_nascimento, logradouro, numero, bairro, quarterao)
                messagebox.showinfo("Sucesso", "Ocorrência cadastrada com sucesso!")
            
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar ocorrência: {str(e)}")
    
    def cancelar_edicao(self):
        self.ocorrencia_editando = None
        self.btn_cadastrar.config(text="Cadastrar Ocorrência")
        self.btn_cancelar_edicao.config(state="disabled")
        self.limpar_campos()
    
    def limpar_campos(self):
        # Limpar campos epidemiológicos
        self.entry_sinan.delete(0, tk.END)
        self.entry_data_notificacao.delete(0, tk.END)
        self.entry_data_notificacao.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.entry_inicio_sintoma.delete(0, tk.END)
        self.entry_data_exame.delete(0, tk.END)
        self.combo_tipo_exame.set("")
        self.combo_resultado.set("")
        self.combo_tipo_doenca.set("")
        self.combo_classificacao.set("")
        self.entry_data_resultado.delete(0, tk.END)
        self.entry_cc.delete(0, tk.END)
        self.entry_np.delete(0, tk.END)
        self.combo_sinais_alerta.set("")
        
        # Limpar campos pessoais
        self.entry_nome.delete(0, tk.END)
        self.entry_data_nascimento.delete(0, tk.END)
        self.entry_data_nascimento.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.entry_logradouro.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_quarterao.delete(0, tk.END)