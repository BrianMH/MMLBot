####################
#   GLOBAL CONSTS  #
####################
DEBUG_FLAG = False

####################
# VISION.PY CONSTS #
####################
V_WINDOW_DELAY = 0.5              # sleep delay for scrotter
V_TUP_SIZE = (1535, 1151)         # scaling up seems to work better than scaling down...
V_CONFIDENCE_VAL = 0.6
V_PRESET_CROP = 0.2               # percentage of crop estate to use (% val in float)

####################
# CONFIG.PY CONSTS #
####################
C_DEFAULT_IMGS = {
    'decFarmText'   : './src/ImgResources/decorateFarmText.png',
    'myMobLoc'      : './src/ImgResources/myMonsterText.png',
    'mobLock'       : './src/ImgResources/mobAsset.png',
    'levelAsset'    : './src/ImgResources/lvlAsset.png',
    'UIAsset'       : './src/ImgResources/farmUI.png',
    'shopButt'      : './src/ImgResources/shopButtAsset.png',
    'usableButt'    : './src/ImgResources/usableTextAsset.png',
    'midBoxAsset'   : './src/ImgResources/storePresentAsset.png',
    'releaseText'   : './src/ImgResources/releaseAsset.png',
    'nurtureText'   : './src/ImgResources/nurtureAsset.png'
}

########################
# CONTROLLER.PY CONSTS #
########################
CONT_MOUSE_MOVE_DUR = 0.3
CONT_DELAY = 0.2