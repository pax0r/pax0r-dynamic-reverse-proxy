# Pax0r DynamicDNS

Simple application to setup DDNS service on your host in internet. 
Designed for personal use so right now it does not support multiple users. 
My main reason was to create a DynamicDNS service for my local Home Assistant instalation, as a replacement for DuckDNS.
DNS server uses `dnslib` and HTTP server runs on `sanic`.

## Deploying

### From bare source
1. Create `config.yaml` file using `config.example.yaml` as reference
2. Simply run `python -m pax0r_ddns_server`

### Docker
1. Create `config.yaml` file using `config.example.yaml` as reference
2. Build image : `docker build -t pax0r .`
3. Run from image : `docker run --publish 8000:8000 --publish 53:53 pax0r `

## Usage

1. Set DNS NS record for domain you want to control to the the server where you are running DDNS service
2. Post with empty body to `http://<your-server>/<domain>`. IP of the posting client will be used as dynamic IP for given domain
3. DNS server run by this script should answer with your dynamic IP

# TODO:

- Persistent backends
- Separate daemon for http and dns (right now it's single process with two threads)
- Client applications
- Rewrite DNSServer to work on asyncio
