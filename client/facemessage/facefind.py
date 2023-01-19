import face_recognition
import shutil
import os


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

    def download_photo_if_face(self, path_now: str, telegram_id: int) -> bool:
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
            shutil.copy(path_now, f'{path}/{path_now.split("/")[-1].split(".")[0]}_{len(os.listdir(path))}.jpg')
            return True
        return False
