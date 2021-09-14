from model import MapManager

if __name__ == '__main__':
    mm = MapManager()
    m=mm.init_map()
    # m.show(str_out=True)
    mm.auto_fill_map(m)
    print("")