#include "pxr/base/vt/array.h"
#include "pxr/base/vt/value.h"
#include "pxr/usd/usd/primRange.h"
#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/points.h"
#include "pxr/base/gf/vec3f.h"

#include <iostream>
#include <string>

int main(int argc, char *argv[]) {
  if (argc != 3) {
    std::cerr << "USAGE: " << argv[0] << " <in.abc> <out.usd>" << std::endl;
    return 1;
  }

  std::string in_filename{argv[1]};
  std::string out_filename{argv[2]};

  auto in_stage = pxr::UsdStage::Open(in_filename);
  if (!in_stage) {
    std::cerr << "ERROR: Could not open file: " << in_filename << std::endl;
    return 2;
  }
  std::cout << "Loaded stage from file: " << in_filename << std::endl;

  auto out_layer = pxr::SdfLayer::CreateNew(out_filename);
  if (!out_layer) {
    std::cerr << "ERROR: Could not create new layer for: " << out_filename
              << std::endl;
    return 2;
  }

  auto out_stage = pxr::UsdStage::Open(out_layer);
  if (!out_stage) {
    std::cerr << "ERROR: Could not create new stage for: " << out_filename
              << std::endl;
    return 2;
  }

  for (auto const &in_prim : in_stage->TraverseAll()) {
    std::cout << in_prim.GetPath().GetText() << std::endl;
    if (in_prim.IsA<pxr::UsdGeomPoints>()) {
      std::cout << "\t... which is a geom points!" << std::endl;
      pxr::UsdGeomPoints const in_points{in_prim};

      auto out_points =
          UsdGeomPoints::Define(stage, SdfPath("/" + "pointcloud"));

      auto const in_points_attr = in_points.GetPointsAttr();
      pxr::VtArray<pxr::GfVec3f> points_data;
      in_points.Get(&points_data, 0);

      auto const out_points_attr = out_points.CreatePointsAttr();
      out_points.Set(points_data, 0);

      break;
    } else {
      std::cout << "\t... which is NOT a points!" << std::endl;
    }
  }

  std::cout << "Traversed prims from file: " << in_filename << std::endl;

  out_stage->Save();
  std::cout << "Saved file: " << out_filename << std::endl;

  return 0;
}
