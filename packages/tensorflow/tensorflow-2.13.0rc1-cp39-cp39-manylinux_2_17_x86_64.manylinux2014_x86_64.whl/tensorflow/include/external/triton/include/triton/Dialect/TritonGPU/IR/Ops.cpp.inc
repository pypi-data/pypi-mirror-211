/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::triton::gpu::AllocTensorOp,
::mlir::triton::gpu::AsyncCommitGroupOp,
::mlir::triton::gpu::AsyncWaitOp,
::mlir::triton::gpu::CmpFOp,
::mlir::triton::gpu::CmpIOp,
::mlir::triton::gpu::ConvertLayoutOp,
::mlir::triton::gpu::ExtractSliceOp,
::mlir::triton::gpu::InsertSliceAsyncOp,
::mlir::triton::gpu::SelectOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace triton {
namespace gpu {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isFloat8E4M3FN())) || ((elementType.isFloat8E5M2())) || ((elementType.isF16())) || ((elementType.isBF16())) || ((elementType.isF32())) || ((elementType.isF64())); }(type.cast<::mlir::ShapedType>().getElementType()))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isSignlessInteger(1))) || ((elementType.isSignlessInteger(8))) || ((elementType.isSignlessInteger(16))) || ((elementType.isSignlessInteger(32))) || ((elementType.isSignlessInteger(64))); }(type.cast<::mlir::ShapedType>().getElementType())))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isa<::mlir::triton::PointerType>())) && ([](::mlir::Type pointeeType) { return (true); }(elementType.cast<::mlir::triton::PointerType>().getPointeeType())); }(type.cast<::mlir::ShapedType>().getElementType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be tensor of floating-point values or tensor of integer values or tensor of ptr values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps1(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((type.isFloat8E4M3FN())) || ((type.isFloat8E5M2())) || ((type.isF16())) || ((type.isBF16())) || ((type.isF32())) || ((type.isF64()))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isFloat8E4M3FN())) || ((elementType.isFloat8E5M2())) || ((elementType.isF16())) || ((elementType.isBF16())) || ((elementType.isF32())) || ((elementType.isF64())); }(type.cast<::mlir::ShapedType>().getElementType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be floating-point or tensor of floating-point values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps2(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isSignlessInteger(1))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return (elementType.isSignlessInteger(1)); }(type.cast<::mlir::ShapedType>().getElementType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be 1-bit signless integer or tensor of 1-bit signless integer values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps3(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((type.isSignlessInteger(1))) || ((type.isSignlessInteger(8))) || ((type.isSignlessInteger(16))) || ((type.isSignlessInteger(32))) || ((type.isSignlessInteger(64)))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isSignlessInteger(1))) || ((elementType.isSignlessInteger(8))) || ((elementType.isSignlessInteger(16))) || ((elementType.isSignlessInteger(32))) || ((elementType.isSignlessInteger(64))); }(type.cast<::mlir::ShapedType>().getElementType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be integer or tensor of integer values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps4(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isa<::mlir::RankedTensorType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be ranked tensor of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps5(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isSignlessInteger(32)))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be 32-bit signless integer, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps6(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isa<::mlir::triton::PointerType>())) && ([](::mlir::Type pointeeType) { return (true); }(elementType.cast<::mlir::triton::PointerType>().getPointeeType())); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be tensor of ptr values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps7(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return (elementType.isSignlessInteger(1)); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be tensor of 1-bit signless integer values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_TritonGPUOps8(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((((type.isFloat8E4M3FN())) || ((type.isFloat8E5M2())) || ((type.isF16())) || ((type.isBF16())) || ((type.isF32())) || ((type.isF64()))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isFloat8E4M3FN())) || ((elementType.isFloat8E5M2())) || ((elementType.isF16())) || ((elementType.isBF16())) || ((elementType.isF32())) || ((elementType.isF64())); }(type.cast<::mlir::ShapedType>().getElementType())))) || ((((type.isSignlessInteger(1))) || ((type.isSignlessInteger(8))) || ((type.isSignlessInteger(16))) || ((type.isSignlessInteger(32))) || ((type.isSignlessInteger(64)))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isSignlessInteger(1))) || ((elementType.isSignlessInteger(8))) || ((elementType.isSignlessInteger(16))) || ((elementType.isSignlessInteger(32))) || ((elementType.isSignlessInteger(64))); }(type.cast<::mlir::ShapedType>().getElementType())))) || ((((type.isa<::mlir::triton::PointerType>())) && ([](::mlir::Type pointeeType) { return (true); }(type.cast<::mlir::triton::PointerType>().getPointeeType()))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isa<::mlir::triton::PointerType>())) && ([](::mlir::Type pointeeType) { return (true); }(elementType.cast<::mlir::triton::PointerType>().getPointeeType())); }(type.cast<::mlir::ShapedType>().getElementType())))) || (((type.isa<::mlir::triton::PointerType>())) && ([](::mlir::Type pointeeType) { return ((((pointeeType.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isFloat8E4M3FN())) || ((elementType.isFloat8E5M2())) || ((elementType.isF16())) || ((elementType.isBF16())) || ((elementType.isF32())) || ((elementType.isF64())); }(pointeeType.cast<::mlir::ShapedType>().getElementType()))) || (((pointeeType.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isSignlessInteger(1))) || ((elementType.isSignlessInteger(8))) || ((elementType.isSignlessInteger(16))) || ((elementType.isSignlessInteger(32))) || ((elementType.isSignlessInteger(64))); }(pointeeType.cast<::mlir::ShapedType>().getElementType())))) || (((pointeeType.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isa<::mlir::triton::PointerType>())) && ([](::mlir::Type pointeeType) { return (true); }(elementType.cast<::mlir::triton::PointerType>().getPointeeType())); }(pointeeType.cast<::mlir::ShapedType>().getElementType()))); }(type.cast<::mlir::triton::PointerType>().getPointeeType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be floating-point or tensor of floating-point values or integer or tensor of integer values or ptr or tensor of ptr values or ptr, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 32-bit signless integer attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::arith::CmpFPredicateAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: allowed 64-bit signless integer cases: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps2(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::arith::CmpIPredicateAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: allowed 64-bit signless integer cases: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps3(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::DenseI64ArrayAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: i64 dense array attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps4(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::triton::CacheModifierAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: allowed 32-bit signless integer cases: 1, 2, 3";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps5(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::triton::EvictionPolicyAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: allowed 32-bit signless integer cases: 1, 2, 3";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_TritonGPUOps6(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::BoolAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: bool attribute";
  }
  return ::mlir::success();
}
} // namespace gpu
} // namespace triton
} // namespace mlir
namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::AllocTensorOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
AllocTensorOpGenericAdaptorBase::AllocTensorOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.alloc_tensor", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> AllocTensorOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr AllocTensorOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
AllocTensorOpAdaptor::AllocTensorOpAdaptor(AllocTensorOp op) : AllocTensorOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult AllocTensorOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> AllocTensorOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range AllocTensorOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> AllocTensorOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range AllocTensorOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value AllocTensorOp::getResult() {
  return ::llvm::cast<::mlir::Value>(*getODSResults(0).begin());
}

void AllocTensorOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result) {
  odsState.addTypes(result);
}

void AllocTensorOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes) {
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllocTensorOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult AllocTensorOp::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult AllocTensorOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult AllocTensorOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  return ::mlir::success();
}

void AllocTensorOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void AllocTensorOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  effects.emplace_back(::mlir::MemoryEffects::Allocate::get(), ::mlir::SideEffects::DefaultResource::get());
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::AllocTensorOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::AsyncCommitGroupOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
AsyncCommitGroupOpGenericAdaptorBase::AsyncCommitGroupOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.async_commit_group", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> AsyncCommitGroupOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr AsyncCommitGroupOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
AsyncCommitGroupOpAdaptor::AsyncCommitGroupOpAdaptor(AsyncCommitGroupOp op) : AsyncCommitGroupOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult AsyncCommitGroupOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> AsyncCommitGroupOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range AsyncCommitGroupOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> AsyncCommitGroupOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range AsyncCommitGroupOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void AsyncCommitGroupOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState) {
}

void AsyncCommitGroupOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes) {
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AsyncCommitGroupOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult AsyncCommitGroupOp::verifyInvariantsImpl() {
  return ::mlir::success();
}

::mlir::LogicalResult AsyncCommitGroupOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult AsyncCommitGroupOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  return ::mlir::success();
}

void AsyncCommitGroupOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::AsyncCommitGroupOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::AsyncWaitOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
AsyncWaitOpGenericAdaptorBase::AsyncWaitOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.async_wait", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> AsyncWaitOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr AsyncWaitOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::IntegerAttr AsyncWaitOpGenericAdaptorBase::getNumAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 0, AsyncWaitOp::getNumAttrName(*odsOpName)).cast<::mlir::IntegerAttr>();
  return attr;
}

uint32_t AsyncWaitOpGenericAdaptorBase::getNum() {
  auto attr = getNumAttr();
  return attr.getValue().getZExtValue();
}

} // namespace detail
AsyncWaitOpAdaptor::AsyncWaitOpAdaptor(AsyncWaitOp op) : AsyncWaitOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult AsyncWaitOpAdaptor::verify(::mlir::Location loc) {
  auto namedAttrRange = odsAttrs;
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_num;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.async_wait' op ""requires attribute 'num'");
    if (namedAttrIt->getName() == AsyncWaitOp::getNumAttrName(*odsOpName)) {
      tblgen_num = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  if (tblgen_num && !(((tblgen_num.isa<::mlir::IntegerAttr>())) && ((tblgen_num.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))))
    return emitError(loc, "'triton_gpu.async_wait' op ""attribute 'num' failed to satisfy constraint: 32-bit signless integer attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> AsyncWaitOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range AsyncWaitOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> AsyncWaitOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range AsyncWaitOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::IntegerAttr AsyncWaitOp::getNumAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 0, getNumAttrName()).cast<::mlir::IntegerAttr>();
}

uint32_t AsyncWaitOp::getNum() {
  auto attr = getNumAttr();
  return attr.getValue().getZExtValue();
}

void AsyncWaitOp::setNumAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getNumAttrName(), attr);
}

void AsyncWaitOp::setNum(uint32_t attrValue) {
  (*this)->setAttr(getNumAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIntegerType(32), attrValue));
}

void AsyncWaitOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::IntegerAttr num) {
  odsState.addAttribute(getNumAttrName(odsState.name), num);
}

void AsyncWaitOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::IntegerAttr num) {
  odsState.addAttribute(getNumAttrName(odsState.name), num);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AsyncWaitOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, uint32_t num) {
  odsState.addAttribute(getNumAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), num));
}

void AsyncWaitOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, uint32_t num) {
  odsState.addAttribute(getNumAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), num));
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AsyncWaitOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult AsyncWaitOp::verifyInvariantsImpl() {
  auto namedAttrRange = (*this)->getAttrs();
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_num;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'num'");
    if (namedAttrIt->getName() == getNumAttrName()) {
      tblgen_num = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps0(*this, tblgen_num, "num")))
    return ::mlir::failure();
  return ::mlir::success();
}

::mlir::LogicalResult AsyncWaitOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult AsyncWaitOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  return ::mlir::success();
}

void AsyncWaitOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::AsyncWaitOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::CmpFOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
CmpFOpGenericAdaptorBase::CmpFOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.cmpf", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> CmpFOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr CmpFOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::arith::CmpFPredicateAttr CmpFOpGenericAdaptorBase::getPredicateAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 0, CmpFOp::getPredicateAttrName(*odsOpName)).cast<::mlir::arith::CmpFPredicateAttr>();
  return attr;
}

::mlir::arith::CmpFPredicate CmpFOpGenericAdaptorBase::getPredicate() {
  auto attr = getPredicateAttr();
  return attr.getValue();
}

} // namespace detail
CmpFOpAdaptor::CmpFOpAdaptor(CmpFOp op) : CmpFOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult CmpFOpAdaptor::verify(::mlir::Location loc) {
  auto namedAttrRange = odsAttrs;
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_predicate;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.cmpf' op ""requires attribute 'predicate'");
    if (namedAttrIt->getName() == CmpFOp::getPredicateAttrName(*odsOpName)) {
      tblgen_predicate = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  if (tblgen_predicate && !((tblgen_predicate.isa<::mlir::arith::CmpFPredicateAttr>())))
    return emitError(loc, "'triton_gpu.cmpf' op ""attribute 'predicate' failed to satisfy constraint: allowed 64-bit signless integer cases: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> CmpFOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range CmpFOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value CmpFOp::getLhs() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(0).begin());
}

::mlir::Value CmpFOp::getRhs() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(1).begin());
}

::mlir::MutableOperandRange CmpFOp::getLhsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange CmpFOp::getRhsMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> CmpFOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range CmpFOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value CmpFOp::getResult() {
  return ::llvm::cast<::mlir::Value>(*getODSResults(0).begin());
}

::mlir::arith::CmpFPredicateAttr CmpFOp::getPredicateAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 0, getPredicateAttrName()).cast<::mlir::arith::CmpFPredicateAttr>();
}

::mlir::arith::CmpFPredicate CmpFOp::getPredicate() {
  auto attr = getPredicateAttr();
  return attr.getValue();
}

void CmpFOp::setPredicateAttr(::mlir::arith::CmpFPredicateAttr attr) {
  (*this)->setAttr(getPredicateAttrName(), attr);
}

void CmpFOp::setPredicate(::mlir::arith::CmpFPredicate attrValue) {
  (*this)->setAttr(getPredicateAttrName(), ::mlir::arith::CmpFPredicateAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void CmpFOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::arith::CmpFPredicateAttr predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), predicate);
  odsState.addTypes(result);
}

void CmpFOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::arith::CmpFPredicateAttr predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), predicate);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void CmpFOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::arith::CmpFPredicate predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), ::mlir::arith::CmpFPredicateAttr::get(odsBuilder.getContext(), predicate));
  odsState.addTypes(result);
}

void CmpFOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::arith::CmpFPredicate predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), ::mlir::arith::CmpFPredicateAttr::get(odsBuilder.getContext(), predicate));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void CmpFOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 2u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult CmpFOp::verifyInvariantsImpl() {
  auto namedAttrRange = (*this)->getAttrs();
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_predicate;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'predicate'");
    if (namedAttrIt->getName() == getPredicateAttrName()) {
      tblgen_predicate = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps1(*this, tblgen_predicate, "predicate")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps2(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult CmpFOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

void CmpFOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::CmpFOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::CmpIOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
CmpIOpGenericAdaptorBase::CmpIOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.cmpi", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> CmpIOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr CmpIOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::arith::CmpIPredicateAttr CmpIOpGenericAdaptorBase::getPredicateAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 0, CmpIOp::getPredicateAttrName(*odsOpName)).cast<::mlir::arith::CmpIPredicateAttr>();
  return attr;
}

::mlir::arith::CmpIPredicate CmpIOpGenericAdaptorBase::getPredicate() {
  auto attr = getPredicateAttr();
  return attr.getValue();
}

} // namespace detail
CmpIOpAdaptor::CmpIOpAdaptor(CmpIOp op) : CmpIOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult CmpIOpAdaptor::verify(::mlir::Location loc) {
  auto namedAttrRange = odsAttrs;
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_predicate;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.cmpi' op ""requires attribute 'predicate'");
    if (namedAttrIt->getName() == CmpIOp::getPredicateAttrName(*odsOpName)) {
      tblgen_predicate = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  if (tblgen_predicate && !((tblgen_predicate.isa<::mlir::arith::CmpIPredicateAttr>())))
    return emitError(loc, "'triton_gpu.cmpi' op ""attribute 'predicate' failed to satisfy constraint: allowed 64-bit signless integer cases: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> CmpIOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range CmpIOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value CmpIOp::getLhs() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(0).begin());
}

::mlir::Value CmpIOp::getRhs() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(1).begin());
}

::mlir::MutableOperandRange CmpIOp::getLhsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange CmpIOp::getRhsMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> CmpIOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range CmpIOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value CmpIOp::getResult() {
  return ::llvm::cast<::mlir::Value>(*getODSResults(0).begin());
}

::mlir::arith::CmpIPredicateAttr CmpIOp::getPredicateAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 0, getPredicateAttrName()).cast<::mlir::arith::CmpIPredicateAttr>();
}

::mlir::arith::CmpIPredicate CmpIOp::getPredicate() {
  auto attr = getPredicateAttr();
  return attr.getValue();
}

void CmpIOp::setPredicateAttr(::mlir::arith::CmpIPredicateAttr attr) {
  (*this)->setAttr(getPredicateAttrName(), attr);
}

void CmpIOp::setPredicate(::mlir::arith::CmpIPredicate attrValue) {
  (*this)->setAttr(getPredicateAttrName(), ::mlir::arith::CmpIPredicateAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void CmpIOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::arith::CmpIPredicateAttr predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), predicate);
  odsState.addTypes(result);
}

void CmpIOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::arith::CmpIPredicateAttr predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), predicate);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void CmpIOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::arith::CmpIPredicate predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), ::mlir::arith::CmpIPredicateAttr::get(odsBuilder.getContext(), predicate));
  odsState.addTypes(result);
}

void CmpIOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::arith::CmpIPredicate predicate, ::mlir::Value lhs, ::mlir::Value rhs) {
  odsState.addOperands(lhs);
  odsState.addOperands(rhs);
  odsState.addAttribute(getPredicateAttrName(odsState.name), ::mlir::arith::CmpIPredicateAttr::get(odsBuilder.getContext(), predicate));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void CmpIOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 2u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult CmpIOp::verifyInvariantsImpl() {
  auto namedAttrRange = (*this)->getAttrs();
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_predicate;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'predicate'");
    if (namedAttrIt->getName() == getPredicateAttrName()) {
      tblgen_predicate = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps2(*this, tblgen_predicate, "predicate")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps2(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult CmpIOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

void CmpIOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::CmpIOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::ConvertLayoutOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
ConvertLayoutOpGenericAdaptorBase::ConvertLayoutOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.convert_layout", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> ConvertLayoutOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr ConvertLayoutOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
ConvertLayoutOpAdaptor::ConvertLayoutOpAdaptor(ConvertLayoutOp op) : ConvertLayoutOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult ConvertLayoutOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ConvertLayoutOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ConvertLayoutOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value ConvertLayoutOp::getSrc() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(0).begin());
}

::mlir::MutableOperandRange ConvertLayoutOp::getSrcMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> ConvertLayoutOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ConvertLayoutOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value ConvertLayoutOp::getResult() {
  return ::llvm::cast<::mlir::Value>(*getODSResults(0).begin());
}

void ConvertLayoutOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src) {
  odsState.addOperands(src);
  odsState.addTypes(result);
}

void ConvertLayoutOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src) {
  odsState.addOperands(src);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ConvertLayoutOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ConvertLayoutOp::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult ConvertLayoutOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

void ConvertLayoutOp::getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context) {
  results.add(canonicalize);
}

::mlir::ParseResult ConvertLayoutOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand srcRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> srcOperands(srcRawOperands);  ::llvm::SMLoc srcOperandsLoc;
  (void)srcOperandsLoc;
  ::llvm::ArrayRef<::mlir::Type> allOperandTypes;
  ::llvm::ArrayRef<::mlir::Type> allResultTypes;

  srcOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(srcRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  ::mlir::FunctionType allOperand__allResult_functionType;
  if (parser.parseType(allOperand__allResult_functionType))
    return ::mlir::failure();
  allOperandTypes = allOperand__allResult_functionType.getInputs();
  allResultTypes = allOperand__allResult_functionType.getResults();
  result.addTypes(allResultTypes);
  if (parser.resolveOperands(srcOperands, allOperandTypes, parser.getNameLoc(), result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void ConvertLayoutOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getSrc();
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  _odsPrinter.printFunctionalType(getOperation()->getOperandTypes(), getOperation()->getResultTypes());
}

void ConvertLayoutOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::ConvertLayoutOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::ExtractSliceOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
ExtractSliceOpGenericAdaptorBase::ExtractSliceOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.extract_slice", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> ExtractSliceOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  assert(odsAttrs && "missing segment size attribute for op");
  auto sizeAttr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 3, ExtractSliceOp::getOperandSegmentSizesAttrName(*odsOpName)).cast<::mlir::DenseI32ArrayAttr>();

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttr[i];
  return {start, sizeAttr[index]};
}

::mlir::DictionaryAttr ExtractSliceOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::DenseI64ArrayAttr ExtractSliceOpGenericAdaptorBase::getStaticOffsetsAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 1, odsAttrs.end() - 2, ExtractSliceOp::getStaticOffsetsAttrName(*odsOpName)).cast<::mlir::DenseI64ArrayAttr>();
  return attr;
}

::llvm::ArrayRef<int64_t> ExtractSliceOpGenericAdaptorBase::getStaticOffsets() {
  auto attr = getStaticOffsetsAttr();
  return attr;
}

::mlir::DenseI64ArrayAttr ExtractSliceOpGenericAdaptorBase::getStaticSizesAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 2, odsAttrs.end() - 1, ExtractSliceOp::getStaticSizesAttrName(*odsOpName)).cast<::mlir::DenseI64ArrayAttr>();
  return attr;
}

::llvm::ArrayRef<int64_t> ExtractSliceOpGenericAdaptorBase::getStaticSizes() {
  auto attr = getStaticSizesAttr();
  return attr;
}

::mlir::DenseI64ArrayAttr ExtractSliceOpGenericAdaptorBase::getStaticStridesAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 3, odsAttrs.end() - 0, ExtractSliceOp::getStaticStridesAttrName(*odsOpName)).cast<::mlir::DenseI64ArrayAttr>();
  return attr;
}

::llvm::ArrayRef<int64_t> ExtractSliceOpGenericAdaptorBase::getStaticStrides() {
  auto attr = getStaticStridesAttr();
  return attr;
}

} // namespace detail
ExtractSliceOpAdaptor::ExtractSliceOpAdaptor(ExtractSliceOp op) : ExtractSliceOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult ExtractSliceOpAdaptor::verify(::mlir::Location loc) {
  auto namedAttrRange = odsAttrs;
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_operand_segment_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.extract_slice' op ""requires attribute 'operand_segment_sizes'");
    if (namedAttrIt->getName() == ExtractSliceOp::getOperandSegmentSizesAttrName(*odsOpName)) {
      tblgen_operand_segment_sizes = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_static_offsets;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.extract_slice' op ""requires attribute 'static_offsets'");
    if (namedAttrIt->getName() == ExtractSliceOp::getStaticOffsetsAttrName(*odsOpName)) {
      tblgen_static_offsets = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_static_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.extract_slice' op ""requires attribute 'static_sizes'");
    if (namedAttrIt->getName() == ExtractSliceOp::getStaticSizesAttrName(*odsOpName)) {
      tblgen_static_sizes = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_static_strides;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.extract_slice' op ""requires attribute 'static_strides'");
    if (namedAttrIt->getName() == ExtractSliceOp::getStaticStridesAttrName(*odsOpName)) {
      tblgen_static_strides = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  {
    auto sizeAttr = tblgen_operand_segment_sizes.cast<::mlir::DenseI32ArrayAttr>();
    auto numElements = sizeAttr.asArrayRef().size();
    if (numElements != 4)
      return emitError(loc, "'triton_gpu.extract_slice' op ""'operand_segment_sizes' attribute for specifying operand segments must have 4 "
                "elements, but got ") << numElements;
  }

  if (tblgen_static_offsets && !((tblgen_static_offsets.isa<::mlir::DenseI64ArrayAttr>())))
    return emitError(loc, "'triton_gpu.extract_slice' op ""attribute 'static_offsets' failed to satisfy constraint: i64 dense array attribute");

  if (tblgen_static_sizes && !((tblgen_static_sizes.isa<::mlir::DenseI64ArrayAttr>())))
    return emitError(loc, "'triton_gpu.extract_slice' op ""attribute 'static_sizes' failed to satisfy constraint: i64 dense array attribute");

  if (tblgen_static_strides && !((tblgen_static_strides.isa<::mlir::DenseI64ArrayAttr>())))
    return emitError(loc, "'triton_gpu.extract_slice' op ""attribute 'static_strides' failed to satisfy constraint: i64 dense array attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ExtractSliceOp::getODSOperandIndexAndLength(unsigned index) {
  auto sizeAttr = ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 3, getOperandSegmentSizesAttrName()).cast<::mlir::DenseI32ArrayAttr>();

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttr[i];
  return {start, sizeAttr[index]};
}

::mlir::Operation::operand_range ExtractSliceOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> ExtractSliceOp::getSource() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSOperands(0).begin());
}

::mlir::Operation::operand_range ExtractSliceOp::getOffsets() {
  return getODSOperands(1);
}

::mlir::Operation::operand_range ExtractSliceOp::getSizes() {
  return getODSOperands(2);
}

::mlir::Operation::operand_range ExtractSliceOp::getStrides() {
  return getODSOperands(3);
}

::mlir::MutableOperandRange ExtractSliceOp::getSourceMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(0u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 3, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange ExtractSliceOp::getOffsetsMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(1u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 3, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange ExtractSliceOp::getSizesMutable() {
  auto range = getODSOperandIndexAndLength(2);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(2u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 3, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange ExtractSliceOp::getStridesMutable() {
  auto range = getODSOperandIndexAndLength(3);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(3u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 3, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

std::pair<unsigned, unsigned> ExtractSliceOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ExtractSliceOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> ExtractSliceOp::getResult() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSResults(0).begin());
}

::mlir::DenseI64ArrayAttr ExtractSliceOp::getStaticOffsetsAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 1, (*this)->getAttrs().end() - 2, getStaticOffsetsAttrName()).cast<::mlir::DenseI64ArrayAttr>();
}

::llvm::ArrayRef<int64_t> ExtractSliceOp::getStaticOffsets() {
  auto attr = getStaticOffsetsAttr();
  return attr;
}

::mlir::DenseI64ArrayAttr ExtractSliceOp::getStaticSizesAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 2, (*this)->getAttrs().end() - 1, getStaticSizesAttrName()).cast<::mlir::DenseI64ArrayAttr>();
}

::llvm::ArrayRef<int64_t> ExtractSliceOp::getStaticSizes() {
  auto attr = getStaticSizesAttr();
  return attr;
}

::mlir::DenseI64ArrayAttr ExtractSliceOp::getStaticStridesAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 3, (*this)->getAttrs().end() - 0, getStaticStridesAttrName()).cast<::mlir::DenseI64ArrayAttr>();
}

::llvm::ArrayRef<int64_t> ExtractSliceOp::getStaticStrides() {
  auto attr = getStaticStridesAttr();
  return attr;
}

void ExtractSliceOp::setStaticOffsetsAttr(::mlir::DenseI64ArrayAttr attr) {
  (*this)->setAttr(getStaticOffsetsAttrName(), attr);
}

void ExtractSliceOp::setStaticOffsets(::llvm::ArrayRef<int64_t> attrValue) {
  (*this)->setAttr(getStaticOffsetsAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI64ArrayAttr(attrValue));
}

void ExtractSliceOp::setStaticSizesAttr(::mlir::DenseI64ArrayAttr attr) {
  (*this)->setAttr(getStaticSizesAttrName(), attr);
}

void ExtractSliceOp::setStaticSizes(::llvm::ArrayRef<int64_t> attrValue) {
  (*this)->setAttr(getStaticSizesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI64ArrayAttr(attrValue));
}

void ExtractSliceOp::setStaticStridesAttr(::mlir::DenseI64ArrayAttr attr) {
  (*this)->setAttr(getStaticStridesAttrName(), attr);
}

void ExtractSliceOp::setStaticStrides(::llvm::ArrayRef<int64_t> attrValue) {
  (*this)->setAttr(getStaticStridesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI64ArrayAttr(attrValue));
}

void ExtractSliceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value source, ::mlir::ValueRange offsets, ::mlir::ValueRange sizes, ::mlir::ValueRange strides, ::mlir::DenseI64ArrayAttr static_offsets, ::mlir::DenseI64ArrayAttr static_sizes, ::mlir::DenseI64ArrayAttr static_strides) {
  odsState.addOperands(source);
  odsState.addOperands(offsets);
  odsState.addOperands(sizes);
  odsState.addOperands(strides);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, static_cast<int32_t>(offsets.size()), static_cast<int32_t>(sizes.size()), static_cast<int32_t>(strides.size())}));
  odsState.addAttribute(getStaticOffsetsAttrName(odsState.name), static_offsets);
  odsState.addAttribute(getStaticSizesAttrName(odsState.name), static_sizes);
  odsState.addAttribute(getStaticStridesAttrName(odsState.name), static_strides);
  odsState.addTypes(result);
}

void ExtractSliceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value source, ::mlir::ValueRange offsets, ::mlir::ValueRange sizes, ::mlir::ValueRange strides, ::mlir::DenseI64ArrayAttr static_offsets, ::mlir::DenseI64ArrayAttr static_sizes, ::mlir::DenseI64ArrayAttr static_strides) {
  odsState.addOperands(source);
  odsState.addOperands(offsets);
  odsState.addOperands(sizes);
  odsState.addOperands(strides);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, static_cast<int32_t>(offsets.size()), static_cast<int32_t>(sizes.size()), static_cast<int32_t>(strides.size())}));
  odsState.addAttribute(getStaticOffsetsAttrName(odsState.name), static_offsets);
  odsState.addAttribute(getStaticSizesAttrName(odsState.name), static_sizes);
  odsState.addAttribute(getStaticStridesAttrName(odsState.name), static_strides);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ExtractSliceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value source, ::mlir::ValueRange offsets, ::mlir::ValueRange sizes, ::mlir::ValueRange strides, ::llvm::ArrayRef<int64_t> static_offsets, ::llvm::ArrayRef<int64_t> static_sizes, ::llvm::ArrayRef<int64_t> static_strides) {
  odsState.addOperands(source);
  odsState.addOperands(offsets);
  odsState.addOperands(sizes);
  odsState.addOperands(strides);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, static_cast<int32_t>(offsets.size()), static_cast<int32_t>(sizes.size()), static_cast<int32_t>(strides.size())}));
  odsState.addAttribute(getStaticOffsetsAttrName(odsState.name), odsBuilder.getDenseI64ArrayAttr(static_offsets));
  odsState.addAttribute(getStaticSizesAttrName(odsState.name), odsBuilder.getDenseI64ArrayAttr(static_sizes));
  odsState.addAttribute(getStaticStridesAttrName(odsState.name), odsBuilder.getDenseI64ArrayAttr(static_strides));
  odsState.addTypes(result);
}

void ExtractSliceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value source, ::mlir::ValueRange offsets, ::mlir::ValueRange sizes, ::mlir::ValueRange strides, ::llvm::ArrayRef<int64_t> static_offsets, ::llvm::ArrayRef<int64_t> static_sizes, ::llvm::ArrayRef<int64_t> static_strides) {
  odsState.addOperands(source);
  odsState.addOperands(offsets);
  odsState.addOperands(sizes);
  odsState.addOperands(strides);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, static_cast<int32_t>(offsets.size()), static_cast<int32_t>(sizes.size()), static_cast<int32_t>(strides.size())}));
  odsState.addAttribute(getStaticOffsetsAttrName(odsState.name), odsBuilder.getDenseI64ArrayAttr(static_offsets));
  odsState.addAttribute(getStaticSizesAttrName(odsState.name), odsBuilder.getDenseI64ArrayAttr(static_sizes));
  odsState.addAttribute(getStaticStridesAttrName(odsState.name), odsBuilder.getDenseI64ArrayAttr(static_strides));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ExtractSliceOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() >= 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ExtractSliceOp::verifyInvariantsImpl() {
  auto namedAttrRange = (*this)->getAttrs();
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_operand_segment_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'operand_segment_sizes'");
    if (namedAttrIt->getName() == getOperandSegmentSizesAttrName()) {
      tblgen_operand_segment_sizes = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_static_offsets;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'static_offsets'");
    if (namedAttrIt->getName() == getStaticOffsetsAttrName()) {
      tblgen_static_offsets = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_static_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'static_sizes'");
    if (namedAttrIt->getName() == getStaticSizesAttrName()) {
      tblgen_static_sizes = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_static_strides;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'static_strides'");
    if (namedAttrIt->getName() == getStaticStridesAttrName()) {
      tblgen_static_strides = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  {
    auto sizeAttr = tblgen_operand_segment_sizes.cast<::mlir::DenseI32ArrayAttr>();
    auto numElements = sizeAttr.asArrayRef().size();
    if (numElements != 4)
      return emitOpError("'operand_segment_sizes' attribute for specifying operand segments must have 4 "
                "elements, but got ") << numElements;
  }

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps3(*this, tblgen_static_offsets, "static_offsets")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps3(*this, tblgen_static_sizes, "static_sizes")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps3(*this, tblgen_static_strides, "static_strides")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps5(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps5(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps5(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps4(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult ExtractSliceOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult ExtractSliceOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand sourceRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> sourceOperands(sourceRawOperands);  ::llvm::SMLoc sourceOperandsLoc;
  (void)sourceOperandsLoc;
  ::llvm::SmallVector<::mlir::OpAsmParser::UnresolvedOperand, 4> offsetsOperands;
  ::llvm::SMLoc offsetsOperandsLoc;
  (void)offsetsOperandsLoc;
  ::mlir::DenseI64ArrayAttr static_offsetsAttr;
  ::llvm::SmallVector<::mlir::OpAsmParser::UnresolvedOperand, 4> sizesOperands;
  ::llvm::SMLoc sizesOperandsLoc;
  (void)sizesOperandsLoc;
  ::mlir::DenseI64ArrayAttr static_sizesAttr;
  ::llvm::SmallVector<::mlir::OpAsmParser::UnresolvedOperand, 4> stridesOperands;
  ::llvm::SMLoc stridesOperandsLoc;
  (void)stridesOperandsLoc;
  ::mlir::DenseI64ArrayAttr static_stridesAttr;
  ::mlir::Type sourceRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> sourceTypes(sourceRawTypes);
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  sourceOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(sourceRawOperands[0]))
    return ::mlir::failure();
  {
    offsetsOperandsLoc = parser.getCurrentLocation();
    if (parseDynamicIndexList(parser, offsetsOperands, static_offsetsAttr))
      return ::mlir::failure();
    result.addAttribute("static_offsets", static_offsetsAttr);
  }
  {
    sizesOperandsLoc = parser.getCurrentLocation();
    if (parseDynamicIndexList(parser, sizesOperands, static_sizesAttr))
      return ::mlir::failure();
    result.addAttribute("static_sizes", static_sizesAttr);
  }
  {
    stridesOperandsLoc = parser.getCurrentLocation();
    if (parseDynamicIndexList(parser, stridesOperands, static_stridesAttr))
      return ::mlir::failure();
    result.addAttribute("static_strides", static_stridesAttr);
  }
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::RankedTensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    sourceRawTypes[0] = type;
  }
  if (parser.parseKeyword("to"))
    return ::mlir::failure();

  {
    ::mlir::RankedTensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addAttribute("operand_segment_sizes", parser.getBuilder().getDenseI32ArrayAttr({1, static_cast<int32_t>(offsetsOperands.size()), static_cast<int32_t>(sizesOperands.size()), static_cast<int32_t>(stridesOperands.size())}));
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getIntegerType(32);
  result.addTypes(resultTypes);
  if (parser.resolveOperands(sourceOperands, sourceTypes, sourceOperandsLoc, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(offsetsOperands, odsBuildableType0, offsetsOperandsLoc, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(sizesOperands, odsBuildableType0, sizesOperandsLoc, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(stridesOperands, odsBuildableType0, stridesOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void ExtractSliceOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getSource();
  printDynamicIndexList(_odsPrinter, *this, getOffsets(), getStaticOffsetsAttr());
  _odsPrinter << ' ';
  printDynamicIndexList(_odsPrinter, *this, getSizes(), getStaticSizesAttr());
  _odsPrinter << ' ';
  printDynamicIndexList(_odsPrinter, *this, getStrides(), getStaticStridesAttr());
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("operand_segment_sizes");
  elidedAttrs.push_back("static_offsets");
  elidedAttrs.push_back("static_sizes");
  elidedAttrs.push_back("static_strides");
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getSource().getType();
    if (auto validType = type.dyn_cast<::mlir::RankedTensorType>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
  _odsPrinter << ' ' << "to";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = type.dyn_cast<::mlir::RankedTensorType>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void ExtractSliceOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::ExtractSliceOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::InsertSliceAsyncOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
InsertSliceAsyncOpGenericAdaptorBase::InsertSliceAsyncOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.insert_slice_async", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> InsertSliceAsyncOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  assert(odsAttrs && "missing segment size attribute for op");
  auto sizeAttr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 4, odsAttrs.end() - 0, InsertSliceAsyncOp::getOperandSegmentSizesAttrName(*odsOpName)).cast<::mlir::DenseI32ArrayAttr>();

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttr[i];
  return {start, sizeAttr[index]};
}

::mlir::DictionaryAttr InsertSliceAsyncOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::triton::CacheModifierAttr InsertSliceAsyncOpGenericAdaptorBase::getCacheAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 1, odsAttrs.end() - 3, InsertSliceAsyncOp::getCacheAttrName(*odsOpName)).cast<::mlir::triton::CacheModifierAttr>();
  return attr;
}

::mlir::triton::CacheModifier InsertSliceAsyncOpGenericAdaptorBase::getCache() {
  auto attr = getCacheAttr();
  return attr.getValue();
}

::mlir::triton::EvictionPolicyAttr InsertSliceAsyncOpGenericAdaptorBase::getEvictAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 2, odsAttrs.end() - 2, InsertSliceAsyncOp::getEvictAttrName(*odsOpName)).cast<::mlir::triton::EvictionPolicyAttr>();
  return attr;
}

::mlir::triton::EvictionPolicy InsertSliceAsyncOpGenericAdaptorBase::getEvict() {
  auto attr = getEvictAttr();
  return attr.getValue();
}

::mlir::BoolAttr InsertSliceAsyncOpGenericAdaptorBase::getIsVolatileAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 3, odsAttrs.end() - 1, InsertSliceAsyncOp::getIsVolatileAttrName(*odsOpName)).cast<::mlir::BoolAttr>();
  return attr;
}

bool InsertSliceAsyncOpGenericAdaptorBase::getIsVolatile() {
  auto attr = getIsVolatileAttr();
  return attr.getValue();
}

::mlir::IntegerAttr InsertSliceAsyncOpGenericAdaptorBase::getAxisAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 4, InsertSliceAsyncOp::getAxisAttrName(*odsOpName)).cast<::mlir::IntegerAttr>();
  return attr;
}

uint32_t InsertSliceAsyncOpGenericAdaptorBase::getAxis() {
  auto attr = getAxisAttr();
  return attr.getValue().getZExtValue();
}

} // namespace detail
InsertSliceAsyncOpAdaptor::InsertSliceAsyncOpAdaptor(InsertSliceAsyncOp op) : InsertSliceAsyncOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult InsertSliceAsyncOpAdaptor::verify(::mlir::Location loc) {
  auto namedAttrRange = odsAttrs;
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_axis;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.insert_slice_async' op ""requires attribute 'axis'");
    if (namedAttrIt->getName() == InsertSliceAsyncOp::getAxisAttrName(*odsOpName)) {
      tblgen_axis = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_cache;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.insert_slice_async' op ""requires attribute 'cache'");
    if (namedAttrIt->getName() == InsertSliceAsyncOp::getCacheAttrName(*odsOpName)) {
      tblgen_cache = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_evict;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.insert_slice_async' op ""requires attribute 'evict'");
    if (namedAttrIt->getName() == InsertSliceAsyncOp::getEvictAttrName(*odsOpName)) {
      tblgen_evict = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_isVolatile;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.insert_slice_async' op ""requires attribute 'isVolatile'");
    if (namedAttrIt->getName() == InsertSliceAsyncOp::getIsVolatileAttrName(*odsOpName)) {
      tblgen_isVolatile = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_operand_segment_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitError(loc, "'triton_gpu.insert_slice_async' op ""requires attribute 'operand_segment_sizes'");
    if (namedAttrIt->getName() == InsertSliceAsyncOp::getOperandSegmentSizesAttrName(*odsOpName)) {
      tblgen_operand_segment_sizes = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  {
    auto sizeAttr = tblgen_operand_segment_sizes.cast<::mlir::DenseI32ArrayAttr>();
    auto numElements = sizeAttr.asArrayRef().size();
    if (numElements != 5)
      return emitError(loc, "'triton_gpu.insert_slice_async' op ""'operand_segment_sizes' attribute for specifying operand segments must have 5 "
                "elements, but got ") << numElements;
  }

  if (tblgen_cache && !((tblgen_cache.isa<::mlir::triton::CacheModifierAttr>())))
    return emitError(loc, "'triton_gpu.insert_slice_async' op ""attribute 'cache' failed to satisfy constraint: allowed 32-bit signless integer cases: 1, 2, 3");

  if (tblgen_evict && !((tblgen_evict.isa<::mlir::triton::EvictionPolicyAttr>())))
    return emitError(loc, "'triton_gpu.insert_slice_async' op ""attribute 'evict' failed to satisfy constraint: allowed 32-bit signless integer cases: 1, 2, 3");

  if (tblgen_isVolatile && !((tblgen_isVolatile.isa<::mlir::BoolAttr>())))
    return emitError(loc, "'triton_gpu.insert_slice_async' op ""attribute 'isVolatile' failed to satisfy constraint: bool attribute");

  if (tblgen_axis && !(((tblgen_axis.isa<::mlir::IntegerAttr>())) && ((tblgen_axis.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))))
    return emitError(loc, "'triton_gpu.insert_slice_async' op ""attribute 'axis' failed to satisfy constraint: 32-bit signless integer attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> InsertSliceAsyncOp::getODSOperandIndexAndLength(unsigned index) {
  auto sizeAttr = ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 4, (*this)->getAttrs().end() - 0, getOperandSegmentSizesAttrName()).cast<::mlir::DenseI32ArrayAttr>();

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttr[i];
  return {start, sizeAttr[index]};
}

::mlir::Operation::operand_range InsertSliceAsyncOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::TensorType> InsertSliceAsyncOp::getSrc() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*getODSOperands(0).begin());
}

::mlir::Value InsertSliceAsyncOp::getDst() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(1).begin());
}

::mlir::TypedValue<::mlir::IntegerType> InsertSliceAsyncOp::getIndex() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::IntegerType>>(*getODSOperands(2).begin());
}

::mlir::TypedValue<::mlir::TensorType> InsertSliceAsyncOp::getMask() {
  auto operands = getODSOperands(3);
  return operands.empty() ? ::mlir::TypedValue<::mlir::TensorType>{} : ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*operands.begin());
}

::mlir::Value InsertSliceAsyncOp::getOther() {
  auto operands = getODSOperands(4);
  return operands.empty() ? ::mlir::Value{} : ::llvm::cast<::mlir::Value>(*operands.begin());
}

::mlir::MutableOperandRange InsertSliceAsyncOp::getSrcMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(0u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 4, (*this)->getAttrs().end() - 0, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange InsertSliceAsyncOp::getDstMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(1u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 4, (*this)->getAttrs().end() - 0, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange InsertSliceAsyncOp::getIndexMutable() {
  auto range = getODSOperandIndexAndLength(2);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(2u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 4, (*this)->getAttrs().end() - 0, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange InsertSliceAsyncOp::getMaskMutable() {
  auto range = getODSOperandIndexAndLength(3);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(3u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 4, (*this)->getAttrs().end() - 0, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange InsertSliceAsyncOp::getOtherMutable() {
  auto range = getODSOperandIndexAndLength(4);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(4u, *::mlir::impl::getNamedAttrFromSortedRange((*this)->getAttrs().begin() + 4, (*this)->getAttrs().end() - 0, getOperandSegmentSizesAttrName())));
  return mutableRange;
}

std::pair<unsigned, unsigned> InsertSliceAsyncOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range InsertSliceAsyncOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value InsertSliceAsyncOp::getResult() {
  return ::llvm::cast<::mlir::Value>(*getODSResults(0).begin());
}

::mlir::triton::CacheModifierAttr InsertSliceAsyncOp::getCacheAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 1, (*this)->getAttrs().end() - 3, getCacheAttrName()).cast<::mlir::triton::CacheModifierAttr>();
}

::mlir::triton::CacheModifier InsertSliceAsyncOp::getCache() {
  auto attr = getCacheAttr();
  return attr.getValue();
}

::mlir::triton::EvictionPolicyAttr InsertSliceAsyncOp::getEvictAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 2, (*this)->getAttrs().end() - 2, getEvictAttrName()).cast<::mlir::triton::EvictionPolicyAttr>();
}

::mlir::triton::EvictionPolicy InsertSliceAsyncOp::getEvict() {
  auto attr = getEvictAttr();
  return attr.getValue();
}

::mlir::BoolAttr InsertSliceAsyncOp::getIsVolatileAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 3, (*this)->getAttrs().end() - 1, getIsVolatileAttrName()).cast<::mlir::BoolAttr>();
}

bool InsertSliceAsyncOp::getIsVolatile() {
  auto attr = getIsVolatileAttr();
  return attr.getValue();
}

::mlir::IntegerAttr InsertSliceAsyncOp::getAxisAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 4, getAxisAttrName()).cast<::mlir::IntegerAttr>();
}

uint32_t InsertSliceAsyncOp::getAxis() {
  auto attr = getAxisAttr();
  return attr.getValue().getZExtValue();
}

void InsertSliceAsyncOp::setCacheAttr(::mlir::triton::CacheModifierAttr attr) {
  (*this)->setAttr(getCacheAttrName(), attr);
}

void InsertSliceAsyncOp::setCache(::mlir::triton::CacheModifier attrValue) {
  (*this)->setAttr(getCacheAttrName(), ::mlir::triton::CacheModifierAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void InsertSliceAsyncOp::setEvictAttr(::mlir::triton::EvictionPolicyAttr attr) {
  (*this)->setAttr(getEvictAttrName(), attr);
}

void InsertSliceAsyncOp::setEvict(::mlir::triton::EvictionPolicy attrValue) {
  (*this)->setAttr(getEvictAttrName(), ::mlir::triton::EvictionPolicyAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void InsertSliceAsyncOp::setIsVolatileAttr(::mlir::BoolAttr attr) {
  (*this)->setAttr(getIsVolatileAttrName(), attr);
}

void InsertSliceAsyncOp::setIsVolatile(bool attrValue) {
  (*this)->setAttr(getIsVolatileAttrName(), ::mlir::Builder((*this)->getContext()).getBoolAttr(attrValue));
}

void InsertSliceAsyncOp::setAxisAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getAxisAttrName(), attr);
}

void InsertSliceAsyncOp::setAxis(uint32_t attrValue) {
  (*this)->setAttr(getAxisAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIntegerType(32), attrValue));
}

void InsertSliceAsyncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src, ::mlir::Value dst, ::mlir::Value index, /*optional*/::mlir::Value mask, /*optional*/::mlir::Value other, ::mlir::triton::CacheModifierAttr cache, ::mlir::triton::EvictionPolicyAttr evict, ::mlir::BoolAttr isVolatile, ::mlir::IntegerAttr axis) {
  odsState.addOperands(src);
  odsState.addOperands(dst);
  odsState.addOperands(index);
  if (mask)
    odsState.addOperands(mask);
  if (other)
    odsState.addOperands(other);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, 1, 1, (mask ? 1 : 0), (other ? 1 : 0)}));
  odsState.addAttribute(getCacheAttrName(odsState.name), cache);
  odsState.addAttribute(getEvictAttrName(odsState.name), evict);
  odsState.addAttribute(getIsVolatileAttrName(odsState.name), isVolatile);
  odsState.addAttribute(getAxisAttrName(odsState.name), axis);
  odsState.addTypes(result);
}

void InsertSliceAsyncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src, ::mlir::Value dst, ::mlir::Value index, /*optional*/::mlir::Value mask, /*optional*/::mlir::Value other, ::mlir::triton::CacheModifierAttr cache, ::mlir::triton::EvictionPolicyAttr evict, ::mlir::BoolAttr isVolatile, ::mlir::IntegerAttr axis) {
  odsState.addOperands(src);
  odsState.addOperands(dst);
  odsState.addOperands(index);
  if (mask)
    odsState.addOperands(mask);
  if (other)
    odsState.addOperands(other);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, 1, 1, (mask ? 1 : 0), (other ? 1 : 0)}));
  odsState.addAttribute(getCacheAttrName(odsState.name), cache);
  odsState.addAttribute(getEvictAttrName(odsState.name), evict);
  odsState.addAttribute(getIsVolatileAttrName(odsState.name), isVolatile);
  odsState.addAttribute(getAxisAttrName(odsState.name), axis);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void InsertSliceAsyncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src, ::mlir::Value dst, ::mlir::Value index, /*optional*/::mlir::Value mask, /*optional*/::mlir::Value other, ::mlir::triton::CacheModifier cache, ::mlir::triton::EvictionPolicy evict, bool isVolatile, uint32_t axis) {
  odsState.addOperands(src);
  odsState.addOperands(dst);
  odsState.addOperands(index);
  if (mask)
    odsState.addOperands(mask);
  if (other)
    odsState.addOperands(other);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, 1, 1, (mask ? 1 : 0), (other ? 1 : 0)}));
  odsState.addAttribute(getCacheAttrName(odsState.name), ::mlir::triton::CacheModifierAttr::get(odsBuilder.getContext(), cache));
  odsState.addAttribute(getEvictAttrName(odsState.name), ::mlir::triton::EvictionPolicyAttr::get(odsBuilder.getContext(), evict));
  odsState.addAttribute(getIsVolatileAttrName(odsState.name), odsBuilder.getBoolAttr(isVolatile));
  odsState.addAttribute(getAxisAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), axis));
  odsState.addTypes(result);
}

void InsertSliceAsyncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src, ::mlir::Value dst, ::mlir::Value index, /*optional*/::mlir::Value mask, /*optional*/::mlir::Value other, ::mlir::triton::CacheModifier cache, ::mlir::triton::EvictionPolicy evict, bool isVolatile, uint32_t axis) {
  odsState.addOperands(src);
  odsState.addOperands(dst);
  odsState.addOperands(index);
  if (mask)
    odsState.addOperands(mask);
  if (other)
    odsState.addOperands(other);
  odsState.addAttribute(getOperandSegmentSizesAttrName(odsState.name), odsBuilder.getDenseI32ArrayAttr({1, 1, 1, (mask ? 1 : 0), (other ? 1 : 0)}));
  odsState.addAttribute(getCacheAttrName(odsState.name), ::mlir::triton::CacheModifierAttr::get(odsBuilder.getContext(), cache));
  odsState.addAttribute(getEvictAttrName(odsState.name), ::mlir::triton::EvictionPolicyAttr::get(odsBuilder.getContext(), evict));
  odsState.addAttribute(getIsVolatileAttrName(odsState.name), odsBuilder.getBoolAttr(isVolatile));
  odsState.addAttribute(getAxisAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), axis));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void InsertSliceAsyncOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() >= 3u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult InsertSliceAsyncOp::verifyInvariantsImpl() {
  auto namedAttrRange = (*this)->getAttrs();
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_axis;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'axis'");
    if (namedAttrIt->getName() == getAxisAttrName()) {
      tblgen_axis = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_cache;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'cache'");
    if (namedAttrIt->getName() == getCacheAttrName()) {
      tblgen_cache = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_evict;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'evict'");
    if (namedAttrIt->getName() == getEvictAttrName()) {
      tblgen_evict = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_isVolatile;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'isVolatile'");
    if (namedAttrIt->getName() == getIsVolatileAttrName()) {
      tblgen_isVolatile = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }
  ::mlir::Attribute tblgen_operand_segment_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end())
      return emitOpError("requires attribute 'operand_segment_sizes'");
    if (namedAttrIt->getName() == getOperandSegmentSizesAttrName()) {
      tblgen_operand_segment_sizes = namedAttrIt->getValue();
      break;
    }
    ++namedAttrIt;
  }

  {
    auto sizeAttr = tblgen_operand_segment_sizes.cast<::mlir::DenseI32ArrayAttr>();
    auto numElements = sizeAttr.asArrayRef().size();
    if (numElements != 5)
      return emitOpError("'operand_segment_sizes' attribute for specifying operand segments must have 5 "
                "elements, but got ") << numElements;
  }

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps4(*this, tblgen_cache, "cache")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps5(*this, tblgen_evict, "evict")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps6(*this, tblgen_isVolatile, "isVolatile")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_TritonGPUOps0(*this, tblgen_axis, "axis")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps6(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps5(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    if (valueGroup3.size() > 1) {
      return emitOpError("operand group starting at #") << index
          << " requires 0 or 1 element, but found " << valueGroup3.size();
    }

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps7(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    if (valueGroup4.size() > 1) {
      return emitOpError("operand group starting at #") << index
          << " requires 0 or 1 element, but found " << valueGroup4.size();
    }

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps8(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  if (!((((*this->getOperation()).getOperands().size() <= 3) || std::equal_to<>()(getI1SameShape((*this->getODSOperands(0).begin()).getType()), (*this->getODSOperands(3).begin()).getType()))))
    return emitOpError("failed to verify that infer mask type from src type");
  if (!((((*this->getOperation()).getOperands().size() <= 4) || std::equal_to<>()(getPointeeType((*this->getODSOperands(0).begin()).getType()), (*this->getODSOperands(4).begin()).getType()))))
    return emitOpError("failed to verify that infer other type from src type");
  return ::mlir::success();
}

::mlir::LogicalResult InsertSliceAsyncOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

void InsertSliceAsyncOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  effects.emplace_back(::mlir::MemoryEffects::Read::get(), ::mlir::SideEffects::DefaultResource::get());
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::InsertSliceAsyncOp)

namespace mlir {
namespace triton {
namespace gpu {

//===----------------------------------------------------------------------===//
// ::mlir::triton::gpu::SelectOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
SelectOpGenericAdaptorBase::SelectOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("triton_gpu.select", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> SelectOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr SelectOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
SelectOpAdaptor::SelectOpAdaptor(SelectOp op) : SelectOpAdaptor(op->getOperands(), op->getAttrDictionary(), op->getRegions()) {}

::mlir::LogicalResult SelectOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> SelectOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range SelectOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value SelectOp::getCondition() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(0).begin());
}

::mlir::Value SelectOp::getTrueValue() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(1).begin());
}

::mlir::Value SelectOp::getFalseValue() {
  return ::llvm::cast<::mlir::Value>(*getODSOperands(2).begin());
}

::mlir::MutableOperandRange SelectOp::getConditionMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange SelectOp::getTrueValueMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange SelectOp::getFalseValueMutable() {
  auto range = getODSOperandIndexAndLength(2);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> SelectOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range SelectOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value SelectOp::getResult() {
  return ::llvm::cast<::mlir::Value>(*getODSResults(0).begin());
}

void SelectOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value condition, ::mlir::Value true_value, ::mlir::Value false_value) {
  odsState.addOperands(condition);
  odsState.addOperands(true_value);
  odsState.addOperands(false_value);
  odsState.addTypes(result);
}

void SelectOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value condition, ::mlir::Value true_value, ::mlir::Value false_value) {
  odsState.addOperands(condition);
  odsState.addOperands(true_value);
  odsState.addOperands(false_value);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void SelectOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 3u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult SelectOp::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_TritonGPUOps8(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult SelectOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

void SelectOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::SelectOp)


#endif  // GET_OP_CLASSES

