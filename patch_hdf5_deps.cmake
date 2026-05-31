macro(patch_file FILE_PATH SEARCH REPLACE)
  if(EXISTS "${FILE_PATH}")
    file(READ "${FILE_PATH}" content)
    string(REPLACE "${SEARCH}" "${REPLACE}" content "${content}")
    file(WRITE "${FILE_PATH}" "${content}")
  endif()
endmacro()

# ZLIB patching
patch_file("${hdf5_SOURCE_DIR}/config/cmake/ZLIB/CMakeLists.txt" "add_library(${ZLIB_LIB_TARGET} STATIC" "add_library(${ZLIB_LIB_TARGET} SHARED")

# LIBAEC patching
patch_file("${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "add_library (${LIBAEC_LIB_TARGET} STATIC" "add_library (${LIBAEC_LIB_TARGET} SHARED")
patch_file("${hdf5_SOURCE_DIR}/config/cmake/LIBAEC/CMakeLists.txt" "add_library (${SZIP_LIB_TARGET} STATIC" "add_library (${SZIP_LIB_TARGET} SHARED")

# Macro fix for SHARED
patch_file("${hdf5_SOURCE_DIR}/config/cmake/HDF5Macros.cmake"
           "macro (H5_SET_LIB_OPTIONS libtarget libname libtype libpackage)"
           "macro (H5_SET_LIB_OPTIONS libtarget libname libtype)\n  set(libpackage \"\${ARGN}\")\n  if(\"\${libpackage}\" STREQUAL \"\")\n    set(libpackage \"HDF5\")\n  endif()")

# Ensure HDF5 links correctly to its internal shared SZIP/ZLIB
patch_file("${hdf5_SOURCE_DIR}/CMakeFilters.cmake"
           "set (H5_SZIP_LIBRARIES \${H5_SZIP_STATIC_LIBRARY})"
           "set (H5_SZIP_LIBRARIES \${H5_SZIP_SHARED_LIBRARY})")
patch_file("${hdf5_SOURCE_DIR}/CMakeFilters.cmake"
           "set (H5_ZLIB_LIBRARIES \${H5_ZLIB_STATIC_LIBRARY})"
           "set (H5_ZLIB_LIBRARIES \${H5_ZLIB_SHARED_LIBRARY})")
