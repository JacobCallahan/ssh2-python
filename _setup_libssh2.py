# This file is part of ssh2-python.
# Copyright (C) 2017-2021 Panos Kittenis and contributors.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
import os
import platform
from sys import stderr
from subprocess import check_call
from glob import glob
from shutil import copy2


def build_ssh2():
    build_dir = os.environ.get('BUILD_DIR', 'build_dir')
    libssh2_path = os.path.abspath('libssh2')
    
    if bool(os.environ.get('SYSTEM_LIBSSH2', False)):
        print("Using system libssh2..")
        return

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    cmake_args = [
        f'cmake {libssh2_path}',
        '-DBUILD_SHARED_LIBS=ON',
        '-DENABLE_ZLIB_COMPRESSION=ON', 
        '-DENABLE_CRYPT_NONE=ON',
        '-DENABLE_MAC_NONE=ON',
        f'-DCMAKE_INSTALL_PREFIX={os.path.join(build_dir, "libssh2_install")}'
    ]

    # Platform specific configurations
    if platform.system() == 'Darwin':
        if os.path.exists('/usr/local/opt/openssl'):
            openssl_root = '/usr/local/opt/openssl'
            cmake_args.extend([
                f'-DOPENSSL_ROOT_DIR={openssl_root}',
                f'-DOPENSSL_INCLUDE_DIR={openssl_root}/include',
                f'-DOPENSSL_CRYPTO_LIBRARY={openssl_root}/lib/libcrypto.dylib',
                f'-DOPENSSL_SSL_LIBRARY={openssl_root}/lib/libssl.dylib'
            ])
    elif platform.system() == 'Windows':
        cmake_args.extend([
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCRYPTO_BACKEND=WinCNG'
        ])
    else:  # Linux
        cmake_args.append('-DCRYPTO_BACKEND=OpenSSL')

    os.chdir(build_dir)
    print(f"************* Building libssh2 in {os.getcwd()} *************")
    print(f"cmake arguments: {cmake_args}")
    check_call(' '.join(cmake_args), shell=True)
    
    if platform.system() == 'Windows':
        check_call('cmake --build . --config Release --target install', shell=True)
    else:
        check_call('cmake --build . --target install', shell=True)
    os.chdir('..')
    print("************* Finished building libssh2 *************")


if __name__ == '__main__':
    build_ssh2()
