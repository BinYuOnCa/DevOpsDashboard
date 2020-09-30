import unittest
from Monitor.github import github
import asyncio


class GithubTestCases(unittest.TestCase):
    loop = None

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_fetch_commits(self):
        def process_result(result):
            commits = result.result()
            print(commits)

        task = self.loop.create_task(github.get_commits('zio', 'zio'))
        task.add_done_callback(process_result)

        self.loop.run_until_complete(task)

