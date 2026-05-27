import sys

with open('CMakeLists.txt', 'r') as f:
    content = f.read()

old_fc = """fetchcontent_declare(tiff
  URL "https://download.osgeo.org/libtiff/tiff-4.7.0.tar.gz"
  URL_HASH MD5=3a0fa4a270a4a192b08913f88d0cfbdd)"""

new_fc = """fetchcontent_declare(tiff
  URL "https://download.osgeo.org/libtiff/tiff-4.7.0.tar.gz"
  URL_HASH MD5=3a0fa4a270a4a192b08913f88d0cfbdd
  PATCH_COMMAND "${PATCH}" -p1 -i "${CMAKE_CURRENT_SOURCE_DIR}/patches/tiff-zstd-conflict.patch")"""

if old_fc in content:
    content = content.replace(old_fc, new_fc)
    with open('CMakeLists.txt', 'w') as f:
        f.write(content)
    print("Successfully patched tiff fetchcontent_declare")
else:
    print("Could not find tiff fetchcontent_declare with expected content")
