import discord
import os
import dotenv
from discord.ext import commands
from settingtoken import token
import aiohttp

# intents = discord.Intents().all()
# client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='$A ', intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Denny"))
    print('Login {0.user}'.format(bot))


#commands view member profile
@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(title = member).set_image(url = member.avatar.url)
    await ctx.send(embed = embed)

#commands invite link
@bot.command()
async def invitelink(ctx):
    await ctx.send(' ### Invite Link ### \n Your link discord server ')

#commands add emoji
@bot.command()
#hanyak akses ascended guest yang bisa mengakses command ini
@commands.has_role('Ascended Guest')
async def addemoji(ctx, *, name=None):

    if len(ctx.message.attachments) == 0:
        await ctx.send('Mohon sertakan gambar untuk menambahkan emoji.')
        return

    # Mengecek afakah guild ada slot emoji yang tersedia
    if len(ctx.guild.emojis) >= ctx.guild.emoji_limit:
        await ctx.send('Maaf, emoji sudah penuh.')
        return

    # Mengambil gambar yang dilampirkan
    attachment = ctx.message.attachments[0]
    image_url = attachment.url

    # Mengecek ukuran file gambar
    if attachment.size > 256000:
        await ctx.send('Maaf, gambar terlalu besar. Maksimal ukuran file adalah 256 KB.')
        return

    # Mendownload gambar dan mengubahnya menjadi emoji
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image_data = await resp.read()
        emoji_name = name or attachment.filename[:-4]
        emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=image_data)
        await ctx.send(f'Emoji {emoji.name} berhasil ditambahkan.')

        # Edit nama emoji jika argumen name ada
        if name:
            await emoji.edit(name=name)
            await ctx.send(f'Nama emoji berhasil diubah menjadi {emoji.name}.')
    except discord.HTTPException:
        await ctx.send('Maaf, terjadi kesalahan saat menambahkan atau mengedit emoji.')
    
@addemoji.error
async def addemoji_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Anda tidak memiliki akses untuk menggunakan perintah ini.')
    else:
        await ctx.send('Terjadi kesalahan saat menjalankan perintah.')
    
bot.run(token)