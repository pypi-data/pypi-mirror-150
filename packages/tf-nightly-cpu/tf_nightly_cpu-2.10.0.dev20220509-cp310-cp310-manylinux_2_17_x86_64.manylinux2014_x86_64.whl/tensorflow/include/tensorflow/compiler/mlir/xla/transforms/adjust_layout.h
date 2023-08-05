/* Copyright 2021 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_COMPILER_MLIR_XLA_TRANSFORMS_ADJUST_LAYOUT_H_
#define TENSORFLOW_COMPILER_MLIR_XLA_TRANSFORMS_ADJUST_LAYOUT_H_

#include <memory>

#include "mlir/IR/Builders.h"  // from @llvm-project
#include "mlir/Pass/Pass.h"  // from @llvm-project

namespace mlir {
namespace mhlo {

// Fill in layouts in module using the TPU executor API.
std::unique_ptr<Pass> CreateAdjustLayoutPass();

// Register the pass for command line testing.
void RegisterAdjustLayoutPass();

// Try to determine the right TPU infeed layout.
FailureOr<Attribute> GetTPUInfeedLayout(const ArrayRef<Type> types,
                                        OpBuilder &rewriter);

}  // namespace mhlo
}  // namespace mlir

#endif  // TENSORFLOW_COMPILER_MLIR_XLA_TRANSFORMS_ADJUST_LAYOUT_H_
