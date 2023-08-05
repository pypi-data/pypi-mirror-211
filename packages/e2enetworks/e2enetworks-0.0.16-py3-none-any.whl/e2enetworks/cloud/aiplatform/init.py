from e2enetworks.cloud.aiplatform import config


class init:
    def __init__(self, apikey, access_token):
        config.apikey = apikey
        config.access_token = access_token

