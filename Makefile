PY=python3
PROTOC=python3 -m grpc_tools.protoc

torchmoji:
	@ $(PY) -c \
		'from torchmoji.dl_utils import execute_download; \
		execute_download("./src/algo/deepmoji/model/pytorch_model.bin")'

proto:
<<<<<<< HEAD
	rm -rf src/microv2/stubs
	mkdir src/microv2/stubs
	$(PROTOC) -I ./src/microv2 \
		--python_out=./src/microv2/stubs \
		--grpc_python_out=./src/microv2/stubs server.proto \
		--mypy_out=./src/microv2/stubs
	sed -i -e 's/server_pb2/microv2.stubs.server_pb2/g' ./src/microv2/stubs/server_pb2_grpc.py

grpc:
	@ $(PY) ./src/microv2/server.py
=======
	$(PROTOC) -I./src/microv2 --python_out=./src/microv2 --grpc_python_out=./src/microv2 server.proto 

rmpb2:
	rm -rf ./src/microv2/server_pb2*
>>>>>>> db68cdb87ca9b53b9071dbc82dd375f9d7bbcbb1
