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


pushd /tmp/calibre-beam-ebooks-downloader-plugin/
for f in *.epub
do
    if [ -f ${f} ]
    then
	if [ "${f}" != "999978060.epub" ]
	then
	    ~/pushbullet-bash/pushbullet push GT-I9505 file ${f}
	fi
    fi
done
popd

mv /tmp/calibre-beam-ebooks-downloader-plugin ${LOGDIR}

