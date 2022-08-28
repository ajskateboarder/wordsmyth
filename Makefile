scale:
	@ ./scripts/scale $(image)

killcons:
	@ ./scripts/killcons

dlmodel:
	@ python3 -c \
		'from torchmoji.dl_utils import execute_download; \
		execute_download("src/deepmoji/model/pytorch_model.bin")'