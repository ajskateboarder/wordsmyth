PY=python3
PROTOC=python3 -m grpc_tools.protoc

scale:
	@ ./scripts/scale $(image)

killcons:
	@ ./scripts/killcons

dlmodel:
	@ $(PY) -c \
		'from torchmoji.dl_utils import execute_download; \
		execute_download("./src/algo/deepmoji/model/pytorch_model.bin")'

proto:
	$(PROTOC) -I./src/microv2 --python_out=./src/microv2 --grpc_python_out=./src/microv2 server.proto 

rmpb2:
	rm -rf ./src/microv2/server_pb2*
