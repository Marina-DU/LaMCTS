# Generated from IG.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .IGParser import IGParser
else:
    from IGParser import IGParser

# This class defines a complete listener for a parse tree produced by IGParser.
class IGListener(ParseTreeListener):

    # Enter a parse tree produced by IGParser#prog.
    def enterProg(self, ctx:IGParser.ProgContext):
        pass

    # Exit a parse tree produced by IGParser#prog.
    def exitProg(self, ctx:IGParser.ProgContext):
        pass


    # Enter a parse tree produced by IGParser#var_block.
    def enterVar_block(self, ctx:IGParser.Var_blockContext):
        pass

    # Exit a parse tree produced by IGParser#var_block.
    def exitVar_block(self, ctx:IGParser.Var_blockContext):
        pass


    # Enter a parse tree produced by IGParser#var_decl.
    def enterVar_decl(self, ctx:IGParser.Var_declContext):
        pass

    # Exit a parse tree produced by IGParser#var_decl.
    def exitVar_decl(self, ctx:IGParser.Var_declContext):
        pass


    # Enter a parse tree produced by IGParser#reg_block.
    def enterReg_block(self, ctx:IGParser.Reg_blockContext):
        pass

    # Exit a parse tree produced by IGParser#reg_block.
    def exitReg_block(self, ctx:IGParser.Reg_blockContext):
        pass


    # Enter a parse tree produced by IGParser#reg_decl.
    def enterReg_decl(self, ctx:IGParser.Reg_declContext):
        pass

    # Exit a parse tree produced by IGParser#reg_decl.
    def exitReg_decl(self, ctx:IGParser.Reg_declContext):
        pass


    # Enter a parse tree produced by IGParser#expr_neg.
    def enterExpr_neg(self, ctx:IGParser.Expr_negContext):
        pass

    # Exit a parse tree produced by IGParser#expr_neg.
    def exitExpr_neg(self, ctx:IGParser.Expr_negContext):
        pass


    # Enter a parse tree produced by IGParser#expr_bool_op.
    def enterExpr_bool_op(self, ctx:IGParser.Expr_bool_opContext):
        pass

    # Exit a parse tree produced by IGParser#expr_bool_op.
    def exitExpr_bool_op(self, ctx:IGParser.Expr_bool_opContext):
        pass


    # Enter a parse tree produced by IGParser#expr_brackets.
    def enterExpr_brackets(self, ctx:IGParser.Expr_bracketsContext):
        pass

    # Exit a parse tree produced by IGParser#expr_brackets.
    def exitExpr_brackets(self, ctx:IGParser.Expr_bracketsContext):
        pass


    # Enter a parse tree produced by IGParser#expr_atome.
    def enterExpr_atome(self, ctx:IGParser.Expr_atomeContext):
        pass

    # Exit a parse tree produced by IGParser#expr_atome.
    def exitExpr_atome(self, ctx:IGParser.Expr_atomeContext):
        pass


    # Enter a parse tree produced by IGParser#expr_mux_name.
    def enterExpr_mux_name(self, ctx:IGParser.Expr_mux_nameContext):
        pass

    # Exit a parse tree produced by IGParser#expr_mux_name.
    def exitExpr_mux_name(self, ctx:IGParser.Expr_mux_nameContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_block.
    def enterHybrid_hoare_block(self, ctx:IGParser.Hybrid_hoare_blockContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_block.
    def exitHybrid_hoare_block(self, ctx:IGParser.Hybrid_hoare_blockContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_decl.
    def enterHybrid_hoare_decl(self, ctx:IGParser.Hybrid_hoare_declContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_decl.
    def exitHybrid_hoare_decl(self, ctx:IGParser.Hybrid_hoare_declContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_pre_decl.
    def enterHybrid_hoare_pre_decl(self, ctx:IGParser.Hybrid_hoare_pre_declContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_pre_decl.
    def exitHybrid_hoare_pre_decl(self, ctx:IGParser.Hybrid_hoare_pre_declContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_post_decl.
    def enterHybrid_hoare_post_decl(self, ctx:IGParser.Hybrid_hoare_post_declContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_post_decl.
    def exitHybrid_hoare_post_decl(self, ctx:IGParser.Hybrid_hoare_post_declContext):
        pass


    # Enter a parse tree produced by IGParser#discrete_condition.
    def enterDiscrete_condition(self, ctx:IGParser.Discrete_conditionContext):
        pass

    # Exit a parse tree produced by IGParser#discrete_condition.
    def exitDiscrete_condition(self, ctx:IGParser.Discrete_conditionContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_condition.
    def enterHybrid_condition(self, ctx:IGParser.Hybrid_conditionContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_condition.
    def exitHybrid_condition(self, ctx:IGParser.Hybrid_conditionContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_trace_decl.
    def enterHybrid_hoare_trace_decl(self, ctx:IGParser.Hybrid_hoare_trace_declContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_trace_decl.
    def exitHybrid_hoare_trace_decl(self, ctx:IGParser.Hybrid_hoare_trace_declContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_trace.
    def enterHybrid_hoare_trace(self, ctx:IGParser.Hybrid_hoare_traceContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_trace.
    def exitHybrid_hoare_trace(self, ctx:IGParser.Hybrid_hoare_traceContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_dpa.
    def enterHybrid_hoare_dpa(self, ctx:IGParser.Hybrid_hoare_dpaContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_dpa.
    def exitHybrid_hoare_dpa(self, ctx:IGParser.Hybrid_hoare_dpaContext):
        pass


    # Enter a parse tree produced by IGParser#hybrid_hoare_slide.
    def enterHybrid_hoare_slide(self, ctx:IGParser.Hybrid_hoare_slideContext):
        pass

    # Exit a parse tree produced by IGParser#hybrid_hoare_slide.
    def exitHybrid_hoare_slide(self, ctx:IGParser.Hybrid_hoare_slideContext):
        pass


