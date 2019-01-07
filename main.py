import ghome
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import config as conf
from math import ceil

mygraphs = []


def main():
    # set up subplots
    style.use('fivethirtyeight')

    fig = plt.figure()

    num_subplots = len(conf.ip_list)
    num_cols = ceil(num_subplots ** 0.5)
    num_rows = (num_subplots // num_cols) + num_subplots % num_cols

    for i, ip in enumerate(conf.ip_list):
        ax = fig.add_subplot(num_rows, num_cols, i + 1)
        mygraphs.append(MyGraph(ax, ip))

    ani = animation.FuncAnimation(fig, animate, interval=500)

    plt.show()


def animate(i):
    for mgraph in mygraphs:
        mgraph.animate()

    # todo only accounts for the last graph's lines. Will need to fix this.
    plt.legend()


class MyGraph:
    def __init__(self, ax, ip):
        self.ax = ax
        self.ip = ip
        self.graph_data = []
        self.seen_macs = []

        self.friendly_name = ghome.get_device_info(ip)

    def animate(self):
        results = ghome.get_results(self.ip)
        print("results (" + self.ip + ")    ", results)

        for mac in results:
            if mac not in self.seen_macs:
                if len(conf.mac_whitelist) == 0 or mac in conf.mac_whitelist:
                    self.seen_macs.append(mac)

        self.graph_data.append(results)

        self.ax.clear()

        for mac in self.seen_macs:
            xs = [i for i in range(len(self.graph_data))]
            # ys = [point for point in self.graph_data]
            ys = [-1 * result[mac] if mac in result else None for result in self.graph_data]

            # trim to show only most recent items
            xs = xs[-conf.max_datapoints:]
            ys = ys[-conf.max_datapoints:]

            self.ax.plot(xs, ys, label=mac)

        self.ax.set_ylim(0, 100)
        self.ax.set_title(self.friendly_name + " (" + self.ip + ")")


main()
