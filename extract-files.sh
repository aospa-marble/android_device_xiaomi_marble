#!/bin/bash
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

set -e

DEVICE=marble
VENDOR=xiaomi

# Load extract_utils and do some sanity checks
MY_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "${MY_DIR}" ]]; then MY_DIR="${PWD}"; fi

ANDROID_ROOT="${MY_DIR}/../../.."

HELPER="${ANDROID_ROOT}/tools/extract-utils/extract_utils.sh"
if [ ! -f "${HELPER}" ]; then
    echo "Unable to find helper script at ${HELPER}"
    exit 1
fi
source "${HELPER}"

# Default to sanitizing the vendor folder before extraction
CLEAN_VENDOR=true

KANG=
SECTION=
FIXUP_ONLY=false

while [ "${#}" -gt 0 ]; do
    case "${1}" in
        -n | --no-cleanup)
             CLEAN_VENDOR=false
             ;;
        -k | --kang)
             KANG="--kang"
             ;;
        -s | --section)
             SECTION="${2}"
             shift
             CLEAN_VENDOR=false
             ;;
        -f | --fixup-only)
             FIXUP_ONLY=true
             ;;
         *)
             SRC="${1}"
             ;;
    esac
    shift
done

if [ -z "${SRC}" ]; then
    SRC="adb"
fi

function blob_fixup() {
    case "${1}" in
        vendor/bin/hw/android.hardware.security.keymint-service-qti | vendor/lib64/libqtikeymint.so)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "android.hardware.security.rkp-V1-ndk_platform.so" || \
                "${PATCHELF}" --add-needed "android.hardware.security.rkp-V1-ndk_platform.so" "${2}"
            ;;
        vendor/bin/hw/dolbycodec2 | vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service | vendor/bin/hw/vendor.dolby.media.c2@1.0-service)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libstagefright_foundation-v33.so" || \
                "${PATCHELF}" --add-needed "libstagefright_foundation-v33.so" "${2}"
            ;;
        vendor/bin/hw/mfp-daemon | vendor/lib64/hw/displayfeature.default.so | vendor/lib64/hw/audio.primary.taro.so)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libstagefright_foundation-v33.so" || \
                "${PATCHELF}" --replace-needed "libstagefright_foundation.so" "libstagefright_foundation-v33.so" "${2}"
            ;;
        vendor/bin/hw/vendor.qti.hardware.display.composer-service)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libutils.so" && \
                "${PATCHELF}" --remove-needed "libutils.so" "${2}"
            "${PATCHELF}" --print-needed "${2}" | grep -q "libutils-v32.so" || \
                "${PATCHELF}" --add-needed "libutils-v32.so" "${2}"
            "${PATCHELF}" --print-needed "${2}" | grep -q "libutils-shim.so" || \
                "${PATCHELF}" --add-needed "libutils-shim.so" "${2}"
            ;;
        vendor/bin/hw/vendor.qti.secure_element@1.2-service)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "jcos_nq_client-v1.so" && \
                "${PATCHELF}" --replace-needed "jcos_nq_client-v1.so" "jcos_nq_client.so" "${2}"
            "${PATCHELF}" --print-needed "${2}" | grep -q "ls_nq_client-v1.so" && \
                "${PATCHELF}" --replace-needed "ls_nq_client-v1.so" "ls_nq_client.so" "${2}"
            "${PATCHELF}" --print-needed "${2}" | grep -q "se_nq_extn_client-v1.so" && \
                "${PATCHELF}" --replace-needed "se_nq_extn_client-v1.so" "se_nq_extn_client.so" "${2}"
            ;;
        vendor/etc/camera/marble*_motiontuning.xml)
            [ "$2" = "" ] && return 0
            sed -i 's/xml=version/xml\ version/g' "${2}"
            ;;
        vendor/etc/camera/pureView_parameter.xml)
            [ "$2" = "" ] && return 0
            sed -i "s/=\([0-9]\+\)>/=\"\1\">/g" "${2}"
            ;;
        vendor/etc/media_codecs*.xml)
            [ "$2" = "" ] && return 0
            sed -Ei "/media_codecs_(google_audio|google_c2|google_telephony|vendor_audio)/d" "${2}"
            ;;
        vendor/lib64/c2.dolby.client.so)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libcodec2_hidl_shim.so" || \
                "${PATCHELF}" --add-needed "libcodec2_hidl_shim.so" "${2}"
            ;;
        vendor/lib64/libwvhidl.so)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libcrypto_shim.so" || \
                "${PATCHELF}" --add-needed "libcrypto_shim.so" "${2}"
            ;;
        vendor/lib64/vendor.libdpmframework.so)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libhidlbase_shim.so" || \
                "${PATCHELF}" --add-needed "libhidlbase_shim.so" "${2}"
            ;;
        vendor/lib64/libcamxcommonutils.so | vendor/lib64/libmialgoengine.so)
            [ "$2" = "" ] && return 0
            "${PATCHELF}" --print-needed "${2}" | grep -q "libprocessgroup_shim.so" || \
                "${PATCHELF}" --add-needed "libprocessgroup_shim.so" "${2}"
            ;;
        *)
             return 1
             ;;
    esac

    return 0
}

function blob_fixup_dry() {
     blob_fixup "$1" ""
}

if [ "${FIXUP_ONLY}" = true ]; then
    setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}" false false
    parse_file_list "${MY_DIR}/proprietary-files.txt" "${SECTION}"
    DEST_LIST=("${PRODUCT_COPY_FILES_DEST[@]}" "${PRODUCT_PACKAGES_DEST[@]}")
    OUTPUT_ROOT="${ANDROID_ROOT}/vendor/${VENDOR}/${DEVICE}/proprietary"
    set +e
    for BLOB in "${DEST_LIST[@]}"; do
        BLOB_FILE="${OUTPUT_ROOT}/${BLOB}"
        if [ ! -f "${BLOB_FILE}" ]; then
            continue
        fi
        if blob_fixup_dry "${BLOB}"; then
            PRE_HASH=$(md5sum "${BLOB_FILE}" | cut -d' ' -f1)
            blob_fixup "${BLOB}" "${BLOB_FILE}"
            POST_HASH=$(md5sum "${BLOB_FILE}" | cut -d' ' -f1)
            [ "${PRE_HASH}" != "${POST_HASH}" ] && printf '  + Fixed up %s\n' "${BLOB}"
        fi
    done
    set -e
    "${MY_DIR}/setup-makefiles.sh"
    exit 0
fi

# Initialize the helper
setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}" false "${CLEAN_VENDOR}"

extract "${MY_DIR}/proprietary-files.txt" "${SRC}" "${KANG}" --section "${SECTION}"

"${MY_DIR}/setup-makefiles.sh"
