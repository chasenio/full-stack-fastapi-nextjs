
.PHONY: Deploy api
api:
	$Q flyctl deploy -c ci/fly.toml

.PHONY: Deploy ui
ui:
	$Q cd ui && pnpm dlx @cloudflare/next-on-pages
	$Q cd ui && pnpm wrangler pages deploy .vercel/output/static --branch master --commit-dirty=true
