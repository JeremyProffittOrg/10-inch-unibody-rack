# Acer four-bay shelf build

## Locked decisions (user-confirmed; do not revisit)
- 2026-11-16: "the shelves extend 3 inches past the back of the dgx's"
- 2026-11-16: "two 40x40 fan cut outs centered at the back behind the dgx's and one behind the power supply"
- 2026-11-16: "the rest of the back needs to be cut out for cables to pass"
- 2026-11-16: "a small 10mm tall wall on the left and right of the dgx, and for the first 5mm of either back and front corner to hold the dgx in place, same for the power supply"
- 2026-11-16: "cut outs as well in the shelf in the last 2 inches to allow cables to pass from shelf to shelf"
- 2026-11-16: "show me diasgrams of all of it, and open an stil in bambul labs of the shelves"
- 2026-11-14: "always open bambulabs projects with a cli call"

## Verified facts
- Workspace: C:/dev/10-inch-unibody-rack. Default branch: master. Origin: https://github.com/JeremyProffittOrg/10-inch-unibody-rack.git.
- Existing build_acer_v13.py marks its 70 x 160 x 36 mm brick UNVERIFIED.
- Delta manufacturer specification: ADP-240KB BA is 162 long x 72 wide x 23 high mm: https://filecenter.deltaww.com/Products/download/02/0201/Products-202310190855436362.pdf
- Acer specifies a 240 W USB-C adapter, but the exact adapter label of the operator's device is not verified: https://community.acer.com/en/en/kb/articles/19556-getting-started-with-the-acer-veriton-gn100-ai-workstation
- Prior approved layout: four 150 x 150 x 50.5 mm devices, five 5 mm shelves, 315 mm total height, 22 mm above devices, 22 mm horizontal outer/inter-device gaps, 5 mm outer walls.
- Existing build.sh/generate.bat and .github/workflows/release.yml build all root SCAD files. Generated STL/PNG files stay out of source commits.
- Existing unrelated changes: CLAUDE.md modified, agents.md untracked, two concept-v13 logs untracked. Preserve these files.

## Assumptions
- ADP-240KB BA dimensions are the candidate Acer brick size. Operator was asked for measured dimensions or exact label; no answer yet. Do not claim physical Acer PSU fit is confirmed.
- Standard 40 mm fans: 32 mm screw pitch, 3.4 mm M3 clearance holes, 35 mm circular flow openings. A complete 40 mm square through-hole would remove the standard screw locations.
- 0.6 mm clearance per device edge; 3 mm retaining-wall thickness; front/rear corner returns cover 5 mm of device width.
- One-piece rear-face-down print places shelf edges on the bed. Rotation gives bed footprint 315 x 298 mm; depth is the print height.
- Fans attach outside the rear; fan thickness and rear cables are not included in printed-part depth.

## shelf-model — build the requested geometry
### shelf-source — add the native parametric model
- [x] shelf-geometry — five shelves, sidewalls, eight retaining pockets, twelve fan mounts, ten cable passages.
- [x] shelf-validation — OpenSCAD assertions plus binary STL manifold and bounds checks pass.
Definition of done: C:/Users/Jeremy/.local/bin/uv.exe run --python 3.13 --with matplotlib python build_acer_four_bay.py exits 0.

## shelf-delivery — document and open the model
Depends on: shelf-source
### shelf-diagrams — render the model and detail drawings
- [x] shelf-drawings — front/rear 1024 PNGs, dimensioned front/top/rear/detail PNGs and corresponding MD/README.
Definition of done: build command above exits 0 and output/acer-four-bay/validation.json reports passed=true.
### shelf-publication — commit, push and monitor
- [x] shelf-commit — stage only the new design, its script/docs, README and plan; commit and push master.
- [x] shelf-workflow — monitor resulting GitHub Build and Release workflow to terminal success.
- [x] shelf-open — invoke Bambu Studio CLI with only the final shelf assembly STL; no desktop control.
Definition of done: git diff --check exits 0, GitHub workflow terminal success, Bambu CLI launch returns no launch error.

## Stop conditions (only these)
- Missing credentials needed to push/monitor delivery.
- A destructive or unrelated change would be required.
- Operator contradicts the candidate PSU dimensions; regenerate with supplied values.
- Exact Acer PSU fit remains unconfirmed if no label/measurement arrives; deliver a clearly labeled candidate rather than claiming measured fit.

## Job policy
- Each OpenSCAD subprocess: capture exit status/stdout/stderr; 10-minute timeout. Deterministic failure: fix first, maximum two corrected retries; transient failure: one retry after 5 seconds. No concurrent retry mechanisms.
- GitHub workflow: monitor success/failure/cancellation and timeout; diagnose a failed run before a bounded corrected push. Maximum two corrected pushes.
- Bambu: one CLI launch after file validation; capture spawn error, report import unverified without UI permission. Do not close existing user sessions.

## Execution log
- 2026-11-16: read existing CAD generator, README, build scripts and workflow. git status preserved unrelated changes; git remote show origin confirmed master.
- 2026-11-16: manufacturer specification resolves candidate PSU body dimensions; OEM identification remains an explicit assumption.

- 2026-11-16: First build rendered in 29 seconds. Validator incorrectly merged distinct STL vertices by rounding to four decimals. Changed validation to compare exact binary STL coordinates; no geometric failure was hidden. Recheck job PID 30708.

- 2026-11-16: uv run --python 3.13 --with matplotlib python -u build_acer_four_bay.py exited 0. STL: 13,476 triangles; all edges twice with consistent winding; one connected component; positive volume 2,500,707.19 mm3; bounds 315 x 298 x 229.8 mm. Native front/rear PNGs 1024 square. Annotated drawings visually checked. Upright mesh render section additionally executed successfully after shading adjustment.
- 2026-11-16: gh auth status reports no login; git fetch origin master succeeds. Delivery monitoring will use the public GitHub API if push succeeds. No credential values were read.

- 2026-11-16: Launched final STL through Bambu Studio CLI, PID 7268. No desktop control. Import completion is not asserted without UI evidence. Upright CAD rear render exited 0; CAD renderer replaces the temporary Matplotlib surface renderer.

- 2026-11-16: Focused commit 11ced752c4c71732c7c6e00f141819984ad2a7e0 pushed successfully using existing Git credentials. GitHub run 43880478356 is monitored through the public API; currently building artifacts.
- 2026-11-16: Exact STL triangle/box SAT checks passed for eight device envelopes, eight raised front-insertion paths and two unobstructed vertical cable corridors. Three detail PNGs opened via CLI.

- 2026-11-16: Final full rebuild failed during OpenBLAS import with memory allocation error. Set OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1 inside the build process before numeric imports; bounded corrected retry PID 28892.

- 2026-11-16: Numeric thread bound succeeded; final retry passed all mesh and fit checks but Pillow could not overwrite open shelf-plan.png (Errno 22). Changed PNG generation to write sibling temporary PNGs then atomically replace completed outputs. Second corrected retry PID 42044; no user applications closed.

- 2026-11-16: Full final build exited 0 after atomic PNG write fix. One-time support audit started PID 22712; normal automatic supports at 45 degrees, max 5 mm bridge, 10-minute timeout ceiling, no blind retry.

- 2026-11-16: Final command C:/Users/Jeremy/.local/bin/uv.exe run --python 3.13 --with matplotlib python -u build_acer_four_bay.py exited 0. All mesh, fit, insertion, cable and render checks passed. This run verified both single-thread numerical imports and atomic PNG replacement with viewers left open.

- 2026-11-16: GitHub Build and Release run 43880478356 completed SUCCESS. Verified release assets acer-four-bay-shelves.stl (673884 bytes), front PNG (31411 bytes), rear PNG (30184 bytes). Native model source is unchanged by subsequent local verification-script improvements.

- 2026-11-16: Optional Bambu support audit exceeded its 600-second limit without a sliced project, result.json, or captured output. Terminated only own audit PID 22712. No retry. Support-free slicing remains UNVERIFIED; earlier requested GUI STL launch is separate and left running.

## Rounded revision locked decisions (user-confirmed; do not revisit)
- 2026-11-16: "move the fans to the far left and right of the dgx including thed 22mm spacing"
- 2026-11-16: "wiring hole should not be a diamond"; width 80% of the respective device; start 12.7 mm behind that device and end 25.4 mm before the rack rear; rounded inside.
- 2026-11-16: "make sure all edges are rounded"; open in a different Bambu Studio copy.
- 2026-11-16: fit-test STL has a 2 mm base, 10 mm walls above it, trimmed from the PSU left retainer to the DGX right retainer, with full outer front/back/side perimeter.

## rounded-shelves — relocate fans and round all model edges
- [x] fit-test-coupon — generated output/acer-fit-test/acer-fit-test.stl; closed mesh and 251.2 x 169.2 x 12 mm bounds checked; Bambu CLI PID 26188. Source pocket snapshot retained with generated coupon to keep its geometry reproducible.
- [x] rounded-geometry — reuse existing CadQuery dependency to replace sharp SCAD construction; one geometry implementation plus SCAD mesh viewer. Keep device pockets, outer dimensions and shelf spacing.
- [x] rounded-proof — valid single CAD solid, no sharp CAD edges, closed STL, unchanged printer bounds, 80% cable widths, correct endpoints, device insertion clear.
- [x] rounded-diagrams — update plan/rear/assembly diagrams and documentation.
- [x] rounded-delivery — commit/push, monitor release, launch revised STL in a separate Bambu process through CLI.
Definition of done: C:/Users/Jeremy/.local/bin/uv.exe run --python 3.13 --with cadquery --with matplotlib python build_acer_four_bay.py exits 0; resulting release succeeds.
Files: acer-four-bay-shelves.scad (viewer), acer_four_bay_geometry.py (replacement CAD implementation), build_acer_four_bay.py, build.sh, generate.bat, .github/workflows/release.yml (existing dependency setup), design documentation, README, plan.md.
Non-goals: change the fit-test STL already opened; change device dimensions or outer rack size.
Geometry choices: 0.5 mm edge fillets throughout, 3 mm plan radii inside cable windows; fan bodies occupy the far edges of the DGX+44 mm lane, centre X=119 and273. PSU fan X=63 stays unchanged. Right outer wall replaces the redundant rightmost fan post. Large rectangular cable windows override the earlier diamond support-free geometry; no support-free claim.

### rounded-restart-policy
- Native CAD build: log exit/failure, 10-minute limit; diagnose deterministic failure before retry, at most two corrected retries per failing geometry.
- Release: existing pipeline, monitor failure and success; no blind retries.
- Bambu launch: separate new process, preserve all existing sessions; no GUI or desktop-control verification.

### rounded-execution-log
- 2026-11-16: One-bay proof found a 1 mm redundant fan-post overlap at the right outer wall. Removed that redundant post; the wall directly supports the mount. All 310 remaining sharp edges accepted 0.5 mm fillets; valid one-solid result, zero remaining discontinuities.

- 2026-11-16: Full four-bay native CAD succeeded: 1,108 edges rounded at R0.5, one valid solid, zero sharp edges. Print-scale STL tessellation uses 0.15 mm deflection and 0.35 rad angular tolerance. Binary float32 encoding collapsed 136 zero-area facets; exporter removes only zero-area facets, then independent closed-manifold/winding/component checks passed. All eight device and insertion paths plus both cable routes passed.
- 2026-11-16: Full final rounded build started PID 29804; CAD dependency pinned to the locally verified 2.8.0 for CI.

- 2026-11-16: Final rounded build exited 0: uv run --python 3.13 --with cadquery==2.8.0 --with matplotlib python -u build_acer_four_bay.py. CAD, mesh, dimensions, 80% window geometry, device insertion and cable path checks passed; all diagrams rendered and visually checked. Revised STL launched in distinct Bambu CLI PID 55644; fit-test process PID 26188 remains separate.

- 2026-11-16: Commit d695d9a2a4974278f0b63f2209f8fa427770b4ea pushed. Release run 43927698784 is in progress; dependency setup completed and artifact build is active. Confirmed separate running Bambu processes 26188 (fit test) and 55644 (rounded shelves) through read-only process queries, not desktop control.

- 2026-11-16: Windows generate.bat now selects the existing local uv executable when available, using the same pinned CadQuery command already verified in the full build. This avoids requiring python on PATH on this machine; Linux CI remains unchanged.

- 2026-11-16: Release run 43927698784 completed SUCCESS. Downloaded published STL: 9,973,084 bytes, 199,460 triangles, bounds 315 x 298 x 229.800006 mm; binary length and bounds passed. Front/rear release PNGs also present. Geometry unchanged by the Windows entry-point follow-up.
