import pandas as pd

def aplicar_filtros(df, tipos, conjuntos, datas):
    # Filtro de datas
    data_ini, data_fim = datas # A entrada agora é sempre um intervalo

    # Garante que o filtro comece à meia-noite do primeiro dia
    data_ini = pd.to_datetime(data_ini).normalize().tz_localize("America/Sao_Paulo")
    # Garante que o filtro termine no último segundo do dia final
    data_fim = pd.to_datetime(data_fim).normalize().tz_localize("America/Sao_Paulo") + pd.Timedelta(days=1, seconds=-1)

    df_filtrado = df[df["data"].between(data_ini, data_fim)]

    # Filtro de tipos (continua igual)
    if tipos:
        df_filtrado = df_filtrado[df_filtrado["tipo"].isin(tipos)]

    # Filtro de conjuntos (continua igual)
    if conjuntos:
        nomes_do_conjunto = []
        if "Torneios grandes" in conjuntos:
            nomes_do_conjunto += df[df["jogadores"] >= 50]["nome"].tolist()
        if "Torneios recentes" in conjuntos:
            # Corrigido para usar a data de agora com fuso horário correto
            agora = pd.Timestamp.now(tz="America/Sao_Paulo")
            nomes_do_conjunto += df[df["data"] >= agora - pd.Timedelta(days=30)]["nome"].tolist()
        if "Meus favoritos" in conjuntos:
            nomes_do_conjunto += ["Torneio X", "Torneio Y"]
        df_filtrado = df_filtrado[df_filtrado["nome"].isin(nomes_do_conjunto)]

    return df_filtrado


__all__ = ["aplicar_filtros"]