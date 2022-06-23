from typing import List

from instagrapi.exceptions import ClientError, ClientNotFoundError, MediaNotFound
from instagrapi.extractors import extract_comment
from instagrapi.types import Comment

from instagrapi import Client

from pathlib import Path
from instagrapi.types import UserShort
import datetime
from os import path, getenv

try:
    from .settings import DeviceSettings
except ImportError:
    DeviceSettings = None
    pass


class CustomClient(Client):
    def media_comments(self, media_id: str, amount: int = 20) -> List[Comment]:
        """
        Get comments on a media

        Parameters
        ----------
        media_id: str
            Unique identifier of a Media
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        List[Comment]
            A list of objects of Comment
        """
        # TODO: to public or private
        def get_comments():
            if result.get("comments"):
                for comment in result.get("comments"):
                    comments.append(extract_comment(comment))
        media_id = self.media_id(media_id)
        params = None
        comments = []
        result = self.private_request(
            f"media/{media_id}/comments/", params
        )
        get_comments()
        while ((result.get("has_more_comments") and result.get("next_max_id"))
               or (result.get("has_more_headload_comments") and result.get("next_min_id"))):
            # TODO: Add a short delay here
            try:
                if result.get("has_more_comments"):
                    params = {"max_id": result.get("next_max_id")}
                else:
                    params = {"min_id": result.get("next_min_id")}
                if not (result.get("next_max_id") or result.get("next_min_id")
                        or result.get("comments")):
                    break
                result = self.private_request(
                    f"media/{media_id}/comments/", params
                )
                get_comments()
            except ClientNotFoundError as e:
                raise MediaNotFound(e, media_id=media_id, **self.last_json)
            except ClientError as e:
                if "Media not found" in str(e):
                    raise MediaNotFound(e, media_id=media_id, **self.last_json)
                raise e
            if amount and len(comments) >= amount:
                break
        if amount:
            comments = comments[:amount]
        return comments


class Instagram:
    def __init__(self):
        self.username = getenv("IG_USERNAME")
        self.password = getenv("IG_PASSWORD")
        self.settings_filename = "ig_credentials.json"
        self.__login()

    def __login(self):
        """Establishes connection to Instagram API."""
        # get_settings()	            dict	Return settings dict
        # set_settings(settings: dict)	    bool	Set session settings
        # load_settings(path: Path)	    dict	Load session settings from file
        # dump_settings(path: Path)	    bool	Serialize and save session settings to file

        cached_settings = Path().cwd() / "cached_settings.json"

        # if saved settings, login with saved settings
        if cached_settings.exists():
            print("Reusing cached settings.")
            self.api = CustomClient()
            self.api.load_settings(cached_settings)

        # else new login and save settings
        else:
            print("New login session.")
            if self.custom_settings():
                self.api = CustomClient(self.custom_settings())
                self.api.set_country(DeviceSettings.COUNTRY)
                self.api.set_locale(DeviceSettings.LOCALE)
                self.api.set_timezone_offset(DeviceSettings.TIMEZONE_OFFSET)

            self.api.login(self.username, self.password)

            self.api.dump_settings(cached_settings)

    def custom_settings(self):
        """Creates custom device settings for client if provided."""
        if DeviceSettings:
            settings = {
                "user_agent": DeviceSettings.USER_AGENT,
                "device_settings": {
                    "cpu": DeviceSettings.PHONE_CHIPSET,
                    "dpi": DeviceSettings.PHONE_DPI,
                    "model": DeviceSettings.PHONE_MODEL,
                    "device": DeviceSettings.PHONE_DEVICE,
                    "resolution": DeviceSettings.PHONE_RESOLUTION,
                    "app_version": DeviceSettings.APP_VERSION,
                    "manufacturer": DeviceSettings.PHONE_MANUFACTURER,
                    "version_code": DeviceSettings.VERSION_CODE,
                    "android_release": DeviceSettings.ANDROID_RELEASE,
                    "android_version": DeviceSettings.ANDROID_VERSION
                }
            }
            return settings
        return None

    def fetch_posts(self, user_id: int, max_posts=12, step=1):
        """Fetch User's posts."""
        media = self.api.user_medias(user_id=user_id, amount=max_posts)

        return media[::step]


if __name__ == '__main__':
    ig = Instagram()
    # user_id = int(ig.api.user_id_from_username(ig.username))
    print(ig.api.media_comments(media_id="Ceg76-8PXEm"))
    # media_pk = ig.api.media_pk_from_code("Ceg76-8PXEm")
    # comms = ig.api.media_comments(ig.api.media_id(media_pk))
    # print(comms)

    # Get user's media
    # media = ig.fetch_posts(user_id=user_id)

    # Get comments of specified media
    # comms = ig.api.media_comments(media_id="2861207262736991941_49645699606")
    # print(comms)

    # Send a direct message to a user/list of users
    # ig.api.direct_send(user_ids=[5386485074], text="Bitcoin went under 20.000$!")

    # Delete media comments
    # ig.api.comment_bulk_delete()
