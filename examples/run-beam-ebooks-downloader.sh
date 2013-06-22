#! /bin/sh -x

export CALIBRE_DEVELOP_FROM=${HOME}/github/calibre/src
export DISPLAY=:1

LOGDIR=${HOME}/Dropbox/Calibre/_plugin_logs/beam-ebooks-downloader/$(date +%Y%m)/$(date +%Y%m%d-%H%M)

mkdir -p ${LOGDIR}

calibre-debug \
    --run-plugin "Beam EBooks Downloader" \
    > ${LOGDIR}/stdout.txt \
    2> ${LOGDIR}/stderr.txt

mv /tmp/calibre-beam-ebooks-downloader-plugin ${LOGDIR}

