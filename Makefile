.PHONY: docker
docker:
	docker build -t icn.ocir.io/axqafkgb0llg/imaginer-story:latest . --platform=linux/amd64
	docker push icn.ocir.io/axqafkgb0llg/imaginer-story:latest