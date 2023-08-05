ace.define("ace/ext/elastic_tabstops_lite",["require","exports","module","ace/editor","ace/config"],(function(t,e,s){"use strict";var i=function(t){this.$editor=t;var e=this,s=[],i=!1;this.onAfterExec=function(){i=!1,e.processRows(s),s=[]},this.onExec=function(){i=!0},this.onChange=function(t){i&&(-1==s.indexOf(t.start.row)&&s.push(t.start.row),t.end.row!=t.start.row&&s.push(t.end.row))}};(function(){this.processRows=function(t){this.$inChange=!0;for(var e=[],s=0,i=t.length;s<i;s++){var o=t[s];if(!(e.indexOf(o)>-1))for(var n=this.$findCellWidthsForBlock(o),r=this.$setBlockCellWidthsToMax(n.cellWidths),h=n.firstRow,a=0,c=r.length;a<c;a++){var l=r[a];e.push(h),this.$adjustRow(h,l),h++}}this.$inChange=!1},this.$findCellWidthsForBlock=function(t){for(var e,s=[],i=t;i>=0&&0!=(e=this.$cellWidthsForRow(i)).length;)s.unshift(e),i--;var o=i+1;i=t;for(var n=this.$editor.session.getLength();i<n-1&&(i++,0!=(e=this.$cellWidthsForRow(i)).length);)s.push(e);return{cellWidths:s,firstRow:o}},this.$cellWidthsForRow=function(t){for(var e=this.$selectionColumnsForRow(t),s=[-1].concat(this.$tabsForRow(t)),i=s.map((function(t){return 0})).slice(1),o=this.$editor.session.getLine(t),n=0,r=s.length-1;n<r;n++){var h=s[n]+1,a=s[n+1],c=this.$rightmostSelectionInCell(e,a),l=o.substring(h,a);i[n]=Math.max(l.replace(/\s+$/g,"").length,c-h)}return i},this.$selectionColumnsForRow=function(t){var e=[],s=this.$editor.getCursorPosition();return this.$editor.session.getSelection().isEmpty()&&t==s.row&&e.push(s.column),e},this.$setBlockCellWidthsToMax=function(t){for(var e,s,i,o=!0,n=this.$izip_longest(t),r=0,h=n.length;r<h;r++){var a=n[r];if(a.push){a.push(NaN);for(var c=0,l=a.length;c<l;c++){var u=a[c];if(o&&(e=c,i=0,o=!1),isNaN(u)){s=c;for(var f=e;f<s;f++)t[f][r]=i;o=!0}i=Math.max(i,u)}}else console.error(a)}return t},this.$rightmostSelectionInCell=function(t,e){var s=0;if(t.length){for(var i=[],o=0,n=t.length;o<n;o++)t[o]<=e?i.push(o):i.push(0);s=Math.max.apply(Math,i)}return s},this.$tabsForRow=function(t){for(var e,s=[],i=this.$editor.session.getLine(t),o=/\t/g;null!=(e=o.exec(i));)s.push(e.index);return s},this.$adjustRow=function(t,e){var s=this.$tabsForRow(t);if(0!=s.length)for(var i=0,o=-1,n=this.$izip(e,s),r=0,h=n.length;r<h;r++){var a=n[r][0],c=n[r][1],l=(o+=1+a)-(c+=i);if(0!=l){var u=this.$editor.session.getLine(t).substr(0,c),f=u.replace(/\s*$/g,""),p=u.length-f.length;l>0&&(this.$editor.session.getDocument().insertInLine({row:t,column:c+1},Array(l+1).join(" ")+"\t"),this.$editor.session.getDocument().removeInLine(t,c,c+1),i+=l),l<0&&p>=-l&&(this.$editor.session.getDocument().removeInLine(t,c+l,c),i+=l)}}},this.$izip_longest=function(t){if(!t[0])return[];for(var e=t[0].length,s=t.length,i=1;i<s;i++){var o=t[i].length;o>e&&(e=o)}for(var n=[],r=0;r<e;r++){var h=[];for(i=0;i<s;i++)""===t[i][r]?h.push(NaN):h.push(t[i][r]);n.push(h)}return n},this.$izip=function(t,e){for(var s=t.length>=e.length?e.length:t.length,i=[],o=0;o<s;o++){var n=[t[o],e[o]];i.push(n)}return i}}).call(i.prototype),e.ElasticTabstopsLite=i;var o=t("../editor").Editor;t("../config").defineOptions(o.prototype,"editor",{useElasticTabstops:{set:function(t){t?(this.elasticTabstops||(this.elasticTabstops=new i(this)),this.commands.on("afterExec",this.elasticTabstops.onAfterExec),this.commands.on("exec",this.elasticTabstops.onExec),this.on("change",this.elasticTabstops.onChange)):this.elasticTabstops&&(this.commands.removeListener("afterExec",this.elasticTabstops.onAfterExec),this.commands.removeListener("exec",this.elasticTabstops.onExec),this.removeListener("change",this.elasticTabstops.onChange))}}})})),ace.require(["ace/ext/elastic_tabstops_lite"],(function(t){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=t)}));