FROM golang:1.11 as runtime-builder	FROM golang:1.17 as runtime-builder
ARG KATA_VERSION	ARG KATA_VERSION
RUN git clone -b ${KATA_VERSION} https://github.com/kata-containers/runtime /go/src/github.com/kata-containers/runtime	RUN git clone -b ${KATA_VERSION} https://github.com/kata-containers/runtime /go/src/github.com/kata-containers/runtime
WORKDIR /go/src/github.com/kata-containers/runtime
