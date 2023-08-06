import platform
import os
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import messagebox
import time


if platform.system( ).lower( ) == "windows":
    user_path = os.environ[ "USERPROFILE" ]
elif platform.system( ).lower( ) == "darwin":
    user_path = os.environ[ "HOME" ]

default_folder = Path( user_path, "Downloads" )
storage_folder = Path( user_path, "Desktop/carkass" )
storage_file = Path( storage_folder, "saccarst.txt" )


def setup_enkrypt( user_defined_actual_storage_path ):
    """
    user_define_actual_storage_path : storage_folder variable is used to store the ACTUAL path where the KEY file and the ENCRYPTED files will be stored. The path is to be determined by the user and only the user will know where the files are stored. Full file is needed and use "forward slash", i.e. "/" and NOT backslash ("\").

    SIDE NOTE: once actual file path has been established, 2 default folders will be created: [1] eyks : to store the ".key" files, [2] erost : to store the encrypted files
    """

    ##create storage_file to store actual path (user-defined)
    if os.path.isfile( storage_file ) == False:
        os.makedirs( storage_folder )

        time.sleep( 0.5 )

        with open( storage_file, "w", encoding = "utf-8" ) as txt_file:
            txt_file.write( user_defined_actual_storage_path )

    else:
        message = "storage_folder file already exists"
        messagebox.showinfo( "Message", message )
        print( message )


    time.sleep( 0.5 )


    ##create actual folder path set by user
    with open( storage_file, "rb" ) as rd_path:
        rd_path = rd_path.read( ).decode( "utf-8" )

    if os.path.exists( rd_path ) == False:
        os.makedirs( Path( rd_path, "eyks" ) )
        os.makedirs( Path( rd_path, "erost" ) )

    else:
        message = "actual storage folder already exists"
        messagebox.showinfo( "Message", message )
        print( message )



def gen_rand_key( key_name ):
    """
    key_name : Assign a name to the key. File format not needed as default is already set as ".key"

    SIDE NOTE: once file with key is generated and AFTER the key has been used to encrypt the original file, move this key file from default_folder to the designated folder set in storage_folder. Refer to storage_folder variable
    """

    key = Fernet.generate_key( )

    mykey_file = Path( default_folder, key_name + ".key" )

    ##store key in file
    with open( mykey_file, 'wb' ) as mykey:
        mykey.write( key )

    message = "random key has been generated and temporarily stored in \n{}".format( default_folder )
    messagebox.showinfo( "Message", message )
    print( message )



def file_encrypt( key_name, file_name, file_format ):
    """
    key_name : Specify name to the key file previously created and saved. File format not needed as default is already set as ".key".
    file_name : Specify name of the original file that needs to be encrypted. File format not needed.
    file_format : Specify file format of the original file that needs to be encrypted.
    """

    ##read key from file
    with open( Path( str( default_folder ), key_name + ".key" ), 'rb' ) as key:
        key = key.read( )

    fernet = Fernet( key )

    file_to_encrypt = Path( str( default_folder ), file_name )
    with open( Path( str( file_to_encrypt ) + file_format ), 'rb' ) as ori_file:
        ori = ori_file.read( ) ##/!\ original file will be deleted after successfully encrypting file /!\

    encrypted = fernet.encrypt( ori )

    with open( Path( str( file_to_encrypt ) + "_encrypted" + file_format ), 'wb' ) as encrypted_file:
        encrypted_file.write( encrypted )

    message = "'{}' file has been encrypted and temporarily stored in\n{}".format( file_name, default_folder )
    messagebox.showinfo( "Message", message )
    print( message )

    os.remove( Path( str( file_to_encrypt ) + file_format ) )
    message = "'{}' original file has been removed".format( file_name )
    messagebox.showwarning( "Alert !!!", message )
    print( message )



def file_decrypt( key_name, encrypt_file, file_format ):
    """
    key_name : Specify name to the key file previously created and saved. File format not needed as default is already set as ".key".
    encrypt_file : Specify name of the encrypted file. File format not needed.
    file_format : Specify file format of the encrypted file.
    """

    ##specify location that store keys and encrypted files
    with open( storage_file, "rb" ) as rd_path:
        rd_path = rd_path.read( ).decode( "utf-8" )

    folder = Path( rd_path )
    key_folder = Path( folder, "eyks" )
    encrypt_folder = Path( folder, "erost" )

    global default_folder
    if key_folder != "":
        default_folder = Path( key_folder )
    else:
        default_folder = Path( default_folder )


    with open( Path( str( default_folder ), key_name + ".key" ), 'rb' ) as key:
        key = key.read( )

    fernet = Fernet( key )

    with open( Path( str( encrypt_folder ), encrypt_file + "_encrypted" + file_format ) ) as encrypted_file:
        read_encrypt = encrypted_file.read( )

    decrypted = fernet.decrypt( bytes( read_encrypt, 'utf-8' ) )
    decoded_str = decrypted.decode( 'utf-8' ).split( ';' )
    return decoded_str
