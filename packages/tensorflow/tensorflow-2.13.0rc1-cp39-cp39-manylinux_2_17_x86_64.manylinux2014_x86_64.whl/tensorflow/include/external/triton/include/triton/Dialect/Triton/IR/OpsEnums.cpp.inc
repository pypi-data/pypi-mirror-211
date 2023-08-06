/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace triton {
::llvm::StringRef stringifyRMWOp(RMWOp val) {
  switch (val) {
    case RMWOp::AND: return "and";
    case RMWOp::OR: return "or";
    case RMWOp::XOR: return "xor";
    case RMWOp::ADD: return "add";
    case RMWOp::FADD: return "fadd";
    case RMWOp::MAX: return "max";
    case RMWOp::MIN: return "min";
    case RMWOp::UMAX: return "umax";
    case RMWOp::UMIN: return "umin";
    case RMWOp::XCHG: return "exch";
  }
  return "";
}

::std::optional<RMWOp> symbolizeRMWOp(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<RMWOp>>(str)
      .Case("and", RMWOp::AND)
      .Case("or", RMWOp::OR)
      .Case("xor", RMWOp::XOR)
      .Case("add", RMWOp::ADD)
      .Case("fadd", RMWOp::FADD)
      .Case("max", RMWOp::MAX)
      .Case("min", RMWOp::MIN)
      .Case("umax", RMWOp::UMAX)
      .Case("umin", RMWOp::UMIN)
      .Case("exch", RMWOp::XCHG)
      .Default(::std::nullopt);
}
::std::optional<RMWOp> symbolizeRMWOp(uint32_t value) {
  switch (value) {
  case 1: return RMWOp::AND;
  case 2: return RMWOp::OR;
  case 3: return RMWOp::XOR;
  case 4: return RMWOp::ADD;
  case 5: return RMWOp::FADD;
  case 6: return RMWOp::MAX;
  case 7: return RMWOp::MIN;
  case 8: return RMWOp::UMAX;
  case 9: return RMWOp::UMIN;
  case 10: return RMWOp::XCHG;
  default: return ::std::nullopt;
  }
}

bool RMWOpAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 3)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 4)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 5)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 6)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 7)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 8)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 9)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 10)));
}
RMWOpAttr RMWOpAttr::get(::mlir::MLIRContext *context, RMWOp val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<RMWOpAttr>();
}
RMWOp RMWOpAttr::getValue() const {
  return static_cast<RMWOp>(::mlir::IntegerAttr::getInt());
}
} // namespace triton
} // namespace mlir

namespace mlir {
namespace triton {
::llvm::StringRef stringifyCacheModifier(CacheModifier val) {
  switch (val) {
    case CacheModifier::NONE: return "none";
    case CacheModifier::CA: return "ca";
    case CacheModifier::CG: return "cg";
  }
  return "";
}

::std::optional<CacheModifier> symbolizeCacheModifier(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<CacheModifier>>(str)
      .Case("none", CacheModifier::NONE)
      .Case("ca", CacheModifier::CA)
      .Case("cg", CacheModifier::CG)
      .Default(::std::nullopt);
}
::std::optional<CacheModifier> symbolizeCacheModifier(uint32_t value) {
  switch (value) {
  case 1: return CacheModifier::NONE;
  case 2: return CacheModifier::CA;
  case 3: return CacheModifier::CG;
  default: return ::std::nullopt;
  }
}

bool CacheModifierAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 3)));
}
CacheModifierAttr CacheModifierAttr::get(::mlir::MLIRContext *context, CacheModifier val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<CacheModifierAttr>();
}
CacheModifier CacheModifierAttr::getValue() const {
  return static_cast<CacheModifier>(::mlir::IntegerAttr::getInt());
}
} // namespace triton
} // namespace mlir

namespace mlir {
namespace triton {
::llvm::StringRef stringifyEvictionPolicy(EvictionPolicy val) {
  switch (val) {
    case EvictionPolicy::NORMAL: return "evict_normal";
    case EvictionPolicy::EVICT_FIRST: return "evict_first";
    case EvictionPolicy::EVICT_LAST: return "evict_last";
  }
  return "";
}

::std::optional<EvictionPolicy> symbolizeEvictionPolicy(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<EvictionPolicy>>(str)
      .Case("evict_normal", EvictionPolicy::NORMAL)
      .Case("evict_first", EvictionPolicy::EVICT_FIRST)
      .Case("evict_last", EvictionPolicy::EVICT_LAST)
      .Default(::std::nullopt);
}
::std::optional<EvictionPolicy> symbolizeEvictionPolicy(uint32_t value) {
  switch (value) {
  case 1: return EvictionPolicy::NORMAL;
  case 2: return EvictionPolicy::EVICT_FIRST;
  case 3: return EvictionPolicy::EVICT_LAST;
  default: return ::std::nullopt;
  }
}

bool EvictionPolicyAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 3)));
}
EvictionPolicyAttr EvictionPolicyAttr::get(::mlir::MLIRContext *context, EvictionPolicy val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<EvictionPolicyAttr>();
}
EvictionPolicy EvictionPolicyAttr::getValue() const {
  return static_cast<EvictionPolicy>(::mlir::IntegerAttr::getInt());
}
} // namespace triton
} // namespace mlir

namespace mlir {
namespace triton {
::llvm::StringRef stringifyPaddingOption(PaddingOption val) {
  switch (val) {
    case PaddingOption::PAD_ZERO: return "zero";
    case PaddingOption::PAD_NAN: return "nan";
  }
  return "";
}

::std::optional<PaddingOption> symbolizePaddingOption(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<PaddingOption>>(str)
      .Case("zero", PaddingOption::PAD_ZERO)
      .Case("nan", PaddingOption::PAD_NAN)
      .Default(::std::nullopt);
}
::std::optional<PaddingOption> symbolizePaddingOption(uint32_t value) {
  switch (value) {
  case 1: return PaddingOption::PAD_ZERO;
  case 2: return PaddingOption::PAD_NAN;
  default: return ::std::nullopt;
  }
}

bool PaddingOptionAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)));
}
PaddingOptionAttr PaddingOptionAttr::get(::mlir::MLIRContext *context, PaddingOption val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<PaddingOptionAttr>();
}
PaddingOption PaddingOptionAttr::getValue() const {
  return static_cast<PaddingOption>(::mlir::IntegerAttr::getInt());
}
} // namespace triton
} // namespace mlir

