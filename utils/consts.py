####################
#   GLOBAL CONSTS  #
####################
DEBUG_FLAG = False
TESSERACT_PATH = r"C:\\Program Files\\Tesseract-OCR\\"

####################
# VISION.PY CONSTS #
####################
V_WINDOW_DELAY = 0.5              # sleep delay for scrotter
V_CONFIDENCE_VAL = 0.6
V_PRESET_CROP = 0.2               # percentage of crop estate to use (% val in float)

####################
# CONFIG.PY CONSTS #
####################
C_DEFAULT_IMGS = {
    'decFarmText'   : './ImgResources/decorateFarmText.png',
    'myMobLoc'      : './ImgResources/myMonsterText.png',
    'mobLock'       : './ImgResources/mobAsset.png',
    'levelAsset'    : './ImgResources/lvlAsset.png',
    'UIAsset'       : './ImgResources/farmUI.png',
    'shopButt'      : './ImgResources/shopButtAsset.png',
    'usableButt'    : './ImgResources/usableTextAsset.png',
    'midBoxAsset'   : './ImgResources/storePresentAsset.png',
    'releaseText'   : './ImgResources/releaseAsset.png',
    'nurtureText'   : './ImgResources/nurtureAsset.png'
}
C_OOB_POS = (300, 10) # default position to place cursor on the maple screen

########################
# CONTROLLER.PY CONSTS #
########################
CONT_MOUSE_MOVE_DUR = 0.3
CONT_DELAY = 0.2

#################
# OCR.PY CONSTS #
#################
O_MAX_PIX_DIST = 30