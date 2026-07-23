FROM postgres:15

HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD pg_isready -U postgres || exit 1