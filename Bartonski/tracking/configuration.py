import sys
import json
import argparse

parser = argparse.ArgumentParser(allow_abbrev=True)

parser.add_argument(
    '--start_frame', '-s', type=int, metavar='START', default=0,
    help='Start program at frame #START'
)

parser.add_argument(
    '--end_frame', '-e', type=int, metavar='END',
    help='End program at frame #END'
)

parser.add_argument(
    '--grey_threshold', '-g', '--gray_threshold',
    type=int, metavar='GREY THRESHOLD', default=255,
    help='''What shades of grey in the detctor mask are counted as
         objects during object detection
         '''
)

parser.add_argument(
    '--area_threshold', '-a', type=int,
    metavar='AREA THRESHOLD', default=100,
    help='''The minimum number of pixels inside an object
         to be counted during objext detection
         '''
)

parser.add_argument(
    '--area_labels', '-l', action="store_true", default=False,
    help='Show the area of each object.'
)

parser.add_argument(
    '--no_trails', action="store_true", default=False,
    help='Do not show the trails showing where the props have been'
)

parser.add_argument(
    '--show_mask', '--mask', '-m', action="store_true", default=False,
    help='''Show the gray scale image used by the object detector,
         instead of the input video.
         '''
)

parser.add_argument(
    '--grid', '-r', action="store_true", default=False,
    help='Show horizontal and vertical lines every 100 pixels'
)

parser.add_argument(
    '--grid_spacing', type=int, metavar='GRID SPACING', default=100,
    help='Adjust the number of pixels between lines displayed by "--grid"'
)

parser.add_argument(
    '--blur_radius', type=int, metavar='BLUR RADIUS',
    help='''Increasing blur radius makes the image blurrier, which may
         increase the area seen by the object detector
         '''
)

parser.add_argument(
    '--throw_roi_bottom', type=int, metavar='PIXELS FROM TOP',
    help='''Bottom edge of of area of interest where props are caught
         and thrown.
         '''
)

parser.add_argument(
    '--detector_history', type=int, metavar='DETECTOR HISTORY', default=100,
    help='''Number of frames available for the object detector to look
         backward during object detection.
         '''
)

parser.add_argument(
    '--tracking_threshold', type=int, metavar='TRACKING THRESHOLD', default=20,
    help='Distance in pixels for objects to be tracked from frame to frame'
)

parser.add_argument(
    '--detector_threshold', type=int, metavar='DETECTOR THRESHOLD', default=40,
    help='Adjust the sensitivity of the object detector'
)

parser.add_argument(
    '--write_throw_mask', action="store_true",
    help='Write throw trails mask to png file.'
)

parser.add_argument(
    '--write_left_hand_mask', action="store_true",
    help='Write left hand trails mask to png file.'
)

parser.add_argument(
    '--write_right_hand_mask', action="store_true",
    help='Write right hand trails mask to png file.'
)

parser.add_argument(
    'VIDEO FILE', type=str,
    help='Input video file'
)

parser.add_argument(
    '--throw_read_mask', type=str, metavar='THROW MASK INPUT FILE',
    help='Png file where locations of throw objects are colored white'
)

parser.add_argument(
    '--left_hand_read_mask', type=str, metavar='LEFT HAND MASK INPUT FILE',
    help='Png file where locations of left hand objects are colored white'
)

parser.add_argument(
    '--right_hand_read_mask', type=str, metavar='RIGHT HAND MASK INPUT FILE',
    help='Png file where locations of right hand objects are colored white'
)
