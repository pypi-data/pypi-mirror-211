ace.define("ace/mode/zeek_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],(function(e,t,o){"use strict";var r=e("../lib/oop"),n=e("./text_highlight_rules").TextHighlightRules,a=function(){this.$rules={start:[{token:"comment.line",regex:"#.*$"},{token:"string.double",regex:/"/,next:"string-state"},{token:"string.regexp",regex:"(/)(?=.*/)",next:"pattern-state"},{token:["keyword.other","meta.preprocessor"],regex:/(@(?:load-plugin|load-sigs|load|unload))(.*$)/},{token:"keyword.other",regex:/@(?:DEBUG|DIR|FILENAME|deprecated|if|ifdef|ifndef|else|endif)/},{token:["keyword.other","meta.preprocessor","keyword.operator","meta.preprocessor"],regex:/(@prefixes)(\s*)(\+?=)(.*$)/},{token:"storage.modifier.attribute",regex:/\&\b(?:redef|priority|log|optional|default|add_func|delete_func|expire_func|read_expire|write_expire|create_expire|synchronized|persistent|rotate_interval|rotate_size|encrypt|raw_output|mergeable|error_handler|type_column|deprecated)\b/},{token:"constant.language",regex:/\b(?:T|F)\b/},{token:"constant.numeric.port",regex:/\b\d{1,5}\/(?:udp|tcp|icmp|unknown)\b/},{token:"constant.numeric.addr",regex:/\b(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\b/,comment:"IPv4 address"},{token:"constant.numeric.addr",regex:/\[(?:[0-9a-fA-F]{0,4}:){2,7}(?:[0-9a-fA-F]{0,4})?(?:(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{1,2}))?\]/,comment:"IPv6 address"},{token:"constant.numeric.float.decimal.interval",regex:/(?:(?:\d*\.\d*(?:[eE][+-]?\d+)?|\d*[eE][+-]?\d+|\d*\.\d*)|\d+)\s*(?:day|hr|min|msec|usec|sec)s?/},{token:"constant.numeric.float.decimal",regex:/\d*\.\d*(?:[eE][+-]?\d+)?|\d*[eE][+-]?\d+|\d*\.\d*/},{token:"constant.numeric.hostname",regex:/\b[A-Za-z0-9][A-Za-z0-9\-]*(?:\.[A-Za-z0-9][A-Za-z0-9\-]*)+\b/},{token:"constant.numeric.integer.hexadecimal",regex:/\b0x[0-9a-fA-F]+\b/},{token:"constant.numeric.integer.decimal",regex:/\b\d+\b/},{token:"keyword.operator",regex:/==|!=|<=|<|>=|>/},{token:"keyword.operator",regex:/(&&)|(\|\|)|(!)/},{token:"keyword.operator",regex:/=|\+=|-=/},{token:"keyword.operator",regex:/\+\+|\+|--|-|\*|\/|%/},{token:"keyword.operator",regex:/&|\||\^|~/},{token:"keyword.operator",regex:/\b(?:in|as|is)\b/},{token:"punctuation.terminator",regex:/;/},{token:"punctuation.accessor",regex:/\??\$/},{token:"punctuation.accessor",regex:/::/},{token:"keyword.operator",regex:/\?/},{token:"punctuation.separator",regex:/:/},{token:"punctuation.separator",regex:/,/},{token:["keyword.other","meta.namespace","entity.name.namespace"],regex:/(module)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)/},{token:"keyword.other",regex:/\bexport\b/},{token:"keyword.control.conditional",regex:/\b(?:if|else)\b/},{token:"keyword.control",regex:/\b(?:for|while)\b/},{token:"keyword.control",regex:/\b(?:return|break|next|continue|fallthrough)\b/},{token:"keyword.control",regex:/\b(?:switch|default|case)\b/},{token:"keyword.other",regex:/\b(?:add|delete)\b/},{token:"keyword.other",regex:/\bprint\b/},{token:"keyword.control",regex:/\b(?:when|timeout|schedule)\b/},{token:["keyword.other","meta.struct.record","entity.name.struct.record","meta.struct.record","punctuation.separator","meta.struct.record","storage.type.struct.record"],regex:/\b(type)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)(\s*)(:)(\s*\b)(record)\b/},{token:["keyword.other","meta.enum","entity.name.enum","meta.enum","punctuation.separator","meta.enum","storage.type.enum"],regex:/\b(type)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)(\s*)(:)(\s*\b)(enum)\b/},{token:["keyword.other","meta.type","entity.name.type","meta.type","punctuation.separator"],regex:/\b(type)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)(\s*)(:)/},{token:["keyword.other","meta.struct.record","storage.type.struct.record","meta.struct.record","entity.name.struct.record"],regex:/\b(redef)(\s+)(record)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)\b/},{token:["keyword.other","meta.enum","storage.type.enum","meta.enum","entity.name.enum"],regex:/\b(redef)(\s+)(enum)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)\b/},{token:["storage.type","text","entity.name.function.event"],regex:/\b(event)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)(?=s*\()/},{token:["storage.type","text","entity.name.function.hook"],regex:/\b(hook)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)(?=s*\()/},{token:["storage.type","text","entity.name.function"],regex:/\b(function)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)(?=s*\()/},{token:"keyword.other",regex:/\bredef\b/},{token:"storage.type",regex:/\bany\b/},{token:"storage.type",regex:/\b(?:enum|record|set|table|vector)\b/},{token:["storage.type","text","keyword.operator","text","storage.type"],regex:/\b(opaque)(\s+)(of)(\s+)([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)\b/},{token:"keyword.operator",regex:/\bof\b/},{token:"storage.type",regex:/\b(?:addr|bool|count|double|file|int|interval|pattern|port|string|subnet|time)\b/},{token:"storage.type",regex:/\b(?:function|hook|event)\b/},{token:"storage.modifier",regex:/\b(?:global|local|const|option)\b/},{token:"entity.name.function.call",regex:/\b[A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*(?=s*\()/},{token:"punctuation.section.block.begin",regex:/\{/},{token:"punctuation.section.block.end",regex:/\}/},{token:"punctuation.section.brackets.begin",regex:/\[/},{token:"punctuation.section.brackets.end",regex:/\]/},{token:"punctuation.section.parens.begin",regex:/\(/},{token:"punctuation.section.parens.end",regex:/\)/}],"string-state":[{token:"constant.character.escape",regex:/\\./},{token:"string.double",regex:/"/,next:"start"},{token:"constant.other.placeholder",regex:/%-?[0-9]*(\.[0-9]+)?[DTdxsefg]/},{token:"string.double",regex:"."}],"pattern-state":[{token:"constant.character.escape",regex:/\\./},{token:"string.regexp",regex:"/",next:"start"},{token:"string.regexp",regex:"."}]},this.normalizeRules()};a.metaData={fileTypes:["bro","zeek"],name:"Zeek",scopeName:"source.zeek"},r.inherits(a,n),t.ZeekHighlightRules=a})),ace.define("ace/mode/folding/cstyle",["require","exports","module","ace/lib/oop","ace/range","ace/mode/folding/fold_mode"],(function(e,t,o){"use strict";var r=e("../../lib/oop"),n=e("../../range").Range,a=e("./fold_mode").FoldMode,i=t.FoldMode=function(e){e&&(this.foldingStartMarker=new RegExp(this.foldingStartMarker.source.replace(/\|[^|]*?$/,"|"+e.start)),this.foldingStopMarker=new RegExp(this.foldingStopMarker.source.replace(/\|[^|]*?$/,"|"+e.end)))};r.inherits(i,a),function(){this.foldingStartMarker=/([\{\[\(])[^\}\]\)]*$|^\s*(\/\*)/,this.foldingStopMarker=/^[^\[\{\(]*([\}\]\)])|^[\s\*]*(\*\/)/,this.singleLineBlockCommentRe=/^\s*(\/\*).*\*\/\s*$/,this.tripleStarBlockCommentRe=/^\s*(\/\*\*\*).*\*\/\s*$/,this.startRegionRe=/^\s*(\/\*|\/\/)#?region\b/,this._getFoldWidgetBase=this.getFoldWidget,this.getFoldWidget=function(e,t,o){var r=e.getLine(o);if(this.singleLineBlockCommentRe.test(r)&&!this.startRegionRe.test(r)&&!this.tripleStarBlockCommentRe.test(r))return"";var n=this._getFoldWidgetBase(e,t,o);return!n&&this.startRegionRe.test(r)?"start":n},this.getFoldWidgetRange=function(e,t,o,r){var n,a=e.getLine(o);if(this.startRegionRe.test(a))return this.getCommentRegionBlock(e,a,o);if(n=a.match(this.foldingStartMarker)){var i=n.index;if(n[1])return this.openingBracketBlock(e,n[1],o,i);var s=e.getCommentFoldRange(o,i+n[0].length,1);return s&&!s.isMultiLine()&&(r?s=this.getSectionRange(e,o):"all"!=t&&(s=null)),s}if("markbegin"!==t&&(n=a.match(this.foldingStopMarker))){i=n.index+n[0].length;return n[1]?this.closingBracketBlock(e,n[1],o,i):e.getCommentFoldRange(o,i,-1)}},this.getSectionRange=function(e,t){for(var o=e.getLine(t),r=o.search(/\S/),a=t,i=o.length,s=t+=1,g=e.getLength();++t<g;){var c=(o=e.getLine(t)).search(/\S/);if(-1!==c){if(r>c)break;var d=this.getFoldWidgetRange(e,"all",t);if(d){if(d.start.row<=a)break;if(d.isMultiLine())t=d.end.row;else if(r==c)break}s=t}}return new n(a,i,s,e.getLine(s).length)},this.getCommentRegionBlock=function(e,t,o){for(var r=t.search(/\s*$/),a=e.getLength(),i=o,s=/^\s*(?:\/\*|\/\/|--)#?(end)?region\b/,g=1;++o<a;){t=e.getLine(o);var c=s.exec(t);if(c&&(c[1]?g--:g++,!g))break}if(o>i)return new n(i,r,o,t.length)}}.call(i.prototype)})),ace.define("ace/mode/zeek",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/zeek_highlight_rules","ace/mode/folding/cstyle"],(function(e,t,o){"use strict";var r=e("../lib/oop"),n=e("./text").Mode,a=e("./zeek_highlight_rules").ZeekHighlightRules,i=e("./folding/cstyle").FoldMode,s=function(){this.HighlightRules=a,this.foldingRules=new i};r.inherits(s,n),function(){this.lineCommentStart="#",this.$id="ace/mode/zeek"}.call(s.prototype),t.Mode=s})),ace.require(["ace/mode/zeek"],(function(e){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=e)}));