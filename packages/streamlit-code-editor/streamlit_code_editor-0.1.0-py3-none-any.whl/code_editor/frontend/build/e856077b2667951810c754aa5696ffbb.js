ace.define("ace/snippets/php.snippets",["require","exports","module"],(function(n,t,e){e.exports="snippet ec\n\techo ${1};\nsnippet ns\n\tnamespace ${1:Foo\\Bar\\Baz};\n\t${2}\nsnippet use\n\tuse ${1:Foo\\Bar\\Baz};\n\t${2}\nsnippet c\n\t${1:abstract }class ${2:$FILENAME}\n\t{\n\t\t${3}\n\t}\nsnippet i\n\tinterface ${1:$FILENAME}\n\t{\n\t\t${2}\n\t}\nsnippet t.\n\t$this->${1}\nsnippet f\n\tfunction ${1:foo}(${2:array }${3:$bar})\n\t{\n\t\t${4}\n\t}\n# method\nsnippet m\n\t${1:abstract }${2:protected}${3: static} function ${4:foo}(${5:array }${6:$bar})\n\t{\n\t\t${7}\n\t}\n# setter method\nsnippet sm\n\t/**\n\t * Sets the value of ${1:foo}\n\t *\n\t * @param ${2:$1} $$1 ${3:description}\n\t *\n\t * @return ${4:$FILENAME}\n\t */\n\t${5:public} function set${6:$2}(${7:$2 }$$1)\n\t{\n\t\t$this->${8:$1} = $$1;\n\t\treturn $this;\n\t}${9}\n# getter method\nsnippet gm\n\t/**\n\t * Gets the value of ${1:foo}\n\t *\n\t * @return ${2:$1}\n\t */\n\t${3:public} function get${4:$2}()\n\t{\n\t\treturn $this->${5:$1};\n\t}${6}\n#setter\nsnippet $s\n\t${1:$foo}->set${2:Bar}(${3});\n#getter\nsnippet $g\n\t${1:$foo}->get${2:Bar}();\n\n# Tertiary conditional\nsnippet =?:\n\t$${1:foo} = ${2:true} ? ${3:a} : ${4};\nsnippet ?:\n\t${1:true} ? ${2:a} : ${3}\n\nsnippet C\n\t$_COOKIE['${1:variable}']${2}\nsnippet E\n\t$_ENV['${1:variable}']${2}\nsnippet F\n\t$_FILES['${1:variable}']${2}\nsnippet G\n\t$_GET['${1:variable}']${2}\nsnippet P\n\t$_POST['${1:variable}']${2}\nsnippet R\n\t$_REQUEST['${1:variable}']${2}\nsnippet S\n\t$_SERVER['${1:variable}']${2}\nsnippet SS\n\t$_SESSION['${1:variable}']${2}\n\n# the following are old ones\nsnippet inc\n\tinclude '${1:file}';${2}\nsnippet inc1\n\tinclude_once '${1:file}';${2}\nsnippet req\n\trequire '${1:file}';${2}\nsnippet req1\n\trequire_once '${1:file}';${2}\n# Start Docblock\nsnippet /*\n\t/**\n\t * ${1}\n\t */\n# Class - post doc\nsnippet doc_cp\n\t/**\n\t * ${1:undocumented class}\n\t *\n\t * @package ${2:default}\n\t * @subpackage ${3:default}\n\t * @author ${4:`g:snips_author`}\n\t */${5}\n# Class Variable - post doc\nsnippet doc_vp\n\t/**\n\t * ${1:undocumented class variable}\n\t *\n\t * @var ${2:string}\n\t */${3}\n# Class Variable\nsnippet doc_v\n\t/**\n\t * ${3:undocumented class variable}\n\t *\n\t * @var ${4:string}\n\t */\n\t${1:var} $${2};${5}\n# Class\nsnippet doc_c\n\t/**\n\t * ${3:undocumented class}\n\t *\n\t * @package ${4:default}\n\t * @subpackage ${5:default}\n\t * @author ${6:`g:snips_author`}\n\t */\n\t${1:}class ${2:}\n\t{\n\t\t${7}\n\t} // END $1class $2\n# Constant Definition - post doc\nsnippet doc_dp\n\t/**\n\t * ${1:undocumented constant}\n\t */${2}\n# Constant Definition\nsnippet doc_d\n\t/**\n\t * ${3:undocumented constant}\n\t */\n\tdefine(${1}, ${2});${4}\n# Function - post doc\nsnippet doc_fp\n\t/**\n\t * ${1:undocumented function}\n\t *\n\t * @return ${2:void}\n\t * @author ${3:`g:snips_author`}\n\t */${4}\n# Function signature\nsnippet doc_s\n\t/**\n\t * ${4:undocumented function}\n\t *\n\t * @return ${5:void}\n\t * @author ${6:`g:snips_author`}\n\t */\n\t${1}function ${2}(${3});${7}\n# Function\nsnippet doc_f\n\t/**\n\t * ${4:undocumented function}\n\t *\n\t * @return ${5:void}\n\t * @author ${6:`g:snips_author`}\n\t */\n\t${1}function ${2}(${3})\n\t{${7}\n\t}\n# Header\nsnippet doc_h\n\t/**\n\t * ${1}\n\t *\n\t * @author ${2:`g:snips_author`}\n\t * @version ${3:$Id$}\n\t * @copyright ${4:$2}, `strftime('%d %B, %Y')`\n\t * @package ${5:default}\n\t */\n\n# Interface\nsnippet interface\n\t/**\n\t * ${2:undocumented class}\n\t *\n\t * @package ${3:default}\n\t * @author ${4:`g:snips_author`}\n\t */\n\tinterface ${1:$FILENAME}\n\t{\n\t\t${5}\n\t}\n# class ...\nsnippet class\n\t/**\n\t * ${1}\n\t */\n\tclass ${2:$FILENAME}\n\t{\n\t\t${3}\n\t\t/**\n\t\t * ${4}\n\t\t */\n\t\t${5:public} function ${6:__construct}(${7:argument})\n\t\t{\n\t\t\t${8:// code...}\n\t\t}\n\t}\n# define(...)\nsnippet def\n\tdefine('${1}'${2});${3}\n# defined(...)\nsnippet def?\n\t${1}defined('${2}')${3}\nsnippet wh\n\twhile (${1:/* condition */}) {\n\t\t${2:// code...}\n\t}\n# do ... while\nsnippet do\n\tdo {\n\t\t${2:// code... }\n\t} while (${1:/* condition */});\nsnippet if\n\tif (${1:/* condition */}) {\n\t\t${2:// code...}\n\t}\nsnippet ife\n\tif (${1:/* condition */}) {\n\t\t${2:// code...}\n\t} else {\n\t\t${3:// code...}\n\t}\n\t${4}\nsnippet else\n\telse {\n\t\t${1:// code...}\n\t}\nsnippet elseif\n\telseif (${1:/* condition */}) {\n\t\t${2:// code...}\n\t}\nsnippet switch\n\tswitch ($${1:variable}) {\n\t\tcase '${2:value}':\n\t\t\t${3:// code...}\n\t\t\tbreak;\n\t\t${5}\n\t\tdefault:\n\t\t\t${4:// code...}\n\t\t\tbreak;\n\t}\nsnippet case\n\tcase '${1:value}':\n\t\t${2:// code...}\n\t\tbreak;${3}\nsnippet for\n\tfor ($${2:i} = 0; $$2 < ${1:count}; $$2${3:++}) {\n\t\t${4: // code...}\n\t}\nsnippet foreach\n\tforeach ($${1:variable} as $${2:value}) {\n\t\t${3:// code...}\n\t}\nsnippet foreachk\n\tforeach ($${1:variable} as $${2:key} => $${3:value}) {\n\t\t${4:// code...}\n\t}\n# $... = array (...)\nsnippet array\n\t$${1:arrayName} = array('${2}' => ${3});${4}\nsnippet try\n\ttry {\n\t\t${2}\n\t} catch (${1:Exception} $e) {\n\t}\n# lambda with closure\nsnippet lambda\n\t${1:static }function (${2:args}) use (${3:&$x, $y /*put vars in scope (closure) */}) {\n\t\t${4}\n\t};\n# pre_dump();\nsnippet pd\n\techo '<pre>'; var_dump(${1}); echo '</pre>';\n# pre_dump(); die();\nsnippet pdd\n\techo '<pre>'; var_dump(${1}); echo '</pre>'; die(${2:});\nsnippet vd\n\tvar_dump(${1});\nsnippet vdd\n\tvar_dump(${1}); die(${2:});\nsnippet http_redirect\n\theader (\"HTTP/1.1 301 Moved Permanently\");\n\theader (\"Location: \".URL);\n\texit();\n# Getters & Setters\nsnippet gs\n\t/**\n\t * Gets the value of ${1:foo}\n\t *\n\t * @return ${2:$1}\n\t */\n\tpublic function get${3:$2}()\n\t{\n\t\treturn $this->${4:$1};\n\t}\n\n\t/**\n\t * Sets the value of $1\n\t *\n\t * @param $2 $$1 ${5:description}\n\t *\n\t * @return ${6:$FILENAME}\n\t */\n\tpublic function set$3(${7:$2 }$$1)\n\t{\n\t\t$this->$4 = $$1;\n\t\treturn $this;\n\t}${8}\n# anotation, get, and set, useful for doctrine\nsnippet ags\n\t/**\n\t * ${1:description}\n\t *\n\t * @${7}\n\t */\n\t${2:protected} $${3:foo};\n\n\tpublic function get${4:$3}()\n\t{\n\t\treturn $this->$3;\n\t}\n\n\tpublic function set$4(${5:$4 }$${6:$3})\n\t{\n\t\t$this->$3 = $$6;\n\t\treturn $this;\n\t}\nsnippet rett\n\treturn true;\nsnippet retf\n\treturn false;\nscope html\nsnippet <?\n\t<?php\n\n\t${1}\nsnippet <?e\n\t<?php echo ${1} ?>\n# this one is for php5.4\nsnippet <?=\n\t<?=${1}?>\nsnippet ifil\n\t<?php if (${1:/* condition */}): ?>\n\t\t${2:\x3c!-- code... --\x3e}\n\t<?php endif; ?>\nsnippet ifeil\n\t<?php if (${1:/* condition */}): ?>\n\t\t${2:\x3c!-- html... --\x3e}\n\t<?php else: ?>\n\t\t${3:\x3c!-- html... --\x3e}\n\t<?php endif; ?>\n\t${4}\nsnippet foreachil\n\t<?php foreach ($${1:variable} as $${2:value}): ?>\n\t\t${3:\x3c!-- html... --\x3e}\n\t<?php endforeach; ?>\nsnippet foreachkil\n\t<?php foreach ($${1:variable} as $${2:key} => $${3:value}): ?>\n\t\t${4:\x3c!-- html... --\x3e}\n\t<?php endforeach; ?>\nscope html-tag\nsnippet ifil\\n\\\n\t<?php if (${1:true}): ?>${2:code}<?php endif; ?>\nsnippet ifeil\\n\\\n\t<?php if (${1:true}): ?>${2:code}<?php else: ?>${3:code}<?php endif; ?>${4}\n"})),ace.define("ace/snippets/php",["require","exports","module","ace/snippets/php.snippets"],(function(n,t,e){"use strict";t.snippetText=n("./php.snippets"),t.scope="php"})),ace.require(["ace/snippets/php"],(function(n){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=n)}));