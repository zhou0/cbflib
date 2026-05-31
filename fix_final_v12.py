import re

with open('CMakeLists.txt', 'r') as f:
    content = f.read()

# 1. Properly set system-first HDF5 discovery name
content = content.replace('if(FALSE OR HDF5_FOUND)', 'if(CBF_AUTO_hdf5_FOUND OR HDF5_FOUND)')

# 2. Fix the shared library forcing variables and patching logic
# We need to make sure we don't have duplicates or bad logic.

# The current block has duplicates and some issues.
# I'll replace the whole if(CBF_WITH_HDF5) block with a clean one that uses the patch.

clean_hdf5_block = r"""if(CBF_WITH_HDF5)
  set(BUILD_TESTING OFF CACHE INTERNAL
    "Build HDF5 unit testing")
  set(HDF5_ALLOW_EXTERNAL_SUPPORT "TGZ" CACHE INTERNAL
    "Allow external library building (NO GIT TGZ)")
  set(HDF5_EXTERNALLY_CONFIGURED ON CACHE INTERNAL
    "HDF5 configured externally")
  set(HDF_PACKAGE_NAMESPACE "hdf5::" CACHE INTERNAL
    "Name for HDF package namespace (can be empty)")
  set(LIBAEC_TGZ_NAME "libaec-1.1.3.tar.gz" CACHE INTERNAL
    "Use SZIP AEC from compressed file")
  set(LIBAEC_TGZ_ORIGPATH
    "https://github.com/MathisRosenhauer/libaec/releases/download/v1.1.3"
    CACHE INTERNAL
    "Use LIBAEC from original location")
  set(ZLIB_TGZ_NAME "zlib-1.3.1.tar.gz" CACHE INTERNAL
    "Use HDF5_ZLib from compressed file")
  set(ZLIB_TGZ_ORIGPATH
    "https://github.com/madler/zlib/releases/download/v1.3.1"
    CACHE INTERNAL
    "Use zlib from original location")

  # Try to use system libraries first (installed by auto-install macro)
  set(ZLIB_USE_EXTERNAL ON CACHE BOOL "" FORCE)
  set(SZIP_USE_EXTERNAL ON CACHE BOOL "" FORCE)

  # Ensure internal builds are shared
  set(ZLIB_BUILD_SHARED_LIBS ON CACHE BOOL "" FORCE)
  set(ZLIB_BUILD_STATIC_LIBS OFF CACHE BOOL "" FORCE)
  set(LIBAEC_BUILD_SHARED_LIBS ON CACHE BOOL "" FORCE)
  set(LIBAEC_BUILD_STATIC_LIBS OFF CACHE BOOL "" FORCE)
  set(HDF5_USE_LIBAEC_STATIC OFF CACHE BOOL "" FORCE)

  FetchContent_GetProperties(hdf5)
  if(NOT hdf5_POPULATED)
    FetchContent_Populate(hdf5)
    # Patch HDF5's internal ZLIB and LIBAEC to build as shared
    message(STATUS "Patching internal HDF5 ZLIB and LIBAEC for shared build...")

    file(READ "${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" zlib_content)
    string(REPLACE "add_library(${ZLIB_LIB_TARGET} STATIC" "add_library(${ZLIB_LIB_TARGET} SHARED" zlib_content "${zlib_content}")
    file(WRITE "${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" "${zlib_content}")

    file(READ "${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" libaec_content)
    string(REPLACE "add_library (${LIBAEC_LIB_TARGET} STATIC" "add_library (${LIBAEC_LIB_TARGET} SHARED" libaec_content "${libaec_content}")
    string(REPLACE "add_library (${SZIP_LIB_TARGET} STATIC" "add_library (${SZIP_LIB_TARGET} SHARED" libaec_content "${libaec_content}")
    file(WRITE "${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "${libaec_content}")

    add_subdirectory(${hdf5_SOURCE_DIR} ${hdf5_BINARY_DIR})
  endif()
"""

# Match the block
content = re.sub(r'if\(CBF_WITH_HDF5\).*?add_subdirectory\(\$\{hdf5_SOURCE_DIR\} \$\{hdf5_BINARY_DIR\}\)\s*endif\(\)', clean_hdf5_block, content, flags=re.DOTALL)

with open('CMakeLists.txt', 'w') as f:
    f.write(content)
