from typing import Union, Any, Callable, Optional, List  # NOQA

import lvgl as _lvgl



class EXPLORER:
    SORT_NONE = _lvgl.EXPLORER_SORT_NONE
    SORT_KIND = _lvgl.EXPLORER_SORT_KIND
    HOME_DIR = _lvgl.EXPLORER_HOME_DIR
    MUSIC_DIR = _lvgl.EXPLORER_MUSIC_DIR
    PICTURES_DIR = _lvgl.EXPLORER_PICTURES_DIR
    VIDEO_DIR = _lvgl.EXPLORER_VIDEO_DIR
    DOCS_DIR = _lvgl.EXPLORER_DOCS_DIR
    FS_DIR = _lvgl.EXPLORER_FS_DIR


class INDEV_TYPE:
    NONE = _lvgl.INDEV_TYPE_NONE
    POINTER = _lvgl.INDEV_TYPE_POINTER
    KEYPAD = _lvgl.INDEV_TYPE_KEYPAD
    BUTTON = _lvgl.INDEV_TYPE_BUTTON
    ENCODER = _lvgl.INDEV_TYPE_ENCODER


class INDEV_STATE:
    RELEASED = _lvgl.INDEV_STATE_RELEASED
    PRESSED = _lvgl.INDEV_STATE_PRESSED


class DRAW_MASK:
    RES_TRANSP = _lvgl.DRAW_MASK_RES_TRANSP
    RES_FULL_COVER = _lvgl.DRAW_MASK_RES_FULL_COVER
    RES_CHANGED = _lvgl.DRAW_MASK_RES_CHANGED
    RES_UNKNOWN = _lvgl.DRAW_MASK_RES_UNKNOWN
    TYPE_LINE = _lvgl.DRAW_MASK_TYPE_LINE
    TYPE_ANGLE = _lvgl.DRAW_MASK_TYPE_ANGLE
    TYPE_RADIUS = _lvgl.DRAW_MASK_TYPE_RADIUS
    TYPE_FADE = _lvgl.DRAW_MASK_TYPE_FADE
    TYPE_MAP = _lvgl.DRAW_MASK_TYPE_MAP
    TYPE_POLYGON = _lvgl.DRAW_MASK_TYPE_POLYGON
    LINE_SIDE_LEFT = _lvgl.DRAW_MASK_LINE_SIDE_LEFT
    LINE_SIDE_RIGHT = _lvgl.DRAW_MASK_LINE_SIDE_RIGHT
    LINE_SIDE_TOP = _lvgl.DRAW_MASK_LINE_SIDE_TOP
    LINE_SIDE_BOTTOM = _lvgl.DRAW_MASK_LINE_SIDE_BOTTOM


class DRAW_LAYER:
    FLAG_NONE = _lvgl.DRAW_LAYER_FLAG_NONE
    FLAG_HAS_ALPHA = _lvgl.DRAW_LAYER_FLAG_HAS_ALPHA
    FLAG_CAN_SUBDIVIDE = _lvgl.DRAW_LAYER_FLAG_CAN_SUBDIVIDE


class FS_RES:
    OK = _lvgl.FS_RES_OK
    HW_ERR = _lvgl.FS_RES_HW_ERR
    FS_ERR = _lvgl.FS_RES_FS_ERR
    NOT_EX = _lvgl.FS_RES_NOT_EX
    FULL = _lvgl.FS_RES_FULL
    LOCKED = _lvgl.FS_RES_LOCKED
    DENIED = _lvgl.FS_RES_DENIED
    BUSY = _lvgl.FS_RES_BUSY
    TOUT = _lvgl.FS_RES_TOUT
    NOT_IMP = _lvgl.FS_RES_NOT_IMP
    OUT_OF_MEM = _lvgl.FS_RES_OUT_OF_MEM
    INV_PARAM = _lvgl.FS_RES_INV_PARAM
    UNKNOWN = _lvgl.FS_RES_UNKNOWN


class FS_MODE:
    WR = _lvgl.FS_MODE_WR
    RD = _lvgl.FS_MODE_RD


class FS_SEEK:
    SET = _lvgl.FS_SEEK_SET
    CUR = _lvgl.FS_SEEK_CUR
    END = _lvgl.FS_SEEK_END


class DISP_ROTATION:
    _0 = _lvgl.DISP_ROTATION_0
    _90 = _lvgl.DISP_ROTATION_90
    _180 = _lvgl.DISP_ROTATION_180
    _270 = _lvgl.DISP_ROTATION_270


class FONT_SUBPX:
    NONE = _lvgl.FONT_SUBPX_NONE
    HOR = _lvgl.FONT_SUBPX_HOR
    VER = _lvgl.FONT_SUBPX_VER
    BOTH = _lvgl.FONT_SUBPX_BOTH

PART_MAIN = _lvgl.ANIM_IMG_PART_MAIN


class SPAN_MODE:
    FIXED = _lvgl.SPAN_MODE_FIXED
    EXPAND = _lvgl.SPAN_MODE_EXPAND
    BREAK = _lvgl.SPAN_MODE_BREAK


class SPAN_OVERFLOW:
    CLIP = _lvgl.SPAN_OVERFLOW_CLIP
    ELLIPSIS = _lvgl.SPAN_OVERFLOW_ELLIPSIS


class FLEX_ALIGN:
    START = _lvgl.FLEX_ALIGN_START
    END = _lvgl.FLEX_ALIGN_END
    CENTER = _lvgl.FLEX_ALIGN_CENTER
    SPACE_EVENLY = _lvgl.FLEX_ALIGN_SPACE_EVENLY
    SPACE_AROUND = _lvgl.FLEX_ALIGN_SPACE_AROUND
    SPACE_BETWEEN = _lvgl.FLEX_ALIGN_SPACE_BETWEEN


class FLEX_FLOW:
    ROW = _lvgl.FLEX_FLOW_ROW
    COLUMN = _lvgl.FLEX_FLOW_COLUMN
    ROW_WRAP = _lvgl.FLEX_FLOW_ROW_WRAP
    ROW_REVERSE = _lvgl.FLEX_FLOW_ROW_REVERSE
    ROW_WRAP_REVERSE = _lvgl.FLEX_FLOW_ROW_WRAP_REVERSE
    COLUMN_WRAP = _lvgl.FLEX_FLOW_COLUMN_WRAP
    COLUMN_REVERSE = _lvgl.FLEX_FLOW_COLUMN_REVERSE
    COLUMN_WRAP_REVERSE = _lvgl.FLEX_FLOW_COLUMN_WRAP_REVERSE


class GRID_ALIGN:
    START = _lvgl.GRID_ALIGN_START
    CENTER = _lvgl.GRID_ALIGN_CENTER
    END = _lvgl.GRID_ALIGN_END
    STRETCH = _lvgl.GRID_ALIGN_STRETCH
    SPACE_EVENLY = _lvgl.GRID_ALIGN_SPACE_EVENLY
    SPACE_AROUND = _lvgl.GRID_ALIGN_SPACE_AROUND
    SPACE_BETWEEN = _lvgl.GRID_ALIGN_SPACE_BETWEEN


class GRID:
    CONTENT = _lvgl.GRID_CONTENT
    TEMPLATE_LAST = _lvgl.GRID_TEMPLATE_LAST


class COLOR_FORMAT:
    UNKNOWN = _lvgl.COLOR_FORMAT_UNKNOWN
    L8 = _lvgl.COLOR_FORMAT_L8
    A8 = _lvgl.COLOR_FORMAT_A8
    I1 = _lvgl.COLOR_FORMAT_I1
    I2 = _lvgl.COLOR_FORMAT_I2
    I4 = _lvgl.COLOR_FORMAT_I4
    I8 = _lvgl.COLOR_FORMAT_I8
    A8L8 = _lvgl.COLOR_FORMAT_A8L8
    ARGB2222 = _lvgl.COLOR_FORMAT_ARGB2222
    RGB565 = _lvgl.COLOR_FORMAT_RGB565
    RGB565_CHROMA_KEYED = _lvgl.COLOR_FORMAT_RGB565_CHROMA_KEYED
    ARGB1555 = _lvgl.COLOR_FORMAT_ARGB1555
    ARGB4444 = _lvgl.COLOR_FORMAT_ARGB4444
    RGB565A8 = _lvgl.COLOR_FORMAT_RGB565A8
    ARGB8565 = _lvgl.COLOR_FORMAT_ARGB8565
    RGB888 = _lvgl.COLOR_FORMAT_RGB888
    RGB888_CHROMA_KEYED = _lvgl.COLOR_FORMAT_RGB888_CHROMA_KEYED
    ARGB8888 = _lvgl.COLOR_FORMAT_ARGB8888
    XRGB8888 = _lvgl.COLOR_FORMAT_XRGB8888
    XRGB8888_CHROMA_KEYED = _lvgl.COLOR_FORMAT_XRGB8888_CHROMA_KEYED
    NATIVE = _lvgl.COLOR_FORMAT_NATIVE
    NATIVE_CHROMA_KEYED = _lvgl.COLOR_FORMAT_NATIVE_CHROMA_KEYED
    NATIVE_ALPHA = _lvgl.COLOR_FORMAT_NATIVE_ALPHA
    NATIVE_REVERSED = _lvgl.COLOR_FORMAT_NATIVE_REVERSED
    NATIVE_ALPHA_REVERSED = _lvgl.COLOR_FORMAT_NATIVE_ALPHA_REVERSED
    RAW = _lvgl.COLOR_FORMAT_RAW
    RAW_ALPHA = _lvgl.COLOR_FORMAT_RAW_ALPHA


class STYLE_RES:
    NOT_FOUND = _lvgl.STYLE_RES_NOT_FOUND
    FOUND = _lvgl.STYLE_RES_FOUND
    INHERIT = _lvgl.STYLE_RES_INHERIT


class STYLE_PROP:
    INV = _lvgl.STYLE_PROP_INV
    ANY = _lvgl.STYLE_PROP_ANY

_MPY_API = _lvgl._MPY_API

DPI_DEF = _lvgl.DPI_DEF


class RES:
    INV = _lvgl.RES_INV
    OK = _lvgl.RES_OK


class LOG_LEVEL:
    TRACE = _lvgl.LOG_LEVEL_TRACE
    INFO = _lvgl.LOG_LEVEL_INFO
    WARN = _lvgl.LOG_LEVEL_WARN
    ERROR = _lvgl.LOG_LEVEL_ERROR
    USER = _lvgl.LOG_LEVEL_USER
    NONE = _lvgl.LOG_LEVEL_NONE


class ANIM:
    REPEAT_INFINITE = _lvgl.ANIM_REPEAT_INFINITE
    PLAYTIME_INFINITE = _lvgl.ANIM_PLAYTIME_INFINITE
    OFF = _lvgl.ANIM_OFF
    ON = _lvgl.ANIM_ON


class _STR:
    SYMBOL_BULLET = _lvgl._STR_SYMBOL_BULLET
    SYMBOL_AUDIO = _lvgl._STR_SYMBOL_AUDIO
    SYMBOL_VIDEO = _lvgl._STR_SYMBOL_VIDEO
    SYMBOL_LIST = _lvgl._STR_SYMBOL_LIST
    SYMBOL_OK = _lvgl._STR_SYMBOL_OK
    SYMBOL_CLOSE = _lvgl._STR_SYMBOL_CLOSE
    SYMBOL_POWER = _lvgl._STR_SYMBOL_POWER
    SYMBOL_SETTINGS = _lvgl._STR_SYMBOL_SETTINGS
    SYMBOL_HOME = _lvgl._STR_SYMBOL_HOME
    SYMBOL_DOWNLOAD = _lvgl._STR_SYMBOL_DOWNLOAD
    SYMBOL_DRIVE = _lvgl._STR_SYMBOL_DRIVE
    SYMBOL_REFRESH = _lvgl._STR_SYMBOL_REFRESH
    SYMBOL_MUTE = _lvgl._STR_SYMBOL_MUTE
    SYMBOL_VOLUME_MID = _lvgl._STR_SYMBOL_VOLUME_MID
    SYMBOL_VOLUME_MAX = _lvgl._STR_SYMBOL_VOLUME_MAX
    SYMBOL_IMAGE = _lvgl._STR_SYMBOL_IMAGE
    SYMBOL_TINT = _lvgl._STR_SYMBOL_TINT
    SYMBOL_PREV = _lvgl._STR_SYMBOL_PREV
    SYMBOL_PLAY = _lvgl._STR_SYMBOL_PLAY
    SYMBOL_PAUSE = _lvgl._STR_SYMBOL_PAUSE
    SYMBOL_STOP = _lvgl._STR_SYMBOL_STOP
    SYMBOL_NEXT = _lvgl._STR_SYMBOL_NEXT
    SYMBOL_EJECT = _lvgl._STR_SYMBOL_EJECT
    SYMBOL_LEFT = _lvgl._STR_SYMBOL_LEFT
    SYMBOL_RIGHT = _lvgl._STR_SYMBOL_RIGHT
    SYMBOL_PLUS = _lvgl._STR_SYMBOL_PLUS
    SYMBOL_MINUS = _lvgl._STR_SYMBOL_MINUS
    SYMBOL_EYE_OPEN = _lvgl._STR_SYMBOL_EYE_OPEN
    SYMBOL_EYE_CLOSE = _lvgl._STR_SYMBOL_EYE_CLOSE
    SYMBOL_WARNING = _lvgl._STR_SYMBOL_WARNING
    SYMBOL_SHUFFLE = _lvgl._STR_SYMBOL_SHUFFLE
    SYMBOL_UP = _lvgl._STR_SYMBOL_UP
    SYMBOL_DOWN = _lvgl._STR_SYMBOL_DOWN
    SYMBOL_LOOP = _lvgl._STR_SYMBOL_LOOP
    SYMBOL_DIRECTORY = _lvgl._STR_SYMBOL_DIRECTORY
    SYMBOL_UPLOAD = _lvgl._STR_SYMBOL_UPLOAD
    SYMBOL_CALL = _lvgl._STR_SYMBOL_CALL
    SYMBOL_CUT = _lvgl._STR_SYMBOL_CUT
    SYMBOL_COPY = _lvgl._STR_SYMBOL_COPY
    SYMBOL_SAVE = _lvgl._STR_SYMBOL_SAVE
    SYMBOL_BARS = _lvgl._STR_SYMBOL_BARS
    SYMBOL_ENVELOPE = _lvgl._STR_SYMBOL_ENVELOPE
    SYMBOL_CHARGE = _lvgl._STR_SYMBOL_CHARGE
    SYMBOL_PASTE = _lvgl._STR_SYMBOL_PASTE
    SYMBOL_BELL = _lvgl._STR_SYMBOL_BELL
    SYMBOL_KEYBOARD = _lvgl._STR_SYMBOL_KEYBOARD
    SYMBOL_GPS = _lvgl._STR_SYMBOL_GPS
    SYMBOL_FILE = _lvgl._STR_SYMBOL_FILE
    SYMBOL_WIFI = _lvgl._STR_SYMBOL_WIFI
    SYMBOL_BATTERY_FULL = _lvgl._STR_SYMBOL_BATTERY_FULL
    SYMBOL_BATTERY_3 = _lvgl._STR_SYMBOL_BATTERY_3
    SYMBOL_BATTERY_2 = _lvgl._STR_SYMBOL_BATTERY_2
    SYMBOL_BATTERY_1 = _lvgl._STR_SYMBOL_BATTERY_1
    SYMBOL_BATTERY_EMPTY = _lvgl._STR_SYMBOL_BATTERY_EMPTY
    SYMBOL_USB = _lvgl._STR_SYMBOL_USB
    SYMBOL_BLUETOOTH = _lvgl._STR_SYMBOL_BLUETOOTH
    SYMBOL_TRASH = _lvgl._STR_SYMBOL_TRASH
    SYMBOL_EDIT = _lvgl._STR_SYMBOL_EDIT
    SYMBOL_BACKSPACE = _lvgl._STR_SYMBOL_BACKSPACE
    SYMBOL_SD_CARD = _lvgl._STR_SYMBOL_SD_CARD
    SYMBOL_NEW_LINE = _lvgl._STR_SYMBOL_NEW_LINE
    SYMBOL_DUMMY = _lvgl._STR_SYMBOL_DUMMY


class ALIGN:
    DEFAULT = _lvgl.ALIGN_DEFAULT
    TOP_LEFT = _lvgl.ALIGN_TOP_LEFT
    TOP_MID = _lvgl.ALIGN_TOP_MID
    TOP_RIGHT = _lvgl.ALIGN_TOP_RIGHT
    BOTTOM_LEFT = _lvgl.ALIGN_BOTTOM_LEFT
    BOTTOM_MID = _lvgl.ALIGN_BOTTOM_MID
    BOTTOM_RIGHT = _lvgl.ALIGN_BOTTOM_RIGHT
    LEFT_MID = _lvgl.ALIGN_LEFT_MID
    RIGHT_MID = _lvgl.ALIGN_RIGHT_MID
    CENTER = _lvgl.ALIGN_CENTER
    OUT_TOP_LEFT = _lvgl.ALIGN_OUT_TOP_LEFT
    OUT_TOP_MID = _lvgl.ALIGN_OUT_TOP_MID
    OUT_TOP_RIGHT = _lvgl.ALIGN_OUT_TOP_RIGHT
    OUT_BOTTOM_LEFT = _lvgl.ALIGN_OUT_BOTTOM_LEFT
    OUT_BOTTOM_MID = _lvgl.ALIGN_OUT_BOTTOM_MID
    OUT_BOTTOM_RIGHT = _lvgl.ALIGN_OUT_BOTTOM_RIGHT
    OUT_LEFT_TOP = _lvgl.ALIGN_OUT_LEFT_TOP
    OUT_LEFT_MID = _lvgl.ALIGN_OUT_LEFT_MID
    OUT_LEFT_BOTTOM = _lvgl.ALIGN_OUT_LEFT_BOTTOM
    OUT_RIGHT_TOP = _lvgl.ALIGN_OUT_RIGHT_TOP
    OUT_RIGHT_MID = _lvgl.ALIGN_OUT_RIGHT_MID
    OUT_RIGHT_BOTTOM = _lvgl.ALIGN_OUT_RIGHT_BOTTOM


class DIR:
    NONE = _lvgl.DIR_NONE
    LEFT = _lvgl.DIR_LEFT
    RIGHT = _lvgl.DIR_RIGHT
    TOP = _lvgl.DIR_TOP
    BOTTOM = _lvgl.DIR_BOTTOM
    HOR = _lvgl.DIR_HOR
    VER = _lvgl.DIR_VER
    ALL = _lvgl.DIR_ALL

SIZE_CONTENT = _lvgl.SIZE_CONTENT


class COORD:
    MAX = _lvgl.COORD_MAX
    MIN = _lvgl.COORD_MIN

COLOR_DEPTH = _lvgl.COLOR_DEPTH


class OPA:
    TRANSP = _lvgl.OPA_TRANSP
    _0 = _lvgl.OPA_0
    _10 = _lvgl.OPA_10
    _20 = _lvgl.OPA_20
    _30 = _lvgl.OPA_30
    _40 = _lvgl.OPA_40
    _50 = _lvgl.OPA_50
    _60 = _lvgl.OPA_60
    _70 = _lvgl.OPA_70
    _80 = _lvgl.OPA_80
    _90 = _lvgl.OPA_90
    _100 = _lvgl.OPA_100
    COVER = _lvgl.OPA_COVER


class PALETTE:
    RED = _lvgl.PALETTE_RED
    PINK = _lvgl.PALETTE_PINK
    PURPLE = _lvgl.PALETTE_PURPLE
    DEEP_PURPLE = _lvgl.PALETTE_DEEP_PURPLE
    INDIGO = _lvgl.PALETTE_INDIGO
    BLUE = _lvgl.PALETTE_BLUE
    LIGHT_BLUE = _lvgl.PALETTE_LIGHT_BLUE
    CYAN = _lvgl.PALETTE_CYAN
    TEAL = _lvgl.PALETTE_TEAL
    GREEN = _lvgl.PALETTE_GREEN
    LIGHT_GREEN = _lvgl.PALETTE_LIGHT_GREEN
    LIME = _lvgl.PALETTE_LIME
    YELLOW = _lvgl.PALETTE_YELLOW
    AMBER = _lvgl.PALETTE_AMBER
    ORANGE = _lvgl.PALETTE_ORANGE
    DEEP_ORANGE = _lvgl.PALETTE_DEEP_ORANGE
    BROWN = _lvgl.PALETTE_BROWN
    BLUE_GREY = _lvgl.PALETTE_BLUE_GREY
    GREY = _lvgl.PALETTE_GREY
    NONE = _lvgl.PALETTE_NONE

_PALETTE_LAST = _lvgl._PALETTE_LAST


class TEXT_FLAG:
    NONE = _lvgl.TEXT_FLAG_NONE
    RECOLOR = _lvgl.TEXT_FLAG_RECOLOR
    EXPAND = _lvgl.TEXT_FLAG_EXPAND
    FIT = _lvgl.TEXT_FLAG_FIT
    CMD_STATE_WAIT = _lvgl.TEXT_CMD_STATE_WAIT
    CMD_STATE_PAR = _lvgl.TEXT_CMD_STATE_PAR
    CMD_STATE_IN = _lvgl.TEXT_CMD_STATE_IN
    ALIGN_AUTO = _lvgl.TEXT_ALIGN_AUTO
    ALIGN_LEFT = _lvgl.TEXT_ALIGN_LEFT
    ALIGN_CENTER = _lvgl.TEXT_ALIGN_CENTER
    ALIGN_RIGHT = _lvgl.TEXT_ALIGN_RIGHT
    DECOR_NONE = _lvgl.TEXT_DECOR_NONE
    DECOR_UNDERLINE = _lvgl.TEXT_DECOR_UNDERLINE
    DECOR_STRIKETHROUGH = _lvgl.TEXT_DECOR_STRIKETHROUGH


class BASE_DIR:
    LTR = _lvgl.BASE_DIR_LTR
    RTL = _lvgl.BASE_DIR_RTL
    AUTO = _lvgl.BASE_DIR_AUTO
    NEUTRAL = _lvgl.BASE_DIR_NEUTRAL
    WEAK = _lvgl.BASE_DIR_WEAK

ZOOM_NONE = _lvgl.ZOOM_NONE


class BLEND_MODE:
    NORMAL = _lvgl.BLEND_MODE_NORMAL
    ADDITIVE = _lvgl.BLEND_MODE_ADDITIVE
    SUBTRACTIVE = _lvgl.BLEND_MODE_SUBTRACTIVE
    MULTIPLY = _lvgl.BLEND_MODE_MULTIPLY
    REPLACE = _lvgl.BLEND_MODE_REPLACE


class BORDER_SIDE:
    NONE = _lvgl.BORDER_SIDE_NONE
    BOTTOM = _lvgl.BORDER_SIDE_BOTTOM
    TOP = _lvgl.BORDER_SIDE_TOP
    LEFT = _lvgl.BORDER_SIDE_LEFT
    RIGHT = _lvgl.BORDER_SIDE_RIGHT
    FULL = _lvgl.BORDER_SIDE_FULL
    INTERNAL = _lvgl.BORDER_SIDE_INTERNAL


class GRAD_DIR:
    NONE = _lvgl.GRAD_DIR_NONE
    VER = _lvgl.GRAD_DIR_VER
    HOR = _lvgl.GRAD_DIR_HOR


class DITHER:
    NONE = _lvgl.DITHER_NONE
    ORDERED = _lvgl.DITHER_ORDERED
    ERR_DIFF = _lvgl.DITHER_ERR_DIFF


class STYLE:
    WIDTH = _lvgl.STYLE_WIDTH
    MIN_WIDTH = _lvgl.STYLE_MIN_WIDTH
    MAX_WIDTH = _lvgl.STYLE_MAX_WIDTH
    HEIGHT = _lvgl.STYLE_HEIGHT
    MIN_HEIGHT = _lvgl.STYLE_MIN_HEIGHT
    MAX_HEIGHT = _lvgl.STYLE_MAX_HEIGHT
    X = _lvgl.STYLE_X
    Y = _lvgl.STYLE_Y
    ALIGN = _lvgl.STYLE_ALIGN
    LAYOUT = _lvgl.STYLE_LAYOUT
    RADIUS = _lvgl.STYLE_RADIUS
    PAD_TOP = _lvgl.STYLE_PAD_TOP
    PAD_BOTTOM = _lvgl.STYLE_PAD_BOTTOM
    PAD_LEFT = _lvgl.STYLE_PAD_LEFT
    PAD_RIGHT = _lvgl.STYLE_PAD_RIGHT
    PAD_ROW = _lvgl.STYLE_PAD_ROW
    PAD_COLUMN = _lvgl.STYLE_PAD_COLUMN
    BASE_DIR = _lvgl.STYLE_BASE_DIR
    CLIP_CORNER = _lvgl.STYLE_CLIP_CORNER
    MARGIN_TOP = _lvgl.STYLE_MARGIN_TOP
    MARGIN_BOTTOM = _lvgl.STYLE_MARGIN_BOTTOM
    MARGIN_LEFT = _lvgl.STYLE_MARGIN_LEFT
    MARGIN_RIGHT = _lvgl.STYLE_MARGIN_RIGHT
    BG_COLOR = _lvgl.STYLE_BG_COLOR
    BG_OPA = _lvgl.STYLE_BG_OPA
    BG_GRAD_COLOR = _lvgl.STYLE_BG_GRAD_COLOR
    BG_GRAD_DIR = _lvgl.STYLE_BG_GRAD_DIR
    BG_MAIN_STOP = _lvgl.STYLE_BG_MAIN_STOP
    BG_GRAD_STOP = _lvgl.STYLE_BG_GRAD_STOP
    BG_GRAD = _lvgl.STYLE_BG_GRAD
    BG_DITHER_MODE = _lvgl.STYLE_BG_DITHER_MODE
    BG_IMG_SRC = _lvgl.STYLE_BG_IMG_SRC
    BG_IMG_OPA = _lvgl.STYLE_BG_IMG_OPA
    BG_IMG_RECOLOR = _lvgl.STYLE_BG_IMG_RECOLOR
    BG_IMG_RECOLOR_OPA = _lvgl.STYLE_BG_IMG_RECOLOR_OPA
    BG_IMG_TILED = _lvgl.STYLE_BG_IMG_TILED
    BORDER_COLOR = _lvgl.STYLE_BORDER_COLOR
    BORDER_OPA = _lvgl.STYLE_BORDER_OPA
    BORDER_WIDTH = _lvgl.STYLE_BORDER_WIDTH
    BORDER_SIDE = _lvgl.STYLE_BORDER_SIDE
    BORDER_POST = _lvgl.STYLE_BORDER_POST
    OUTLINE_WIDTH = _lvgl.STYLE_OUTLINE_WIDTH
    OUTLINE_COLOR = _lvgl.STYLE_OUTLINE_COLOR
    OUTLINE_OPA = _lvgl.STYLE_OUTLINE_OPA
    OUTLINE_PAD = _lvgl.STYLE_OUTLINE_PAD
    SHADOW_WIDTH = _lvgl.STYLE_SHADOW_WIDTH
    SHADOW_OFS_X = _lvgl.STYLE_SHADOW_OFS_X
    SHADOW_OFS_Y = _lvgl.STYLE_SHADOW_OFS_Y
    SHADOW_SPREAD = _lvgl.STYLE_SHADOW_SPREAD
    SHADOW_COLOR = _lvgl.STYLE_SHADOW_COLOR
    SHADOW_OPA = _lvgl.STYLE_SHADOW_OPA
    IMG_OPA = _lvgl.STYLE_IMG_OPA
    IMG_RECOLOR = _lvgl.STYLE_IMG_RECOLOR
    IMG_RECOLOR_OPA = _lvgl.STYLE_IMG_RECOLOR_OPA
    LINE_WIDTH = _lvgl.STYLE_LINE_WIDTH
    LINE_DASH_WIDTH = _lvgl.STYLE_LINE_DASH_WIDTH
    LINE_DASH_GAP = _lvgl.STYLE_LINE_DASH_GAP
    LINE_ROUNDED = _lvgl.STYLE_LINE_ROUNDED
    LINE_COLOR = _lvgl.STYLE_LINE_COLOR
    LINE_OPA = _lvgl.STYLE_LINE_OPA
    ARC_WIDTH = _lvgl.STYLE_ARC_WIDTH
    ARC_ROUNDED = _lvgl.STYLE_ARC_ROUNDED
    ARC_COLOR = _lvgl.STYLE_ARC_COLOR
    ARC_OPA = _lvgl.STYLE_ARC_OPA
    ARC_IMG_SRC = _lvgl.STYLE_ARC_IMG_SRC
    TEXT_COLOR = _lvgl.STYLE_TEXT_COLOR
    TEXT_OPA = _lvgl.STYLE_TEXT_OPA
    TEXT_FONT = _lvgl.STYLE_TEXT_FONT
    TEXT_LETTER_SPACE = _lvgl.STYLE_TEXT_LETTER_SPACE
    TEXT_LINE_SPACE = _lvgl.STYLE_TEXT_LINE_SPACE
    TEXT_DECOR = _lvgl.STYLE_TEXT_DECOR
    TEXT_ALIGN = _lvgl.STYLE_TEXT_ALIGN
    OPA = _lvgl.STYLE_OPA
    COLOR_FILTER_DSC = _lvgl.STYLE_COLOR_FILTER_DSC
    COLOR_FILTER_OPA = _lvgl.STYLE_COLOR_FILTER_OPA
    ANIM = _lvgl.STYLE_ANIM
    ANIM_TIME = _lvgl.STYLE_ANIM_TIME
    ANIM_SPEED = _lvgl.STYLE_ANIM_SPEED
    TRANSITION = _lvgl.STYLE_TRANSITION
    BLEND_MODE = _lvgl.STYLE_BLEND_MODE
    TRANSFORM_WIDTH = _lvgl.STYLE_TRANSFORM_WIDTH
    TRANSFORM_HEIGHT = _lvgl.STYLE_TRANSFORM_HEIGHT
    TRANSLATE_X = _lvgl.STYLE_TRANSLATE_X
    TRANSLATE_Y = _lvgl.STYLE_TRANSLATE_Y
    TRANSFORM_ZOOM = _lvgl.STYLE_TRANSFORM_ZOOM
    TRANSFORM_ANGLE = _lvgl.STYLE_TRANSFORM_ANGLE
    TRANSFORM_PIVOT_X = _lvgl.STYLE_TRANSFORM_PIVOT_X
    TRANSFORM_PIVOT_Y = _lvgl.STYLE_TRANSFORM_PIVOT_Y


class _STYLE:
    LAST_BUILT_IN_PROP = _lvgl._STYLE_LAST_BUILT_IN_PROP
    NUM_BUILT_IN_PROPS = _lvgl._STYLE_NUM_BUILT_IN_PROPS
    PROP_CONST = _lvgl._STYLE_PROP_CONST
    STATE_CMP_SAME = _lvgl._STYLE_STATE_CMP_SAME
    STATE_CMP_DIFF_REDRAW = _lvgl._STYLE_STATE_CMP_DIFF_REDRAW
    STATE_CMP_DIFF_DRAW_PAD = _lvgl._STYLE_STATE_CMP_DIFF_DRAW_PAD
    STATE_CMP_DIFF_LAYOUT = _lvgl._STYLE_STATE_CMP_DIFF_LAYOUT


class STATE:
    DEFAULT = _lvgl.STATE_DEFAULT
    CHECKED = _lvgl.STATE_CHECKED
    FOCUSED = _lvgl.STATE_FOCUSED
    FOCUS_KEY = _lvgl.STATE_FOCUS_KEY
    EDITED = _lvgl.STATE_EDITED
    HOVERED = _lvgl.STATE_HOVERED
    PRESSED = _lvgl.STATE_PRESSED
    SCROLLED = _lvgl.STATE_SCROLLED
    DISABLED = _lvgl.STATE_DISABLED
    USER_1 = _lvgl.STATE_USER_1
    USER_2 = _lvgl.STATE_USER_2
    USER_3 = _lvgl.STATE_USER_3
    USER_4 = _lvgl.STATE_USER_4
    ANY = _lvgl.STATE_ANY


class PART:
    MAIN = _lvgl.PART_MAIN
    SCROLLBAR = _lvgl.PART_SCROLLBAR
    INDICATOR = _lvgl.PART_INDICATOR
    KNOB = _lvgl.PART_KNOB
    SELECTED = _lvgl.PART_SELECTED
    ITEMS = _lvgl.PART_ITEMS
    TICKS = _lvgl.PART_TICKS
    CURSOR = _lvgl.PART_CURSOR
    CUSTOM_FIRST = _lvgl.PART_CUSTOM_FIRST
    ANY = _lvgl.PART_ANY
    TEXTAREA_PLACEHOLDER = _lvgl.PART_TEXTAREA_PLACEHOLDER


class EVENT:
    ALL = _lvgl.EVENT_ALL
    PRESSED = _lvgl.EVENT_PRESSED
    PRESSING = _lvgl.EVENT_PRESSING
    PRESS_LOST = _lvgl.EVENT_PRESS_LOST
    SHORT_CLICKED = _lvgl.EVENT_SHORT_CLICKED
    LONG_PRESSED = _lvgl.EVENT_LONG_PRESSED
    LONG_PRESSED_REPEAT = _lvgl.EVENT_LONG_PRESSED_REPEAT
    CLICKED = _lvgl.EVENT_CLICKED
    RELEASED = _lvgl.EVENT_RELEASED
    SCROLL_BEGIN = _lvgl.EVENT_SCROLL_BEGIN
    SCROLL_THROW_BEGIN = _lvgl.EVENT_SCROLL_THROW_BEGIN
    SCROLL_END = _lvgl.EVENT_SCROLL_END
    SCROLL = _lvgl.EVENT_SCROLL
    GESTURE = _lvgl.EVENT_GESTURE
    KEY = _lvgl.EVENT_KEY
    FOCUSED = _lvgl.EVENT_FOCUSED
    DEFOCUSED = _lvgl.EVENT_DEFOCUSED
    LEAVE = _lvgl.EVENT_LEAVE
    HIT_TEST = _lvgl.EVENT_HIT_TEST
    COVER_CHECK = _lvgl.EVENT_COVER_CHECK
    REFR_EXT_DRAW_SIZE = _lvgl.EVENT_REFR_EXT_DRAW_SIZE
    DRAW_MAIN_BEGIN = _lvgl.EVENT_DRAW_MAIN_BEGIN
    DRAW_MAIN = _lvgl.EVENT_DRAW_MAIN
    DRAW_MAIN_END = _lvgl.EVENT_DRAW_MAIN_END
    DRAW_POST_BEGIN = _lvgl.EVENT_DRAW_POST_BEGIN
    DRAW_POST = _lvgl.EVENT_DRAW_POST
    DRAW_POST_END = _lvgl.EVENT_DRAW_POST_END
    DRAW_PART_BEGIN = _lvgl.EVENT_DRAW_PART_BEGIN
    DRAW_PART_END = _lvgl.EVENT_DRAW_PART_END
    VALUE_CHANGED = _lvgl.EVENT_VALUE_CHANGED
    INSERT = _lvgl.EVENT_INSERT
    REFRESH = _lvgl.EVENT_REFRESH
    READY = _lvgl.EVENT_READY
    CANCEL = _lvgl.EVENT_CANCEL
    DELETE = _lvgl.EVENT_DELETE
    CHILD_CHANGED = _lvgl.EVENT_CHILD_CHANGED
    CHILD_CREATED = _lvgl.EVENT_CHILD_CREATED
    CHILD_DELETED = _lvgl.EVENT_CHILD_DELETED
    SCREEN_UNLOAD_START = _lvgl.EVENT_SCREEN_UNLOAD_START
    SCREEN_LOAD_START = _lvgl.EVENT_SCREEN_LOAD_START
    SCREEN_LOADED = _lvgl.EVENT_SCREEN_LOADED
    SCREEN_UNLOADED = _lvgl.EVENT_SCREEN_UNLOADED
    SIZE_CHANGED = _lvgl.EVENT_SIZE_CHANGED
    STYLE_CHANGED = _lvgl.EVENT_STYLE_CHANGED
    LAYOUT_CHANGED = _lvgl.EVENT_LAYOUT_CHANGED
    GET_SELF_SIZE = _lvgl.EVENT_GET_SELF_SIZE
    MSG_RECEIVED = _lvgl.EVENT_MSG_RECEIVED
    INVALIDATE_AREA = _lvgl.EVENT_INVALIDATE_AREA
    RENDER_START = _lvgl.EVENT_RENDER_START
    RENDER_READY = _lvgl.EVENT_RENDER_READY
    RESOLUTION_CHANGED = _lvgl.EVENT_RESOLUTION_CHANGED
    REFR_START = _lvgl.EVENT_REFR_START
    REFR_FINISH = _lvgl.EVENT_REFR_FINISH
    PREPROCESS = _lvgl.EVENT_PREPROCESS

_EVENT_LAST = _lvgl._EVENT_LAST


class DISP_RENDER:
    MODE_PARTIAL = _lvgl.DISP_RENDER_MODE_PARTIAL
    MODE_DIRECT = _lvgl.DISP_RENDER_MODE_DIRECT
    MODE_FULL = _lvgl.DISP_RENDER_MODE_FULL


class SCR_LOAD:
    ANIM_NONE = _lvgl.SCR_LOAD_ANIM_NONE
    ANIM_OVER_LEFT = _lvgl.SCR_LOAD_ANIM_OVER_LEFT
    ANIM_OVER_RIGHT = _lvgl.SCR_LOAD_ANIM_OVER_RIGHT
    ANIM_OVER_TOP = _lvgl.SCR_LOAD_ANIM_OVER_TOP
    ANIM_OVER_BOTTOM = _lvgl.SCR_LOAD_ANIM_OVER_BOTTOM
    ANIM_MOVE_LEFT = _lvgl.SCR_LOAD_ANIM_MOVE_LEFT
    ANIM_MOVE_RIGHT = _lvgl.SCR_LOAD_ANIM_MOVE_RIGHT
    ANIM_MOVE_TOP = _lvgl.SCR_LOAD_ANIM_MOVE_TOP
    ANIM_MOVE_BOTTOM = _lvgl.SCR_LOAD_ANIM_MOVE_BOTTOM
    ANIM_FADE_IN = _lvgl.SCR_LOAD_ANIM_FADE_IN
    ANIM_FADE_ON = _lvgl.SCR_LOAD_ANIM_FADE_ON
    ANIM_FADE_OUT = _lvgl.SCR_LOAD_ANIM_FADE_OUT
    ANIM_OUT_LEFT = _lvgl.SCR_LOAD_ANIM_OUT_LEFT
    ANIM_OUT_RIGHT = _lvgl.SCR_LOAD_ANIM_OUT_RIGHT
    ANIM_OUT_TOP = _lvgl.SCR_LOAD_ANIM_OUT_TOP
    ANIM_OUT_BOTTOM = _lvgl.SCR_LOAD_ANIM_OUT_BOTTOM


class SCROLLBAR_MODE:
    OFF = _lvgl.SCROLLBAR_MODE_OFF
    ON = _lvgl.SCROLLBAR_MODE_ON
    ACTIVE = _lvgl.SCROLLBAR_MODE_ACTIVE
    AUTO = _lvgl.SCROLLBAR_MODE_AUTO


class SCROLL_SNAP:
    NONE = _lvgl.SCROLL_SNAP_NONE
    START = _lvgl.SCROLL_SNAP_START
    END = _lvgl.SCROLL_SNAP_END
    CENTER = _lvgl.SCROLL_SNAP_CENTER

RADIUS_CIRCLE = _lvgl.RADIUS_CIRCLE


class COVER_RES:
    COVER = _lvgl.COVER_RES_COVER
    NOT_COVER = _lvgl.COVER_RES_NOT_COVER
    MASKED = _lvgl.COVER_RES_MASKED


class LAYER_TYPE:
    NONE = _lvgl.LAYER_TYPE_NONE
    SIMPLE = _lvgl.LAYER_TYPE_SIMPLE
    TRANSFORM = _lvgl.LAYER_TYPE_TRANSFORM


class KEY:
    UP = _lvgl.KEY_UP
    DOWN = _lvgl.KEY_DOWN
    RIGHT = _lvgl.KEY_RIGHT
    LEFT = _lvgl.KEY_LEFT
    ESC = _lvgl.KEY_ESC
    DEL = _lvgl.KEY_DEL
    BACKSPACE = _lvgl.KEY_BACKSPACE
    ENTER = _lvgl.KEY_ENTER
    NEXT = _lvgl.KEY_NEXT
    PREV = _lvgl.KEY_PREV
    HOME = _lvgl.KEY_HOME
    END = _lvgl.KEY_END


class GROUP_REFOCUS:
    POLICY_NEXT = _lvgl.GROUP_REFOCUS_POLICY_NEXT
    POLICY_PREV = _lvgl.GROUP_REFOCUS_POLICY_PREV


class FONT_FMT:
    TXT_CMAP_FORMAT0_FULL = _lvgl.FONT_FMT_TXT_CMAP_FORMAT0_FULL
    TXT_CMAP_SPARSE_FULL = _lvgl.FONT_FMT_TXT_CMAP_SPARSE_FULL
    TXT_CMAP_FORMAT0_TINY = _lvgl.FONT_FMT_TXT_CMAP_FORMAT0_TINY
    TXT_CMAP_SPARSE_TINY = _lvgl.FONT_FMT_TXT_CMAP_SPARSE_TINY
    TXT_PLAIN = _lvgl.FONT_FMT_TXT_PLAIN
    TXT_COMPRESSED = _lvgl.FONT_FMT_TXT_COMPRESSED
    TXT_COMPRESSED_NO_PREFILTER = _lvgl.FONT_FMT_TXT_COMPRESSED_NO_PREFILTER


class _BTNMATRIX:
    WIDTH = _lvgl._BTNMATRIX_WIDTH
    CTRL_RESERVED_1 = _lvgl._BTNMATRIX_CTRL_RESERVED_1
    CTRL_RESERVED_2 = _lvgl._BTNMATRIX_CTRL_RESERVED_2

_CHART_AXIS_LAST = _lvgl._CHART_AXIS_LAST

_IMGBTN_STATE_NUM = _lvgl._IMGBTN_STATE_NUM


class GRIDNAV_CTRL:
    NONE = _lvgl.GRIDNAV_CTRL_NONE
    ROLLOVER = _lvgl.GRIDNAV_CTRL_ROLLOVER
    SCROLL_FIRST = _lvgl.GRIDNAV_CTRL_SCROLL_FIRST


class DEMO_BENCHMARK:
    MODE_RENDER_AND_DRIVER = _lvgl.DEMO_BENCHMARK_MODE_RENDER_AND_DRIVER
    MODE_REAL = _lvgl.DEMO_BENCHMARK_MODE_REAL
    MODE_RENDER_ONLY = _lvgl.DEMO_BENCHMARK_MODE_RENDER_ONLY

_tick_dsc_t = _lvgl._tick_dsc_t
_timer_t = _lvgl._timer_t
sqrt_res_t = _lvgl.sqrt_res_t
_anim_t = _lvgl._anim_t
anim_timeline_dsc_t = _lvgl.anim_timeline_dsc_t
_anim_timeline_t = _lvgl._anim_timeline_t
vaformat_t = _lvgl.vaformat_t
font_glyph_dsc_t = _lvgl.font_glyph_dsc_t
_font_t = _lvgl._font_t
color1_t = _lvgl.color1_t
color_hsv_t = _lvgl.color_hsv_t
_color_filter_dsc_t = _lvgl._color_filter_dsc_t
gradient_stop_t = _lvgl.gradient_stop_t
grad_dsc_t = _lvgl.grad_dsc_t
style_value_t = _lvgl.style_value_t
style_const_prop_t = _lvgl.style_const_prop_t
style_v_p_t = _lvgl.style_v_p_t
_event_t = _lvgl._event_t
_event_dsc_t = _lvgl._event_dsc_t
layout_dsc_t = _lvgl.layout_dsc_t
_obj_style_t = _lvgl._obj_style_t
_obj_style_transition_dsc_t = _lvgl._obj_style_transition_dsc_t
img_header_t = _lvgl.img_header_t
_fs_drv_t = _lvgl._fs_drv_t
fs_file_cache_t = _lvgl.fs_file_cache_t
_img_decoder_t = _lvgl._img_decoder_t
_img_decoder_dsc_t = _lvgl._img_decoder_dsc_t
_img_cache_entry_t = _lvgl._img_cache_entry_t
_gradient_cache_t = _lvgl._gradient_cache_t
_draw_label_hint_t = _lvgl._draw_label_hint_t
draw_img_sup_t = _lvgl.draw_img_sup_t
_draw_mask_saved_t = _lvgl._draw_mask_saved_t
_draw_mask_common_dsc_t = _lvgl._draw_mask_common_dsc_t
draw_mask_line_param_cfg_t = _lvgl.draw_mask_line_param_cfg_t
draw_mask_angle_param_cfg_t = _lvgl.draw_mask_angle_param_cfg_t
_draw_mask_radius_circle_dsc_t = _lvgl._draw_mask_radius_circle_dsc_t
draw_mask_radius_param_cfg_t = _lvgl.draw_mask_radius_param_cfg_t
draw_mask_fade_param_cfg_t = _lvgl.draw_mask_fade_param_cfg_t
draw_mask_map_param_cfg_t = _lvgl.draw_mask_map_param_cfg_t
_draw_mask_map_param_t = _lvgl._draw_mask_map_param_t
draw_mask_polygon_param_cfg_t = _lvgl.draw_mask_polygon_param_cfg_t
draw_mask_t = _lvgl.draw_mask_t
draw_layer_ctx_original_t = _lvgl.draw_layer_ctx_original_t
_draw_layer_ctx_t = _lvgl._draw_layer_ctx_t
_draw_ctx_t = _lvgl._draw_ctx_t
_obj_class_t = _lvgl._obj_class_t
ll_t = _lvgl.ll_t
_group_t = _lvgl._group_t
indev_data_t = _lvgl.indev_data_t
hit_test_info_t = _lvgl.hit_test_info_t
cover_check_info_t = _lvgl.cover_check_info_t
_obj_spec_attr_t = _lvgl._obj_spec_attr_t
_obj_t = _lvgl._obj_t
_theme_t = _lvgl._theme_t
font_fmt_txt_glyph_dsc_t = _lvgl.font_fmt_txt_glyph_dsc_t
font_fmt_txt_cmap_t = _lvgl.font_fmt_txt_cmap_t
font_fmt_txt_kern_pair_t = _lvgl.font_fmt_txt_kern_pair_t
font_fmt_txt_kern_classes_t = _lvgl.font_fmt_txt_kern_classes_t
font_fmt_txt_glyph_cache_t = _lvgl.font_fmt_txt_glyph_cache_t
font_fmt_txt_dsc_t = _lvgl.font_fmt_txt_dsc_t
img_t = _lvgl.img_t
animimg_t = _lvgl.animimg_t
arc_t = _lvgl.arc_t
label_dot_t = _lvgl.label_dot_t
label_t = _lvgl.label_t
_bar_anim_t = _lvgl._bar_anim_t
bar_t = _lvgl.bar_t
btn_t = _lvgl.btn_t
btnmatrix_t = _lvgl.btnmatrix_t
calendar_date_t = _lvgl.calendar_date_t
calendar_t = _lvgl.calendar_t
canvas_t = _lvgl.canvas_t
chart_series_t = _lvgl.chart_series_t
chart_cursor_t = _lvgl.chart_cursor_t
chart_tick_dsc_t = _lvgl.chart_tick_dsc_t
chart_t = _lvgl.chart_t
checkbox_t = _lvgl.checkbox_t
colorwheel_knob_t = _lvgl.colorwheel_knob_t
colorwheel_t = _lvgl.colorwheel_t
dropdown_t = _lvgl.dropdown_t
dropdown_list_t = _lvgl.dropdown_list_t
imgbtn_src_info_t = _lvgl.imgbtn_src_info_t
imgbtn_t = _lvgl.imgbtn_t
keyboard_t = _lvgl.keyboard_t
led_t = _lvgl.led_t
line_t = _lvgl.line_t
menu_load_page_event_data_t = _lvgl.menu_load_page_event_data_t
menu_history_t = _lvgl.menu_history_t
menu_t = _lvgl.menu_t
menu_page_t = _lvgl.menu_page_t
meter_indicator_type_data_needle_img_t = _lvgl.meter_indicator_type_data_needle_img_t
meter_indicator_type_data_needle_line_t = _lvgl.meter_indicator_type_data_needle_line_t
meter_indicator_type_data_arc_t = _lvgl.meter_indicator_type_data_arc_t
meter_indicator_type_data_scale_lines_t = _lvgl.meter_indicator_type_data_scale_lines_t
meter_indicator_type_data_t = _lvgl.meter_indicator_type_data_t
meter_indicator_t = _lvgl.meter_indicator_t
meter_scale_t = _lvgl.meter_scale_t
meter_t = _lvgl.meter_t
msgbox_t = _lvgl.msgbox_t
roller_t = _lvgl.roller_t
slider_t = _lvgl.slider_t
spangroup_t = _lvgl.spangroup_t
textarea_cursor_t = _lvgl.textarea_cursor_t
textarea_t = _lvgl.textarea_t
spinbox_t = _lvgl.spinbox_t
switch_t = _lvgl.switch_t
table_t = _lvgl.table_t
tabview_t = _lvgl.tabview_t
tileview_t = _lvgl.tileview_t
tileview_tile_t = _lvgl.tileview_tile_t
win_t = _lvgl.win_t
pinyin_dict_t = _lvgl.pinyin_dict_t
ime_pinyin_k9_py_str_t = _lvgl.ime_pinyin_k9_py_str_t
ime_pinyin_t = _lvgl.ime_pinyin_t
file_explorer_t = _lvgl.file_explorer_t
barcode_t = _lvgl.barcode_t
_gd_Palette = _lvgl._gd_Palette
_gd_GCE = _lvgl._gd_GCE
_gd_GIF = _lvgl._gd_GIF
gif_t = _lvgl.gif_t
qrcode_t = _lvgl.qrcode_t
_disp_t = _lvgl._disp_t
_indev_pointer_t = _lvgl._indev_pointer_t
_indev_keypad_t = _lvgl._indev_keypad_t
_indev_t = _lvgl._indev_t
grad_color_t = _lvgl.grad_color_t
grad_t = _lvgl.grad_t
draw_label_hint_t = _lvgl.draw_label_hint_t
draw_layer_ctx_t = _lvgl.draw_layer_ctx_t
obj_t = _lvgl.obj_t
gd_Palette = _lvgl.gd_Palette
gd_GCE = _lvgl.gd_GCE


_global_cb_store = _lvgl._global_cb_store
tick_cb_t = _lvgl.tick_cb_t
timer_cb_t = _lvgl.timer_cb_t
async_cb_t = _lvgl.async_cb_t
anim_path_cb_t = _lvgl.anim_path_cb_t
anim_custom_exec_cb_t = _lvgl.anim_custom_exec_cb_t
anim_ready_cb_t = _lvgl.anim_ready_cb_t
anim_start_cb_t = _lvgl.anim_start_cb_t
anim_get_value_cb_t = _lvgl.anim_get_value_cb_t
anim_deleted_cb_t = _lvgl.anim_deleted_cb_t
font_get_glyph_dsc_cb_t = _lvgl.font_get_glyph_dsc_cb_t
font_get_glyph_bitmap_cb_t = _lvgl.font_get_glyph_bitmap_cb_t
color_filter_cb_t = _lvgl.color_filter_cb_t
event_cb_t = _lvgl.event_cb_t
disp_flush_cb_t = _lvgl.disp_flush_cb_t
disp_draw_ctx_init_cb_t = _lvgl.disp_draw_ctx_init_cb_t
disp_draw_ctx_deinit_cb_t = _lvgl.disp_draw_ctx_deinit_cb_t
disp_wait_cb_t = _lvgl.disp_wait_cb_t
obj_tree_walk_cb_t = _lvgl.obj_tree_walk_cb_t
layout_update_cb_t = _lvgl.layout_update_cb_t
fs_drv_ready_cb_t = _lvgl.fs_drv_ready_cb_t
fs_drv_open_cb_t = _lvgl.fs_drv_open_cb_t
fs_drv_close_cb_t = _lvgl.fs_drv_close_cb_t
fs_drv_read_cb_t = _lvgl.fs_drv_read_cb_t
fs_drv_write_cb_t = _lvgl.fs_drv_write_cb_t
fs_drv_seek_cb_t = _lvgl.fs_drv_seek_cb_t
fs_drv_tell_cb_t = _lvgl.fs_drv_tell_cb_t
fs_drv_dir_open_cb_t = _lvgl.fs_drv_dir_open_cb_t
fs_drv_dir_read_cb_t = _lvgl.fs_drv_dir_read_cb_t
fs_drv_dir_close_cb_t = _lvgl.fs_drv_dir_close_cb_t
img_decoder_info_f_t = _lvgl.img_decoder_info_f_t
img_decoder_open_f_t = _lvgl.img_decoder_open_f_t
img_decoder_read_line_f_t = _lvgl.img_decoder_read_line_f_t
img_decoder_close_f_t = _lvgl.img_decoder_close_f_t
draw_ctx_init_buf_cb_t = _lvgl.draw_ctx_init_buf_cb_t
draw_ctx_draw_rect_cb_t = _lvgl.draw_ctx_draw_rect_cb_t
draw_ctx_draw_arc_cb_t = _lvgl.draw_ctx_draw_arc_cb_t
draw_ctx_draw_img_decoded_cb_t = _lvgl.draw_ctx_draw_img_decoded_cb_t
draw_ctx_draw_img_cb_t = _lvgl.draw_ctx_draw_img_cb_t
draw_ctx_draw_letter_cb_t = _lvgl.draw_ctx_draw_letter_cb_t
draw_ctx_draw_line_cb_t = _lvgl.draw_ctx_draw_line_cb_t
draw_ctx_draw_polygon_cb_t = _lvgl.draw_ctx_draw_polygon_cb_t
draw_ctx_draw_transform_cb_t = _lvgl.draw_ctx_draw_transform_cb_t
draw_ctx_wait_for_finish_cb_t = _lvgl.draw_ctx_wait_for_finish_cb_t
draw_ctx_buffer_copy_cb_t = _lvgl.draw_ctx_buffer_copy_cb_t
draw_ctx_buffer_convert_cb_t = _lvgl.draw_ctx_buffer_convert_cb_t
draw_ctx_buffer_clear_cb_t = _lvgl.draw_ctx_buffer_clear_cb_t
draw_ctx_layer_init_cb_t = _lvgl.draw_ctx_layer_init_cb_t
draw_ctx_layer_adjust_cb_t = _lvgl.draw_ctx_layer_adjust_cb_t
draw_ctx_layer_blend_cb_t = _lvgl.draw_ctx_layer_blend_cb_t
draw_ctx_layer_destroy_cb_t = _lvgl.draw_ctx_layer_destroy_cb_t
obj_class_constructor_cb_t = _lvgl.obj_class_constructor_cb_t
obj_class_destructor_cb_t = _lvgl.obj_class_destructor_cb_t
obj_class_event_cb_t = _lvgl.obj_class_event_cb_t
group_focus_cb_t = _lvgl.group_focus_cb_t
group_edge_cb_t = _lvgl.group_edge_cb_t
indev_read_cb_t = _lvgl.indev_read_cb_t
theme_apply_cb_t = _lvgl.theme_apply_cb_t
btnmatrix_btn_draw_cb_t = _lvgl.btnmatrix_btn_draw_cb_t
imgfont_get_path_cb_t = _lvgl.imgfont_get_path_cb_t
msg_subscribe_cb_t = _lvgl.msg_subscribe_cb_t
indev_feedback_cb_t = _lvgl.indev_feedback_cb_t
font_montserrat_12_subpx = _lvgl.font_montserrat_12_subpx
font_montserrat_28_compressed = _lvgl.font_montserrat_28_compressed
font_dejavu_16_persian_hebrew = _lvgl.font_dejavu_16_persian_hebrew
font_simsun_16_cjk = _lvgl.font_simsun_16_cjk
font_unscii_8 = _lvgl.font_unscii_8
font_unscii_16 = _lvgl.font_unscii_16
font_montserrat_8 = _lvgl.font_montserrat_8
font_montserrat_10 = _lvgl.font_montserrat_10
font_montserrat_12 = _lvgl.font_montserrat_12
font_montserrat_14 = _lvgl.font_montserrat_14
font_montserrat_16 = _lvgl.font_montserrat_16
font_montserrat_18 = _lvgl.font_montserrat_18
font_montserrat_20 = _lvgl.font_montserrat_20
font_montserrat_22 = _lvgl.font_montserrat_22
font_montserrat_24 = _lvgl.font_montserrat_24
font_montserrat_26 = _lvgl.font_montserrat_26
font_montserrat_28 = _lvgl.font_montserrat_28
font_montserrat_30 = _lvgl.font_montserrat_30
font_montserrat_32 = _lvgl.font_montserrat_32
font_montserrat_34 = _lvgl.font_montserrat_34
font_montserrat_36 = _lvgl.font_montserrat_36
font_montserrat_38 = _lvgl.font_montserrat_38
font_montserrat_40 = _lvgl.font_montserrat_40
font_montserrat_42 = _lvgl.font_montserrat_42
font_montserrat_44 = _lvgl.font_montserrat_44
font_montserrat_46 = _lvgl.font_montserrat_46
font_montserrat_48 = _lvgl.font_montserrat_48



def binding_version() -> "empty":
    return _lvgl.binding_version()


def anim_exec_xcb_t(value: _lvgl.int32_t) -> None:
    return _lvgl.anim_exec_xcb_t(value)


def img_cache_manager_open_xcb_t(src: None, color: "color_t", frame_id: _lvgl.int32_t) -> "img_cache_entry_t":
    return _lvgl.img_cache_manager_open_xcb_t(src, color, frame_id)


def draw_mask_xcb_t(mask_buf: _lvgl.opa_t, abs_x: _lvgl.coord_t, abs_y: _lvgl.coord_t, len: _lvgl.coord_t, p: None) -> _lvgl.draw_mask_res_t:
    return _lvgl.draw_mask_xcb_t(mask_buf, abs_x, abs_y, len, p)


def tick_inc(tick_period: _lvgl.uint32_t) -> None:
    return _lvgl.tick_inc(tick_period)


def tick_get() -> _lvgl.uint32_t:
    return _lvgl.tick_get()


def tick_elaps(prev_tick: _lvgl.uint32_t) -> _lvgl.uint32_t:
    return _lvgl.tick_elaps(prev_tick)


def _timer_core_init() -> None:
    return _lvgl._timer_core_init()


def timer_handler() -> _lvgl.uint32_t:
    return _lvgl.timer_handler()


def timer_handler_run_in_period(ms: _lvgl.uint32_t) -> _lvgl.uint32_t:
    return _lvgl.timer_handler_run_in_period(ms)


def timer_create_basic() -> "timer_t":
    return _lvgl.timer_create_basic()


def timer_enable(en: _lvgl._Bool) -> None:
    return _lvgl.timer_enable(en)


def timer_get_idle() -> _lvgl.uint8_t:
    return _lvgl.timer_get_idle()


def trigo_sin(angle: _lvgl.int16_t) -> _lvgl.int16_t:
    return _lvgl.trigo_sin(angle)


def trigo_cos(angle: _lvgl.int16_t) -> _lvgl.int16_t:
    return _lvgl.trigo_cos(angle)


def bezier3(t: _lvgl.uint32_t, u0: _lvgl.uint32_t, u1: _lvgl.uint32_t, u2: _lvgl.uint32_t, u3: _lvgl.uint32_t) -> _lvgl.uint32_t:
    return _lvgl.bezier3(t, u0, u1, u2, u3)


def atan2(x: _lvgl.int_, y: _lvgl.int_) -> _lvgl.uint16_t:
    return _lvgl.atan2(x, y)


def sqrt(x: _lvgl.uint32_t, q: _lvgl.sqrt_res_t, mask: _lvgl.uint32_t) -> None:
    return _lvgl.sqrt(x, q, mask)


def pow(base: _lvgl.int64_t, exp: _lvgl.int8_t) -> _lvgl.int64_t:
    return _lvgl.pow(base, exp)


def map(x: _lvgl.int32_t, min_in: _lvgl.int32_t, max_in: _lvgl.int32_t, min_out: _lvgl.int32_t, max_out: _lvgl.int32_t) -> _lvgl.int32_t:
    return _lvgl.map(x, min_in, max_in, min_out, max_out)


def rand(min: _lvgl.uint32_t, max: _lvgl.uint32_t) -> _lvgl.uint32_t:
    return _lvgl.rand(min, max)


def malloc(size: _lvgl.size_t) -> Any:
    return _lvgl.malloc(size)


def free(data: None) -> None:
    return _lvgl.free(data)


def realloc(data_p: None, new_size: _lvgl.size_t) -> Any:
    return _lvgl.realloc(data_p, new_size)


def memcpy(dst: None, src: None, len: _lvgl.size_t) -> Any:
    return _lvgl.memcpy(dst, src, len)


def memset(dst: None, v: _lvgl.uint8_t, len: _lvgl.size_t) -> None:
    return _lvgl.memset(dst, v, len)


def memzero(dst: None, len: _lvgl.size_t) -> None:
    return _lvgl.memzero(dst, len)


def strlen(str: _lvgl.char) -> _lvgl.size_t:
    return _lvgl.strlen(str)


def strncpy(dst: _lvgl.char, src: _lvgl.char, dest_size: _lvgl.size_t) -> _lvgl.char:
    return _lvgl.strncpy(dst, src, dest_size)


def strcpy(dst: _lvgl.char, src: _lvgl.char) -> _lvgl.char:
    return _lvgl.strcpy(dst, src)


def mem_test() -> _lvgl.res_t:
    return _lvgl.mem_test()


def async_call(async_xcb: "async_cb_t", user_data: Any) -> _lvgl.res_t:
    return _lvgl.async_call(async_xcb, user_data)


def async_call_cancel(async_xcb: "async_cb_t", user_data: Any) -> _lvgl.res_t:
    return _lvgl.async_call_cancel(async_xcb, user_data)


def _anim_core_init() -> None:
    return _lvgl._anim_core_init()


def anim_del(var: None, exec_cb: "anim_exec_xcb_t") -> _lvgl._Bool:
    return _lvgl.anim_del(var, exec_cb)


def anim_del_all() -> None:
    return _lvgl.anim_del_all()


def anim_get(var: None, exec_cb: "anim_exec_xcb_t") -> "anim_t":
    return _lvgl.anim_get(var, exec_cb)


def anim_get_timer() -> "timer_t":
    return _lvgl.anim_get_timer()


def anim_count_running() -> _lvgl.uint16_t:
    return _lvgl.anim_count_running()


def anim_speed_to_time(speed: _lvgl.uint32_t, start: _lvgl.int32_t, end: _lvgl.int32_t) -> _lvgl.uint32_t:
    return _lvgl.anim_speed_to_time(speed, start, end)


def anim_refr_now() -> None:
    return _lvgl.anim_refr_now()


def snprintf_builtin(buffer: _lvgl.char, count: _lvgl.size_t, format: _lvgl.char, *args) -> _lvgl.int_:
    return _lvgl.snprintf_builtin(buffer, count, format, *args)


def vsnprintf_builtin(buffer: _lvgl.char, count: _lvgl.size_t, format: _lvgl.char, va: "va_list") -> _lvgl.int_:
    return _lvgl.vsnprintf_builtin(buffer, count, format, va)


def _area_set_pos(area_p: "area_t", x: _lvgl.coord_t, y: _lvgl.coord_t) -> None:
    return _lvgl._area_set_pos(area_p, x, y)


def _area_intersect(res_p: "area_t", a1_p: "area_t", a2_p: "area_t") -> _lvgl._Bool:
    return _lvgl._area_intersect(res_p, a1_p, a2_p)


def _area_join(a_res_p: "area_t", a1_p: "area_t", a2_p: "area_t") -> None:
    return _lvgl._area_join(a_res_p, a1_p, a2_p)


def _area_is_point_on(a_p: "area_t", p_p: _lvgl.point_t, radius: _lvgl.coord_t) -> _lvgl._Bool:
    return _lvgl._area_is_point_on(a_p, p_p, radius)


def _area_is_on(a1_p: "area_t", a2_p: "area_t") -> _lvgl._Bool:
    return _lvgl._area_is_on(a1_p, a2_p)


def _area_is_in(ain_p: "area_t", aholder_p: "area_t", radius: _lvgl.coord_t) -> _lvgl._Bool:
    return _lvgl._area_is_in(ain_p, aholder_p, radius)


def _area_is_out(aout_p: "area_t", aholder_p: "area_t", radius: _lvgl.coord_t) -> _lvgl._Bool:
    return _lvgl._area_is_out(aout_p, aholder_p, radius)


def _area_is_equal(a: "area_t", b: "area_t") -> _lvgl._Bool:
    return _lvgl._area_is_equal(a, b)


def pct(x: _lvgl.coord_t) -> _lvgl.coord_t:
    return _lvgl.pct(x)


def font_default() -> "font_t":
    return _lvgl.font_default()


def color_to_native(src_buf: _lvgl.uint8_t, src_cf: _lvgl.color_format_t, c_out: "color_t", a_out: _lvgl.opa_t, alpha_color: "color_t", px_cnt: _lvgl.uint32_t) -> None:
    return _lvgl.color_to_native(src_buf, src_cf, c_out, a_out, alpha_color, px_cnt)


def color_from_native_alpha(src_buf: _lvgl.uint8_t, dest_buf: _lvgl.uint8_t, dest_cf: _lvgl.color_format_t, px_cnt: _lvgl.uint32_t) -> None:
    return _lvgl.color_from_native_alpha(src_buf, dest_buf, dest_cf, px_cnt)


def color_format_get_size(src_cf: _lvgl.color_format_t) -> _lvgl.uint8_t:
    return _lvgl.color_format_get_size(src_cf)


def color_format_has_alpha(src_cf: _lvgl.color_format_t) -> _lvgl._Bool:
    return _lvgl.color_format_has_alpha(src_cf)


def color8_from_buf(buf: _lvgl.uint8_t) -> "color8_t":
    return _lvgl.color8_from_buf(buf)


def color16_from_buf(buf: _lvgl.uint8_t) -> "color16_t":
    return _lvgl.color16_from_buf(buf)


def color24_from_buf(buf: _lvgl.uint8_t) -> "color24_t":
    return _lvgl.color24_from_buf(buf)


def color32_from_buf(buf: _lvgl.uint8_t) -> "color32_t":
    return _lvgl.color32_from_buf(buf)


def color_from_buf(buf: _lvgl.uint8_t) -> "color_t":
    return _lvgl.color_from_buf(buf)


def color_mix_premult(premult_c1: _lvgl.uint16_t, c2: "color_t", mix: _lvgl.uint8_t) -> "color_t":
    return _lvgl.color_mix_premult(premult_c1, c2, mix)


def color_make(r: _lvgl.uint8_t, g: _lvgl.uint8_t, b: _lvgl.uint8_t) -> "color_t":
    return _lvgl.color_make(r, g, b)


def color_hex(c: _lvgl.uint32_t) -> "color_t":
    return _lvgl.color_hex(c)


def color_hex3(c: _lvgl.uint32_t) -> "color_t":
    return _lvgl.color_hex3(c)


def color_hsv_to_rgb(h: _lvgl.uint16_t, s: _lvgl.uint8_t, v: _lvgl.uint8_t) -> "color_t":
    return _lvgl.color_hsv_to_rgb(h, s, v)


def color_rgb_to_hsv(r8: _lvgl.uint8_t, g8: _lvgl.uint8_t, b8: _lvgl.uint8_t) -> "color_hsv_t":
    return _lvgl.color_rgb_to_hsv(r8, g8, b8)


def color_chroma_key() -> "color_t":
    return _lvgl.color_chroma_key()


def palette_main(p: _lvgl.palette_t) -> "color_t":
    return _lvgl.palette_main(p)


def color_white() -> "color_t":
    return _lvgl.color_white()


def color_black() -> "color_t":
    return _lvgl.color_black()


def palette_lighten(p: _lvgl.palette_t, lvl: _lvgl.uint8_t) -> "color_t":
    return _lvgl.palette_lighten(p, lvl)


def palette_darken(p: _lvgl.palette_t, lvl: _lvgl.uint8_t) -> "color_t":
    return _lvgl.palette_darken(p, lvl)


def txt_get_size(size_res: _lvgl.point_t, text: _lvgl.char, font: "font_t", letter_space: _lvgl.coord_t, line_space: _lvgl.coord_t, max_width: _lvgl.coord_t, flag: _lvgl.text_flag_t) -> None:
    return _lvgl.txt_get_size(size_res, text, font, letter_space, line_space, max_width, flag)


def _txt_get_next_line(txt: _lvgl.char, font: "font_t", letter_space: _lvgl.coord_t, max_width: _lvgl.coord_t, used_width: _lvgl.coord_t, flag: _lvgl.text_flag_t) -> _lvgl.uint32_t:
    return _lvgl._txt_get_next_line(txt, font, letter_space, max_width, used_width, flag)


def txt_get_width(txt: _lvgl.char, length: _lvgl.uint32_t, font: "font_t", letter_space: _lvgl.coord_t, flag: _lvgl.text_flag_t) -> _lvgl.coord_t:
    return _lvgl.txt_get_width(txt, length, font, letter_space, flag)


def _txt_is_cmd(state: _lvgl.text_cmd_state_t, c: _lvgl.uint32_t) -> _lvgl._Bool:
    return _lvgl._txt_is_cmd(state, c)


def _txt_ins(txt_buf: _lvgl.char, pos: _lvgl.uint32_t, ins_txt: _lvgl.char) -> None:
    return _lvgl._txt_ins(txt_buf, pos, ins_txt)


def _txt_cut(txt: _lvgl.char, pos: _lvgl.uint32_t, len: _lvgl.uint32_t) -> None:
    return _lvgl._txt_cut(txt, pos, len)


def _txt_set_text_vfmt(fmt: _lvgl.char, ap: "va_list") -> _lvgl.char:
    return _lvgl._txt_set_text_vfmt(fmt, ap)


def _txt_encoded_letter_next_2(txt: _lvgl.char, letter: _lvgl.uint32_t, letter_next: _lvgl.uint32_t, ofs: _lvgl.uint32_t) -> None:
    return _lvgl._txt_encoded_letter_next_2(txt, letter, letter_next, ofs)


def _txt_is_break_char(letter: _lvgl.uint32_t) -> _lvgl._Bool:
    return _lvgl._txt_is_break_char(letter)


def _txt_is_a_word(letter: _lvgl.uint32_t) -> _lvgl._Bool:
    return _lvgl._txt_is_a_word(letter)


def _txt_encoded_size() -> _lvgl.uint8_t:
    return _lvgl._txt_encoded_size()


def _txt_unicode_to_encoded() -> _lvgl.uint32_t:
    return _lvgl._txt_unicode_to_encoded()


def _txt_encoded_conv_wc(c: _lvgl.uint32_t) -> _lvgl.uint32_t:
    return _lvgl._txt_encoded_conv_wc(c)


def _txt_encoded_next() -> _lvgl.uint32_t:
    return _lvgl._txt_encoded_next()


def _txt_encoded_prev() -> _lvgl.uint32_t:
    return _lvgl._txt_encoded_prev()


def _txt_encoded_get_byte_id() -> _lvgl.uint32_t:
    return _lvgl._txt_encoded_get_byte_id()


def _txt_encoded_get_char_id() -> _lvgl.uint32_t:
    return _lvgl._txt_encoded_get_char_id()


def _txt_get_encoded_length() -> _lvgl.uint32_t:
    return _lvgl._txt_get_encoded_length()


def _bidi_process(str_in: _lvgl.char, str_out: _lvgl.char, base_dir: _lvgl.base_dir_t) -> None:
    return _lvgl._bidi_process(str_in, str_out, base_dir)


def _bidi_detect_base_dir(txt: _lvgl.char) -> _lvgl.base_dir_t:
    return _lvgl._bidi_detect_base_dir(txt)


def _bidi_get_logical_pos(str_in: _lvgl.char, bidi_txt: _lvgl.char, len: _lvgl.uint32_t, base_dir: _lvgl.base_dir_t, visual_pos: _lvgl.uint32_t, is_rtl: _lvgl._Bool) -> _lvgl.uint16_t:
    return _lvgl._bidi_get_logical_pos(str_in, bidi_txt, len, base_dir, visual_pos, is_rtl)


def _bidi_get_visual_pos(str_in: _lvgl.char, bidi_txt: _lvgl.char, len: _lvgl.uint16_t, base_dir: _lvgl.base_dir_t, logical_pos: _lvgl.uint32_t, is_rtl: _lvgl._Bool) -> _lvgl.uint16_t:
    return _lvgl._bidi_get_visual_pos(str_in, bidi_txt, len, base_dir, logical_pos, is_rtl)


def _bidi_process_paragraph(str_in: _lvgl.char, str_out: _lvgl.char, len: _lvgl.uint32_t, base_dir: _lvgl.base_dir_t, pos_conv_out: _lvgl.uint16_t, pos_conv_len: _lvgl.uint16_t) -> None:
    return _lvgl._bidi_process_paragraph(str_in, str_out, len, base_dir, pos_conv_out, pos_conv_len)


def bidi_calculate_align(align: _lvgl.text_align_t, base_dir: _lvgl.base_dir_t, txt: _lvgl.char) -> None:
    return _lvgl.bidi_calculate_align(align, base_dir, txt)


def style_register_prop(flag: _lvgl.uint8_t) -> _lvgl.style_prop_t:
    return _lvgl.style_register_prop(flag)


def style_get_num_custom_props() -> _lvgl.style_prop_t:
    return _lvgl.style_get_num_custom_props()


def style_prop_get_default(prop: _lvgl.style_prop_t) -> "style_value_t":
    return _lvgl.style_prop_get_default(prop)


def _style_get_prop_group(prop: _lvgl.style_prop_t) -> _lvgl.uint8_t:
    return _lvgl._style_get_prop_group(prop)


def _style_prop_lookup_flags(prop: _lvgl.style_prop_t) -> _lvgl.uint8_t:
    return _lvgl._style_prop_lookup_flags(prop)


def style_prop_has_flag(prop: _lvgl.style_prop_t, flag: _lvgl.uint8_t) -> _lvgl._Bool:
    return _lvgl.style_prop_has_flag(prop, flag)


def _event_push(e: "event_t") -> None:
    return _lvgl._event_push(e)


def _event_pop(e: "event_t") -> None:
    return _lvgl._event_pop(e)


def event_register_id() -> _lvgl.uint32_t:
    return _lvgl.event_register_id()


def _event_mark_deleted(target: None) -> None:
    return _lvgl._event_mark_deleted(target)


def disp_get_default() -> "disp_t":
    return _lvgl.disp_get_default()


def disp_load_scr(scr: "obj") -> None:
    return _lvgl.disp_load_scr(scr)


def scr_load_anim(scr: "obj", anim_type: _lvgl.scr_load_anim_t, time: _lvgl.uint32_t, delay: _lvgl.uint32_t, auto_del: _lvgl._Bool) -> None:
    return _lvgl.scr_load_anim(scr, anim_type, time, delay, auto_del)


def scr_act() -> "obj":
    return _lvgl.scr_act()


def layer_top() -> "obj":
    return _lvgl.layer_top()


def layer_sys() -> "obj":
    return _lvgl.layer_sys()


def layer_bottom() -> "obj":
    return _lvgl.layer_bottom()


def scr_load(scr: "obj") -> None:
    return _lvgl.scr_load(scr)


def _disp_get_refr_timer(disp: "disp_t") -> "timer_t":
    return _lvgl._disp_get_refr_timer(disp)


def dpx(n: _lvgl.coord_t) -> _lvgl.coord_t:
    return _lvgl.dpx(n)


def obj_del_anim_ready_cb(a: "anim_t") -> None:
    return _lvgl.obj_del_anim_ready_cb(a)


def layout_register(cb: "layout_update_cb_t", user_data: Any) -> _lvgl.uint32_t:
    return _lvgl.layout_register(cb, user_data)


def clamp_width(width: _lvgl.coord_t, min_width: _lvgl.coord_t, max_width: _lvgl.coord_t, ref_width: _lvgl.coord_t) -> _lvgl.coord_t:
    return _lvgl.clamp_width(width, min_width, max_width, ref_width)


def clamp_height(height: _lvgl.coord_t, min_height: _lvgl.coord_t, max_height: _lvgl.coord_t, ref_height: _lvgl.coord_t) -> _lvgl.coord_t:
    return _lvgl.clamp_height(height, min_height, max_height, ref_height)


def _obj_scroll_by_raw(obj: "obj", x: _lvgl.coord_t, y: _lvgl.coord_t) -> _lvgl.res_t:
    return _lvgl._obj_scroll_by_raw(obj, x, y)


def _obj_style_init() -> None:
    return _lvgl._obj_style_init()


def obj_report_style_change(style: "style_t") -> None:
    return _lvgl.obj_report_style_change(style)


def obj_enable_style_refresh(en: _lvgl._Bool) -> None:
    return _lvgl.obj_enable_style_refresh(en)


def _obj_style_apply_color_filter(obj: "obj", part: _lvgl.uint32_t, v: "style_value_t") -> "style_value_t":
    return _lvgl._obj_style_apply_color_filter(obj, part, v)


def _obj_style_create_transition(obj: "obj", part: _lvgl.part_t, prev_state: _lvgl.state_t, new_state: _lvgl.state_t, tr: "obj_style_transition_dsc_t") -> None:
    return _lvgl._obj_style_create_transition(obj, part, prev_state, new_state, tr)


def _obj_style_state_compare(obj: "obj", state1: _lvgl.state_t, state2: _lvgl.state_t) -> "style_state_cmp_t":
    return _lvgl._obj_style_state_compare(obj, state1, state2)


def obj_style_get_selector_state(selector: _lvgl.style_selector_t) -> _lvgl.state_t:
    return _lvgl.obj_style_get_selector_state(selector)


def obj_style_get_selector_part(selector: _lvgl.style_selector_t) -> _lvgl.part_t:
    return _lvgl.obj_style_get_selector_part(selector)


def _img_buf_get_transformed_area(res: "area_t", w: _lvgl.coord_t, h: _lvgl.coord_t, angle: _lvgl.int16_t, zoom: _lvgl.uint16_t, pivot: _lvgl.point_t) -> None:
    return _lvgl._img_buf_get_transformed_area(res, w, h, angle, zoom, pivot)


def _fs_init() -> None:
    return _lvgl._fs_init()


def fs_get_drv(letter: _lvgl.char) -> "fs_drv_t":
    return _lvgl.fs_get_drv(letter)


def fs_is_ready(letter: _lvgl.char) -> _lvgl._Bool:
    return _lvgl.fs_is_ready(letter)


def fs_get_letters(buf: _lvgl.char) -> _lvgl.char:
    return _lvgl.fs_get_letters(buf)


def fs_get_ext(fn: _lvgl.char) -> _lvgl.char:
    return _lvgl.fs_get_ext(fn)


def fs_up(path: _lvgl.char) -> _lvgl.char:
    return _lvgl.fs_up(path)


def fs_get_last(path: _lvgl.char) -> _lvgl.char:
    return _lvgl.fs_get_last(path)


def _img_decoder_init() -> None:
    return _lvgl._img_decoder_init()


def img_decoder_get_info(src: None, header: "img_header_t") -> _lvgl.res_t:
    return _lvgl.img_decoder_get_info(src, header)


def _img_cache_open(src: None, color: "color_t", frame_id: _lvgl.int32_t) -> "img_cache_entry_t":
    return _lvgl._img_cache_open(src, color, frame_id)


def img_cache_set_size(new_entry_cnt: _lvgl.uint16_t) -> None:
    return _lvgl.img_cache_set_size(new_entry_cnt)


def img_cache_invalidate_src(src: None) -> None:
    return _lvgl.img_cache_invalidate_src(src)


def gradient_calculate(dsc: "grad_dsc_t", range: _lvgl.coord_t, frac: _lvgl.coord_t) -> "grad_color_t":
    return _lvgl.gradient_calculate(dsc, range, frac)


def gradient_set_cache_size(max_bytes: _lvgl.size_t) -> None:
    return _lvgl.gradient_set_cache_size(max_bytes)


def gradient_free_cache() -> None:
    return _lvgl.gradient_free_cache()


def gradient_get(gradient: "grad_dsc_t", w: _lvgl.coord_t, h: _lvgl.coord_t) -> "grad_t":
    return _lvgl.gradient_get(gradient, w, h)


def gradient_cleanup(grad: "grad_t") -> None:
    return _lvgl.gradient_cleanup(grad)


def img_src_get_type(src: None) -> _lvgl.img_src_t:
    return _lvgl.img_src_get_type(src)


def draw_arc_get_area(x: _lvgl.coord_t, y: _lvgl.coord_t, radius: _lvgl.uint16_t, start_angle: _lvgl.uint16_t, end_angle: _lvgl.uint16_t, w: _lvgl.coord_t, rounded: _lvgl._Bool, area: "area_t") -> None:
    return _lvgl.draw_arc_get_area(x, y, radius, start_angle, end_angle, w, rounded, area)


def draw_mask_add(param: None, custom_id: None) -> _lvgl.int16_t:
    return _lvgl.draw_mask_add(param, custom_id)


def draw_mask_apply(mask_buf: _lvgl.opa_t, abs_x: _lvgl.coord_t, abs_y: _lvgl.coord_t, len: _lvgl.coord_t) -> _lvgl.draw_mask_res_t:
    return _lvgl.draw_mask_apply(mask_buf, abs_x, abs_y, len)


def draw_mask_apply_ids(mask_buf: _lvgl.opa_t, abs_x: _lvgl.coord_t, abs_y: _lvgl.coord_t, len: _lvgl.coord_t, ids: _lvgl.int16_t, ids_count: _lvgl.int16_t) -> _lvgl.draw_mask_res_t:
    return _lvgl.draw_mask_apply_ids(mask_buf, abs_x, abs_y, len, ids, ids_count)


def draw_mask_remove_id(id: _lvgl.int16_t) -> Any:
    return _lvgl.draw_mask_remove_id(id)


def draw_mask_remove_custom(custom_id: None) -> Any:
    return _lvgl.draw_mask_remove_custom(custom_id)


def draw_mask_free_param(p: None) -> None:
    return _lvgl.draw_mask_free_param(p)


def _draw_mask_cleanup() -> None:
    return _lvgl._draw_mask_cleanup()


def draw_mask_get_cnt() -> _lvgl.uint8_t:
    return _lvgl.draw_mask_get_cnt()


def draw_mask_is_any(a: "area_t") -> _lvgl._Bool:
    return _lvgl.draw_mask_is_any(a)


def draw_init() -> None:
    return _lvgl.draw_init()


def _obj_get_ext_draw_size(obj: "obj") -> _lvgl.coord_t:
    return _lvgl._obj_get_ext_draw_size(obj)


def _obj_get_layer_type(obj: "obj") -> _lvgl.layer_type_t:
    return _lvgl._obj_get_layer_type(obj)


def _obj_destruct(obj: "obj") -> None:
    return _lvgl._obj_destruct(obj)


def _ll_init(ll_p: "ll_t", node_size: _lvgl.uint32_t) -> None:
    return _lvgl._ll_init(ll_p, node_size)


def _ll_ins_head(ll_p: "ll_t") -> Any:
    return _lvgl._ll_ins_head(ll_p)


def _ll_ins_prev(ll_p: "ll_t", n_act: None) -> Any:
    return _lvgl._ll_ins_prev(ll_p, n_act)


def _ll_ins_tail(ll_p: "ll_t") -> Any:
    return _lvgl._ll_ins_tail(ll_p)


def _ll_remove(ll_p: "ll_t", node_p: None) -> None:
    return _lvgl._ll_remove(ll_p, node_p)


def _ll_clear(ll_p: "ll_t") -> None:
    return _lvgl._ll_clear(ll_p)


def _ll_chg_list(ll_ori_p: "ll_t", ll_new_p: "ll_t", node: None, head: _lvgl._Bool) -> None:
    return _lvgl._ll_chg_list(ll_ori_p, ll_new_p, node, head)


def _ll_get_head(ll_p: "ll_t") -> Any:
    return _lvgl._ll_get_head(ll_p)


def _ll_get_tail(ll_p: "ll_t") -> Any:
    return _lvgl._ll_get_tail(ll_p)


def _ll_get_next(ll_p: "ll_t", n_act: None) -> Any:
    return _lvgl._ll_get_next(ll_p, n_act)


def _ll_get_prev(ll_p: "ll_t", n_act: None) -> Any:
    return _lvgl._ll_get_prev(ll_p, n_act)


def _ll_get_len(ll_p: "ll_t") -> _lvgl.uint32_t:
    return _lvgl._ll_get_len(ll_p)


def _ll_move_before(ll_p: "ll_t", n_act: None, n_after: None) -> None:
    return _lvgl._ll_move_before(ll_p, n_act, n_after)


def _ll_is_empty(ll_p: "ll_t") -> _lvgl._Bool:
    return _lvgl._ll_is_empty(ll_p)


def _group_init() -> None:
    return _lvgl._group_init()


def group_get_default() -> "group_t":
    return _lvgl.group_get_default()


def group_swap_obj(obj1: "obj", obj2: "obj") -> None:
    return _lvgl.group_swap_obj(obj1, obj2)


def group_remove_obj(obj: "obj") -> None:
    return _lvgl.group_remove_obj(obj)


def group_focus_obj(obj: "obj") -> None:
    return _lvgl.group_focus_obj(obj)


def indev_create() -> "indev_t":
    return _lvgl.indev_create()


def _indev_read(indev: "indev_t", data: "indev_data_t") -> None:
    return _lvgl._indev_read(indev, data)


def indev_read_timer_cb(timer: "timer_t") -> None:
    return _lvgl.indev_read_timer_cb(timer)


def indev_get_act() -> "indev_t":
    return _lvgl.indev_get_act()


def indev_get_obj_act() -> "obj":
    return _lvgl.indev_get_obj_act()


def indev_search_obj(obj: "obj", point: _lvgl.point_t) -> "obj":
    return _lvgl.indev_search_obj(obj, point)


def init() -> None:
    return _lvgl.init()


def deinit() -> None:
    return _lvgl.deinit()


def is_initialized() -> _lvgl._Bool:
    return _lvgl.is_initialized()


def _refr_init() -> None:
    return _lvgl._refr_init()


def refr_now(disp: "disp_t") -> None:
    return _lvgl.refr_now(disp)


def obj_redraw(draw_ctx: "draw_ctx_t", obj: "obj") -> None:
    return _lvgl.obj_redraw(draw_ctx, obj)


def _inv_area(disp: "disp_t", area_p: "area_t") -> None:
    return _lvgl._inv_area(disp, area_p)


def _refr_get_disp_refreshing() -> "disp_t":
    return _lvgl._refr_get_disp_refreshing()


def _disp_refr_timer(timer: "timer_t") -> None:
    return _lvgl._disp_refr_timer(timer)


def theme_get_from_obj(obj: "obj") -> "theme_t":
    return _lvgl.theme_get_from_obj(obj)


def theme_apply(obj: "obj") -> None:
    return _lvgl.theme_apply(obj)


def theme_get_font_small(obj: "obj") -> "font_t":
    return _lvgl.theme_get_font_small(obj)


def theme_get_font_normal(obj: "obj") -> "font_t":
    return _lvgl.theme_get_font_normal(obj)


def theme_get_font_large(obj: "obj") -> "font_t":
    return _lvgl.theme_get_font_large(obj)


def theme_get_color_primary(obj: "obj") -> "color_t":
    return _lvgl.theme_get_color_primary(obj)


def theme_get_color_secondary(obj: "obj") -> "color_t":
    return _lvgl.theme_get_color_secondary(obj)


def font_load(fontName: _lvgl.char) -> "font_t":
    return _lvgl.font_load(fontName)


def _font_clean_up_fmt_txt() -> None:
    return _lvgl._font_clean_up_fmt_txt()


def keyboard_def_event_cb(e: "event_t") -> None:
    return _lvgl.keyboard_def_event_cb(e)


def snapshot_take(obj: "obj", cf: _lvgl.color_format_t) -> "img_dsc_t":
    return _lvgl.snapshot_take(obj, cf)


def snapshot_free(dsc: "img_dsc_t") -> None:
    return _lvgl.snapshot_free(dsc)


def snapshot_buf_size_needed(obj: "obj", cf: _lvgl.color_format_t) -> _lvgl.uint32_t:
    return _lvgl.snapshot_buf_size_needed(obj, cf)


def snapshot_take_to_buf(obj: "obj", cf: _lvgl.color_format_t, dsc: "img_dsc_t", buf: None, buff_size: _lvgl.uint32_t) -> _lvgl.res_t:
    return _lvgl.snapshot_take_to_buf(obj, cf, dsc, buf, buff_size)


def gridnav_add(obj: "obj", ctrl: _lvgl.gridnav_ctrl_t) -> None:
    return _lvgl.gridnav_add(obj, ctrl)


def gridnav_remove(obj: "obj") -> None:
    return _lvgl.gridnav_remove(obj)


def gridnav_set_focused(cont: "obj", to_focus: "obj", anim_en: _lvgl.anim_enable_t) -> None:
    return _lvgl.gridnav_set_focused(cont, to_focus, anim_en)


def imgfont_destroy(font: "font_t") -> None:
    return _lvgl.imgfont_destroy(font)


def msg_init() -> None:
    return _lvgl.msg_init()


def msg_subscribe(msg_id: _lvgl.msg_id_t, cb: "msg_subscribe_cb_t", user_data: Any) -> Any:
    return _lvgl.msg_subscribe(msg_id, cb, user_data)


def msg_subscribe_obj(msg_id: _lvgl.msg_id_t, obj: "obj", user_data: Any) -> Any:
    return _lvgl.msg_subscribe_obj(msg_id, obj, user_data)


def msg_unsubscribe(s: None) -> None:
    return _lvgl.msg_unsubscribe(s)


def msg_send(msg_id: _lvgl.msg_id_t, payload: None) -> None:
    return _lvgl.msg_send(msg_id, payload)


def msg_update_value(v: None) -> None:
    return _lvgl.msg_update_value(v)


def bmp_init() -> None:
    return _lvgl.bmp_init()


def png_init() -> None:
    return _lvgl.png_init()


def gd_open_gif_file(fname: _lvgl.char) -> "gd_GIF":
    return _lvgl.gd_open_gif_file(fname)


def gd_open_gif_data(data: None) -> "gd_GIF":
    return _lvgl.gd_open_gif_data(data)


def split_jpeg_init() -> None:
    return _lvgl.split_jpeg_init()


def tiny_ttf_create_file(path: _lvgl.char, line_height: _lvgl.coord_t) -> "font_t":
    return _lvgl.tiny_ttf_create_file(path, line_height)


def tiny_ttf_create_file_ex(path: _lvgl.char, line_height: _lvgl.coord_t, cache_size: _lvgl.size_t) -> "font_t":
    return _lvgl.tiny_ttf_create_file_ex(path, line_height, cache_size)


def tiny_ttf_create_data(data: None, data_size: _lvgl.size_t, line_height: _lvgl.coord_t) -> "font_t":
    return _lvgl.tiny_ttf_create_data(data, data_size, line_height)


def tiny_ttf_create_data_ex(data: None, data_size: _lvgl.size_t, line_height: _lvgl.coord_t, cache_size: _lvgl.size_t) -> "font_t":
    return _lvgl.tiny_ttf_create_data_ex(data, data_size, line_height, cache_size)


def tiny_ttf_set_size(font: "font_t", line_height: _lvgl.coord_t) -> None:
    return _lvgl.tiny_ttf_set_size(font, line_height)


def tiny_ttf_destroy(font: "font_t") -> None:
    return _lvgl.tiny_ttf_destroy(font)


def flex_init() -> None:
    return _lvgl.flex_init()


def grid_init() -> None:
    return _lvgl.grid_init()


def grid_fr(x: _lvgl.uint8_t) -> _lvgl.coord_t:
    return _lvgl.grid_fr(x)


def theme_default_init(disp: "disp_t", color_primary: "color_t", color_secondary: "color_t", dark: _lvgl._Bool, font: "font_t") -> "theme_t":
    return _lvgl.theme_default_init(disp, color_primary, color_secondary, dark, font)


def theme_default_get() -> "theme_t":
    return _lvgl.theme_default_get()


def theme_default_is_inited() -> _lvgl._Bool:
    return _lvgl.theme_default_is_inited()


def theme_basic_init(disp: "disp_t") -> "theme_t":
    return _lvgl.theme_basic_init(disp)


def theme_basic_is_inited() -> _lvgl._Bool:
    return _lvgl.theme_basic_is_inited()


def task_handler() -> _lvgl.uint32_t:
    return _lvgl.task_handler()


def sdl_window_create(hor_res: _lvgl.coord_t, ver_res: _lvgl.coord_t) -> "disp_t":
    return _lvgl.sdl_window_create(hor_res, ver_res)


def sdl_window_set_zoom(disp: "disp_t", zoom: _lvgl.uint8_t) -> None:
    return _lvgl.sdl_window_set_zoom(disp, zoom)


def sdl_window_get_zoom(disp: "disp_t") -> _lvgl.uint8_t:
    return _lvgl.sdl_window_get_zoom(disp)


def _sdl_get_disp_from_win_id(win_id: _lvgl.uint32_t) -> "disp_t":
    return _lvgl._sdl_get_disp_from_win_id(win_id)


def sdl_window_set_title(disp: "disp_t", title: _lvgl.char) -> None:
    return _lvgl.sdl_window_set_title(disp, title)


def sdl_mouse_create() -> "indev_t":
    return _lvgl.sdl_mouse_create()


def sdl_mousewheel_create() -> "indev_t":
    return _lvgl.sdl_mousewheel_create()


def sdl_keyboard_create() -> "indev_t":
    return _lvgl.sdl_keyboard_create()


def version_major() -> _lvgl.int_:
    return _lvgl.version_major()


def version_minor() -> _lvgl.int_:
    return _lvgl.version_minor()


def version_patch() -> _lvgl.int_:
    return _lvgl.version_patch()


def version_info() -> _lvgl.char:
    return _lvgl.version_info()


def demo_benchmark(mode: _lvgl.demo_benchmark_mode_t) -> None:
    return _lvgl.demo_benchmark(mode)


def demo_benchmark_run_scene(mode: _lvgl.demo_benchmark_mode_t, scene_no: _lvgl.uint16_t) -> None:
    return _lvgl.demo_benchmark_run_scene(mode, scene_no)


def timer_create(timer_xcb: "timer_cb_t", period: _lvgl.uint32_t, user_data: Any) -> "timer_t":
    return _lvgl.timer_create(timer_xcb, period, user_data)


def disp_create(hor_res: _lvgl.coord_t, ver_res: _lvgl.coord_t) -> "disp_t":
    return _lvgl.disp_create(hor_res, ver_res)


def imgfont_create(height: _lvgl.uint16_t, path_cb: "imgfont_get_path_cb_t", user_data: Any) -> "font_t":
    return _lvgl.imgfont_create(height, path_cb, user_data)



class gd_GIF(_lvgl.gd_GIF):

    def plain_text_xcb_t(self, tx: _lvgl.uint16_t, ty: _lvgl.uint16_t, tw: _lvgl.uint16_t, th: _lvgl.uint16_t, cw: _lvgl.uint8_t, ch: _lvgl.uint8_t, fg: _lvgl.uint8_t, bg: _lvgl.uint8_t) -> None:
        return _lvgl.gd_GIF_plain_text_xcb_t(self, tx, ty, tw, th, cw, ch, fg, bg)

    def comment_xcb_t(self) -> None:
        return _lvgl.gd_GIF_comment_xcb_t(self)

    def application_xcb_t(self, id: List[_lvgl.char], auth: List[_lvgl.char]) -> None:
        return _lvgl.gd_GIF_application_xcb_t(self, id, auth)

    def render_frame(self, buffer: _lvgl.uint8_t) -> None:
        return _lvgl.gd_render_frame(self, buffer)

    def get_frame(self) -> _lvgl.int_:
        return _lvgl.gd_get_frame(self)

    def rewind(self) -> None:
        return _lvgl.gd_rewind(self)

    def close_gif(self) -> None:
        return _lvgl.gd_close_gif(self)


class tick_dsc_t(_lvgl.tick_dsc_t):

    def set_cb(self, tick_cb: "tick_cb_t", user_data: Any) -> None:
        return _lvgl.tick_set_cb(self, tick_cb, user_data)


class timer_t(_lvgl.timer_t):

    def _del(self) -> None:
        return _lvgl.timer_del(self)

    def pause(self) -> None:
        return _lvgl.timer_pause(self)

    def resume(self) -> None:
        return _lvgl.timer_resume(self)

    def set_cb(self, timer_cb: "timer_cb_t") -> None:
        return _lvgl.timer_set_cb(self, timer_cb)

    def set_period(self, period: _lvgl.uint32_t) -> None:
        return _lvgl.timer_set_period(self, period)

    def ready(self) -> None:
        return _lvgl.timer_ready(self)

    def set_repeat_count(self, repeat_count: _lvgl.int32_t) -> None:
        return _lvgl.timer_set_repeat_count(self, repeat_count)

    def reset(self) -> None:
        return _lvgl.timer_reset(self)

    def get_next(self) -> "timer_t":
        return _lvgl.timer_get_next(self)

    def get_user_data(self) -> Any:
        return _lvgl.timer_get_user_data(self)


class mem_monitor_t(_lvgl.mem_monitor_t):

    def mem_monitor(self) -> None:
        return _lvgl.mem_monitor(self)


class anim_t(_lvgl.anim_t):

    def init(self) -> None:
        return _lvgl.anim_init(self)

    def set_var(self, var: _lvgl.void) -> None:
        return _lvgl.anim_set_var(self, var)

    def set_exec_cb(self, exec_cb: "anim_exec_xcb_t") -> None:
        return _lvgl.anim_set_exec_cb(self, exec_cb)

    def set_time(self, duration: _lvgl.uint32_t) -> None:
        return _lvgl.anim_set_time(self, duration)

    def set_delay(self, delay: _lvgl.uint32_t) -> None:
        return _lvgl.anim_set_delay(self, delay)

    def set_values(self, start: _lvgl.int32_t, end: _lvgl.int32_t) -> None:
        return _lvgl.anim_set_values(self, start, end)

    def set_custom_exec_cb(self, exec_cb: "anim_custom_exec_cb_t") -> None:
        return _lvgl.anim_set_custom_exec_cb(self, exec_cb)

    def set_path_cb(self, path_cb: "anim_path_cb_t") -> None:
        return _lvgl.anim_set_path_cb(self, path_cb)

    def set_start_cb(self, start_cb: "anim_start_cb_t") -> None:
        return _lvgl.anim_set_start_cb(self, start_cb)

    def set_get_value_cb(self, get_value_cb: "anim_get_value_cb_t") -> None:
        return _lvgl.anim_set_get_value_cb(self, get_value_cb)

    def set_ready_cb(self, ready_cb: "anim_ready_cb_t") -> None:
        return _lvgl.anim_set_ready_cb(self, ready_cb)

    def set_deleted_cb(self, deleted_cb: "anim_deleted_cb_t") -> None:
        return _lvgl.anim_set_deleted_cb(self, deleted_cb)

    def set_playback_time(self, time: _lvgl.uint32_t) -> None:
        return _lvgl.anim_set_playback_time(self, time)

    def set_playback_delay(self, delay: _lvgl.uint32_t) -> None:
        return _lvgl.anim_set_playback_delay(self, delay)

    def set_repeat_count(self, cnt: _lvgl.uint16_t) -> None:
        return _lvgl.anim_set_repeat_count(self, cnt)

    def set_repeat_delay(self, delay: _lvgl.uint32_t) -> None:
        return _lvgl.anim_set_repeat_delay(self, delay)

    def set_early_apply(self, en: _lvgl._Bool) -> None:
        return _lvgl.anim_set_early_apply(self, en)

    def set_user_data(self, user_data: Any) -> None:
        return _lvgl.anim_set_user_data(self, user_data)

    def start(self) -> "anim_t":
        return _lvgl.anim_start(self)

    def get_delay(self) -> _lvgl.uint32_t:
        return _lvgl.anim_get_delay(self)

    def get_playtime(self) -> _lvgl.uint32_t:
        return _lvgl.anim_get_playtime(self)

    def get_time(self) -> _lvgl.uint32_t:
        return _lvgl.anim_get_time(self)

    def get_repeat_count(self) -> _lvgl.uint16_t:
        return _lvgl.anim_get_repeat_count(self)

    def get_user_data(self) -> Any:
        return _lvgl.anim_get_user_data(self)

    def custom_del(self, exec_cb: "anim_custom_exec_cb_t") -> _lvgl._Bool:
        return _lvgl.anim_custom_del(self, exec_cb)

    def custom_get(self, exec_cb: "anim_custom_exec_cb_t") -> "anim_t":
        return _lvgl.anim_custom_get(self, exec_cb)

    def path_linear(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_linear(self)

    def path_ease_in(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_ease_in(self)

    def path_ease_out(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_ease_out(self)

    def path_ease_in_out(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_ease_in_out(self)

    def path_overshoot(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_overshoot(self)

    def path_bounce(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_bounce(self)

    def path_step(self) -> _lvgl.int32_t:
        return _lvgl.anim_path_step(self)


class anim_timeline_t(_lvgl.anim_timeline_t):

    def _del(self) -> None:
        return _lvgl.anim_timeline_del(self)

    def add(self, start_time: _lvgl.uint32_t, a: "anim_t") -> None:
        return _lvgl.anim_timeline_add(self, start_time, a)

    def start(self) -> _lvgl.uint32_t:
        return _lvgl.anim_timeline_start(self)

    def stop(self) -> None:
        return _lvgl.anim_timeline_stop(self)

    def set_reverse(self, reverse: _lvgl._Bool) -> None:
        return _lvgl.anim_timeline_set_reverse(self, reverse)

    def set_progress(self, progress: _lvgl.uint16_t) -> None:
        return _lvgl.anim_timeline_set_progress(self, progress)

    def get_playtime(self) -> _lvgl.uint32_t:
        return _lvgl.anim_timeline_get_playtime(self)

    def get_reverse(self) -> _lvgl._Bool:
        return _lvgl.anim_timeline_get_reverse(self)


class area_t(_lvgl.area_t):

    def set(self, x1: _lvgl.coord_t, y1: _lvgl.coord_t, x2: _lvgl.coord_t, y2: _lvgl.coord_t) -> None:
        return _lvgl.area_set(self, x1, y1, x2, y2)

    def copy(self, src: "area_t") -> None:
        return _lvgl.area_copy(self, src)

    def get_width(self) -> _lvgl.coord_t:
        return _lvgl.area_get_width(self)

    def get_height(self) -> _lvgl.coord_t:
        return _lvgl.area_get_height(self)

    def set_width(self, w: _lvgl.coord_t) -> None:
        return _lvgl.area_set_width(self, w)

    def set_height(self, h: _lvgl.coord_t) -> None:
        return _lvgl.area_set_height(self, h)

    def get_size(self) -> _lvgl.uint32_t:
        return _lvgl.area_get_size(self)

    def increase(self, w_extra: _lvgl.coord_t, h_extra: _lvgl.coord_t) -> None:
        return _lvgl.area_increase(self, w_extra, h_extra)

    def move(self, x_ofs: _lvgl.coord_t, y_ofs: _lvgl.coord_t) -> None:
        return _lvgl.area_move(self, x_ofs, y_ofs)

    def align(self, to_align: "area_t", align: _lvgl.align_t, ofs_x: _lvgl.coord_t, ofs_y: _lvgl.coord_t) -> None:
        return _lvgl.area_align(self, to_align, align, ofs_x, ofs_y)


class point_t(_lvgl.point_t):

    def transform(self, angle: _lvgl.int32_t, zoom: _lvgl.int32_t, pivot: _lvgl.point_t) -> None:
        return _lvgl.point_transform(self, angle, zoom, pivot)


class font_t(_lvgl.font_t):

    def get_glyph_bitmap(self, letter: _lvgl.uint32_t) -> _lvgl.uint8_t:
        return _lvgl.font_get_glyph_bitmap(self, letter)

    def get_glyph_dsc(self, dsc_out: "font_glyph_dsc_t", letter: _lvgl.uint32_t, letter_next: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.font_get_glyph_dsc(self, dsc_out, letter, letter_next)

    def get_glyph_width(self, letter: _lvgl.uint32_t, letter_next: _lvgl.uint32_t) -> _lvgl.uint16_t:
        return _lvgl.font_get_glyph_width(self, letter, letter_next)

    def get_line_height(self) -> _lvgl.coord_t:
        return _lvgl.font_get_line_height(self)

    def free(self) -> None:
        return _lvgl.font_free(self)

    def get_bitmap_fmt_txt(self, letter: _lvgl.uint32_t) -> _lvgl.uint8_t:
        return _lvgl.font_get_bitmap_fmt_txt(self, letter)

    def get_glyph_dsc_fmt_txt(self, dsc_out: "font_glyph_dsc_t", unicode_letter: _lvgl.uint32_t, unicode_letter_next: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.font_get_glyph_dsc_fmt_txt(self, dsc_out, unicode_letter, unicode_letter_next)


class color_t(_lvgl.color_t):

    def from_native(self, dest_buf: _lvgl.uint8_t, dest_cf: _lvgl.color_format_t, px_cnt: _lvgl.uint32_t) -> None:
        return _lvgl.color_from_native(self, dest_buf, dest_cf, px_cnt)

    def set_int(self, v: _lvgl.uint32_t) -> None:
        return _lvgl.color_set_int(self, v)

    def to_int(self) -> _lvgl.uint32_t:
        return _lvgl.color_to_int(self)

    def eq(self, c2: "color_t") -> _lvgl._Bool:
        return _lvgl.color_eq(self, c2)

    def to8(self) -> "color8_t":
        return _lvgl.color_to8(self)

    def to16(self) -> "color16_t":
        return _lvgl.color_to16(self)

    def to24(self) -> "color24_t":
        return _lvgl.color_to24(self)

    def to32(self) -> "color32_t":
        return _lvgl.color_to32(self)

    def mix(self, c2: "color_t", mix: _lvgl.uint8_t) -> "color_t":
        return _lvgl.color_mix(self, c2, mix)

    def premult(self, mix: _lvgl.uint8_t, out: _lvgl.uint16_t) -> None:
        return _lvgl.color_premult(self, mix, out)

    def mix_with_alpha(self, bg_opa: _lvgl.opa_t, fg_color: "color_t", fg_opa: _lvgl.opa_t, res_color: "color_t", res_opa: _lvgl.opa_t) -> None:
        return _lvgl.color_mix_with_alpha(self, bg_opa, fg_color, fg_opa, res_color, res_opa)

    def brightness(self) -> _lvgl.uint8_t:
        return _lvgl.color_brightness(self)

    def fill(self, color: "color_t", px_num: _lvgl.uint32_t) -> None:
        return _lvgl.color_fill(self, color, px_num)

    def lighten(self, lvl: _lvgl.opa_t) -> "color_t":
        return _lvgl.color_lighten(self, lvl)

    def darken(self, lvl: _lvgl.opa_t) -> "color_t":
        return _lvgl.color_darken(self, lvl)

    def change_lightness(self, lvl: _lvgl.opa_t) -> "color_t":
        return _lvgl.color_change_lightness(self, lvl)

    def to_hsv(self) -> "color_hsv_t":
        return _lvgl.color_to_hsv(self)


class color8_t(_lvgl.color8_t):

    def set_int(self, v: _lvgl.uint8_t) -> None:
        return _lvgl.color8_set_int(self, v)

    def to_int(self) -> _lvgl.uint8_t:
        return _lvgl.color8_to_int(self)


class color16_t(_lvgl.color16_t):

    def set_int(self, v: _lvgl.uint16_t) -> None:
        return _lvgl.color16_set_int(self, v)

    def to_int(self) -> _lvgl.uint16_t:
        return _lvgl.color16_to_int(self)


class color24_t(_lvgl.color24_t):

    def set_int(self, v: _lvgl.uint32_t) -> None:
        return _lvgl.color24_set_int(self, v)

    def to_int(self) -> _lvgl.uint32_t:
        return _lvgl.color24_to_int(self)


class color32_t(_lvgl.color32_t):

    def set_int(self, v: _lvgl.uint32_t) -> None:
        return _lvgl.color32_set_int(self, v)

    def to_int(self) -> _lvgl.uint32_t:
        return _lvgl.color32_to_int(self)


class color_filter_dsc_t(_lvgl.color_filter_dsc_t):

    def init(self, cb: "color_filter_cb_t") -> None:
        return _lvgl.color_filter_dsc_init(self, cb)


class style_t(_lvgl.style_t):

    def init(self) -> None:
        return _lvgl.style_init(self)

    def reset(self) -> None:
        return _lvgl.style_reset(self)

    def remove_prop(self, prop: _lvgl.style_prop_t) -> _lvgl._Bool:
        return _lvgl.style_remove_prop(self, prop)

    def set_prop(self, prop: _lvgl.style_prop_t, value: "style_value_t") -> None:
        return _lvgl.style_set_prop(self, prop, value)

    def set_prop_meta(self, prop: _lvgl.style_prop_t, meta: _lvgl.uint16_t) -> None:
        return _lvgl.style_set_prop_meta(self, prop, meta)

    def get_prop(self, prop: _lvgl.style_prop_t, value: "style_value_t") -> _lvgl.style_res_t:
        return _lvgl.style_get_prop(self, prop, value)

    def get_prop_inlined(self, prop: _lvgl.style_prop_t, value: "style_value_t") -> _lvgl.style_res_t:
        return _lvgl.style_get_prop_inlined(self, prop, value)

    def is_empty(self) -> _lvgl._Bool:
        return _lvgl.style_is_empty(self)

    def set_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_width(self, value)

    def set_min_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_min_width(self, value)

    def set_max_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_max_width(self, value)

    def set_height(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_height(self, value)

    def set_min_height(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_min_height(self, value)

    def set_max_height(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_max_height(self, value)

    def set_x(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_x(self, value)

    def set_y(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_y(self, value)

    def set_align(self, value: _lvgl.align_t) -> None:
        return _lvgl.style_set_align(self, value)

    def set_transform_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_transform_width(self, value)

    def set_transform_height(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_transform_height(self, value)

    def set_translate_x(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_translate_x(self, value)

    def set_translate_y(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_translate_y(self, value)

    def set_transform_zoom(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_transform_zoom(self, value)

    def set_transform_angle(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_transform_angle(self, value)

    def set_transform_pivot_x(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_transform_pivot_x(self, value)

    def set_transform_pivot_y(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_transform_pivot_y(self, value)

    def set_pad_top(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_top(self, value)

    def set_pad_bottom(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_bottom(self, value)

    def set_pad_left(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_left(self, value)

    def set_pad_right(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_right(self, value)

    def set_pad_row(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_row(self, value)

    def set_pad_column(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_column(self, value)

    def set_margin_top(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_margin_top(self, value)

    def set_margin_bottom(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_margin_bottom(self, value)

    def set_margin_left(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_margin_left(self, value)

    def set_margin_right(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_margin_right(self, value)

    def set_bg_color(self, value: "color_t") -> None:
        return _lvgl.style_set_bg_color(self, value)

    def set_bg_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_bg_opa(self, value)

    def set_bg_grad_color(self, value: "color_t") -> None:
        return _lvgl.style_set_bg_grad_color(self, value)

    def set_bg_grad_dir(self, value: _lvgl.grad_dir_t) -> None:
        return _lvgl.style_set_bg_grad_dir(self, value)

    def set_bg_main_stop(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_bg_main_stop(self, value)

    def set_bg_grad_stop(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_bg_grad_stop(self, value)

    def set_bg_grad(self, value: "grad_dsc_t") -> None:
        return _lvgl.style_set_bg_grad(self, value)

    def set_bg_dither_mode(self, value: _lvgl.dither_mode_t) -> None:
        return _lvgl.style_set_bg_dither_mode(self, value)

    def set_bg_img_src(self, value: _lvgl.void) -> None:
        return _lvgl.style_set_bg_img_src(self, value)

    def set_bg_img_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_bg_img_opa(self, value)

    def set_bg_img_recolor(self, value: "color_t") -> None:
        return _lvgl.style_set_bg_img_recolor(self, value)

    def set_bg_img_recolor_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_bg_img_recolor_opa(self, value)

    def set_bg_img_tiled(self, value: _lvgl._Bool) -> None:
        return _lvgl.style_set_bg_img_tiled(self, value)

    def set_border_color(self, value: "color_t") -> None:
        return _lvgl.style_set_border_color(self, value)

    def set_border_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_border_opa(self, value)

    def set_border_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_border_width(self, value)

    def set_border_side(self, value: _lvgl.border_side_t) -> None:
        return _lvgl.style_set_border_side(self, value)

    def set_border_post(self, value: _lvgl._Bool) -> None:
        return _lvgl.style_set_border_post(self, value)

    def set_outline_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_outline_width(self, value)

    def set_outline_color(self, value: "color_t") -> None:
        return _lvgl.style_set_outline_color(self, value)

    def set_outline_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_outline_opa(self, value)

    def set_outline_pad(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_outline_pad(self, value)

    def set_shadow_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_shadow_width(self, value)

    def set_shadow_ofs_x(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_shadow_ofs_x(self, value)

    def set_shadow_ofs_y(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_shadow_ofs_y(self, value)

    def set_shadow_spread(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_shadow_spread(self, value)

    def set_shadow_color(self, value: "color_t") -> None:
        return _lvgl.style_set_shadow_color(self, value)

    def set_shadow_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_shadow_opa(self, value)

    def set_img_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_img_opa(self, value)

    def set_img_recolor(self, value: "color_t") -> None:
        return _lvgl.style_set_img_recolor(self, value)

    def set_img_recolor_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_img_recolor_opa(self, value)

    def set_line_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_line_width(self, value)

    def set_line_dash_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_line_dash_width(self, value)

    def set_line_dash_gap(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_line_dash_gap(self, value)

    def set_line_rounded(self, value: _lvgl._Bool) -> None:
        return _lvgl.style_set_line_rounded(self, value)

    def set_line_color(self, value: "color_t") -> None:
        return _lvgl.style_set_line_color(self, value)

    def set_line_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_line_opa(self, value)

    def set_arc_width(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_arc_width(self, value)

    def set_arc_rounded(self, value: _lvgl._Bool) -> None:
        return _lvgl.style_set_arc_rounded(self, value)

    def set_arc_color(self, value: "color_t") -> None:
        return _lvgl.style_set_arc_color(self, value)

    def set_arc_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_arc_opa(self, value)

    def set_arc_img_src(self, value: _lvgl.void) -> None:
        return _lvgl.style_set_arc_img_src(self, value)

    def set_text_color(self, value: "color_t") -> None:
        return _lvgl.style_set_text_color(self, value)

    def set_text_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_text_opa(self, value)

    def set_text_font(self, value: "font_t") -> None:
        return _lvgl.style_set_text_font(self, value)

    def set_text_letter_space(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_text_letter_space(self, value)

    def set_text_line_space(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_text_line_space(self, value)

    def set_text_decor(self, value: _lvgl.text_decor_t) -> None:
        return _lvgl.style_set_text_decor(self, value)

    def set_text_align(self, value: _lvgl.text_align_t) -> None:
        return _lvgl.style_set_text_align(self, value)

    def set_radius(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_radius(self, value)

    def set_clip_corner(self, value: _lvgl._Bool) -> None:
        return _lvgl.style_set_clip_corner(self, value)

    def set_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_opa(self, value)

    def set_color_filter_dsc(self, value: "color_filter_dsc_t") -> None:
        return _lvgl.style_set_color_filter_dsc(self, value)

    def set_color_filter_opa(self, value: _lvgl.opa_t) -> None:
        return _lvgl.style_set_color_filter_opa(self, value)

    def set_anim(self, value: "anim_t") -> None:
        return _lvgl.style_set_anim(self, value)

    def set_anim_time(self, value: _lvgl.uint32_t) -> None:
        return _lvgl.style_set_anim_time(self, value)

    def set_anim_speed(self, value: _lvgl.uint32_t) -> None:
        return _lvgl.style_set_anim_speed(self, value)

    def set_transition(self, value: "style_transition_dsc_t") -> None:
        return _lvgl.style_set_transition(self, value)

    def set_blend_mode(self, value: _lvgl.blend_mode_t) -> None:
        return _lvgl.style_set_blend_mode(self, value)

    def set_layout(self, value: _lvgl.uint16_t) -> None:
        return _lvgl.style_set_layout(self, value)

    def set_base_dir(self, value: _lvgl.base_dir_t) -> None:
        return _lvgl.style_set_base_dir(self, value)

    def set_size(self, width: _lvgl.coord_t, height: _lvgl.coord_t) -> None:
        return _lvgl.style_set_size(self, width, height)

    def set_pad_all(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_all(self, value)

    def set_pad_hor(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_hor(self, value)

    def set_pad_ver(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_ver(self, value)

    def set_pad_gap(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_pad_gap(self, value)

    def set_flex_flow(self, value: _lvgl.flex_flow_t) -> None:
        return _lvgl.style_set_flex_flow(self, value)

    def set_flex_main_place(self, value: _lvgl.flex_align_t) -> None:
        return _lvgl.style_set_flex_main_place(self, value)

    def set_flex_cross_place(self, value: _lvgl.flex_align_t) -> None:
        return _lvgl.style_set_flex_cross_place(self, value)

    def set_flex_track_place(self, value: _lvgl.flex_align_t) -> None:
        return _lvgl.style_set_flex_track_place(self, value)

    def set_flex_grow(self, value: _lvgl.uint8_t) -> None:
        return _lvgl.style_set_flex_grow(self, value)

    def set_grid_row_dsc_array(self, value: List[_lvgl.coord_t]) -> None:
        return _lvgl.style_set_grid_row_dsc_array(self, value)

    def set_grid_column_dsc_array(self, value: List[_lvgl.coord_t]) -> None:
        return _lvgl.style_set_grid_column_dsc_array(self, value)

    def set_grid_row_align(self, value: _lvgl.grid_align_t) -> None:
        return _lvgl.style_set_grid_row_align(self, value)

    def set_grid_column_align(self, value: _lvgl.grid_align_t) -> None:
        return _lvgl.style_set_grid_column_align(self, value)

    def set_grid_cell_column_pos(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_grid_cell_column_pos(self, value)

    def set_grid_cell_column_span(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_grid_cell_column_span(self, value)

    def set_grid_cell_row_pos(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_grid_cell_row_pos(self, value)

    def set_grid_cell_row_span(self, value: _lvgl.coord_t) -> None:
        return _lvgl.style_set_grid_cell_row_span(self, value)

    def set_grid_cell_x_align(self, value: _lvgl.grid_align_t) -> None:
        return _lvgl.style_set_grid_cell_x_align(self, value)

    def set_grid_cell_y_align(self, value: _lvgl.grid_align_t) -> None:
        return _lvgl.style_set_grid_cell_y_align(self, value)


class style_transition_dsc_t(_lvgl.style_transition_dsc_t):

    def init(self, props: List[_lvgl.style_prop_t], path_cb: "anim_path_cb_t", time: _lvgl.uint32_t, delay: _lvgl.uint32_t, user_data: Any) -> None:
        return _lvgl.style_transition_dsc_init(self, props, path_cb, time, delay, user_data)


class event_list_t(_lvgl.event_list_t):

    def send(self, e: "event_t", preprocess: _lvgl._Bool) -> _lvgl.res_t:
        return _lvgl.event_send(self, e, preprocess)

    def add(self, cb: "event_cb_t", filter: _lvgl.event_code_t, user_data: Any) -> None:
        return _lvgl.event_add(self, cb, filter, user_data)

    def get_count(self) -> _lvgl.uint32_t:
        return _lvgl.event_get_count(self)

    def get_dsc(self, index: _lvgl.uint32_t) -> "event_dsc_t":
        return _lvgl.event_get_dsc(self, index)

    def remove(self, index: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.event_remove(self, index)


class event_dsc_t(_lvgl.event_dsc_t):

    def get_cb(self) -> "event_cb_t":
        return _lvgl.event_dsc_get_cb(self)

    def get_user_data(self) -> Any:
        return _lvgl.event_dsc_get_user_data(self)


class event_t(_lvgl.event_t):

    def get_target(self) -> Any:
        return _lvgl.event_get_target(self)

    def get_current_target(self) -> Any:
        return _lvgl.event_get_current_target(self)

    def get_code(self) -> _lvgl.event_code_t:
        return _lvgl.event_get_code(self)

    def get_param(self) -> Any:
        return _lvgl.event_get_param(self)

    def get_user_data(self) -> Any:
        return _lvgl.event_get_user_data(self)

    def stop_bubbling(self) -> None:
        return _lvgl.event_stop_bubbling(self)

    def stop_processing(self) -> None:
        return _lvgl.event_stop_processing(self)

    def get_current_target_obj(self) -> "obj":
        return _lvgl.event_get_current_target_obj(self)

    def get_target_obj(self) -> "obj":
        return _lvgl.event_get_target_obj(self)

    def get_indev(self) -> "indev_t":
        return _lvgl.event_get_indev(self)

    def get_draw_part_dsc(self) -> "obj_draw_part_dsc_t":
        return _lvgl.event_get_draw_part_dsc(self)

    def get_draw_ctx(self) -> "draw_ctx_t":
        return _lvgl.event_get_draw_ctx(self)

    def get_old_size(self) -> "area_t":
        return _lvgl.event_get_old_size(self)

    def get_key(self) -> _lvgl.uint32_t:
        return _lvgl.event_get_key(self)

    def get_scroll_anim(self) -> "anim_t":
        return _lvgl.event_get_scroll_anim(self)

    def set_ext_draw_size(self, size: _lvgl.coord_t) -> None:
        return _lvgl.event_set_ext_draw_size(self, size)

    def get_self_size_info(self) -> _lvgl.point_t:
        return _lvgl.event_get_self_size_info(self)

    def get_hit_test_info(self) -> "hit_test_info_t":
        return _lvgl.event_get_hit_test_info(self)

    def get_cover_area(self) -> "area_t":
        return _lvgl.event_get_cover_area(self)

    def set_cover_res(self, res: _lvgl.cover_res_t) -> None:
        return _lvgl.event_set_cover_res(self, res)

    def get_msg(self) -> "msg_t":
        return _lvgl.event_get_msg(self)


class disp_t(_lvgl.disp_t):

    def remove(self) -> None:
        return _lvgl.disp_remove(self)

    def set_default(self) -> None:
        return _lvgl.disp_set_default(self)

    def get_next(self) -> "disp_t":
        return _lvgl.disp_get_next(self)

    def set_res(self, hor_res: _lvgl.coord_t, ver_res: _lvgl.coord_t) -> None:
        return _lvgl.disp_set_res(self, hor_res, ver_res)

    def set_physical_res(self, hor_res: _lvgl.coord_t, ver_res: _lvgl.coord_t) -> None:
        return _lvgl.disp_set_physical_res(self, hor_res, ver_res)

    def set_offset(self, x: _lvgl.coord_t, y: _lvgl.coord_t) -> None:
        return _lvgl.disp_set_offset(self, x, y)

    def set_rotation(self, rotation: _lvgl.disp_rotation_t, sw_rotate: _lvgl._Bool) -> None:
        return _lvgl.disp_set_rotation(self, rotation, sw_rotate)

    def set_dpi(self, dpi: _lvgl.coord_t) -> None:
        return _lvgl.disp_set_dpi(self, dpi)

    def get_hor_res(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_hor_res(self)

    def get_ver_res(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_ver_res(self)

    def get_physical_hor_res(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_physical_hor_res(self)

    def get_physical_ver_res(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_physical_ver_res(self)

    def get_offset_x(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_offset_x(self)

    def get_offset_y(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_offset_y(self)

    def get_rotation(self) -> _lvgl.disp_rotation_t:
        return _lvgl.disp_get_rotation(self)

    def get_dpi(self) -> _lvgl.coord_t:
        return _lvgl.disp_get_dpi(self)

    def set_draw_buffers(self, buf1: _lvgl.void, buf2: _lvgl.void, buf_size_byte: _lvgl.uint32_t, render_mode: _lvgl.disp_render_mode_t) -> None:
        return _lvgl.disp_set_draw_buffers(self, buf1, buf2, buf_size_byte, render_mode)

    def set_flush_cb(self, flush_cb: "disp_flush_cb_t", user_data: Any) -> None:
        return _lvgl.disp_set_flush_cb(self, flush_cb, user_data)

    def set_color_format(self, color_format: _lvgl.color_format_t) -> None:
        return _lvgl.disp_set_color_format(self, color_format)

    def get_color_format(self) -> _lvgl.color_format_t:
        return _lvgl.disp_get_color_format(self)

    def set_antialaising(self, en: _lvgl._Bool) -> None:
        return _lvgl.disp_set_antialaising(self, en)

    def get_antialiasing(self) -> _lvgl._Bool:
        return _lvgl.disp_get_antialiasing(self)

    def flush_ready(self) -> None:
        return _lvgl.disp_flush_ready(self)

    def flush_is_last(self) -> _lvgl._Bool:
        return _lvgl.disp_flush_is_last(self)

    def is_double_buffered(self) -> _lvgl._Bool:
        return _lvgl.disp_is_double_buffered(self)

    def set_draw_ctx(self, draw_ctx_init: "disp_draw_ctx_init_cb_t", draw_ctx_deinit: "disp_draw_ctx_deinit_cb_t", draw_ctx_size: _lvgl.size_t) -> None:
        return _lvgl.disp_set_draw_ctx(self, draw_ctx_init, draw_ctx_deinit, draw_ctx_size)

    def get_scr_act(self) -> "obj":
        return _lvgl.disp_get_scr_act(self)

    def get_scr_prev(self) -> "obj":
        return _lvgl.disp_get_scr_prev(self)

    def get_layer_top(self) -> "obj":
        return _lvgl.disp_get_layer_top(self)

    def get_layer_sys(self) -> "obj":
        return _lvgl.disp_get_layer_sys(self)

    def get_layer_bottom(self) -> "obj":
        return _lvgl.disp_get_layer_bottom(self)

    def add_event(self, event_cb: "event_cb_t", filter: _lvgl.event_code_t, user_data: Any) -> None:
        return _lvgl.disp_add_event(self, event_cb, filter, user_data)

    def get_event_count(self) -> _lvgl.uint32_t:
        return _lvgl.disp_get_event_count(self)

    def get_event_dsc(self, index: _lvgl.uint32_t) -> "event_dsc_t":
        return _lvgl.disp_get_event_dsc(self, index)

    def remove_event(self, index: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.disp_remove_event(self, index)

    def send_event(self, code: _lvgl.event_code_t, user_data: Any) -> _lvgl.res_t:
        return _lvgl.disp_send_event(self, code, user_data)

    def set_theme(self, th: "theme_t") -> None:
        return _lvgl.disp_set_theme(self, th)

    def get_theme(self) -> "theme_t":
        return _lvgl.disp_get_theme(self)

    def get_inactive_time(self) -> _lvgl.uint32_t:
        return _lvgl.disp_get_inactive_time(self)

    def trig_activity(self) -> None:
        return _lvgl.disp_trig_activity(self)

    def enable_invalidation(self, en: _lvgl._Bool) -> None:
        return _lvgl.disp_enable_invalidation(self, en)

    def is_invalidation_enabled(self) -> _lvgl._Bool:
        return _lvgl.disp_is_invalidation_enabled(self)

    def get_chroma_key_color(self) -> "color_t":
        return _lvgl.disp_get_chroma_key_color(self)

    def set_user_data(self, user_data: Any) -> None:
        return _lvgl.disp_set_user_data(self, user_data)

    def set_driver_data(self, driver_data: _lvgl.void) -> None:
        return _lvgl.disp_set_driver_data(self, driver_data)

    def get_user_data(self) -> Any:
        return _lvgl.disp_get_user_data(self)

    def get_driver_data(self) -> Any:
        return _lvgl.disp_get_driver_data(self)

    def dpx(self, n: _lvgl.coord_t) -> _lvgl.coord_t:
        return _lvgl.disp_dpx(self, n)


class img_dsc_t(_lvgl.img_dsc_t):

    def buf_set_palette(self, id: _lvgl.uint8_t, c: "color32_t") -> None:
        return _lvgl.img_buf_set_palette(self, id, c)

    def buf_free(self) -> None:
        return _lvgl.img_buf_free(self)


class fs_drv_t(_lvgl.fs_drv_t):

    def init(self) -> None:
        return _lvgl.fs_drv_init(self)

    def register(self) -> None:
        return _lvgl.fs_drv_register(self)


class fs_file_t(_lvgl.fs_file_t):

    def open(self, path: _lvgl.char, mode: _lvgl.fs_mode_t) -> _lvgl.fs_res_t:
        return _lvgl.fs_open(self, path, mode)

    def close(self) -> _lvgl.fs_res_t:
        return _lvgl.fs_close(self)

    def read(self, buf: _lvgl.void, btr: _lvgl.uint32_t, br: _lvgl.uint32_t) -> _lvgl.fs_res_t:
        return _lvgl.fs_read(self, buf, btr, br)

    def write(self, buf: _lvgl.void, btw: _lvgl.uint32_t, bw: _lvgl.uint32_t) -> _lvgl.fs_res_t:
        return _lvgl.fs_write(self, buf, btw, bw)

    def seek(self, pos: _lvgl.uint32_t, whence: _lvgl.fs_whence_t) -> _lvgl.fs_res_t:
        return _lvgl.fs_seek(self, pos, whence)

    def tell(self, pos: _lvgl.uint32_t) -> _lvgl.fs_res_t:
        return _lvgl.fs_tell(self, pos)


class fs_dir_t(_lvgl.fs_dir_t):

    def open(self, path: _lvgl.char) -> _lvgl.fs_res_t:
        return _lvgl.fs_dir_open(self, path)

    def read(self, fn: _lvgl.char) -> _lvgl.fs_res_t:
        return _lvgl.fs_dir_read(self, fn)

    def close(self) -> _lvgl.fs_res_t:
        return _lvgl.fs_dir_close(self)


class img_decoder_dsc_t(_lvgl.img_decoder_dsc_t):

    def open(self, src: _lvgl.void, color: "color_t", frame_id: _lvgl.int32_t) -> _lvgl.res_t:
        return _lvgl.img_decoder_open(self, src, color, frame_id)

    def read_line(self, x: _lvgl.coord_t, y: _lvgl.coord_t, len: _lvgl.coord_t, buf: _lvgl.uint8_t) -> _lvgl.res_t:
        return _lvgl.img_decoder_read_line(self, x, y, len, buf)

    def close(self) -> None:
        return _lvgl.img_decoder_close(self)


class img_decoder_t(_lvgl.img_decoder_t):

    def delete(self) -> None:
        return _lvgl.img_decoder_delete(self)

    def set_info_cb(self, info_cb: "img_decoder_info_f_t") -> None:
        return _lvgl.img_decoder_set_info_cb(self, info_cb)

    def set_open_cb(self, open_cb: "img_decoder_open_f_t") -> None:
        return _lvgl.img_decoder_set_open_cb(self, open_cb)

    def set_read_line_cb(self, read_line_cb: "img_decoder_read_line_f_t") -> None:
        return _lvgl.img_decoder_set_read_line_cb(self, read_line_cb)

    def set_close_cb(self, close_cb: "img_decoder_close_f_t") -> None:
        return _lvgl.img_decoder_set_close_cb(self, close_cb)

    def built_in_info(self, src: _lvgl.void, header: "img_header_t") -> _lvgl.res_t:
        return _lvgl.img_decoder_built_in_info(self, src, header)

    def built_in_open(self, dsc: "img_decoder_dsc_t") -> _lvgl.res_t:
        return _lvgl.img_decoder_built_in_open(self, dsc)

    def built_in_close(self, dsc: "img_decoder_dsc_t") -> None:
        return _lvgl.img_decoder_built_in_close(self, dsc)


class img_cache_manager_t(_lvgl.img_cache_manager_t):

    def init(self) -> None:
        return _lvgl.img_cache_manager_init(self)

    def apply(self) -> None:
        return _lvgl.img_cache_manager_apply(self)


class draw_rect_dsc_t(_lvgl.draw_rect_dsc_t):

    def init(self) -> None:
        return _lvgl.draw_rect_dsc_init(self)


class draw_ctx_t(_lvgl.draw_ctx_t):

    def rect(self, dsc: "draw_rect_dsc_t", coords: "area_t") -> None:
        return _lvgl.draw_rect(self, dsc, coords)

    def label(self, dsc: "draw_label_dsc_t", coords: "area_t", txt: _lvgl.char, hint: _lvgl.draw_label_hint_t) -> None:
        return _lvgl.draw_label(self, dsc, coords, txt, hint)

    def letter(self, dsc: "draw_label_dsc_t", pos_p: _lvgl.point_t, letter: _lvgl.uint32_t) -> None:
        return _lvgl.draw_letter(self, dsc, pos_p, letter)

    def img(self, dsc: "draw_img_dsc_t", coords: "area_t", src: _lvgl.void) -> None:
        return _lvgl.draw_img(self, dsc, coords, src)

    def img_decoded(self, dsc: "draw_img_dsc_t", coords: "area_t", map_p: _lvgl.uint8_t, sup: "draw_img_sup_t", color_format: _lvgl.color_format_t) -> None:
        return _lvgl.draw_img_decoded(self, dsc, coords, map_p, sup, color_format)

    def line(self, dsc: "draw_line_dsc_t", point1: _lvgl.point_t, point2: _lvgl.point_t) -> None:
        return _lvgl.draw_line(self, dsc, point1, point2)

    def polygon(self, draw_dsc: "draw_rect_dsc_t", points: List[_lvgl.point_t], point_cnt: _lvgl.uint16_t) -> None:
        return _lvgl.draw_polygon(self, draw_dsc, points, point_cnt)

    def triangle(self, draw_dsc: "draw_rect_dsc_t", points: List[_lvgl.point_t]) -> None:
        return _lvgl.draw_triangle(self, draw_dsc, points)

    def arc(self, dsc: "draw_arc_dsc_t", center: _lvgl.point_t, radius: _lvgl.uint16_t, start_angle: _lvgl.uint16_t, end_angle: _lvgl.uint16_t) -> None:
        return _lvgl.draw_arc(self, dsc, center, radius, start_angle, end_angle)

    def transform(self, dest_area: "area_t", src_buf: _lvgl.void, src_w: _lvgl.coord_t, src_h: _lvgl.coord_t, src_stride: _lvgl.coord_t, draw_dsc: "draw_img_dsc_t", sup: "draw_img_sup_t", cf: _lvgl.color_format_t, cbuf: "color_t", abuf: _lvgl.opa_t) -> None:
        return _lvgl.draw_transform(self, dest_area, src_buf, src_w, src_h, src_stride, draw_dsc, sup, cf, cbuf, abuf)

    def layer_adjust(self, layer_ctx: "draw_layer_ctx_t", flags: _lvgl.draw_layer_flags_t) -> None:
        return _lvgl.draw_layer_adjust(self, layer_ctx, flags)

    def layer_blend(self, layer_ctx: "draw_layer_ctx_t", draw_dsc: "draw_img_dsc_t") -> None:
        return _lvgl.draw_layer_blend(self, layer_ctx, draw_dsc)

    def layer_destroy(self, layer_ctx: "draw_layer_ctx_t") -> None:
        return _lvgl.draw_layer_destroy(self, layer_ctx)

    def wait_for_finish(self) -> None:
        return _lvgl.draw_wait_for_finish(self)

    def layer_create(self, layer_area: "area_t", flags: _lvgl.draw_layer_flags_t) -> "draw_layer_ctx_t":
        return _lvgl.draw_layer_create(self, layer_area, flags)


class draw_label_dsc_t(_lvgl.draw_label_dsc_t):

    def init(self) -> None:
        return _lvgl.draw_label_dsc_init(self)


class draw_img_dsc_t(_lvgl.draw_img_dsc_t):

    def init(self) -> None:
        return _lvgl.draw_img_dsc_init(self)


class draw_line_dsc_t(_lvgl.draw_line_dsc_t):

    def init(self) -> None:
        return _lvgl.draw_line_dsc_init(self)


class draw_arc_dsc_t(_lvgl.draw_arc_dsc_t):

    def init(self) -> None:
        return _lvgl.draw_arc_dsc_init(self)


class draw_mask_line_param_t(_lvgl.draw_mask_line_param_t):

    def points_init(self, p1x: _lvgl.coord_t, p1y: _lvgl.coord_t, p2x: _lvgl.coord_t, p2y: _lvgl.coord_t, side: _lvgl.draw_mask_line_side_t) -> None:
        return _lvgl.draw_mask_line_points_init(self, p1x, p1y, p2x, p2y, side)

    def angle_init(self, p1x: _lvgl.coord_t, py: _lvgl.coord_t, angle: _lvgl.int16_t, side: _lvgl.draw_mask_line_side_t) -> None:
        return _lvgl.draw_mask_line_angle_init(self, p1x, py, angle, side)


class draw_mask_angle_param_t(_lvgl.draw_mask_angle_param_t):

    def init(self, vertex_x: _lvgl.coord_t, vertex_y: _lvgl.coord_t, start_angle: _lvgl.coord_t, end_angle: _lvgl.coord_t) -> None:
        return _lvgl.draw_mask_angle_init(self, vertex_x, vertex_y, start_angle, end_angle)


class draw_mask_radius_param_t(_lvgl.draw_mask_radius_param_t):

    def init(self, rect: "area_t", radius: _lvgl.coord_t, inv: _lvgl._Bool) -> None:
        return _lvgl.draw_mask_radius_init(self, rect, radius, inv)


class draw_mask_fade_param_t(_lvgl.draw_mask_fade_param_t):

    def init(self, coords: "area_t", opa_top: _lvgl.opa_t, y_top: _lvgl.coord_t, opa_bottom: _lvgl.opa_t, y_bottom: _lvgl.coord_t) -> None:
        return _lvgl.draw_mask_fade_init(self, coords, opa_top, y_top, opa_bottom, y_bottom)


class draw_mask_map_param_t(_lvgl.draw_mask_map_param_t):

    def init(self, coords: "area_t", map: _lvgl.opa_t) -> None:
        return _lvgl.draw_mask_map_init(self, coords, map)


class draw_mask_polygon_param_t(_lvgl.draw_mask_polygon_param_t):

    def init(self, points: _lvgl.point_t, point_cnt: _lvgl.uint16_t) -> None:
        return _lvgl.draw_mask_polygon_init(self, points, point_cnt)


class obj_draw_part_dsc_t(_lvgl.obj_draw_part_dsc_t):

    def dsc_init(self, draw_ctx: "draw_ctx_t") -> None:
        return _lvgl.obj_draw_dsc_init(self, draw_ctx)

    def check_type(self, class_p: "obj_class_t", type: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_draw_part_check_type(self, class_p, type)


class obj_class_t(_lvgl.obj_class_t):

    def create_obj(self, parent: "obj") -> "obj":
        return _lvgl.obj_class_create_obj(self, parent)

    def event_base(self, e: "event_t") -> _lvgl.res_t:
        return _lvgl.obj_event_base(self, e)


class group_t(_lvgl.group_t):

    def _del(self) -> None:
        return _lvgl.group_del(self)

    def set_default(self) -> None:
        return _lvgl.group_set_default(self)

    def add_obj(self, obj: "obj") -> None:
        return _lvgl.group_add_obj(self, obj)

    def remove_all_objs(self) -> None:
        return _lvgl.group_remove_all_objs(self)

    def focus_next(self) -> None:
        return _lvgl.group_focus_next(self)

    def focus_prev(self) -> None:
        return _lvgl.group_focus_prev(self)

    def focus_freeze(self, en: _lvgl._Bool) -> None:
        return _lvgl.group_focus_freeze(self, en)

    def send_data(self, c: _lvgl.uint32_t) -> _lvgl.res_t:
        return _lvgl.group_send_data(self, c)

    def set_focus_cb(self, focus_cb: "group_focus_cb_t") -> None:
        return _lvgl.group_set_focus_cb(self, focus_cb)

    def set_edge_cb(self, edge_cb: "group_edge_cb_t") -> None:
        return _lvgl.group_set_edge_cb(self, edge_cb)

    def set_refocus_policy(self, policy: _lvgl.group_refocus_policy_t) -> None:
        return _lvgl.group_set_refocus_policy(self, policy)

    def set_editing(self, edit: _lvgl._Bool) -> None:
        return _lvgl.group_set_editing(self, edit)

    def set_wrap(self, en: _lvgl._Bool) -> None:
        return _lvgl.group_set_wrap(self, en)

    def get_focused(self) -> "obj":
        return _lvgl.group_get_focused(self)

    def get_focus_cb(self) -> "group_focus_cb_t":
        return _lvgl.group_get_focus_cb(self)

    def get_edge_cb(self) -> "group_edge_cb_t":
        return _lvgl.group_get_edge_cb(self)

    def get_editing(self) -> _lvgl._Bool:
        return _lvgl.group_get_editing(self)

    def get_wrap(self) -> _lvgl._Bool:
        return _lvgl.group_get_wrap(self)

    def get_obj_count(self) -> _lvgl.uint32_t:
        return _lvgl.group_get_obj_count(self)


class indev_t(_lvgl.indev_t):

    def delete(self) -> None:
        return _lvgl.indev_delete(self)

    def get_next(self) -> "indev_t":
        return _lvgl.indev_get_next(self)

    def enable(self, en: _lvgl._Bool) -> None:
        return _lvgl.indev_enable(self, en)

    def set_type(self, indev_type: _lvgl.indev_type_t) -> None:
        return _lvgl.indev_set_type(self, indev_type)

    def set_read_cb(self, read_cb: "indev_read_cb_t", user_data: Any) -> None:
        return _lvgl.indev_set_read_cb(self, read_cb, user_data)

    def set_user_data(self, user_data: Any) -> None:
        return _lvgl.indev_set_user_data(self, user_data)

    def set_driver_data(self, driver_data: _lvgl.void) -> None:
        return _lvgl.indev_set_driver_data(self, driver_data)

    def get_type(self) -> _lvgl.indev_type_t:
        return _lvgl.indev_get_type(self)

    def get_state(self) -> _lvgl.indev_state_t:
        return _lvgl.indev_get_state(self)

    def get_group(self) -> "group_t":
        return _lvgl.indev_get_group(self)

    def get_disp(self) -> "disp_t":
        return _lvgl.indev_get_disp(self)

    def set_disp(self, disp: "disp_t") -> None:
        return _lvgl.indev_set_disp(self, disp)

    def get_user_data(self) -> Any:
        return _lvgl.indev_get_user_data(self)

    def get_driver_data(self) -> Any:
        return _lvgl.indev_get_driver_data(self)

    def reset(self, obj: "obj") -> None:
        return _lvgl.indev_reset(self, obj)

    def reset_long_press(self) -> None:
        return _lvgl.indev_reset_long_press(self)

    def set_cursor(self, cur_obj: "obj") -> None:
        return _lvgl.indev_set_cursor(self, cur_obj)

    def set_group(self, group: "group_t") -> None:
        return _lvgl.indev_set_group(self, group)

    def set_button_points(self, points: List[_lvgl.point_t]) -> None:
        return _lvgl.indev_set_button_points(self, points)

    def get_point(self, point: _lvgl.point_t) -> None:
        return _lvgl.indev_get_point(self, point)

    def get_gesture_dir(self) -> _lvgl.dir_t:
        return _lvgl.indev_get_gesture_dir(self)

    def get_key(self) -> _lvgl.uint32_t:
        return _lvgl.indev_get_key(self)

    def get_scroll_dir(self) -> _lvgl.dir_t:
        return _lvgl.indev_get_scroll_dir(self)

    def get_scroll_obj(self) -> "obj":
        return _lvgl.indev_get_scroll_obj(self)

    def get_vect(self, point: _lvgl.point_t) -> None:
        return _lvgl.indev_get_vect(self, point)

    def wait_release(self) -> None:
        return _lvgl.indev_wait_release(self)

    def get_read_timer(self) -> "timer_t":
        return _lvgl.indev_get_read_timer(self)


class theme_t(_lvgl.theme_t):

    def set_parent(self, parent: "theme_t") -> None:
        return _lvgl.theme_set_parent(self, parent)

    def set_apply_cb(self, apply_cb: "theme_apply_cb_t") -> None:
        return _lvgl.theme_set_apply_cb(self, apply_cb)


class span_t(_lvgl.span_t):

    def set_text(self, text: _lvgl.char) -> None:
        return _lvgl.span_set_text(self, text)

    def set_text_static(self, text: _lvgl.char) -> None:
        return _lvgl.span_set_text_static(self, text)


class msg_t(_lvgl.msg_t):

    def get_id(self) -> _lvgl.msg_id_t:
        return _lvgl.msg_get_id(self)

    def get_payload(self) -> Any:
        return _lvgl.msg_get_payload(self)

    def get_user_data(self) -> Any:
        return _lvgl.msg_get_user_data(self)


class obj(_lvgl.obj_t):
    
    class CLASS_THEME_INHERITABLE:
        FALSE = _lvgl.OBJ_CLASS_THEME_INHERITABLE_FALSE
        TRUE = _lvgl.OBJ_CLASS_THEME_INHERITABLE_TRUE
    
    class CLASS_GROUP_DEF:
        FALSE = _lvgl.OBJ_CLASS_GROUP_DEF_FALSE
        INHERIT = _lvgl.OBJ_CLASS_GROUP_DEF_INHERIT
        TRUE = _lvgl.OBJ_CLASS_GROUP_DEF_TRUE
    
    class CLASS_EDITABLE:
        FALSE = _lvgl.OBJ_CLASS_EDITABLE_FALSE
        INHERIT = _lvgl.OBJ_CLASS_EDITABLE_INHERIT
        TRUE = _lvgl.OBJ_CLASS_EDITABLE_TRUE

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.obj_create(parent)
            cls.cast(self)
   
    def _del(self) -> None:
        return _lvgl.obj_del(self)

    def clean(self) -> None:
        return _lvgl.obj_clean(self)

    def del_delayed(self, delay_ms: _lvgl.uint32_t) -> None:
        return _lvgl.obj_del_delayed(self, delay_ms)

    def del_async(self) -> None:
        return _lvgl.obj_del_async(self)

    def set_parent(self, parent: "obj") -> None:
        return _lvgl.obj_set_parent(self, parent)

    def swap(self, obj2: "obj") -> None:
        return _lvgl.obj_swap(self, obj2)

    def move_to_index(self, index: _lvgl.int32_t) -> None:
        return _lvgl.obj_move_to_index(self, index)

    def get_screen(self) -> "obj":
        return _lvgl.obj_get_screen(self)

    def get_disp(self) -> "disp_t":
        return _lvgl.obj_get_disp(self)

    def get_parent(self) -> "obj":
        return _lvgl.obj_get_parent(self)

    def get_child(self, id: _lvgl.int32_t) -> "obj":
        return _lvgl.obj_get_child(self, id)

    def get_child_cnt(self) -> _lvgl.uint32_t:
        return _lvgl.obj_get_child_cnt(self)

    def get_index(self) -> _lvgl.uint32_t:
        return _lvgl.obj_get_index(self)

    def tree_walk(self, cb: "objree_walk_cb_t", user_data: Any) -> None:
        return _lvgl.obj_tree_walk(self, cb, user_data)

    def set_pos(self, x: _lvgl.coord_t, y: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_pos(self, x, y)

    def set_x(self, x: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_x(self, x)

    def set_y(self, y: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_y(self, y)

    def set_size(self, w: _lvgl.coord_t, h: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_size(self, w, h)

    def refr_size(self) -> _lvgl._Bool:
        return _lvgl.obj_refr_size(self)

    def set_width(self, w: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_width(self, w)

    def set_height(self, h: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_height(self, h)

    def set_content_width(self, w: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_content_width(self, w)

    def set_content_height(self, h: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_content_height(self, h)

    def set_layout(self, layout: _lvgl.uint32_t) -> None:
        return _lvgl.obj_set_layout(self, layout)

    def is_layout_positioned(self) -> _lvgl._Bool:
        return _lvgl.obj_is_layout_positioned(self)

    def mark_layout_as_dirty(self) -> None:
        return _lvgl.obj_mark_layout_as_dirty(self)

    def update_layout(self) -> None:
        return _lvgl.obj_update_layout(self)

    def set_align(self, align: _lvgl.align_t) -> None:
        return _lvgl.obj_set_align(self, align)

    def align(self, align: _lvgl.align_t, x_ofs: _lvgl.coord_t, y_ofs: _lvgl.coord_t) -> None:
        return _lvgl.obj_align(self, align, x_ofs, y_ofs)

    def align_to(self, base: "obj", align: _lvgl.align_t, x_ofs: _lvgl.coord_t, y_ofs: _lvgl.coord_t) -> None:
        return _lvgl.obj_align_to(self, base, align, x_ofs, y_ofs)

    def center(self) -> None:
        return _lvgl.obj_center(self)

    def get_coords(self, coords: "area_t") -> None:
        return _lvgl.obj_get_coords(self, coords)

    def get_x(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_x(self)

    def get_x2(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_x2(self)

    def get_y(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_y(self)

    def get_y2(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_y2(self)

    def get_x_aligned(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_x_aligned(self)

    def get_y_aligned(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_y_aligned(self)

    def get_width(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_width(self)

    def get_height(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_height(self)

    def get_content_width(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_content_width(self)

    def get_content_height(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_content_height(self)

    def get_content_coords(self, area: "area_t") -> None:
        return _lvgl.obj_get_content_coords(self, area)

    def get_self_width(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_self_width(self)

    def get_self_height(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_self_height(self)

    def refresh_self_size(self) -> _lvgl._Bool:
        return _lvgl.obj_refresh_self_size(self)

    def refr_pos(self) -> None:
        return _lvgl.obj_refr_pos(self)

    def move_to(self, x: _lvgl.coord_t, y: _lvgl.coord_t) -> None:
        return _lvgl.obj_move_to(self, x, y)

    def move_children_by(self, x_diff: _lvgl.coord_t, y_diff: _lvgl.coord_t, ignore_floating: _lvgl._Bool) -> None:
        return _lvgl.obj_move_children_by(self, x_diff, y_diff, ignore_floating)

    def transform_point(self, p: _lvgl.point_t, recursive: _lvgl._Bool, inv: _lvgl._Bool) -> None:
        return _lvgl.obj_transform_point(self, p, recursive, inv)

    def get_transformed_area(self, area: "area_t", recursive: _lvgl._Bool, inv: _lvgl._Bool) -> None:
        return _lvgl.obj_get_transformed_area(self, area, recursive, inv)

    def invalidate_area(self, area: "area_t") -> None:
        return _lvgl.obj_invalidate_area(self, area)

    def invalidate(self) -> None:
        return _lvgl.obj_invalidate(self)

    def area_is_visible(self, area: "area_t") -> _lvgl._Bool:
        return _lvgl.obj_area_is_visible(self, area)

    def is_visible(self) -> _lvgl._Bool:
        return _lvgl.obj_is_visible(self)

    def set_ext_click_area(self, size: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_ext_click_area(self, size)

    def get_click_area(self, area: "area_t") -> None:
        return _lvgl.obj_get_click_area(self, area)

    def hit_test(self, point: _lvgl.point_t) -> _lvgl._Bool:
        return _lvgl.obj_hit_test(self, point)

    def set_scrollbar_mode(self, mode: _lvgl.scrollbar_mode_t) -> None:
        return _lvgl.obj_set_scrollbar_mode(self, mode)

    def set_scroll_dir(self, dir: _lvgl.dir_t) -> None:
        return _lvgl.obj_set_scroll_dir(self, dir)

    def set_scroll_snap_x(self, align: _lvgl.scroll_snap_t) -> None:
        return _lvgl.obj_set_scroll_snap_x(self, align)

    def set_scroll_snap_y(self, align: _lvgl.scroll_snap_t) -> None:
        return _lvgl.obj_set_scroll_snap_y(self, align)

    def get_scrollbar_mode(self) -> _lvgl.scrollbar_mode_t:
        return _lvgl.obj_get_scrollbar_mode(self)

    def get_scroll_dir(self) -> _lvgl.dir_t:
        return _lvgl.obj_get_scroll_dir(self)

    def get_scroll_snap_x(self) -> _lvgl.scroll_snap_t:
        return _lvgl.obj_get_scroll_snap_x(self)

    def get_scroll_snap_y(self) -> _lvgl.scroll_snap_t:
        return _lvgl.obj_get_scroll_snap_y(self)

    def get_scroll_x(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_scroll_x(self)

    def get_scroll_y(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_scroll_y(self)

    def get_scroll_top(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_scroll_top(self)

    def get_scroll_bottom(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_scroll_bottom(self)

    def get_scroll_left(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_scroll_left(self)

    def get_scroll_right(self) -> _lvgl.coord_t:
        return _lvgl.obj_get_scroll_right(self)

    def get_scroll_end(self, end: _lvgl.point_t) -> None:
        return _lvgl.obj_get_scroll_end(self, end)

    def scroll_by(self, x: _lvgl.coord_t, y: _lvgl.coord_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_by(self, x, y, anim_en)

    def scroll_by_bounded(self, dx: _lvgl.coord_t, dy: _lvgl.coord_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_by_bounded(self, dx, dy, anim_en)

    def scroll_to(self, x: _lvgl.coord_t, y: _lvgl.coord_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_to(self, x, y, anim_en)

    def scroll_to_x(self, x: _lvgl.coord_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_to_x(self, x, anim_en)

    def scroll_to_y(self, y: _lvgl.coord_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_to_y(self, y, anim_en)

    def scroll_to_view(self, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_to_view(self, anim_en)

    def scroll_to_view_recursive(self, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_scroll_to_view_recursive(self, anim_en)

    def is_scrolling(self) -> _lvgl._Bool:
        return _lvgl.obj_is_scrolling(self)

    def update_snap(self, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_update_snap(self, anim_en)

    def get_scrollbar_area(self, hor: "area_t", ver: "area_t") -> None:
        return _lvgl.obj_get_scrollbar_area(self, hor, ver)

    def scrollbar_invalidate(self) -> None:
        return _lvgl.obj_scrollbar_invalidate(self)

    def readjust_scroll(self, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_readjust_scroll(self, anim_en)

    def add_style(self, style: "style_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_add_style(self, style, selector)

    def replace_style(self, old_style: "style_t", new_style: "style_t", selector: _lvgl.style_selector_t) -> _lvgl._Bool:
        return _lvgl.obj_replace_style(self, old_style, new_style, selector)

    def remove_style(self, style: "style_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_remove_style(self, style, selector)

    def remove_style_all(self) -> None:
        return _lvgl.obj_remove_style_all(self)

    def refresh_style(self, part: _lvgl.part_t, prop: _lvgl.style_prop_t) -> None:
        return _lvgl.obj_refresh_style(self, part, prop)

    def get_style_prop(self, part: _lvgl.part_t, prop: _lvgl.style_prop_t) -> "style_value_t":
        return _lvgl.obj_get_style_prop(self, part, prop)

    def set_local_style_prop(self, prop: _lvgl.style_prop_t, value: "style_value_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_local_style_prop(self, prop, value, selector)

    def set_local_style_prop_meta(self, prop: _lvgl.style_prop_t, meta: _lvgl.uint16_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_local_style_prop_meta(self, prop, meta, selector)

    def get_local_style_prop(self, prop: _lvgl.style_prop_t, value: "style_value_t", selector: _lvgl.style_selector_t) -> _lvgl.style_res_t:
        return _lvgl.obj_get_local_style_prop(self, prop, value, selector)

    def remove_local_style_prop(self, prop: _lvgl.style_prop_t, selector: _lvgl.style_selector_t) -> _lvgl._Bool:
        return _lvgl.obj_remove_local_style_prop(self, prop, selector)

    def fade_in(self, time: _lvgl.uint32_t, delay: _lvgl.uint32_t) -> None:
        return _lvgl.obj_fade_in(self, time, delay)

    def fade_out(self, time: _lvgl.uint32_t, delay: _lvgl.uint32_t) -> None:
        return _lvgl.obj_fade_out(self, time, delay)

    def get_style_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_width(self, part)

    def get_style_min_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_min_width(self, part)

    def get_style_max_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_max_width(self, part)

    def get_style_height(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_height(self, part)

    def get_style_min_height(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_min_height(self, part)

    def get_style_max_height(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_max_height(self, part)

    def get_style_x(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_x(self, part)

    def get_style_y(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_y(self, part)

    def get_style_align(self, part: _lvgl.uint32_t) -> _lvgl.align_t:
        return _lvgl.obj_get_style_align(self, part)

    def get_style_transform_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_width(self, part)

    def get_style_transform_height(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_height(self, part)

    def get_style_translate_x(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_translate_x(self, part)

    def get_style_translate_y(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_translate_y(self, part)

    def get_style_transform_zoom(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_zoom(self, part)

    def get_style_transform_angle(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_angle(self, part)

    def get_style_transform_pivot_x(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_pivot_x(self, part)

    def get_style_transform_pivot_y(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_pivot_y(self, part)

    def get_style_pad_top(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_pad_top(self, part)

    def get_style_pad_bottom(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_pad_bottom(self, part)

    def get_style_pad_left(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_pad_left(self, part)

    def get_style_pad_right(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_pad_right(self, part)

    def get_style_pad_row(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_pad_row(self, part)

    def get_style_pad_column(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_pad_column(self, part)

    def get_style_margin_top(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_margin_top(self, part)

    def get_style_margin_bottom(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_margin_bottom(self, part)

    def get_style_margin_left(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_margin_left(self, part)

    def get_style_margin_right(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_margin_right(self, part)

    def get_style_bg_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_bg_color(self, part)

    def get_style_bg_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_bg_color_filtered(self, part)

    def get_style_bg_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_bg_opa(self, part)

    def get_style_bg_grad_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_bg_grad_color(self, part)

    def get_style_bg_grad_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_bg_grad_color_filtered(self, part)

    def get_style_bg_grad_dir(self, part: _lvgl.uint32_t) -> _lvgl.grad_dir_t:
        return _lvgl.obj_get_style_bg_grad_dir(self, part)

    def get_style_bg_main_stop(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_bg_main_stop(self, part)

    def get_style_bg_grad_stop(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_bg_grad_stop(self, part)

    def get_style_bg_grad(self, part: _lvgl.uint32_t) -> "grad_dsc_t":
        return _lvgl.obj_get_style_bg_grad(self, part)

    def get_style_bg_dither_mode(self, part: _lvgl.uint32_t) -> _lvgl.dither_mode_t:
        return _lvgl.obj_get_style_bg_dither_mode(self, part)

    def get_style_bg_img_src(self, part: _lvgl.uint32_t) -> Any:
        return _lvgl.obj_get_style_bg_img_src(self, part)

    def get_style_bg_img_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_bg_img_opa(self, part)

    def get_style_bg_img_recolor(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_bg_img_recolor(self, part)

    def get_style_bg_img_recolor_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_bg_img_recolor_filtered(self, part)

    def get_style_bg_img_recolor_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_bg_img_recolor_opa(self, part)

    def get_style_bg_img_tiled(self, part: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_get_style_bg_img_tiled(self, part)

    def get_style_border_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_border_color(self, part)

    def get_style_border_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_border_color_filtered(self, part)

    def get_style_border_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_border_opa(self, part)

    def get_style_border_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_border_width(self, part)

    def get_style_border_side(self, part: _lvgl.uint32_t) -> _lvgl.border_side_t:
        return _lvgl.obj_get_style_border_side(self, part)

    def get_style_border_post(self, part: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_get_style_border_post(self, part)

    def get_style_outline_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_outline_width(self, part)

    def get_style_outline_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_outline_color(self, part)

    def get_style_outline_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_outline_color_filtered(self, part)

    def get_style_outline_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_outline_opa(self, part)

    def get_style_outline_pad(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_outline_pad(self, part)

    def get_style_shadow_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_shadow_width(self, part)

    def get_style_shadow_ofs_x(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_shadow_ofs_x(self, part)

    def get_style_shadow_ofs_y(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_shadow_ofs_y(self, part)

    def get_style_shadow_spread(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_shadow_spread(self, part)

    def get_style_shadow_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_shadow_color(self, part)

    def get_style_shadow_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_shadow_color_filtered(self, part)

    def get_style_shadow_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_shadow_opa(self, part)

    def get_style_img_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_img_opa(self, part)

    def get_style_img_recolor(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_img_recolor(self, part)

    def get_style_img_recolor_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_img_recolor_filtered(self, part)

    def get_style_img_recolor_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_img_recolor_opa(self, part)

    def get_style_line_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_line_width(self, part)

    def get_style_line_dash_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_line_dash_width(self, part)

    def get_style_line_dash_gap(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_line_dash_gap(self, part)

    def get_style_line_rounded(self, part: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_get_style_line_rounded(self, part)

    def get_style_line_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_line_color(self, part)

    def get_style_line_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_line_color_filtered(self, part)

    def get_style_line_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_line_opa(self, part)

    def get_style_arc_width(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_arc_width(self, part)

    def get_style_arc_rounded(self, part: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_get_style_arc_rounded(self, part)

    def get_style_arc_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_arc_color(self, part)

    def get_style_arc_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_arc_color_filtered(self, part)

    def get_style_arc_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_arc_opa(self, part)

    def get_style_arc_img_src(self, part: _lvgl.uint32_t) -> Any:
        return _lvgl.obj_get_style_arc_img_src(self, part)

    def get_style_text_color(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_text_color(self, part)

    def get_style_text_color_filtered(self, part: _lvgl.uint32_t) -> "color_t":
        return _lvgl.obj_get_style_text_color_filtered(self, part)

    def get_style_text_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_text_opa(self, part)

    def get_style_text_font(self, part: _lvgl.uint32_t) -> "font_t":
        return _lvgl.obj_get_style_text_font(self, part)

    def get_style_text_letter_space(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_text_letter_space(self, part)

    def get_style_text_line_space(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_text_line_space(self, part)

    def get_style_text_decor(self, part: _lvgl.uint32_t) -> _lvgl.text_decor_t:
        return _lvgl.obj_get_style_text_decor(self, part)

    def get_style_text_align(self, part: _lvgl.uint32_t) -> _lvgl.text_align_t:
        return _lvgl.obj_get_style_text_align(self, part)

    def get_style_radius(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_radius(self, part)

    def get_style_clip_corner(self, part: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_get_style_clip_corner(self, part)

    def get_style_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_opa(self, part)

    def get_style_color_filter_dsc(self, part: _lvgl.uint32_t) -> "color_filter_dsc_t":
        return _lvgl.obj_get_style_color_filter_dsc(self, part)

    def get_style_color_filter_opa(self, part: _lvgl.uint32_t) -> _lvgl.opa_t:
        return _lvgl.obj_get_style_color_filter_opa(self, part)

    def get_style_anim(self, part: _lvgl.uint32_t) -> "anim_t":
        return _lvgl.obj_get_style_anim(self, part)

    def get_style_anim_time(self, part: _lvgl.uint32_t) -> _lvgl.uint32_t:
        return _lvgl.obj_get_style_anim_time(self, part)

    def get_style_anim_speed(self, part: _lvgl.uint32_t) -> _lvgl.uint32_t:
        return _lvgl.obj_get_style_anim_speed(self, part)

    def get_style_transition(self, part: _lvgl.uint32_t) -> "style_transition_dsc_t":
        return _lvgl.obj_get_style_transition(self, part)

    def get_style_blend_mode(self, part: _lvgl.uint32_t) -> _lvgl.blend_mode_t:
        return _lvgl.obj_get_style_blend_mode(self, part)

    def get_style_layout(self, part: _lvgl.uint32_t) -> _lvgl.uint16_t:
        return _lvgl.obj_get_style_layout(self, part)

    def get_style_base_dir(self, part: _lvgl.uint32_t) -> _lvgl.base_dir_t:
        return _lvgl.obj_get_style_base_dir(self, part)

    def set_style_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_width(self, value, selector)

    def set_style_min_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_min_width(self, value, selector)

    def set_style_max_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_max_width(self, value, selector)

    def set_style_height(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_height(self, value, selector)

    def set_style_min_height(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_min_height(self, value, selector)

    def set_style_max_height(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_max_height(self, value, selector)

    def set_style_x(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_x(self, value, selector)

    def set_style_y(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_y(self, value, selector)

    def set_style_align(self, value: _lvgl.align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_align(self, value, selector)

    def set_style_transform_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transform_width(self, value, selector)

    def set_style_transform_height(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transform_height(self, value, selector)

    def set_style_translate_x(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_translate_x(self, value, selector)

    def set_style_translate_y(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_translate_y(self, value, selector)

    def set_style_transform_zoom(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transform_zoom(self, value, selector)

    def set_style_transform_angle(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transform_angle(self, value, selector)

    def set_style_transform_pivot_x(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transform_pivot_x(self, value, selector)

    def set_style_transform_pivot_y(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transform_pivot_y(self, value, selector)

    def set_style_pad_top(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_top(self, value, selector)

    def set_style_pad_bottom(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_bottom(self, value, selector)

    def set_style_pad_left(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_left(self, value, selector)

    def set_style_pad_right(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_right(self, value, selector)

    def set_style_pad_row(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_row(self, value, selector)

    def set_style_pad_column(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_column(self, value, selector)

    def set_style_margin_top(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_top(self, value, selector)

    def set_style_margin_bottom(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_bottom(self, value, selector)

    def set_style_margin_left(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_left(self, value, selector)

    def set_style_margin_right(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_right(self, value, selector)

    def set_style_bg_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_color(self, value, selector)

    def set_style_bg_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_opa(self, value, selector)

    def set_style_bg_grad_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_grad_color(self, value, selector)

    def set_style_bg_grad_dir(self, value: _lvgl.grad_dir_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_grad_dir(self, value, selector)

    def set_style_bg_main_stop(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_main_stop(self, value, selector)

    def set_style_bg_grad_stop(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_grad_stop(self, value, selector)

    def set_style_bg_grad(self, value: "grad_dsc_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_grad(self, value, selector)

    def set_style_bg_dither_mode(self, value: _lvgl.dither_mode_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_dither_mode(self, value, selector)

    def set_style_bg_img_src(self, value: None, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_img_src(self, value, selector)

    def set_style_bg_img_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_img_opa(self, value, selector)

    def set_style_bg_img_recolor(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_img_recolor(self, value, selector)

    def set_style_bg_img_recolor_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_img_recolor_opa(self, value, selector)

    def set_style_bg_img_tiled(self, value: _lvgl._Bool, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_bg_img_tiled(self, value, selector)

    def set_style_border_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_border_color(self, value, selector)

    def set_style_border_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_border_opa(self, value, selector)

    def set_style_border_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_border_width(self, value, selector)

    def set_style_border_side(self, value: _lvgl.border_side_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_border_side(self, value, selector)

    def set_style_border_post(self, value: _lvgl._Bool, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_border_post(self, value, selector)

    def set_style_outline_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_outline_width(self, value, selector)

    def set_style_outline_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_outline_color(self, value, selector)

    def set_style_outline_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_outline_opa(self, value, selector)

    def set_style_outline_pad(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_outline_pad(self, value, selector)

    def set_style_shadow_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_shadow_width(self, value, selector)

    def set_style_shadow_ofs_x(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_shadow_ofs_x(self, value, selector)

    def set_style_shadow_ofs_y(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_shadow_ofs_y(self, value, selector)

    def set_style_shadow_spread(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_shadow_spread(self, value, selector)

    def set_style_shadow_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_shadow_color(self, value, selector)

    def set_style_shadow_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_shadow_opa(self, value, selector)

    def set_style_img_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_img_opa(self, value, selector)

    def set_style_img_recolor(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_img_recolor(self, value, selector)

    def set_style_img_recolor_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_img_recolor_opa(self, value, selector)

    def set_style_line_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_line_width(self, value, selector)

    def set_style_line_dash_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_line_dash_width(self, value, selector)

    def set_style_line_dash_gap(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_line_dash_gap(self, value, selector)

    def set_style_line_rounded(self, value: _lvgl._Bool, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_line_rounded(self, value, selector)

    def set_style_line_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_line_color(self, value, selector)

    def set_style_line_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_line_opa(self, value, selector)

    def set_style_arc_width(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_arc_width(self, value, selector)

    def set_style_arc_rounded(self, value: _lvgl._Bool, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_arc_rounded(self, value, selector)

    def set_style_arc_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_arc_color(self, value, selector)

    def set_style_arc_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_arc_opa(self, value, selector)

    def set_style_arc_img_src(self, value: None, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_arc_img_src(self, value, selector)

    def set_style_text_color(self, value: "color_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_color(self, value, selector)

    def set_style_text_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_opa(self, value, selector)

    def set_style_text_font(self, value: "font_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_font(self, value, selector)

    def set_style_text_letter_space(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_letter_space(self, value, selector)

    def set_style_text_line_space(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_line_space(self, value, selector)

    def set_style_text_decor(self, value: _lvgl.text_decor_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_decor(self, value, selector)

    def set_style_text_align(self, value: _lvgl.text_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_text_align(self, value, selector)

    def set_style_radius(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_radius(self, value, selector)

    def set_style_clip_corner(self, value: _lvgl._Bool, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_clip_corner(self, value, selector)

    def set_style_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_opa(self, value, selector)

    def set_style_color_filter_dsc(self, value: "color_filter_dsc_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_color_filter_dsc(self, value, selector)

    def set_style_color_filter_opa(self, value: _lvgl.opa_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_color_filter_opa(self, value, selector)

    def set_style_anim(self, value: "anim_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_anim(self, value, selector)

    def set_style_anim_time(self, value: _lvgl.uint32_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_anim_time(self, value, selector)

    def set_style_anim_speed(self, value: _lvgl.uint32_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_anim_speed(self, value, selector)

    def set_style_transition(self, value: "style_transition_dsc_t", selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_transition(self, value, selector)

    def set_style_blend_mode(self, value: _lvgl.blend_mode_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_blend_mode(self, value, selector)

    def set_style_layout(self, value: _lvgl.uint16_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_layout(self, value, selector)

    def set_style_base_dir(self, value: _lvgl.base_dir_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_base_dir(self, value, selector)

    def set_style_pad_all(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_all(self, value, selector)

    def set_style_pad_hor(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_hor(self, value, selector)

    def set_style_pad_ver(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_ver(self, value, selector)

    def set_style_margin_all(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_all(self, value, selector)

    def set_style_margin_hor(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_hor(self, value, selector)

    def set_style_margin_ver(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_margin_ver(self, value, selector)

    def set_style_pad_gap(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_pad_gap(self, value, selector)

    def set_style_size(self, width: _lvgl.coord_t, height: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_size(self, width, height, selector)

    def get_style_space_left(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_space_left(self, part)

    def get_style_space_right(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_space_right(self, part)

    def get_style_space_top(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_space_top(self, part)

    def get_style_space_bottom(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_space_bottom(self, part)

    def calculate_style_text_align(self, part: _lvgl.part_t, txt: _lvgl.char) -> _lvgl.text_align_t:
        return _lvgl.obj_calculate_style_text_align(self, part, txt)

    def get_style_transform_zoom_safe(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_transform_zoom_safe(self, part)

    def init_draw_rect_dsc(self, part: _lvgl.uint32_t, draw_dsc: "draw_rect_dsc_t") -> None:
        return _lvgl.obj_init_draw_rect_dsc(self, part, draw_dsc)

    def init_draw_label_dsc(self, part: _lvgl.uint32_t, draw_dsc: "draw_label_dsc_t") -> None:
        return _lvgl.obj_init_draw_label_dsc(self, part, draw_dsc)

    def init_draw_img_dsc(self, part: _lvgl.uint32_t, draw_dsc: "draw_img_dsc_t") -> None:
        return _lvgl.obj_init_draw_img_dsc(self, part, draw_dsc)

    def init_draw_line_dsc(self, part: _lvgl.uint32_t, draw_dsc: "draw_line_dsc_t") -> None:
        return _lvgl.obj_init_draw_line_dsc(self, part, draw_dsc)

    def init_draw_arc_dsc(self, part: _lvgl.uint32_t, draw_dsc: "draw_arc_dsc_t") -> None:
        return _lvgl.obj_init_draw_arc_dsc(self, part, draw_dsc)

    def calculate_ext_draw_size(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_calculate_ext_draw_size(self, part)

    def refresh_ext_draw_size(self) -> None:
        return _lvgl.obj_refresh_ext_draw_size(self)

    def class_init_obj(self) -> None:
        return _lvgl.obj_class_init_obj(self)

    def is_editable(self) -> _lvgl._Bool:
        return _lvgl.obj_is_editable(self)

    def is_group_def(self) -> _lvgl._Bool:
        return _lvgl.obj_is_group_def(self)

    def send_event(self, event_code: _lvgl.event_code_t, param: None) -> _lvgl.res_t:
        return _lvgl.obj_send_event(self, event_code, param)

    def add_event(self, event_cb: "event_cb_t", filter: _lvgl.event_code_t, user_data: Any) -> None:
        return _lvgl.obj_add_event(self, event_cb, filter, user_data)

    def get_event_count(self) -> _lvgl.uint32_t:
        return _lvgl.obj_get_event_count(self)

    def get_event_dsc(self, index: _lvgl.uint32_t) -> "event_dsc_t":
        return _lvgl.obj_get_event_dsc(self, index)

    def remove_event(self, index: _lvgl.uint32_t) -> _lvgl._Bool:
        return _lvgl.obj_remove_event(self, index)

    def add_flag(self, f: _lvgl.obj_flag_t) -> None:
        return _lvgl.obj_add_flag(self, f)

    def clear_flag(self, f: _lvgl.obj_flag_t) -> None:
        return _lvgl.obj_clear_flag(self, f)

    def add_state(self, state: _lvgl.state_t) -> None:
        return _lvgl.obj_add_state(self, state)

    def clear_state(self, state: _lvgl.state_t) -> None:
        return _lvgl.obj_clear_state(self, state)

    def set_user_data(self, user_data: Any) -> None:
        return _lvgl.obj_set_user_data(self, user_data)

    def has_flag(self, f: _lvgl.obj_flag_t) -> _lvgl._Bool:
        return _lvgl.obj_has_flag(self, f)

    def has_flag_any(self, f: _lvgl.obj_flag_t) -> _lvgl._Bool:
        return _lvgl.obj_has_flag_any(self, f)

    def get_state(self) -> _lvgl.state_t:
        return _lvgl.obj_get_state(self)

    def has_state(self, state: _lvgl.state_t) -> _lvgl._Bool:
        return _lvgl.obj_has_state(self, state)

    def get_group(self) -> "group_t":
        return _lvgl.obj_get_group(self)

    def get_user_data(self) -> Any:
        return _lvgl.obj_get_user_data(self)

    def allocate_spec_attr(self) -> None:
        return _lvgl.obj_allocate_spec_attr(self)

    def check_type(self, class_p: "obj_class_t") -> _lvgl._Bool:
        return _lvgl.obj_check_type(self, class_p)

    def has_class(self, class_p: "obj_class_t") -> _lvgl._Bool:
        return _lvgl.obj_has_class(self, class_p)

    def get_class(self) -> "obj_class_t":
        return _lvgl.obj_get_class(self)

    def is_valid(self) -> _lvgl._Bool:
        return _lvgl.obj_is_valid(self)

    def set_tile(self, tile_obj: "obj", anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_set_tile(self, tile_obj, anim_en)

    def set_tile_id(self, col_id: _lvgl.uint32_t, row_id: _lvgl.uint32_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.obj_set_tile_id(self, col_id, row_id, anim_en)

    def set_flex_flow(self, flow: _lvgl.flex_flow_t) -> None:
        return _lvgl.obj_set_flex_flow(self, flow)

    def set_flex_align(self, main_place: _lvgl.flex_align_t, cross_place: _lvgl.flex_align_t, track_cross_place: _lvgl.flex_align_t) -> None:
        return _lvgl.obj_set_flex_align(self, main_place, cross_place, track_cross_place)

    def set_flex_grow(self, grow: _lvgl.uint8_t) -> None:
        return _lvgl.obj_set_flex_grow(self, grow)

    def set_style_flex_flow(self, value: _lvgl.flex_flow_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_flex_flow(self, value, selector)

    def set_style_flex_main_place(self, value: _lvgl.flex_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_flex_main_place(self, value, selector)

    def set_style_flex_cross_place(self, value: _lvgl.flex_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_flex_cross_place(self, value, selector)

    def set_style_flex_track_place(self, value: _lvgl.flex_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_flex_track_place(self, value, selector)

    def set_style_flex_grow(self, value: _lvgl.uint8_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_flex_grow(self, value, selector)

    def get_style_flex_flow(self, part: _lvgl.uint32_t) -> _lvgl.flex_flow_t:
        return _lvgl.obj_get_style_flex_flow(self, part)

    def get_style_flex_main_place(self, part: _lvgl.uint32_t) -> _lvgl.flex_align_t:
        return _lvgl.obj_get_style_flex_main_place(self, part)

    def get_style_flex_cross_place(self, part: _lvgl.uint32_t) -> _lvgl.flex_align_t:
        return _lvgl.obj_get_style_flex_cross_place(self, part)

    def get_style_flex_track_place(self, part: _lvgl.uint32_t) -> _lvgl.flex_align_t:
        return _lvgl.obj_get_style_flex_track_place(self, part)

    def get_style_flex_grow(self, part: _lvgl.uint32_t) -> _lvgl.uint8_t:
        return _lvgl.obj_get_style_flex_grow(self, part)

    def set_grid_dsc_array(self, col_dsc: List[_lvgl.coord_t], row_dsc: List[_lvgl.coord_t]) -> None:
        return _lvgl.obj_set_grid_dsc_array(self, col_dsc, row_dsc)

    def set_grid_align(self, column_align: _lvgl.grid_align_t, row_align: _lvgl.grid_align_t) -> None:
        return _lvgl.obj_set_grid_align(self, column_align, row_align)

    def set_grid_cell(self, column_align: _lvgl.grid_align_t, col_pos: _lvgl.coord_t, col_span: _lvgl.coord_t, row_align: _lvgl.grid_align_t, row_pos: _lvgl.coord_t, row_span: _lvgl.coord_t) -> None:
        return _lvgl.obj_set_grid_cell(self, column_align, col_pos, col_span, row_align, row_pos, row_span)

    def set_style_grid_row_dsc_array(self, value: List[_lvgl.coord_t], selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_row_dsc_array(self, value, selector)

    def set_style_grid_column_dsc_array(self, value: List[_lvgl.coord_t], selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_column_dsc_array(self, value, selector)

    def set_style_grid_row_align(self, value: _lvgl.grid_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_row_align(self, value, selector)

    def set_style_grid_column_align(self, value: _lvgl.grid_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_column_align(self, value, selector)

    def set_style_grid_cell_column_pos(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_cell_column_pos(self, value, selector)

    def set_style_grid_cell_column_span(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_cell_column_span(self, value, selector)

    def set_style_grid_cell_row_pos(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_cell_row_pos(self, value, selector)

    def set_style_grid_cell_row_span(self, value: _lvgl.coord_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_cell_row_span(self, value, selector)

    def set_style_grid_cell_x_align(self, value: _lvgl.grid_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_cell_x_align(self, value, selector)

    def set_style_grid_cell_y_align(self, value: _lvgl.grid_align_t, selector: _lvgl.style_selector_t) -> None:
        return _lvgl.obj_set_style_grid_cell_y_align(self, value, selector)

    def get_style_grid_row_dsc_array(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_grid_row_dsc_array(self, part)

    def get_style_grid_column_dsc_array(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_grid_column_dsc_array(self, part)

    def get_style_grid_row_align(self, part: _lvgl.uint32_t) -> _lvgl.grid_align_t:
        return _lvgl.obj_get_style_grid_row_align(self, part)

    def get_style_grid_column_align(self, part: _lvgl.uint32_t) -> _lvgl.grid_align_t:
        return _lvgl.obj_get_style_grid_column_align(self, part)

    def get_style_grid_cell_column_pos(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_grid_cell_column_pos(self, part)

    def get_style_grid_cell_column_span(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_grid_cell_column_span(self, part)

    def get_style_grid_cell_row_pos(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_grid_cell_row_pos(self, part)

    def get_style_grid_cell_row_span(self, part: _lvgl.uint32_t) -> _lvgl.coord_t:
        return _lvgl.obj_get_style_grid_cell_row_span(self, part)

    def get_style_grid_cell_x_align(self, part: _lvgl.uint32_t) -> _lvgl.grid_align_t:
        return _lvgl.obj_get_style_grid_cell_x_align(self, part)

    def get_style_grid_cell_y_align(self, part: _lvgl.uint32_t) -> _lvgl.grid_align_t:
        return _lvgl.obj_get_style_grid_cell_y_align(self, part)

    def move_foreground(self) -> None:
        return _lvgl.obj_move_foreground(self)

    def move_background(self) -> None:
        return _lvgl.obj_move_background(self)

    def get_child_id(self) -> _lvgl.uint32_t:
        return _lvgl.obj_get_child_id(self)


class img(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.img_create(parent)
            cls.cast(self)
   
    def set_src(self, src: None) -> None:
        return _lvgl.img_set_src(self, src)

    def set_offset_x(self, x: _lvgl.coord_t) -> None:
        return _lvgl.img_set_offset_x(self, x)

    def set_offset_y(self, y: _lvgl.coord_t) -> None:
        return _lvgl.img_set_offset_y(self, y)

    def set_angle(self, angle: _lvgl.int16_t) -> None:
        return _lvgl.img_set_angle(self, angle)

    def set_pivot(self, x: _lvgl.coord_t, y: _lvgl.coord_t) -> None:
        return _lvgl.img_set_pivot(self, x, y)

    def set_zoom(self, zoom: _lvgl.uint16_t) -> None:
        return _lvgl.img_set_zoom(self, zoom)

    def set_antialias(self, antialias: _lvgl._Bool) -> None:
        return _lvgl.img_set_antialias(self, antialias)

    def set_size_mode(self, mode: _lvgl.img_size_mode_t) -> None:
        return _lvgl.img_set_size_mode(self, mode)

    def get_src(self) -> Any:
        return _lvgl.img_get_src(self)

    def get_offset_x(self) -> _lvgl.coord_t:
        return _lvgl.img_get_offset_x(self)

    def get_offset_y(self) -> _lvgl.coord_t:
        return _lvgl.img_get_offset_y(self)

    def get_angle(self) -> _lvgl.uint16_t:
        return _lvgl.img_get_angle(self)

    def get_pivot(self, pivot: _lvgl.point_t) -> None:
        return _lvgl.img_get_pivot(self, pivot)

    def get_zoom(self) -> _lvgl.uint16_t:
        return _lvgl.img_get_zoom(self)

    def get_antialias(self) -> _lvgl._Bool:
        return _lvgl.img_get_antialias(self)

    def get_size_mode(self) -> _lvgl.img_size_mode_t:
        return _lvgl.img_get_size_mode(self)


class animimg(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.animimg_create(parent)
            cls.cast(self)
   
    def set_src(self, dsc: List[_lvgl.void], num: _lvgl.uint8_t) -> None:
        return _lvgl.animimg_set_src(self, dsc, num)

    def start(self) -> None:
        return _lvgl.animimg_start(self)

    def set_duration(self, duration: _lvgl.uint32_t) -> None:
        return _lvgl.animimg_set_duration(self, duration)

    def set_repeat_count(self, count: _lvgl.uint16_t) -> None:
        return _lvgl.animimg_set_repeat_count(self, count)

    def get_src(self) -> Any:
        return _lvgl.animimg_get_src(self)

    def get_src_count(self) -> _lvgl.uint8_t:
        return _lvgl.animimg_get_src_count(self)

    def get_duration(self) -> _lvgl.uint32_t:
        return _lvgl.animimg_get_duration(self)

    def get_repeat_count(self) -> _lvgl.uint16_t:
        return _lvgl.animimg_get_repeat_count(self)


class arc(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.arc_create(parent)
            cls.cast(self)
   
    def set_start_angle(self, start: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_start_angle(self, start)

    def set_end_angle(self, end: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_end_angle(self, end)

    def set_angles(self, start: _lvgl.uint16_t, end: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_angles(self, start, end)

    def set_bg_start_angle(self, start: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_bg_start_angle(self, start)

    def set_bg_end_angle(self, end: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_bg_end_angle(self, end)

    def set_bg_angles(self, start: _lvgl.uint16_t, end: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_bg_angles(self, start, end)

    def set_rotation(self, rotation: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_rotation(self, rotation)

    def set_mode(self, type: _lvgl.arc_mode_t) -> None:
        return _lvgl.arc_set_mode(self, type)

    def set_value(self, value: _lvgl.int16_t) -> None:
        return _lvgl.arc_set_value(self, value)

    def set_range(self, min: _lvgl.int16_t, max: _lvgl.int16_t) -> None:
        return _lvgl.arc_set_range(self, min, max)

    def set_change_rate(self, rate: _lvgl.uint16_t) -> None:
        return _lvgl.arc_set_change_rate(self, rate)

    def set_knob_offset(self, offset: _lvgl.int16_t) -> None:
        return _lvgl.arc_set_knob_offset(self, offset)

    def get_angle_start(self) -> _lvgl.uint16_t:
        return _lvgl.arc_get_angle_start(self)

    def get_angle_end(self) -> _lvgl.uint16_t:
        return _lvgl.arc_get_angle_end(self)

    def get_bg_angle_start(self) -> _lvgl.uint16_t:
        return _lvgl.arc_get_bg_angle_start(self)

    def get_bg_angle_end(self) -> _lvgl.uint16_t:
        return _lvgl.arc_get_bg_angle_end(self)

    def get_value(self) -> _lvgl.int16_t:
        return _lvgl.arc_get_value(self)

    def get_min_value(self) -> _lvgl.int16_t:
        return _lvgl.arc_get_min_value(self)

    def get_max_value(self) -> _lvgl.int16_t:
        return _lvgl.arc_get_max_value(self)

    def get_mode(self) -> _lvgl.arc_mode_t:
        return _lvgl.arc_get_mode(self)

    def get_rotation(self) -> _lvgl.int16_t:
        return _lvgl.arc_get_rotation(self)

    def get_knob_offset(self) -> _lvgl.int16_t:
        return _lvgl.arc_get_knob_offset(self)

    def align_obj_to_angle(self, obj_to_align: "obj", r_offset: _lvgl.coord_t) -> None:
        return _lvgl.arc_align_obj_to_angle(self, obj_to_align, r_offset)

    def rotate_obj_to_angle(self, obj_to_rotate: "obj", r_offset: _lvgl.coord_t) -> None:
        return _lvgl.arc_rotate_obj_to_angle(self, obj_to_rotate, r_offset)


class label(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.label_create(parent)
            cls.cast(self)
   
    def set_text(self, text: _lvgl.char) -> None:
        return _lvgl.label_set_text(self, text)

    def set_text_fmt(self, fmt: _lvgl.char, *args) -> None:
        return _lvgl.label_set_text_fmt(self, fmt, *args)

    def set_text_static(self, text: _lvgl.char) -> None:
        return _lvgl.label_set_text_static(self, text)

    def set_long_mode(self, long_mode: _lvgl.label_long_mode_t) -> None:
        return _lvgl.label_set_long_mode(self, long_mode)

    def set_recolor(self, en: _lvgl._Bool) -> None:
        return _lvgl.label_set_recolor(self, en)

    def set_text_selection_start(self, index: _lvgl.uint32_t) -> None:
        return _lvgl.label_set_text_selection_start(self, index)

    def set_text_selection_end(self, index: _lvgl.uint32_t) -> None:
        return _lvgl.label_set_text_selection_end(self, index)

    def get_text(self) -> _lvgl.char:
        return _lvgl.label_get_text(self)

    def get_long_mode(self) -> _lvgl.label_long_mode_t:
        return _lvgl.label_get_long_mode(self)

    def get_recolor(self) -> _lvgl._Bool:
        return _lvgl.label_get_recolor(self)

    def get_letter_pos(self, char_id: _lvgl.uint32_t, pos: _lvgl.point_t) -> None:
        return _lvgl.label_get_letter_pos(self, char_id, pos)

    def get_letter_on(self, pos_in: _lvgl.point_t) -> _lvgl.uint32_t:
        return _lvgl.label_get_letter_on(self, pos_in)

    def is_char_under_pos(self, pos: _lvgl.point_t) -> _lvgl._Bool:
        return _lvgl.label_is_char_under_pos(self, pos)

    def get_text_selection_start(self) -> _lvgl.uint32_t:
        return _lvgl.label_get_text_selection_start(self)

    def get_text_selection_end(self) -> _lvgl.uint32_t:
        return _lvgl.label_get_text_selection_end(self)

    def ins_text(self, pos: _lvgl.uint32_t, txt: _lvgl.char) -> None:
        return _lvgl.label_ins_text(self, pos, txt)

    def cut_text(self, pos: _lvgl.uint32_t, cnt: _lvgl.uint32_t) -> None:
        return _lvgl.label_cut_text(self, pos, cnt)


class bar(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.bar_create(parent)
            cls.cast(self)
   
    def set_value(self, value: _lvgl.int32_t, anim: _lvgl.anim_enable_t) -> None:
        return _lvgl.bar_set_value(self, value, anim)

    def set_start_value(self, start_value: _lvgl.int32_t, anim: _lvgl.anim_enable_t) -> None:
        return _lvgl.bar_set_start_value(self, start_value, anim)

    def set_range(self, min: _lvgl.int32_t, max: _lvgl.int32_t) -> None:
        return _lvgl.bar_set_range(self, min, max)

    def set_mode(self, mode: _lvgl.bar_mode_t) -> None:
        return _lvgl.bar_set_mode(self, mode)

    def get_value(self) -> _lvgl.int32_t:
        return _lvgl.bar_get_value(self)

    def get_start_value(self) -> _lvgl.int32_t:
        return _lvgl.bar_get_start_value(self)

    def get_min_value(self) -> _lvgl.int32_t:
        return _lvgl.bar_get_min_value(self)

    def get_max_value(self) -> _lvgl.int32_t:
        return _lvgl.bar_get_max_value(self)

    def get_mode(self) -> _lvgl.bar_mode_t:
        return _lvgl.bar_get_mode(self)


class btn(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.btn_create(parent)
            cls.cast(self)
   


class btnmatrix(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.btnmatrix_create(parent)
            cls.cast(self)
   
    def set_map(self, map: List[_lvgl.char]) -> None:
        return _lvgl.btnmatrix_set_map(self, map)

    def set_ctrl_map(self, ctrl_map: List[_lvgl.btnmatrix_ctrl_t]) -> None:
        return _lvgl.btnmatrix_set_ctrl_map(self, ctrl_map)

    def set_selected_btn(self, btn_id: _lvgl.uint16_t) -> None:
        return _lvgl.btnmatrix_set_selected_btn(self, btn_id)

    def set_btn_ctrl(self, btn_id: _lvgl.uint16_t, ctrl: _lvgl.btnmatrix_ctrl_t) -> None:
        return _lvgl.btnmatrix_set_btn_ctrl(self, btn_id, ctrl)

    def clear_btn_ctrl(self, btn_id: _lvgl.uint16_t, ctrl: _lvgl.btnmatrix_ctrl_t) -> None:
        return _lvgl.btnmatrix_clear_btn_ctrl(self, btn_id, ctrl)

    def set_btn_ctrl_all(self, ctrl: _lvgl.btnmatrix_ctrl_t) -> None:
        return _lvgl.btnmatrix_set_btn_ctrl_all(self, ctrl)

    def clear_btn_ctrl_all(self, ctrl: _lvgl.btnmatrix_ctrl_t) -> None:
        return _lvgl.btnmatrix_clear_btn_ctrl_all(self, ctrl)

    def set_btn_width(self, btn_id: _lvgl.uint16_t, width: _lvgl.uint8_t) -> None:
        return _lvgl.btnmatrix_set_btn_width(self, btn_id, width)

    def set_one_checked(self, en: _lvgl._Bool) -> None:
        return _lvgl.btnmatrix_set_one_checked(self, en)

    def get_map(self) -> _lvgl.char:
        return _lvgl.btnmatrix_get_map(self)

    def get_selected_btn(self) -> _lvgl.uint16_t:
        return _lvgl.btnmatrix_get_selected_btn(self)

    def get_btn_text(self, btn_id: _lvgl.uint16_t) -> _lvgl.char:
        return _lvgl.btnmatrix_get_btn_text(self, btn_id)

    def has_btn_ctrl(self, btn_id: _lvgl.uint16_t, ctrl: _lvgl.btnmatrix_ctrl_t) -> _lvgl._Bool:
        return _lvgl.btnmatrix_has_btn_ctrl(self, btn_id, ctrl)

    def get_one_checked(self) -> _lvgl._Bool:
        return _lvgl.btnmatrix_get_one_checked(self)

    def get_popovers(self) -> _lvgl._Bool:
        return _lvgl.btnmatrix_get_popovers(self)


class calendar(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.calendar_create(parent)
            cls.cast(self)
   
    def set_today_date(self, year: _lvgl.uint32_t, month: _lvgl.uint32_t, day: _lvgl.uint32_t) -> None:
        return _lvgl.calendar_set_today_date(self, year, month, day)

    def set_showed_date(self, year: _lvgl.uint32_t, month: _lvgl.uint32_t) -> None:
        return _lvgl.calendar_set_showed_date(self, year, month)

    def set_highlighted_dates(self, highlighted: List["calendar_date_t"], date_num: _lvgl.uint16_t) -> None:
        return _lvgl.calendar_set_highlighted_dates(self, highlighted, date_num)

    def set_day_names(self, day_names: _lvgl.char) -> None:
        return _lvgl.calendar_set_day_names(self, day_names)

    def get_btnmatrix(self) -> "obj":
        return _lvgl.calendar_get_btnmatrix(self)

    def get_today_date(self) -> "calendar_date_t":
        return _lvgl.calendar_get_today_date(self)

    def get_showed_date(self) -> "calendar_date_t":
        return _lvgl.calendar_get_showed_date(self)

    def get_highlighted_dates(self) -> "calendar_date_t":
        return _lvgl.calendar_get_highlighted_dates(self)

    def get_highlighted_dates_num(self) -> _lvgl.uint16_t:
        return _lvgl.calendar_get_highlighted_dates_num(self)

    def get_pressed_date(self, date: "calendar_date_t") -> _lvgl.res_t:
        return _lvgl.calendar_get_pressed_date(self, date)


class calendar_header_arrow(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.calendar_header_arrow_create(parent)
            cls.cast(self)
   


class calendar_header_dropdown(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.calendar_header_dropdown_create(parent)
            cls.cast(self)
   


class canvas(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.canvas_create(parent)
            cls.cast(self)
   
    def set_buffer(self, buf: None, w: _lvgl.coord_t, h: _lvgl.coord_t, cf: _lvgl.color_format_t) -> None:
        return _lvgl.canvas_set_buffer(self, buf, w, h, cf)

    def set_px(self, x: _lvgl.coord_t, y: _lvgl.coord_t, color: "color_t", opa: _lvgl.opa_t) -> None:
        return _lvgl.canvas_set_px(self, x, y, color, opa)

    def set_palette(self, id: _lvgl.uint8_t, c: "color32_t") -> None:
        return _lvgl.canvas_set_palette(self, id, c)

    def get_px(self, x: _lvgl.coord_t, y: _lvgl.coord_t, color: "color_t", opa: _lvgl.opa_t) -> None:
        return _lvgl.canvas_get_px(self, x, y, color, opa)

    def get_img(self) -> "img_dsc_t":
        return _lvgl.canvas_get_img(self)

    def copy_buf(self, to_copy: None, x: _lvgl.coord_t, y: _lvgl.coord_t, w: _lvgl.coord_t, h: _lvgl.coord_t) -> None:
        return _lvgl.canvas_copy_buf(self, to_copy, x, y, w, h)

    def transform(self, img: "img_dsc_t", angle: _lvgl.int16_t, zoom: _lvgl.uint16_t, offset_x: _lvgl.coord_t, offset_y: _lvgl.coord_t, pivot_x: _lvgl.int32_t, pivot_y: _lvgl.int32_t, antialias: _lvgl._Bool) -> None:
        return _lvgl.canvas_transform(self, img, angle, zoom, offset_x, offset_y, pivot_x, pivot_y, antialias)

    def blur_hor(self, area: "area_t", r: _lvgl.uint16_t) -> None:
        return _lvgl.canvas_blur_hor(self, area, r)

    def blur_ver(self, area: "area_t", r: _lvgl.uint16_t) -> None:
        return _lvgl.canvas_blur_ver(self, area, r)

    def fill_bg(self, color: "color_t", opa: _lvgl.opa_t) -> None:
        return _lvgl.canvas_fill_bg(self, color, opa)

    def draw_rect(self, x: _lvgl.coord_t, y: _lvgl.coord_t, w: _lvgl.coord_t, h: _lvgl.coord_t, draw_dsc: "draw_rect_dsc_t") -> None:
        return _lvgl.canvas_draw_rect(self, x, y, w, h, draw_dsc)

    def draw_text(self, x: _lvgl.coord_t, y: _lvgl.coord_t, max_w: _lvgl.coord_t, draw_dsc: "draw_label_dsc_t", txt: _lvgl.char) -> None:
        return _lvgl.canvas_draw_text(self, x, y, max_w, draw_dsc, txt)

    def draw_img(self, x: _lvgl.coord_t, y: _lvgl.coord_t, src: None, draw_dsc: "draw_img_dsc_t") -> None:
        return _lvgl.canvas_draw_img(self, x, y, src, draw_dsc)

    def draw_line(self, points: List[_lvgl.point_t], point_cnt: _lvgl.uint32_t, draw_dsc: "draw_line_dsc_t") -> None:
        return _lvgl.canvas_draw_line(self, points, point_cnt, draw_dsc)

    def draw_polygon(self, points: List[_lvgl.point_t], point_cnt: _lvgl.uint32_t, draw_dsc: "draw_rect_dsc_t") -> None:
        return _lvgl.canvas_draw_polygon(self, points, point_cnt, draw_dsc)

    def draw_arc(self, x: _lvgl.coord_t, y: _lvgl.coord_t, r: _lvgl.coord_t, start_angle: _lvgl.int32_t, end_angle: _lvgl.int32_t, draw_dsc: "draw_arc_dsc_t") -> None:
        return _lvgl.canvas_draw_arc(self, x, y, r, start_angle, end_angle, draw_dsc)


class chart(obj):
    
    class AXIS_PRIMARY:
        X = _lvgl.CHART_AXIS_PRIMARY_X
        Y = _lvgl.CHART_AXIS_PRIMARY_Y
    
    class AXIS_SECONDARY:
        X = _lvgl.CHART_AXIS_SECONDARY_X
        Y = _lvgl.CHART_AXIS_SECONDARY_Y

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.chart_create(parent)
            cls.cast(self)
   
    def set_type(self, type: _lvgl.chart_type_t) -> None:
        return _lvgl.chart_set_type(self, type)

    def set_point_count(self, cnt: _lvgl.uint16_t) -> None:
        return _lvgl.chart_set_point_count(self, cnt)

    def set_range(self, axis: _lvgl.chart_axis_t, min: _lvgl.coord_t, max: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_range(self, axis, min, max)

    def set_update_mode(self, update_mode: _lvgl.chart_update_mode_t) -> None:
        return _lvgl.chart_set_update_mode(self, update_mode)

    def set_div_line_count(self, hdiv: _lvgl.uint8_t, vdiv: _lvgl.uint8_t) -> None:
        return _lvgl.chart_set_div_line_count(self, hdiv, vdiv)

    def set_zoom_x(self, zoom_x: _lvgl.uint16_t) -> None:
        return _lvgl.chart_set_zoom_x(self, zoom_x)

    def set_zoom_y(self, zoom_y: _lvgl.uint16_t) -> None:
        return _lvgl.chart_set_zoom_y(self, zoom_y)

    def get_zoom_x(self) -> _lvgl.uint16_t:
        return _lvgl.chart_get_zoom_x(self)

    def get_zoom_y(self) -> _lvgl.uint16_t:
        return _lvgl.chart_get_zoom_y(self)

    def set_axis_tick(self, axis: _lvgl.chart_axis_t, major_len: _lvgl.coord_t, minor_len: _lvgl.coord_t, major_cnt: _lvgl.coord_t, minor_cnt: _lvgl.coord_t, label_en: _lvgl._Bool, draw_size: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_axis_tick(self, axis, major_len, minor_len, major_cnt, minor_cnt, label_en, draw_size)

    def get_type(self) -> _lvgl.chart_type_t:
        return _lvgl.chart_get_type(self)

    def get_point_count(self) -> _lvgl.uint16_t:
        return _lvgl.chart_get_point_count(self)

    def get_x_start_point(self, ser: _lvgl.chart_series_t) -> _lvgl.uint16_t:
        return _lvgl.chart_get_x_start_point(self, ser)

    def get_point_pos_by_id(self, ser: _lvgl.chart_series_t, id: _lvgl.uint16_t, p_out: _lvgl.point_t) -> None:
        return _lvgl.chart_get_point_pos_by_id(self, ser, id, p_out)

    def refresh(self) -> None:
        return _lvgl.chart_refresh(self)

    def add_series(self, color: "color_t", axis: _lvgl.chart_axis_t) -> _lvgl.chart_series_t:
        return _lvgl.chart_add_series(self, color, axis)

    def remove_series(self, series: _lvgl.chart_series_t) -> None:
        return _lvgl.chart_remove_series(self, series)

    def hide_series(self, series: _lvgl.chart_series_t, hide: _lvgl._Bool) -> None:
        return _lvgl.chart_hide_series(self, series, hide)

    def set_series_color(self, series: _lvgl.chart_series_t, color: "color_t") -> None:
        return _lvgl.chart_set_series_color(self, series, color)

    def set_x_start_point(self, ser: _lvgl.chart_series_t, id: _lvgl.uint16_t) -> None:
        return _lvgl.chart_set_x_start_point(self, ser, id)

    def get_series_next(self, ser: _lvgl.chart_series_t) -> _lvgl.chart_series_t:
        return _lvgl.chart_get_series_next(self, ser)

    def add_cursor(self, color: "color_t", dir: _lvgl.dir_t) -> _lvgl.chart_cursor_t:
        return _lvgl.chart_add_cursor(self, color, dir)

    def set_cursor_pos(self, cursor: _lvgl.chart_cursor_t, pos: _lvgl.point_t) -> None:
        return _lvgl.chart_set_cursor_pos(self, cursor, pos)

    def set_cursor_point(self, cursor: _lvgl.chart_cursor_t, ser: _lvgl.chart_series_t, point_id: _lvgl.uint16_t) -> None:
        return _lvgl.chart_set_cursor_point(self, cursor, ser, point_id)

    def get_cursor_point(self, cursor: _lvgl.chart_cursor_t) -> _lvgl.point_t:
        return _lvgl.chart_get_cursor_point(self, cursor)

    def set_all_value(self, ser: _lvgl.chart_series_t, value: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_all_value(self, ser, value)

    def set_next_value(self, ser: _lvgl.chart_series_t, value: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_next_value(self, ser, value)

    def set_next_value2(self, ser: _lvgl.chart_series_t, x_value: _lvgl.coord_t, y_value: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_next_value2(self, ser, x_value, y_value)

    def set_value_by_id(self, ser: _lvgl.chart_series_t, id: _lvgl.uint16_t, value: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_value_by_id(self, ser, id, value)

    def set_value_by_id2(self, ser: _lvgl.chart_series_t, id: _lvgl.uint16_t, x_value: _lvgl.coord_t, y_value: _lvgl.coord_t) -> None:
        return _lvgl.chart_set_value_by_id2(self, ser, id, x_value, y_value)

    def set_ext_y_array(self, ser: _lvgl.chart_series_t, array: List[_lvgl.coord_t]) -> None:
        return _lvgl.chart_set_ext_y_array(self, ser, array)

    def set_ext_x_array(self, ser: _lvgl.chart_series_t, array: List[_lvgl.coord_t]) -> None:
        return _lvgl.chart_set_ext_x_array(self, ser, array)

    def get_y_array(self, ser: _lvgl.chart_series_t) -> _lvgl.coord_t:
        return _lvgl.chart_get_y_array(self, ser)

    def get_x_array(self, ser: _lvgl.chart_series_t) -> _lvgl.coord_t:
        return _lvgl.chart_get_x_array(self, ser)

    def get_pressed_point(self) -> _lvgl.uint32_t:
        return _lvgl.chart_get_pressed_point(self)


class checkbox(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.checkbox_create(parent)
            cls.cast(self)
   
    def set_text(self, txt: _lvgl.char) -> None:
        return _lvgl.checkbox_set_text(self, txt)

    def set_text_static(self, txt: _lvgl.char) -> None:
        return _lvgl.checkbox_set_text_static(self, txt)

    def get_text(self) -> _lvgl.char:
        return _lvgl.checkbox_get_text(self)


class colorwheel(obj):

    def __init__(self, parent: _lvgl.obj_t, knob_recolor: _lvgl._Bool):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent, knob_recolor,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.colorwheel_create(parent, knob_recolor)
            cls.cast(self)
   
    def set_hsv(self, hsv: "color_hsv_t") -> _lvgl._Bool:
        return _lvgl.colorwheel_set_hsv(self, hsv)

    def set_rgb(self, color: "color_t") -> _lvgl._Bool:
        return _lvgl.colorwheel_set_rgb(self, color)

    def set_mode(self, mode: _lvgl.colorwheel_mode_t) -> None:
        return _lvgl.colorwheel_set_mode(self, mode)

    def set_mode_fixed(self, fixed: _lvgl._Bool) -> None:
        return _lvgl.colorwheel_set_mode_fixed(self, fixed)

    def get_hsv(self) -> "color_hsv_t":
        return _lvgl.colorwheel_get_hsv(self)

    def get_rgb(self) -> "color_t":
        return _lvgl.colorwheel_get_rgb(self)

    def get_color_mode(self) -> _lvgl.colorwheel_mode_t:
        return _lvgl.colorwheel_get_color_mode(self)

    def get_color_mode_fixed(self) -> _lvgl._Bool:
        return _lvgl.colorwheel_get_color_mode_fixed(self)


class dropdown(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.dropdown_create(parent)
            cls.cast(self)
   
    def set_text(self, txt: _lvgl.char) -> None:
        return _lvgl.dropdown_set_text(self, txt)

    def set_options(self, options: _lvgl.char) -> None:
        return _lvgl.dropdown_set_options(self, options)

    def set_options_static(self, options: _lvgl.char) -> None:
        return _lvgl.dropdown_set_options_static(self, options)

    def add_option(self, option: _lvgl.char, pos: _lvgl.uint32_t) -> None:
        return _lvgl.dropdown_add_option(self, option, pos)

    def clear_options(self) -> None:
        return _lvgl.dropdown_clear_options(self)

    def set_selected(self, sel_opt: _lvgl.uint16_t) -> None:
        return _lvgl.dropdown_set_selected(self, sel_opt)

    def set_dir(self, dir: _lvgl.dir_t) -> None:
        return _lvgl.dropdown_set_dir(self, dir)

    def set_symbol(self, symbol: None) -> None:
        return _lvgl.dropdown_set_symbol(self, symbol)

    def set_selected_highlight(self, en: _lvgl._Bool) -> None:
        return _lvgl.dropdown_set_selected_highlight(self, en)

    def get_list(self) -> "obj":
        return _lvgl.dropdown_get_list(self)

    def get_text(self) -> _lvgl.char:
        return _lvgl.dropdown_get_text(self)

    def get_options(self) -> _lvgl.char:
        return _lvgl.dropdown_get_options(self)

    def get_selected(self) -> _lvgl.uint16_t:
        return _lvgl.dropdown_get_selected(self)

    def get_option_cnt(self) -> _lvgl.uint16_t:
        return _lvgl.dropdown_get_option_cnt(self)

    def get_selected_str(self, buf: _lvgl.char, buf_size: _lvgl.uint32_t) -> None:
        return _lvgl.dropdown_get_selected_str(self, buf, buf_size)

    def get_option_index(self, option: _lvgl.char) -> _lvgl.int32_t:
        return _lvgl.dropdown_get_option_index(self, option)

    def get_symbol(self) -> _lvgl.char:
        return _lvgl.dropdown_get_symbol(self)

    def get_selected_highlight(self) -> _lvgl._Bool:
        return _lvgl.dropdown_get_selected_highlight(self)

    def get_dir(self) -> _lvgl.dir_t:
        return _lvgl.dropdown_get_dir(self)

    def open(self) -> None:
        return _lvgl.dropdown_open(self)

    def close(self) -> None:
        return _lvgl.dropdown_close(self)

    def is_open(self) -> _lvgl._Bool:
        return _lvgl.dropdown_is_open(self)


class imgbtn(obj):
    
    class STATE:
        CHECKED_DISABLED = _lvgl.IMGBTN_STATE_CHECKED_DISABLED
        CHECKED_PRESSED = _lvgl.IMGBTN_STATE_CHECKED_PRESSED
        CHECKED_RELEASED = _lvgl.IMGBTN_STATE_CHECKED_RELEASED
        DISABLED = _lvgl.IMGBTN_STATE_DISABLED
        PRESSED = _lvgl.IMGBTN_STATE_PRESSED
        RELEASED = _lvgl.IMGBTN_STATE_RELEASED

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.imgbtn_create(parent)
            cls.cast(self)
   
    def set_src(self, state: _lvgl.imgbtn_state_t, src_left: None, src_mid: None, src_right: None) -> None:
        return _lvgl.imgbtn_set_src(self, state, src_left, src_mid, src_right)

    def set_state(self, state: _lvgl.imgbtn_state_t) -> None:
        return _lvgl.imgbtn_set_state(self, state)

    def get_src_left(self, state: _lvgl.imgbtn_state_t) -> Any:
        return _lvgl.imgbtn_get_src_left(self, state)

    def get_src_middle(self, state: _lvgl.imgbtn_state_t) -> Any:
        return _lvgl.imgbtn_get_src_middle(self, state)

    def get_src_right(self, state: _lvgl.imgbtn_state_t) -> Any:
        return _lvgl.imgbtn_get_src_right(self, state)


class keyboard(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.keyboard_create(parent)
            cls.cast(self)
   
    def set_textarea(self, ta: "obj") -> None:
        return _lvgl.keyboard_set_textarea(self, ta)

    def set_mode(self, mode: _lvgl.keyboard_mode_t) -> None:
        return _lvgl.keyboard_set_mode(self, mode)

    def set_popovers(self, en: _lvgl._Bool) -> None:
        return _lvgl.keyboard_set_popovers(self, en)

    def set_map(self, mode: _lvgl.keyboard_mode_t, map: List[_lvgl.char], ctrl_map: List[_lvgl.btnmatrix_ctrl_t]) -> None:
        return _lvgl.keyboard_set_map(self, mode, map, ctrl_map)

    def get_textarea(self) -> "obj":
        return _lvgl.keyboard_get_textarea(self)

    def get_mode(self) -> _lvgl.keyboard_mode_t:
        return _lvgl.keyboard_get_mode(self)

    def get_map_array(self) -> _lvgl.char:
        return _lvgl.keyboard_get_map_array(self)

    def get_selected_btn(self) -> _lvgl.uint16_t:
        return _lvgl.keyboard_get_selected_btn(self)

    def get_btn_text(self, btn_id: _lvgl.uint16_t) -> _lvgl.char:
        return _lvgl.keyboard_get_btn_text(self, btn_id)


class led(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.led_create(parent)
            cls.cast(self)
   
    def set_color(self, color: "color_t") -> None:
        return _lvgl.led_set_color(self, color)

    def set_brightness(self, bright: _lvgl.uint8_t) -> None:
        return _lvgl.led_set_brightness(self, bright)

    def on(self) -> None:
        return _lvgl.led_on(self)

    def off(self) -> None:
        return _lvgl.led_off(self)

    def toggle(self) -> None:
        return _lvgl.led_toggle(self)

    def get_brightness(self) -> _lvgl.uint8_t:
        return _lvgl.led_get_brightness(self)


class line(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.line_create(parent)
            cls.cast(self)
   
    def set_points(self, points: List[_lvgl.point_t], point_num: _lvgl.uint16_t) -> None:
        return _lvgl.line_set_points(self, points, point_num)

    def set_y_invert(self, en: _lvgl._Bool) -> None:
        return _lvgl.line_set_y_invert(self, en)

    def get_y_invert(self) -> _lvgl._Bool:
        return _lvgl.line_get_y_invert(self)


class list(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.list_create(parent)
            cls.cast(self)
   
    def add_text(self, txt: _lvgl.char) -> "obj":
        return _lvgl.list_add_text(self, txt)

    def add_btn(self, icon: None, txt: _lvgl.char) -> "obj":
        return _lvgl.list_add_btn(self, icon, txt)

    def get_btn_text(self, btn: "obj") -> _lvgl.char:
        return _lvgl.list_get_btn_text(self, btn)

    def set_btn_text(self, btn: "obj", txt: _lvgl.char) -> None:
        return _lvgl.list_set_btn_text(self, btn, txt)


class menu(obj):
    
    class ROOT_BACK_BTN:
        DISABLED = _lvgl.MENU_ROOT_BACK_BTN_DISABLED
        ENABLED = _lvgl.MENU_ROOT_BACK_BTN_ENABLED

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.menu_create(parent)
            cls.cast(self)
   
    def set_page(self, page: "obj") -> None:
        return _lvgl.menu_set_page(self, page)

    def set_page_title(self, title: _lvgl.char) -> None:
        return _lvgl.menu_set_page_title(self, title)

    def set_page_title_static(self, title: _lvgl.char) -> None:
        return _lvgl.menu_set_page_title_static(self, title)

    def set_sidebar_page(self, page: "obj") -> None:
        return _lvgl.menu_set_sidebar_page(self, page)

    def set_mode_header(self, mode_header: _lvgl.menu_mode_header_t) -> None:
        return _lvgl.menu_set_mode_header(self, mode_header)

    def set_mode_root_back_btn(self, mode_root_back_btn: _lvgl.menu_mode_root_back_btn_t) -> None:
        return _lvgl.menu_set_mode_root_back_btn(self, mode_root_back_btn)

    def set_load_page_event(self, obj: "obj", page: "obj") -> None:
        return _lvgl.menu_set_load_page_event(self, obj, page)

    def get_cur_main_page(self) -> "obj":
        return _lvgl.menu_get_cur_main_page(self)

    def get_cur_sidebar_page(self) -> "obj":
        return _lvgl.menu_get_cur_sidebar_page(self)

    def get_main_header(self) -> "obj":
        return _lvgl.menu_get_main_header(self)

    def get_main_header_back_btn(self) -> "obj":
        return _lvgl.menu_get_main_header_back_btn(self)

    def get_sidebar_header(self) -> "obj":
        return _lvgl.menu_get_sidebar_header(self)

    def get_sidebar_header_back_btn(self) -> "obj":
        return _lvgl.menu_get_sidebar_header_back_btn(self)

    def back_btn_is_root(self, obj: "obj") -> _lvgl._Bool:
        return _lvgl.menu_back_btn_is_root(self, obj)

    def clear_history(self) -> None:
        return _lvgl.menu_clear_history(self)


class menu_page(obj):

    def __init__(self, parent: _lvgl.obj_t, title: _lvgl.char):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent, title,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.menu_page_create(parent, title)
            cls.cast(self)
   


class menu_cont(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.menu_cont_create(parent)
            cls.cast(self)
   


class menu_section(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.menu_section_create(parent)
            cls.cast(self)
   


class menu_separator(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.menu_separator_create(parent)
            cls.cast(self)
   


class meter(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.meter_create(parent)
            cls.cast(self)
   
    def set_scale_ticks(self, cnt: _lvgl.uint16_t, width: _lvgl.uint16_t, len: _lvgl.uint16_t, color: "color_t") -> None:
        return _lvgl.meter_set_scale_ticks(self, cnt, width, len, color)

    def set_scale_major_ticks(self, nth: _lvgl.uint16_t, width: _lvgl.uint16_t, len: _lvgl.uint16_t, color: "color_t", label_gap: _lvgl.int16_t) -> None:
        return _lvgl.meter_set_scale_major_ticks(self, nth, width, len, color, label_gap)

    def set_scale_range(self, min: _lvgl.int32_t, max: _lvgl.int32_t, angle_range: _lvgl.uint32_t, rotation: _lvgl.uint32_t) -> None:
        return _lvgl.meter_set_scale_range(self, min, max, angle_range, rotation)

    def add_needle_line(self, width: _lvgl.uint16_t, color: "color_t", r_mod: _lvgl.int16_t) -> "meter_indicator_t":
        return _lvgl.meter_add_needle_line(self, width, color, r_mod)

    def add_needle_img(self, src: None, pivot_x: _lvgl.coord_t, pivot_y: _lvgl.coord_t) -> "meter_indicator_t":
        return _lvgl.meter_add_needle_img(self, src, pivot_x, pivot_y)

    def add_arc(self, width: _lvgl.uint16_t, color: "color_t", r_mod: _lvgl.int16_t) -> "meter_indicator_t":
        return _lvgl.meter_add_arc(self, width, color, r_mod)

    def add_scale_lines(self, color_start: "color_t", color_end: "color_t", local: _lvgl._Bool, width_mod: _lvgl.int16_t) -> "meter_indicator_t":
        return _lvgl.meter_add_scale_lines(self, color_start, color_end, local, width_mod)

    def set_indicator_value(self, indic: "meter_indicator_t", value: _lvgl.int32_t) -> None:
        return _lvgl.meter_set_indicator_value(self, indic, value)

    def set_indicator_start_value(self, indic: "meter_indicator_t", value: _lvgl.int32_t) -> None:
        return _lvgl.meter_set_indicator_start_value(self, indic, value)

    def set_indicator_end_value(self, indic: "meter_indicator_t", value: _lvgl.int32_t) -> None:
        return _lvgl.meter_set_indicator_end_value(self, indic, value)


class msgbox(obj):

    def __init__(self, parent: _lvgl.obj_t, title: _lvgl.char, txt: _lvgl.char, btn_txts: List[_lvgl.char], add_close_btn: _lvgl._Bool):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent, title, txt, btn_txts, add_close_btn,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.msgbox_create(parent, title, txt, btn_txts, add_close_btn)
            cls.cast(self)
   
    def get_title(self) -> "obj":
        return _lvgl.msgbox_get_title(self)

    def get_close_btn(self) -> "obj":
        return _lvgl.msgbox_get_close_btn(self)

    def get_text(self) -> "obj":
        return _lvgl.msgbox_get_text(self)

    def get_content(self) -> "obj":
        return _lvgl.msgbox_get_content(self)

    def get_btns(self) -> "obj":
        return _lvgl.msgbox_get_btns(self)

    def get_active_btn(self) -> _lvgl.uint16_t:
        return _lvgl.msgbox_get_active_btn(self)

    def get_active_btn_text(self) -> _lvgl.char:
        return _lvgl.msgbox_get_active_btn_text(self)

    def close(self) -> None:
        return _lvgl.msgbox_close(self)

    def close_async(self) -> None:
        return _lvgl.msgbox_close_async(self)


class roller(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.roller_create(parent)
            cls.cast(self)
   
    def set_options(self, options: _lvgl.char, mode: _lvgl.roller_mode_t) -> None:
        return _lvgl.roller_set_options(self, options, mode)

    def set_selected(self, sel_opt: _lvgl.uint16_t, anim: _lvgl.anim_enable_t) -> None:
        return _lvgl.roller_set_selected(self, sel_opt, anim)

    def set_visible_row_count(self, row_cnt: _lvgl.uint8_t) -> None:
        return _lvgl.roller_set_visible_row_count(self, row_cnt)

    def get_selected(self) -> _lvgl.uint16_t:
        return _lvgl.roller_get_selected(self)

    def get_selected_str(self, buf: _lvgl.char, buf_size: _lvgl.uint32_t) -> None:
        return _lvgl.roller_get_selected_str(self, buf, buf_size)

    def get_options(self) -> _lvgl.char:
        return _lvgl.roller_get_options(self)

    def get_option_cnt(self) -> _lvgl.uint16_t:
        return _lvgl.roller_get_option_cnt(self)


class slider(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.slider_create(parent)
            cls.cast(self)
   
    def set_value(self, value: _lvgl.int32_t, anim: _lvgl.anim_enable_t) -> None:
        return _lvgl.slider_set_value(self, value, anim)

    def set_left_value(self, value: _lvgl.int32_t, anim: _lvgl.anim_enable_t) -> None:
        return _lvgl.slider_set_left_value(self, value, anim)

    def set_range(self, min: _lvgl.int32_t, max: _lvgl.int32_t) -> None:
        return _lvgl.slider_set_range(self, min, max)

    def set_mode(self, mode: _lvgl.slider_mode_t) -> None:
        return _lvgl.slider_set_mode(self, mode)

    def get_value(self) -> _lvgl.int32_t:
        return _lvgl.slider_get_value(self)

    def get_left_value(self) -> _lvgl.int32_t:
        return _lvgl.slider_get_left_value(self)

    def get_min_value(self) -> _lvgl.int32_t:
        return _lvgl.slider_get_min_value(self)

    def get_max_value(self) -> _lvgl.int32_t:
        return _lvgl.slider_get_max_value(self)

    def is_dragged(self) -> _lvgl._Bool:
        return _lvgl.slider_is_dragged(self)

    def get_mode(self) -> _lvgl.slider_mode_t:
        return _lvgl.slider_get_mode(self)


class spangroup(obj):

    def __init__(self, par: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (par,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.spangroup_create(par)
            cls.cast(self)
   
    def new_span(self) -> "span_t":
        return _lvgl.spangroup_new_span(self)

    def del_span(self, span: "span_t") -> None:
        return _lvgl.spangroup_del_span(self, span)

    def set_align(self, align: _lvgl.text_align_t) -> None:
        return _lvgl.spangroup_set_align(self, align)

    def set_overflow(self, overflow: _lvgl.span_overflow_t) -> None:
        return _lvgl.spangroup_set_overflow(self, overflow)

    def set_indent(self, indent: _lvgl.coord_t) -> None:
        return _lvgl.spangroup_set_indent(self, indent)

    def set_mode(self, mode: _lvgl.span_mode_t) -> None:
        return _lvgl.spangroup_set_mode(self, mode)

    def set_lines(self, lines: _lvgl.int32_t) -> None:
        return _lvgl.spangroup_set_lines(self, lines)

    def get_child(self, id: _lvgl.int32_t) -> "span_t":
        return _lvgl.spangroup_get_child(self, id)

    def get_child_cnt(self) -> _lvgl.uint32_t:
        return _lvgl.spangroup_get_child_cnt(self)

    def get_align(self) -> _lvgl.text_align_t:
        return _lvgl.spangroup_get_align(self)

    def get_overflow(self) -> _lvgl.span_overflow_t:
        return _lvgl.spangroup_get_overflow(self)

    def get_indent(self) -> _lvgl.coord_t:
        return _lvgl.spangroup_get_indent(self)

    def get_mode(self) -> _lvgl.span_mode_t:
        return _lvgl.spangroup_get_mode(self)

    def get_lines(self) -> _lvgl.int32_t:
        return _lvgl.spangroup_get_lines(self)

    def get_max_line_h(self) -> _lvgl.coord_t:
        return _lvgl.spangroup_get_max_line_h(self)

    def get_expand_width(self, max_width: _lvgl.uint32_t) -> _lvgl.uint32_t:
        return _lvgl.spangroup_get_expand_width(self, max_width)

    def get_expand_height(self, width: _lvgl.coord_t) -> _lvgl.coord_t:
        return _lvgl.spangroup_get_expand_height(self, width)

    def refr_mode(self) -> None:
        return _lvgl.spangroup_refr_mode(self)


class textarea(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.textarea_create(parent)
            cls.cast(self)
   
    def add_char(self, c: _lvgl.uint32_t) -> None:
        return _lvgl.textarea_add_char(self, c)

    def add_text(self, txt: _lvgl.char) -> None:
        return _lvgl.textarea_add_text(self, txt)

    def del_char(self) -> None:
        return _lvgl.textarea_del_char(self)

    def del_char_forward(self) -> None:
        return _lvgl.textarea_del_char_forward(self)

    def set_text(self, txt: _lvgl.char) -> None:
        return _lvgl.textarea_set_text(self, txt)

    def set_placeholder_text(self, txt: _lvgl.char) -> None:
        return _lvgl.textarea_set_placeholder_text(self, txt)

    def set_cursor_pos(self, pos: _lvgl.int32_t) -> None:
        return _lvgl.textarea_set_cursor_pos(self, pos)

    def set_cursor_click_pos(self, en: _lvgl._Bool) -> None:
        return _lvgl.textarea_set_cursor_click_pos(self, en)

    def set_password_mode(self, en: _lvgl._Bool) -> None:
        return _lvgl.textarea_set_password_mode(self, en)

    def set_password_bullet(self, bullet: _lvgl.char) -> None:
        return _lvgl.textarea_set_password_bullet(self, bullet)

    def set_one_line(self, en: _lvgl._Bool) -> None:
        return _lvgl.textarea_set_one_line(self, en)

    def set_accepted_chars(self, list: _lvgl.char) -> None:
        return _lvgl.textarea_set_accepted_chars(self, list)

    def set_max_length(self, num: _lvgl.uint32_t) -> None:
        return _lvgl.textarea_set_max_length(self, num)

    def set_insert_replace(self, txt: _lvgl.char) -> None:
        return _lvgl.textarea_set_insert_replace(self, txt)

    def set_text_selection(self, en: _lvgl._Bool) -> None:
        return _lvgl.textarea_set_text_selection(self, en)

    def set_password_show_time(self, time: _lvgl.uint16_t) -> None:
        return _lvgl.textarea_set_password_show_time(self, time)

    def set_align(self, align: _lvgl.text_align_t) -> None:
        return _lvgl.textarea_set_align(self, align)

    def get_text(self) -> _lvgl.char:
        return _lvgl.textarea_get_text(self)

    def get_placeholder_text(self) -> _lvgl.char:
        return _lvgl.textarea_get_placeholder_text(self)

    def get_label(self) -> "obj":
        return _lvgl.textarea_get_label(self)

    def get_cursor_pos(self) -> _lvgl.uint32_t:
        return _lvgl.textarea_get_cursor_pos(self)

    def get_cursor_click_pos(self) -> _lvgl._Bool:
        return _lvgl.textarea_get_cursor_click_pos(self)

    def get_password_mode(self) -> _lvgl._Bool:
        return _lvgl.textarea_get_password_mode(self)

    def get_password_bullet(self) -> _lvgl.char:
        return _lvgl.textarea_get_password_bullet(self)

    def get_one_line(self) -> _lvgl._Bool:
        return _lvgl.textarea_get_one_line(self)

    def get_accepted_chars(self) -> _lvgl.char:
        return _lvgl.textarea_get_accepted_chars(self)

    def get_max_length(self) -> _lvgl.uint32_t:
        return _lvgl.textarea_get_max_length(self)

    def text_is_selected(self) -> _lvgl._Bool:
        return _lvgl.textarea_text_is_selected(self)

    def get_text_selection(self) -> _lvgl._Bool:
        return _lvgl.textarea_get_text_selection(self)

    def get_password_show_time(self) -> _lvgl.uint16_t:
        return _lvgl.textarea_get_password_show_time(self)

    def get_current_char(self) -> _lvgl.uint32_t:
        return _lvgl.textarea_get_current_char(self)

    def clear_selection(self) -> None:
        return _lvgl.textarea_clear_selection(self)

    def cursor_right(self) -> None:
        return _lvgl.textarea_cursor_right(self)

    def cursor_left(self) -> None:
        return _lvgl.textarea_cursor_left(self)

    def cursor_down(self) -> None:
        return _lvgl.textarea_cursor_down(self)

    def cursor_up(self) -> None:
        return _lvgl.textarea_cursor_up(self)


class spinbox(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.spinbox_create(parent)
            cls.cast(self)
   
    def set_value(self, i: _lvgl.int32_t) -> None:
        return _lvgl.spinbox_set_value(self, i)

    def set_rollover(self, b: _lvgl._Bool) -> None:
        return _lvgl.spinbox_set_rollover(self, b)

    def set_digit_format(self, digit_count: _lvgl.uint8_t, separator_position: _lvgl.uint8_t) -> None:
        return _lvgl.spinbox_set_digit_format(self, digit_count, separator_position)

    def set_step(self, step: _lvgl.uint32_t) -> None:
        return _lvgl.spinbox_set_step(self, step)

    def set_range(self, range_min: _lvgl.int32_t, range_max: _lvgl.int32_t) -> None:
        return _lvgl.spinbox_set_range(self, range_min, range_max)

    def set_cursor_pos(self, pos: _lvgl.uint8_t) -> None:
        return _lvgl.spinbox_set_cursor_pos(self, pos)

    def set_digit_step_direction(self, direction: _lvgl.dir_t) -> None:
        return _lvgl.spinbox_set_digit_step_direction(self, direction)

    def get_rollover(self) -> _lvgl._Bool:
        return _lvgl.spinbox_get_rollover(self)

    def get_value(self) -> _lvgl.int32_t:
        return _lvgl.spinbox_get_value(self)

    def get_step(self) -> _lvgl.int32_t:
        return _lvgl.spinbox_get_step(self)

    def step_next(self) -> None:
        return _lvgl.spinbox_step_next(self)

    def step_prev(self) -> None:
        return _lvgl.spinbox_step_prev(self)

    def increment(self) -> None:
        return _lvgl.spinbox_increment(self)

    def decrement(self) -> None:
        return _lvgl.spinbox_decrement(self)


class spinner(obj):

    def __init__(self, parent: _lvgl.obj_t, time: _lvgl.uint32_t, arc_length: _lvgl.uint32_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent, time, arc_length,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.spinner_create(parent, time, arc_length)
            cls.cast(self)
   


class switch(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.switch_create(parent)
            cls.cast(self)
   


class table(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.table_create(parent)
            cls.cast(self)
   
    def set_cell_value(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t, txt: _lvgl.char) -> None:
        return _lvgl.table_set_cell_value(self, row, col, txt)

    def set_cell_value_fmt(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t, fmt: _lvgl.char, *args) -> None:
        return _lvgl.table_set_cell_value_fmt(self, row, col, fmt, *args)

    def set_row_cnt(self, row_cnt: _lvgl.uint16_t) -> None:
        return _lvgl.table_set_row_cnt(self, row_cnt)

    def set_col_cnt(self, col_cnt: _lvgl.uint16_t) -> None:
        return _lvgl.table_set_col_cnt(self, col_cnt)

    def set_col_width(self, col_id: _lvgl.uint16_t, w: _lvgl.coord_t) -> None:
        return _lvgl.table_set_col_width(self, col_id, w)

    def add_cell_ctrl(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t, ctrl: _lvgl.table_cell_ctrl_t) -> None:
        return _lvgl.table_add_cell_ctrl(self, row, col, ctrl)

    def clear_cell_ctrl(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t, ctrl: _lvgl.table_cell_ctrl_t) -> None:
        return _lvgl.table_clear_cell_ctrl(self, row, col, ctrl)

    def get_cell_value(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t) -> _lvgl.char:
        return _lvgl.table_get_cell_value(self, row, col)

    def get_row_cnt(self) -> _lvgl.uint16_t:
        return _lvgl.table_get_row_cnt(self)

    def get_col_cnt(self) -> _lvgl.uint16_t:
        return _lvgl.table_get_col_cnt(self)

    def get_col_width(self, col: _lvgl.uint16_t) -> _lvgl.coord_t:
        return _lvgl.table_get_col_width(self, col)

    def has_cell_ctrl(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t, ctrl: _lvgl.table_cell_ctrl_t) -> _lvgl._Bool:
        return _lvgl.table_has_cell_ctrl(self, row, col, ctrl)

    def get_selected_cell(self, row: _lvgl.uint16_t, col: _lvgl.uint16_t) -> None:
        return _lvgl.table_get_selected_cell(self, row, col)


class tabview(obj):

    def __init__(self, parent: _lvgl.obj_t, tab_pos: _lvgl.dir_t, tab_size: _lvgl.coord_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent, tab_pos, tab_size,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.tabview_create(parent, tab_pos, tab_size)
            cls.cast(self)
   
    def add_tab(self, name: _lvgl.char) -> "obj":
        return _lvgl.tabview_add_tab(self, name)

    def rename_tab(self, tab_id: _lvgl.uint32_t, new_name: _lvgl.char) -> None:
        return _lvgl.tabview_rename_tab(self, tab_id, new_name)

    def get_content(self) -> "obj":
        return _lvgl.tabview_get_content(self)

    def get_tab_btns(self) -> "obj":
        return _lvgl.tabview_get_tab_btns(self)

    def set_act(self, id: _lvgl.uint32_t, anim_en: _lvgl.anim_enable_t) -> None:
        return _lvgl.tabview_set_act(self, id, anim_en)

    def get_tab_act(self) -> _lvgl.uint16_t:
        return _lvgl.tabview_get_tab_act(self)


class tileview(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.tileview_create(parent)
            cls.cast(self)
   
    def add_tile(self, col_id: _lvgl.uint8_t, row_id: _lvgl.uint8_t, dir: _lvgl.dir_t) -> "obj":
        return _lvgl.tileview_add_tile(self, col_id, row_id, dir)

    def get_tile_act(self) -> "obj":
        return _lvgl.tileview_get_tile_act(self)


class win(obj):

    def __init__(self, parent: _lvgl.obj_t, header_height: _lvgl.coord_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent, header_height,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.win_create(parent, header_height)
            cls.cast(self)
   
    def add_title(self, txt: _lvgl.char) -> "obj":
        return _lvgl.win_add_title(self, txt)

    def add_btn(self, icon: None, btn_w: _lvgl.coord_t) -> "obj":
        return _lvgl.win_add_btn(self, icon, btn_w)

    def get_header(self) -> "obj":
        return _lvgl.win_get_header(self)

    def get_content(self) -> "obj":
        return _lvgl.win_get_content(self)


class ime_pinyin(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.ime_pinyin_create(parent)
            cls.cast(self)
   
    def set_keyboard(self, kb: "obj") -> None:
        return _lvgl.ime_pinyin_set_keyboard(self, kb)

    def set_dict(self, dict: "pinyin_dict_t") -> None:
        return _lvgl.ime_pinyin_set_dict(self, dict)

    def set_mode(self, mode: _lvgl.ime_pinyin_mode_t) -> None:
        return _lvgl.ime_pinyin_set_mode(self, mode)

    def get_kb(self) -> "obj":
        return _lvgl.ime_pinyin_get_kb(self)

    def get_cand_panel(self) -> "obj":
        return _lvgl.ime_pinyin_get_cand_panel(self)

    def get_dict(self) -> "pinyin_dict_t":
        return _lvgl.ime_pinyin_get_dict(self)


class file_explorer(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.file_explorer_create(parent)
            cls.cast(self)
   
    def set_quick_access_path(self, dir: _lvgl.file_explorer_dir_t, path: _lvgl.char) -> None:
        return _lvgl.file_explorer_set_quick_access_path(self, dir, path)

    def set_sort(self, sort: _lvgl.file_explorer_sort_t) -> None:
        return _lvgl.file_explorer_set_sort(self, sort)

    def get_selected_file_name(self) -> _lvgl.char:
        return _lvgl.file_explorer_get_selected_file_name(self)

    def get_current_path(self) -> _lvgl.char:
        return _lvgl.file_explorer_get_current_path(self)

    def get_header(self) -> "obj":
        return _lvgl.file_explorer_get_header(self)

    def get_quick_access_area(self) -> "obj":
        return _lvgl.file_explorer_get_quick_access_area(self)

    def get_path_label(self) -> "obj":
        return _lvgl.file_explorer_get_path_label(self)

    def get_places_list(self) -> "obj":
        return _lvgl.file_explorer_get_places_list(self)

    def get_device_list(self) -> "obj":
        return _lvgl.file_explorer_get_device_list(self)

    def get_file_table(self) -> "obj":
        return _lvgl.file_explorer_get_file_table(self)

    def get_sort(self) -> _lvgl.file_explorer_sort_t:
        return _lvgl.file_explorer_get_sort(self)

    def open_dir(self, dir: _lvgl.char) -> None:
        return _lvgl.file_explorer_open_dir(self, dir)


class barcode(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.barcode_create(parent)
            cls.cast(self)
   
    def set_dark_color(self, color: "color32_t") -> None:
        return _lvgl.barcode_set_dark_color(self, color)

    def set_light_color(self, color: "color32_t") -> None:
        return _lvgl.barcode_set_light_color(self, color)

    def set_scale(self, scale: _lvgl.uint16_t) -> None:
        return _lvgl.barcode_set_scale(self, scale)

    def update(self, data: _lvgl.char) -> _lvgl.res_t:
        return _lvgl.barcode_update(self, data)

    def get_dark_color(self) -> "color32_t":
        return _lvgl.barcode_get_dark_color(self)

    def get_light_color(self) -> "color32_t":
        return _lvgl.barcode_get_light_color(self)

    def get_scale(self) -> _lvgl.uint16_t:
        return _lvgl.barcode_get_scale(self)


class gif(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.gif_create(parent)
            cls.cast(self)
   
    def set_src(self, src: None) -> None:
        return _lvgl.gif_set_src(self, src)

    def restart(self) -> None:
        return _lvgl.gif_restart(self)


class qrcode(obj):

    def __init__(self, parent: _lvgl.obj_t):
        if self.__class__.__name__ == 'obj':
            super().__init__()
        else:
            super().__init__(_lvgl._DefaultArg)  # NOQA
                                    
        for arg in (parent,):
            if arg == _lvgl._DefaultArg:  # NOQA
                break
        else:
            cls = _lvgl.qrcode_create(parent)
            cls.cast(self)
   
    def set_size(self, size: _lvgl.coord_t) -> None:
        return _lvgl.qrcode_set_size(self, size)

    def set_dark_color(self, color: "color_t") -> None:
        return _lvgl.qrcode_set_dark_color(self, color)

    def set_light_color(self, color: "color_t") -> None:
        return _lvgl.qrcode_set_light_color(self, color)

    def update(self, data: None, data_len: _lvgl.uint32_t) -> _lvgl.res_t:
        return _lvgl.qrcode_update(self, data, data_len)


