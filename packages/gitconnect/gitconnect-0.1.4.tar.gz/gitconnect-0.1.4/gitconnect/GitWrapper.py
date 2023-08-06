# gitconnect/gitwrapper.py

import requests


class GitWrapper:
    """
    A wrapper class for the GitHub API.
    """

    BASE_URL = 'https://api.github.com'

    def __init__(self, access_token: str):
        """
        Initialize a new GitWrapper object.

        :param access_token: A personal access token for the GitHub API.
        """
        self._access_token = access_token

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """
        Send a GET request to the specified GitHub API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :param params: Optional parameters to include in the request.
        :return: The JSON response from the API.
        """
        headers = {'Authorization': f'token {self._access_token}'}
        url = f'{self.BASE_URL}{endpoint}'
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_user(self, username: str) -> dict:
        """
        Get information about a GitHub user.

        :param username: The username of the user to get information about.
        :return: A dictionary containing the user's information.
        """
        endpoint = f'/users/{username}'
        return self._get(endpoint)

    def get_repo(self, owner: str, repo_name: str) -> dict:
        """
        Get information about a GitHub repository.

        :param owner: The username or organization that owns the repository.
        :param repo_name: The name of the repository.
        :return: A dictionary containing the repository's information.
        """
        endpoint = f'/repos/{owner}/{repo_name}'
        return self._get(endpoint)

    def search_repos(self, query: str, sort: str = 'stars', order: str = 'desc') -> list:
        """
        Search for GitHub repositories based on a keyword query.

        :param query: The keyword(s) to search for.
        :param sort: The field to sort the results by. Defaults to 'stars'.
        :param order: The order to sort the results in. Defaults to 'desc'.
        :return: A list of dictionaries containing information about the matching repositories.
        """
        endpoint = '/search/repositories'
        params = {'q': query, 'sort': sort, 'order': order}
        response = self._get(endpoint, params)
        return response['items']

    def search_user_repos(self, username: str, query: str, sort: str = 'stars', order: str = 'desc') -> list:
        """
        Search for GitHub repositories for a specific user based on a keyword query.

        :param username: The username of the user to search for repositories.
        :param query: The keyword(s) to search for.
        :param sort: The field to sort the results by. Defaults to 'stars'.
        :param order: The order to sort the results in. Defaults to 'desc'.
        :return: A list of dictionaries containing information about the matching repositories.
        """
        endpoint = f'/search/repositories?q=user:{username}+{query}&sort={sort}&order={order}'
        response = self._get(endpoint)
        return response['items']
    

    def get_commits(self, owner: str, repo_name: str, branch: str = 'master') -> list:
        """
        Get a list of commits for a given repository and branch.

        :param owner: The username or organization that owns the repository.
        :str
        :param repo_name: The name of the repository.
        :type repo_name: str
        :param branch: The name of the branch to get commits for. Defaults to 'master'.
        :type branch: str
        :return: A list of dictionaries containing information about the commits.
        """
        endpoint = f'/repos/{owner}/{repo_name}/commits'
        params = {'sha': branch}
        response = self._get(endpoint, params)
        return response

    def get_commit_files(self, owner: str, repo_name: str, sha: str) -> list:
        """
        Get a list of files changed in a given commit.
        :param owner: The username or organization that owns the repository.
        :type owner: str
        :param repo_name: The name of the repository.
        :type repo_name: str
        :param sha: The SHA hash of the commit to get files for.
        :type sha: str
        :return: A list of dictionaries containing information about the files.
        """
        endpoint = f'/repos/{owner}/{repo_name}/commits/{sha}'
        response = self._get(endpoint)
        return response['files']

    def get_commit_file_content(self, owner: str, repo_name: str, path: str, sha: str) -> str:
        """
        Get the content of a file changed in a given commit.

        :param owner: The username or organization that owns the repository.
        :type owner: str
        :param repo_name: The name of the repository.
        :type repo_name: str
        :param path: The path to the file to get content for.
        :type path: str
        :param sha: The SHA hash of the commit the file was changed in.
        :type sha: str
        :return: The content of the file.
        """
        endpoint = f'/repos/{owner}/{repo_name}/contents/{path}'
        params = {'ref': sha}
        response = self._get(endpoint, params)
        return response['content']
    

    def get_source_files(self, owner: str, repo_name: str, file_extensions: list) -> list:
        """
        Get a list of source files with the specified file extensions for a given repository.

        :param owner: The username or organization that owns the repository.
        :type owner: str
        :param repo_name: The name of the repository.
        :type repo_name: str
        :param file_extensions: The list of file extensions to filter for.
        :type file_extensions: list
        :return: A list of dictionaries containing information about the source files.
        """
        endpoint = f'/repos/{owner}/{repo_name}/contents'
        response = self._get(endpoint)
        source_files = []

        for file in response:
            if file['type'] == 'file' and any(file['name'].endswith(ext) for ext in file_extensions):
                source_files.append(file)

        return source_files
    

