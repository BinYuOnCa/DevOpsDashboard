import asyncio
import configparser
import aiohttp
import os, sys


async def get_urls():
    config = await __get_config()
    conf = config['DEFAULT']
    return conf['github.url']


async def __get_config():
    try:
        config_folder = os.environ['PYTHONHOME']
    except KeyError:
        config_folder = os.path.dirname(os.path.dirname(sys.executable))

    if not os.path.exists(config_folder + "/conf/config.properties"):
        path = os.path.dirname(__file__)
        config_folder = path + "/../"

    print("Load config from folder %s" % config_folder)

    config = configparser.ConfigParser()
    config.read(config_folder + "/conf/config.properties")
    return config


async def get_commits(user, repo):
    url = (await get_urls()) + "/repos/%s/%s/commits" % (user, repo)
    http_client = aiohttp.ClientSession()
    try:
        resp = await http_client.get(url, ssl=False)
        if resp.status == 200:
            body = await resp.json()
            return body
        else:
            resp.raise_for_status()
    finally:
        await http_client.close()

