import aiohttp
import asyncio

async def send_post_request(url, json_data=None):
	async with aiohttp.ClientSession() as session:
		async with session.post(url, json=json_data) as response:
			return await response.text()