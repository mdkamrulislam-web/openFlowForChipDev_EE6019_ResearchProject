# Setting up the flow

The only things you install are a container engine, `make`, `python3` and `git`. Every EDA tool and PDK lives inside one pinned image (see [`env/tools.env`](../env/tools.env)), so everyone gets the same versions and the same results.

Budget about **20 GB of free disk**: the image is a 3.9 GB download and about 17 GB once unpacked.

## Linux (Ubuntu, Debian, Fedora)

1. Install Docker Engine: <https://docs.docker.com/engine/install/>
2. Let your user run Docker without `sudo`, then log out and back in:
   ```bash
   sudo usermod -aG docker "$USER"
   ```
3. Install the rest:
   ```bash
   sudo apt install make python3 git        # Fedora: sudo dnf install make python3 git
   ```

## macOS (Intel or Apple Silicon)

1. Install Docker Desktop: <https://docs.docker.com/desktop/setup/install/mac-install/>. The image has a native arm64 build, so Apple Silicon runs it without emulation.
2. In Docker Desktop → Settings → Resources, give it at least 8 GB of memory and 40 GB of disk.
3. `make`, `python3` and `git` come with the Xcode command-line tools: `xcode-select --install`.

## Windows

Use WSL2 rather than native Windows.

1. In PowerShell as administrator: `wsl --install -d Ubuntu`, then restart.
2. Install Docker Desktop and turn on *Use the WSL 2 based engine* and WSL integration for Ubuntu.
3. Open the Ubuntu terminal and follow the Linux steps from step 3. Clone the repository inside the WSL file system (for example `~/`), not under `/mnt/c/`, or the flow runs much more slowly.

## Podman instead of Docker

Set `CONTAINER_ENGINE=podman` in your shell. Everything else is the same.

## Check the installation

```bash
make shell                  # first run pulls the image; you get a shell in /work
librelane --version
exit
make sim                    # should print "PASS: counter_tb (8-bit), 0 errors"
```

## Viewing layouts

`make view` opens the final GDS in KLayout from inside the container, which needs X11 forwarding and is fiddly on macOS and Windows. The simpler route is to install [KLayout](https://www.klayout.de/build.html) on your own machine and open `designs/<design>/runs/<pdk>/final/gds/<design>.gds` directly. A PNG render is also written to `final/render/`.

The image can also serve a full desktop in the browser (VNC). See the [IIC-OSIC-TOOLS documentation](https://github.com/iic-jku/IIC-OSIC-TOOLS) if you want the graphical tools (Xschem, KLayout, Magic) without installing anything.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `permission denied ... docker.sock` | Your user is not in the `docker` group, or you have not logged out and in since adding it. |
| `toomanyrequests: ... pull rate limit` | Docker Hub limits anonymous pulls. Run `docker login` with a free Docker Hub account, or wait an hour. |
| `no space left on device` during the pull | Free disk space or give Docker Desktop a bigger disk. `docker system prune` removes old images. |
| Files in `build/` or `runs/` owned by root | You ran an old version of the wrapper as root. `sudo chown -R "$USER" .` fixes it; the current wrapper runs as your user. |
| `[INFO] Final PATH variable ...` lines at the start of every command | Printed by the image's login script. Harmless. |
