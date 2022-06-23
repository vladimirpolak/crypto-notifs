
class DeviceSettings(object):
        APP_VERSION = '203.0.0.29.118'
        APPLICATION_ID = '567067343352427'
        FB_HTTP_ENGINE = 'Liger'

        ANDROID_VERSION = 29
        ANDROID_RELEASE = '10'
        PHONE_MANUFACTURER = 'HUAWEI'
        PHONE_DEVICE = 'ELS-NX9'
        PHONE_MODEL = 'HWELS'
        PHONE_DPI = '530dpi'
        PHONE_RESOLUTION = '1200x2499'
        PHONE_CHIPSET = 'kirin990'
        VERSION_CODE = '314665232'

        COUNTRY = "SK"
        LOCALE = "en_SK"
        TIMEZONE_OFFSET = 7200

        USER_AGENT_FORMAT = \
                'Instagram {app_version} Android ({android_version:d}/{android_release}; ' \
                '{dpi}; {resolution}; {brand}; {device}; {model}; {chipset}; en_SK; {version_code})'

        params = {
                'app_version': APP_VERSION,
                'android_version': ANDROID_VERSION,
                'android_release': ANDROID_RELEASE,
                'brand': PHONE_MANUFACTURER,
                'device': PHONE_DEVICE,
                'model': PHONE_MODEL,
                'dpi': PHONE_DPI,
                'resolution': PHONE_RESOLUTION,
                'chipset': PHONE_CHIPSET,
                'version_code': VERSION_CODE}
        USER_AGENT = USER_AGENT_FORMAT.format(**params)