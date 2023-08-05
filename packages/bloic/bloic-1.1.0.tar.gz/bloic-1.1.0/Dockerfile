# Build stage
FROM python:3.11-alpine AS build

# Install tools for build stage
# hadolint ignore=DL3013,DL3018
RUN apk add --no-cache git && pip install --no-cache-dir --upgrade build 

WORKDIR /build
COPY . .
RUN pip install --no-cache-dir .

# Runtime stage
FROM python:3.11-alpine

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin/bloic /usr/local/bin/bloic

ENTRYPOINT ["bloic"]
