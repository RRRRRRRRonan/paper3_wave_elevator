# Registrations of 2026-09-26 (IJPR revision), index

Status (2026-09-26, updated after the registered run): S1A, S1B, the Phase 6 protocol (L1), the decision sheet, and the story contract are SIGNED, and S1C and S1D are ACKNOWLEDGED, all pinned in `archive_package/MANIFEST_SIGNED.json` (superseded manifests are kept beside it). The L1 set is registered on OSF under embargo as https://osf.io/kps2c; the S1D update set is prepared in `archive_package/osf_update_2026-09-26_S1D/` and is still to be submitted by the author. All eleven registered Study 1 commands and the three completion modules ran on 2026-09-26 (EXECUTION-LOG entries 55 to 58; results in `../study1_run_2026-09-26/STUDY1_RESULTS_SUMMARY.md`). The L2 addendum is PENDING (week 4); no Study 2 test pool has been generated.

| File | Items | Tag | Status (2026-09-26) |
|---|---|---|---|
| `AMEND-2026-09-26-S1A_reanalyses.md` | S1-1 clustered bootstrap; S1-6 minimax-regret and stability; S1-7 Supp-1 coupling display; TH-2 abstraction-bias display | [RA] | SIGNED; run 2026-09-26 (S1-1, S1-6, S1-7, TH-2) |
| `AMEND-2026-09-26-S1B_new_simulations.md` | S1-2 full-pool enumeration; S1-3 Block C extension; S1-8 best-wave location; S1-9 tie-break regeneration of Blocks A and B; S1-11 complementary fractions; S1-12 B-5 rerun under the corrected DES-M2 boarding rule | [NS], S1-9 and S1-12 [QA] | SIGNED, S1-11 box ticked; run 2026-09-26 (S1-2, S1-3, S1-8, S1-9, S1-11, S1-12) |
| `AMEND-2026-09-26-S1C_execution_note_B4_B6.md` | S1-4 = AMEND-B B-4; S1-5 = AMEND-B B-6(ii) | already signed 2026-07-08 | ACKNOWLEDGED; run 2026-09-26 (S1-4, S1-5) |
| `AMEND-2026-09-26-S1D_execution_deviation.md` | execution deviation: code changes after signing (guard checkbox fix, code-tree provenance in the Study 1 outputs, S1D required by the guard); evidence in `../helper_reports/S1D_equivalence_2026-09-26.md` | no new item | ACKNOWLEDGED and pinned; OSF update to be submitted by the author |
| `../../paper_draft/phase6_method_study_protocol.md` | Study 2 (Phase 6) | [NS] P6 | SIGNED (L1); Study 2 not run |
| `../../paper_draft/phase6_protocol_L2_addendum.md` | Study 2 Stage L2 (P11 weights, case parameters, code hash, OSF id) | [NS] P6 | PENDING; filled and signed in week 4 |

Order of use after signing (steps 1 to 3 were carried out on 2026-09-26; see EXECUTION-LOG):
1. Pin the SHA-256 of every signed file: `archive_package/make_manifest.py SIGNED`.
2. Upload the package to OSF Registries (decision D-J) or keep the internal timestamped manifest if D-J is not signed.
3. Only then run the scripts. Each script refuses to run until its registration's `author_signoff` field starts with `SIGNED` (`ACKNOWLEDGED` for the S1C and S1D execution notes) and its bytes equal the pinned hash (`prototype/src/registration_guard.py`).

Relation to the frozen files: `paper_draft/phase5_scaleup_preregistration.md` and the six signed amendments of 2026-07-08 are not edited (decision D-I). The preregistration stays byte-identical and no pointer is appended to it; the pointer to the 2026-09-26 registrations goes into the manuscript's registration appendix (decision D-I as signed).
