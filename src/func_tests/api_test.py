import os
import pathlib
import sys

src_module_path = os.path.join(os.getcwd(), "src")
sys.path.insert(1, src_module_path)

from database import Database  # noqa: E402
from service import Service  # noqa: E402
from utils.common_utils import generate_time_id  # noqa: E402
from logger import Logger  # noqa: E402
from server import app, db_service  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class FunctionalApiTest:

    def __init__(
            self,
            client: TestClient,
            db_service: Service,
    ) -> None:
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)
        self.client = client
        self.db_service = db_service

    def test_post_image_check_in_db(self):
        images_dir = str(pathlib.Path(__file__).resolve().parent.parent.parent)
        img_path = images_dir + '/client_images/' + '000002.jpg'

        self.log.info(f'Image path: {img_path}')

        files = {
            'file': open(img_path, 'rb')
        }
        response = self.client.post(
            url='http://localhost:8000/upload/',
            files=files,
        )

        json = response.content.decode()

        assert response.status_code == 200
        self.log.info(f'Response json: {json}')
        ground_truth = '{"filename":"000002.jpg","is_male":"female"}'

        assert json == ground_truth, f'Expected {ground_truth}, got {json}'

        is_male_from_db = self.db_service.get_image_male(
            image_name='000002.jpg',
        )[0][0]

        assert is_male_from_db is False, f'Expected {False}, got {is_male_from_db}'

        self.log.info('Post Image Checkout DB Test Passed')

    # def test_upload_photo(self):
    #     images_dir = str(pathlib.Path(__file__).resolve().parent.parent.parent)
    #     print(images_dir)
    #     img_path = images_dir + '/client_images/' + '000002.jpg'
    #
    #     files = {
    #         'file': open(img_path, 'rb')
    #     }
    #     response = self.client.post(
    #         url='http://localhost:8000/upload/',
    #         files=files,
    #     )
    #
    #     json = response.content.decode()
    #
    #     assert response.status_code == 200
    #     self.log.info(f'Response json: {json}')
    #     ground_truth = '{"filename":"000002.jpg","is_male":"female"}'
    #
    #     assert json == ground_truth, f'Expected {ground_truth}, got {json}'
    #
    #     self.log.info('Server Test Passed')
    #
    # def test_db_upload_photo(self):
    #     db = Database()
    #     service = Service(db)
    #
    #     filename = generate_time_id()
    #     self.log.info(f'filename: {filename}')
    #
    #     service.save_image_prediction(
    #         image_name=filename,
    #         is_male=True,
    #     )
    #
    #     is_male_from_db = service.get_image_male(
    #         image_name=filename,
    #     )[0][0]
    #
    #     assert is_male_from_db is True, f'Expected {True}, got {is_male_from_db}'
    #
    #     self.log.info('Db Test Passed')


if __name__ == '__main__':
    mock_client = TestClient(app)
    api_test = FunctionalApiTest(mock_client, db_service=db_service)

    api_test.test_post_image_check_in_db()
    # api_test.test_upload_photo()
    # api_test.test_db_upload_photo()
