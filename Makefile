.PHONY: docker
docker:
	docker build -t icn.ocir.io/axqafkgb0llg/imaginer-story:latest . --platform=linux/amd64
	docker push icn.ocir.io/axqafkgb0llg/imaginer-story:latest

.PHONY: proto
proto:
	cd storyai/proto &&\
	python3 -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. ./imaginer.proto &&\
	sed 's/^import imaginer_pb2/from \. import imaginer_pb2/' ./imaginer_pb2_grpc.py > ./imaginer_pb2_grpc.py.1 &&\
	mv ./imaginer_pb2_grpc.py.1 ./imaginer_pb2_grpc.py