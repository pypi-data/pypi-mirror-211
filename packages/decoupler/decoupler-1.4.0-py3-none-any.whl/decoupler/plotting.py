import numpy as np
import pandas as pd
from anndata import AnnData

from .pre import extract, rename_net
from .utils_anndata import get_filterbyexpr_inputs, get_min_sample_size, get_cpm_cutoff, get_cpm


def check_if_matplotlib(return_mpl=False):
    if not return_mpl:
        try:
            import matplotlib.pyplot as plt
        except Exception:
            raise ImportError('matplotlib is not installed. Please install it with: pip install matplotlib')
        return plt
    else:
        try:
            import matplotlib as mpl
        except Exception:
            raise ImportError('matplotlib is not installed. Please install it with: pip install matplotlib')
        return mpl


def check_if_seaborn():
    try:
        import seaborn as sns
    except Exception:
        raise ImportError('seaborn is not installed. Please install it with: pip install seaborn')
    return sns


def check_if_adjustText():
    try:
        import adjustText as at
    except Exception:
        raise ImportError('adjustText is not installed. Please install it with: pip install adjustText')
    return at


def save_plot(fig, ax, save):
    if save is not None:
        if ax is not None:
            if fig is not None:
                fig.savefig(save, bbox_inches='tight')
            else:
                raise ValueError("fig is None, cannot save figure.")
        else:
            raise ValueError("ax is None, cannot save figure.")


def filter_limits(df, sign_limit=None, lFCs_limit=None):

    # Define limits if not defined
    if sign_limit is None:
        sign_limit = np.inf
    if lFCs_limit is None:
        lFCs_limit = np.inf

    # Filter by absolute value limits
    msk_sign = df['pvals'] < np.abs(sign_limit)
    msk_lFCs = np.abs(df['logFCs']) < np.abs(lFCs_limit)
    df = df.loc[msk_sign & msk_lFCs]

    return df


def plot_volcano(logFCs, pvals, contrast, name=None, net=None, top=5, source='source', target='target',
                 weight='weight', sign_thr=0.05, lFCs_thr=0.5, sign_limit=None, lFCs_limit=None, figsize=(7, 5),
                 dpi=100, ax=None, return_fig=False, save=None):
    """
    Plot logFC and p-values. If name and net are provided, it does the same for the targets of a selected source.

    Parameters
    ----------
    logFCs : DataFrame
        Data-frame of logFCs (contrasts x features).
    pvals : DataFrame
        Data-frame of p-values (contrasts x features).
    contrast : str
        Name of the contrast (row) to plot.
    name : str, None
        Name of the source to plot. If None, plot classic volcano (without subsetting targets).
    net : DataFrame, None
        Network dataframe. If None, plot classic volcano (without subsetting targets).
    top : int
        Number of top differentially expressed features.
    source : str
        Column name in net with source nodes.
    target : str
        Column name in net with target nodes.
    weight : str, None
        Column name in net with weights. If none, set to None.
    sign_thr : float
        Significance threshold for p-values.
    lFCs_thr : float
        Significance threshold for logFCs.
    sign_limit : float
        Limit of p-values to plot in -log10.
    lFCs_limit : float
        Limit of logFCs to plot in absolute value.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    plt = check_if_matplotlib()
    at = check_if_adjustText()

    # Match dfs
    index = logFCs.index.intersection(pvals.index)
    columns = logFCs.columns.intersection(pvals.columns)
    logFCs = logFCs.loc[index, columns]
    pvals = pvals.loc[index, columns]

    # Transform sign_thr
    sign_thr = -np.log10(sign_thr)

    # Plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    # Check for net
    if net is not None:
        # Rename nets
        net = rename_net(net, source=source, target=target, weight=weight)

        # Get max and if + and -
        max_n = np.std(np.abs(net['weight']), ddof=1)*2
        has_neg = np.any(net['weight'] < 0)

        # Filter by shared targets
        if name is None:
            raise ValueError('If net is given, name cannot be None.')
        df = net[net['source'] == name].set_index('target')
        df['logFCs'] = logFCs.loc[[contrast]].T
        df['pvals'] = -np.log10(pvals.loc[[contrast]].T)
        df = df[~np.any(pd.isnull(df), axis=1)]
        df = filter_limits(df, sign_limit=sign_limit, lFCs_limit=lFCs_limit)

        if has_neg:
            vmin = -max_n
        else:
            vmin = 0
        df.plot.scatter(x='logFCs', y='pvals', c='weight', cmap='coolwarm',
                        vmin=vmin, vmax=max_n, sharex=False, ax=ax)
        ax.set_title('{0} | {1}'.format(contrast, name))
    else:
        df = logFCs.loc[[contrast]].T.rename({contrast: 'logFCs'}, axis=1)
        df['pvals'] = -np.log10(pvals.loc[[contrast]].T)
        df = df[~np.any(pd.isnull(df), axis=1)]
        df = filter_limits(df, sign_limit=sign_limit, lFCs_limit=lFCs_limit)
        df['weight'] = 'gray'
        df.loc[(df['logFCs'] >= lFCs_thr) & (df['pvals'] >= sign_thr), 'weight'] = '#D62728'
        df.loc[(df['logFCs'] <= -lFCs_thr) & (df['pvals'] >= sign_thr), 'weight'] = '#1F77B4'
        df.plot.scatter(x='logFCs', y='pvals', c='weight', sharex=False, ax=ax)
        ax.set_title('{0}'.format(contrast))

    # Draw sign lines
    ax.axhline(y=sign_thr, linestyle='--', color="black")
    ax.axvline(x=lFCs_thr, linestyle='--', color="black")
    ax.axvline(x=-lFCs_thr, linestyle='--', color="black")

    # Plot top sign features
    signs = df[(np.abs(df['logFCs']) >= lFCs_thr) & (df['pvals'] >= sign_thr)].sort_values('pvals', ascending=False)
    signs = signs.iloc[:top]

    # Add labels
    ax.set_ylabel('-log10(pvals)')
    texts = []
    for x, y, s in zip(signs['logFCs'], signs['pvals'], signs.index):
        texts.append(ax.text(x, y, s))
    if len(texts) > 0:
        at.adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black'), ax=ax)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_volcano_df(data, x, y, top=5, sign_thr=0.05, lFCs_thr=0.5, sign_limit=None, lFCs_limit=None,
                    figsize=(7, 5), dpi=100, ax=None, return_fig=False, save=None):
    """
    Plot logFC and p-values from a long formated data-frame.

    Parameters
    ----------
    data : pd.DataFrame
        Results of DEA in long format.
    x : str
        Column name of data storing the logFCs.
    y : str
        Columns name of data storing the p-values.
    top : int
        Number of top differentially expressed features to show.
    sign_thr : float
        Significance threshold for p-values.
    lFCs_thr : float
        Significance threshold for logFCs.
    sign_limit : float
        Limit of p-values to plot in -log10.
    lFCs_limit : float
        Limit of logFCs to plot in absolute value.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    plt = check_if_matplotlib()
    at = check_if_adjustText()

    # Transform sign_thr
    sign_thr = -np.log10(sign_thr)

    # Extract df
    df = data.copy()
    df['logFCs'] = df[x]
    df['pvals'] = -np.log10(df[y])

    # Filter by limits
    df = filter_limits(df, sign_limit=sign_limit, lFCs_limit=lFCs_limit)

    # Define color by up or down regulation and significance
    df['weight'] = 'gray'
    up_msk = (df['logFCs'] >= lFCs_thr) & (df['pvals'] >= sign_thr)
    dw_msk = (df['logFCs'] <= -lFCs_thr) & (df['pvals'] >= sign_thr)
    df.loc[up_msk, 'weight'] = '#D62728'
    df.loc[dw_msk, 'weight'] = '#1F77B4'

    # Plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    df.plot.scatter(x='logFCs', y='pvals', c='weight', sharex=False, ax=ax)

    # Draw sign lines
    ax.axhline(y=sign_thr, linestyle='--', color="black")
    ax.axvline(x=lFCs_thr, linestyle='--', color="black")
    ax.axvline(x=-lFCs_thr, linestyle='--', color="black")

    # Plot top sign features
    signs = df[up_msk | dw_msk].sort_values('pvals', ascending=False)
    signs = signs.iloc[:top]

    # Add labels
    ax.set_ylabel('-log10(pvals)')
    texts = []
    for x, y, s in zip(signs['logFCs'], signs['pvals'], signs.index):
        texts.append(ax.text(x, y, s))
    if len(texts) > 0:
        at.adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black'), ax=ax)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_targets(data, stat, source_name, net, source='source', target='target', weight='weight', top=10, figsize=(5, 5),
                 dpi=100, ax=None, return_fig=False, save=None):
    """
    Plot the weight and statistic of the target genes of a given source.

    Parameters
    ----------
    data : pd.DataFrame
        Results of DEA in long format.
    stat : str
        Column name of data storing feature statistics.
    source_name : str
        Name of source to plot.
    net : DataFrame
        Network dataframe..
    source : str
        Column name in net with source nodes.
    target : str
        Column name in net with target nodes.
    weight : str, None
        Column name in net with weights.
    top : int
        Number of features to show labels.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    plt = check_if_matplotlib()
    at = check_if_adjustText()

    # Extract data
    data = data[stat].copy()
    net = net.copy()

    # Extract weights of given source from net
    w = net[net[source] == source_name].set_index(target)[[weight]]

    # Join
    data = pd.concat([data, w], axis=1, join='inner')

    # Define activation/inhibition color
    pos = ((data[weight] >= 0) & (data[stat] >= 0)) | ((data[weight] < 0) & (data[stat] < 0))
    data['color'] = '#1F77B4'
    data.loc[pos, 'color'] = '#D62728'

    # Plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    data.plot.scatter(x=weight, y=stat, c='color', ax=ax)
    ax.grid()

    # Draw sign lines
    ax.axhline(y=0, linestyle='--', color="black")
    ax.axvline(x=0, linestyle='--', color="black")
    ax.set_title(source_name)

    # Add labels for top features
    top_names = np.abs((data[weight] * data[stat])).sort_values().tail(top).index
    data = data.loc[top_names, :]
    texts = []
    for x, y, s in zip(data[weight], data[stat], data.index):
        texts.append(ax.text(x, y, s))
    if len(texts) > 0:
        at.adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black'), ax=ax)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_violins(mat, thr=None, log=False, use_raw=False, figsize=(7, 5), dpi=100, ax=None, title=None, ylabel=None,
                 color='#1F77B4', return_fig=False, save=None):
    """
    Plot distribution of features' values per sample.

    Parameters
    ----------
    mat : list, DataFrame or AnnData
        List of [features, matrix], dataframe (samples x features) or an AnnData instance.
    thr : float
        Threshold to plot horizontal line.
    log : bool
        Whether to log1p the data or not.
    use_raw : bool
        Use raw attribute of mat if present.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    title : str
        Text to write as title of the plot.
    ylabel : str
        Text to write as ylabel of the plot.
    color : str
        Color to plot the violins.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    sns = check_if_seaborn()
    plt = check_if_matplotlib()

    # Extract data
    m, r, c = extract(mat, use_raw=use_raw)

    # Format
    x = np.repeat(r, m.shape[1])
    y = m.A.flatten()

    # Plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    # log(x+1) transform
    if log:
        y = np.log1p(y)

    sns.violinplot(x=x, y=y, ax=ax, color=color)
    if thr is not None:
        ax.axhline(y=thr, linestyle='--', color="black")
    ax.tick_params(axis='x', rotation=90)

    # Label
    if title is not None:
        ax.set_title(title)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def set_limits(vmin, vcenter, vmax, values):

    if vmin is None:
        vmin = values.min()

    if vmax is None:
        vmax = values.max()

    if vcenter is None:
        vcenter = values.mean()

    if vmin >= vcenter:
        vmin = -vmax

    if vcenter >= vmax:
        vmax = -vmin

    return vmin, vcenter, vmax


def plot_barplot(acts, contrast, top=25, vertical=False, cmap='coolwarm', vmin=None, vcenter=0, vmax=None,
                 figsize=(7, 5), dpi=100, return_fig=False, save=None):
    """
    Plot barplots showing the top absolute value activities.

    Parameters
    ----------
    acts : DataFrame
        Activities obtained from any method.
    contrast : str
        Name of the contrast (row) to plot.
    top : int
        Number of top features to plot.
    vertical : bool
        Whether to plot verticaly or horizontaly.
    cmap : str
        Colormap to use.
    vmin : float, None
        The value representing the lower limit of the color scale.
    vcenter : float, None
        The value representing the center of the color scale.
    vmax : float, None
        The value representing the upper limit of the color scale.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    sns = check_if_seaborn()
    plt = check_if_matplotlib()
    mpl = check_if_matplotlib(return_mpl=True)

    # Check for non finite values
    if np.any(~np.isfinite(acts)):
        raise ValueError('Input acts contains non finite values.')

    # Process df
    df = acts.loc[[contrast]]
    df.index.name = None
    df.columns.name = None
    df = (df

          # Sort by absolute value and transpose
          .iloc[:, np.argsort(abs(df.values))[0]].T

          # Select top features and add index col
          .tail(top).reset_index()

          # Rename col
          .rename({contrast: 'acts'}, axis=1)

          # Sort by activities
          .sort_values('acts'))

    if vertical:
        x, y = 'acts', 'index'
    else:
        x, y = 'index', 'acts'

    # Plot
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    sns.barplot(data=df, x=x, y=y, ax=ax)

    if vertical:
        sizes = np.array([bar.get_width() for bar in ax.containers[0]])
        ax.set_xlabel('Activity')
        ax.set_ylabel('')
    else:
        sizes = np.array([bar.get_height() for bar in ax.containers[0]])
        ax.tick_params(axis='x', rotation=90)
        ax.set_ylabel('Activity')
        ax.set_xlabel('')

    # Compute color limits
    vmin, vcenter, vmax = set_limits(vmin, vcenter, vmax, df['acts'])

    # Rescale cmap
    divnorm = mpl.colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    cmap_f = plt.get_cmap(cmap)
    div_colors = cmap_f(divnorm(sizes))
    for bar, color in zip(ax.containers[0], div_colors):
        bar.set_facecolor(color)

    # Add legend
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=divnorm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def build_msks(df, groupby):

    # Process groupby
    if type(groupby) is str:
        groupby = [groupby]

    # Build msks
    if groupby is None:
        msks = [np.full(df.shape[0], True)]
        cats = [None]
    else:
        msks = []
        sub = df[groupby].values
        cats = np.unique(sub)
        for cat in cats:
            msk = sub == cat
            msks.append(msk)
    return msks, cats


def write_labels(ax, title, xlabel, ylabel, x, y):

    if title is not None:
        ax.set_title(title)
    if xlabel is None:
        xlabel = x.upper()
    ax.set_xlabel(xlabel)
    if ylabel is None:
        ylabel = y.upper()
    ax.set_ylabel(ylabel)


def plot_metrics_scatter(df, x='auroc', y='auprc', groupby=None, show_text=True, show_legend=True, mirror_xy=True,
                         figsize=(5, 5), dpi=100, ax=None, title=None, xlabel=None, ylabel=None, color='black',
                         return_fig=False, save=None):
    """
    Plot scatter plot of metrics across two different axes.

    Parameters
    ----------
    df : DataFrame
        Performance metrics per method, obtained by running run_benchmark.
    x : str
        Name of the metric to plot in the x axis.
    y : str
        Name of the metric to plot in the y axis.
    groupby : str
        Metrics can be gruped by an extra categorical column.
    show_text : bool
        Whether to plot text labels.
    show_legend : bool
        Whether to plot the legend.
    mirror_xy : bool
        Whether to make x and y axis have the same values.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    title : str
        Text to write as title of the plot.
    xlabel : str
        Text to write as xlabel of the plot.
    ylabel : str
        Text to write as ylabel of the plot.
    color : str
        Color to plot the dots.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    plt = check_if_matplotlib()
    at = check_if_adjustText()

    # Build msks and cats
    msks, cats = build_msks(df, groupby)

    # Plot for each group in groupby
    fig = None
    texts = []
    for cat, msk in zip(cats, msks):

        # Reformat df
        sub = (
            df[msk]
            .groupby(['method', 'metric'])
            .mean(numeric_only=True).reset_index()
            .pivot(index='method', columns='metric', values='score').reset_index()
        )

        # Extract values
        x_vals = sub[x].values
        y_vals = sub[y].values
        s_vals = sub['method'].values

        # Plot
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        ax.set_axisbelow(True)
        ax.grid(zorder=0)
        ax.scatter(x_vals, y_vals, zorder=1, label=cat)
        if show_text:
            text = [ax.text(x_vals[i], y_vals[i], s_vals[i], zorder=2) for i in range(len(x_vals))]
            texts.extend(text)

    # Add legend
    if groupby is not None and show_legend:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

    # Adjust limits
    if mirror_xy:
        max_n = np.max([np.max(ax.get_xticks()), np.max(ax.get_yticks())])
        min_n = np.min([np.min(ax.get_xticks()), np.min(ax.get_yticks())])
        ax.set_xlim(min_n, max_n)
        ax.set_ylim(min_n, max_n)
    if show_text:
        at.adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'), ax=ax)

    # Write labels
    write_labels(ax, title, xlabel, ylabel, x, y)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_metrics_scatter_cols(df, col, x='auroc', y='auprc', groupby=None, n_cols=4, figsize=(10, 12), dpi=100,
                              return_fig=False, save=None):
    """
    Extension of the function plot_metrics_scatter to group metrics by two categories at the same time.

    Parameters
    ----------
    df : DataFrame
        Performance metrics per method, obtained by running run_benchmark.
    col : str
        Name of the group column to group by. Each of its categories will become a subplot.
    x : str
        Name of the metric to plot in the x axis.
    y : str
        Name of the metric to plot in the y axis.
    groupby : str
        Name of the group column to additionaly group by. Each of its categories will appear in the legend.
    n_cols : int
        Number of columns per row.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    plt = check_if_matplotlib()

    # Get unique cats
    cats = np.unique(df[col].values)
    n_rows = int(np.ceil(cats.size / n_cols))

    # Fill missing combinations
    groupbys = np.unique(df[groupby].values)
    metrics = np.unique(df['metric'].values)

    for cat in cats:
        for grpby in groupbys:
            is_empty = df[(df[col] == cat) & (df[groupby] == grpby)].shape[0] == 0
            if is_empty:
                for m in metrics:
                    if col == 'method' or groupby == 'method':
                        tmp = pd.DataFrame([[cat, grpby, m, np.nan, np.nan]], columns=[col, groupby, 'metric', 'score', 'ci'])
                    else:
                        tmp = pd.DataFrame([[cat, grpby, '', m, np.nan, np.nan]],
                                           columns=[col, groupby, 'method', 'metric', 'score', 'ci'])
                    df = pd.concat([df, tmp])

    # Start figure
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize, dpi=dpi, tight_layout=True, sharex=True, sharey=True)
    axes = axes.ravel()

    # Draw a subplot per cat
    for i in range(axes.size):
        ax = axes[i]
        if i < len(cats):
            cat = cats[i]
            plot_metrics_scatter(df[df[col] == cat], x=x, y=y, groupby=groupby, show_text=False, show_legend=False,
                                 mirror_xy=False, ax=ax, title=cat, xlabel='', ylabel='')
        else:
            ax.axis('off')

    # Format legend
    handles, labels = axes[len(cats) - 1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_metrics_boxplot(df, metric, groupby=None, figsize=(5, 5), dpi=100, ax=None, title=None,
                         xlabel=None, ylabel=None, return_fig=False, save=None, **kwargs):
    """
    Plot boxplots showing the distribution of scores between methods for a metric.

    Parameters
    ----------
    df : DataFrame
        Performance metrics per method, obtained by running run_benchmark.
    metric : str
        Name of metric to plot, must be either "mcauroc" or "mcauprc".
    groupby : str
        Metrics can be gruped by an extra categorical column.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    title : str
        Text to write as title of the plot.
    xlabel : str
        Text to write as xlabel of the plot.
    ylabel : str
        Text to write as ylabel of the plot.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.
    kwargs : dict
        Other keyword arguments are passed through to seaborn.boxplot().

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """

    # Load plotting packages
    sns = check_if_seaborn()
    plt = check_if_matplotlib()

    if metric not in ['mcauroc', 'mcauprc']:
        raise ValueError('Argument metric must be either "mcauroc" or "mcauprc".')

    # Subset metric
    df = df[df['metric'] == metric]

    # Plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    ax.set_axisbelow(True)
    ax.grid(zorder=0)

    if type(groupby) is str and groupby != 'method':

        # Compute order
        order = (
            df
            .groupby(['method', groupby])
            .mean(numeric_only=True)
            .reset_index()
            .groupby('method')
            .max()
            .sort_values('score')
            .index
        )

        sns.boxplot(x='method', y='score', hue=groupby, data=df, ax=ax, order=order, **kwargs)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

    elif groupby is None:

        # Compute order
        order = (
            df
            .groupby(['method'])
            .mean(numeric_only=True)
            .sort_values('score')
            .index
        )

        sns.boxplot(x='method', y='score', data=df, ax=ax, order=order, **kwargs)

    else:
        raise ValueError('Argument groupby must be a string and not be "method".')

    # Rotate xticks
    ax.tick_params(axis='x', rotation=90)

    # Write labels
    if title is not None:
        ax.set_title(title)
    if xlabel is None:
        xlabel = 'Methods'
    ax.set_xlabel(xlabel)
    if ylabel is None:
        ylabel = metric.upper()
    ax.set_ylabel(ylabel)

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_psbulk_samples(adata, groupby, figsize=(5, 5), dpi=100, ax=None, return_fig=False, save=None, **kwargs):
    """
    Quality Control plot to assess the quality of the obtained pseudobulk samples.

    Parameters
    ----------
    adata : AnnData
        AnnData obtained after running ``decoupler.get_pseudobulk``.
    groupby : str, list
        Name of the ``.obs`` column to group by. Can also be a list of columns.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.
    kwargs : dict
        Other keyword arguments are passed through to seaborn.scatterplot().

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """
    # Load plotting packages
    sns = check_if_seaborn()
    plt = check_if_matplotlib()

    # Extract obs
    df = adata.obs.copy()

    # Transform to log10
    df['psbulk_n_cells'] = np.log10(df['psbulk_n_cells'])
    df['psbulk_counts'] = np.log10(df['psbulk_counts'])

    if type(groupby) is list and ax is not None:
        raise ValueError("""If a grupby is a list of columns ax must be None.""")
    elif type(groupby) is list:
        fig, axes = plt.subplots(1, len(groupby), figsize=figsize, dpi=dpi, tight_layout=True)
        axes = axes.ravel()
        for ax, grp in zip(axes, groupby):
            ax.grid(zorder=0)
            sns.scatterplot(x='psbulk_n_cells', y='psbulk_counts', hue=grp, ax=ax, data=df, zorder=1, **kwargs)
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, title=grp)
            ax.set_xlabel('Log10 number of cells')
            ax.set_ylabel('Log10 total sum of counts')
    else:
        # Plot
        fig = None
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        ax.grid(zorder=0)
        sns.scatterplot(x='psbulk_n_cells', y='psbulk_counts', hue=groupby, ax=ax, data=df, zorder=1, **kwargs)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, title=groupby)
        ax.set_xlabel('Log10 number of cells')
        ax.set_ylabel('Log10 total sum of counts')

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_filter_by_expr(adata, obs=None, group=None, lib_size=None, min_count=10, min_total_count=15, large_n=10,
                        min_prop=0.7, cmap='viridis', figsize=(5, 4), dpi=100, ax=None, return_fig=False, save=None, **kwargs):
    """
    Plot to help determining the thresholds of the ``decoupler.filter_by_expr`` function.

    Parameters
    ----------
    adata : AnnData
        AnnData obtained after running ``decoupler.get_pseudobulk``.
    obs : DataFrame, None
        If provided, metadata dataframe, only needed if ``adata`` is not an ``AnnData``.
    group : str, None
        Name of the ``.obs`` column to group by. If None, it assumes that all samples belong to one group.
    lib_size : int, float, None
        Library size. If None, default to the sum of reads per sample.
    min_count : int
        Minimum count requiered per gene for at least some samples.
    min_total_count : int
        Minimum total count required per gene across all samples.
    large_n : int
        Number of samples per group that is considered to be "large".
    min_prop : float
        Minimum proportion of samples in the smallest group that express the gene.
    cmap : str
        Colormap to use.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.
    kwargs : dict
        Other keyword arguments are passed through to ``sns.histplot``.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """
    # Load plotting packages
    sns = check_if_seaborn()
    plt = check_if_matplotlib()

    # Extract inputs
    y, obs, var_names = get_filterbyexpr_inputs(adata, obs)

    # Compute lib_size if needed
    if lib_size is None:
        lib_size = np.sum(y, axis=1)

    # Minimum sample size cutoff
    min_sample_size = get_min_sample_size(group, obs, large_n, min_prop)
    min_sample_size -= 1e-14

    # Total count cutoff
    min_total_count -= 1e-14

    # CPM cutoff
    cpm_cutoff = get_cpm_cutoff(lib_size, min_count)

    # CPM thr
    cpm = get_cpm(y, lib_size)
    sample_size = np.sum(cpm >= cpm_cutoff, axis=0)

    # Total counts
    total_counts = np.sum(y, axis=0)
    total_counts[total_counts < 1.] = np.nan  # Handle 0s

    # Plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    sns.histplot(x=np.log10(total_counts), y=sample_size, cmap=cmap, cbar=True,
                 cbar_kws=dict(shrink=.75, label='Number of features'),
                 discrete=(False, True), ax=ax, **kwargs)
    ax.axhline(y=min_sample_size - 0.5, c='gray', ls='--')
    ax.axvline(x=np.log10(min_total_count), c='gray', ls='--')
    ax.set_xlabel('Log10 total sum of counts')
    ax.set_ylabel('Number of samples')

    save_plot(fig, ax, save)

    if return_fig:
        return fig


def plot_filter_by_prop(adata, min_prop=0.2, min_smpls=2, cmap='viridis', figsize=(5, 4),
                        dpi=100, ax=None, return_fig=False, save=None, **kwargs):
    """
    Plot to help determining the thresholds of the ``decoupler.filter_by_expr`` function.

    Parameters
    ----------
    adata : AnnData
        AnnData obtained after running ``decoupler.get_pseudobulk``. It requieres ``.layer['psbulk_props']``.
    min_prop : float
        Minimum proportion of cells that express a gene in a sample.
    min_smpls : int
        Minimum number of samples with bigger or equal proportion of cells with expression than ``min_prop``.
    cmap : str
        Colormap to use.
    figsize : tuple
        Figure size.
    dpi : int
        DPI resolution of figure.
    ax : Axes, None
        A matplotlib axes object. If None returns new figure.
    return_fig : bool
        Whether to return a Figure object or not.
    save : str, None
        Path to where to save the plot. Infer the filetype if ending on {`.pdf`, `.png`, `.svg`}.
    kwargs : dict
        Other keyword arguments are passed through to ``matplotlib.pyplot.hist``.

    Returns
    -------
    fig : Figure, None
        If return_fig, returns Figure object.
    """
    # Load plotting packages
    plt = check_if_matplotlib()
    msg = """adata must be an AnnData object that contains the layer 'psbulk_props'. Please check the
            function decoupler.get_pseudobulk."""

    if isinstance(adata, AnnData):
        layer_keys = adata.layers.keys()
        if 'psbulk_props' in list(layer_keys):
            props = adata.layers['psbulk_props']
            if isinstance(props, pd.DataFrame):
                props = props.values
        else:
            raise ValueError(msg)

        # Compute nsamples by minprop
        nsmpls = np.sum(props >= min_prop, axis=0)

        # Plot
        fig = None
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        _ = ax.hist(nsmpls, log=True, color='gray', **kwargs)
        ax.axvline(x=min_smpls, c='black', ls='--')
        ax.set_xlabel('Number of samples where >= min_prop')
        ax.set_ylabel('Number of genes')

        save_plot(fig, ax, save)

        if return_fig:
            return fig
    else:
        raise ValueError(msg)
