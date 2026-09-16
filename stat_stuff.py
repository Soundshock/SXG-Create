import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib import ticker
from typing import Literal
from collections import defaultdict

# utilities for teststatistics.py


# dataset   tuple   (label, data{})
Formats = Literal['sample format', 'prg', 'program', 'unique waveforms', 'keysplits', 'unique sample count', 'avg samples per wave']
DataFormat = defaultdict[Formats, list]


def create_char_plot(datasets : dict[str, DataFormat], chart_name: str, xAxis : Formats, yAxis : Formats, Ylim : float = -1, mask : list[str] = [], ext: str = 'png'):

    VERSION = 2

    # plt.figure(figsize=(16, 9))
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.style.use('dark_background')
    plt.gca().set_facecolor("black")
    plt.gcf().set_facecolor("black")

    suffix : str = ''
    if len(mask) : 
       for muname in mask : 
           suffix = suffix + muname     
    
    for idx, mu in enumerate(datasets.keys()) :

        dataformat = datasets[mu]

        Xdata = dataformat[xAxis]
        Ydata = dataformat[yAxis]

        if idx == 0 : 
            max_x = len(dataformat[xAxis])
            ax.set_xlim(left=-0.4, right=max_x )
            # ax.xaxis.set_minor_locator(ticker.MultipleLocator(8)) # minor ticks eh
            ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            # ax.xaxis.set_ticklabels([])
            # ax.xaxis.title
            if Ylim > 0 : 
                ax.set_ylim(bottom=0, top=(Ylim*1.05))

        # ax.set_xlabel('', fontsize=8)
        plt.xticks(fontsize=6, family='monospace', rotation=85)

        if len(mask) : 
            if mu not in mask : 
                continue

        # todo make the 1 and 2 bigger if we can
        markerstyles = {
            "mu80": '1',
            "mu50": 'x',
            "syxg50": '+',
            "mu90": '2',
        }
        mark = markerstyles.get(mu, 'X' )

        colormaps = {
            "mu80": (plt.colormaps.get_cmap("Blues"), 0.7),
            "mu50": (plt.colormaps.get_cmap("Reds"), 0.7),
            "syxg50": (plt.colormaps.get_cmap("YlOrRd"), 0.3),
            "mu90": (plt.colormaps.get_cmap("RdPu"), 0.5),
        }
        cmap, intensity = colormaps.get(mu, (plt.colormaps.get_cmap('viridis'),0.5) )
        # color_value = (idx + 1) / (len(datasets) + 1)
        # line_color = cmap(color_value)
        line_color = cmap(intensity)

        # plt.axes
        plt.scatter(
            Xdata, Ydata, marker=mark, linestyle='-.', color=line_color, label=mu
        )

        # grid and axes format

    plt.grid(True, color='grey', linestyle='--', linewidth=0.5, alpha=0.5)

    for spine in plt.gca().spines.values():
        spine.set_color('grey')

    # # Labels
    plt.xlabel(f'{xAxis}', color='gainsboro', family='monospace')
    plt.ylabel(f'{yAxis}', color='gainsboro', family='monospace')



    plt.title(
        f'{chart_name}',
        color='white',
        family='monospace',
        pad=12,
    )

    plt.tick_params(axis='both', colors='grey')
    plt.legend()
    plt.tight_layout()

    # Save the plot to file.
    output_filename = f'{chart_name}{suffix}_plt{VERSION}.{ext}'
    # plt.savefig(output_filename, format=fmt)
    print(f'saving figure to {output_filename}')
    plt.savefig(output_filename, format=ext, dpi=200)
    plt.close()




def print_data(datasets : dict[str, DataFormat], name : str, xAxis : Formats, yAxis : Formats, _ : list = []) :

    for mu in datasets.keys() : 
        dataformat = datasets[mu]
        Xdata = dataformat[xAxis]
        Ydata = dataformat[yAxis]
        data_cnt = min(len(Xdata),len(Ydata))
        print(f'\n{mu}: {name} (cnt={data_cnt}) - {xAxis} / {yAxis}    min={min(Xdata)}/{min(Ydata)}  max={max(Xdata)}/{max(Ydata)} /vvvv')
        s : str = ''
        for i in range(0,data_cnt) : 
            # y : str = '{:.2f}'.format(Ydata[i]) if Ydata[i] == float else str(Ydata[i])
            y : str = '{:.2f}'.format(Ydata[i])
            s = s + f'({Xdata[i]},{y}),'
        print(s[:-1])
