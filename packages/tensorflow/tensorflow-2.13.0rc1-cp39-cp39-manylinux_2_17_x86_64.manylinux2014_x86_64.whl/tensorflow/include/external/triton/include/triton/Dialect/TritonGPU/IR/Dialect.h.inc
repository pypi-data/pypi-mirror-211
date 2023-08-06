/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Dialect Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace triton {
namespace gpu {

class TritonGPUDialect : public ::mlir::Dialect {
  explicit TritonGPUDialect(::mlir::MLIRContext *context);

  void initialize();
  friend class ::mlir::MLIRContext;
public:
  ~TritonGPUDialect() override;
  static constexpr ::llvm::StringLiteral getDialectNamespace() {
    return ::llvm::StringLiteral("triton_gpu");
  }

  /// Parse an attribute registered to this dialect.
  ::mlir::Attribute parseAttribute(::mlir::DialectAsmParser &parser,
                                   ::mlir::Type type) const override;

  /// Print an attribute registered to this dialect.
  void printAttribute(::mlir::Attribute attr,
                      ::mlir::DialectAsmPrinter &os) const override;

    /// Provides a hook for verifying dialect attributes attached to the given
    /// op.
    ::mlir::LogicalResult verifyOperationAttribute(
        ::mlir::Operation *op, ::mlir::NamedAttribute attribute) override;

    static std::string getNumWarpsAttrName() { return "triton_gpu.num-warps"; }
    static int getNumWarps(ModuleOp mod) {
      if(!mod->hasAttr("triton_gpu.num-warps"))
        llvm::report_fatal_error(
            "TritonGPU module should contain a triton_gpu.num-warps attribute");
      return mod->getAttr("triton_gpu.num-warps").cast<IntegerAttr>().getInt();
    }
  };
} // namespace gpu
} // namespace triton
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::triton::gpu::TritonGPUDialect)
