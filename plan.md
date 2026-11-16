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
- [ ] shelf-commit — stage only the new design, its script/docs, README and plan; commit and push master.
- [ ] shelf-workflow — monitor resulting GitHub Build and Release workflow to terminal success.
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
