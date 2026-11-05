# Tiny Tapeout RISC-V survey scripts

These scripts produce [docs/research/data/tt-riscv-metrics.csv](../../docs/research/data/tt-riscv-metrics.csv), used by [the characterisation](../../docs/research/tt-riscv-characterisation.md). They need Python 3.9+ and a logged-in `gh` CLI. They read GitHub only; nothing is written to GitHub.

1. Make an empty working folder. Copy the four scripts into it.
2. Download every shuttle index into it:
   ```sh
   for f in $(gh api repos/TinyTapeout/tinytapeout-index/contents/index --jq '.[].name' | grep -v '^index.json$'); do
     gh api "repos/TinyTapeout/tinytapeout-index/contents/index/$f" -H "Accept: application/vnd.github.raw" > "$f"
   done
   ```
3. `python fetch.py`: finds RISC-V projects in the index files and downloads each project's `info.yaml` and `stats/` from its shuttle repository. Output: `riscv_raw.json`.
4. `python fetch2.py`: adds each project's flow configuration (clock period) from its own repository at the taped-out commit, and its datasheet `docs/info.md`.
5. `python parse.py`: extracts cell count, gate equivalents, flip-flops, die area, utilisation, power and setup slack, and estimates Fmax. Output: `riscv_rows.json`.
6. `python export.py riscv_rows.json tt-riscv-metrics.csv`: writes the CSV.

Last run: 5 November 2026, index up to TTSKY26c. On Windows, write or edit these scripts with an editor, not a Git Bash heredoc: heredocs drop the backslashes in the regular expressions.
