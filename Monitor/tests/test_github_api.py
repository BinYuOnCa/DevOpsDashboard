import unittest
from github import github


class GithubTestCases(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_commits(self):
        commits = await github.get_commits('zio', 'zio')
        print(len(commits))
        self.assertTrue(len(commits) == 30)

