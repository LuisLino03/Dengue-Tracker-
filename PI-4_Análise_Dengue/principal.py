from datetime import date, datetime
import pandas as pd
import streamlit as st
from database import Database
import plotly.express as px
import time

# Banco de dados
db = Database()

# Config pág. 
st.set_page_config(page_title="Sistema de Ocorrências", layout="wide")

# Lista dos bairros (Mococa)
BAIRROS = [
    "ALTOS DO VALE", "ALTOS DO VALE 2",  "ANITA VENTURI PRICOLI", "APARECIDA", "CONJ. HAB. ARY ESTEVAO", "BRÁS",
    "CENTRO", "RESIDENCIAL CARLITO QUILICI", "CDHU", "CECAP I", "CECAP II", "CHÁCARA BELA VISTA",
    "JARDIM CHICO PISCINA", "CLUBE DO VALE", "CONJ HABIT GABRIEL DO O", "CONJ. HAB. GILBERTO ROSSETTI",
    "COLINA VERDE", "CONDOMINIO MONTE BELO", "DESCANSO", "DISTRITO INDUSTRIAL 2", "FRANCISCO GARÓFALO",
    "GILDO GERALDO", "IGARAI", "JARDIM ALVORADA", "JD. BIANCHESI", "JD. DAS FIGUEIRAS", "JARDIM LAVINIA",
    "JD. MIGUEL GOMES", "JARDIM NOVA MOCOCA", "JD. PROGRESSO", "JD. RECREIO", "JD. RIGOBELLO",
    "JD. SANTA LUZIA", "SANTA TEREZINHA I", "JD. SÃO BENEDITO", "JARDIM SAO FRANCISCO", "JARDIM SAO JOSE",
    "JD. SÃO LUIZ", "JARDIM BOTANICO", "JOSÉ ANDRÉ DE LIMA", "JARDIM JOSE JUSTI", "MOCOQUINHA",
    "JARDIM MORRO AZUL", "CONJUNTO HABITACIONAL NELSON NIERO", "NENE PEREIRA LIMA", "PALMERINHA",
    "PARQUE CANOAS", "JARDIM PLANALTO VERDE", "BAIRRO POR DO SOL", "PRIMAVERA", "PROJETO CEM",
    "RESIDENCIAL DO BOSQUE", "RIACHUELO", "RURAL", "SAMAMBAIA", "JARDIM SANTA CECILIA",
    "SANTA CLARA", "SANTA CRUZ", "SANTA EMÍLIA", "JARDIM SANTA MARIA", "VILA SANTA ROSA",
    "SANTA MARINA", "SÃO BENEDITO DAS AREIAS", "CHACARAS SAO DOMINGOS", "VILA CARVALHO", "VILA LAMBARI",
    "VILA MARIA", "VILA MARIANA", "VILA NAUFEL", "DISTRITO INDUSTRIAL II", "JARDIM IMPERADOR",
    "RESIDENCIAL MAIS PARQUE", "VILA QUINTINO"
]

hoje = date.today()

# ABAS do projeto
tab_cadastro, tab_banco, tab_graficos = st.tabs(["Cadastro", "Banco", "Gráficos"])

# -------------------- ABA CADASTRO --------------------
with tab_cadastro:
    st.title("📋 Cadastro de Ocorrências")
    st.markdown("Preencha os dados epidemiológicos e pessoais do paciente.")

    with st.form("form_ocorrencia", clear_on_submit=True):
        st.subheader("Dados Epidemiológicos")
        col1, col2, col3 = st.columns(3)
        with col1:
            sinan = st.text_input("SINAN")
            data_notificacao = st.date_input(
                "Data de Notificação", value=None, min_value=date(1900,1,1), max_value=date.today(),
                format="DD/MM/YYYY"
            )
            inicio_sintoma = st.date_input(
                "Início dos Sintomas", value=None, min_value=date(1900,1,1), max_value=date.today(),
                format="DD/MM/YYYY"
            )
            cc = st.date_input(
                "CC", value=None, min_value=date(1900,1,1), max_value=date.today(), format="DD/MM/YYYY"
            )
        with col2:
            data_exame = st.date_input(
                "Data do Exame", value=None, min_value=date(1900,1,1), max_value=date.today(),
                format="DD/MM/YYYY"
            )
            tipo_exame = st.selectbox("Tipo de Exame", ["", "NS1", "Sorologia", "PCR"])
            resultado = st.selectbox("Resultado", ["", "Positivo", "Negativo", "Inconclusivo"])
            np = st.date_input(
                "NP", value=None, min_value=date(1900,1,1), max_value=date.today(), format="DD/MM/YYYY"
            )
        with col3:
            tipo_doenca = st.selectbox("Tipo de Doença", ["", "Dengue", "Zika", "Chikungunya"])
            classificacao = st.selectbox("Classificação", ["", "Autóctone", "Importada"])
            data_resultado = st.date_input(
                "Data do Resultado", value=None, min_value=date(1900,1,1), max_value=date.today(),
                format="DD/MM/YYYY"
            )
            sinais_alerta = st.selectbox("Sinais de Alerta", ["", "Leve", "Moderada", "Grave", "Óbito"])

        st.subheader("Dados Pessoais")
        col1, col2, col3 = st.columns(3)
        with col1:
            nome = st.text_input("Nome")
            data_nascimento = st.date_input(
                "Data de Nascimento", value=None, min_value=date(1900,1,1), max_value=date.today(),
                format="DD/MM/YYYY"
            )
        with col2:
            logradouro = st.text_input("Logradouro")
            numero = st.text_input("Número")
        with col3:
            bairro = st.selectbox("Bairro", options=[""] + BAIRROS, index=0)
            quarterao = st.text_input("Quarteão")

        submitted = st.form_submit_button("Cadastrar Ocorrência")
if submitted:
    db.inserir_ocorrencia(
        sinan,
        data_notificacao.strftime("%d/%m/%Y") if data_notificacao else "",
        inicio_sintoma.strftime("%d/%m/%Y") if inicio_sintoma else "",
        data_exame.strftime("%d/%m/%Y") if data_exame else "",
        tipo_exame, resultado, tipo_doenca, classificacao,
        data_resultado.strftime("%d/%m/%Y") if data_resultado else "",
        cc.strftime("%d/%m/%Y") if cc else "",
        np.strftime("%d/%m/%Y") if np else "",
        sinais_alerta, nome,
        data_nascimento.strftime("%d/%m/%Y") if data_nascimento else "",
        logradouro, numero, bairro, quarterao
    )
    
    # Mensagem de finalização
    msg_placeholder = st.empty()
    msg_placeholder.success("✅ Ocorrência cadastrada com sucesso!")
    time.sleep(4)
    msg_placeholder.empty()
    
    st.session_state["updated"] = True


# -------------------- ABA BANCO --------------------
with tab_banco:
    st.title("📂 Banco de Ocorrências")

    if "ocorrencias" not in st.session_state or st.session_state.get("updated", False):
        st.session_state["ocorrencias"] = db.buscar_ocorrencias()
        st.session_state["updated"] = False

    filtros_keys = ["filtro_nome", "filtro_bairro", "filtro_quarteao", "filtro_sinan", "filtro_doenca"]
    for key in filtros_keys:
        if key not in st.session_state:
            st.session_state[key] = ""
    def limpar_filtros():
        for key in filtros_keys:
            st.session_state[key] = ""

    with st.expander("🔎 Filtros de Ocorrências", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.text_input("Nome", key="filtro_nome")
        col2.text_input("Bairro", key="filtro_bairro")
        col3.text_input("Quarteão", key="filtro_quarteao")
        col4.text_input("SINAN", key="filtro_sinan")
        col5.selectbox("Doença", ["", "Dengue", "Zika", "Chikungunya"], key="filtro_doenca")
        st.button("🧹 Limpar Filtros", on_click=limpar_filtros)

    df = pd.DataFrame(st.session_state["ocorrencias"], columns=[
        "ID","SINAN","Data Notificação","Início Sintomas","Data Exame","Tipo Exame","Resultado",
        "Tipo Doença","Classificação","Data Resultado","CC","NP","Sinais de Alerta",
        "Nome","Data Nascimento","Logradouro","Número","Bairro","Quarteão","Data Criação"
    ])

    # Datas em BR
    def format_date(dt):
        if dt is None or pd.isna(dt) or dt == "":
            return ""
        dt_parsed = pd.to_datetime(dt, dayfirst=True, errors='coerce')
        if pd.isna(dt_parsed):
            return ""
        return dt_parsed.strftime("%d/%m/%Y")

    for col in ["Data Notificação","Início Sintomas","Data Exame","Data Resultado",
                "CC","NP","Data Nascimento","Data Criação"]:
        df[col] = df[col].apply(format_date)

    # Filtros
    df_filtrado = df.copy()
    if st.session_state.filtro_nome:
        df_filtrado = df_filtrado[df_filtrado["Nome"].str.contains(st.session_state.filtro_nome, case=False, na=False)]
    if st.session_state.filtro_bairro:
        df_filtrado = df_filtrado[df_filtrado["Bairro"].str.contains(st.session_state.filtro_bairro, case=False, na=False)]
    if st.session_state.filtro_quarteao:
        df_filtrado = df_filtrado[df_filtrado["Quarteão"].str.contains(st.session_state.filtro_quarteao, case=False, na=False)]
    if st.session_state.filtro_sinan:
        df_filtrado = df_filtrado[df_filtrado["SINAN"].str.contains(st.session_state.filtro_sinan, case=False, na=False)]
    if st.session_state.filtro_doenca:
        df_filtrado = df_filtrado[df_filtrado["Tipo Doença"].str.contains(st.session_state.filtro_doenca, case=False, na=False)]

    if not df_filtrado.empty:
        st.markdown("### 📋 Ocorrências Cadastradas")
        todas_colunas = df_filtrado.columns.tolist()
        colunas_visiveis = ["ID","SINAN","Nome","Data Nascimento","Bairro","Tipo Doença","Resultado","Classificação","Data Criação"]
        colunas_mostrar = st.multiselect("Escolha colunas para exibir:", options=todas_colunas, default=colunas_visiveis)
        st.data_editor(df_filtrado[colunas_mostrar], hide_index=True, use_container_width=True, disabled=True, key="tabela_ocorrencias")
        st.markdown("---")
        st.subheader("⚙️ Ações")
        selected_ids = st.multiselect("Selecione uma ocorrência:", df_filtrado["ID"].tolist())

        if selected_ids:
            ocorrencia = db.buscar_ocorrencia_por_id(selected_ids[0])
            if ocorrencia:
                st.markdown("### 📑 Detalhes da Ocorrência")
                col_ep, col_pes = st.columns(2)
                with col_ep:
                    st.write("#### Dados Epidemiológicos")
                    st.write(f"SINAN: {ocorrencia[1]}")
                    st.write(f"Data Notificação: {format_date(ocorrencia[2])}")
                    st.write(f"Início Sintomas: {format_date(ocorrencia[3])}")
                    st.write(f"Data Exame: {format_date(ocorrencia[4])}")
                    st.write(f"Tipo Exame: {ocorrencia[5]}")
                    st.write(f"Resultado: {ocorrencia[6]}")
                    st.write(f"Tipo Doença: {ocorrencia[7]}")
                    st.write(f"Classificação: {ocorrencia[8]}")
                    st.write(f"Data Resultado: {format_date(ocorrencia[9])}")
                    st.write(f"CC: {format_date(ocorrencia[10])}")
                    st.write(f"NP: {format_date(ocorrencia[11])}")
                    st.write(f"Sinais de Alerta: {ocorrencia[12]}")
                with col_pes:
                    st.write("#### Dados Pessoais")
                    st.write(f"Nome: {ocorrencia[13]}")
                    st.write(f"Data Nascimento: {format_date(ocorrencia[14])}")
                    st.write(f"Logradouro: {ocorrencia[15]}")
                    st.write(f"Número: {ocorrencia[16]}")
                    st.write(f"Bairro: {ocorrencia[17]}")
                    st.write(f"Quarteão: {ocorrencia[18]}")
                    st.write(f"Data Criação: {format_date(ocorrencia[19])}")

                # ---------------- EDITAR / EXCLUIR ----------------
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Editar Selecionada"):
                        st.session_state["edit_id"] = ocorrencia[0]
                        st.session_state["edit_data"] = ocorrencia
                        st.session_state["show_edit_form"] = True
                with col2:
                    if st.button("🗑️ Excluir Selecionada"):
                        db.excluir_ocorrencia(ocorrencia[0])
                        st.session_state["ocorrencias"] = db.buscar_ocorrencias()
                        st.session_state["show_edit_form"] = False
                        if "edit_id" in st.session_state: del st.session_state["edit_id"]
                        if "edit_data" in st.session_state: del st.session_state["edit_data"]
                        st.session_state["updated"] = True
                        st.success("❌ Ocorrência excluída!")

    else:
        st.info("Nenhuma ocorrência encontrada.")

    # ---------------- Formulário de edição ----------------
if st.session_state.get("show_edit_form", False):
    st.divider()
    st.subheader("✏️ Editar Ocorrência")
    edit_data = st.session_state["edit_data"]

    with st.form("form_editar_ocorrencia"):
        col1, col2, col3 = st.columns(3)
        with col1:
            sinan = st.text_input("SINAN", value=edit_data[1])
            data_notificacao = st.date_input(
                "Data de Notificação", 
                value=pd.to_datetime(edit_data[2], dayfirst=True) if edit_data[2] else date.today()
            )
            inicio_sintoma = st.date_input(
                "Início dos Sintomas", 
                value=pd.to_datetime(edit_data[3], dayfirst=True) if edit_data[3] else date.today()
            )
            cc = st.date_input(
                "CC", 
                value=pd.to_datetime(edit_data[10], dayfirst=True) if edit_data[10] else date.today()
            )
        with col2:
            data_exame = st.date_input(
                "Data do Exame", 
                value=pd.to_datetime(edit_data[4], dayfirst=True) if edit_data[4] else date.today()
            )
            tipo_exame = st.selectbox(
                "Tipo de Exame", ["", "NS1", "Sorologia", "PCR"], 
                index=["", "NS1", "Sorologia", "PCR"].index(edit_data[5]) if edit_data[5] in ["", "NS1", "Sorologia", "PCR"] else 0
            )
            resultado = st.selectbox(
                "Resultado", ["", "Positivo", "Negativo", "Inconclusivo"], 
                index=["", "Positivo", "Negativo", "Inconclusivo"].index(edit_data[6]) if edit_data[6] in ["", "Positivo", "Negativo", "Inconclusivo"] else 0
            )
            np = st.date_input(
                "NP", 
                value=pd.to_datetime(edit_data[11], dayfirst=True) if edit_data[11] else date.today()
            )
        with col3:
            tipo_doenca = st.selectbox(
                "Tipo Doença", ["", "Dengue", "Zika", "Chikungunya"], 
                index=["", "Dengue", "Zika", "Chikungunya"].index(edit_data[7]) if edit_data[7] in ["", "Dengue", "Zika", "Chikungunya"] else 0
            )
            classificacao = st.selectbox(
                "Classificação", ["", "Autóctone", "Importada"], 
                index=["", "Autóctone", "Importada"].index(edit_data[8]) if edit_data[8] in ["", "Autóctone", "Importada"] else 0
            )
            data_resultado = st.date_input(
                "Data do Resultado", 
                value=pd.to_datetime(edit_data[9], dayfirst=True) if edit_data[9] else date.today()
            )
            sinais_alerta = st.selectbox(
                "Sinais de Alerta", ["", "Leve", "Moderada", "Grave", "Óbito"], 
                index=["", "Leve", "Moderada", "Grave", "Óbito"].index(edit_data[12]) if edit_data[12] in ["", "Leve", "Moderada", "Grave", "Óbito"] else 0
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            nome = st.text_input("Nome", value=edit_data[13])
            data_nascimento = st.date_input(
                "Data Nascimento", 
                value=pd.to_datetime(edit_data[14], dayfirst=True) if edit_data[14] else date.today()
            )
        with col2:
            logradouro = st.text_input("Logradouro", value=edit_data[15])
            numero = st.text_input("Número", value=edit_data[16])
        with col3:
            bairro = st.selectbox(
                "Bairro", BAIRROS, 
                index=BAIRROS.index(edit_data[17]) if edit_data[17] in BAIRROS else 0
            )
            quarterao = st.text_input("Quarteão", value=edit_data[18])

        submitted = st.form_submit_button("Salvar Alterações")
        cancel = st.form_submit_button("Cancelar")

        if submitted:
                db.atualizar_ocorrencia(
                    edit_data[0],
                    sinan, 
                    data_notificacao.strftime("%d/%m/%Y"), 
                    inicio_sintoma.strftime("%d/%m/%Y"), 
                    data_exame.strftime("%d/%m/%Y"),
                    tipo_exame, 
                    resultado, 
                    tipo_doenca, 
                    classificacao, 
                    data_resultado.strftime("%d/%m/%Y"),
                    cc.strftime("%d/%m/%Y"), 
                    np.strftime("%d/%m/%Y"), 
                    sinais_alerta, 
                    nome, 
                    data_nascimento.strftime("%d/%m/%Y"), 
                    logradouro, 
                    numero, 
                    bairro, 
                    quarterao
                )
                st.session_state["ocorrencias"] = db.buscar_ocorrencias()
                st.session_state["show_edit_form"] = False
                del st.session_state["edit_id"]
                del st.session_state["edit_data"]
                st.session_state["updated"] = True
                st.success("✅ Ocorrência atualizada com sucesso!")

        if cancel:
            st.session_state["show_edit_form"] = False
            del st.session_state["edit_id"]
            del st.session_state["edit_data"]


    # -------------------- ABA GRÁFICOS --------------------
with tab_graficos:
    st.title("📊 Análise das Ocorrências")

    ocorrencias = db.buscar_ocorrencias()
    if not ocorrencias:
        st.info("Nenhuma ocorrência cadastrada ainda.")
    else:
        # Cria DataFrame
        colunas = [
            "id","sinan","data_notificacao","inicio_sintoma","data_exame","tipo_exame",
            "resultado","tipo_doenca","classificacao","data_resultado","cc","np",
            "sinais_alerta","nome","data_nascimento","logradouro","numero","bairro","quarterao","data_criacao"
        ]
        df = pd.DataFrame(ocorrencias, columns=colunas)
        df.columns = [c.lower().replace(" ", "_").replace("ç", "c") for c in df.columns]

        # Converte datas
        datas_cols = ["data_criacao", "data_notificacao", "inicio_sintoma", 
                      "data_exame", "data_resultado", "data_nascimento"]
        for col in datas_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)

        # ---------------- Possivel Local para aprendizagem da máquina (PENDENTE) ----------------
        # ---------------- Possivel Local para aprendizagem da máquina (PENDENTE) ----------------
        # ---------------- Possivel Local para aprendizagem da máquina (PENDENTE) ----------------
        # ---------------- Possivel Local para aprendizagem da máquina (PENDENTE) ----------------

        total_casos = len(df)
        bairro_mais_casos = df.groupby("bairro").size().idxmax() if not df.empty else "Nenhum"
        total_bairro_mais_casos = df.groupby("bairro").size().max() if not df.empty else 0

        if not df.empty and "data_notificacao" in df.columns:
            df["mes_notificacao"] = df["data_notificacao"].dt.to_period("M")
            mes_mais_casos = df.groupby("mes_notificacao").size().idxmax()
            total_mes_mais_casos = df.groupby("mes_notificacao").size().max()
            mes_mais_casos_str = mes_mais_casos.strftime("%B/%Y")
        else:
            mes_mais_casos_str = "Nenhum"
            total_mes_mais_casos = 0

        col1, col2, col3 = st.columns(3)
        col1.metric("📌 Total de Ocorrências", total_casos)
        col2.metric(f"🏘️ Bairro com mais casos ({total_bairro_mais_casos})", bairro_mais_casos)
        col3.metric(f"🗓️ Mês com mais casos ({total_mes_mais_casos})", mes_mais_casos_str)

        st.markdown("---")

        # ---------------- Gráficos com expander ----------------

        # 1️⃣ Ocorrências por Bairro
        with st.expander("📍 Ocorrências por Bairro", expanded=False):
            BAIRROS = ["ALTOS DO VALE", "ANITA VENTURI PRICOLI", "APARECIDA", "CONJ. HAB. ARY ESTEVAO", "BRÁS",
                       "CENTRO", "RESIDENCIAL CARLITO QUILICI", "CDHU", "CECAP I", "CECAP II", "CHÁCARA BELA VISTA",
                       "JARDIM CHICO PISCINA", "CLUBE DO VALE", "CONJ HABIT GABRIEL DO O", "CONJ. HAB. GILBERTO ROSSETTI",
                       "COLINA VERDE", "CONDOMINIO MONTE BELO", "DESCANSO", "DISTRITO INDUSTRIAL 2", "FRANCISCO GARÓFALO",
                       "GILDO GERALDO", "IGARAI", "JARDIM ALVORADA", "JD. BIANCHESI", "JD. DAS FIGUEIRAS", "JARDIM LAVINIA",
                       "JD. MIGUEL GOMES", "JARDIM NOVA MOCOCA", "JD. PROGRESSO", "JD. RECREIO", "JD. RIGOBELLO",
                       "JD. SANTA LUZIA", "SANTA TEREZINHA I", "JD. SÃO BENEDITO", "JARDIM SAO FRANCISCO", "JARDIM SAO JOSE",
                       "JD. SÃO LUIZ", "JARDIM BOTANICO", "JOSÉ ANDRÉ DE LIMA", "JARDIM JOSE JUSTI", "MOCOQUINHA",
                       "JARDIM MORRO AZUL", "CONJUNTO HABITACIONAL NELSON NIERO", "NENE PEREIRA LIMA", "PALMERINHA",
                       "PARQUE CANOAS", "JARDIM PLANALTO VERDE", "BAIRRO POR DO SOL", "PRIMAVERA", "PROJETO CEM",
                       "RESIDENCIAL DO BOSQUE", "RIACHUELO", "RURAL", "SAMAMBAIA", "JARDIM SANTA CECILIA",
                       "SANTA CLARA", "SANTA CRUZ", "SANTA EMÍLIA", "JARDIM SANTA MARIA", "VILA SANTA ROSA",
                       "SANTA MARINA", "SÃO BENEDITO DAS AREIAS", "CHACARAS SAO DOMINGOS", "VILA CARVALHO", "VILA LAMBARI",
                       "VILA MARIA", "VILA MARIANA", "VILA NAUFEL", "DISTRITO INDUSTRIAL II", "JARDIM IMPERADOR",
                       "RESIDENCIAL MAIS PARQUE", "VILA QUINTINO"]
            filtro_bairros = st.multiselect("Selecione os bairros", options=["Todos"] + BAIRROS, default=[])
            df_bairro = df.groupby("bairro").size().reindex(BAIRROS, fill_value=0).reset_index()
            df_bairro.columns = ["bairro", "total"]

            if "Todos" in filtro_bairros:
                df_bairro_filtrado = df_bairro.copy()
            elif filtro_bairros:
                df_bairro_filtrado = df_bairro[df_bairro["bairro"].isin(filtro_bairros)]
            else:
                df_bairro_filtrado = df_bairro[df_bairro["total"] > 0]

            df_bairro_filtrado = df_bairro_filtrado.sort_values(by="total", ascending=True)
            df_bairro_filtrado["cor"] = df_bairro_filtrado["total"].apply(lambda x: "lightgrey" if x==0 else x)
            altura = 700 if len(df_bairro_filtrado) <= 20 else len(df_bairro_filtrado) * 25

            fig_bairro = px.bar(df_bairro_filtrado, x="total", y="bairro", orientation="h", color="cor",
                                text="total", color_continuous_scale="Reds", hover_data={"bairro": True, "total": True, "cor": False})
            fig_bairro.update_traces(textposition='outside', textfont_size=12)
            fig_bairro.update_layout(
                xaxis_title="Total de Ocorrências", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False, height=altura,
                margin=dict(l=150, r=50, t=50, b=50), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_bairro, use_container_width=True)

        # 2 Evolução Temporal dos Casos
        with st.expander("📈 Evolução Temporal dos Casos", expanded=False):
            timestamps = pd.to_datetime(df["data_notificacao"].dropna()).sort_values().unique()
            if len(timestamps) == 0:
                st.warning("Nenhuma data válida disponível.")
            else:
                datas_str = [d.strftime("%d/%m/%Y") for d in timestamps]
                slider_datas_str = st.select_slider("Selecione o período", options=datas_str,
                                                    value=(datas_str[0], datas_str[-1]))
                slider_datas = (pd.to_datetime(slider_datas_str[0], dayfirst=True),
                                pd.to_datetime(slider_datas_str[1], dayfirst=True))
                df_periodo = df[(df["data_notificacao"] >= slider_datas[0]) &
                                (df["data_notificacao"] <= slider_datas[1])]
                df_line = df_periodo.groupby("data_notificacao").size().reset_index(name="total")

                if not df_line.empty:
                    df_line["data_str"] = df_line["data_notificacao"].dt.strftime("%d/%m/%Y")
                    fig_evol = px.line(df_line, x="data_str", y="total", markers=True, title="Evolução Temporal",
                                       labels={"data_str": "Data de Notificação", "total": "Ocorrências"})
                    fig_evol.update_traces(line_color="#FF5733", marker=dict(size=8, color="#FF5733"))
                    fig_evol.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                           xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                                           margin=dict(l=50, r=50, t=50, b=50), height=500)
                    st.plotly_chart(fig_evol, use_container_width=True)
                else:
                    st.warning("Nenhum dado disponível para o período selecionado.")

        col1, col2 = st.columns(2)
        with col1:
            # 3 Classificação dos Casos
            with st.expander("📋 Classificação dos Casos", expanded=False):
                fig_class = px.pie(df, names="classificacao", title="Distribuição por Classificação")
                st.plotly_chart(fig_class, use_container_width=True)
        with col2:
            # 4 Resultados dos Exames
            with st.expander("🧪 Resultados dos Exames", expanded=False):
                fig_res = px.bar(df.groupby("resultado").size().reset_index(name="total"),
                                x="resultado", y="total", color="total", text="total")
                st.plotly_chart(fig_res, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
             # 5 Tipos de Sinais de Alerta
            with st.expander("🚨 Tipos de Sinais de Alerta", expanded=False):
                if df["sinais_alerta"].notna().any():
                    df_alerta = df["sinais_alerta"].dropna().str.upper().str.split(",", expand=True).stack().reset_index(level=1, drop=True)
                    df_alerta = df_alerta.str.strip()
                    df_alerta_count = df_alerta.value_counts().reset_index()
                    df_alerta_count.columns = ["sinal_alerta", "total"]
                    fig_alerta = px.bar(df_alerta_count, x="sinal_alerta", y="total", color="total", text="total",
                                        title="Distribuição dos Sinais de Alerta")
                    st.plotly_chart(fig_alerta, use_container_width=True)
                else:
                    st.info("Nenhum sinal de alerta registrado.")
        with col2:
             # 6 Ocorrências por Tipo de Doença
            with st.expander("🦠 Ocorrências por Tipo de Doença", expanded=False):
                fig_tipo = px.pie(df, names="tipo_doenca", title="Distribuição por Tipo de Doença")
                st.plotly_chart(fig_tipo, use_container_width=True)
       
        # 7 Distribuição por Faixa Etária
        with st.expander("👥 Distribuição por Faixa Etária", expanded=False):
            df["idade"] = (pd.Timestamp.today() - df["data_nascimento"]).dt.days // 365
            bins = [0, 10, 20, 40, 60, 80, 100]
            labels = ["0-9", "10-19", "20-39", "40-59", "60-79", "80+"]
            df["faixa_etaria"] = pd.cut(df["idade"], bins=bins, labels=labels, right=False)
            df_idade = df.groupby("faixa_etaria").size().reset_index(name="total")
            fig_idade = px.bar(df_idade, x="faixa_etaria", y="total", color="total", text="total")
            st.plotly_chart(fig_idade, use_container_width=True)

