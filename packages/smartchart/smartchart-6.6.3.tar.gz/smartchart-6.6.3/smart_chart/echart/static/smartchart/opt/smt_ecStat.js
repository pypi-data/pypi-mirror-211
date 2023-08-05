var smt_ecStat;!function(n,r){"object"==typeof exports&&"object"==typeof module?module.exports=r():"function"==typeof define&&define.amd?define([],r):"object"==typeof exports?exports.ecStat=r():n.ecStat=r()}(this,function(){return function(n){function r(e){if(t[e])return t[e].exports;var o=t[e]={exports:{},id:e,loaded:!1};return n[e].call(o.exports,o,o.exports,r),o.loaded=!0,o.exports}var t={};return r.m=n,r.c=t,r.p="",r(0)}([function(n,r,t){var e;e=function(n){return{clustering:t(6),regression:t(8),statistics:t(15),histogram:t(7),transform:{regression:t(19),histogram:t(18),clustering:t(17)}}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){return n=null===n?NaN:+n,"number"==typeof n&&!isNaN(n)}function t(n){return isFinite(n)&&n===Math.round(n)}function e(n){if(0===n)return 0;var r=Math.floor(Math.log(n)/Math.LN10);return n/Math.pow(10,r)>=10&&r++,r}return{isNumber:r,isInteger:t,quantityExponent:e}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){for(var r=[];t(n);)r.push(n.length),n=n[0];return r}function t(n){return"[object Array]"===l.call(n)}function e(n,r){for(var t=[],e=0;e<n;e++){t[e]=[];for(var o=0;o<r;o++)t[e][o]=0}return t}function o(n){for(var r=0,t=0;t<n.length;t++)r+=n[t];return r}function i(n,r){for(var t=0,e=0;e<n.length;e++)t+=n[e][r];return t}function a(n,r){return n>r?1:n<r?-1:n===r?0:NaN}function u(n,r,t,e){for(null==t&&(t=0),null==e&&(e=n.length);t<e;){var o=Math.floor((t+e)/2),i=a(n[o],r);if(i>0)e=o;else{if(!(i<0))return o+1;t=o+1}}return t}function s(n,r,t){if(n&&r){if(n.map&&n.map===c)return n.map(r,t);for(var e=[],o=0,i=n.length;o<i;o++)e.push(r.call(t,n[o],o,n));return e}}var l=Object.prototype.toString,f=Array.prototype,c=f.map;return{size:r,isArray:t,zeros:e,sum:o,sumOfColumn:i,ascending:a,bisect:u,map:s}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n,r){return"number"==typeof n?[n]:null==n?r:n}function e(n,r){function t(n){return!e||o.hasOwnProperty(n)}r=r||{};var e=r.dimensions,o={};if(null!=e)for(var i=0;i<e.length;i++)o[e[i]]=!0;var s=r.toOneDimensionArray?e?e[0]:0:null;if(!a(n))throw new Error("Invalid data type, you should input an array");var f=[],c=u(n);if(1===c.length)for(var i=0;i<c[0];i++){var v=n[i];l(v)&&f.push(v)}else if(2===c.length)for(var i=0;i<c[0];i++){for(var h=!0,v=n[i],p=0;p<c[1];p++)t(p)&&!l(v[p])&&(h=!1);h&&f.push(null!=s?v[s]:v)}return f}function o(n){var r=n.toString(),t=r.indexOf(".");return t<0?0:r.length-1-t}var i=t(2),a=i.isArray,u=i.size,s=t(1),l=s.isNumber;return{normalizeDimensions:r,dataPreprocess:e,getPrecision:o}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){return function(n,r){var t=n.length;if(!t)return 0;if(r<=0||t<2)return n[0];if(r>=1)return n[t-1];var e=(t-1)*r,o=Math.floor(e),i=n[o],a=n[o+1];return i+(a-i)*(e-o)}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n,r){function t(n,r){if(!n)throw new Error("Can not find dimension by "+r)}if(null!=r){var e=n.upstream;if(o.isArray(r)){for(var i=[],a=0;a<r.length;a++){var u=e.getDimensionInfo(r[a]);t(u,r[a]),i[a]=u.index}return i}var u=e.getDimensionInfo(r);return t(u,r),u.index}}function e(n){function r(n){if(i.isNumber(n))return{index:n};if(a.isObject(n)&&i.isNumber(n.index))return n;throw new Error("Illegle new dimensions config. Expect `{ name: string, index: number }`.")}if(o.isArray(n)){for(var t=[],e=[],u=0;u<n.length;u++){var s=r(n[u]);t.push(s.name),e.push(s.index)}return{name:t,index:e}}if(null!=n)return r(n)}var o=t(2),i=t(1),a=t(20);return{normalizeExistingDimensions:r,normalizeNewDimensions:e}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n,r,t){for(var o,i,s,f,c=x(n.length,2),v=a(r,l(n,t.dimensions)),h=!0;h;){h=!1;for(var p=0;p<n.length;p++){o=1/0,i=-1;for(var d=0;d<r;d++)s=u(n[p],v[d],t),s<o&&(o=s,i=d);c[p][0]!==i&&(h=!0),c[p][0]=i,c[p][1]=o}for(var p=0;p<r;p++){f=[];for(var d=0;d<c.length;d++)c[d][0]===p&&f.push(n[d]);v[p]=e(f,t)}}var m={centroids:v,clusterAssigned:c};return m}function e(n,r){for(var t,e,o=[],i=0;i<r.dimensions.length;i++){var a=r.dimensions[i];t=0;for(var u=0;u<n.length;u++)t+=n[u][a];e=t/n.length,o.push(e)}return o}function o(n,t,o){function a(n,r){N[n][1]=r}function l(n){return N[n][1]}function f(){if(F<h){S=1/0;for(var n,t,e,o=0;o<O.length;o++){q=[],P=[];for(var i=0;i<E.length;i++)y(i)===o?q.push(E[i]):P.push(l(i));L=r(q,2,b),T=m(L.clusterAssigned,1),j=g(P),T+j<S&&(S=j+T,n=o,t=L.centroids,e=L.clusterAssigned)}for(var i=0;i<e.length;i++)0===e[i][0]?e[i][0]=n:1===e[i][0]&&(e[i][0]=O.length);O[n]=t[0],O.push(t[1]);for(var i=0,o=0;i<E.length&&o<e.length;i++)y(i)===n&&(d(i,e[o][0]),a(i,e[o++][1]));var u=[];if(!D){for(var i=0;i<O.length;i++){u[i]=[];for(var o=0;o<E.length;o++)y(o)===i&&u[i].push(E[o])}V.pointsInCluster=u}F++}else V.isEnd=!0}var v=(M(t)?{clusterCount:t,stepByStep:o}:t)||{clusterCount:2},h=v.clusterCount;if(!(h<2)){var p,d,y,b=s(n,v),D=b.outputType===w.SINGLE,E=c(n,{dimensions:b.dimensions}),N=x(E.length,2);if(D){p=[];var C=b.outputClusterIndexDimension;d=function(n,r){p[n][C]=r},y=function(n){return p[n][C]};for(var I=0;I<E.length;I++)p.push(E[I].slice()),a(I,0),d(I,0)}else d=function(n,r){N[n][0]=r},y=function(n){return N[n][0]};for(var A=e(E,b),O=[A],I=0;I<E.length;I++){var z=u(E[I],A,b);a(I,z)}var S,q,P,L,T,j,F=1,V={data:p,centroids:O,isEnd:!1};if(D||(V.clusterAssment=N),v.stepByStep)V.next=function(){return f(),i(V,b),V};else for(;f(),!V.isEnd;);return i(V,b),V}}function i(n,r){var t=r.outputCentroidDimensions;if(r.outputType===w.SINGLE&&null!=t)for(var e=n.data,o=n.centroids,i=0;i<e.length;i++)for(var a=e[i],u=a[r.outputClusterIndexDimension],s=o[u],l=Math.min(s.length,t.length),f=0;f<l;f++)a[t[f]]=s[f]}function a(n,r){for(var t=x(n,r.length),e=0;e<r.length;e++)for(var o=r[e],i=0;i<n;i++)t[i][e]=o.min+o.span*Math.random();return t}function u(n,r,t){for(var e=0,o=t.dimensions,i=t.rawExtents,a=0;a<o.length;a++){var u=i[a].span;if(u){var s=o[a],l=(n[s]-r[a])/u;e+=y(l,2)}}return e}function s(n,r){var t=d(n);if(t.length<1)throw new Error("The input data of clustering should be two-dimension array.");for(var e=t[1],o=[],i=0;i<e;i++)o.push(i);var a=v(r.dimensions,o),u=r.outputType||w.MULTIPLE,s=r.outputClusterIndexDimension;if(u===w.SINGLE&&!p.isNumber(s))throw new Error("outputClusterIndexDimension is required as a number.");var f=l(n,a);return{dimensions:a,rawExtents:f,outputType:u,outputClusterIndexDimension:s,outputCentroidDimensions:r.outputCentroidDimensions}}function l(n,r){for(var t=[],e=r.length,o=0;o<e;o++)t.push({min:1/0,max:-(1/0)});for(var o=0;o<n.length;o++)for(var i=n[o],a=0;a<e;a++){var u=t[a],s=i[r[a]];u.min>s&&(u.min=s),u.max<s&&(u.max=s)}for(var o=0;o<e;o++)t[o].span=t[o].max-t[o].min;return t}var f=t(3),c=f.dataPreprocess,v=f.normalizeDimensions,h=t(2),p=t(1),d=h.size,m=h.sumOfColumn,g=h.sum,x=h.zeros,p=t(1),M=p.isNumber,y=Math.pow,w={SINGLE:"single",MULTIPLE:"multiple"};return{OutputType:w,hierarchicalKMeans:o}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n,r){for(var t="string"==typeof r?{method:r}:r||{},i=null==t.method?m.squareRoot:m[t.method],a=l(t.dimensions),u=s(n,{dimensions:a,toOneDimensionArray:!0}),f=e(u),c=o(u),g=i(u,c,f),x=d(c,f,g),M=x.step,y=x.toFixedPrecision,w=h(+(Math.ceil(c/M)*M).toFixed(y),+(Math.floor(f/M)*M).toFixed(y),M,y),b=w.length,D=new Array(b+1),E=0;E<=b;E++)D[E]={},D[E].sample=[],D[E].x0=E>0?w[E-1]:w[E]-c===M?c:w[E]-M,D[E].x1=E<b?w[E]:f-w[E-1]===M?f:w[E-1]+M;for(var E=0;E<u.length;E++)c<=u[E]&&u[E]<=f&&D[p(w,u[E],0,b)].sample.push(u[E]);var n=v(D,function(n){return[+((n.x0+n.x1)/2).toFixed(y),n.sample.length,n.x0,n.x1,n.x0+" - "+n.x1]}),N=v(D,function(n){return[n.x0,n.x1,n.sample.length]});return{bins:D,data:n,customData:N}}var e=t(10),o=t(12),i=t(4),a=t(9),u=t(3),s=u.dataPreprocess,l=u.normalizeDimensions,f=t(2),c=f.ascending,v=f.map,h=t(21),p=f.bisect,d=t(22),m={squareRoot:function(n){var r=Math.ceil(Math.sqrt(n.length));return r>50?50:r},scott:function(n,r,t){return Math.ceil((t-r)/(3.5*a(n)*Math.pow(n.length,-1/3)))},freedmanDiaconis:function(n,r,t){return n.sort(c),Math.ceil((t-r)/(2*(i(n,.75)-i(n,.25))*Math.pow(n.length,-1/3)))},sturges:function(n){return Math.ceil(Math.log(n.length)/Math.LN2)+1}};return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n,r){for(var t=0;t<n.length-1;t++){for(var e=t,o=t+1;o<n.length-1;o++)Math.abs(n[t][o])>Math.abs(n[t][e])&&(e=o);for(var i=t;i<n.length;i++){var a=n[i][t];n[i][t]=n[i][e],n[i][e]=a}for(var u=t+1;u<n.length-1;u++)for(var s=n.length-1;s>=t;s--)n[s][u]-=n[s][t]/n[t][t]*n[t][u]}for(var l=new Array(r),f=n.length-1,o=n.length-2;o>=0;o--){for(var a=0,t=o+1;t<n.length-1;t++)a+=n[t][o]*l[t];l[o]=(n[f][o]-a)/n[o][o]}return l}var e=t(3),o=e.dataPreprocess,i=e.normalizeDimensions,a={linear:function(n,r){for(var t=r.dimensions[0],e=r.dimensions[1],o=0,i=0,a=0,u=0,s=n.length,l=0;l<s;l++){var f=n[l];o+=f[t],i+=f[e],a+=f[t]*f[e],u+=f[t]*f[t]}for(var c=(s*a-o*i)/(s*u-o*o),v=i/s-c*o/s,h=[],p=0;p<n.length;p++){var f=n[p],d=f.slice();d[t]=f[t],d[e]=c*f[t]+v,h.push(d)}var m="y = "+Math.round(100*c)/100+"x + "+Math.round(100*v)/100;return{points:h,parameter:{gradient:c,intercept:v},expression:m}},linearThroughOrigin:function(n,r){for(var t=r.dimensions[0],e=r.dimensions[1],o=0,i=0,a=0;a<n.length;a++){var u=n[a];o+=u[t]*u[t],i+=u[t]*u[e]}for(var s=i/o,l=[],f=0;f<n.length;f++){var u=n[f],c=u.slice();c[t]=u[t],c[e]=u[t]*s,l.push(c)}var v="y = "+Math.round(100*s)/100+"x";return{points:l,parameter:{gradient:s},expression:v}},exponential:function(n,r){for(var t=r.dimensions[0],e=r.dimensions[1],o=0,i=0,a=0,u=0,s=0,l=0,f=0;f<n.length;f++){var c=n[f];o+=c[t],i+=c[e],l+=c[t]*c[e],a+=c[t]*c[t]*c[e],u+=c[e]*Math.log(c[e]),s+=c[t]*c[e]*Math.log(c[e])}for(var v=i*a-l*l,h=Math.pow(Math.E,(a*u-l*s)/v),p=(i*s-l*u)/v,d=[],m=0;m<n.length;m++){var c=n[m],g=c.slice();g[t]=c[t],g[e]=h*Math.pow(Math.E,p*c[t]),d.push(g)}var x="y = "+Math.round(100*h)/100+"e^("+Math.round(100*p)/100+"x)";return{points:d,parameter:{coefficient:h,index:p},expression:x}},logarithmic:function(n,r){for(var t=r.dimensions[0],e=r.dimensions[1],o=0,i=0,a=0,u=0,s=0;s<n.length;s++){var l=n[s];o+=Math.log(l[t]),i+=l[e]*Math.log(l[t]),a+=l[e],u+=Math.pow(Math.log(l[t]),2)}for(var f=(s*i-a*o)/(s*u-o*o),c=(a-f*o)/s,v=[],h=0;h<n.length;h++){var l=n[h],p=l.slice();p[t]=l[t],p[e]=f*Math.log(l[t])+c,v.push(p)}var d="y = "+Math.round(100*c)/100+" + "+Math.round(100*f)/100+"ln(x)";return{points:v,parameter:{gradient:f,intercept:c},expression:d}},polynomial:function(n,t){var e=t.dimensions[0],o=t.dimensions[1],i=t.order;null==i&&(i=2);for(var a=[],u=[],s=i+1,l=0;l<s;l++){for(var f=0,c=0;c<n.length;c++){var v=n[c];f+=v[o]*Math.pow(v[e],l)}u.push(f);for(var h=[],p=0;p<s;p++){for(var d=0,m=0;m<n.length;m++)d+=Math.pow(n[m][e],l+p);h.push(d)}a.push(h)}a.push(u);for(var g=r(a,s),x=[],l=0;l<n.length;l++){for(var M=0,v=n[l],c=0;c<g.length;c++)M+=g[c]*Math.pow(v[e],c);var y=v.slice();y[e]=v[e],y[o]=M,x.push(y)}for(var w="y = ",l=g.length-1;l>=0;l--)w+=l>1?Math.round(g[l]*Math.pow(10,l+1))/Math.pow(10,l+1)+"x^"+l+" + ":1===l?Math.round(100*g[l])/100+"x + ":Math.round(100*g[l])/100;return{points:x,parameter:g,expression:w}}},u=function(n,r,t){var e="number"==typeof t?{order:t}:t||{},u=i(e.dimensions,[0,1]),s=o(r,{dimensions:u}),l=a[n](s,{order:e.order,dimensions:u}),f=u[0];return l.points.sort(function(n,r){return n[f]-r[f]}),l};return u}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r=t(13);return function(n){var t=r(n);return t?Math.sqrt(t):t}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){for(var r=-(1/0),t=0;t<n.length;t++)o(n[t])&&n[t]>r&&(r=n[t]);return r}var e=t(1),o=e.isNumber;return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){var r=n.length;return r?e(n)/n.length:0}var e=t(14);return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){for(var r=1/0,t=0;t<n.length;t++)o(n[t])&&n[t]<r&&(r=n[t]);return r}var e=t(1),o=e.isNumber;return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){var r=n.length;if(!r||r<2)return 0;if(n.length>=2){for(var t,e=i(n),a=0,u=0;u<n.length;u++)o(n[u])&&(t=n[u]-e,a+=t*t);return a/(n.length-1)}}var e=t(1),o=e.isNumber,i=t(11);return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){var r=n.length;if(!r)return 0;for(var t=0,e=0;e<r;e++)o(n[e])&&(t+=n[e]);return t}var e=t(1),o=e.isNumber;return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r={};return r.max=t(10),r.deviation=t(9),r.mean=t(11),r.median=t(16),r.min=t(12),r.quantile=t(4),r.sampleVariance=t(13),r.sum=t(14),r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n){return e(n,.5)}var e=t(4);return r}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r=t(6),e=t(1),o=t(5),i=e.isNumber;return{type:"ecStat:clustering",transform:function(n){var t=n.upstream,e=n.config||{},a=e.clusterCount;if(!i(a)||a<=0)throw new Error('config param "clusterCount" need to be specified as an interger greater than 1.');if(1===a)return[{},{data:[]}];var u=o.normalizeNewDimensions(e.outputClusterIndexDimension),s=o.normalizeNewDimensions(e.outputCentroidDimensions);if(null==u)throw new Error("outputClusterIndexDimension is required as a number.");for(var l=r.hierarchicalKMeans(t.cloneRawData(),{clusterCount:a,stepByStep:!1,dimensions:o.normalizeExistingDimensions(n,e.dimensions),outputType:r.OutputType.SINGLE,outputClusterIndexDimension:u.index,outputCentroidDimensions:(s||{}).index}),f=t.cloneAllDimensionInfo(),c=[],v=0;v<f.length;v++){var h=f[v];c.push(h.name)}if(c[u.index]=u.name,s)for(var v=0;v<s.index.length;v++)null!=s.name[v]&&(c[s.index[v]]=s.name[v]);return[{dimensions:c,data:l.data},{data:l.centroids}]}}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r=t(7),e=t(5);return{type:"ecStat:histogram",transform:function(n){var t=n.upstream,o=n.config||{},i=r(t.cloneRawData(),{method:o.method,dimensions:e.normalizeExistingDimensions(n,o.dimensions)});return[{dimensions:["MeanOfV0V1","VCount","V0","V1","DisplayableName"],data:i.data},{data:i.customData}]}}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r=t(8),e=t(5),o=2;return{type:"ecStat:regression",transform:function(n){var t=n.upstream,i=n.config||{},a=i.method||"linear",u=r(a,t.cloneRawData(),{order:i.order,dimensions:e.normalizeExistingDimensions(n,i.dimensions)}),s=u.points,l=i.formulaOn;null==l&&(l="end");var f;if("none"!==l){for(var c=0;c<s.length;c++)s[c][o]="start"===l&&0===c||"all"===l||"end"===l&&c===s.length-1?u.expression:"";f=t.cloneAllDimensionInfo(),f[o]={}}return[{dimensions:f,data:s}]}}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){function r(n,r){if(Object.assign)Object.assign(n,r);else for(var t in r)r.hasOwnProperty(t)&&(n[t]=r[t]);return n}function t(n){const r=typeof n;return"function"===r||!!n&&"object"===r}return{extend:r,isObject:t}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r=t(3),e=r.getPrecision;return function(n,r,t,o){var i=arguments.length;i<2?(r=n,n=0,t=1):i<3?t=1:i<4?(t=+t,o=e(t)):o=+o;for(var a=Math.ceil(((r-n)/t).toFixed(o)),u=new Array(a+1),s=0;s<a+1;s++)u[s]=+(n+s*t).toFixed(o);return u}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))},function(n,r,t){var e;e=function(n){var r=t(1);return function(n,t,e){var o=Math.abs(t-n)/e,i=r.quantityExponent(o),a=Math.pow(10,i),u=o/a;u>=Math.sqrt(50)?a*=10:u>=Math.sqrt(10)?a*=5:u>=Math.sqrt(2)&&(a*=2);var s=i<0?-i:0,l=+(t>=n?a:-a).toFixed(s);return{step:l,toFixedPrecision:s}}}.call(r,t,r,n),!(void 0!==e&&(n.exports=e))}])});