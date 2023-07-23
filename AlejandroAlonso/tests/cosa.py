import cv2

def bg_substraction_tracking_max_balls(source_path, min_contour_area=1000, enclosing_area_diff=0.5, arc_const=0.1, max_balls=3, save_data=-1, visualize=False, output_path=None):
    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=10)

    ret, img = cap.read()
    if visualize:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    if save_data != -1:
        ret, img = cap.read()
        mask = object_detector.apply(img)
        width = mask.shape[0]
        height = mask.shape[1]
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/videos/tmp2.mp4', fourcc, fps, (width, height))

    while ret:
        ret, img = cap.read()
        mask = object_detector.apply(img)

        if visualize and ret:
            cv2.imshow('img', mask)
            k = cv2.waitKey(0)
            if k == 27:
                break

        if save_data != -1:
            out.write(mask)

    if visualize:
        cv2.destroyAllWindows()
    cap.release()

    if save_data != -1:
        out.release()

if __name__ == "__main__":
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tanda2/ss5_red2_AlejandroAlonso.mp4'
    output_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tanda2/output.mp4'
    bg_substraction_tracking_max_balls(source_path, max_balls=5, visualize=True, save_data=2, output_path=output_path)
