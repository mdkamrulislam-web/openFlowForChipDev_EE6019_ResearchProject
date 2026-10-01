#!/usr/bin/env bash
# Run a command inside the pinned tool container, with the repository
# mounted at /work. Used by the Makefile; can also be called directly:
#
#   scripts/run-in-container.sh verilator --version
#   scripts/run-in-container.sh            # interactive shell
#
# Set CONTAINER_ENGINE=podman to use Podman instead of Docker.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=../env/tools.env
source "${repo_root}/env/tools.env"
image="${IMAGE_NAME}:${IMAGE_TAG}@${IMAGE_DIGEST}"
engine="${CONTAINER_ENGINE:-docker}"

tty_flags=()
if [ -t 0 ] && [ -t 1 ]; then tty_flags=(-it); fi

# The image defaults to IHP SG13G2; pass the chosen PDK through so its
# environment variables (PDK, PDKPATH, STD_CELL_LIBRARY) match.
env_flags=(-e HOME=/tmp)
[ -n "${PDK:-}" ] && env_flags+=(-e "PDK=${PDK}")
[ -n "${SCL:-}" ] && env_flags+=(-e "STD_CELL_LIBRARY=${SCL}")

if [ $# -eq 0 ]; then set -- bash; fi

exec "${engine}" run --rm "${tty_flags[@]}" \
    --user "$(id -u):$(id -g)" \
    "${env_flags[@]}" \
    -v "${repo_root}:/work" -w /work \
    --entrypoint /bin/bash \
    "${image}" -lc 'exec "$@"' bash "$@"
