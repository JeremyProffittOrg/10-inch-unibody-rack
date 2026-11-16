#!/bin/bash
# Generate STL and preview images for 10-Inch Unibody Rack
# Output files are gitignored - GitHub Actions pipeline generates them for releases

OPENSCAD="openscad"
OUTPUT_DIR="output"

echo "Creating output directories..."
mkdir -p "${OUTPUT_DIR}/stl"
mkdir -p "${OUTPUT_DIR}/images"

echo "Building rounded Acer shelf geometry..."
python3 acer_four_bay_geometry.py || exit 1

# Process all SCAD files
for scad_file in *.scad; do
    # Skip if no .scad files found
    [ -e "$scad_file" ] || continue

    # Get filename without extension
    name="${scad_file%.scad}"

    # Skip shared config files — not standalone parts
    if [[ "$name" == "all-racks-config" ]]; then
        continue
    fi

    echo ""
    echo "=== Processing ${name} ==="

    if [[ "${name}" == waveshare-7inch-lcd-case-* ]]; then
        echo "  Building base STL..."
        ${OPENSCAD} --export-format binstl -D 'part="base"' \
            -o "${OUTPUT_DIR}/stl/${name}-base.stl" "${scad_file}"

        echo "  Building lid STL..."
        ${OPENSCAD} --export-format binstl -D 'part="lid"' \
            -o "${OUTPUT_DIR}/stl/${name}-lid.stl" "${scad_file}"
    else
        echo "  Building STL..."
        ${OPENSCAD} --export-format binstl \
            -o "${OUTPUT_DIR}/stl/${name}.stl" "${scad_file}"
    fi

    echo "  Rendering front view..."
    ${OPENSCAD} --render \
        -o "${OUTPUT_DIR}/images/${name}_front.png" \
        --camera=0,0,0,55,0,45,0 \
        --autocenter --viewall \
        --imgsize=1024,1024 \
        --colorscheme=Tomorrow \
        "${scad_file}"

    echo "  Rendering rear view..."
    ${OPENSCAD} --render \
        -o "${OUTPUT_DIR}/images/${name}_rear.png" \
        --camera=0,0,0,55,0,225,0 \
        --autocenter --viewall \
        --imgsize=1024,1024 \
        --colorscheme=Tomorrow \
        "${scad_file}"

    echo "  Done with ${name}"
done

echo ""
echo "=== Build Complete ==="
echo ""
echo "STL files:"
ls -1 "${OUTPUT_DIR}/stl/"*.stl 2>/dev/null || echo "  No STL files generated"
echo ""
echo "Image files:"
ls -1 "${OUTPUT_DIR}/images/"*.png 2>/dev/null || echo "  No images generated"
