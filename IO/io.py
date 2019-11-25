import os
import glob
from ..logger import logger

def get_glob_path(path: str, pattern: str) -> list:
    '''
    得到path下符合pattern的文件路径列表
    '''
    try:
        return glob.glob(os.path.join(path, pattern))
    except:
        logger.warning('[get_glob_path] check {} {}'.format(path, pattern))
        import traceback
        traceback.print_exc()
        return []

if __name__=="__main__":
    res = get_glob_path('./', '*')
    logger.info(res)
