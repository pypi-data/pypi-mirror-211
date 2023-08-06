#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "VTK::U3DExporter" for configuration "Release"
set_property(TARGET VTK::U3DExporter APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(VTK::U3DExporter PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/vtkU3DExporter.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "VTK::CommonCore;VTK::CommonDataModel;VTK::CommonTransforms;VTK::FiltersCore;VTK::FiltersGeometry;VTK::RenderingCore;VTK::RenderingOpenGL2"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/vtkmodules/vtkU3DExporter.dll"
  )

list(APPEND _cmake_import_check_targets VTK::U3DExporter )
list(APPEND _cmake_import_check_files_for_VTK::U3DExporter "${_IMPORT_PREFIX}/lib/vtkU3DExporter.lib" "${_IMPORT_PREFIX}/lib/vtkmodules/vtkU3DExporter.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
