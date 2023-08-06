import re
import requests


class AI:

    def __init__(self, rapid_api_key: str):

        if not isinstance(rapid_api_key, str):
            raise TypeError(
                        'rapid_api_key must be a string, ',
                        'got ' + type(rapid_api_key).__name__
            )

        self.url = 'https://crypto-ai.p.rapidapi.com{0}'
        self.headers = {
                "X-RapidAPI-Host": "crypto-ai.p.rapidapi.com",
                "X-RapidAPI-Key": rapid_api_key,
        }

        self.timeframes = [
                "1m", "3m", "5m", "15m", "30m",
                "1h", "2h", "4h", "6h", "8h", "12h",
                "1d", "3d",
        ]

        self.timelines = [
                '5m', '15m', '30m',
                '1h', '3h', '6h', '12h',
                '1d', '2d', '3d',
                '1w', '2w'
        ]

    class exceptions:
        class InvalidRapidAPIKey(ValueError):
            pass
        class InvalidSymbol(ValueError):
            pass
        class SymbolTooYoung(ValueError):
            pass
        class SymbolNotFound(ValueError):
            pass
        class UnknownError(Exception):
            pass


    def __validate_args(self, endpoint: str, args: dict):

        if endpoint not in ['/predict', '/forecast']:
            raise ValueError(
                        'invalid endpoint'
            )

        symbol    = args.get('symbol')
        timeframe = args.get('timeframe')
        timeline  = args.get('timeline')

        if not isinstance(symbol, str):
            raise TypeError(
                        'symbol must be a string, ',
                        'got ' + type(symbol).__name__
            )

        # Uppercase the symbol
        symbol = symbol.upper()

        if not re.match('^[A-Z0-9]{6,11}$', symbol):
            raise ValueError(
                        'invalid symbol'
            )

        if endpoint == '/predict':

            if timeframe:

                if not isinstance(timeframe, str):
                    raise TypeError(
                                'timeframe must be a string, ',
                                'got ' + type(timeframe).__name__
                    )

                # Lowercase the timeframe
                timeframe = timeframe.lower()

                if timeframe not in self.timeframes:
                    raise ValueError(
                                'invalid timeframe'
                    )


            elif timeline:

                if not isinstance(timeline, str):
                    raise TypeError(
                                'timeline must be a string, ',
                                'got ' + type(timeline).__name__
                    )

                # Lowercase the timeline
                timeline = timeline.lower()

                if timeline not in self.timelines:
                    raise ValueError(
                                'invalid timeline'
                    )

            else:
                raise ValueError(
                            'received no timeframe nor timeline'
                )


    def predict(self, symbol: str, timeframe: str=None, timeline: str=None) -> dict:

        # Raise an exception if any of the provided
        # arguments is invalid
        self.__validate_args(
                        '/predict',
                        locals()
        )

        # =======================================================

        params = {
            'symbol': symbol,
        }

        if timeframe:
            params['timeframe'] = timeframe

        elif timeline:
            params['timeline'] = timeline

        # =======================================================

        response = requests.get(
                            self.url.format('/predict'),
                            params=params,
                            headers=self.headers
                   ).json()

        # =======================================================

        status = response.get('status')
        if not status:

            message = response.get('message')
            if message:
                if 'not subscribed' in message:
                    raise self.exceptions.InvalidRapidAPIKey

            raise self.exceptions.UnknownError(str(response))

        # =======================================================

        if response['status'] != 'ok':

            if 'invalid symbol' in response['message']:
                raise self.exceptions.InvalidSymbol

            if 'not find' in response['message']:
                raise self.exceptions.SymbolNotFound

            if 'too young' in response['message']:
                raise self.exceptions.SymbolTooYoung

            raise self.exceptions.UnknownError(response['message'])

        # =======================================================

        return response


    def forecast(self, symbol: str) -> dict:

        # Raise an exception if any of the provided
        # arguments is invalid
        self.__validate_args(
                        '/forecast',
                        locals()
        )

        # =======================================================

        params = {
            'symbol': symbol,
        }

        # =======================================================

        response = requests.get(
                            self.url.format('/forecast'),
                            params=params,
                            headers=self.headers
                   ).json()

        # =======================================================

        status = response.get('status')
        if not status:

            message = response.get('message')
            if message:
                if 'not subscribed' in message:
                    raise self.exceptions.InvalidRapidAPIKey

            raise self.exceptions.UnknownError(str(response))

        # =======================================================

        if response['status'] != 'ok':

            if 'invalid symbol' in response['message']:
                raise self.exceptions.InvalidSymbol

            if 'not find' in response['message']:
                raise self.exceptions.SymbolNotFound

            raise self.exceptions.UnknownError(response.message)

        # =======================================================

        return response
