# Generated from IG.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .IGParser import IGParser
else:
    from IGParser import IGParser

# This class defines a complete generic visitor for a parse tree produced by IGParser.

class IGVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IGParser#prog.
    def visitProg(self, ctx:IGParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#var_block.
    def visitVar_block(self, ctx:IGParser.Var_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#var_decl.
    def visitVar_decl(self, ctx:IGParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#reg_block.
    def visitReg_block(self, ctx:IGParser.Reg_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#reg_decl.
    def visitReg_decl(self, ctx:IGParser.Reg_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#expr_neg.
    def visitExpr_neg(self, ctx:IGParser.Expr_negContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#expr_bool_op.
    def visitExpr_bool_op(self, ctx:IGParser.Expr_bool_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#expr_brackets.
    def visitExpr_brackets(self, ctx:IGParser.Expr_bracketsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#expr_atome.
    def visitExpr_atome(self, ctx:IGParser.Expr_atomeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#expr_mux_name.
    def visitExpr_mux_name(self, ctx:IGParser.Expr_mux_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_block.
    def visitHybrid_hoare_block(self, ctx:IGParser.Hybrid_hoare_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_decl.
    def visitHybrid_hoare_decl(self, ctx:IGParser.Hybrid_hoare_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_pre_decl.
    def visitHybrid_hoare_pre_decl(self, ctx:IGParser.Hybrid_hoare_pre_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_post_decl.
    def visitHybrid_hoare_post_decl(self, ctx:IGParser.Hybrid_hoare_post_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#discrete_condition.
    def visitDiscrete_condition(self, ctx:IGParser.Discrete_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_condition.
    def visitHybrid_condition(self, ctx:IGParser.Hybrid_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_trace_decl.
    def visitHybrid_hoare_trace_decl(self, ctx:IGParser.Hybrid_hoare_trace_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_trace.
    def visitHybrid_hoare_trace(self, ctx:IGParser.Hybrid_hoare_traceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_dpa.
    def visitHybrid_hoare_dpa(self, ctx:IGParser.Hybrid_hoare_dpaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IGParser#hybrid_hoare_slide.
    def visitHybrid_hoare_slide(self, ctx:IGParser.Hybrid_hoare_slideContext):
        return self.visitChildren(ctx)



del IGParser