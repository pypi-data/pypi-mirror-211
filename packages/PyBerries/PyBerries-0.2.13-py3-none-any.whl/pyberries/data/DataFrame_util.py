import numpy as np
import pandas as pd


def get_histogram(df_in, col, binsize, density: bool = False, groupby: str = 'Group'):
    groupby_name = '-'.join(map(str, groupby)) if isinstance(groupby, list) else str(groupby)
    bins = np.arange(df_in[col].min(), df_in[col].max()+2*binsize, binsize)
    df_out = pd.DataFrame(columns=['bins', 'height', groupby_name])
    for grp, data in df_in.groupby(groupby, sort=False):
        groupName = '--'.join(map(str, grp)) if isinstance(grp, tuple) else str(grp)
        df = pd.DataFrame({'bins': bins[:-1]+binsize/2,
                           'height': (pd.cut(data[col], bins, include_lowest=True, right=False)
                                      .value_counts(normalize=density)
                                      .sort_index()
                                      ),
                           groupby_name: groupName})
        df_out = pd.concat([df_out, df], axis=0)
    if isinstance(groupby, list):
        df_out[groupby] = (df_out[groupby_name]
                           .str.split('--', expand=True)
                           )
        df_out = df_out.drop(columns=groupby_name)
    return df_out


def order_categories(df, col: str, order: list):
    df = (df.assign(tmp_col=lambda df:
                    df[col]
                    .astype('category')
                    .cat.reorder_categories(order, ordered=True))
            .drop(columns=col)
            .rename(columns={'tmp_col': col})
            .sort_values(by=col)
          )
    return df
