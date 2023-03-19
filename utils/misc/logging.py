import logging

logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
)
