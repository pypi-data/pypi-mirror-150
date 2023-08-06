# wai-annotations-redis-predictions
wai.annotations plugin for making predictions via models communication through Redis backend.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins
### REDIS-PREDICT-IC
Makes image classification predictions via Redis backend, passing in an image and receiving JSON predictions back (at least one of 'label: probability').
Predictions example:
{"dog": 0.9, "cat": 0.1}

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: redis-predict-ic [--channel-in CHANNEL_IN] [--channel-out CHANNEL_OUT] [-d REDIS_DB] [-h REDIS_HOST] [-p REDIS_PORT] [-t TIMEOUT] [-v]

optional arguments:
  --channel-in CHANNEL_IN
                        the Redis channel on which to receive predictions.
  --channel-out CHANNEL_OUT
                        the Redis channel to send the images out
  -d REDIS_DB, --redis-db REDIS_DB
                        the database to use
  -h REDIS_HOST, --redis-host REDIS_HOST
                        the Redis server to connect to
  -p REDIS_PORT, --redis-port REDIS_PORT
                        the port the Redis server is running on
  -t TIMEOUT, --timeout TIMEOUT
                        the timeout in seconds to wait for a prediction to arrive
  -v, --verbose         whether to output debugging information.
```


### REDIS-PREDICT-IS
Makes image segmentation predictions via Redis backend, passing in an image and receiving an image with predicted segmentations.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: redis-predict-is [--channel-in CHANNEL_IN] [--channel-out CHANNEL_OUT] [--image-format IMAGE_FORMAT] --labels LABEL [LABEL ...] [-d REDIS_DB] [-h REDIS_HOST] [-p REDIS_PORT] [-t TIMEOUT] [-v]

optional arguments:
  --channel-in CHANNEL_IN
                        the Redis channel on which to receive predictions.
  --channel-out CHANNEL_OUT
                        the Redis channel to send the images out
  --image-format IMAGE_FORMAT
                        the format of the image that comes back as prediction: indexedpng,bluechannel
  --labels LABEL [LABEL ...]
                        specifies the labels for each index
  -d REDIS_DB, --redis-db REDIS_DB
                        the database to use
  -h REDIS_HOST, --redis-host REDIS_HOST
                        the Redis server to connect to
  -p REDIS_PORT, --redis-port REDIS_PORT
                        the port the Redis server is running on
  -t TIMEOUT, --timeout TIMEOUT
                        the timeout in seconds to wait for a prediction to arrive
  -v, --verbose         whether to output debugging information.
```


### REDIS-PREDICT-OD
Makes object detection predictions via Redis backend, passing in an image and receiving OPEX predictions back:
https://github.com/WaikatoLink2020/objdet-predictions-exchange-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: redis-predict-od [--channel-in CHANNEL_IN] [--channel-out CHANNEL_OUT] [--key-label KEY_LABEL] [--key-score KEY_SCORE] [-d REDIS_DB] [-h REDIS_HOST] [-p REDIS_PORT] [-t TIMEOUT] [-v]

optional arguments:
  --channel-in CHANNEL_IN
                        the Redis channel on which to receive predictions.
  --channel-out CHANNEL_OUT
                        the Redis channel to send the images out
  --key-label KEY_LABEL
                        the meta-data key in the annotations to use for storing the label.
  --key-score KEY_SCORE
                        the meta-data key in the annotations to use for storing the prediction score.
  -d REDIS_DB, --redis-db REDIS_DB
                        the database to use
  -h REDIS_HOST, --redis-host REDIS_HOST
                        the Redis server to connect to
  -p REDIS_PORT, --redis-port REDIS_PORT
                        the port the Redis server is running on
  -t TIMEOUT, --timeout TIMEOUT
                        the timeout in seconds to wait for a prediction to arrive
  -v, --verbose         whether to output debugging information.
```
