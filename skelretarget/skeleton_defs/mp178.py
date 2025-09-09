# see original info at https://github.com/walsharry/SLRTP-Sign-Production-Evaluation

IDS = {
    # ------------- TORSO -------------
    'RShoulder': 0,
    'RElbow': 1,
    'RWrist': 2,
    'LShoulder': 3,
    'LElbow': 4,
    'LWrist': 5,
    'RHip': 6,
    'LHip': 7,

    # ------------- RH -------------
    'RHWrist': 8,
    'RThumb1CMC': 9,
    'RThumb2Knuckles': 10,
    'RThumb3IP': 11,
    'RThumb4FingerTip': 12,
    'RIndex1Knuckles': 13,
    'RIndex2PIP': 14,
    'RIndex3DIP': 15,
    'RIndex4FingerTip': 16,
    'RMiddle1Knuckles': 17,
    'RMiddle2PIP': 18,
    'RMiddle3DIP': 19,
    'RMiddle4FingerTip': 20,
    'RRing1Knuckles': 21,
    'RRing2PIP': 22,
    'RRing3DIP': 23,
    'RRing4FingerTip': 24,
    'RPinky1Knuckles': 25,
    'RPinky2PIP': 26,
    'RPinky3DIP': 27,
    'RPinky4FingerTip': 28,

    # ------------- LH -------------
    'LHWrist': 29,
    'LThumb1CMC': 30,
    'LThumb2Knuckles': 31,
    'LThumb3IP': 32,
    'LThumb4FingerTip': 33,
    'LIndex1Knuckles': 34,
    'LIndex2PIP': 35,
    'LIndex3DIP': 36,
    'LIndex4FingerTip': 37,
    'LMiddle1Knuckles': 38,
    'LMiddle2PIP': 39,
    'LMiddle3DIP': 40,
    'LMiddle4FingerTip': 41,
    'LRing1Knuckles': 42,
    'LRing2PIP': 43,
    'LRing3DIP': 44,
    'LRing4FingerTip': 45,
    'LPinky1Knuckles': 46,
    'LPinky2PIP': 47,
    'LPinky3DIP': 48,
    'LPinky4FingerTip': 49,

    # ------------- FACE -------------
    'face0': 50,
    'face1': 51,
    'face2': 52,
    'face3': 53,
    'face4': 54,
    'face5': 55,
    'face6': 56,
    'face7': 57,
    'face8': 58,
    'face9': 59,
    'face10': 60,
    'face11': 61,
    'face12': 62,
    'face13': 63,
    'face14': 64,
    'face15': 65,
    'face16': 66,
    'face17': 67,
    'face18': 68,
    'face19': 69,
    'face20': 70,
    'face21': 71,
    'face22': 72,
    'face23': 73,
    'face24': 74,
    'face25': 75,
    'face26': 76,
    'face27': 77,
    'face28': 78,
    'face29': 79,
    'face30': 80,
    'face31': 81,
    'face32': 82,
    'face33': 83,
    'face34': 84,
    'face35': 85,
    'face36': 86,
    'face37': 87,
    'face38': 88,
    'face39': 89,
    'face40': 90,
    'face41': 91,
    'face42': 92,
    'face43': 93,
    'face44': 94,
    'face45': 95,
    'face46': 96,
    'face47': 97,
    'face48': 98,
    'face49': 99,
    'face50': 100,
    'face51': 101,
    'face52': 102,
    'face53': 103,
    'face54': 104,
    'face55': 105,
    'face56': 106,
    'face57': 107,
    'face58': 108,
    'face59': 109,
    'face60': 110,
    'face61': 111,
    'face62': 112,
    'face63': 113,
    'face64': 114,
    'face65': 115,
    'face66': 116,
    'face67': 117,
    'face68': 118,
    'face69': 119,
    'face70': 120,
    'face71': 121,
    'face72': 122,
    'face73': 123,
    'face74': 124,
    'face75': 125,
    'face76': 126,
    'face77': 127,
    'face78': 128,
    'face79': 129,
    'face80': 130,
    'face81': 131,
    'face82': 132,
    'face83': 133,
    'face84': 134,
    'face85': 135,
    'face86': 136,
    'face87': 137,
    'face88': 138,
    'face89': 139,
    'face90': 140,
    'face91': 141,
    'face92': 142,
    'face93': 143,
    'face94': 144,
    'face95': 145,
    'face96': 146,
    'face97': 147,
    'face98': 148,
    'face99': 149,
    'face100': 150,
    'face101': 151,
    'face102': 152,
    'face103': 153,
    'face104': 154,
    'face105': 155,
    'face106': 156,
    'face107': 157,
    'face108': 158,
    'face109': 159,
    'face110': 160,
    'face111': 161,
    'face112': 162,
    'face113': 163,
    'face114': 164,
    'face115': 165,
    'face116': 166,
    'face117': 167,
    'face118': 168,
    'face119': 169,
    'face120': 170,
    'face121': 171,
    'face122': 172,
    'face123': 173,
    'face124': 174,
    'face125': 175,
    'face126': 176,
    'face127': 177,
}

# format = (ID_Parent, ID_Child)
CONNECTIONS = [
    # ------------- TORSO -------------
    (0, 1, 0.36),  # RShoulder -> RElbow
    (1, 2, 0.27),  # RElbow -> RWrist

    (3, 4, 0.36),  # LShoulder -> LElbow
    (4, 5, 0.27),  # LElbow -> LWrist

    (0, 3, None),  # RShoulder -> LShoulder
    (0, 6, None),  # RShoulder -> RHip
    (3, 7, None),  # LShoulder -> LHip
    (6, 7, None),  # RHip -> LHip

    # ------------- RH -------------
    (2, 8, 0.01),  # RWrist
    (8, 9, 0.06),  # RHWrist -> RThumb1CMC
    (9, 10, 0.04),  # RThumb1CMC -> RThumb2Knuckles
    (10, 11, 0.03),  # RThumb2Knuckles -> RThumb3IP
    (11, 12, 0.025),  # RThumb3IP -> RThumb4FingerTip

    (8, 13, 0.12),  # RHWrist -> RIndex1Knuckles
    (13, 14, 0.05),  # RIndex1Knuckles -> RIndex2PIP
    (14, 15, 0.04),  # RIndex2PIP -> RIndex3DIP
    (15, 16, 0.025),  # RIndex3DIP -> RIndex4FingerTip

    (13, 17, 0.02),  # RIndex1Knuckles -> RMiddle1Knuckles
    (17, 18, 0.055),  # RMiddle1Knuckles -> RMiddle2PIP
    (18, 19, 0.04),  # RMiddle2PIP -> RMiddle3DIP
    (19, 20, 0.025),  # RMiddle3DIP -> RMiddle4FingerTip

    (17, 21, 0.02),  # RMiddle1Knuckles -> RRing1Knuckles
    (21, 22, 0.04),  # RRing1Knuckles -> RRing2PIP
    (22, 23, 0.035),  # RRing2PIP -> RRing3DIP
    (23, 24, 0.025),  # RRing3DIP -> RRing4FingerTip

    (21, 25, 0.02),  # RRing1Knuckles -> RPinky1Knuckles
    (25, 26, 0.035),  # RPinky1Knuckles -> RPinky2PIP
    (26, 27, 0.03),  # RPinky2PIP -> RPinky3DIP
    (27, 28, 0.025),  # RPinky3DIP -> RPinky4FingerTip

    (25, 8, None),  # RPinky1Knuckles -> RWrist

    # ------------- LH -------------
    (5, 29, 0.01),  # LWrist
    (29, 30, 0.06),  # LWrist -> LThumb1CMC
    (30, 31, 0.04),  # LThumb1CMC -> LThumb2Knuckles
    (31, 32, 0.03),  # LThumb2Knuckles -> LThumb3IP
    (32, 33, 0.025),  # LThumb3IP -> LThumb4FingerTip

    (29, 34, 0.12),  # LWrist -> LIndex1Knuckles
    (34, 35, 0.05),  # LIndex1Knuckles -> LIndex2PIP
    (35, 36, 0.04),  # LIndex2PIP -> LIndex3DIP
    (36, 37, 0.025),  # LIndex3DIP -> LIndex4FingerTip

    (34, 38, 0.02),  # LIndex1Knuckles -> LMiddle1Knuckles
    (38, 39, 0.055),  # LMiddle1Knuckles -> LMiddle2PIP
    (39, 40, 0.04),  # LMiddle2PIP -> LMiddle3DIP
    (40, 41, 0.025),  # LMiddle3DIP -> LMiddle4FingerTip

    (38, 42, 0.02),  # LMiddle1Knuckles -> LRing1Knuckles
    (42, 43, 0.04),  # LRing1Knuckles -> LRing2PIP
    (43, 44, 0.035),  # LRing2PIP -> LRing3DIP
    (44, 45, 0.025),  # LRing3DIP -> LRing4FingerTip

    (42, 46, 0.02),  # LRing1Knuckles -> LPinky1Knuckles
    (46, 47, 0.035),  # LPinky1Knuckles -> LPinky2PIP
    (47, 48, 0.03),  # LPinky2PIP -> LPinky3DIP
    (48, 49, 0.025),  # LPinky3DIP -> LPinky4FingerTip

    (46, 29, None),  # LPinky1Knuckles -> LWrist

    # ------------- FACE -------------
    (126, 127, None),
    (127, 96, None),
    (96, 97, None),
    (97, 150, None),
    (150, 151, None),
    (151, 169, None),
    (169, 114, None),
    (114, 115, None),
    (115, 116, None),
    (116, 171, None),
    (171, 133, None),
    (133, 88, None),
    (88, 89, None),
    (89, 93, None),
    (93, 94, None),
    (94, 67, None),
    (67, 68, None),
    (68, 132, None),
    (132, 117, None),
    (117, 118, None),
    (118, 177, None),
    (177, 145, None),
    (145, 134, None),
    (134, 135, None),
    (135, 137, None),
    (137, 75, None),
    (75, 76, None),
    (76, 139, None),
    (139, 98, None),
    (98, 99, None),
    (99, 136, None),
    (136, 109, None),
    (109, 110, None),
    (110, 154, None),
    (154, 174, None),
    (174, 126, None),
    (147, 77, None),
    (77, 78, None),
    (78, 152, None),
    (152, 153, None),
    (153, 122, None),
    (122, 121, None),
    (121, 144, None),
    (144, 143, None),
    (143, 161, None),
    (161, 147, None),
    (70, 69, None),
    (69, 146, None),
    (146, 57, None),
    (57, 56, None),
    (56, 158, None),
    (158, 111, None),
    (111, 112, None),
    (112, 155, None),
    (155, 176, None),
    (176, 70, None),
    (82, 81, None),
    (81, 125, None),
    (125, 124, None),
    (124, 106, None),
    (106, 105, None),
    (105, 164, None),
    (164, 173, None),
    (173, 141, None),
    (141, 142, None),
    (142, 128, None),
    (128, 129, None),
    (129, 168, None),
    (168, 113, None),
    (113, 79, None),
    (79, 80, None),
    (80, 87, None),
    (87, 86, None),
    (86, 163, None),
    (163, 162, None),
    (162, 82, None),
    (95, 130, None),
    (130, 55, None),
    (55, 54, None),
    (54, 84, None),
    (84, 51, None),
    (51, 50, None),
    (50, 62, None),
    (62, 61, None),
    (61, 167, None),
    (167, 166, None),
    (166, 172, None),
    (172, 175, None),
    (175, 140, None),
    (140, 58, None),
    (58, 59, None),
    (59, 123, None),
    (123, 165, None),
    (165, 91, None),
    (91, 92, None),
    (92, 95, None)
]

DATA = {"IDS": IDS, "CONNECTIONS": CONNECTIONS}
