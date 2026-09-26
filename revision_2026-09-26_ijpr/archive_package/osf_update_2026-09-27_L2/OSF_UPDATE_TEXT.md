# OSF update of registration kps2c: Stage L2 addendum (2026-09-27)

Paste the "Justification" and "Summary" blocks into the update form; upload the files of this folder to the
project's OSF Storage (folder `osf_update_2026-09-27_L2`) first. Submit the S1D update (`osf_update_2026-09-26_S1D/`)
before this one if it has not been submitted yet, so the updates appear in the order in which they were made.

## Justification (for the update form)

The registered protocol (Study 2, Section 5.4 and Section 12) fixes a Stage L2 step that is completed after the L1
registration and before any test pool is generated: tuning of the P11 weights on training pools, the runtime
projection, the code freeze and its validation (G0), and the case parameters. The protocol bytes are frozen, so these
values are registered in a separate addendum, signed on 2026-09-27 and pinned in the SIGNED_L2 manifest. No Study 2
test pool or case pool had been generated when it was signed.

## Summary (for the update form)

Stage L2 addendum to the Phase 6 (Study 2) protocol, signed 2026-09-27.
- Protocol L1 SHA-256 (line-ending normalized): a92d93c1a1cbe900c29c50734b2de0802fc7dd01afa99f378761f7a8ecc0d0d7
- L2 addendum SHA-256 (line-ending normalized, as pinned): 891e727e9759de9685639cd1e7130f616389e4d737fe74da1d20d0f64200118d
- Code tree SHA-256 frozen at tuning: ccdbd6d28c96a2903b24573c1e71ac29e152f609f2bb7083493a4c84fe26c581
- P11 weights (alpha, beta, gamma) = (1, 1, 0.5), selected by the registered rule on 108 training instances (four
  triples tied exactly; the registered lexicographic rule applies, and the tied triples generate identical candidates).
- Runtime projection 2.6 hours, so the DES subset mode is off.
- Calibrated case included (decision D-K); data UCI Online Retail II (CC BY 4.0), workbook SHA-256
  bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980, Section 11.2 checks passed.
- Case parameters (midpoint; range, seconds): travel per floor 13.81 (6.76, 20.86); loading 15.15 (8.3, 22.0);
  unloading 14.705 (7.8, 21.61); AMR service 10.5 (1.0, 20.0). The sources, a declared deviation from the source types
  named in Section 11.3, and three decisions recorded before signature are in the addendum.
- G0 checks 1 to 7 passed.
- SIGNED_L2 manifest: 185 files, generated 2026-09-26T17:06:08Z at git commit b1eaff7.
Uploaded files and their SHA-256, line-ending normalized as in the addendum and the manifests (registration_guard.sha256_file; SHA256SUMS.txt in the upload gives the raw-byte hashes of the same copies):
- phase6_protocol_L2_addendum.md: 891e727e9759de9685639cd1e7130f616389e4d737fe74da1d20d0f64200118d
- MANIFEST_SIGNED_L2.json: f046327609a853ef327c5b6c974fd87c1d62a30167962a774975b9fbbba6b4ba
- MANIFEST_SIGNED_L2.md: c3ce16572451434d02b8315f1d18d3827db2d3c42914a05765cb9f58916a24b2
- v0_6_phase6_L2_tuning.json: 6fa28f9493133c5fcc9ba4420b926c3e40aec3dfb54fd12f3b42cfbb62ebfe66
- g0_item6_guard_check.json: 8a6a087c8bd371c20a0a7b82fb513309f296f13ce91516424d02a06134386ae8
- case_data_check_2026-09-27.json: 868152e7770692d26b9cc2fe55d23a870e0deb5adba155b8c9392155074d0638
- case_parameters_README.md: e41ff28653f6308885be729c32e6cb3decc16a496f436e0020697505f3fd7ef7
- case_params_proposed_for_L2.json: e31d0ec23e59e50091c406e3ca3c9d383f64d76ed8fc126479d2937e1c2caa90
- case_parameters_evidence_wf_d3eb6a5e-3c6.json: 87b210aa0d56ad51ab16a838f9fc62de5d2e54144c507dda23c84289b994bfe9
