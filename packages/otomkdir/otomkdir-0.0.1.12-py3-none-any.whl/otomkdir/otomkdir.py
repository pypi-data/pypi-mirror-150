import platform
import os
from pathlib import Path


##DETECT OPERATING SYSTEM
if platform.system( ).lower( ) == "windows":
    default_path = Path( os.environ[ 'USERPROFILE' ], "Desktop" )
    default_driver = "C"
elif platform.system( ).lower( ) == "darwin":
    default_path = Path( os.environ[ 'HOME' ], "Desktop" )
    default_driver = Path( os.environ[ 'HOME' ] )
else:
    pass



def auto_create_folder(
     default_path = default_path
    , folder_extend = "task_list"
    , subfolder_extend = None
):
    """
    default_path : only for Windows path
    folder_extend : set folder names
    subfolder_extend : set subfolder names
    """

    default_path = Path( default_path )

    if platform.system( ).lower( ) == "windows":
        default_list = str( default_path ).split( "\\" )
    elif platform.system( ).lower( ) == "darwin":
        default_list = str( default_path ).split( "/" )
    else:
        pass

    for elem in default_list:
        if elem == "":
            default_list.remove( "" )
        else:
            pass
    # print( default_list )

    if subfolder_extend == None:
        folder_path = Path( default_path, folder_extend )
    else:
        folder_path = Path( default_path, folder_extend, subfolder_extend )
        # print( folder_path )

    if platform.system( ).lower( ) == "windows":
        folder_list = str( folder_path ).split( "\\" )
    elif platform.system( ).lower( ) == "darwin":
        folder_list = str( folder_path ).split( "/" )
    else:
        pass
    # print( folder_list )

    ##remove default path from full path
    for def_folder in default_list:
        folder_list.remove( def_folder )

    # print( len( folder_list ) )
    # print( folder_list )


    increment_path = default_path
    for folder in folder_list:
        increment_path = Path( increment_path, folder )
        # print( increment_path )

        if os.path.isdir( increment_path ) == False:
            os.mkdir( increment_path )
            # return folder_path

        else:
            print( "Directory already exists." )
            # return folder_path
            pass

    return folder_path



def auto_create_folder_2(
     driver_name = default_driver
    , folder_extend = "task_list"
    , subfolder_extend = None
):
    """
    driver_name : determine driver name, i.e. C drive or D drive, etc
    folder_extend : set folder names
    subfolder_extend : set subfolder names
    """

    if platform.system( ).lower( ) == "windows":
        default_path = Path( driver_name + ":/" )
    elif platform.system( ).lower( ) == "darwin":
        default_path = Path( default_driver )
    else:
        pass

    if platform.system( ).lower( ) == "windows":
        default_list = str( default_path ).split( "\\" )
    elif platform.system( ).lower( ) == "darwin":
        default_list = str( default_path ).split( "/" )
    else:
        pass

    for elem in default_list:
        if elem == "":
            default_list.remove( "" )
        else:
            pass
    # print( default_list )

    if subfolder_extend == None:
        folder_path = Path( default_path, folder_extend )
    else:
        folder_path = Path( default_path, folder_extend, subfolder_extend )
        # print( folder_path )

    if platform.system( ).lower( ) == "windows":
        folder_list = str( folder_path ).split( "\\" )
    elif platform.system( ).lower( ) == "darwin":
        folder_list = str( folder_path ).split( "/" )
    else:
        pass
    # print( folder_list )

    ##remove default path from full path
    for def_folder in default_list:
        folder_list.remove( def_folder )

    # print( len( folder_list ) )
    # print( folder_list )


    increment_path = default_path
    for folder in folder_list:
        increment_path = Path( increment_path, folder )
        # print( increment_path )

        if os.path.isdir( increment_path ) == False:
            os.mkdir( increment_path )
            # return folder_path

        else:
            print( "Directory already exists." )
            # return folder_path
            pass

    return folder_path
