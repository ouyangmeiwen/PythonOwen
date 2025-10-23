#!/bin/bash

root=$(dirname $(realpath $0))
cwd="$root/.."

zip(){
    find $cwd/dist -name lms_aarch64_*.iso -exec pbzip2 -k {} \;
}

checksums(){
    cd $cwd/dist
    zip_file=$(find lms_aarch64_*.iso.bz2)
    sha256sum $zip_file > $zip_file.sha256
}

zip
checksums