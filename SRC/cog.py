import discord, json
from discord import Embed, ui, ButtonStyle
from discord.ext import commands, tasks
from SRC import embed, datamanip, requestToForm

LINK='Google drive link for request'

class Easyflow(commands.Cog):
    def __init__(self, bot, guild_id, channel_id):
        self.bot = bot
        self.commands = None
        self.guild_id = guild_id
        self.channel = channel_id
        self.bot.slash_command(guild_ids=[guild_id], description="Add a time slot")(self.add)
        self.bot.slash_command(guild_ids=[guild_id], description="Create a new student file")(self.new_file)
        self.bot.slash_command(guild_ids=[guild_id], description="Update your email address")(self.update_email)
        self.bot.slash_command(guild_ids=[guild_id], description="Update your resume link")(self.update_cv)
        self.bot.slash_command(guild_ids=[guild_id], description="Update your linkdin profile link")(self.update_linkdin)
        self.bot.slash_command(guild_ids=[guild_id], description="dl json")(self.ping_down)
        self.bot.slash_command(guild_ids=[guild_id], description="ul json")(self.ping_up)

    async def add_date_selection(self, interaction, EntName, color: int):
        content = f" ***{EntName}*** Selected"
        title = "Please select a date you are intrested in :"
        embed = Embed(title=title, description=None, color=color)
        view = await self.get_view_for_timeslots(interaction.user.nick.split(',')[0], EntName)
        return content, embed, view

    async def callback(self, interaction):
        info = str(interaction.custom_id).split(".")
        if (info[0] == "ENT"):
            content, embed, view = await self.add_date_selection(interaction, info[1], 0x00ff00)
        elif (info[0] == "DAT"):
            await datamanip.reserve_ent_slot(interaction.user.nick.split(',')[0], info[1], info[2])
            await datamanip.reserve_std_slot(interaction.user.nick.split(',')[0], info[1], info[2])
            content = f"Rdv avec  **{info[2]}** pour **{info[1]}** confirmé!"
            embed = None
            view = None
        else:
            content = "Tand pis pour toi..."
            embed = None
            view = None
        await interaction.response.edit_message(content=content, embed=embed, view=view)

    async def get_view_for_timeslots(self, stdlog, ent):
        view = ui.View()
        allentdata = await datamanip.get_free_ent_slot()
        entfreetime = []
        for line in allentdata:
            if (line["ent"] == ent):
                entfreetime.append(line["slot"])
        studentdata = await datamanip.get_student_data(stdlog)
        stdslots = await datamanip.freespot_std_from_data(studentdata)
        mutual_data = list(set(entfreetime) & set(stdslots))
        if (mutual_data):
            for slot in mutual_data:
                button = (ui.Button(custom_id=f"DAT.{slot}.{ent}", label=slot, style=ButtonStyle.primary))
                button.callback = self.callback
                view.add_item(button)
        button = (ui.Button(custom_id=f"QUIT.", label="' j'ai changer d'avis' ", style=ButtonStyle.primary))
        button.callback = self.callback
        view.add_item(button)
        return view

    async def get_view_for_ent_timeslots(self, stdlog):
        view = ui.View()

        studentdata = await datamanip.get_student_data(stdlog)
        free_ent_slot = await datamanip.get_free_ent_slot()
        ent = []
        for line in free_ent_slot:
            if (line["ent"] not in ent):
                ent.append(line["ent"])
        ent_in_studentdata = []
        for i in range(len(studentdata["slots"])):
            if (studentdata["slots"][i]["usage"] not in ent_in_studentdata) & (studentdata["slots"][i]["usage"] != "None"):
                ent_in_studentdata.append(studentdata["slots"][i]["usage"])
        mutual_exclusive_data = list(set(ent) - set(ent_in_studentdata))
        for ent in mutual_exclusive_data:
            button = (ui.Button(custom_id=f"ENT.{ent}", label=ent, style=ButtonStyle.primary))
            button.callback = self.callback
            view.add_item(button)
        button = (ui.Button(custom_id=f"QUIT.", label="' j'ai changer d'avis' ", style=ButtonStyle.primary))
        button.callback = self.callback
        view.add_item(button)
        return view

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Initialized {self.__class__.__name__}")
        print(discord.__version__)
        self.commands = self.bot.commands
        self.send_reminder.start()

    @tasks.loop(hours=1)
    async def send_reminder(self):
        guild = await self.bot.fetch_guild(self.guild_id)
        channel = await guild.fetch_channel(self.channel)
        await embed.send_embed("Entreprise dating !", "n'oublier pas de vous inscrire a votre date !!!", 0x00ff00, self.commands, channel)

    async def update_email(self, ctx, email):
        if (await datamanip.check_student_file(ctx.author.nick.split(',')[0])):
            await datamanip.update_data(ctx.author.nick.split(',')[0], "email", email)
            studentdata = await datamanip.get_student_data(ctx.author.nick.split(',')[0])
            content = f"Your mail is now **{studentdata['email']}**"
        else:
            content = f"{ctx.author.nick.split(',')[0]} You are not registered please use /new_file first !"
        await ctx.respond(content, ephemeral=True)

    async def update_cv(self, ctx, cvlink):
        if (await datamanip.check_student_file(ctx.author.nick.split(',')[0])):
            await datamanip.update_data(ctx.author.nick.split(',')[0], "cvlink", cvlink)
            studentdata = await datamanip.get_student_data(ctx.author.nick.split(',')[0])
            content = f"Your cv link is now **{studentdata['cvlink']}**"
        else:
            content = f"{ctx.author.nick.split(',')[0]} You are not registered please use /new_file first !"
        await ctx.respond(content, ephemeral=True)

    async def update_linkdin(self, ctx, linkdin):
        if (await datamanip.check_student_file(ctx.author.nick.split(',')[0])):
            await datamanip.update_data(ctx.author.nick.split(',')[0], "linkdin", linkdin)
            studentdata = await datamanip.get_student_data(ctx.author.nick.split(',')[0])
            content = f"Your linkdin is now **{studentdata['linkdin']}**"
        else:
            content = f"{ctx.author.nick.split(',')[0]} You are not registered please use /new_file first !"
        await ctx.respond(content, ephemeral=True)

    async def new_file (self, ctx, name, surname):
        if not (await datamanip.check_student_file(ctx.author.nick.split(',')[0])):
            await datamanip.create_student_file(ctx.author.nick.split(',')[0], name, surname)
            user = await datamanip.get_student_data(ctx.author.nick.split(',')[0])
            if user:
                content = f"You are now registered as {user['name']} {user['surname']}"
                if (user["cvlink"] == "None"):
                    content += "\nPlease provide a link to your resume /update_cv"
                if (user["email"] == "None"):
                    content += "\nPlease provide an email /update_email"
                if (user["linkdin"] == "None"):
                    content += "\nPlease provide a link to your linkdin (if you have one) /update_linkdin"
                await ctx.respond(content, ephemeral=True)
        else:
            await ctx.respond(f"{ctx.author.nick.split(',')[0]} You are already registered", ephemeral=True)

    async def ping_down(self, ctx):
        await datamanip.make_new_ent_json(await requestToForm.send_post_request(LINK))
        await ctx.respond("json overwritten", ephemeral=True)

    async def ping_up(self, ctx):
        entjson = await datamanip.get_ent_data()
        await requestToForm.send_post_request(LINK, entjson)
        await ctx.respond("json uploaded", ephemeral=True)
    async def add(self, ctx):
        if (await datamanip.check_student_file(ctx.author.nick.split(',')[0])):
            await embed.send_add_selection(self, ctx, 0x00ff00)
        else:
            await ctx.respond(f"{ctx.author.nick.split(',')[0]} You are not registered please use /new_file first !", ephemeral=True)