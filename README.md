- [Full Stack With FastAPI \& Next.js](#full-stack-with-fastapi--nextjs)
- [Dependencies](#dependencies)
- [Services ops](#services-ops)
- [Deploy](#deploy)
- [Support](#support)

## Full Stack With FastAPI & Next.js

This is a full stack template using FastAPI and Next.js.

- deploy api with [fly.io][1]
  - app config with consul (via fly.io)
- deploy frontend with [cloudflare pages][2]


## Dependencies

Command line tools:
- [flyctl](https://fly.io/docs/flyctl/install/)
- [pnpm](https://pnpm.io/installation)
- [wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update/)

## Services ops

**api**

create your app with fly.io

```shell
fly apps create --name <your app name> -o <org name>
```

attach consul to api

```shell
fly consul attach -a <your app name>
```

set config with consul

1. get consul url, `fly ssh console -a <your app name>`
2. show consul url, `echo $FLY_CONSUL_URL`

example:

`https://:<token>@consul-syd-5.fly-shared.net/<app name>-xxxxxxxxxx/`

- `consul-syd-5.fly-shared.net` is consul server, open in browser
- click `Login` and input consul `<token>`
- click `Key/Value` and input `<app name>-xxxxxxxxxx/<app-name>` in `Key or folder` input; example: `appname-xxxxxxxxx/appname`
- copy `config.yml` content to `Value` input, click `Save`
- `main.py` will read consul config; see [config.py][4]


**ui**

create project with cloudflare pages

```shell
cd ui && pnpm wrangler pages project create <app name> --production-branch master
```

deploy project with cloudflare pages , See this file [Makefile][3]

```shell
make ui # deploy ui
```

## Deploy

deploy api
```
make api
```

deploy frontend
```
make ui
```

## Support

If you like this project, please consider supporting me for coffee ☕️

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20-coffee-%2322BC18.svg)](https://www.buymeacoffee.com/chasengao) [![get youtself link](https://img.shields.io/badge/get%20youtself%20link-buymeacoffee-orange.svg)](https://www.buymeacoffee.com/invite/chasengao)


[1]: https://fly.io
[2]: https://pages.cloudflare.com
[3]: Makefile
[4]: src/config.py
