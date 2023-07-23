from tracking.color_tracking_max_balls import color_tracking_max_balls
from prediction.seq_extractor import seq_extraction
from prediction.ss_prediction import prediction

def full_metrics(siteswap, source_path, preprocessing, tracking, tracking_params, postprocessing, seq_extractor):
    match tracking:
        case 0:
            ids = color_tracking_max_balls(source_path, tracking_params[0], max_balls=tracking_params[1], visualize=False)

    # SS
    throw_seq = seq_extraction(ids)

    ss = prediction(throw_seq)

    return ss == siteswap