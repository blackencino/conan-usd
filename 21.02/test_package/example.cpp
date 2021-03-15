#include "pxr/base/vt/array.h"
#include "pxr/base/vt/value.h"
#include "pxr/usd/usd/primRange.h"
#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/mesh.h"

#include <iostream>
#include <string>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    std::cerr << "USAGE: " << argv[0] << " <USDArchive.usd>" << std::endl;
    return 1;
  }

  std::string filename{argv[1]};

  auto stage = pxr::UsdStage::Open(filename);
  if (!stage) {
    std::cerr << "ERROR: Could not open file: " << filename << std::endl;
    return 2;
  }
  std::cout << "Loaded stage from file: " << filename << std::endl;
  if (stage) {
    for (auto const &prim : stage->TraverseAll()) {
      std::cout << prim.GetPath().GetText() << std::endl;
      if (prim.IsA<pxr::UsdGeomMesh>()) {
        std::cout << "\t... which is a mesh!" << std::endl;
        pxr::UsdGeomMesh const mesh{prim};
        for (auto const &attr : prim.GetAttributes()) {
          std::cout << "\t... attr: " << attr.GetTypeName() << ", "
                    << attr.GetBaseName() << std::endl;
        }
        auto const face_vertex_indices_attr = mesh.GetFaceVertexIndicesAttr();
        std::cout << "\t number of time samples for face vertices: "
                  << face_vertex_indices_attr.GetNumTimeSamples() << std::endl
                  << "\t does it have a value? "
                  << face_vertex_indices_attr.HasValue() << std::endl;
        pxr::VtArray<int> face_vertices;
        if (!face_vertex_indices_attr.Get(&face_vertices, 0)) {
          std::cerr << "\tCouldn't get face vertices attr value" << std::endl;
          return -1;
        } else {
          std::cout << "\t face vertex indices count: " << face_vertices.size()
                    << std::endl;
        }

      } else {
        std::cout << "\t... which is NOT a mesh!" << std::endl;
      }
    }
  }
  std::cout << "Traversed prims from file: " << filename << std::endl;

  return 0;
}
