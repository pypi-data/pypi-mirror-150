import redis

from datetime import datetime
from time import sleep

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import ImageInstance


class DataContainer(object):
    """
    Simple data container.
    """

    def __init__(self):
        self.redis: redis.Redis = None
        self.channel_out: str = "images"
        self.channel_in: str = "predictions"
        self.timeout: float = 5.0
        self.data = None


class BasePredict(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Base class for Stream processors that make predictions via Redis backend.
    """

    redis_host: str = TypedOption(
        "-h", "--redis-host",
        type=str,
        default="localhost",
        help="the Redis server to connect to"
    )

    redis_port: int = TypedOption(
        "-p", "--redis-port",
        type=int,
        default=6379,
        help="the port the Redis server is running on"
    )

    redis_db: int = TypedOption(
        "-d", "--redis-db",
        type=int,
        default=0,
        help="the database to use"
    )

    channel_out: str = TypedOption(
        "--channel-out",
        type=str,
        default="images",
        help="the Redis channel to send the images out"
    )

    channel_in: str = TypedOption(
        "--channel-in",
        type=str,
        default="predictions",
        help="the Redis channel on which to receive predictions."
    )

    timeout: float = TypedOption(
        "-t", "--timeout",
        type=float,
        default=5.0,
        help="the timeout in seconds to wait for a prediction to arrive"
    )

    verbose: bool = FlagOption(
        "-v", "--verbose",
        help="whether to output debugging information."
    )

    def _process_predictions(self, element, data, then, done):
        """
        Processes the prediction data.

        :param element: the incoming image
        :param data: the data to process
        :param then: the function to call with the parsed prediction data
        :param done: if necessary to call
        :return:
        """
        raise NotImplementedError()

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_redis_conn"):
            self._redis_conn = DataContainer()
            self._redis_conn.redis = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
            self._redis_conn.channel_out = self.channel_out
            self._redis_conn.channel_in = self.channel_in
            self._redis_conn.timeout = self.timeout
            self._redis_conn.data = None

        def anon_handler(message):
            data = message['data']
            self._redis_conn.data = data
            self._redis_conn.pubsub_thread.stop()
            self._redis_conn.pubsub.close()
            self._redis_conn.pubsub = None

        self._redis_conn.pubsub = self._redis_conn.redis.pubsub()
        self._redis_conn.pubsub.psubscribe(**{self._redis_conn.channel_in: anon_handler})
        self._redis_conn.pubsub_thread = self._redis_conn.pubsub.run_in_thread(sleep_time=0.001)
        self._redis_conn.redis.publish(self._redis_conn.channel_out, element.data.data)

        # wait for data to show up
        start = datetime.now()
        no_data = False
        while self._redis_conn.pubsub is not None:
            sleep(0.001)
            end = datetime.now()
            if self._redis_conn.timeout > 0:
                if (end - start).total_seconds() >= self._redis_conn.timeout:
                    if self.verbose:
                        self.logger.info("Timeout reached!")
                    no_data = True
                    break

        if no_data:
            return
        elif self.verbose:
            end = datetime.now()
            self.logger.info("Round trip time: %f sec" % (end - start).total_seconds())

        # process predictions
        self._process_predictions(element, self._redis_conn.data, then, done)
