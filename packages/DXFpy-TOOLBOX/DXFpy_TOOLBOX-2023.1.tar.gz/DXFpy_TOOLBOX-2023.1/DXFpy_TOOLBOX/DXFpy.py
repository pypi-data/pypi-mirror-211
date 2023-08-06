#############################################################################################
# Python native libraries
from tkinter import filedialog
import sys
from operator import itemgetter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#############################################################################################
# DXF FILE IMPORT LIBRARY
def IMPORT_TWO_DIMENSIONAL_DXF():
    """
    This function imports and reads a DXF file; finds the coordinates of the joints, purlins
    and frames; calculates the purlin influence lengths, frame lengths and frame angles and
    plots the 2D drawing using the matplotlib library.

    Input:
    FILENAME      |  File uploaded (.dxf extension)  |     |  file
    UNIT          |  File metric unit                |     |  string
                  |    m
                  |    cm
                  |    mm

    Output:
    JOINT_COORD   |  Joint coordinates               |  m  |  py list
    PURLIN_COORD  |  Purlin coordinates              |  m  |  py dictionary
    INF_LENGTH    |  Influence lengths               |  m  |  py dictionary
    FRAME_COORD   |  Frame coordinates               |  m  |  py dictionary
    FRAME_LENGTH  |  Frame lengths                   |  m  |  py dictionary
    FRAME_ANGLE   |  Frame angles                    | rad |  py dictionary
    DF_JOINTS     |  Joints DataFrame                |     |  py pandas DataFrame
    DF_PURLINS    |  Purlins DataFrame               |     |  py pandas DataFrame
    DF_FRAMES     |  Frames DataFrame                |     |  py pandas DataFrame
    """

    # IMPORTS AND READS THE DXF FILE
    FILENAME = filedialog.askopenfilename(title='Select the file',
                                          filetypes=[('DXF file', '*.dxf')])
    if not FILENAME.endswith('.dxf'):
        MESSAGE = 'No file loaded.' if not FILENAME else \
            'Error: Only .dxf files are supported.'
        print(MESSAGE)
        sys.exit()
    with open(FILENAME, 'r', encoding='utf-8') as file:
        FILE_CONTENT = file.read().split('\n')

    # ADJUSTS THE METRIC UNIT TO THE SI
    UNIT_FACTORS = {'m': 1, 'cm': 1e-2, 'mm': 1e-3}
    while True:
        UNIT = input('Enter the metric unit of the .dxf file (m/cm/mm): ')
        if UNIT in UNIT_FACTORS:
            UNIT_FACTOR = UNIT_FACTORS[UNIT]
            break
        else:
            print('Invalid unit. Please enter one of the following options: m/cm/mm.')

    # POSITION RANGE OF COORDINATES IN FILE CONTENT
    POSITION = (range(12, 16, 2), range(18, 22, 2))

    # FINDS THE JOINT COORDINATES IN THE FILE CONTENT
    JOINT_COORD = []
    for j, LINE in enumerate(FILE_CONTENT):
        if LINE == 'LINE':
            COORD = tuple(tuple(round(float(FILE_CONTENT[j + i]), 12) * UNIT_FACTOR
                                for i in POSITION[k]) for k in range(2))
            JOINT_COORD.append(COORD[0] + COORD[1])
    JOINT_COORD = list(set(JOINT_COORD))
    JOINT_COORD.sort()

    # FINDS THE PURLIN LAYERS IN THE FILE CONTENT
    PURLIN_GROUPS = []
    for j, LINE in enumerate(FILE_CONTENT):
        if LINE == 'POINT':
            PURLIN_GROUPS.append(FILE_CONTENT[j + 8])
    PURLIN_GROUPS = list(set(PURLIN_GROUPS))
    PURLIN_GROUPS.sort()

    # FINDS THE PURLIN COORDINATES IN THE FILE CONTENT
    PURLIN_GROUP, PURLIN_COORD = [], {}
    for GROUP in PURLIN_GROUPS:
        GROUP_COORD = []
        for j, LINE in enumerate(FILE_CONTENT):
            if LINE == 'POINT' and FILE_CONTENT[j + 8] == GROUP:
                PURLIN_GROUP.append(GROUP)
                COORD = tuple(round(float(FILE_CONTENT[j + i]), 12) * UNIT_FACTOR
                              for i in POSITION[0])
                GROUP_COORD.append(COORD)
        PURLIN_COORD[GROUP] = GROUP_COORD
        PURLIN_COORD[GROUP] = sorted(PURLIN_COORD[GROUP], key=itemgetter(0, 1))

    # CALCULATES THE PURLIN INFLUENCE LENGTHS
    INF_LENGTH = {}
    for GROUP in PURLIN_GROUPS:
        GROUP_INF_LENGTH, LAST = [], len(PURLIN_COORD[GROUP]) - 1
        for i, (X, Y) in enumerate(PURLIN_COORD[GROUP]):
            X_0, Y_0 = (X, Y) if i == 0 else PURLIN_COORD[GROUP][i - 1]
            X_1, Y_1 = (X, Y) if i == LAST else PURLIN_COORD[GROUP][i + 1]
            D_0 = np.linalg.norm([X - X_0, Y - Y_0]) / 2
            D_1 = np.linalg.norm([X_1 - X, Y_1 - Y]) / 2
            GROUP_INF_LENGTH.append(D_0 + D_1)
        INF_LENGTH[GROUP] = GROUP_INF_LENGTH

    # FINDS THE FRAME LAYERS IN THE FILE CONTENT
    FRAME_GROUPS = []
    for j, LINE in enumerate(FILE_CONTENT):
        if LINE == 'LINE':
            FRAME_GROUPS.append(FILE_CONTENT[j + 8])
    FRAME_GROUPS = list(set(FRAME_GROUPS))
    FRAME_GROUPS.sort()

    # FINDS THE FRAME COORDINATES IN THE FILE CONTENT
    FRAME_GROUP, FRAME_COORD = [], {}
    for GROUP in FRAME_GROUPS:
        GROUP_COORD = []
        for j, LINE in enumerate(FILE_CONTENT):
            if LINE == 'LINE' and FILE_CONTENT[j + 8] == GROUP:
                FRAME_GROUP.append(GROUP)
                COORD = tuple(tuple(round(float(FILE_CONTENT[j + i]), 12) * UNIT_FACTOR
                                    for i in POSITION[k]) for k in range(2))
                GROUP_COORD.append(sorted([COORD[0], COORD[1]]))
        FRAME_COORD[GROUP] = GROUP_COORD
        FRAME_COORD[GROUP].sort()

    # CALCULATES THE LENGTHS AND ANGLES OF THE FRAMES
    FRAME_LENGTH, FRAME_ANGLE = {}, {}
    for GROUP in FRAME_GROUPS:
        GROUP_LENGTH, GROUP_ANGLE = [], []
        for FRAME in FRAME_COORD[GROUP]:
            (X_0, Y_0), (X, Y) = FRAME
            # calculates the frame length
            LENGTH = np.linalg.norm([X - X_0, Y - Y_0])
            GROUP_LENGTH.append(LENGTH)
            # calculates the frame angle, in radians
            ALPHA_X = np.arccos((X - X_0) / LENGTH)  # x-axis
            ALPHA_Y = np.arccos((Y - Y_0) / LENGTH)  # y-axis
            GROUP_ANGLE.append((ALPHA_X, ALPHA_Y))
        FRAME_LENGTH[GROUP], FRAME_ANGLE[GROUP] = GROUP_LENGTH, GROUP_ANGLE

    # CREATES DATAFRAME WITH JOINT COORDINATES
    DATA_JOINTS = {'X': [COORD[0] for COORD in JOINT_COORD],
                   'Y': [COORD[1] for COORD in JOINT_COORD]}
    DF_JOINTS = pd.DataFrame(DATA_JOINTS, index=[j + 1 for j in range(len(JOINT_COORD))])

    # CREATES DATAFRAME WITH THE GROUPS, COORDINATES AND INFLUENCE LENGTHS OF THE PURLINS
    DATA_PURLINS = {'GROUP': PURLIN_GROUP,
                    'X': [COORD[0] for PG in PURLIN_GROUPS for COORD in PURLIN_COORD[PG]],
                    'Y': [COORD[1] for PG in PURLIN_GROUPS for COORD in PURLIN_COORD[PG]],
                    'INF_LENGTH': [LENGTH for PG in PURLIN_GROUPS for LENGTH in INF_LENGTH[PG]]}
    DF_PURLINS = pd.DataFrame(DATA_PURLINS, index=[p + 1 for p in range(len(PURLIN_GROUP))])

    # CREATES DATAFRAME WITH THE GROUPS, COORDINATES, LENGTHS AND ANGLES OF THE FRAMES
    DATA_FRAMES = {'GROUP': FRAME_GROUP,
                   'X_0': [COORD[0][0] for FG in FRAME_GROUPS for COORD in FRAME_COORD[FG]],
                   'Y_0': [COORD[0][1] for FG in FRAME_GROUPS for COORD in FRAME_COORD[FG]],
                   'X': [COORD[1][0] for FG in FRAME_GROUPS for COORD in FRAME_COORD[FG]],
                   'Y': [COORD[1][1] for FG in FRAME_GROUPS for COORD in FRAME_COORD[FG]],
                   'LENGTH': [LENGTH for FG in FRAME_GROUPS for LENGTH in FRAME_LENGTH[FG]],
                   'ALPHA_X': [ANGLE[0] for FG in FRAME_GROUPS for ANGLE in FRAME_ANGLE[FG]],
                   'ALPHA_Y': [ANGLE[1] for FG in FRAME_GROUPS for ANGLE in FRAME_ANGLE[FG]]}
    DF_FRAMES = pd.DataFrame(DATA_FRAMES, index=[f + 1 for f in range(len(FRAME_GROUP))])

    # DATAFRAMES DISPLAY SETTINGS
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    # FINDS THE LAYER COLORS IN THE FILE CONTENT
    # DXF file color table
    COLOR_TABLE = {
        0: (0, 0, 0), 1: (255, 0, 0), 2: (255, 255, 0), 3: (0, 255, 0),
        4: (0, 255, 255), 5: (0, 0, 255), 6: (255, 0, 255), 7: (255, 255, 255),
        8: (65, 65, 65), 9: (128, 128, 128), 10: (255, 0, 0), 11: (255, 170, 170),
        12: (189, 0, 0), 13: (189, 126, 126), 14: (129, 0, 0), 15: (129, 86, 86),
        16: (104, 0, 0), 17: (104, 69, 69), 18: (79, 0, 0), 19: (79, 53, 53),
        20: (255, 63, 0), 21: (255, 191, 170), 22: (189, 46, 0), 23: (189, 141, 126),
        24: (129, 31, 0), 25: (129, 96, 86), 26: (104, 25, 0), 27: (104, 78, 69),
        28: (79, 19, 0), 29: (79, 59, 53), 30: (255, 127, 0), 31: (255, 212, 170),
        32: (189, 94, 0), 33: (189, 157, 126), 34: (129, 64, 0), 35: (129, 107, 86),
        36: (104, 52, 0), 37: (104, 86, 69), 38: (79, 39, 0), 39: (79, 66, 53),
        40: (255, 191, 0), 41: (255, 234, 170), 42: (189, 141, 0), 43: (189, 173, 126),
        44: (129, 96, 0), 45: (129, 118, 86), 46: (104, 78, 0), 47: (104, 95, 69),
        48: (79, 59, 0), 49: (79, 73, 53), 50: (255, 255, 0), 51: (255, 255, 170),
        52: (189, 189, 0), 53: (189, 189, 126), 54: (129, 129, 0), 55: (129, 129, 86),
        56: (104, 104, 0), 57: (104, 104, 69), 58: (79, 79, 0), 59: (79, 79, 53),
        60: (191, 255, 0), 61: (234, 255, 170), 62: (141, 189, 0), 63: (173, 189, 126),
        64: (96, 129, 0), 65: (118, 129, 86), 66: (78, 104, 0), 67: (95, 104, 69),
        68: (59, 79, 0), 69: (73, 79, 53), 70: (127, 255, 0), 71: (212, 255, 170),
        72: (94, 189, 0), 73: (157, 189, 126), 74: (64, 129, 0), 75: (107, 129, 86),
        76: (52, 104, 0), 77: (86, 104, 69), 78: (39, 79, 0), 79: (66, 79, 53),
        80: (63, 255, 0), 81: (191, 255, 170), 82: (46, 189, 0), 83: (141, 189, 126),
        84: (31, 129, 0), 85: (96, 129, 86), 86: (25, 104, 0), 87: (78, 104, 69),
        88: (19, 79, 0), 89: (59, 79, 53), 90: (0, 255, 0), 91: (170, 255, 170),
        92: (0, 189, 0), 93: (126, 189, 126), 94: (0, 129, 0), 95: (86, 129, 86),
        96: (0, 104, 0), 97: (69, 104, 69), 98: (0, 79, 0), 99: (53, 79, 53),
        100: (0, 255, 63), 101: (170, 255, 191), 102: (0, 189, 46), 103: (126, 189, 141),
        104: (0, 129, 31), 105: (86, 129, 96), 106: (0, 104, 25), 107: (69, 104, 78),
        108: (0, 79, 19), 109: (53, 79, 59), 110: (0, 255, 127), 111: (170, 255, 212),
        112: (0, 189, 94), 113: (126, 189, 157), 114: (0, 129, 64), 115: (86, 129, 107),
        116: (0, 104, 52), 117: (69, 104, 86), 118: (0, 79, 39), 119: (53, 79, 66),
        120: (0, 255, 191), 121: (170, 255, 234), 122: (0, 189, 141), 123: (126, 189, 173),
        124: (0, 129, 96), 125: (86, 129, 118), 126: (0, 104, 78), 127: (69, 104, 95),
        128: (0, 79, 59), 129: (53, 79, 73), 130: (0, 255, 255), 131: (170, 255, 255),
        132: (0, 189, 189), 133: (126, 189, 189), 134: (0, 129, 129), 135: (86, 129, 129),
        136: (0, 104, 104), 137: (69, 104, 104), 138: (0, 79, 79), 139: (53, 79, 79),
        140: (0, 191, 255), 141: (170, 234, 255), 142: (0, 141, 189), 143: (126, 173, 189),
        144: (0, 96, 129), 145: (86, 118, 129), 146: (0, 78, 104), 147: (69, 95, 104),
        148: (0, 59, 79), 149: (53, 73, 79), 150: (0, 127, 255), 151: (170, 212, 255),
        152: (0, 94, 189), 153: (126, 157, 189), 154: (0, 64, 129), 155: (86, 107, 129),
        156: (0, 52, 104), 157: (69, 86, 104), 158: (0, 39, 79), 159: (53, 66, 79),
        160: (0, 63, 255), 161: (170, 191, 255), 162: (0, 46, 189), 163: (126, 141, 189),
        164: (0, 31, 129), 165: (86, 96, 129), 166: (0, 25, 104), 167: (69, 78, 104),
        168: (0, 19, 79), 169: (53, 59, 79), 170: (0, 0, 255), 171: (170, 170, 255),
        172: (0, 0, 189), 173: (126, 126, 189), 174: (0, 0, 129), 175: (86, 86, 129),
        176: (0, 0, 104), 177: (69, 69, 104), 178: (0, 0, 79), 179: (53, 53, 79),
        180: (63, 0, 255), 181: (191, 170, 255), 182: (46, 0, 189), 183: (141, 126, 189),
        184: (31, 0, 129), 185: (96, 86, 129), 186: (25, 0, 104), 187: (78, 69, 104),
        188: (19, 0, 79), 189: (59, 53, 79), 190: (127, 0, 255), 191: (212, 170, 255),
        192: (94, 0, 189), 193: (157, 126, 189), 194: (64, 0, 129), 195: (107, 86, 129),
        196: (52, 0, 104), 197: (86, 69, 104), 198: (39, 0, 79), 199: (66, 53, 79),
        200: (191, 0, 255), 201: (234, 170, 255), 202: (141, 0, 189), 203: (173, 126, 189),
        204: (96, 0, 129), 205: (118, 86, 129), 206: (78, 0, 104), 207: (95, 69, 104),
        208: (59, 0, 79), 209: (73, 53, 79), 210: (255, 0, 255), 211: (255, 170, 255),
        212: (189, 0, 189), 213: (189, 126, 189), 214: (129, 0, 129), 215: (129, 86, 129),
        216: (104, 0, 104), 217: (104, 69, 104), 218: (79, 0, 79), 219: (79, 53, 79),
        220: (255, 0, 191), 221: (255, 170, 234), 222: (189, 0, 141), 223: (189, 126, 173),
        224: (129, 0, 96), 225: (129, 86, 118), 226: (104, 0, 78), 227: (104, 69, 95),
        228: (79, 0, 59), 229: (79, 53, 73), 230: (255, 0, 127), 231: (255, 170, 212),
        232: (189, 0, 94), 233: (189, 126, 157), 234: (129, 0, 64), 235: (129, 86, 107),
        236: (104, 0, 52), 237: (104, 69, 86), 238: (79, 0, 39), 239: (79, 53, 66),
        240: (255, 0, 63), 241: (255, 170, 191), 242: (189, 0, 46), 243: (189, 126, 141),
        244: (129, 0, 31), 245: (129, 86, 96), 246: (104, 0, 25), 247: (104, 69, 78),
        248: (79, 0, 19), 249: (79, 53, 59), 250: (51, 51, 51), 251: (80, 80, 80),
        252: (105, 105, 105), 253: (130, 130, 130), 254: (190, 190, 190), 255: (255, 255, 255)
    }
    COLORS = {}
    for j, LINE in enumerate(FILE_CONTENT):
        if LINE == 'LAYER' and FILE_CONTENT[j + 13] == ' 62':
            GROUP = FILE_CONTENT[j + 10]
            INDEX_COLOR = int(FILE_CONTENT[j + 14].replace('     ', ''))
            COLORS[GROUP] = tuple(COLOR_TABLE[INDEX_COLOR][i] / 255 for i in range(3))

    # PLOTS THE 2D DRAWING
    # plots the purlins
    for GROUP in PURLIN_GROUPS:
        for i, PURLIN in enumerate(PURLIN_COORD[GROUP]):
            X, Y = PURLIN
            plt.scatter(X, Y, color=COLORS[GROUP], label=GROUP if i == 0 else None)
    # plots the frames
    for GROUP in FRAME_GROUPS:
        for i, FRAME in enumerate(FRAME_COORD[GROUP]):
            X, Y = zip(*FRAME)
            plt.plot(X, Y, color=COLORS[GROUP], label=GROUP if i == 0 else None)
    # axes adjustments
    MIN_VALUE = np.min(DF_JOINTS[['X', 'Y']].values) - 0.1
    MAX_VALUE = np.max(DF_JOINTS[['X', 'Y']].values) + 0.1
    plt.xlim(MIN_VALUE, MAX_VALUE)
    plt.ylim(MIN_VALUE, MAX_VALUE)
    plt.xticks(list(set(DF_JOINTS['X'])))
    plt.yticks(list(set(DF_JOINTS['Y'])))
    plt.xlabel('X axis [m]')
    plt.ylabel('Y axis [m]')
    plt.legend()

    return (JOINT_COORD, PURLIN_COORD, INF_LENGTH, FRAME_COORD, FRAME_LENGTH, FRAME_ANGLE,DF_JOINTS, DF_PURLINS, DF_FRAMES)