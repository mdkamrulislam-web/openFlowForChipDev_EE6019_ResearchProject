# Tiny Tapeout beginner guide

The main teaching resource is the editable [Word manual](tiny-tapeout-beginner-guide.docx), with a [PDF copy](tiny-tapeout-beginner-guide.pdf) for reading and printing. It explains the digital-design concepts, then walks through a browser-first SKY130 counter example: create a repository from the official template, add the example files, check the automated tests, inspect the generated layout and download the evidence. Local simulation is an optional route.

The reviewed Word/PDF manual contains **85 pages, approximately 23,000 words and 30 figure placements**, including real waveform captures. Some retained image assets are not used in the manual.

## Starter files

[counter-starter.zip](counter-starter.zip) contains exactly these seven files, with their repository paths preserved:

```text
info.yaml
src/counter.v
src/project.v
test/Makefile
test/tb.v
test/test.py
docs/info.md
```

Create the repository from the official Tiny Tapeout SKY template first. Extract the ZIP and upload `info.yaml` together with the `src`, `test` and `docs` folders at the repository root, preserving the folder structure. The ZIP supplies the example; the template supplies the workflows, development environment, test dependencies, licence and process configuration. It does not replace those template files. The manual also includes the full example code in its appendix.

[starter-checksums.json](starter-checksums.json) records the reference commit and SHA-256 hash of every starter file. The ZIP's exact seven-file set and all seven hashes have been checked against this manifest.

## Rebuild the Word manual

[guide.md](guide.md) is the text source. [build_guide.py](build_guide.py) reads that source and the figures in [img](img), then writes `tiny-tapeout-beginner-guide.docx` in this directory. It does not generate the PDF. [requirements.txt](requirements.txt) pins `python-docx==1.2.0` and `Pillow==12.3.0`; these are document-building dependencies, separate from the counter's simulator dependencies.

From the repository root, use Python 3 and an isolated environment. In PowerShell:

```powershell
python -m venv .venv-guide
.\.venv-guide\Scripts\python.exe -m pip install -r docs\beginner-guide\requirements.txt
.\.venv-guide\Scripts\python.exe docs\beginner-guide\build_guide.py
```

On Linux or macOS:

```sh
python3 -m venv .venv-guide
.venv-guide/bin/python -m pip install -r docs/beginner-guide/requirements.txt
.venv-guide/bin/python docs/beginner-guide/build_guide.py
```

Keep the virtual environment out of commits. After building:

1. Open the generated DOCX in Microsoft Word.
2. Refresh the table of contents: right-click it, choose **Update Field**, then **Update entire table**. Update document fields with **Ctrl+A**, **F9** as needed.
3. Review pagination, screenshots, tables, code blocks and page-number fields; save the DOCX.
4. Use **File → Export → Create PDF/XPS**, or Word's **Save As → PDF**, to replace `tiny-tapeout-beginner-guide.pdf`.
5. Check the exported PDF visually and update the page count above. Word performs the final layout, so rebuilding the DOCX alone does not refresh the checked PDF.

## Verified example and evidence

The worked example is the public [tt-sky130-counter repository](https://github.com/mdkamrulislam-web/tt-sky130-counter), at commit [`61ef06bed008e76000f9ae46d65182e476d15dd6`](https://github.com/mdkamrulislam-web/tt-sky130-counter/tree/61ef06bed008e76000f9ae46d65182e476d15dd6). Evidence belongs to that commit:

| Check | Successful run | Evidence |
| --- | --- | --- |
| RTL simulation | [37693100752](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100752) | One test, zero failures/errors; actual `test-results/tb.fst` waveform |
| Generated documentation | [37693100755](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100755) | Two-page generated datasheet |
| Layout and verification | [37693100748](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100748) | `gds`, `gl_test`, `precheck` and `viewer` jobs passed; gate-level test passed and all 15 prechecks passed |

The SKY130A layout occupies one tile. Its reported counts are **47 cells after synthesis**, **279 non-fill standard-cell instances including 225 tap cells**, and **4,600 instances including fillers**. These describe different build stages and cell categories; they are not interchangeable logic-gate counts. Reported core utilisation is approximately **4.96%**. The manual explains these distinctions and separates functional gate-level simulation from static timing analysis.

[example-evidence/rtl-results.xml](example-evidence/rtl-results.xml) and [example-evidence/metrics.csv](example-evidence/metrics.csv) retain the downloaded result data used in the guide. [screenshot-sources.json](screenshot-sources.json) records image sources, capture/retrieval dates, hashes and evidence classifications, including the waveform's run, artifact and commit.

## Screenshot provenance and attribution

The figures deliberately distinguish these sources:

- Actual browser captures of the public example's files, Actions runs and native layout viewer, plus dated Tiny Tapeout calculator captures.
- Native Surfer waveform-area captures of the actual RTL `tb.fst`, showing reset, count, hold and wrap. The traces were not redrawn.
- Local HTML views of the unchanged downloaded `results.xml` and `metrics.csv`. These present actual artifacts; they are not GitHub-generated results pages.
- A rendered page from the actual generated two-page datasheet PDF.
- Official GitHub Docs and Tiny Tapeout documentation screenshots for controls requiring an account, such as repository creation, editing, commits and Pages settings. Their captions identify them as documentation images, rather than actions performed in our account; some show older example repositories.

GitHub Docs publishes documentation content under [CC BY 4.0](https://github.com/github/docs/blob/main/LICENSE). Retain the GitHub Docs attribution, source links and licence reference when reusing those documentation assets, and identify any alterations. The manifest preserves the individual source URLs for GitHub, Tiny Tapeout and Surfer material; that provenance does not assign a uniform licence to all third-party images. Counter source carries Apache-2.0 notices: preserve those notices and the template's [Apache-2.0 licence](https://github.com/mdkamrulislam-web/tt-sky130-counter/blob/61ef06bed008e76000f9ae46d65182e476d15dd6/LICENSE) when reusing the starter files.

## Learning endpoint and review

The practical route uses free standard GitHub-hosted Actions compute for a public repository and ends with a **checked digital layout and its downloadable artifacts**. GitHub's artifact-storage allowances still apply. Creating a fabrication project, ordering and submitting a revision are explained as separate later steps. No payment, fabrication order or fabrication submission was performed for this guide; successful Actions runs do not manufacture a chip.

The guide has received technical checks against the source and successful counter runs. All pages were rendered in installed Microsoft Word and visually reviewed; corrected tables, screenshots, source listings and local setup were checked again. The final PDF has no blank pages or detected text outside page bounds. All seven starter files match the reviewed commit byte for byte. These checks are not a student usability trial; the instructions have not yet been evaluated through an observed beginner walkthrough.
