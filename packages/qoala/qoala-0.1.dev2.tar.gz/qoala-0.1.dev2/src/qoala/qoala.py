class HirProgram:
    pass


class LirProgram:
    pass


class LhrProgram:
    pass


class Compiler:
    def hir_to_lir(self, hir_program: HirProgram) -> LirProgram:
        return LirProgram()

    def lir_to_lhr(self, lir_program: LirProgram) -> LhrProgram:
        return LhrProgram()


if __name__ == "__main__":
    compiler = Compiler()
    hir = HirProgram()
    lir = compiler.hir_to_lir(hir)
    lhr = compiler.lir_to_lhr(lir)

    print(lhr)
