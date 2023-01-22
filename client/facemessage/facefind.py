import face_recognition
import shutil
import os
from database import databasefunc
from aiogram import types


class Face:

    def face_rec(self, path: str) -> bool:
        """
        проверяет есть ли лицо на фото
        :param path: path to photo
        :return: True if face in photo and False if foce not in photo
        """
        gal_face_rec = face_recognition.load_image_file(path)
        gal_face_location = face_recognition.face_locations(gal_face_rec)
        if len(gal_face_location) == 0:
            return False
        return True

    def download_photo_if_face(self, path_now: str, telegram_id: int, message: types.Message) -> bool:
        """
        сохраняет фотографию с лицом/ми в папку пользователя
        :param path_now: путь до фотографии, которую проверять будем
        :param telegram_id:
        :return: True if photo with face and OK, False if photo without face
        """
        if self.face_rec(path_now):
            path = f'database/photo_with_face/{telegram_id}user'
            if not os.path.isdir(path):
                # if the demo_folder2 directory is
                # not present then create it.
                os.makedirs(path)
            try:  # узнаём номер ГС
                num_photo = len(os.listdir(f"database/photo_with_face/{message.from_user.id}user"))
            except FileNotFoundError:
                num_photo = 0
            shutil.copy(path_now, f'{path}/{path_now.split("/")[-1].split(".")[0]}_{len(os.listdir(path))}.jpg')
            databasefunc.add_column(table='photo',
                                    name_column=f'photo{num_photo}',
                                    path=f'{path}/{path_now.split("/")[-1].split(".")[0]}_{len(os.listdir(path))}.jpg',
                                    telegramid=message.from_user.id)
            return True
        return False
