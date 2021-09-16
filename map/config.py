DEFAULT_SHAPE = (10, 6)
INTERFACE_RELATIVE_INDEX = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}
INTERFACE_UNCHANGE_INDEX = {0: 0, 1: 1, 2: 2,
                            3: 3, 4: 4, 5: 5,
                            6: 6, 7: 7, 8: 8}
INTERFACE_LEFT_INDEX = {0: 6, 1: 3, 2: 0,
                        3: 7, 4: 4, 5: 1,
                        6: 8, 7: 5, 8: 2}
INTERFACE_RIGHT_INDEX = {0: 2, 1: 5, 2: 8,
                         3: 1, 4: 4, 5: 7,
                         6: 0, 7: 3, 8: 6}
INTERFACE_AROUND_INDEX = {0: 8, 1: 7, 2: 6,
                          3: 5, 4: 4, 5: 3,
                          6: 2, 7: 1, 8: 0}
INTERFACE_MIRROR_INDEX = {0: 2, 1: 1, 2: 0,
                          3: 5, 4: 4, 5: 3,
                          6: 8, 7: 7, 8: 6}
INTERFACE_MIRRORLF_INDEX = {0: 0, 1: 3, 2: 6,
                            3: 1, 4: 4, 5: 7,
                            6: 2, 7: 5, 8: 8}
INTERFACE_MIRRORRT_INDEX = {0: 8, 1: 5, 2: 2,
                            3: 7, 4: 4, 5: 1,
                            6: 6, 7: 3, 8: 0}
INTERFACE_MIRRORAR_INDEX = {0: 6, 1: 7, 2: 8,
                            3: 3, 4: 4, 5: 5,
                            6: 0, 7: 1, 8: 2}
ROTATE_INDEX_MAP = {
    0: INTERFACE_UNCHANGE_INDEX,
    1: INTERFACE_LEFT_INDEX,
    2: INTERFACE_RIGHT_INDEX,
    3: INTERFACE_AROUND_INDEX,
    4: INTERFACE_MIRROR_INDEX,
    5: INTERFACE_MIRRORLF_INDEX,
    6: INTERFACE_MIRRORRT_INDEX,
    7: INTERFACE_MIRRORAR_INDEX,
}
