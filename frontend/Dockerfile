FROM node:25-alpine AS base

ENV TZ=Europe/Berlin

# stage 1 builder: rebuild the source code only when needed
FROM base AS builder

# check if needed
RUN apk add --no-cache git findutils

WORKDIR /app

# init shadcn
RUN yes | npx shadcn@latest init --preset b2BphlPSy --template next --name frontend
WORKDIR /app/frontend

# install shadcn components
COPY components.txt .
RUN cat components.txt | xargs npx shadcn@latest add --yes

# copy project files
COPY next.config.mjs .
COPY app/ app/

# build
RUN npm run build

# stage 2 runner: production image, copy all the files and run next
FROM base AS runner

WORKDIR /app

# don't run production as root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

# automatically leverage output traces to reduce image size
COPY --from=builder /app/frontend/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/frontend/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/frontend/.next/static ./.next/static

CMD ["node", "server.js"]
