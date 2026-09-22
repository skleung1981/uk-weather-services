##### Default Python Build Process to support get the library from local nexus #####
##### Do not try to update if it is finalized.                                 #####
####################################################################################
FROM python:3.14-slim AS builder

WORKDIR /build
COPY requirements.txt .

# NEXUS_INDEX is passed at build time — see Jenkins stage below
# NEXUS_USER and NEXUS_PASS are using nexus read only account for PyPi only
ARG NEXUS_INDEX
ARG NEXUS_HOST
ARG NEXUS_USER
ARG NEXUS_PASS

RUN pip install --no-cache-dir --target=/deps \
        --extra-index-url "https://$NEXUS_USER:$NEXUS_PASS@$NEXUS_HOST/$NEXUS_INDEX/" \
        --trusted-host $NEXUS_HOST \
        -r requirements.txt

COPY . .

#####################################################################################
FROM python:3.14-slim
COPY --from=builder /deps /usr/local/lib/python3.14/site-packages
COPY --from=builder /build /app
WORKDIR /app
##### Application level, it is required to update
CMD ["python3", "--version"]