save_dir = '/home/alex/tfg_jugglingTrackingSiteswap/results/mot16/'
bounding_box_size = 50


def file_initializer(system: str, ss:str, mode:str=''):
    return open(f'{save_dir}{mode}/{ss}_{system}.txt', 'w+')


def file_writer(file, frame: int, id: int, coords: tuple[int, int]):
    if coords and coords[0] != None and coords[1] != None:
        bb_left = coords[0]-bounding_box_size//2
        bb_top = coords[1]-bounding_box_size//2
        file.write("{},{},{},{},{},{},1,-1,-1,-1\n".format(frame,id,bb_left,bb_top,bounding_box_size,bounding_box_size))

def file_saver(file):
    file.close()
    print("File"+" successfully saved in: "+ save_dir)

def load_data_visualizer(path: str):
    ret = {}
    with open(path) as file:
        for line in file:
            frame, id, bb_left, bb_top,bounding_box_size,bounding_box_size, _, _,_,_ = [int(i) for i in line.split(',')]
            id = id
            if id in ret:
                if len(ret[id]) == frame-1:
                    ret[id].append((bb_left+bounding_box_size//2,bb_top+bounding_box_size//2))
                else:
                    while len(ret[id]) < frame-1:
                        ret[id].append((None,None))
                    ret[id].append((bb_left+bounding_box_size//2,bb_top+bounding_box_size//2))
            else:
                ret[id] = []
                while len(ret[id]) < frame-1:
                    ret[id].append((None,None))
                ret[id].append((bb_left+bounding_box_size//2,bb_top+bounding_box_size//2))

    return ret, len(ret)

def load_data(path: str):
    ret = {}
    with open(path) as file:
        for line in file:
            frame, id, bb_left, bb_top,bounding_box_size,bounding_box_size, _, _,_,_ = [int(i) for i in line.split(',')]
            id = id-1
            if id in ret:
                if len(ret[id]['x']) == frame-1:
                    ret[id]['x'].append(bb_left+bounding_box_size//2)
                    ret[id]['y'].append(bb_top+bounding_box_size//2)
                else:
                    while len(ret[id]['x']) < frame-1:
                        ret[id]['x'].append(None)
                        ret[id]['y'].append(None)
                    ret[id]['x'].append(bb_left+bounding_box_size//2)
                    ret[id]['y'].append(bb_top+bounding_box_size//2)
            else:
                ret[id] = {}
                ret[id]['x'] = []
                ret[id]['y'] = []
                ret[id]['Start'] = 0
                while len(ret[id]['x']) < frame-1:
                    ret[id]['x'].append(None)
                    ret[id]['y'].append(None)
                ret[id]['x'].append(bb_left+bounding_box_size//2)
                ret[id]['y'].append(bb_top+bounding_box_size//2)

    return ret