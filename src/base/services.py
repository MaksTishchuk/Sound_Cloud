import os

from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file):
    """Генерация пути к файлу аватара. Format: media/avatar/user_id/photo.jpg
    instance - объект пользователя.
    """
    return f'avatar/user_{instance.id}/{file}'


def get_path_upload_cover_album(instance, file):
    """Генерация пути к файлу обложки альбома. Format: media/album/user_id/photo.jpg
    instance - объект пользователя.
    """
    return f'album/user_{instance.user.id}/{file}'


def get_path_upload_track(instance, file):
    """Генерация пути к файлу трека. Format: media/track/user_id/music.mp3
    instance - объект пользователя.
    """
    return f'track/user_{instance.user.id}/{file}'


def get_path_upload_cover_track(instance, file):
    """Генерация пути к файлу обложки трека. Format: media/track/cover/user_id/photo.jpg
    instance - объект пользователя.
    """
    return f'track/cover/user_{instance.user.id}/{file}'


def get_path_upload_cover_play_list(instance, file):
    """Генерация пути к файлу обложки плейлиста. Format: media/play_list/user_id/photo.jpg
    instance - объект пользователя.
    """
    return f'play_list/user_{instance.user.id}/{file}'


def validate_size_image(file_obj):
    """Проверка размера файла"""

    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла - {megabyte_limit}MB')


def delete_old_file(path_file):
    """Удаление старого файла"""

    if os.path.exists(path_file):
        os.remove(path_file)


