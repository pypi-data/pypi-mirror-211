from itertools import combinations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
from scanpy._utils import _check_use_raw
from statannotations.Annotator import Annotator

from anutils.scutils.utils import _get_df_or_adata_obs
from anutils.utils import Silent


def init_fig_params():
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='Helvetica')
    plt.rcParams['pdf.fonttype'] = 42
    # sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
    # sc.logging.print_header()
    sc.set_figure_params(dpi=120, facecolor='w', frameon=True, figsize=(4, 4))
    # %config InlineBackend.figure_format='retina'
    # %matplotlib inline


def subplots(ncols, nrows, subfigsize=None, wspace=None, hspace=None, **subplots_kwargs):
    """`plt.subplots` with `figsize` calculated from `ncols`, `nrows`, `subfigsize`, `wspace`, `hspace`
    """
    if subfigsize is None:
        subfigsize = mpl.rcParams['figure.figsize']
    if wspace is None:
        wspace = mpl.rcParams['figure.subplot.wspace']
    if hspace is None:
        hspace = mpl.rcParams['figure.subplot.hspace']
    figsize = (subfigsize[0] * (ncols + wspace * (ncols - 1)),
               subfigsize[1] * (nrows + hspace * (nrows - 1)))
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=figsize, **subplots_kwargs)
    fig.subplots_adjust(wspace=wspace, hspace=hspace)
    return fig, axes


def embeddings(adata,
               basis=None,
               *,
               groupby,
               replicate_key=None,
               groups_order=None,
               add_bg=False,
               ncols=None,
               figsize=None,
               zoom=False,
               return_fig_axes=False,
               wspace=None,
               hspace=None,
               **embedding_kwargs):
    """plot embeddings of adata grouped by group_adata_by

    Parameters
    ----------
    groupby : str or list of str
        column(s) in adata.obs. if a list, they will be concatenated with '::' as the group key
    replicate_key : str, optional
        a column in adata.obs, by default None. If not None, the number of replicates will be shown in the title
    groups_order : iterable, optional
        a ordered list of keys in `adata.obs[groupby]`, by default None
    add_bg : bool, optional
        whether to add umap background (from other groups), by default False
    ncols : int, optional
        ncols, by default 3
    figsize : 2 length tuple, optional
        figsize of each embedding, by default None
    zoom : bool, optional
        whether to zoom each umap plot, by default False, which means the xlim and ylim will be the same for all plots
    return_fig_axes : bool, optional
        whether to return the fig and axes, by default False
    embedding_kwargs : dict
        kwargs for sc.pl.embedding. `adata` is required. if `basis` is not provided, `X_umap` will be used.

    Returns
    -------
    fig
        the fig object
    """
    if basis is None:
        basis = 'X_umap'

    # handle groupby
    if isinstance(groupby, str):
        pass
    else:  # iterable
        groupby = '::'.join(groupby)
        adata.obs[groupby] = adata.obs[list(groupby.split('::'))].apply(lambda x: '::'.join(x),
                                                                        axis=1)
    group_indices_dict = adata.obs.groupby(groupby).indices
    if groups_order is None:
        groups_order = group_indices_dict.keys()
    group_indices_dict = {k: group_indices_dict[k] for k in groups_order}

    # handle color
    if 'color' in embedding_kwargs:
        if isinstance(embedding_kwargs['color'], str):
            embedding_kwargs['color'] = [embedding_kwargs['color']]

    # now plot
    if ncols is None:
        ncols = min(4, len(group_indices_dict))
    N = adata.obs[groupby].nunique()
    nrows = (N - 1) // ncols + 1
    fig, axes = subplots(
        ncols=ncols,
        nrows=nrows,
        subfigsize=figsize,
        wspace=wspace,
        hspace=hspace,
    )

    for i_group, (group, group_idcs) in enumerate(group_indices_dict.items()):
        ad = adata[group_idcs, :]

        # scanpy changes the number of categories when subseting the adata, so we need
        # to reset the categories
        if 'color' in embedding_kwargs:
            for c in embedding_kwargs['color']:
                if c not in ad.obs.columns:
                    # might be a gene name
                    continue
                # if it is categorical
                if adata.obs[c].dtype.name == 'category':
                    # reset the categories to the original categories
                    ad.obs[c].cat.set_categories(adata.obs[c].cat.categories, inplace=True)

        title = group
        if replicate_key is not None:
            title += f' (n={ad.obs[replicate_key].nunique()})'

        kwargs = embedding_kwargs.copy()

        # background umap
        if add_bg:
            _ = sc.pl.embedding(
                adata,
                basis=basis,
                ax=axes.flatten()[i_group],
                show=False,
            )

        # foreground umap
        _ = sc.pl.embedding(
            ad,
            basis=basis,
            **kwargs,
            ax=axes.flatten()[i_group],
            show=False,
            title=title,
        )

    # remove empty axes
    while i_group < ncols * nrows - 1:
        i_group += 1
        axes.flatten()[i_group].axis('off')

    # adjust axes lims to make them equal
    # maybe use `sharex=True, sharey=True` in `plt.subplots`?
    # need to test.
    if not zoom:
        axes_used = axes.flatten()[:N]
        xlims = np.array([ax.get_xlim() for ax in axes_used.flat])
        ylims = np.array([ax.get_ylim() for ax in axes_used.flat])
        xlims = np.array([xlims[:, 0].min(), xlims[:, 1].max()])
        ylims = np.array([ylims[:, 0].min(), ylims[:, 1].max()])
        for ax in axes_used.flat:
            ax.set_xlim(xlims)
            ax.set_ylim(ylims)

    # fig.tight_layout()
    return (fig, axes) if return_fig_axes else None


def _change_bar_width(ax, new_value):
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)


def dotplot(adata,
            groupby,
            var_names,
            inplace=False,
            return_object=False,
            dendogram=True,
            **dotplot_kwargs):
    if not inplace:
        adata = adata.copy()
    if 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = np.e
    adata.obs[groupby] = adata.obs[groupby].astype('category')

    dp = sc.pl.DotPlot(adata,
                       groupby=groupby,
                       var_names=var_names,
                       cmap='Reds',
                       **dotplot_kwargs)
    if dendogram:
        sc.tl.dendrogram(adata, groupby=groupby, var_names=var_names)
        dp.add_dendrogram()
    dp.show()
    return dp if return_object else None


def matrixplot_zscore(adata,
                      groupby,
                      var_names,
                      inplace=False,
                      cmap='RdBu_r',
                      return_object=False,
                      dendogram=True,
                      **matrixplot_kwargs):
    if not inplace:
        adata = adata.copy()
    adata.obs[groupby] = adata.obs[groupby].astype('category')
    mp = sc.pl.MatrixPlot(adata, var_names=var_names, groupby=groupby, **matrixplot_kwargs)
    df = mp.values_df.copy()
    df = df.sub(df.mean(0), 1).div(df.std(0), 1)
    mp.values_df = df
    mp.color_legend_title = 'z-score\nby gene'
    mp = mp.style(cmap=cmap)

    if dendogram:
        sc.tl.dendrogram(adata, groupby=groupby, var_names=var_names)
        mp.add_dendrogram()

    mp.show()
    return mp if return_object else None


def composition_plot(
    data,
    x,
    hue,
    x_subset=None,
    hue_subset=None,
    hue_colors=None,
    bar_width=0.6,
    figsize=None,
    legend_fontsize=None,
    legend_ncols=2,
    label_fontsize=None,
    label_pad=None,
    label_rotation=45,
    return_df=False,
    add_counts=True,
    add_counts_text=True,
    hspace=0.1,
    counts_height_ratio=.25,
    counts_color='#154c79',
):
    """plot the composition of a categorical variable `hue` in different groups of `x`

    Parameters
    ----------
    data : Union[DataFrame, AnnData]
        data to plot
    x : str
        groupby variable
    hue : str
        categorical variable to plot
    x_subset : List[str], optional
        x subset, by default None
    hue_subset : List[str], optional
        hue subset, by default None
    hue_colors : Iterable, optional
        hue colors, by default None
    add_counts : bool, optional
        whether to add an additional barplot of counts on the top, by default True

    Returns
    -------
    matplotlib.axes.Axes
        axes

    Raises
    ------
    ValueError
        data must be a pandas.DataFrame or an anndata.AnnData
    """
    df = _get_df_or_adata_obs(data)

    counts_df: pd.DataFrame = df.groupby(x)[hue].value_counts().unstack()
    if x_subset is None:
        x_subset = counts_df.index
    if hue_subset is None:
        hue_subset = counts_df.columns
    counts_df = counts_df.loc[x_subset, hue_subset]
    counts_df = counts_df.T
    counts = counts_df.sum(axis=0)
    comp_df = counts_df.div(counts_df.sum(axis=0), axis=1).T * 100

    if add_counts:
        # make two axes, both share the same x axis. the top one is for the counts,
        # the bottom one is for the composition. the top one's height is 1/3 of the bottom one.
        fig, (ax1, ax2) = plt.subplots(
            nrows=2,
            ncols=1,
            sharex=True,
            gridspec_kw={'height_ratios': [counts_height_ratio, 1 - counts_height_ratio]},
            figsize=figsize,
        )
        fig.subplots_adjust(hspace=hspace)

        # plot counts
        ax = counts.plot.bar(ax=ax1, color=counts_color, width=bar_width)
        ax.set_ylabel('Cell counts', fontsize=label_fontsize)
        # set fontsize of the counts plot
        ax.tick_params(labelsize=label_fontsize)

        if add_counts_text:
            # Add counts above the two bar graphs
            highest_height = 0
            highest_txt = None
            for rect in ax.patches:
                barx = rect.get_x()
                barw = rect.get_width()
                barh = rect.get_height()
                txt = ax.text(barx + barw / 2.0,
                              barh,
                              f'{barh:.0f}',
                              ha='center',
                              va='bottom',
                              fontsize=label_fontsize)
                if barh > highest_height:
                    highest_height = barh
                    highest_txt = txt
            # adjust the ylim of the counts plot to make sure the counts text is visible
            # by adding font height to the ylim
            txtbb = highest_txt.get_window_extent(
                renderer=fig.canvas.get_renderer()).transformed(ax.transData.inverted())
            ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] + txtbb.height * 1.5)

    else:
        fig, ax2 = plt.subplots(1, 1, figsize=figsize)

    # plot composition
    ax: plt.Axes = comp_df.plot.bar(ax=ax2,
                                    stacked=True,
                                    figsize=figsize,
                                    color=hue_colors,
                                    width=bar_width)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=label_fontsize, rotation=label_rotation)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=label_fontsize)
    ax.set_ylabel('Relative celltype abundacy(%)', fontsize=label_fontsize)
    ax.set_xlabel('', fontsize=label_fontsize, labelpad=label_pad)
    legend_params = {
        'loc': 'center left',
        'bbox_to_anchor': (1.01, 0.5),
        'fontsize': legend_fontsize,
        'ncol': legend_ncols,
        'frameon': False,
        'markerscale': 100,
    }
    ax.legend(**legend_params)

    # remove grid
    for ax in fig.axes:
        ax.grid(False)

    # adjust the figure to make sure all ylabels and xlabels are visible
    #TODO

    return (ax1, ax2) if not return_df else ((ax1, ax2), comp_df)


def get_cmap_colors(cmap, n, alpha=1, pad=1):
    colors = getattr(mpl.cm, cmap)(np.linspace(start=0, stop=1, num=n + 2 * pad), alpha=alpha)
    if pad > 0:
        colors = colors[pad:-pad]
    return colors


def get_grouped_colors(items, group_items, group_cmaps, alpha=1, pad=1):
    """
    Example
    ---
    ```Python
    # define the group items
    cts = adata.obs['ct_mye'].unique().tolist()
    cts = sorted(cts) # same as the order in plots. scanpy sorts the cts, but if not as this order, change this value. 
    
    # group the cell types and assign the colors
    group_cts = {
        'AM': [s for s in cts if s.startswith('AM')],
        'Mac': [s for s in cts if s.startswith('Mac')],
        'Mono': [s for s in cts if s.startswith('Mono')],
        'Others': ['cDC2', 'cDC3', 'pDC', 'Mast', 'Neutrophil'],
        'Doublets': ['Epi doublet', 'T doublet'],
    }
    group_cmaps = {
        'AM': 'Greens',
        'Mac': 'Blues',
        'Mono': 'Oranges',
        'Others': 'Purples',
        'Doublets': 'Greys',
    }
    
    # get the colors
    colors = get_grouped_colors(items=cts, group_items=group_cts, group_cmaps=group_cmaps)
    
    # plot
    sc.pl.umap(adata, color='ct_mye', palette=colors)
    ax = composition_plot(adata.obs, 'donor', 'ct_mye', figsize=(5,5), label_fontsize=10, legend_fontsize=10, hue_colors=colors)
    ```
    """
    group_colors = {}
    item_colors = {}
    groups = list(group_items.keys())
    for g in groups:
        group_colors[g] = get_cmap_colors(cmap=group_cmaps[g],
                                          n=len(group_items[g]),
                                          pad=pad,
                                          alpha=alpha)
        for i, item in enumerate(group_items[g]):
            item_colors[item] = group_colors[g][i]
    item_colors = {k: item_colors[k] for k in items}
    colors = list(item_colors.values())
    return colors


def barplot_with_pvals_by_group(
    data,
    x,
    y,
    groupby,
    add_legend=None,
    figsize=None,
    return_fig_axes=False,
    ncols=None,
    wspace=None,
    hspace=None,
    x_order=None,
    groups_order=None,
    pairs=None,
    verbose=False,
    palette=None,
    add_swarmplot=True,
    showfliers=True,
    simple_format=True,
    test='t-test_ind',
    text_format='star',
):
    """sns.barplot with p-values, grouped by groupby
    
    Recommended to use with figsize = (1.5, 2)
    """
    if hasattr(data, 'obs') and y not in data.obs.columns:
        data = data.obs.join(sc.get.obs_df(data, keys=[y], use_raw=True))

    df = _get_df_or_adata_obs(data)

    # handle x_order
    if x_order is None:
        x_order = sorted(df[x].unique())

    # handle groupby
    if isinstance(groupby, str):
        pass
    else:  # iterable
        groupby = '::'.join(groupby)
        df[groupby] = df[list(groupby.split('::'))].apply(lambda x: '::'.join(x), axis=1)
    group_indices_dict = df.groupby(groupby).indices
    if groups_order is None:
        groups_order = group_indices_dict.keys()
    group_indices_dict = {k: group_indices_dict[k] for k in groups_order}

    # handle add_legend
    if add_legend is None:
        add_legend = simple_format

    # now plot
    if ncols is None:
        ncols = min(4, len(group_indices_dict))
    N = df[groupby].nunique()
    if add_legend:
        N += 1
    nrows = (N - 1) // ncols + 1
    if figsize is None:
        figsize = (1.5, 2)

    fig, axes = subplots(
        ncols=ncols,
        nrows=nrows,
        subfigsize=figsize,
        wspace=wspace,
        hspace=hspace,
    )

    for i_group, (group, group_idcs) in enumerate(group_indices_dict.items()):
        group_df = df.iloc[group_idcs, :]

        barplot_with_pvals(
            data=group_df,
            x=x,
            y=y,
            x_order=x_order,
            pairs=pairs,
            verbose=verbose,
            ax=axes.flatten()[i_group],
            title=group,
            palette=palette,
            add_swarmplot=add_swarmplot,
            showfliers=showfliers,
            simple_format=simple_format,
            test=test,
            text_format=text_format,
        )

    # remove empty axes
    while i_group < ncols * nrows - 1:
        i_group += 1
        axes.flatten()[i_group].axis('off')

    # add legend
    if add_legend:
        patch_names = x_order
        patch_colors = [patch.get_facecolor() for patch in axes.flatten()[0].patches]
        color_dict = dict(zip(patch_names, patch_colors))
        plot_legend(axes.flatten()[-1], color_dict=color_dict)

    # remove grid
    for ax in fig.axes:
        ax.grid(False)

    # fig.tight_layout()

    return (fig, axes) if return_fig_axes else None


def barplot_with_pvals(data,
                       x,
                       y,
                       x_order=None,
                       pairs=None,
                       verbose=True,
                       ax=None,
                       title=None,
                       palette=None,
                       add_swarmplot=True,
                       showfliers=True,
                       simple_format=False,
                       test='t-test_ind',
                       text_format='star'):
    """sns.barplot with p-values
    
    Recommended to use with figsize = (1.5, 2)

    Parameters
    ----------
    data : DataFrame
        df
    x : str
        column name (group by)
    y : str
        column name (bar height)
    order : Iterable, optional
        order of x
    pairs : Iterable of tuples, optional
        pairs to compare and add p-values. If None, all pairs will be compared, by default None
    verbose : bool, optional
        whether to show p-val calculation details, by default True
    ax : Axes, optional
        ax, by default None
    palette : _type_, optional
        _description_, by default None
    add_swarmplot : bool, optional
        whether to add swarmplot, by default True
    showfliers: bool, optional
        whether to show outliers, by default True. When simple_format is True, this will be set to False
    simple_format : bool, optional
        if True, do not show outliers, and remove xlabel and ylabel, instead, use y key as x label, by default True
    test : str, optional
        see `statannotations.Annotator.Annotator`, by default 't-test_ind'
    text_format : str, optional
        see `statannotations.Annotator.Annotator`, by default 'star'

    Returns
    -------
    Axes
        ax
    """
    if hasattr(data, 'obs') and y not in data.obs.columns:
        data = data.obs.join(sc.get.obs_df(data, keys=[y], use_raw=True))

    data = _get_df_or_adata_obs(data)

    if x_order is None:
        x_order = sorted(data[x].unique())
    if pairs is None:
        pairs = list(combinations(x_order, 2))
    if simple_format:
        showfliers = False

    ax = sns.boxplot(
        data=data[data[x].isin(x_order)],
        x=x,
        y=y,
        ax=ax,
        order=x_order,
        linewidth=1,
        width=.4,
        saturation=1,
        showfliers=showfliers,
        palette=palette,
    )
    if add_swarmplot:
        # if too many points, do not add swarmplot
        if data.groupby(x).size().max() > 100:
            print('Too many points, not adding swarmplot.')
            add_swarmplot = False
        else:
            ax = sns.swarmplot(data=data[data[x].isin(x_order)],
                               x=x,
                               y=y,
                               ax=ax,
                               order=x_order,
                               edgecolor='k',
                               palette=palette,
                               alpha=.9,
                               size=3,
                               linewidth=0.5)
    ax.grid(False)
    if simple_format:
        if title is not None:
            ax.set_xlabel(title)
        else:
            ax.set_xlabel(y)
        # ax.set_ylabel('Percentage')
        ax.set_ylabel('')
        # ax.set_xticks([])
        ax.tick_params(bottom=False, labelbottom=False)
    else:
        if title is not None:
            ax.set_title(title)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=8)
    if len(pairs) > 0:
        if verbose:
            annotator = Annotator(ax, pairs, data=data, x=x, y=y, order=x_order)
            annotator.configure(test=test,
                                text_format=text_format,
                                loc='inside',
                                show_test_name=False,
                                line_width=1)
            annotator.apply_and_annotate()
        else:
            with Silent('stdout'):
                annotator = Annotator(ax, pairs, data=data, x=x, y=y, order=x_order)
                annotator.configure(test=test,
                                    text_format=text_format,
                                    loc='inside',
                                    show_test_name=False,
                                    line_width=1)
                annotator.apply_and_annotate()
    return ax


def plot_legend(
    ax,
    color_dict,
    ncol=1,
    title='',
    marker='s',
    loc='lower right',
):
    """plot legend on an ax.

    Parameters
    ----------
    ax : _type_
        _description_
    color_map : dict
        {str: color} dict
    ncol : int, optional
        ncol of legend, by default 1
    title : str, optional
        title, by default ''
    marker : str, optional
        marker type, by default 's'

    Returns
    -------
    Axes
        ax
    """
    from matplotlib.lines import Line2D

    # plt.figure(figsize=figsize)
    legend_TN = [
        Line2D([0], [0], color=color, label=c, marker=marker)
        for c, color in color_dict.items()
    ]
    ax.legend(handles=legend_TN,
              ncol=ncol,
              frameon=False,
              title=title,
              prop={'size': 10},
              loc=loc)
    ax.axis('off')
    return ax


def embedding_region(adata: sc.AnnData,
                     basis=None,
                     *,
                     groupby,
                     color,
                     metric='mean',
                     ax=None,
                     layer=None,
                     use_raw=False,
                     **embedding_kwargs):
    """plot embedding with color representing metrics of groups
    """
    if basis is None:
        basis = 'X_umap'

    assert metric in ['mean', 'median']

    adata._sanitize()
    use_raw = _check_use_raw(adata, use_raw)
    if isinstance(color, str):
        keys = [color]
    else:
        keys = color
    obs_df = sc.get.obs_df(adata, keys=[groupby] + keys, layer=layer, use_raw=use_raw)

    if metric == 'mean':
        group_metric = obs_df.groupby(groupby).mean()
    elif metric == 'median':
        group_metric = obs_df.groupby(groupby).median()
    obs_metric = group_metric.loc[obs_df[groupby].values, keys]

    keys = [f'{metric}_{key}_by_{groupby}' for key in keys]
    obs_metric.columns = keys

    ad = adata.copy()
    ad.obs = obs_metric

    sc.pl.embedding(ad, basis=basis, color=keys, ax=ax, **embedding_kwargs)