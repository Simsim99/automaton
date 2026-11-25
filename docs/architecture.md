- **Bottom `<missing>` layers** — Debian bookworm-slim + Python 3.13.18, built by the official maintainers, inherited by digest, read-only, shared on disk with every image built on this base.
- **`RUN ...savedAptMark...` — 36.9 MB** — downloads, GPG-verifies and installs CPython into `/usr/local`. The fattest layer in the image: it is Python itself.
- **`RUN ...idle3...` — 36 B** — the maintainers' housekeeping, deleting unneeded symlinks. (Yes, a layer can be smaller than this sentence.)
- **`COPY /opt/venv /opt/venv` — 17.2 MB** — the smuggled artifact: Flask + gunicorn + their dependency tree, and nothing else. The only thing that crossed from the builder world.
- **`ENV PATH=/opt/venv/bin:...` — 0 B** — makes the venv's binaries the default Python from now on.
- **`RUN useradd -r -u 1000 notes` — 4.3 kB** — writes `/etc/passwd` + `/etc/shadow`. An identity weighs four kilobytes.
- **`WORKDIR /app/src` — 0 B / `COPY src/ .` — 8.27 kB** — your entire application. Lighter than a screenshot. Defense line to memorize: “My app's contribution to this image is about 12 kilobytes; everything else is borrowed, verified foundation.”
- **`USER notes` — 0 B** — the crown-drop; from here, unprivileged.
- **`EXPOSE 8000`, `CMD gunicorn` — 0 B** — documentation, then the boot command that ends the story.

The builder? Not overwritten, not hidden — never a member. Final image = final stage's chain + the one copied layer. (Its cache survives for rebuild speed — that's the `CACHED` you keep enjoying.)