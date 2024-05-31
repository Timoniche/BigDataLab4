import os
import pathlib
import sys
import time

src_module_path = os.path.join(os.getcwd(), "src")
sys.path.insert(1, src_module_path)

from service import Service  # noqa: E402
from logger import Logger  # noqa: E402
from server import app, db_service  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class FunctionalApiTest:

    def __init__(
            self,
            client: TestClient,
            db: Service,
    ) -> None:
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)
        self.client = client
        self.db_service = db

    def test_post_image_check_in_db(self):
        images_dir = str(pathlib.Path(__file__).resolve().parent.parent.parent)
        img_path = images_dir + '/client_images/' + '000002.jpg'

        self.log.info(f'Image path: {img_path}')

        files = {
            'file': open(img_path, 'rb')
        }
        response = self.client.post(
            url='http://localhost:8001/upload/',
            files=files,
        )

        json = response.content.decode()

        assert response.status_code == 200
        self.log.info(f'Response json: {json}')
        ground_truth = '{"filename":"000002.jpg","is_male":"female"}'

        assert json == ground_truth, f'Expected {ground_truth}, got {json}'

        time.sleep(10)

        is_male_from_db = self.db_service.get_image_male(
            image_name='000002.jpg',
        )[0][0]

        assert is_male_from_db is False, f'Expected {False}, got {is_male_from_db}'

        self.log.info('Post Image Checkout DB Test Passed')


if __name__ == '__main__':
    mock_client = TestClient(app)
    api_test = FunctionalApiTest(mock_client, db=db_service)

    api_test.test_post_image_check_in_db()
