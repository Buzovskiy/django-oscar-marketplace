import glob
import os
import imghdr
import re
import time
from pathlib import Path, PurePosixPath
from django.conf import settings


class FileCore:


    def __init__(self, upload_to, file_name=None):
        """
        upload_to - '1c/temp/images/'
        file_name - import_files/ps/some-image.jpg
        full_path - ..weestep-brand.eu\project\media-test\1c\temp\images\import_files\ps\some-image.jpg
        relative_path - 1c\temp\images\import_files\ps\some-image.jpg
        url - /media/1c/temp/images/import_files/ps/some-image.jpg
        """
        self.__upload_to = upload_to
        Path(settings.MEDIA_ROOT / self.__upload_to).mkdir(parents=True, exist_ok=True)
        if file_name is not None:
            self.__full_path = Path(settings.MEDIA_ROOT / self.__upload_to / file_name)
            self.__relative_path = self.__full_path.relative_to(settings.MEDIA_ROOT)
            self.__file_name = file_name
            url_segments_list = [str(PurePosixPath(s)) for s in [settings.MEDIA_URL, self.__relative_path]]
            self.__url = '/' + '/'.join(s.strip('/') for s in url_segments_list)

    @property
    def file_name(self):
        return self.__file_name

    @property
    def url(self):
        return self.__url

    @property
    def upload_to(self):
        return self.__upload_to

    @property
    def full_path(self):
        return self.__full_path

    @property
    def relative_path(self, test=None):
        return self.__relative_path

    @property
    def is_image(self):
        return False if imghdr.what(self.full_path) is None else True

    @property
    def date_created(self):
        return time.ctime(os.path.getmtime(self.full_path))

    @property
    def size(self):
        return f'{round(os.path.getsize(self.full_path) / (1024 * 1024), 2)} MB'

    def save_file(self, content):
        with open(self.__full_path, mode='wb') as f:
            f.write(content)

    def remove(self):
        if self.file_name is None:
            return False
        Path(self.full_path).unlink(missing_ok=True)
        self.remove_empty_dirs()

    def remove_empty_dirs(self):
        src_dir = settings.MEDIA_ROOT / self.upload_to
        for dir_path, _, _ in os.walk(src_dir, topdown=False):  # Listing the files
            if dir_path == str(src_dir):
                break
            try:
                os.rmdir(dir_path)
            except OSError as ex:
                pass

    def get_name_parts(self):
        """
        Method that processes a name of the file and returns tuple.
        The first element of a tuple is 1c product extended id.
        The second is image order.
        E.g., if image file name is '3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg' return is
        ('3cb3474f-d9a8-11e9-81dc-2c4d5446690f', 0)
        if '3cb3474f-d9a8-11e9-81dc-2c4d5446690f_1' return is
        ('3cb3474f-d9a8-11e9-81dc-2c4d5446690f', 1)
        :return: (tuple)
        """
        if not self.is_image:
            return None
        # File name without path and extension, e.g 3cb3474f-d9a8-11e9-81dc-2c4d5446690f
        file_name_no_ext = self.full_path.stem
        match_obj = re.search(r'^([0-9A-Za-z-]{36})(?:_(\d))?$', file_name_no_ext)
        if match_obj is None:
            return None
        return match_obj.group(1), int(match_obj.group(2)) if match_obj.group(2) else 0


class FileImage(FileCore):
    def __init__(self, file_name=None):
        """
        :param file_name: this is a path that is related to upload_to path.
        may by just the name of the file, i.e: image.jpg. In this case the full
        relational path is 1c/temp/images/image.jpg.
        """
        self.__upload_to = '1c/temp/images/'
        super(FileImage, self).__init__(upload_to='1c/temp/images/', file_name=file_name)


class FileXml(FileCore):
    def __init__(self, file_name=None):
        super(FileXml, self).__init__(upload_to='1c/temp/xml/', file_name=file_name)

    def save_part(self, filename, content):
        """
        Saves the parts of the file
        :param content: byte code of the file
        :param filename: the name of the file, i.e import.xml or offers.xml
        """
        # определяем индекс файла
        index = len(glob.glob(str(Path(settings.MEDIA_ROOT / self.upload_to / f'{filename}.part*'))))
        # сохраняем файл
        with open(settings.MEDIA_ROOT / self.upload_to / f'{filename}.part{index}', mode='wb') as f:
            f.write(content)

    def make_file(self, filename):
        # get temp files, if they do not exist, suppose they are merged
        partfiles = sorted(glob.glob(str(settings.MEDIA_ROOT / self.upload_to / f'{filename}.part*')))
        if not len(partfiles):
            return

        new_filename = filename
        with open(settings.MEDIA_ROOT / self.upload_to / new_filename, mode='a+b') as f:
            for file in partfiles:
                with open(file, mode='rb') as part_f:
                    f.write(part_f.read())
                Path(file).unlink()


def get_images_list():
    image_obj = FileImage()
    files_list = []
    for root, dirs, files in os.walk(settings.MEDIA_ROOT / image_obj.upload_to, topdown=False):
        for name in files:
            file_path = Path(os.path.join(root, name))
            # Get relative path to temp/images directory
            file_path_rel = file_path.relative_to(settings.MEDIA_ROOT / image_obj.upload_to)
            files_list.append(FileImage(file_path_rel))
    return files_list
