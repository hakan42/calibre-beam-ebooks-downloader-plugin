#! /bin/sh -x

export CALIBRE_DEVELOP_FROM=${HOME}/github/calibre/src
export DISPLAY=:1

# LOGDIR=${HOME}/Dropbox/Calibre
LOGDIR=${HOME}/tmp
LOGDIR=${LOGDIR}/_plugin_logs/beam-ebooks-downloader/$(date +%Y%m)/$(date +%Y%m%d-%H%M)

mkdir -p ${LOGDIR}

(cd ${HOME}/github/calibre-beam-ebooks-downloader-plugin && ant test) \
    > ${LOGDIR}/ant-stdout.txt
    2> ${LOGDIR}/ant-stderr.txt

calibre-debug \
    --run-plugin "Beam EBooks Downloader" \
    > ${LOGDIR}/stdout.txt \
    2> ${LOGDIR}/stderr.txt

mv /tmp/calibre-beam-ebooks-downloader-plugin ${LOGDIR}

