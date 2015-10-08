#!/bin/sh
# cxOracleSIP.sh
# Copyright (c) 2015 Stefano Apostolico
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.



help () {
    echo `basename $0` "[-o] [-e]"
    echo " -o apply patch to oracle binaries ($ORACLE_HOME)"
    [[ -z "$VIRTUAL_ENV" ]] && V="need active virtualenv" || V=$VIRTUAL_ENV
    echo " -e apply patch to cx_Oracle ($V)"
    exit 1
}

echo $# $@

[[ $# -eq 0 ]]  && help

while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -o)
            ORA=1
            ;;
        -e) if [ -z $VIRTUAL_ENV ]; then
                echo "ERROR: no active virtualenv"
                exit 1
            fi
            ENV=1
            ;;
        *) help
           exit 1
        ;;
    esac
    shift # past argument or value
done

patch (){
    echo "patching $1"
    basetarget=`basename $1`
    otool -L $1 | awk '/oracle/ {print $1}' | awk '/[^:]$/ ' | while read lib
    do
        echo "    - $lib"
        baselib=`basename $lib`
        if [ "$basetarget" = "$baselib" ]
        then
            echo "    - changing id to $baselib for $1"
            sudo install_name_tool -id $baselib $1
        else
            echo "    - changing path id for $lib in $1"
            sudo install_name_tool -change $lib $ORACLE_HOME/$baselib $1
        fi
    done
}

if [[ $ORA -eq 1 ]];then
    find $ORACLE_HOME -maxdepth 1 -type f \( -perm -1 -o \( -perm -10 -o -perm -100 \) \) -print | while read target
    do
        patch $target
    done
fi

if [[ $ENV -eq 1 ]];then
    patch $VIRTUAL_ENV/lib/python2.7/site-packages/cx_Oracle.so
fi

