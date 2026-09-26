# Section 4 figure generation prompts

Mode: built-in image-generation tool. These are raster PNG assets. Each initial image is a new drawing with the shared Fig. 1 palette specified in text.

## Figure 2

```text
Use case: scientific-educational. Create a clean publication figure for an operations-research journal, in the same unified visual family as a flat engineering warehouse schematic. White background, dark charcoal #24343F text and thin outlines, muted slate blue #52758D with pale blue #E7EEF3, teal #467F7D with pale teal #E3EFEC, muted amber #AF7C42 with pale amber #F5EAD8, neutral grey #EEF1F3. Flat 2D geometric drawing, no gradients, no shadow, no glossy effects, no decorative icons, no photos. Consistent Arial/Helvetica-like sans-serif text, math in clean italic serif with real subscripts and superscripts. Bold lowercase panel labels (a), (b), (c) where specified. All text readable at a full text-width print placement. No figure number or external caption inside image. Render at 3200 by 1800 pixels or higher comparable resolution. Keep labels short, ample white space, balanced alignment. All content is prescribed manuscript theory, not empirical data. Preserve exact symbols and arrow directions. No Chinese text.
FIGURE CONTENT: a methodology map with a primary pipeline across the upper 60% and three supporting-analysis boxes below. Five aligned primary columns with clear solid arrows left to right.
Column 1, neutral box: heading "Inputs · Section 3". Three short lines: "Candidate pool (Wᵏ, πᵏ)", "Classes Q and release laws νq", "Resources and common initial state".
Column 2, a single box heading "Paired evaluation · 4.1.1", containing two stacked subboxes labeled "M₁ · independent slots" in blue and "M₂ · shared trips" in teal. Footer "Same candidates and sequences".
Column 3 heading "Class medians", two rows "μ⁰·⁵qM₁" and "μ⁰·⁵qM₂" in conventional mathematical notation (0.5 superscript; qM1/qM2 subscripts), and short footer "One score per class and model". Two incoming lines from respective evaluator subboxes.
Column 4 amber box heading "Robust class choice · 4.1.2" with precise formula "Vq = max{μ⁰·⁵qM₁, μ⁰·⁵qM₂}" and "q* ∈ arg minq Vq". The two medians must be combined only here, AFTER medians have been computed. Conventional mathematical subscript q.
Column 5 teal-outline box heading "Within-class release" with "κ ∼ νq*" and "Wave Wκ"; render κ as the superscript on W. Footer "Fixed release distribution". This is random within-class draw, NOT candidate minimization.
A small neutral separate box below column 5: "M₃ · phase-time assessment", connected downward by one dashed arrow from release.
Below columns 1–4, three equal pale boxes:
"4.2 Performance diagnosis" / "Class spread and selection loss".
"4.3 Evaluator ordering" / "Sufficient conditions and reversals".
"4.4 Decision properties" / "Reduction and stability".
Dashed data-use connectors: from class medians to 4.2, paired evaluation to 4.3, robust score to 4.4; a short dashed arrow from 4.3 to 4.4 may indicate theoretical support. Route connectors cleanly outside labels. These support boxes must NOT form a sequential operational chain and no arrow feeds a support conclusion back as a mandatory selection step.
Small legible key at lower left: "Solid: decision flow    Dashed: supporting analysis or assessment".
Do not include additional text, invented plots, numeric examples, or M3 in the main minimax. The main visual should immediately answer how the method selects a class and releases a wave.
```

### Targeted correction

```text
Edit only the supplied methodology map. Preserve all geometry, colors, fonts, upper-row formulas, M3 placement and upper-row arrows. The bottom two support headings are connected to the wrong sources. In the bottom LEFT box under Paired evaluation, replace heading with '4.3 Evaluator ordering' and description with 'Sufficient conditions and reversals'. In the bottom MIDDLE box under Class medians, replace heading with '4.2 Performance diagnosis' and description with 'Class spread and selection loss'. Retain each vertical dashed connector exactly, so Paired evaluation leads to4.3 and Class medians leads to4.2. REMOVE the short horizontal dashed connector between bottom middle box and bottom right4.4 box entirely; it would otherwise imply incorrect support. Leave bottom-right 4.4 unchanged. This is a targeted text/connector correction only, no new text or layout changes. Preserve the exact mathematical formulas and symbols. Increase output pixel resolution if available without changing aspect ratio.
```

## Figure 3

```text
Use case: scientific-educational. Create a clean publication figure for an operations-research journal, in the same unified visual family as a flat engineering warehouse schematic. White background, dark charcoal #24343F text and thin outlines, muted slate blue #52758D with pale blue #E7EEF3, teal #467F7D with pale teal #E3EFEC, muted amber #AF7C42 with pale amber #F5EAD8, neutral grey #EEF1F3. Flat 2D geometric drawing, no gradients, no shadow, no glossy effects, no decorative icons, no photos. Consistent Arial/Helvetica-like sans-serif text, math in clean italic serif with real subscripts and superscripts. Bold lowercase panel labels (a), (b), (c) where specified. All text readable at a full text-width print placement. No figure number or external caption inside image. Render at 3200 by 1800 pixels or higher comparable resolution. Keep labels short, ample white space, balanced alignment. All content is prescribed manuscript theory, not empirical data. Preserve exact symbols and arrow directions. No Chinese text.
FIGURE CONTENT: three horizontally arranged panels, panels (a) and (b) slightly wider than (c). Mathematical comparison diagram, NOT a plot of experimental data.
(a) heading "Class-relative comparisons · 4.2.1". A neutral rounded rectangle at upper left "Pool reference" with symbol b₀. Separate outlined group "Selectable corner classes Q" containing three labeled symbolic markers in ascending order on a horizontal line: b₋ "Best", bqΦ "Selected", b₊ "Worst" (qΦ subscript on b). The b₀ box is OFF this class line; do NOT position it between best and worst. Under the group, formula cards with large readable equations: "UB = (b₊ − b₋)/b₀", "LB = (b₀ − bqΦ)/b₀". Below these, "GAP = UB − LB". Use a bracket spanning best to worst marked "Class spread", and a shorter bracket best to selected marked "Selection miss". A small note below: "The pool median may lie outside the class range."
(b) heading "Diagnostic decomposition · 4.2.1–4.2.2". A prominent formula across top "GAP = Hup + MΦ" with up subscript, Φ subscript. Beneath, two clean cards side by side. Neutral-blue card "Upper-tail headroom" with "Hup = (b₊ − b₀)/b₀" and "Signed reference comparison". Amber card "Class-selection miss" with "MΦ = (bqΦ − b₋)/b₀" and "Nonnegative decision loss". Branching lines connect the two terms in the top formula to their cards. A lower box "LSPO = b₀ MΦ", conventional SPO subscript, connected ONLY from the selection-miss card. Bottom note "UB ≥ 0; 0 ≤ MΦ ≤ UB" and second line "Hup, LB and GAP can be negative." Do NOT depict GAP as universally positive bars.
(c) heading "Partition resolution · 4.2.3". Two equal rectangles as candidate-pool diagrams, left coarse partition P with two equal vertical cells, right nested partition P′ with exactly those same outer boundaries and vertical split retained, plus a horizontal split inside each parent, giving four cells. Arrow from coarse to fine labeled "Nested refinement". Labels "Coarse P" and "Fine P′". Use pale blue and teal cell fill tints with visible charcoal boundaries. Under the grids, three short lines: "Disjoint, covering cells", "Same pool distribution", "Positive cell weights". Under those, a box with "Minimum median does not increase", "Maximum median does not decrease", "Class spread UB does not decrease". Bottom note "P is distinct from corner family Q." The nested-partition result is NOT drawn as an automatic property of the noncovering corner classes.
No invented numeric values; no CDF, no decorative scatterplot. Keep formulas large enough to read and every term exact.
```

### Targeted correction

```text
Edit only panel(c) of this scientific diagram. Preserve panels(a),(b) completely, all equations, colors, exact dimensions, and all other labels. In coarse partition P replace cell labels C1 and C2 with P1 and P2. In fine partition P′ replace top-left C1 with P11, bottom-left C3 with P12, top-right C2 with P21, bottom-right C4 with P22; use proper subscripts on P. This makes parent-child labels explicit and does not reuse descriptor C. Replace middle line 'Same pool distribution' with 'Same pool distribution and evaluator' (can wrap onto two lines). All four fine cells stay nested within unchanged coarse boundaries. Do not add formulas or values. Keep the restrained palette and scientific typography. Increase output pixel resolution if available without changing aspect ratio.
```

## Figure 4

```text
Use case: scientific-educational. Create a clean publication figure for an operations-research journal, in the same unified visual family as a flat engineering warehouse schematic. White background, dark charcoal #24343F text and thin outlines, muted slate blue #52758D with pale blue #E7EEF3, teal #467F7D with pale teal #E3EFEC, muted amber #AF7C42 with pale amber #F5EAD8, neutral grey #EEF1F3. Flat 2D geometric drawing, no gradients, no shadow, no glossy effects, no decorative icons, no photos. Consistent Arial/Helvetica-like sans-serif text, math in clean italic serif with real subscripts and superscripts. Bold lowercase panel labels (a), (b), (c) where specified. All text readable at a full text-width print placement. No figure number or external caption inside image. Render at 3200 by 1800 pixels or higher comparable resolution. Keep labels short, ample white space, balanced alignment. All content is prescribed manuscript theory, not empirical data. Preserve exact symbols and arrow directions. No Chinese text.
FIGURE CONTENT: three panels. Landscape but generous height, top (a) spans full width; lower (b) and (c) are equal panels. One-way logical implication above, two exact counterexample timelines below.
(a) heading "Conditional evaluator ordering · 4.3.1". Left box has "Common initial state" as heading and FOUR conditions underneath, each one short line: "(a) Same recorded sequence πᵏ", "(b) Same AMR assignments", "(c) No shared-trip overtaking", "(d) No M₁ repositioning disadvantage". ONE right-pointing implication arrow to a center box: "Request ordering: D₁(ϱ) ≤ D₂(ϱ)" and "Wave ordering: YkM₁ ≤ YkM₂" with subscripts. Then one right arrow labeled "For every candidate in class q" to a box "Class medians: μ⁰·⁵qM₁ ≤ μ⁰·⁵qM₂". All inequalities use ≤. Small note below this upper row: "The conditions are sufficient; their failure does not imply reversal."
(b) heading "Shared-trip reversal · 4.3.2". Small subtitle "Two orders 1 → 3; ready offsets 0 and 2". Three horizontal timeline rows on one exact common scale from 5 to 30 seconds. Row labels "M₁ slot 1", "M₁ slot 2", "M₂ shared car". Row 1 blue trip bar from t=5 to 19, then pale grey drop-off from 19 to 24. Row 2 blue trip bar t=7 to 21, then grey drop-off 21 to 26. Row 3 teal shared-trip bar from 5 to 19, then grey drop-off 19 to 24. Boundaries at 19/24,21/26,19/24 have numerical endpoint labels respectively. On M2 row only, the short loading segment 5–7 is pale amber; the trip after7 is teal. An amber arrow at exactly t=7 on the M2 row says "Second request joins at loading end". No separate second load for M2. Axis labeled "Time (s)"; ticks 5,10,15,20,25,30. Finish callout below: "Wave makespan: M₁ 26 s > M₂ 24 s". One small explanation "Sharing violates condition (c).".
(c) heading "Repositioning reversal · 4.3.2". Subtitle "Orders 1 → 8 then 8 → 7; second request at 54 s". Two horizontal timeline rows on one common exact scale from 54 to104 seconds. Row labels "M₁ unused slot", "M₂ car at floor 8". M1 row: hatched pale-blue empty repositioning from54 to89, blue trip from89 to98, grey drop-off from98 to103. Inside the long hatched segment: "Empty repositioning: 35 s". Endpoint labels54,89,98,103. M2 row: teal trip54 to63, grey drop-off63 to68. Endpoint labels54,63,68. Axis label "Time (s)", ticks54,64,74,84,94,104. The axis scale is specific to panel(c), not shared with(b). Before or under row labels, use a small neutral box "Earliest-available assignment" and "M₁: B=0, G=1   M₂: B=44, G=8". Finish callout below "Wave makespan: M₁ 103 s > M₂ 68 s". One small explanation "No sharing; condition (d) fails." All bar widths must match their numerical durations.
Bottom global compact legend: "Blue: M₁ trip   Teal: M₂ trip   Grey: AMR drop-off   Hatching: empty repositioning". Small parameter line "E=1, c=2, γ=5, τᴸ=τᵁ=2, τᴾ=τᴰ=5; times in seconds." Do not write any Fig number. Do not invent additional experiment points or change any numbers. This image illustrates exact numerical examples, not observational data.
```

### Targeted correction

```text
Edit this scientific three-panel diagram very conservatively. Preserve all upper-panel(a) mathematical conditions and arrows, all counterexample times, all palettes and labels except these specified changes. Panel(c) currently draws widths inconsistent with its numeric axis. REMOVE the horizontal Time(s) axis and all six ticks 54,64,74,84,94,104 at bottom of panel(c). In that freed space put the short centered note 'Event times in seconds; schematic spacing'. Keep event labels54,89,98,103 above the M1bar and54,63,68 above M2bar; keep all bar shapes unchanged. Panel(b)'s axis may stay unchanged. In panel(b), change ONLY the word 'Trip' on the TEAL segment of the M2 shared-car bar (the segment after the amber5–7 Load) to 'Travel + unload'. M1 bar labels Trip stay unchanged. Do not change the6specific event times or the final26>24 and103>68 comparisons. Keep lineweights, sans-serif typography, and panel layout consistent. No other changes.
```

## Figure 5

```text
Use case: scientific-educational. Create a clean publication figure for an operations-research journal, in the same unified visual family as a flat engineering warehouse schematic. White background, dark charcoal #24343F text and thin outlines, muted slate blue #52758D with pale blue #E7EEF3, teal #467F7D with pale teal #E3EFEC, muted amber #AF7C42 with pale amber #F5EAD8, neutral grey #EEF1F3. Flat 2D geometric drawing, no gradients, no shadow, no glossy effects, no decorative icons, no photos. Consistent Arial/Helvetica-like sans-serif text, math in clean italic serif with real subscripts and superscripts. Bold lowercase panel labels (a), (b), (c) where specified. All text readable at a full text-width print placement. No figure number or external caption inside image. Render at 3200 by 1800 pixels or higher comparable resolution. Keep labels short, ample white space, balanced alignment. All content is prescribed manuscript theory, not empirical data. Preserve exact symbols and arrow directions. No Chinese text.
FIGURE CONTENT: a clean 3-panel mathematical decision map. Panel (a) occupies left 65% of canvas; panel (b) upper right35%, panel (c) lower right35%. All mathematics uses proper subscript q, q_H, H and Greek symbols. Simple short labels and no decorative shapes.
(a) heading "Median-based reduction and stability · 4.4.1–4.4.2".
Top compact definition box:
"a_q = M₁ class median; b_q = M₂ class median"
"e_q = [a_q − b_q]₊; V_q = b_q + e_q"
A downward arrow to a diamond "a_q ≤ b_q for every q?"
YES branch goes left to teal box "V_q = b_q" / "M₂ minimization is robust-optimal".
NO branch goes down to a second diamond "Unique q_H and Δ_H > e_q_H?" Render e with q_H as its complete subscript. Above this diamond, a short line defining "q_H ∈ arg min_q b_q".
YES branch goes right to teal box "q_H remains the unique robust choice".
"Otherwise" branch goes down to amber box "Full-score comparison" / "q* ∈ arg min_q V_q".
No arrow should say that failure of a condition means the class changes.
Bottom annotation in this panel:
"Δ_H = min_{q ≠ q_H}(b_q − b_q_H)"
"Excess robust loss is bounded by e_q_H".
All branches unambiguous, no crossed arrow lines through boxes.
(b) heading "Distributional certificate · 4.4.2".
A vertical mini-chain of 3 grey/pale-blue boxes:
"Paired ordering violations" / "Pr(Y₁ > Y₂ | q) ≤ ε_q < 1/2"
then arrow to
"Median-neighborhood quantile gap" / "0 ≤ e_q ≤ U_q^mid(ε_q)"
then arrow to
"Δ_H > U_q_H^mid(ε_q_H)" / "certifies the same unique choice".
Footer "The certificate also requires unique q_H." Dashed short connector from final box to the stability branch of panel(a), route away from other labels.
(c) heading "Complementary extensions · 4.4.3".
TWO separate cards, no causal arrow between them.
First card "Mean-based Wasserstein comparison" with 3 short lines "Center P_q1; radius ρ_q = W₁(P_q1, P_q2)", "Under first-order stochastic ordering", "Worst mean = M₂ mean". Bottom tiny-but-readable line "A mean-based counterpart of the objective".
Second card "Finite evaluator family" with 2 lines "One evaluator has the largest median in every class", "Its median alone determines the minimax score".
Clearly segregate panel(c) from the median decision flow. DO NOT equate a median with an expectation, do not depict the Wasserstein ball as an empirical confidence guarantee, do not add M3 to the default two-model decision. No long prose paragraph inside figure.
```
