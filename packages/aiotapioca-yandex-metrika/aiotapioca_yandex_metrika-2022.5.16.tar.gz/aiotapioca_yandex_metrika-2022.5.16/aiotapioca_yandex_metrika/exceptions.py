class YandexMetrikaApiError(Exception):
    def __init__(self, response, message=None, *args, **kwargs):
        self.response = response
        self.message = message or ""

    def __str__(self):
        return "{} {} {}\nHEADERS = {}\nURL = {}".format(
            self.response.status,
            self.response.reason,
            self.message,
            self.response.headers,
            self.response.url,
        )


class YandexMetrikaClientError(YandexMetrikaApiError):
    def __init__(self, response, message=None, code=None, errors=None):
        super().__init__(response, message)
        self.code = code
        self.message = message
        self.errors = errors

    def __str__(self):
        return "code={}, message={}, errors={}".format(
            self.code, self.message, self.errors
        )


class YandexMetrikaServerError(YandexMetrikaClientError):
    pass


class YandexMetrikaTokenError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YandexMetrikaLimitError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YandexMetrikaDownloadReportError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.message


class BackwardCompatibilityError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return (
            "This {} is deprecated and not supported. "
            "Install a later version "
            "'pip install --upgrade async-tapi-yandex-metrika'. "
            "Info https://github.com/ilindrey/async-tapi-yandex-metrika"
        ).format(self.name)
