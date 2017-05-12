set -e

# Equivalent to "cd $(dirname $0)." Works also on platforms that don't have the
# dirname command.
script_dir="${0%/*}"
cd "${script_dir:-/}"

pushd ./gstreamer
. ./setup.sh
popd


MR_AUDIO_DESCRIPTIONS=0
MR_CLOSED_CAPTIONS=0
MR_DIGITAL_AUDIO_FORMAT=0
MR_LANGUAGE=en
MR_SCREEN_MODE=hd1080p
MR_SPEECH=0
MR_NETWORK_TYPE=Wired
MR_OEM_NAME=arris
MR_MODEL_NAME=vip5662
MR_SOC_NAME=7252
MR_OPERA_VERSION=4.8.3
MR_PLAT_BUILD_NUM=236
MR_VERSION_NUMBER=$MR_OPERA_VERSION.$MR_PLAT_BUILD_NUM

# YouTube really only needs the language code from these settings
if [ -e /extapps/data/mrsettings.sh ]; then
	. /extapps/data/mrsettings.sh
fi

if [ "$SOURCETYPE" == "APPKEY" ]; then
	LAUNCH_TYPE=remote
else
	LAUNCH_TYPE=menu
fi

SED_CMD='s/.*tv?\(.*$\)/\&\1/p'

if [[ "$@" == /tmp/dialparam[0-9]* ]]; then
        DIAL_PARAMS=$( sed -n $SED_CMD $@)
elif (( $# > 0)); then
	DIAL_PARAMS="&"$@
fi

DESTINATION_URL="https://www.youtube.com/tv?launch=${LAUNCH_TYPE}${DIAL_PARAMS}&additionalDataUrl=..."
USER_AGENT="OPR/${MR_OPERA_VERSION}, ${MR_OEM_NAME}_STB_Broadcom${MR_SOC_NAME}/${MR_VERSION_NUMBER} (Mediaroom, ${MR_OEM_NAME}${MR_MODEL_NAME}, $MR_NETWORK_TYPE)"

echo --- DESTINATION_URL=$DESTINATION_URL -----
echo --- USER_AGENT=$USER_AGENT -----
echo ------ additional args: $@ ------

# 150 MB
export MEMORY_LIMIT=154572800

exec ./run_opera.sh simple_gles -u "$DESTINATION_URL" --user-agent="$USER_AGENT" --show-fps-counter --log-level=info --remote-debugging-port=9222 $@


