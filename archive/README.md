# Earlier project work

`legacy-flow/` preserves the earlier standalone LibreLane counter flow: Makefile,
designs, scripts, pinned environment, original README, setup/flow notes, layout
images and old CI definition. Files were moved together; their original bytes
were checked after the move.

The current Tiny Tapeout example is at the repository root. For the old flow,
read `legacy-flow/README.md`. Before running its historical commands, enter its
own working directory:

```text
cd archive/legacy-flow
make sim
```

The archived `.github/workflows/flow.yml` is historical source. GitHub runs the
four Tiny Tapeout workflows in the repository root's `.github/workflows`.
The archive's old plan and reported results are retained as historical records.
