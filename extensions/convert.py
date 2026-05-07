import functools

import discord
from discord import app_commands
from discord.ext import commands

try:
    from daug.utils.dpyexcept import excepter
except Exception:
    # 環境変数未設定などで dpyexcept の import に失敗した場合は no-op decorator を利用する
    def excepter(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

try:
    from moviepy import AudioFileClip, ImageClip
except ImportError:
    from moviepy.editor import AudioFileClip, ImageClip

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
            audio_type = audio.content_type or ''
            image_type = image.content_type or ''
            # 何故か逆になることがあるので
            if audio_type.startswith('image') and image_type.startswith('audio'):
                audio, image = image, audio
                audio_type, image_type = image_type, audio_type
            # ファイルが適切にアップロードされていない場合
            if not audio_type.startswith('audio') or not image_type.startswith('image'):
                await interaction.response.send_message('正しい形式のファイルを指定してください', ephemeral=True)
                return

        await interaction.response.defer()

        audio_path = f'/tmp/{audio.filename}'
        image_path = f'/tmp/{image.filename}' if image else PATH_DEFAULT_IMAGE
        movie_path = '/tmp/output.mp4'

        with open(audio_path, 'wb') as audio_file:
            await audio.save(audio_file)

        if image is not None:
            with open(image_path, 'wb') as image_file:
                await image.save(image_file)

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).with_duration(audio_clip.duration)
        image_clip = image_clip.with_audio(audio_clip)
        image_clip.write_videofile(movie_path, fps=1, codec='libx264', audio_codec='aac', temp_audiofile='temp_audiofile.m4a')

        await interaction.followup.send(comment or None, file=discord.File(movie_path, filename='output.mp4'))


async def setup(bot: commands.Bot):
    await bot.add_cog(ConvertCog(bot))
