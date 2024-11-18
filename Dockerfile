# syntax=docker/dockerfile:1
FROM ghcr.io/graalvm/native-image-community:17 as build
COPY ./moss /home/moss/moss

WORKDIR /home/moss

RUN echo "Main-Class: moss.Miner" > manifest
run javac -Xlint moss/*.java
run jar cfm miner.jar manifest moss/*.class


run native-image -jar miner.jar miner_1

from scratch
copy --from=build /home/moss/miner_1 /
entrypoint ["/miner_1"]
