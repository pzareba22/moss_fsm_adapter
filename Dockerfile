# syntax=docker/dockerfile:1
FROM ghcr.io/graalvm/native-image:ol8-java17-22.3.3 AS build

COPY ./moss /home/moss
WORKDIR /home/moss

RUN echo "Main-Class: moss.Miner" > manifest
RUN jar cfm miner.jar manifest moss/*.class
RUN rm -f manifest

RUN native-image -jar miner.jar miner_1


FROM scratch
COPY --from=build /home/moss/miner_1 /
ENTRYPOINT ["/miner_1"]
