from pysykkel import Pysykkel
from blessings import Terminal
import os

class PysykkelPrinter():
    def _fmt_header(self, col_width, num_cols):
        line_1_gfx = " ledige plasser ┓ "
        line_1_fmt = self.term.white("{0:>" + str(col_width) + "s}")
        line_1 = line_1_fmt.format(line_1_gfx)
        retval = line_1 * num_cols + os.linesep

        line_2_gfx = " ledige sykler ┓  ┃ "
        line_2_fmt = self.term.white("{0:>" + str(col_width) + "s}")
        line_2 = line_2_fmt.format(line_2_gfx)
        retval += line_2 * num_cols + os.linesep

        line_3_fmt = self.term.white("{0:>" + str(col_width) + "s}")
        line_3_gfx = "stativnavn ┓  ┃  ┃ "
        line_3 = line_3_fmt.format(line_3_gfx)
        retval += line_3 * num_cols

        return retval

    def __init__(self):
        self.pysykkel = Pysykkel()
        stations = self.pysykkel.stations
        self.term = Terminal()
        # 
        stations = sorted(stations, key=lambda k: k['title']) 
        longest_station_name = len(max([s['title'] for s in stations], key=len))
        col_width = longest_station_name + 7
        num_cols = int(self.term.width / col_width)

        line_width = num_cols * col_width

        if self.pysykkel.all_stations_closed:
            msg = 'OBS: Bysykkelsystemet er på nåværende tidspunkt ute av drift!'
            fmt_string = self.term.bright_red('{0:^' + str(line_width) + 's}')
            print(fmt_string.format(msg))

        print(self._fmt_header(col_width, num_cols))

        cur_col = 0

        for station in stations:
            print(self._fmt_entry(station, col_width), end='')
            cur_col += 1
            if cur_col == num_cols:
                print('')
                cur_col = 0
        print('')

    # I would be using F"" for formatting but I didn't think it
    # appropriate to require python3.6 just yet
    def _fmt_entry(self, station, width):
        fmt_string = self.term.bright_cyan("{0:>" + str(width - 7) + "s}")

        if station['availability']['bikes'] == 0:
            fmt_string += self.term.bright_red(" {1:2}")
        elif station['availability']['bikes'] < 3:
            fmt_string += self.term.bright_yellow(" {1:2}")
        else:
            fmt_string += self.term.bright_green(" {1:2}")

        if station['availability']['locks'] == 0:
            fmt_string += self.term.bright_red(" {2:2} ")
        elif station['availability']['locks'] < 3:
            fmt_string += self.term.bright_yellow(" {2:2} ")
        else:
            fmt_string += self.term.bright_green(" {2:2} ")

        return fmt_string.format(station['title'], \
                station['availability']['bikes'], \
                station['availability']['locks'])

if __name__ == '__main__':
    PysykkelPrinter()
