import re

with open('CMakeLists.txt', 'r') as f:
    content = f.read()

# 1. Merge the patch logic into CMakeLists.txt instead of including an external file.
patch_logic = r"""    # Patch HDF5's internal ZLIB and LIBAEC to build as shared
    message(STATUS "Patching internal HDF5 ZLIB and LIBAEC for shared build...")

    file(READ "${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" zlib_content)
    string(REPLACE "add_library(${ZLIB_LIB_TARGET} STATIC" "add_library(${ZLIB_LIB_TARGET} SHARED" zlib_content "${zlib_content}")
    file(WRITE "${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" "${zlib_content}")

    file(READ "${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" libaec_content)
    string(REPLACE "add_library (${LIBAEC_LIB_TARGET} STATIC" "add_library (${LIBAEC_LIB_TARGET} SHARED" libaec_content "${libaec_content}")
    string(REPLACE "add_library (${SZIP_LIB_TARGET} STATIC" "add_library (${SZIP_LIB_TARGET} SHARED" libaec_content "${libaec_content}")
    file(WRITE "${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "${libaec_content}")

    # Correct H5_SET_LIB_OPTIONS call for internal deps if needed
    # Actually, setting the libtype to SHARED in the replace above should handle it if the macro uses it.
"""

old_patch_call = r'# Patch HDF5\'s internal ZLIB and LIBAEC to build as shared\s+message\(STATUS "Patching internal HDF5 ZLIB and LIBAEC for shared build..."\)\s+configure_file\("\${CMAKE_CURRENT_SOURCE_DIR}/patch_hdf5_deps\.cmake" "\${CMAKE_CURRENT_BINARY_DIR}/patch_hdf5_deps\.cmake" COPYONLY\)\s+include\("\${CMAKE_CURRENT_BINARY_DIR}/patch_hdf5_deps\.cmake"\)'

content = re.sub(old_patch_call, patch_logic, content)

with open('CMakeLists.txt', 'w') as f:
    f.write(content)
