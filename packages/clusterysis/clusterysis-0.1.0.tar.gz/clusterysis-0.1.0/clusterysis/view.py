import pandas as pd
from IPython.display import display, HTML
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

class View():
    def __init__(self, df, cluster_col, quant_cols=None, cat_cols=None):
        self.df = df
        self.quant_cols = quant_cols if quant_cols else _get_quant_cols(df, cluster_col)
        self.cat_cols = cat_cols if cat_cols else _get_cat_cols(df, cluster_col)
        self.df_quant = df[self.quant_cols]
        self.df_cat = df[self.cat_cols]
        self.cluster_col = cluster_col
        self.df_cluster = df[cluster_col]
        self.n_clusters = df[cluster_col].unique().shape[0]

        self.view_table()

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