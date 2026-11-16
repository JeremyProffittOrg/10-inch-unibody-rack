@echo off
REM Generate STL and preview images for 10-Inch Unibody Rack
REM Output files are gitignored - GitHub Actions pipeline generates them for releases

set OPENSCAD="C:\Program Files\OpenSCAD\openscad.exe"
set OUTPUT_DIR=output

echo Creating output directories...
if not exist %OUTPUT_DIR%\stl mkdir %OUTPUT_DIR%\stl
if not exist %OUTPUT_DIR%\images mkdir %OUTPUT_DIR%\images

REM Build the rounded shelf mesh before its SCAD viewer is rendered.
python acer_four_bay_geometry.py
if errorlevel 1 exit /b 1

REM Process all SCAD files
for %%f in (*.scad) do (
    REM Skip shared config files - not standalone parts
    if not "%%~nf"=="all-racks-config" (
        echo.
        echo === Processing %%~nf ===

        echo %%~nf| findstr /b /c:"waveshare-7inch-lcd-case-" >nul
        if errorlevel 1 (
            echo   Building STL...
            %OPENSCAD% --export-format binstl -o %OUTPUT_DIR%\stl\%%~nf.stl "%%f"
        ) else (
            echo   Building base STL...
            %OPENSCAD% --export-format binstl -D "part=\"base\"" -o %OUTPUT_DIR%\stl\%%~nf-base.stl "%%f"

            echo   Building lid STL...
            %OPENSCAD% --export-format binstl -D "part=\"lid\"" -o %OUTPUT_DIR%\stl\%%~nf-lid.stl "%%f"
        )

        echo   Rendering front view...
        %OPENSCAD% --render ^
            -o %OUTPUT_DIR%\images\%%~nf_front.png ^
            --camera=0,0,0,55,0,45,0 ^
            --autocenter --viewall ^
            --imgsize=1024,1024 ^
            --colorscheme=Tomorrow ^
            "%%f"

        echo   Rendering rear view...
        %OPENSCAD% --render ^
            -o %OUTPUT_DIR%\images\%%~nf_rear.png ^
            --camera=0,0,0,55,0,225,0 ^
            --autocenter --viewall ^
            --imgsize=1024,1024 ^
            --colorscheme=Tomorrow ^
            "%%f"

        echo   Done with %%~nf
    )
)

echo.
echo === Build Complete ===
echo.
echo STL files:
dir /b %OUTPUT_DIR%\stl\*.stl 2>nul || echo   No STL files generated
echo.
echo Image files:
dir /b %OUTPUT_DIR%\images\*.png 2>nul || echo   No images generated
