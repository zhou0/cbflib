macro(patch_file FILE_PATH SEARCH REPLACE)
  if(EXISTS "${FILE_PATH}")
    file(READ "${FILE_PATH}" content)
    string(REPLACE "${SEARCH}" "${REPLACE}" content "${content}")
    file(WRITE "${FILE_PATH}" "${content}")
  endif()
endmacro()

# ZLIB patching
patch_file("${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" "add_library(${ZLIB_LIB_TARGET} STATIC" "add_library(${ZLIB_LIB_TARGET} SHARED")
# Correct H5_SET_LIB_OPTIONS call for ZLIB (it needs 4 arguments)
patch_file("${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" "H5_SET_LIB_OPTIONS (${ZLIB_LIB_TARGET} \${ZLIB_LIB_NAME} STATIC 0)" "H5_SET_LIB_OPTIONS (${ZLIB_LIB_TARGET} \${ZLIB_LIB_NAME} SHARED ZLIB)")

# LIBAEC patching
patch_file("${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "add_library (\${LIBAEC_LIB_TARGET} STATIC" "add_library (\${LIBAEC_LIB_TARGET} SHARED")
patch_file("${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "add_library (\${SZIP_LIB_TARGET} STATIC" "add_library (\${SZIP_LIB_TARGET} SHARED")
# Correct H5_SET_LIB_OPTIONS calls for LIBAEC/SZIP
patch_file("${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "H5_SET_LIB_OPTIONS (\${LIBAEC_LIB_TARGET} \${LIBAEC_LIB_NAME} STATIC 0)" "H5_SET_LIB_OPTIONS (\${LIBAEC_LIB_TARGET} \${LIBAEC_LIB_NAME} SHARED SZIP)")
patch_file("${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "H5_SET_LIB_OPTIONS (\${SZIP_LIB_TARGET} \${SZIP_LIB_NAME} STATIC 0)" "H5_SET_LIB_OPTIONS (\${SZIP_LIB_TARGET} \${SZIP_LIB_NAME} SHARED SZIP)")
