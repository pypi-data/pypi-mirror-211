ace.define("ace/mode/latex_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],(function(e,t,r){"use strict";var a=e("../lib/oop"),n=e("./text_highlight_rules").TextHighlightRules,o=function(){this.$rules={start:[{token:"comment",regex:"%.*$"},{token:["keyword","lparen","variable.parameter","rparen","lparen","storage.type","rparen"],regex:"(\\\\(?:documentclass|usepackage|input))(?:(\\[)([^\\]]*)(\\]))?({)([^}]*)(})"},{token:["keyword","lparen","variable.parameter","rparen"],regex:"(\\\\(?:label|v?ref|cite(?:[^{]*)))(?:({)([^}]*)(}))?"},{token:["storage.type","lparen","variable.parameter","rparen"],regex:"(\\\\begin)({)(verbatim)(})",next:"verbatim"},{token:["storage.type","lparen","variable.parameter","rparen"],regex:"(\\\\begin)({)(lstlisting)(})",next:"lstlisting"},{token:["storage.type","lparen","variable.parameter","rparen"],regex:"(\\\\(?:begin|end))({)([\\w*]*)(})"},{token:"storage.type",regex:/\\verb\b\*?/,next:[{token:["keyword.operator","string","keyword.operator"],regex:"(.)(.*?)(\\1|$)|",next:"start"}]},{token:"storage.type",regex:"\\\\[a-zA-Z]+"},{token:"lparen",regex:"[[({]"},{token:"rparen",regex:"[\\])}]"},{token:"constant.character.escape",regex:"\\\\[^a-zA-Z]?"},{token:"string",regex:"\\${1,2}",next:"equation"}],equation:[{token:"comment",regex:"%.*$"},{token:"string",regex:"\\${1,2}",next:"start"},{token:"constant.character.escape",regex:"\\\\(?:[^a-zA-Z]|[a-zA-Z]+)"},{token:"error",regex:"^\\s*$",next:"start"},{defaultToken:"string"}],verbatim:[{token:["storage.type","lparen","variable.parameter","rparen"],regex:"(\\\\end)({)(verbatim)(})",next:"start"},{defaultToken:"text"}],lstlisting:[{token:["storage.type","lparen","variable.parameter","rparen"],regex:"(\\\\end)({)(lstlisting)(})",next:"start"},{defaultToken:"text"}]},this.normalizeRules()};a.inherits(o,n),t.LatexHighlightRules=o})),ace.define("ace/mode/folding/latex",["require","exports","module","ace/lib/oop","ace/mode/folding/fold_mode","ace/range","ace/token_iterator"],(function(e,t,r){"use strict";var a=e("../../lib/oop"),n=e("./fold_mode").FoldMode,o=e("../../range").Range,i=e("../../token_iterator").TokenIterator,l={"\\subparagraph":1,"\\paragraph":2,"\\subsubsubsection":3,"\\subsubsection":4,"\\subsection":5,"\\section":6,"\\chapter":7,"\\part":8,"\\begin":9,"\\end":10},s=t.FoldMode=function(){};a.inherits(s,n),function(){this.foldingStartMarker=/^\s*\\(begin)|\s*\\(part|chapter|(?:sub)*(?:section|paragraph))\b|{\s*$/,this.foldingStopMarker=/^\s*\\(end)\b|^\s*}/,this.getFoldWidgetRange=function(e,t,r){var a,n=e.doc.getLine(r);return(a=this.foldingStartMarker.exec(n))?a[1]?this.latexBlock(e,r,a[0].length-1):a[2]?this.latexSection(e,r,a[0].length-1):this.openingBracketBlock(e,"{",r,a.index):(a=this.foldingStopMarker.exec(n))?a[1]?this.latexBlock(e,r,a[0].length-1):this.closingBracketBlock(e,"}",r,a.index+a[0].length):void 0},this.latexBlock=function(e,t,r,a){var n={"\\begin":1,"\\end":-1},l=new i(e,t,r),s=l.getCurrentToken();if(s&&("storage.type"==s.type||"constant.character.escape"==s.type)){var g=n[s.value],c=function(){var e="lparen"==l.stepForward().type?l.stepForward().value:"";return-1===g&&(l.stepBackward(),e&&l.stepBackward()),e},p=[c()],u=-1===g?l.getCurrentTokenColumn():e.getLine(t).length,d=t;for(l.step=-1===g?l.stepBackward:l.stepForward;s=l.step();)if(s&&("storage.type"==s.type||"constant.character.escape"==s.type)){var h=n[s.value];if(h){var x=c();if(h===g)p.unshift(x);else if(p.shift()!==x||!p.length)break}}if(!p.length){if(1==g&&(l.stepBackward(),l.stepBackward()),a)return l.getCurrentTokenRange();t=l.getCurrentTokenRow();return-1===g?new o(t,e.getLine(t).length,d,u):new o(d,u,t,l.getCurrentTokenColumn())}}},this.latexSection=function(e,t,r){var a=new i(e,t,r),n=a.getCurrentToken();if(n&&"storage.type"==n.type){for(var s=l[n.value]||0,g=0,c=t;n=a.stepForward();)if("storage.type"===n.type){var p=l[n.value]||0;if(p>=9){if(g||(c=a.getCurrentTokenRow()-1),(g+=9==p?1:-1)<0)break}else if(p>=s)break}for(g||(c=a.getCurrentTokenRow()-1);c>t&&!/\S/.test(e.getLine(c));)c--;return new o(t,e.getLine(t).length,c,e.getLine(c).length)}}}.call(s.prototype)})),ace.define("ace/mode/latex",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/latex_highlight_rules","ace/mode/behaviour/cstyle","ace/mode/folding/latex"],(function(e,t,r){"use strict";var a=e("../lib/oop"),n=e("./text").Mode,o=e("./latex_highlight_rules").LatexHighlightRules,i=e("./behaviour/cstyle").CstyleBehaviour,l=e("./folding/latex").FoldMode,s=function(){this.HighlightRules=o,this.foldingRules=new l,this.$behaviour=new i({braces:!0})};a.inherits(s,n),function(){this.type="text",this.lineCommentStart="%",this.$id="ace/mode/latex",this.getMatching=function(e,t,r){void 0==t&&(t=e.selection.lead),"object"==typeof t&&(r=t.column,t=t.row);var a=e.getTokenAt(t,r);if(a)return"\\begin"==a.value||"\\end"==a.value?this.foldingRules.latexBlock(e,t,r,!0):void 0}}.call(s.prototype),t.Mode=s})),ace.require(["ace/mode/latex"],(function(e){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=e)}));