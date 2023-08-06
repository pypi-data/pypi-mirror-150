import math

import pandas as pd
from IPython.display import display, HTML
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

class View():
    def __init__(self, df, cluster_col, quant_cols=None, cat_cols=None, diff_cluster=None):
        self.df = df
        self.quant_cols = quant_cols if quant_cols else _get_quant_cols(df, cluster_col)
        self.cat_cols = cat_cols if cat_cols else _get_cat_cols(df, cluster_col)
        self.df_quant = df[self.quant_cols]
        self.df_cat = df[self.cat_cols]
        self.cluster_col = cluster_col
        self.df_cluster = df[cluster_col]
        self.n_clusters = df[cluster_col].unique().shape[0]
        self.diff_cluster = diff_cluster

        self.view_table()
        self.view_pies()
        self.view_box()

    def view_box(self):
        rows=2
        cols=int(math.ceil(len(self.quant_cols)/2))
        fig = make_subplots(rows=rows, cols=cols)

        i=0
        for var in self.quant_cols:
            row = int(i//cols+1)
            col = int(i%cols+1)
            for cluster in self.df[self.cluster_col].unique():
                marker_color = 'rgb(96, 163, 144)' if cluster==self.diff_cluster else 'rgb(48, 70, 128)'
                fig.add_trace(go.Box(y=self.df[self.df["cluster"]==cluster][var], boxmean=True, marker_color=marker_color, boxpoints=False, name=f"{cluster}: {var}"),row=row, col=col)
            i+=1
        fig.update_layout(height=1000, title_text="Side By Side Subplots")
        fig.show()

    def view_pies(self):
        df_pie = self.df.copy()

        for var in self.cat_cols:
            if df_pie[var].apply(len).mean() < 15:
                textinfo = 'percent+label'
                textposition = None
            else:
                df_pie[var] = df_pie[var].apply(lambda x: f"{x[:25]}...")
                textinfo = 'percent'
                textposition = 'inside'

            rows=2
            cols=int(math.ceil(self.n_clusters/2))

            fig = make_subplots(rows=rows, cols=cols, specs=[[{'type':'domain'} for i in range(cols)], [{'type':'domain'} for i in range(cols)]])

            i = 0
            for name, group_df in df_pie.groupby(self.cluster_col):
                row = int(i//cols+1)
                col = int(i%cols+1)
                width = 2 if name==self.diff_cluster else None
                fig.add_trace(go.Pie(labels=group_df[var], values=group_df[self.quant_cols[0]], name=name, title=f"Cluster {name}", hole=.4, marker={'line': {'width': width}}), row, col)
                i+=1
            fig.update_traces(hoverinfo="label+percent+name", textinfo=textinfo, textposition=textposition)
            fig.update_layout(
                title_text=f"{var} percentage in each cluster.",
                height=1000)
            fig.show()

    def view_table(self):
        grouped_df = self._group_by_cluster()
        display_df(grouped_df)

    def _group_by_cluster(self):
        count_col = self.cat_cols[0] if self.cat_cols[0] != self.cluster_col else self.cat_cols[1]
        agg_quant = {i: "mean" for i in self.quant_cols}
        agg_quant[count_col] = "count"

        return (
            self.df
            .groupby([self.cluster_col])
            .agg(agg_quant)
            .rename(columns={count_col: "count"})
        )

def display_df(df):
    display(HTML(df.style.background_gradient("Blues").to_html()))

def _get_quant_cols(df, cluster_col):
    return df.select_dtypes(include='number').columns.drop(cluster_col, errors="ignore").to_list()

def _get_cat_cols(df, cluster_col):
    return df.select_dtypes(include='object').columns.drop(cluster_col, errors="ignore").to_list()