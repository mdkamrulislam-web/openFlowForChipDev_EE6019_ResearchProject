"""Editable teaching diagrams; these are illustrations, never run evidence.

The course builder supplies its rectangle, text and connector helpers.  Every
diagram stays within the content region and leaves the title/check to it.
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN


INK = "142C3A"
TEAL = "087F83"
CORAL = "F06445"
WHITE = "FFFFFF"
MIST = "E3F0EE"
MUTED = "496471"
RULE = "C7D6D5"
PALE_CORAL = "FBE2D9"
BLUE = "326C9B"
PALE_BLUE = "E5EEF6"


def _prose(slide, text, first, second, third=None):
    """Two or three concise lines, above the actual diagram."""
    lines = [first, second] + ([third] if third else [])
    text(slide, .82, 2.12, 11.62, .93 if third else .73,
         "\n".join(lines), 22, INK)


def _caption(slide, text, value="Conceptual diagram — not measured geometry"):
    text(slide, .82, 6.00, 11.62, .19, value, 10, MUTED)


def _label(slide, text, x, y, w, h, value, size=22, fill=INK,
           bold=False, centre=False):
    h = max(h, size / 72 * 1.30 + .06)
    return text(slide, x, y, w, h, value, size, fill, bold,
                align=PP_ALIGN.CENTER if centre else PP_ALIGN.LEFT)


def _chip_grid(slide, box, x, y, step=.56, cell=.46):
    """A few example die sites inside an illustrative wafer disc."""
    for row in range(3):
        for col in range(3):
            box(slide, x + col * step, y + row * step, cell, cell,
                CORAL if (row, col) == (1, 1) else TEAL)


def _floorplan(slide, box, text, line):
    _prose(slide, text,
           "Floorplan = boundary + usable core + pins + power plan.",
           "Tiny Tapeout provides a fixed tile within a larger shared chip.")
    # Boundary and inset core deliberately have no dimensions or scale.
    box(slide, 1.08, 3.29, 6.65, 2.47, PALE_BLUE, BLUE)
    _label(slide, text, 1.27, 3.39, 3.30, .36, "Tile boundary", 22,
           BLUE, True)
    box(slide, 1.74, 3.89, 5.30, 1.42, WHITE, TEAL)
    _label(slide, text, 1.90, 3.98, 3.50, .33, "Usable core", 20,
           TEAL, True)
    # Rows contain only illustrative cells, without a reference cell count.
    for row in range(2):
        yy = 4.48 + row * .46
        line(slide, 1.97, yy + .27, 6.83, yy + .27, RULE, 1)
        for col in range(7):
            box(slide, 2.06 + col * .64, yy, .47, .24, MIST, TEAL)
    for i in range(4):
        yy = 4.02 + i * .40
        box(slide, .87, yy, .21, .10, TEAL)
        box(slide, 7.73, yy, .21, .10, TEAL)
    # The red rails are a conceptual power plan, not the actual reference PDN.
    line(slide, 1.30, 5.47, 7.49, 5.47, CORAL, 4)
    line(slide, 1.30, 5.63, 7.49, 5.63, CORAL, 4)
    legends = [
        ("Boundary", "Limits the tile", BLUE),
        ("Core / rows", "Legal cell positions", TEAL),
        ("Pins", "External connections", TEAL),
        ("Power rails", "Distribute supply", CORAL),
    ]
    for i, (name, detail, fill) in enumerate(legends):
        yy = 3.14 + i * .73
        box(slide, 8.34, yy + .08, .16, .16, fill)
        _label(slide, text, 8.67, yy, 3.74, .74,
               name + "\n" + detail, 20, INK, False)
    _caption(slide, text)


def _clock_tree(slide, box, text, line):
    _prose(slide, text,
           "One clock must reach many storage elements.",
           "Buffers distribute load; physical clock arrivals can differ.")
    # Connections precede the nodes so they end cleanly behind filled shapes.
    line(slide, 2.87, 4.26, 4.15, 4.26, TEAL, 3)
    line(slide, 5.55, 4.26, 6.42, 4.26, TEAL, 3)
    line(slide, 6.42, 3.68, 6.42, 4.91, TEAL, 3)
    line(slide, 6.42, 3.68, 7.02, 3.68, TEAL, 3)
    line(slide, 6.42, 4.91, 7.02, 4.91, TEAL, 3)
    leaves = [(3.32, 3.68), (3.98, 3.68),
              (4.63, 4.91), (5.29, 4.91)]
    for yy, branch in leaves:
        line(slide, 8.62, branch, 9.32, branch, TEAL, 3)
        line(slide, 9.32, branch, 9.32, yy + .20, TEAL, 3)
        line(slide, 9.32, yy + .20, 10.00, yy + .20, TEAL, 3)
    box(slide, .98, 3.90, 1.89, .72, INK)
    _label(slide, text, 1.10, 4.04, 1.65, .41, "Clock", 26,
           WHITE, True, True)
    for x, y, w in [(4.15, 3.95, 1.40),
                    (7.02, 3.38, 1.60), (7.02, 4.61, 1.60)]:
        box(slide, x, y, w, .60, TEAL)
        _label(slide, text, x + .08, y + .12, w - .16, .35,
               "Buffer", 22, WHITE, True, True)
    for i, (yy, _) in enumerate(leaves, 1):
        box(slide, 10.00, yy, 2.13, .43, MIST, TEAL)
        _label(slide, text, 10.12, yy + .03, 1.89, .34,
               "Flip-flop " + str(i), 20, INK, False, True)
    _label(slide, text, .98, 5.62, 8.82, .38,
           "Skew = difference between clock arrival times.", 20, TEAL, True)
    _caption(slide, text, "Conceptual branching tree — not the reference clock network")


def _routing(slide, box, text, line):
    _prose(slide, text,
           "Routing makes physical wire paths; vias change layers.",
           "Width, spacing and required connectivity must be checked.")
    # A layer view of a single net, not a reconstruction of routed geometry.
    for y, name in [(3.32, "Metal 3"), (4.27, "Metal 2"),
                    (5.22, "Metal 1")]:
        box(slide, 2.12, y, 6.73, .45, PALE_BLUE)
        _label(slide, text, .88, y + .03, 1.21, .37, name, 20,
               BLUE, True)
    # M1 -> via -> M2 -> via -> M3, with the two endpoints labelled A/B.
    line(slide, 2.93, 5.44, 4.43, 5.44, CORAL, 5)
    line(slide, 4.43, 4.49, 4.43, 5.44, TEAL, 5)
    line(slide, 4.43, 4.49, 6.59, 4.49, BLUE, 5)
    line(slide, 6.59, 3.54, 6.59, 4.49, TEAL, 5)
    line(slide, 6.59, 3.54, 8.05, 3.54, CORAL, 5)
    for x, y in [(4.43, 5.44), (4.43, 4.49),
                 (6.59, 4.49), (6.59, 3.54)]:
        box(slide, x - .09, y - .09, .18, .18, TEAL,
            kind=MSO_SHAPE.OVAL)
    for x, y, name in [(2.20, 5.14, "A"), (8.05, 3.24, "B")]:
        box(slide, x, y, .72, .60, INK)
        _label(slide, text, x + .08, y + .11, .56, .37,
               name, 24, WHITE, True, True)
    _label(slide, text, 9.24, 3.35, 3.12, .85,
           "Metal wires\nrun on a layer.", 22, CORAL, True)
    _label(slide, text, 9.24, 4.28, 3.12, .84,
           "Vias connect\ndifferent layers.", 22, TEAL, True)
    _label(slide, text, 9.24, 5.28, 3.12, .46,
           "One required net", 20, INK)
    _caption(slide, text, "Conceptual layer view — spacing and wire lengths are not measured")


def _setup_hold(slide, box, text, line):
    _prose(slide, text,
           "Data must be stable around the receiving clock edge.",
           "Setup is before; hold is after. STA checks both.")
    # Deliberately unscaled stable-time windows on opposite sides of one edge.
    box(slide, 4.10, 3.15, 2.27, 2.08, MIST)
    box(slide, 6.37, 3.15, 2.27, 2.08, PALE_CORAL)
    _label(slide, text, 4.27, 3.35, 1.91, .40,
           "SETUP", 24, TEAL, True, True)
    _label(slide, text, 6.54, 3.35, 1.91, .40,
           "HOLD", 24, CORAL, True, True)
    _label(slide, text, .92, 4.17, 1.48, .48, "Clock", 22,
           INK, True)
    line(slide, 2.52, 4.81, 6.37, 4.81, INK, 4)
    line(slide, 6.37, 4.81, 6.37, 4.05, CORAL, 5)
    line(slide, 6.37, 4.05, 12.14, 4.05, INK, 4)
    _label(slide, text, 2.16, 5.45, 3.62, .44,
           "Stable before", 24, TEAL, True, True)
    _label(slide, text, 7.01, 5.45, 3.62, .44,
           "Stable after", 24, CORAL, True, True)
    _label(slide, text, 9.03, 4.73, 3.10, .50,
           "↑ Sampling edge", 22, INK)
    line(slide, 8.91, 4.99, 6.47, 4.43, MUTED, 1.5)
    _caption(slide, text, "Conceptual timing windows — widths do not represent cell requirements")


def _wafer_layers(slide, box, text, line):
    _prose(slide, text,
           "A wafer contains repeated chip sites.",
           "Patterns and repeated process steps form devices and interconnect.")
    box(slide, 1.05, 3.40, 2.55, 2.55, PALE_BLUE, BLUE,
        kind=MSO_SHAPE.OVAL)
    _chip_grid(slide, box, 1.54, 3.87, .55, .44)
    _label(slide, text, 1.10, 3.03, 2.46, .39,
           "Wafer", 24, BLUE, True, True)
    box(slide, 4.12, 4.26, .62, .49, TEAL,
        kind=MSO_SHAPE.CHEVRON)
    _label(slide, text, 5.05, 3.10, 6.81, .38,
           "Layers in one illustrative chip site", 22, INK, True)
    layers = [
        (3.72, MIST, "Insulation", INK),
        (4.13, CORAL, "Conductive layer", INK),
        (4.54, MIST, "Insulation", INK),
        (4.95, INK, "Silicon / device region", WHITE),
    ]
    for y, fill, name, ink in layers:
        box(slide, 5.05, y, 6.81, .40, fill)
        _label(slide, text, 5.26, y + .03, 6.40, .35,
               name, 20, ink)
    _label(slide, text, 4.99, 5.62, 7.14, .38,
           "Form → pattern → modify → repeat", 22, TEAL, True)
    _caption(slide, text, "Conceptual wafer and layers — not a SKY130 cross-section or mask count")


def _dicing(slide, box, text, line):
    _prose(slide, text,
           "Test devices; dice the wafer into dies; package for protection and connections.",
           "Board assembly and testing prepare usable hardware.")
    box(slide, 1.05, 3.45, 2.54, 2.54, PALE_BLUE, BLUE,
        kind=MSO_SHAPE.OVAL)
    _chip_grid(slide, box, 1.53, 3.92, .55, .44)
    # Gaps between example sites convey the separation step without a photograph.
    box(slide, 4.05, 4.33, .57, .55, TEAL,
        kind=MSO_SHAPE.CHEVRON)
    box(slide, 5.15, 3.84, 1.66, 1.66, INK)
    box(slide, 5.42, 4.11, 1.12, 1.12, CORAL)
    box(slide, 7.23, 4.33, .57, .55, TEAL,
        kind=MSO_SHAPE.CHEVRON)
    box(slide, 8.44, 3.91, 2.74, 1.52, INK)
    box(slide, 9.15, 4.22, 1.32, .89, CORAL)
    for i in range(4):
        yy = 4.05 + i * .33
        box(slide, 8.15, yy, .29, .09, TEAL)
        box(slide, 11.18, yy, .29, .09, TEAL)
    _label(slide, text, 1.12, 3.07, 2.40, .38,
           "Wafer sites", 20, BLUE, True, True)
    _label(slide, text, 5.17, 5.64, 1.62, .35,
           "Die", 22, INK, True, True)
    _label(slide, text, 8.35, 5.64, 2.92, .35,
           "Package", 22, INK, True, True)
    _caption(slide, text, "Conceptual separation and packaging — actual delivery depends on the service")


def _clock_edge(slide, box, text, line):
    _prose(slide, text,
           "A rising edge is 0 → 1; a held-high clock adds no edges.",
           "20 ns per cycle = 50 MHz in this test.")
    # The interval between the two illustrated rising edges is one full cycle.
    line(slide, 3.60, 3.34, 8.00, 3.34, MUTED, 1.5)
    line(slide, 3.60, 3.23, 3.60, 3.45, MUTED, 1.5)
    line(slide, 8.00, 3.23, 8.00, 3.45, MUTED, 1.5)
    _label(slide, text, 5.01, 2.90, 1.62, .38,
           "20 ns", 20, TEAL, True, True)
    points = [(1.90, 4.13), (3.60, 4.13), (3.60, 3.56),
              (5.80, 3.56), (5.80, 4.13), (8.00, 4.13),
              (8.00, 3.56), (10.20, 3.56), (10.20, 4.13),
              (12.30, 4.13)]
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        rising = y2 < y1
        line(slide, x1, y1, x2, y2, CORAL if rising else INK,
             5 if rising else 3)
    _label(slide, text, .85, 3.62, 1.02, .45,
           "Clock", 22, INK, True)
    _label(slide, text, .85, 4.72, 1.02, .43,
           "Count", 22, INK, True)
    for x, w, value in [(1.90, 1.70, "0"),
                         (3.60, 4.40, "1"), (8.00, 4.30, "2")]:
        box(slide, x, 4.65, w, .65, MIST, TEAL)
        _label(slide, text, x + .10, 4.78, w - .20, .42,
               value, 26, TEAL, True, True)
    for xx in (3.60, 8.00):
        line(slide, xx, 4.18, xx, 4.58, CORAL, 1.5)
    _label(slide, text, .90, 5.60, 11.36, .38,
           "Enable = 1; reset released. Count changes only at ↑clk.",
           22, INK)
    _caption(slide, text, "Predicted RTL trace — not a recorded FST screenshot")


def draw_visual(slide, data, box, text, line) -> bool:
    """Draw only explicitly selected conceptual lessons; leave others alone."""
    slide_id = data.get("id")
    title = data.get("title", "").lower()
    diagrams = {
        "P05": _floorplan,
        "P08": _clock_tree,
        "P09": _routing,
        "P30": _wafer_layers,
        "P32": _dicing,
        "C16": _clock_edge,
    }
    if slide_id == "P12" and "setup" in title and "hold" in title:
        _setup_hold(slide, box, text, line)
        return True
    # P13 remains the actual-metrics slide, rather than an illustrative override.
    draw = diagrams.get(slide_id)
    if draw is None:
        return False
    draw(slide, box, text, line)
    return True
