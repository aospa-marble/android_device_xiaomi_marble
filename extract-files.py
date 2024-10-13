#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/marble',
    'hardware/xiaomi',
    'vendor/qcom/common/vendor/adreno-s',
    'vendor/qcom/common/vendor/display/5.10',
    'vendor/qcom/common/vendor/perf',
    'vendor/qcom/common/vendor/media',
]

def lib_fixup_marble_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_marble' if partition == 'vendor' else None

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_vendor' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'audio.primary.taro',
        'android.hardware.gnss@2.1-impl-qti',
        'android.hardware.gnss-aidl-impl-qti',
        'vendor.qti.hardware.pal@1.0',
        'libsdm-disp-vndapis',
        'libsdmextension',
    ): lib_fixup_marble_suffix,
    (
        'libgrpc++_unsecure',
        'com.qualcomm.qti.dpm.api@1.0',
        'com.qualcomm.qti.imscmservice@1.0',
        'com.qualcomm.qti.imscmservice@2.0',
        'com.qualcomm.qti.imscmservice@2.1',
        'com.qualcomm.qti.imscmservice@2.2',
        'com.qualcomm.qti.uceservice@2.0',
        'com.qualcomm.qti.uceservice@2.1',
        'com.qualcomm.qti.uceservice@2.2',
        'com.qualcomm.qti.uceservice@2.3',
        'vendor.qti.data.factory@2.0',
        'vendor.qti.data.factory@2.1',
        'vendor.qti.data.factory@2.2',
        'vendor.qti.data.factory@2.3',
        'vendor.qti.data.factory@2.4',
        'vendor.qti.data.factory@2.5',
        'vendor.qti.data.factory@2.6',
        'vendor.qti.data.factory@2.7',
        'vendor.qti.data.mwqem@1.0',
        'vendor.qti.data.slm@1.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.data.cne.internal.api@1.0',
        'vendor.qti.hardware.data.cne.internal.constants@1.0',
        'vendor.qti.hardware.data.cne.internal.server@1.0',
        'vendor.qti.hardware.data.cne.internal.server@1.1',
        'vendor.qti.hardware.data.cne.internal.server@1.2',
        'vendor.qti.hardware.data.cne.internal.server@1.3',
        'vendor.qti.hardware.data.connection@1.0',
        'vendor.qti.hardware.data.connection@1.1',
        'vendor.qti.hardware.data.connectionfactory-V1-ndk_platform',
        'vendor.qti.hardware.data.dataactivity-V1-ndk_platform',
        'vendor.qti.hardware.data.dynamicdds@1.0',
        'vendor.qti.hardware.data.dynamicdds@1.1',
        'vendor.qti.hardware.data.flow@1.0',
        'vendor.qti.hardware.data.flow@1.1',
        'vendor.qti.hardware.data.iwlan@1.0',
        'vendor.qti.hardware.data.iwlan@1.1',
        'vendor.qti.hardware.data.ka-V1-ndk_platform',
        'vendor.qti.hardware.data.latency@1.0',
        'vendor.qti.hardware.data.lce@1.0',
        'vendor.qti.hardware.data.qmi@1.0',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.hardware.dpmservice@1.1',
        'vendor.qti.hardware.embmssl@1.0',
        'vendor.qti.hardware.embmssl@1.1',
        'vendor.qti.hardware.limits@1.0',
        'vendor.qti.hardware.limits@1.1',
        'vendor.qti.hardware.limits@1.2',
        'vendor.qti.hardware.ListenSoundModel@1.0',
        'vendor.qti.hardware.mwqemadapter@1.0',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.hardware.radio.am-V1-ndk_platform',
        'vendor.qti.hardware.radio.am@1.0',
        'vendor.qti.hardware.radio.atcmdfwd@1.0',
        'vendor.qti.hardware.radio.ims-V7-ndk_platform',
        'vendor.qti.hardware.radio.ims@1.0',
        'vendor.qti.hardware.radio.ims@1.1',
        'vendor.qti.hardware.radio.ims@1.2',
        'vendor.qti.hardware.radio.ims@1.3',
        'vendor.qti.hardware.radio.ims@1.4',
        'vendor.qti.hardware.radio.ims@1.5',
        'vendor.qti.hardware.radio.ims@1.6',
        'vendor.qti.hardware.radio.ims@1.7',
        'vendor.qti.hardware.radio.ims@1.8',
        'vendor.qti.hardware.radio.internal.deviceinfo@1.0',
        'vendor.qti.hardware.radio.lpa@1.0',
        'vendor.qti.hardware.radio.lpa@1.1',
        'vendor.qti.hardware.radio.lpa@1.2',
        'vendor.qti.hardware.radio.lpa@1.3',
        'vendor.qti.hardware.radio.qcrilhook@1.0',
        'vendor.qti.hardware.radio.qtiradio-V5-ndk_platform',
        'vendor.qti.hardware.radio.qtiradio@1.0',
        'vendor.qti.hardware.radio.qtiradio@2.0',
        'vendor.qti.hardware.radio.qtiradio@2.1',
        'vendor.qti.hardware.radio.qtiradio@2.2',
        'vendor.qti.hardware.radio.qtiradio@2.3',
        'vendor.qti.hardware.radio.qtiradio@2.4',
        'vendor.qti.hardware.radio.qtiradio@2.5',
        'vendor.qti.hardware.radio.qtiradio@2.6',
        'vendor.qti.hardware.radio.uim@1.0',
        'vendor.qti.hardware.radio.uim@1.1',
        'vendor.qti.hardware.radio.uim@1.2',
        'vendor.qti.hardware.radio.uim_remote_client@1.0',
        'vendor.qti.hardware.radio.uim_remote_client@1.1',
        'vendor.qti.hardware.radio.uim_remote_client@1.2',
        'vendor.qti.hardware.radio.uim_remote_server@1.0',
        'vendor.qti.hardware.slmadapter@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.ims.callcapability@1.0',
        'vendor.qti.ims.callinfo@1.0',
        'vendor.qti.ims.configservice@1.0',
        'vendor.qti.ims.configservice@1.1',
        'vendor.qti.ims.connection@1.0',
        'vendor.qti.ims.factory@1.0',
        'vendor.qti.ims.factory@1.1',
        'vendor.qti.ims.factory@2.0',
        'vendor.qti.ims.factory@2.1',
        'vendor.qti.ims.factory@2.2',
        'vendor.qti.ims.rcsconfig@1.0',
        'vendor.qti.ims.rcsconfig@1.1',
        'vendor.qti.ims.rcsconfig@2.0',
        'vendor.qti.ims.rcsconfig@2.1',
        'vendor.qti.ims.rcssip@1.0',
        'vendor.qti.ims.rcssip@1.1',
        'vendor.qti.ims.rcssip@1.2',
        'vendor.qti.ims.rcsuce@1.0',
        'vendor.qti.ims.rcsuce@1.1',
        'vendor.qti.ims.rcsuce@1.2',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.latency@2.0',
        'vendor.qti.latency@2.1',
        'vendor.qti.latency@2.2',
        'vendor.qti.latency@2.3',
        'vendor.xiaomi.hardware.displayfeature@1.0',
        'vendor.xiaomi.hardware.fingerprintextension@1.0',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
        .add_needed('android.hardware.security.rkp-V1-ndk_platform.so'),
    (
        'vendor/bin/hw/dolbycodec2',
        'vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service',
        'vendor/bin/hw/vendor.dolby.media.c2@1.0-service', 
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    (
        'vendor/bin/hw/mfp-daemon',
        'vendor/lib64/hw/displayfeature.default.so',
        'vendor/lib64/hw/audio.primary.taro.so',
    ): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/bin/hw/vendor.qti.hardware.display.composer-service': blob_fixup()
        .remove_needed('libutils.so')
        .add_needed('libutils-v32.so')
        .add_needed('libutils-shim.so'),
    'vendor/lib64/c2.dolby.client.so': blob_fixup()
        .add_needed('libcodec2_hidl_shim.so'),
    'vendor/bin/hw/vendor.qti.secure_element@1.2-service': blob_fixup()
        .replace_needed('jcos_nq_client-v1.so', 'jcos_nq_client.so')
        .replace_needed('ls_nq_client-v1.so', 'ls_nq_client.so')
        .replace_needed('se_nq_extn_client-v1.so', 'se_nq_extn_client.so'),
    (
        'vendor/etc/camera/marble_enhance_motiontuning.xml',
        'vendor/etc/camera/marble_motiontuning.xml',
    ): blob_fixup().regex_replace('xml=version', 'xml version'),
    'vendor/etc/camera/pureView_parameter.xml': blob_fixup().regex_replace(
        r'=([0-9]+)>', r'="\1">'
    ),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup().add_needed('libcrypto_shim.so')
}  # fmt: skip

module = ExtractUtilsModule(
    'marble',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
