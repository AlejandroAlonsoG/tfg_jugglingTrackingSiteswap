save_dir = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'
bounding_box_size = 50


def file_initializer(system: str, ss:str):
    return open(f'{save_dir}{ss}_{system}.txt', 'w+')


def file_writer(file, frame: int, id: int, coords: tuple[int, int]):
    if coords:
        bb_left = coords[0]-bounding_box_size//2
        bb_top = coords[1]-bounding_box_size//2
        file.write("{},{},{},{},{},{},1,-1,-1,-1\n".format(frame,id,bb_left,bb_top,bounding_box_size,bounding_box_size))

def file_saver(file):
    file.close()
    print("File"+" successfully saved in: "+ save_dir)

