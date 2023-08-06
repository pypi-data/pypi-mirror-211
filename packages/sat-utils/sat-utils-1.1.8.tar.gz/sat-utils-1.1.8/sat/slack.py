from slack_sdk import WebClient

from sat.logs import SATLogger

logger = SATLogger(name=__name__)


class Slack:
    """
    Upload files directly to a Slack channel.
    :param token: Slack API token
    """

    def __init__(self, token):
        self.client = WebClient(token=token)

    def upload_file(self, channel, file_path, file_name, file_type, title, initial_comment):
        """
        Upload a file to Slack.
        :param channel: Slack channel to upload to
        :param file_path: Path to file to upload
        :param file_name: Name of file to upload
        :param file_type: Type of file to upload
        :param title: Will display as title of file in Slace
        :param initial_comment: Initial comment to add to file
        """
        try:
            self.client.files_upload(
                channels=channel,
                file=file_path,
                filename=file_name,
                filetype=file_type,
                title=title,
                initial_comment=initial_comment,
            )
        # TODO: Add specific exceptions
        except Exception as e:
            logger.info(f"Slack encountered an error: {e}")
