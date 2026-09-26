# Registrations of 2026-09-26 (IJPR revision), index

All files here are DRAFTS prepared overnight on 2026-09-26. None is signed and nothing registered here has been run.

| File | Items | Tag | Needs |
|---|---|---|---|
| `AMEND-2026-09-26-S1A_reanalyses.md` | S1-1 clustered bootstrap; S1-6 minimax-regret and stability; S1-7 Supp-1 coupling display; TH-2 abstraction-bias display | [RA] | signature |
| `AMEND-2026-09-26-S1B_new_simulations.md` | S1-2 full-pool enumeration; S1-3 Block C extension; S1-8 best-wave location; S1-9 tie-break regeneration of Blocks A and B; S1-11 complementary fractions; S1-12 B-5 rerun under the corrected DES-M2 boarding rule | [NS], S1-9 and S1-12 [QA] | signature; S1-11 only if D-D1 is signed |
| `AMEND-2026-09-26-S1C_execution_note_B4_B6.md` | S1-4 = AMEND-B B-4; S1-5 = AMEND-B B-6(ii) | already signed 2026-07-08 | acknowledgement of the two new details |
| `../../paper_draft/phase6_method_study_protocol.md` | Study 2 (Phase 6) | [NS] P6 | signature (L1 now) |
| `../../paper_draft/phase6_protocol_L2_addendum.md` | Study 2 Stage L2 (P11 weights, case parameters, code hash, OSF id) | [NS] P6 | filled and signed in week 4 |

Order of use after signing:
1. Pin the SHA-256 of every signed file: `archive_package/make_manifest.py SIGNED`.
2. Upload the package to OSF Registries (decision D-J) or keep the internal timestamped manifest if D-J is not signed.
3. Only then run the scripts. Each script refuses to run until its registration's `author_signoff` field starts with `SIGNED` and its bytes equal the pinned hash (`prototype/src/registration_guard.py`).

Relation to the frozen files: `paper_draft/phase5_scaleup_preregistration.md` and the six signed amendments of 2026-07-08 are not edited (decision D-I). The preregistration stays byte-identical and no pointer is appended to it; the pointer to the 2026-09-26 registrations goes into the manuscript's registration appendix (decision D-I as signed).
