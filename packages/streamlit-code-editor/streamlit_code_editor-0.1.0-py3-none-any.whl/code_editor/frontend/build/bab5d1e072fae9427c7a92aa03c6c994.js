ace.define("ace/theme/dreamweaver.css",["require","exports","module"],(function(e,a,r){r.exports='.ace-dreamweaver .ace_gutter {\n  background: #e8e8e8;\n  color: #333;\n}\n\n.ace-dreamweaver .ace_print-margin {\n  width: 1px;\n  background: #e8e8e8;\n}\n\n.ace-dreamweaver {\n  background-color: #FFFFFF;\n  color: black;\n}\n\n.ace-dreamweaver .ace_fold {\n    background-color: #757AD8;\n}\n\n.ace-dreamweaver .ace_cursor {\n  color: black;\n}\n        \n.ace-dreamweaver .ace_invisible {\n  color: rgb(191, 191, 191);\n}\n\n.ace-dreamweaver .ace_storage,\n.ace-dreamweaver .ace_keyword {\n  color: blue;\n}\n\n.ace-dreamweaver .ace_constant.ace_buildin {\n  color: rgb(88, 72, 246);\n}\n\n.ace-dreamweaver .ace_constant.ace_language {\n  color: rgb(88, 92, 246);\n}\n\n.ace-dreamweaver .ace_constant.ace_library {\n  color: rgb(6, 150, 14);\n}\n\n.ace-dreamweaver .ace_invalid {\n  background-color: rgb(153, 0, 0);\n  color: white;\n}\n\n.ace-dreamweaver .ace_support.ace_function {\n  color: rgb(60, 76, 114);\n}\n\n.ace-dreamweaver .ace_support.ace_constant {\n  color: rgb(6, 150, 14);\n}\n\n.ace-dreamweaver .ace_support.ace_type,\n.ace-dreamweaver .ace_support.ace_class {\n  color: #009;\n}\n\n.ace-dreamweaver .ace_support.ace_php_tag {\n  color: #f00;\n}\n\n.ace-dreamweaver .ace_keyword.ace_operator {\n  color: rgb(104, 118, 135);\n}\n\n.ace-dreamweaver .ace_string {\n  color: #00F;\n}\n\n.ace-dreamweaver .ace_comment {\n  color: rgb(76, 136, 107);\n}\n\n.ace-dreamweaver .ace_comment.ace_doc {\n  color: rgb(0, 102, 255);\n}\n\n.ace-dreamweaver .ace_comment.ace_doc.ace_tag {\n  color: rgb(128, 159, 191);\n}\n\n.ace-dreamweaver .ace_constant.ace_numeric {\n  color: rgb(0, 0, 205);\n}\n\n.ace-dreamweaver .ace_variable {\n  color: #06F\n}\n\n.ace-dreamweaver .ace_xml-pe {\n  color: rgb(104, 104, 91);\n}\n\n.ace-dreamweaver .ace_entity.ace_name.ace_function {\n  color: #00F;\n}\n\n\n.ace-dreamweaver .ace_heading {\n  color: rgb(12, 7, 255);\n}\n\n.ace-dreamweaver .ace_list {\n  color:rgb(185, 6, 144);\n}\n\n.ace-dreamweaver .ace_marker-layer .ace_selection {\n  background: rgb(181, 213, 255);\n}\n\n.ace-dreamweaver .ace_marker-layer .ace_step {\n  background: rgb(252, 255, 0);\n}\n\n.ace-dreamweaver .ace_marker-layer .ace_stack {\n  background: rgb(164, 229, 101);\n}\n\n.ace-dreamweaver .ace_marker-layer .ace_bracket {\n  margin: -1px 0 0 -1px;\n  border: 1px solid rgb(192, 192, 192);\n}\n\n.ace-dreamweaver .ace_marker-layer .ace_active-line {\n  background: rgba(0, 0, 0, 0.07);\n}\n\n.ace-dreamweaver .ace_gutter-active-line {\n  background-color : #DCDCDC;\n}\n\n.ace-dreamweaver .ace_marker-layer .ace_selected-word {\n  background: rgb(250, 250, 255);\n  border: 1px solid rgb(200, 200, 250);\n}\n\n.ace-dreamweaver .ace_meta.ace_tag {\n  color:#009;\n}\n\n.ace-dreamweaver .ace_meta.ace_tag.ace_anchor {\n  color:#060;\n}\n\n.ace-dreamweaver .ace_meta.ace_tag.ace_form {\n  color:#F90;\n}\n\n.ace-dreamweaver .ace_meta.ace_tag.ace_image {\n  color:#909;\n}\n\n.ace-dreamweaver .ace_meta.ace_tag.ace_script {\n  color:#900;\n}\n\n.ace-dreamweaver .ace_meta.ace_tag.ace_style {\n  color:#909;\n}\n\n.ace-dreamweaver .ace_meta.ace_tag.ace_table {\n  color:#099;\n}\n\n.ace-dreamweaver .ace_string.ace_regex {\n  color: rgb(255, 0, 0)\n}\n\n.ace-dreamweaver .ace_indent-guide {\n  background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAE0lEQVQImWP4////f4bLly//BwAmVgd1/w11/gAAAABJRU5ErkJggg==") right repeat-y;\n}\n\n.ace-dreamweaver .ace_indent-guide-active {\n  background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAZSURBVHjaYvj///9/hivKyv8BAAAA//8DACLqBhbvk+/eAAAAAElFTkSuQmCC") right repeat-y;\n} \n'})),ace.define("ace/theme/dreamweaver",["require","exports","module","ace/theme/dreamweaver.css","ace/lib/dom"],(function(e,a,r){a.isDark=!1,a.cssClass="ace-dreamweaver",a.cssText=e("./dreamweaver.css"),e("../lib/dom").importCssString(a.cssText,a.cssClass,!1)})),ace.require(["ace/theme/dreamweaver"],(function(e){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=e)}));