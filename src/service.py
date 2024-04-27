from database import Database
from logger import Logger
from repository.image_predictions_dao import ImagePredictionsDAO


class Service:
    def __init__(self, db: Database):
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)

        self.imagedao = ImagePredictionsDAO(db)

    def init_db(self):
        self.log.info('Initializing image_prediction table')
        self.imagedao.init_table()

    def save_image_prediction(
            self,
            image_name: str,
            is_male: bool,
    ):
        self.log.info('Saving image to db: {} is_male: {}'.format(image_name, is_male))
        self.imagedao.insert_image_predictions(
            image_name=image_name,
            is_male=is_male,
        )

    def get_image_male(
            self,
            image_name: str,
    ):
        self.log.info('Selecting image from db: {}'.format(image_name))
        return self.imagedao.select_image_predictions(
            image_name=image_name,
        )
