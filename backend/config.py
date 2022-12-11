"""App config"""

# MODEL = "rubert_tiny"
# MODEL = "sentence_transformer_multilingual"
MODEL = "sentence_transformer_multilingual_labse"
DEFAULT_TRESHOLD = 0.2
DEFAULT_BATCHSIZE = 200
DEFAULT_WINDOW = 50
TEST_RESTRICTION_MAX_BATCHES = 2000
PROCESSORS_COUNT = 1
EMBED_BATCH_SIZE = 5
NORMALIZE_EMBEDDINGS = True
VIS_REGRESSION = False
VIS_BATCH_INFO = True
API_PORT = 80