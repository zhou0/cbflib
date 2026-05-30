macro (H5_SET_LIB_OPTIONS libtarget libname libtype)
  message(STATUS "libtarget: ${libtarget}, libname: ${libname}, libtype: ${libtype}")
  set_target_properties (${libtarget} PROPERTIES
      PREFIX ""
      IMPORT_PREFIX ""
      ${ARGN}
  )
endmacro ()
