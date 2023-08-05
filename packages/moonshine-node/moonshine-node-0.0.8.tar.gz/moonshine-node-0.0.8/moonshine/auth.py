import requests
from typing import Union
import os


class auth:
    api_url = os.environ.get('AUTH_API_URL', 'http://msws-auth-api')

    @classmethod
    def get_token(cls, username: str, password: str) -> (bool, str):
        """
        Get auth token by moonshine AD account.

        :param username: AD username.
        :param password: AD password.
        :return: tuple(is_success, token/message).
        """
        resp = requests.post(
            f'{cls.api_url}/login',
            auth=(username, password)
        )

        return resp.ok, resp.text

    @classmethod
    def validate_token(cls, token: str=None) -> (bool, Union[dict, str]):
        """
        Check whether auth token is valid.
        Using cookie instead if token arg not specified.

        :param token: auth token to validate.
        :return: tuple(is_success, {username, token}/message).
        """
        if token is None:
            from flask import request
            cookies = request.cookies
            if 'auth_token' in cookies:
                token = cookies['auth_token']
            else:
                authorization = request.headers.get('Authorization')
                if authorization is None or not authorization.startswith('auth_token'):
                    return 'No token founded.', 401
                tokens = authorization.split()
                if len(tokens) != 2:
                    return 'invalid Authorization!', 401
                token = tokens[1]

        cookies = {'auth_token': token}

        try:
            resp = requests.get(
                f'{cls.api_url}/validate',
                cookies=cookies
            )
        except requests.exceptions.ConnectionError as error:
            raise requests.exceptions.ConnectionError(
                'In dev environment? Use env "AUTH_API_URL" instead.'
            ) from error

        if resp.ok:
            return True, resp.json()
        return False, resp.text

    @classmethod
    def get_user_info(cls, token: str=None) -> (bool, Union[dict, str]):
        """
        Get user info by token.
        Using cookie instead if token arg not specified.

        :param token: user info to received.
        :return: tuple(is_success, user_info/message).
        """
        result, data = cls.validate_token(token)
        if isinstance(result, str):
            return False, result
        if not result:
            return result, data

        cookies = {'auth_token': data['token']}
        resp = requests.get(
            f'{cls.api_url}/user',
            cookies=cookies
        )

        if resp.ok:
            return True, resp.json()
        return False, resp.text
