// Generated from /home/romain/Documents/BioEvolNet/Code/parser/grammar/IG.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class IGParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, KVAR=13, KREG=14, KHYBRIDHOARE=15, KPRE=16, 
		KTRACE=17, KPOST=18, KCYCLIC=19, NOKB=20, AND=21, SLIDE=22, NOSLIDE=23, 
		ID=24, NUM=25, FLOAT=26, EQ=27, SEMI=28, NEG=29, BOOL_OP=30, SEUIL=31, 
		CIBLE=32, OPER=33, WS=34, COMMENT=35;
	public static final int
		RULE_prog = 0, RULE_var_block = 1, RULE_var_decl = 2, RULE_reg_block = 3, 
		RULE_reg_decl = 4, RULE_reg_expr = 5, RULE_hybrid_hoare_block = 6, RULE_hybrid_hoare_decl = 7, 
		RULE_hybrid_hoare_pre_decl = 8, RULE_hybrid_hoare_post_decl = 9, RULE_discrete_condition = 10, 
		RULE_hybrid_condition = 11, RULE_hybrid_hoare_trace_decl = 12, RULE_hybrid_hoare_trace = 13, 
		RULE_hybrid_hoare_dpa = 14, RULE_hybrid_hoare_slide = 15;
	private static String[] makeRuleNames() {
		return new String[] {
			"prog", "var_block", "var_decl", "reg_block", "reg_decl", "reg_expr", 
			"hybrid_hoare_block", "hybrid_hoare_decl", "hybrid_hoare_pre_decl", "hybrid_hoare_post_decl", 
			"discrete_condition", "hybrid_condition", "hybrid_hoare_trace_decl", 
			"hybrid_hoare_trace", "hybrid_hoare_dpa", "hybrid_hoare_slide"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'END'", "'..'", "'['", "']'", "'('", "')'", "':'", "'{'", "'}'", 
			"','", "'eta'", "'pi'", "'VAR'", "'REG'", "'HYBRID HOARE'", "'PRE'", 
			"'TRACE'", "'POST'", "'CYCLIC'", "'True'", "'and'", "'slide'", "'noslide'", 
			null, null, null, "'='", "';'", "'!'", null, "'>='", "'=>'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "KVAR", "KREG", "KHYBRIDHOARE", "KPRE", "KTRACE", "KPOST", "KCYCLIC", 
			"NOKB", "AND", "SLIDE", "NOSLIDE", "ID", "NUM", "FLOAT", "EQ", "SEMI", 
			"NEG", "BOOL_OP", "SEUIL", "CIBLE", "OPER", "WS", "COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "IG.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public IGParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class ProgContext extends ParserRuleContext {
		public Var_blockContext var_block() {
			return getRuleContext(Var_blockContext.class,0);
		}
		public Reg_blockContext reg_block() {
			return getRuleContext(Reg_blockContext.class,0);
		}
		public Hybrid_hoare_blockContext hybrid_hoare_block() {
			return getRuleContext(Hybrid_hoare_blockContext.class,0);
		}
		public TerminalNode KCYCLIC() { return getToken(IGParser.KCYCLIC, 0); }
		public ProgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prog; }
	}

	public final ProgContext prog() throws RecognitionException {
		ProgContext _localctx = new ProgContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_prog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(32);
			var_block();
			setState(33);
			reg_block();
			setState(34);
			hybrid_hoare_block();
			setState(36);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==KCYCLIC) {
				{
				setState(35);
				match(KCYCLIC);
				}
			}

			setState(38);
			match(T__0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Var_blockContext extends ParserRuleContext {
		public TerminalNode KVAR() { return getToken(IGParser.KVAR, 0); }
		public List<Var_declContext> var_decl() {
			return getRuleContexts(Var_declContext.class);
		}
		public Var_declContext var_decl(int i) {
			return getRuleContext(Var_declContext.class,i);
		}
		public Var_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_block; }
	}

	public final Var_blockContext var_block() throws RecognitionException {
		Var_blockContext _localctx = new Var_blockContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_var_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(40);
			match(KVAR);
			setState(42); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(41);
				var_decl();
				}
				}
				setState(44); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ID );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Var_declContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public TerminalNode EQ() { return getToken(IGParser.EQ, 0); }
		public List<TerminalNode> NUM() { return getTokens(IGParser.NUM); }
		public TerminalNode NUM(int i) {
			return getToken(IGParser.NUM, i);
		}
		public TerminalNode SEMI() { return getToken(IGParser.SEMI, 0); }
		public Var_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_decl; }
	}

	public final Var_declContext var_decl() throws RecognitionException {
		Var_declContext _localctx = new Var_declContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_var_decl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(46);
			match(ID);
			setState(47);
			match(EQ);
			setState(48);
			match(NUM);
			setState(49);
			match(T__1);
			setState(50);
			match(NUM);
			setState(51);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Reg_blockContext extends ParserRuleContext {
		public TerminalNode KREG() { return getToken(IGParser.KREG, 0); }
		public List<Reg_declContext> reg_decl() {
			return getRuleContexts(Reg_declContext.class);
		}
		public Reg_declContext reg_decl(int i) {
			return getRuleContext(Reg_declContext.class,i);
		}
		public Reg_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reg_block; }
	}

	public final Reg_blockContext reg_block() throws RecognitionException {
		Reg_blockContext _localctx = new Reg_blockContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_reg_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(53);
			match(KREG);
			setState(55); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(54);
				reg_decl();
				}
				}
				setState(57); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ID );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Reg_declContext extends ParserRuleContext {
		public List<TerminalNode> ID() { return getTokens(IGParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(IGParser.ID, i);
		}
		public Reg_exprContext reg_expr() {
			return getRuleContext(Reg_exprContext.class,0);
		}
		public TerminalNode CIBLE() { return getToken(IGParser.CIBLE, 0); }
		public TerminalNode SEMI() { return getToken(IGParser.SEMI, 0); }
		public Reg_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reg_decl; }
	}

	public final Reg_declContext reg_decl() throws RecognitionException {
		Reg_declContext _localctx = new Reg_declContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_reg_decl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(59);
			match(ID);
			setState(60);
			match(T__2);
			setState(61);
			reg_expr(0);
			setState(62);
			match(T__3);
			setState(63);
			match(CIBLE);
			setState(65); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(64);
				match(ID);
				}
				}
				setState(67); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ID );
			setState(69);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Reg_exprContext extends ParserRuleContext {
		public Reg_exprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reg_expr; }
	 
		public Reg_exprContext() { }
		public void copyFrom(Reg_exprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class Expr_negContext extends Reg_exprContext {
		public TerminalNode NEG() { return getToken(IGParser.NEG, 0); }
		public Reg_exprContext reg_expr() {
			return getRuleContext(Reg_exprContext.class,0);
		}
		public Expr_negContext(Reg_exprContext ctx) { copyFrom(ctx); }
	}
	public static class Expr_bool_opContext extends Reg_exprContext {
		public List<Reg_exprContext> reg_expr() {
			return getRuleContexts(Reg_exprContext.class);
		}
		public Reg_exprContext reg_expr(int i) {
			return getRuleContext(Reg_exprContext.class,i);
		}
		public TerminalNode BOOL_OP() { return getToken(IGParser.BOOL_OP, 0); }
		public Expr_bool_opContext(Reg_exprContext ctx) { copyFrom(ctx); }
	}
	public static class Expr_bracketsContext extends Reg_exprContext {
		public Reg_exprContext reg_expr() {
			return getRuleContext(Reg_exprContext.class,0);
		}
		public Expr_bracketsContext(Reg_exprContext ctx) { copyFrom(ctx); }
	}
	public static class Expr_atomeContext extends Reg_exprContext {
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public TerminalNode SEUIL() { return getToken(IGParser.SEUIL, 0); }
		public TerminalNode NUM() { return getToken(IGParser.NUM, 0); }
		public Expr_atomeContext(Reg_exprContext ctx) { copyFrom(ctx); }
	}
	public static class Expr_mux_nameContext extends Reg_exprContext {
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public Expr_mux_nameContext(Reg_exprContext ctx) { copyFrom(ctx); }
	}

	public final Reg_exprContext reg_expr() throws RecognitionException {
		return reg_expr(0);
	}

	private Reg_exprContext reg_expr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		Reg_exprContext _localctx = new Reg_exprContext(_ctx, _parentState);
		Reg_exprContext _prevctx = _localctx;
		int _startState = 10;
		enterRecursionRule(_localctx, 10, RULE_reg_expr, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(82);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
			case 1:
				{
				_localctx = new Expr_negContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(72);
				match(NEG);
				setState(73);
				reg_expr(5);
				}
				break;
			case 2:
				{
				_localctx = new Expr_bracketsContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(74);
				match(T__4);
				setState(75);
				reg_expr(0);
				setState(76);
				match(T__5);
				}
				break;
			case 3:
				{
				_localctx = new Expr_atomeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(78);
				match(ID);
				setState(79);
				match(SEUIL);
				setState(80);
				match(NUM);
				}
				break;
			case 4:
				{
				_localctx = new Expr_mux_nameContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(81);
				match(ID);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(89);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new Expr_bool_opContext(new Reg_exprContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_reg_expr);
					setState(84);
					if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
					setState(85);
					match(BOOL_OP);
					setState(86);
					reg_expr(5);
					}
					} 
				}
				setState(91);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class Hybrid_hoare_blockContext extends ParserRuleContext {
		public TerminalNode KHYBRIDHOARE() { return getToken(IGParser.KHYBRIDHOARE, 0); }
		public Hybrid_hoare_declContext hybrid_hoare_decl() {
			return getRuleContext(Hybrid_hoare_declContext.class,0);
		}
		public Hybrid_hoare_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_block; }
	}

	public final Hybrid_hoare_blockContext hybrid_hoare_block() throws RecognitionException {
		Hybrid_hoare_blockContext _localctx = new Hybrid_hoare_blockContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_hybrid_hoare_block);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(92);
			match(KHYBRIDHOARE);
			setState(93);
			hybrid_hoare_decl();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_declContext extends ParserRuleContext {
		public Hybrid_hoare_pre_declContext hybrid_hoare_pre_decl() {
			return getRuleContext(Hybrid_hoare_pre_declContext.class,0);
		}
		public Hybrid_hoare_trace_declContext hybrid_hoare_trace_decl() {
			return getRuleContext(Hybrid_hoare_trace_declContext.class,0);
		}
		public Hybrid_hoare_post_declContext hybrid_hoare_post_decl() {
			return getRuleContext(Hybrid_hoare_post_declContext.class,0);
		}
		public Hybrid_hoare_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_decl; }
	}

	public final Hybrid_hoare_declContext hybrid_hoare_decl() throws RecognitionException {
		Hybrid_hoare_declContext _localctx = new Hybrid_hoare_declContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_hybrid_hoare_decl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(95);
			hybrid_hoare_pre_decl();
			setState(96);
			hybrid_hoare_trace_decl();
			setState(97);
			hybrid_hoare_post_decl();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_pre_declContext extends ParserRuleContext {
		public TerminalNode KPRE() { return getToken(IGParser.KPRE, 0); }
		public Hybrid_hoare_pre_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_pre_decl; }
	}

	public final Hybrid_hoare_pre_declContext hybrid_hoare_pre_decl() throws RecognitionException {
		Hybrid_hoare_pre_declContext _localctx = new Hybrid_hoare_pre_declContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_hybrid_hoare_pre_decl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(99);
			match(KPRE);
			setState(100);
			match(T__6);
			setState(101);
			match(T__7);
			setState(102);
			match(T__8);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_post_declContext extends ParserRuleContext {
		public TerminalNode KPOST() { return getToken(IGParser.KPOST, 0); }
		public TerminalNode SEMI() { return getToken(IGParser.SEMI, 0); }
		public List<Discrete_conditionContext> discrete_condition() {
			return getRuleContexts(Discrete_conditionContext.class);
		}
		public Discrete_conditionContext discrete_condition(int i) {
			return getRuleContext(Discrete_conditionContext.class,i);
		}
		public List<Hybrid_conditionContext> hybrid_condition() {
			return getRuleContexts(Hybrid_conditionContext.class);
		}
		public Hybrid_conditionContext hybrid_condition(int i) {
			return getRuleContext(Hybrid_conditionContext.class,i);
		}
		public Hybrid_hoare_post_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_post_decl; }
	}

	public final Hybrid_hoare_post_declContext hybrid_hoare_post_decl() throws RecognitionException {
		Hybrid_hoare_post_declContext _localctx = new Hybrid_hoare_post_declContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_hybrid_hoare_post_decl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(104);
			match(KPOST);
			setState(105);
			match(T__6);
			setState(106);
			match(T__7);
			setState(111); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(107);
				discrete_condition();
				setState(109);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(108);
					match(T__9);
					}
				}

				}
				}
				setState(113); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__10 || _la==NOKB );
			setState(115);
			match(SEMI);
			setState(120); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(116);
				hybrid_condition();
				setState(118);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(117);
					match(T__9);
					}
				}

				}
				}
				setState(122); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__11 || _la==NOKB );
			setState(124);
			match(T__8);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Discrete_conditionContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public TerminalNode EQ() { return getToken(IGParser.EQ, 0); }
		public TerminalNode NUM() { return getToken(IGParser.NUM, 0); }
		public TerminalNode NOKB() { return getToken(IGParser.NOKB, 0); }
		public Discrete_conditionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_discrete_condition; }
	}

	public final Discrete_conditionContext discrete_condition() throws RecognitionException {
		Discrete_conditionContext _localctx = new Discrete_conditionContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_discrete_condition);
		try {
			setState(133);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__10:
				enterOuterAlt(_localctx, 1);
				{
				setState(126);
				match(T__10);
				setState(127);
				match(T__4);
				setState(128);
				match(ID);
				setState(129);
				match(T__5);
				setState(130);
				match(EQ);
				setState(131);
				match(NUM);
				}
				break;
			case NOKB:
				enterOuterAlt(_localctx, 2);
				{
				setState(132);
				match(NOKB);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_conditionContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public TerminalNode EQ() { return getToken(IGParser.EQ, 0); }
		public TerminalNode FLOAT() { return getToken(IGParser.FLOAT, 0); }
		public TerminalNode NOKB() { return getToken(IGParser.NOKB, 0); }
		public Hybrid_conditionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_condition; }
	}

	public final Hybrid_conditionContext hybrid_condition() throws RecognitionException {
		Hybrid_conditionContext _localctx = new Hybrid_conditionContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_hybrid_condition);
		try {
			setState(142);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__11:
				enterOuterAlt(_localctx, 1);
				{
				setState(135);
				match(T__11);
				setState(136);
				match(T__4);
				setState(137);
				match(ID);
				setState(138);
				match(T__5);
				setState(139);
				match(EQ);
				setState(140);
				match(FLOAT);
				}
				break;
			case NOKB:
				enterOuterAlt(_localctx, 2);
				{
				setState(141);
				match(NOKB);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_trace_declContext extends ParserRuleContext {
		public TerminalNode KTRACE() { return getToken(IGParser.KTRACE, 0); }
		public List<Hybrid_hoare_traceContext> hybrid_hoare_trace() {
			return getRuleContexts(Hybrid_hoare_traceContext.class);
		}
		public Hybrid_hoare_traceContext hybrid_hoare_trace(int i) {
			return getRuleContext(Hybrid_hoare_traceContext.class,i);
		}
		public List<TerminalNode> SEMI() { return getTokens(IGParser.SEMI); }
		public TerminalNode SEMI(int i) {
			return getToken(IGParser.SEMI, i);
		}
		public Hybrid_hoare_trace_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_trace_decl; }
	}

	public final Hybrid_hoare_trace_declContext hybrid_hoare_trace_decl() throws RecognitionException {
		Hybrid_hoare_trace_declContext _localctx = new Hybrid_hoare_trace_declContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_hybrid_hoare_trace_decl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(144);
			match(KTRACE);
			setState(145);
			match(T__6);
			setState(149); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(146);
				hybrid_hoare_trace();
				setState(147);
				match(SEMI);
				}
				}
				setState(151); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__4 );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_traceContext extends ParserRuleContext {
		public TerminalNode FLOAT() { return getToken(IGParser.FLOAT, 0); }
		public Hybrid_hoare_dpaContext hybrid_hoare_dpa() {
			return getRuleContext(Hybrid_hoare_dpaContext.class,0);
		}
		public List<Hybrid_hoare_slideContext> hybrid_hoare_slide() {
			return getRuleContexts(Hybrid_hoare_slideContext.class);
		}
		public Hybrid_hoare_slideContext hybrid_hoare_slide(int i) {
			return getRuleContext(Hybrid_hoare_slideContext.class,i);
		}
		public List<TerminalNode> AND() { return getTokens(IGParser.AND); }
		public TerminalNode AND(int i) {
			return getToken(IGParser.AND, i);
		}
		public Hybrid_hoare_traceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_trace; }
	}

	public final Hybrid_hoare_traceContext hybrid_hoare_trace() throws RecognitionException {
		Hybrid_hoare_traceContext _localctx = new Hybrid_hoare_traceContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_hybrid_hoare_trace);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(153);
			match(T__4);
			setState(154);
			match(FLOAT);
			setState(155);
			match(T__9);
			setState(160); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(156);
				hybrid_hoare_slide();
				setState(158);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AND) {
					{
					setState(157);
					match(AND);
					}
				}

				}
				}
				setState(162); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << NOKB) | (1L << SLIDE) | (1L << NOSLIDE))) != 0) );
			setState(164);
			match(T__9);
			setState(165);
			hybrid_hoare_dpa();
			setState(166);
			match(T__5);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_dpaContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public TerminalNode OPER() { return getToken(IGParser.OPER, 0); }
		public TerminalNode NOKB() { return getToken(IGParser.NOKB, 0); }
		public Hybrid_hoare_dpaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_dpa; }
	}

	public final Hybrid_hoare_dpaContext hybrid_hoare_dpa() throws RecognitionException {
		Hybrid_hoare_dpaContext _localctx = new Hybrid_hoare_dpaContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_hybrid_hoare_dpa);
		try {
			setState(171);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ID:
				enterOuterAlt(_localctx, 1);
				{
				setState(168);
				match(ID);
				setState(169);
				match(OPER);
				}
				break;
			case NOKB:
				enterOuterAlt(_localctx, 2);
				{
				setState(170);
				match(NOKB);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Hybrid_hoare_slideContext extends ParserRuleContext {
		public TerminalNode SLIDE() { return getToken(IGParser.SLIDE, 0); }
		public TerminalNode ID() { return getToken(IGParser.ID, 0); }
		public TerminalNode OPER() { return getToken(IGParser.OPER, 0); }
		public TerminalNode NOSLIDE() { return getToken(IGParser.NOSLIDE, 0); }
		public TerminalNode NOKB() { return getToken(IGParser.NOKB, 0); }
		public Hybrid_hoare_slideContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_hybrid_hoare_slide; }
	}

	public final Hybrid_hoare_slideContext hybrid_hoare_slide() throws RecognitionException {
		Hybrid_hoare_slideContext _localctx = new Hybrid_hoare_slideContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_hybrid_hoare_slide);
		int _la;
		try {
			setState(188);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case SLIDE:
				enterOuterAlt(_localctx, 1);
				{
				setState(173);
				match(SLIDE);
				setState(175);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OPER) {
					{
					setState(174);
					match(OPER);
					}
				}

				setState(177);
				match(T__4);
				setState(178);
				match(ID);
				setState(179);
				match(T__5);
				}
				break;
			case NOSLIDE:
				enterOuterAlt(_localctx, 2);
				{
				setState(180);
				match(NOSLIDE);
				setState(182);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OPER) {
					{
					setState(181);
					match(OPER);
					}
				}

				setState(184);
				match(T__4);
				setState(185);
				match(ID);
				setState(186);
				match(T__5);
				}
				break;
			case NOKB:
				enterOuterAlt(_localctx, 3);
				{
				setState(187);
				match(NOKB);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 5:
			return reg_expr_sempred((Reg_exprContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean reg_expr_sempred(Reg_exprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 4);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3%\u00c1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\3\2\3"+
		"\2\3\2\5\2\'\n\2\3\2\3\2\3\3\3\3\6\3-\n\3\r\3\16\3.\3\4\3\4\3\4\3\4\3"+
		"\4\3\4\3\4\3\5\3\5\6\5:\n\5\r\5\16\5;\3\6\3\6\3\6\3\6\3\6\3\6\6\6D\n\6"+
		"\r\6\16\6E\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7U\n"+
		"\7\3\7\3\7\3\7\7\7Z\n\7\f\7\16\7]\13\7\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\n"+
		"\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\5\13p\n\13\6\13r\n\13\r\13\16"+
		"\13s\3\13\3\13\3\13\5\13y\n\13\6\13{\n\13\r\13\16\13|\3\13\3\13\3\f\3"+
		"\f\3\f\3\f\3\f\3\f\3\f\5\f\u0088\n\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\5\r\u0091"+
		"\n\r\3\16\3\16\3\16\3\16\3\16\6\16\u0098\n\16\r\16\16\16\u0099\3\17\3"+
		"\17\3\17\3\17\3\17\5\17\u00a1\n\17\6\17\u00a3\n\17\r\17\16\17\u00a4\3"+
		"\17\3\17\3\17\3\17\3\20\3\20\3\20\5\20\u00ae\n\20\3\21\3\21\5\21\u00b2"+
		"\n\21\3\21\3\21\3\21\3\21\3\21\5\21\u00b9\n\21\3\21\3\21\3\21\3\21\5\21"+
		"\u00bf\n\21\3\21\2\3\f\22\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \2\2"+
		"\2\u00c6\2\"\3\2\2\2\4*\3\2\2\2\6\60\3\2\2\2\b\67\3\2\2\2\n=\3\2\2\2\f"+
		"T\3\2\2\2\16^\3\2\2\2\20a\3\2\2\2\22e\3\2\2\2\24j\3\2\2\2\26\u0087\3\2"+
		"\2\2\30\u0090\3\2\2\2\32\u0092\3\2\2\2\34\u009b\3\2\2\2\36\u00ad\3\2\2"+
		"\2 \u00be\3\2\2\2\"#\5\4\3\2#$\5\b\5\2$&\5\16\b\2%\'\7\25\2\2&%\3\2\2"+
		"\2&\'\3\2\2\2\'(\3\2\2\2()\7\3\2\2)\3\3\2\2\2*,\7\17\2\2+-\5\6\4\2,+\3"+
		"\2\2\2-.\3\2\2\2.,\3\2\2\2./\3\2\2\2/\5\3\2\2\2\60\61\7\32\2\2\61\62\7"+
		"\35\2\2\62\63\7\33\2\2\63\64\7\4\2\2\64\65\7\33\2\2\65\66\7\36\2\2\66"+
		"\7\3\2\2\2\679\7\20\2\28:\5\n\6\298\3\2\2\2:;\3\2\2\2;9\3\2\2\2;<\3\2"+
		"\2\2<\t\3\2\2\2=>\7\32\2\2>?\7\5\2\2?@\5\f\7\2@A\7\6\2\2AC\7\"\2\2BD\7"+
		"\32\2\2CB\3\2\2\2DE\3\2\2\2EC\3\2\2\2EF\3\2\2\2FG\3\2\2\2GH\7\36\2\2H"+
		"\13\3\2\2\2IJ\b\7\1\2JK\7\37\2\2KU\5\f\7\7LM\7\7\2\2MN\5\f\7\2NO\7\b\2"+
		"\2OU\3\2\2\2PQ\7\32\2\2QR\7!\2\2RU\7\33\2\2SU\7\32\2\2TI\3\2\2\2TL\3\2"+
		"\2\2TP\3\2\2\2TS\3\2\2\2U[\3\2\2\2VW\f\6\2\2WX\7 \2\2XZ\5\f\7\7YV\3\2"+
		"\2\2Z]\3\2\2\2[Y\3\2\2\2[\\\3\2\2\2\\\r\3\2\2\2][\3\2\2\2^_\7\21\2\2_"+
		"`\5\20\t\2`\17\3\2\2\2ab\5\22\n\2bc\5\32\16\2cd\5\24\13\2d\21\3\2\2\2"+
		"ef\7\22\2\2fg\7\t\2\2gh\7\n\2\2hi\7\13\2\2i\23\3\2\2\2jk\7\24\2\2kl\7"+
		"\t\2\2lq\7\n\2\2mo\5\26\f\2np\7\f\2\2on\3\2\2\2op\3\2\2\2pr\3\2\2\2qm"+
		"\3\2\2\2rs\3\2\2\2sq\3\2\2\2st\3\2\2\2tu\3\2\2\2uz\7\36\2\2vx\5\30\r\2"+
		"wy\7\f\2\2xw\3\2\2\2xy\3\2\2\2y{\3\2\2\2zv\3\2\2\2{|\3\2\2\2|z\3\2\2\2"+
		"|}\3\2\2\2}~\3\2\2\2~\177\7\13\2\2\177\25\3\2\2\2\u0080\u0081\7\r\2\2"+
		"\u0081\u0082\7\7\2\2\u0082\u0083\7\32\2\2\u0083\u0084\7\b\2\2\u0084\u0085"+
		"\7\35\2\2\u0085\u0088\7\33\2\2\u0086\u0088\7\26\2\2\u0087\u0080\3\2\2"+
		"\2\u0087\u0086\3\2\2\2\u0088\27\3\2\2\2\u0089\u008a\7\16\2\2\u008a\u008b"+
		"\7\7\2\2\u008b\u008c\7\32\2\2\u008c\u008d\7\b\2\2\u008d\u008e\7\35\2\2"+
		"\u008e\u0091\7\34\2\2\u008f\u0091\7\26\2\2\u0090\u0089\3\2\2\2\u0090\u008f"+
		"\3\2\2\2\u0091\31\3\2\2\2\u0092\u0093\7\23\2\2\u0093\u0097\7\t\2\2\u0094"+
		"\u0095\5\34\17\2\u0095\u0096\7\36\2\2\u0096\u0098\3\2\2\2\u0097\u0094"+
		"\3\2\2\2\u0098\u0099\3\2\2\2\u0099\u0097\3\2\2\2\u0099\u009a\3\2\2\2\u009a"+
		"\33\3\2\2\2\u009b\u009c\7\7\2\2\u009c\u009d\7\34\2\2\u009d\u00a2\7\f\2"+
		"\2\u009e\u00a0\5 \21\2\u009f\u00a1\7\27\2\2\u00a0\u009f\3\2\2\2\u00a0"+
		"\u00a1\3\2\2\2\u00a1\u00a3\3\2\2\2\u00a2\u009e\3\2\2\2\u00a3\u00a4\3\2"+
		"\2\2\u00a4\u00a2\3\2\2\2\u00a4\u00a5\3\2\2\2\u00a5\u00a6\3\2\2\2\u00a6"+
		"\u00a7\7\f\2\2\u00a7\u00a8\5\36\20\2\u00a8\u00a9\7\b\2\2\u00a9\35\3\2"+
		"\2\2\u00aa\u00ab\7\32\2\2\u00ab\u00ae\7#\2\2\u00ac\u00ae\7\26\2\2\u00ad"+
		"\u00aa\3\2\2\2\u00ad\u00ac\3\2\2\2\u00ae\37\3\2\2\2\u00af\u00b1\7\30\2"+
		"\2\u00b0\u00b2\7#\2\2\u00b1\u00b0\3\2\2\2\u00b1\u00b2\3\2\2\2\u00b2\u00b3"+
		"\3\2\2\2\u00b3\u00b4\7\7\2\2\u00b4\u00b5\7\32\2\2\u00b5\u00bf\7\b\2\2"+
		"\u00b6\u00b8\7\31\2\2\u00b7\u00b9\7#\2\2\u00b8\u00b7\3\2\2\2\u00b8\u00b9"+
		"\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba\u00bb\7\7\2\2\u00bb\u00bc\7\32\2\2"+
		"\u00bc\u00bf\7\b\2\2\u00bd\u00bf\7\26\2\2\u00be\u00af\3\2\2\2\u00be\u00b6"+
		"\3\2\2\2\u00be\u00bd\3\2\2\2\u00bf!\3\2\2\2\25&.;ET[osx|\u0087\u0090\u0099"+
		"\u00a0\u00a4\u00ad\u00b1\u00b8\u00be";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}