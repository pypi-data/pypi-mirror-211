ace.define("ace/mode/scheme_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],(function(e,t,n){"use strict";var i=e("../lib/oop"),r=e("./text_highlight_rules").TextHighlightRules,o=function(){var e=this.createKeywordMapper({"keyword.control":"case|do|let|loop|if|else|when","keyword.operator":"eq?|eqv?|equal?|and|or|not|null?","constant.language":"#t|#f","support.function":"cons|car|cdr|cond|lambda|lambda*|syntax-rules|format|set!|quote|eval|append|list|list?|member?|load"},"identifier",!0);this.$rules={start:[{token:"comment",regex:";.*$"},{token:["storage.type.function-type.scheme","text","entity.name.function.scheme"],regex:"(?:\\b(?:(define|define-syntax|define-macro))\\b)(\\s+)((?:\\w|\\-|\\!|\\?)*)"},{token:"punctuation.definition.constant.character.scheme",regex:"#:\\S+"},{token:["punctuation.definition.variable.scheme","variable.other.global.scheme","punctuation.definition.variable.scheme"],regex:"(\\*)(\\S*)(\\*)"},{token:"constant.numeric",regex:"#[xXoObB][0-9a-fA-F]+"},{token:"constant.numeric",regex:"[+-]?\\d+(?:(?:\\.\\d*)?(?:[eE][+-]?\\d+)?)?"},{token:e,regex:"[a-zA-Z_#][a-zA-Z0-9_\\-\\?\\!\\*]*"},{token:"string",regex:'"(?=.)',next:"qqstring"}],qqstring:[{token:"constant.character.escape.scheme",regex:"\\\\."},{token:"string",regex:'[^"\\\\]+',merge:!0},{token:"string",regex:"\\\\$",next:"qqstring",merge:!0},{token:"string",regex:'"|$',next:"start",merge:!0}]}};i.inherits(o,r),t.SchemeHighlightRules=o})),ace.define("ace/mode/matching_parens_outdent",["require","exports","module","ace/range"],(function(e,t,n){"use strict";var i=e("../range").Range,r=function(){};(function(){this.checkOutdent=function(e,t){return!!/^\s+$/.test(e)&&/^\s*\)/.test(t)},this.autoOutdent=function(e,t){var n=e.getLine(t).match(/^(\s*\))/);if(!n)return 0;var r=n[1].length,o=e.findMatchingBracket({row:t,column:r});if(!o||o.row==t)return 0;var s=this.$getIndent(e.getLine(o.row));e.replace(new i(t,0,t,r-1),s)},this.$getIndent=function(e){var t=e.match(/^(\s+)/);return t?t[1]:""}}).call(r.prototype),t.MatchingParensOutdent=r})),ace.define("ace/mode/scheme",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/scheme_highlight_rules","ace/mode/matching_parens_outdent"],(function(e,t,n){"use strict";var i=e("../lib/oop"),r=e("./text").Mode,o=e("./scheme_highlight_rules").SchemeHighlightRules,s=e("./matching_parens_outdent").MatchingParensOutdent,a=function(){this.HighlightRules=o,this.$outdent=new s,this.$behaviour=this.$defaultBehaviour};i.inherits(a,r),function(){this.lineCommentStart=";",this.minorIndentFunctions=["define","lambda","define-macro","define-syntax","syntax-rules","define-record-type","define-structure"],this.$toIndent=function(e){return e.split("").map((function(e){return/\s/.exec(e)?e:" "})).join("")},this.$calculateIndent=function(e,t){for(var n,i,r=this.$getIndent(e),o=0,s=e.length-1;s>=0&&("("===(i=e[s])?(o--,n=!0):"("===i||"["===i||"{"===i?(o--,n=!1):")"!==i&&"]"!==i&&"}"!==i||o++,!(o<0));s--);if(!(o<0&&n))return o<0&&!n?this.$toIndent(e.substring(0,s+1)):o>0?r=r.substring(0,r.length-t.length):r;for(var a=s+=1,c="";;){if(" "===(i=e[s])||"\t"===i)return-1!==this.minorIndentFunctions.indexOf(c)?this.$toIndent(e.substring(0,a-1)+t):this.$toIndent(e.substring(0,s+1));if(void 0===i)return this.$toIndent(e.substring(0,a-1)+t);c+=e[s],s++}},this.getNextLineIndent=function(e,t,n){return this.$calculateIndent(t,n)},this.checkOutdent=function(e,t,n){return this.$outdent.checkOutdent(t,n)},this.autoOutdent=function(e,t,n){this.$outdent.autoOutdent(t,n)},this.$id="ace/mode/scheme"}.call(a.prototype),t.Mode=a})),ace.require(["ace/mode/scheme"],(function(e){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=e)}));