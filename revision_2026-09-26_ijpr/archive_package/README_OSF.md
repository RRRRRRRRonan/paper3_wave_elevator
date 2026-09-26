# Registration package for OSF Registries (draft, not uploaded)

Prepared 2026-09-26 by the assistant at the author's request. **Nothing has been uploaded.** Uploading needs the author's OSF account and decision D-J.

## 1. What goes into the registration

| Component | Files |
|---|---|
| Study 2 protocol (Phase 6) | `paper_draft/phase6_method_study_protocol.md` (signed version) |
| Study 1 registrations | `revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1A_reanalyses.md`, `...-S1B_new_simulations.md`, `...-S1C_execution_note_B4_B6.md`, `README.md` |
| Decision record and story | `revision_2026-09-26_ijpr/01_DECISIONS_TO_SIGN.md` and `revision_2026-09-26_ijpr/STORY_CONTRACT.md` (signed versions; the story contract pre-commits the wording rules of §8) |
| Frozen context (read only) | `paper_draft/phase5_scaleup_preregistration.md`; `paper_draft/theorems_m4.md`, `theorems_m5.md`, `methodology_v0_2.md` (linked from the preregistration); `prototype/results/configs_v0_5.json`; the six amendments in `revision_2026-07-08/amendments/` |
| Hash manifest | `MANIFEST_SIGNED.md` and `.json` from `make_manifest.py SIGNED`, run after signing |
| Stage L2 (week 4, as an OSF update) | `paper_draft/phase6_protocol_L2_addendum.md` (signed) and `MANIFEST_SIGNED_L2.*` |

Code and data are not part of the registration. Under decision D-J, option J4 (chosen by the author on 2026-09-26), they go to the editor and reviewers as confidential supplementary material at submission and, after publication, are provided by the author upon reasonable request; they are not deposited in a public repository. Before submission, check which Taylor & Francis data-sharing policy IJPR applies: J4 fits "Basic" and "Share upon reasonable request"; if the journal requires publicly available data, fall back to option J3 (Zenodo release after acceptance; a Zenodo record shows its title, authors, and abstract even under embargo, so nothing goes there before acceptance).

## 2. Suggested OSF metadata

- **Registration template:** "OSF Preregistration" or "Open-Ended Registration" (the open-ended form accepts the protocol file as an attachment and is the simpler choice).
- **Title:** Registered analyses for a study of wave composition under shared freight elevators in multi-story AMR warehouses (Study 1 re-analyses and Study 2 method study)
- **Description (one paragraph):** This registration fixes, before execution, (i) re-analyses and new simulations that complete a preregistered simulation study of wave composition under shared freight elevators (Study 1), and (ii) a method study of a generate, screen, and verify release procedure evaluated with closed-form and event-driven evaluators (Study 2). All designs, seeds, metrics, gates, and wording rules are in the attached files; their SHA-256 hashes are listed in the manifest.
- **Contributors:** the author(s) as on the manuscript.
- **License:** CC BY 4.0 for the documents.
- **Embargo (required by D-J):** register under embargo, not as a public registration. Pick an end date at most 4 years ahead and end the embargo early when the paper is accepted. Nothing is public before then, while the registration date stays verifiable. A registration that has been made public cannot be embargoed again. During the embargo, share it with the editor through a view-only link (OSF also offers anonymized view-only links). The signed files carry the author's name, which an anonymized link does not hide, so under double-anonymous review the review version of the manuscript cites the registration without the link.

## 3. Honest statement on earlier registrations (for the paper's registration appendix)

The repository record supports the following statements, and no stronger ones:

1. **Phase 5 preregistration (2026-05-19).** Its text records the author's sign-off on 2026-05-19 after the smoke gate, and two same-day amendments (§9.1, §9.2) logged "before the W6 confirmatory analysis". Its first git commit is `2c47cc5` (2026-05-20 00:29 +0900), the same commit that added the Phase 5 results. The file's last modification time (2026-05-19 23:19 +0900) is later than the Phase 5 raw result files (20:28 +0900) and the supplementary results (23:16 +0900); the text includes execution notes recorded that evening. The repository therefore cannot show independently that the locked design preceded the results. The paper should call it an internally locked preregistration with a documented sign-off, and should not claim an external timestamp.
2. **Amendments of 2026-07-08.** Signed in their text. They are not tracked by git (untracked as of 2026-09-26), and at least one was last modified on 2026-07-18 (`AMEND-2026-07-08-B_deferred_experiments.md`, a dated addendum). Only file-system timestamps exist.
3. **Registrations of 2026-09-26.** If uploaded to OSF before any registered analysis runs, these are the first registrations of the project with an external, verifiable timestamp. The paper can state this directly.

Suggested appendix sentence: "The Phase 5 design was locked internally on 19 May 2026 and is reported with its signed text; the Study 1 re-analyses and the Study 2 protocol were registered on OSF on [date] ([identifier]) before any of them was executed."

## 4. Steps for the author

1. Sign `01_DECISIONS_TO_SIGN.md`, `STORY_CONTRACT.md`, the Study 2 protocol (L1), and the Study 1 registrations: in one edit per file, set `author_signoff` to `SIGNED (<name>, <date>)` (S1C may read `ACKNOWLEDGED (<name>, <date>)`) and replace the `status` line (tick the S1-11 box in S1B if D-D1 is signed).
2. Run `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`. This pins the signed bytes; from now on `src/registration_guard.py` stops every registered script if a signed file changes. The script refuses to overwrite an existing signed manifest unless `--supersede` is given, and then keeps the old one.
3. Create the OSF registration; attach the files of §1 and `MANIFEST_SIGNED.md`; choose an embargo (not "make public"); submit.
4. Record the OSF identifier in the manuscript's registration appendix and, in week 4, in the L2 addendum. Never write it into a signed file (that would change its hash).
5. Only then run any registered script.
6. Week 4: fill and sign the L2 addendum, run `make_manifest.py SIGNED_L2`, and register it as an OSF update before any test pool is generated.
7. At submission: give the code and data release package (plan item P-6) to the editor and reviewers as confidential supplementary material, and keep that exact package with its hashes so that later requests receive the version used in the paper. Data availability statement: "The simulation code and the generated data that support the findings of this study are available from the corresponding author upon reasonable request. The study's registrations are available on OSF at [link]."
8. After acceptance: end the OSF embargo so that readers can check the registrations; code and data stay available upon reasonable request (D-J, J4).

## 5. Stage L2 addendum (week 4)

The Stage L2 content (P11 hyperparameters, case parameter table, G0 code hash, OSF id, and the L1 hash) lives in a separate file, `paper_draft/phase6_protocol_L2_addendum.md`, so the signed protocol bytes never change. Register it as an OSF update (or a linked second registration) on the day it is signed, with the `SIGNED_L2` manifest.
