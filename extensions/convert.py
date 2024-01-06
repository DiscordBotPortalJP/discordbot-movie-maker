import discord
from discord import app_commands
from discord.ext import commands
from moviepy.editor import AudioFileClip, ImageClip
from daug.utils.dpyexcept import excepter

PATH_DEFAULT_IMAGE = 'icon.png'


class ConvertCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='動画生成', description='音声と画像から動画を生成します')
    @app_commands.rename(audio='音声', image='画像', comment='コメント')
    @app_commands.describe(audio='音声ファイル', image='画像ファイル', comment='動画と一緒に送信するコメント')
    @excepter
    async def _convert_movie_app_command(self, interaction: discord.Interaction, audio: discord.Attachment, image: discord.Attachment | None, comment: str = ''):
        if image is not None:
            # 何故か逆になることがあるので
            if audio.content_type.startswith('image') and image.content_type.startswith('audio'):
                audio, image = image, audio
            # ファイルが適切にアップロードされていない場合
            if not audio.content_type.startswith('audio') or not image.content_type.startswith('image'):
                await interaction.response.send_message('正しい形式のファイルを指定してください', ephemeral=True)
                return

        await interaction.response.defer()

        audio_path = f'/tmp/{audio.filename}'
        image_path = f'/tmp/{image.filename}' if image else PATH_DEFAULT_IMAGE
        movie_path = f'/tmp/output.mp4'

        with open(audio_path, 'wb') as audio_file:
            await audio.save(audio_file)

        if image is not None:
            with open(image_path, 'wb') as image_file:
                await (image or interaction.user.avatar).save(image_file)

        image_clip = ImageClip(image_path, duration=AudioFileClip(audio_path).duration)
        image_clip: ImageClip = image_clip.set_audio(AudioFileClip(audio_path))
        image_clip.write_videofile(movie_path, fps=1, codec='libx264', audio_codec='aac', temp_audiofile='temp_audiofile.m4a')
        if comment:
            await interaction.followup.send(comment, file=discord.File(movie_path, filename='output.mp4'))
        else:
            await interaction.followup.send(comment, file=discord.File(movie_path, filename='output.mp4'))


async def setup(bot: commands.Bot):
    await bot.add_cog(ConvertCog(bot))
