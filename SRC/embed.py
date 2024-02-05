from discord import Embed, ui, ButtonStyle
from SRC import datamanip

async def send_embed(title: str, description: str, color: int, fields, channel):
	embed = Embed(title=title, description=description, color=color)
	if fields:
		for field in fields:
			embed.add_field(name=field.name, value=field.description, inline=False)
	await channel.send(content="@everyone", embed=embed)

async def send_add_selection(self, ctx, color: int):
	embed = Embed(title="Entreprise Selection", description="Please select an entreprise you are intresed in", color=color)
	view = await self.get_view_for_ent_timeslots(ctx.author.nick.split(',')[0])
	await ctx.respond(content="@everyone", embed=embed, view=view, ephemeral=True)