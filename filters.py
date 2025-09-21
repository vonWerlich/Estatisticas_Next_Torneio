import pandas as pd

def aplicar_filtros(df, tipos, conjuntos, datas):
    # Filtro de datas
    if isinstance(datas, tuple):
        data_ini, data_fim = datas
    else:
        data_ini = data_fim = datas
    data_ini = pd.to_datetime(data_ini).tz_localize("America/Sao_Paulo")
    data_fim = pd.to_datetime(data_fim).tz_localize("America/Sao_Paulo")
    df_filtrado = df[df["data"].between(data_ini, data_fim)]

    # Filtro de tipos
    if tipos:
        df_filtrado = df_filtrado[df_filtrado["tipo"].isin(tipos)]

    # Filtro de conjuntos
    if conjuntos:
        nomes_do_conjunto = []
        if "Torneios grandes" in conjuntos:
            nomes_do_conjunto += df[df["jogadores"] >= 50]["nome"].tolist()
        if "Torneios recentes" in conjuntos:
            nomes_do_conjunto += df[df["data"] >= pd.Timestamp.now(tz="America/Sao_Paulo") - pd.Timedelta(days=30)]["nome"].tolist()
        if "Meus favoritos" in conjuntos:
            nomes_do_conjunto += ["Torneio X", "Torneio Y"]
        df_filtrado = df_filtrado[df_filtrado["nome"].isin(nomes_do_conjunto)]

    return df_filtrado


__all__ = ["aplicar_filtros"]