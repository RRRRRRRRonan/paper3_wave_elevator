"""LaTeX (as written in the week-3 md drafts) -> OMML, via latex2mathml and Office's MML2OMML.XSL.

MML2OMML drops MathML spacing elements, so LaTeX spacing commands are replaced by Unicode spaces
inside \\text{}; operator names (max, min, arg min, Reg, Pr) are set upright; in displays, max, min
and arg min take their limits below.
"""
import re
from latex2mathml.converter import convert
from lxml import etree

XSL = etree.XSLT(etree.parse(r"C:/Program Files/Microsoft Office/root/Office16/MML2OMML.XSL"))
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
EM, FOUR, THIN = "\u2003", "\u2005", "\u2009"
GROUP = r"\{([^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*)\}"      # balanced braces, depth 3


def normalize(tex: str, display: bool) -> str:
    t = tex.strip()
    t = re.sub(r"\\tag\{[^}]*\}", "", t).strip()
    t = re.sub(r"\\[Bb]igg?[lr]?(?=[\\(\[|./)\]])", "", t)             # \bigl\{ -> \{ (sizing dropped)
    t = re.sub(r"\\mathcal\s+([A-Za-z])", r"\\mathcal{\1}", t)          # \mathcal K -> \mathcal{K}
    t = re.sub(r"\\mathrm\s+([A-Za-z])", r"\\mathrm{\1}", t)            # \mathrm V -> \mathrm{V}
    t = t.replace(r"\operatorname{Reg}", r"\mathrm{Reg}").replace(r"\Pr", r"\mathrm{Pr}")
    t = t.replace(r"\mid", r"\text{" + FOUR + "|" + FOUR + "}")
    # operators: limits below in displays, upright names everywhere, a space after a limit operator
    ARGMIN = r"{\mathrm{arg}\text{" + FOUR + r"}\mathrm{min}}"
    if display:
        t = re.sub(r"\\arg\\min_" + GROUP, lambda m: r"\underset{" + m.group(1) + "}" + ARGMIN + r"\;", t)
        t = re.sub(r"\\underset" + GROUP + r"\{\\mathrm\{arg\\,min\}\}",
                   lambda m: r"\underset{" + m.group(1) + "}" + ARGMIN + r"\;", t)
        t = re.sub(r"\\(max|min)_" + GROUP, lambda m: r"\underset{" + m.group(2) + r"}{\mathrm{" + m.group(1) + r"}}\;", t)
    t = re.sub(r"\\underset" + GROUP + r"\{\\(max|min)\}", lambda m: r"\underset{" + m.group(1) + r"}{\mathrm{" + m.group(2) + r"}}\;", t)
    t = re.sub(r"\\(max|min)(?![a-zA-Z])", r"\\mathrm{\1}", t)
    t = re.sub(r"(\\;)(\s*\\[;,])+", r"\1", t)                        # no double spaces
    t = re.sub(r"\\;\s*(?=[.,)}=]|\\Bigr|\\Big/|$)", "", t)          # no space before punctuation
    # single upright letters (\mathrm{V}) are set as normal text, which Word keeps upright
    t = re.sub(r"\\mathrm\{([A-Za-z])\}", r"\\text{\1}", t)
    # spacing
    for cmd, sp in ((r"\qquad", EM + EM), (r"\quad", EM), (r"\;", FOUR), (r"\,", THIN), (r"\ ", FOUR)):
        t = t.replace(cmd, r"\text{" + sp + "}")
    return t


def omml(tex: str, display: bool = False) -> etree._Element:
    mml = convert(normalize(tex, display))
    out = XSL(etree.fromstring(mml)).getroot()
    bad = [x for x in out.iter(f"{{{M_NS}}}t") if x.text and "\\" in x.text]
    if bad:
        raise ValueError(f"unconverted LaTeX in {tex!r}: {[b.text for b in bad]}")
    return out
