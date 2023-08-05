ace.define("ace/ext/textarea",["require","exports","module","ace/lib/event","ace/lib/useragent","ace/lib/net","ace/ace"],(function(e,t,i){"use strict";var n=e("../lib/event"),o=e("../lib/useragent"),r=(e("../lib/net"),e("../ace"));i.exports=t=r;var a=function(e,t,i){var n=e.style[i];return n||(n=window.getComputedStyle?window.getComputedStyle(e,"").getPropertyValue(i):e.currentStyle[i]),n&&"auto"!=n&&"intrinsic"!=n||(n=t.style[i]),n};function s(e,t){for(var i in t)e.style[i]=t[i]}t.transformTextarea=function(e,i){var l,c=e.autofocus||document.activeElement==e,u=function(e,t){if("textarea"!=e.type)throw new Error("Textarea required!");var i=e.parentNode,o=document.createElement("div"),r=function(){var t="position:relative;";["margin-top","margin-left","margin-right","margin-bottom"].forEach((function(i){t+=i+":"+a(e,o,i)+";"}));var i=a(e,o,"width")||e.clientWidth+"px",n=a(e,o,"height")||e.clientHeight+"px";t+="height:"+n+";width:"+i+";",t+="display:inline-block;",o.setAttribute("style",t)};for(n.addListener(window,"resize",r),r(),i.insertBefore(o,e.nextSibling);i!==document;){if("FORM"===i.tagName.toUpperCase()){var s=i.onsubmit;i.onsubmit=function(i){e.value=t(),s&&s.call(this,i)};break}i=i.parentNode}return o}(e,(function(){return l.getValue()}));e.style.display="none",u.style.background="white";var d=document.createElement("div");s(d,{top:"0px",left:"0px",right:"0px",bottom:"0px",border:"1px solid gray",position:"absolute"}),u.appendChild(d);var p=document.createElement("div");s(p,{position:"absolute",right:"0px",bottom:"0px",cursor:"nw-resize",border:"solid 9px",borderColor:"lightblue gray gray #ceade6",zIndex:101});var h=document.createElement("div"),f={top:"0px",left:"20%",right:"0px",bottom:"0px",position:"absolute",padding:"5px",zIndex:100,color:"white",display:"none",overflow:"auto",fontSize:"14px",boxShadow:"-5px 2px 3px gray"};o.isOldIE?f.backgroundColor="#333":f.backgroundColor="rgba(0, 0, 0, 0.6)",s(h,f),u.appendChild(h),i=i||t.defaultOptions;var m=r.edit(d);(l=m.getSession()).setValue(e.value||e.innerHTML),c&&m.focus(),u.appendChild(p),function(e,t,i,n,o){e.getSession(),e.renderer;function r(e){return"true"===e||1==e}e.setDisplaySettings=function(t){null==t&&(t="none"==i.style.display),t?(i.style.display="block",i.hideButton.focus(),e.on("focus",(function t(){e.removeListener("focus",t),i.style.display="none"}))):e.focus()},e.$setOption=e.setOption,e.$getOption=e.getOption,e.setOption=function(t,i){switch(t){case"mode":e.$setOption("mode","ace/mode/"+i);break;case"theme":e.$setOption("theme","ace/theme/"+i);break;case"keybindings":switch(i){case"vim":e.setKeyboardHandler("ace/keyboard/vim");break;case"emacs":e.setKeyboardHandler("ace/keyboard/emacs");break;default:e.setKeyboardHandler(null)}break;case"wrap":case"fontSize":e.$setOption(t,i);break;default:e.$setOption(t,r(i))}},e.getOption=function(t){switch(t){case"mode":return e.$getOption("mode").substr("ace/mode/".length);case"theme":return e.$getOption("theme").substr("ace/theme/".length);case"keybindings":var i=e.getKeyboardHandler();switch(i&&i.$id){case"ace/keyboard/vim":return"vim";case"ace/keyboard/emacs":return"emacs";default:return"ace"}break;default:return e.$getOption(t)}},e.setOptions(o)}(m,0,h,0,i),function(e,i,o){var r=null,a={mode:"Mode:",wrap:"Soft Wrap:",theme:"Theme:",fontSize:"Font Size:",showGutter:"Display Gutter:",keybindings:"Keyboard",showPrintMargin:"Show Print Margin:",useSoftTabs:"Use Soft Tabs:",showInvisibles:"Show Invisibles"},s={mode:{text:"Plain",javascript:"JavaScript",xml:"XML",html:"HTML",css:"CSS",scss:"SCSS",python:"Python",php:"PHP",java:"Java",ruby:"Ruby",c_cpp:"C/C++",coffee:"CoffeeScript",json:"json",perl:"Perl",clojure:"Clojure",ocaml:"OCaml",csharp:"C#",haxe:"haXe",svg:"SVG",textile:"Textile",groovy:"Groovy",liquid:"Liquid",Scala:"Scala"},theme:{clouds:"Clouds",clouds_midnight:"Clouds Midnight",cobalt:"Cobalt",crimson_editor:"Crimson Editor",dawn:"Dawn",gob:"Green on Black",eclipse:"Eclipse",idle_fingers:"Idle Fingers",kr_theme:"Kr Theme",merbivore:"Merbivore",merbivore_soft:"Merbivore Soft",mono_industrial:"Mono Industrial",monokai:"Monokai",pastel_on_dark:"Pastel On Dark",solarized_dark:"Solarized Dark",solarized_light:"Solarized Light",textmate:"Textmate",twilight:"Twilight",vibrant_ink:"Vibrant Ink"},showGutter:r,fontSize:{"10px":"10px","11px":"11px","12px":"12px","14px":"14px","16px":"16px"},wrap:{off:"Off",40:"40",80:"80",free:"Free"},keybindings:{ace:"ace",vim:"vim",emacs:"emacs"},showPrintMargin:r,useSoftTabs:r,showInvisibles:r},l=[];function c(e,t,i,n){if(i){for(var o in e.push("<select title='"+t+"'>"),i)e.push("<option value='"+o+"' "),n==o&&e.push(" selected "),e.push(">",i[o],"</option>");e.push("</select>")}else e.push("<input type='checkbox' title='",t,"' ",n+""=="true"?"checked='true'":"","'></input>")}for(var u in l.push("<table><tr><th>Setting</th><th>Value</th></tr>"),t.defaultOptions)l.push("<tr><td>",a[u],"</td>"),l.push("<td>"),c(l,u,s[u],o.getOption(u)),l.push("</td></tr>");l.push("</table>"),e.innerHTML=l.join("");for(var d=function(e){var t=e.currentTarget;o.setOption(t.title,t.value)},p=function(e){var t=e.currentTarget;o.setOption(t.title,t.checked)},h=e.getElementsByTagName("select"),f=0;f<h.length;f++)h[f].onchange=d;var m=e.getElementsByTagName("input");for(f=0;f<m.length;f++)m[f].onclick=p;var g=document.createElement("input");g.type="button",g.value="Hide",n.addListener(g,"click",(function(){o.setDisplaySettings(!1)})),e.appendChild(g),e.hideButton=g}(h,0,m);var g="";return n.addListener(p,"mousemove",(function(e){var t=this.getBoundingClientRect();e.clientX-t.left+(e.clientY-t.top)<(t.width+t.height)/2?(this.style.cursor="pointer",g="toggle"):(g="resize",this.style.cursor="nw-resize")})),n.addListener(p,"mousedown",(function(e){if(e.preventDefault(),"toggle"!=g){u.style.zIndex=1e5;var t=u.getBoundingClientRect(),i=t.width+t.left-e.clientX,o=t.height+t.top-e.clientY;n.capture(p,(function(e){u.style.width=e.clientX-t.left+i+"px",u.style.height=e.clientY-t.top+o+"px",m.resize()}),(function(){}))}else m.setDisplaySettings()})),m},t.defaultOptions={mode:"javascript",theme:"textmate",wrap:"off",fontSize:"12px",showGutter:"false",keybindings:"ace",showPrintMargin:"false",useSoftTabs:"true",showInvisibles:"false"}})),ace.require(["ace/ext/textarea"],(function(e){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=e)}));