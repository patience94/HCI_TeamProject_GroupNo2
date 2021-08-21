(this["webpackJsonptool-library"]=this["webpackJsonptool-library"]||[]).push([[49,59],{1668:function(t,e,n){"use strict";n.r(e),n.d(e,"getRendererCreator",(function(){return c})),n.d(e,"forceSoftwareRendering",(function(){return h}));var i,r=n(22),o=n.n(r),s=n(1667),a=n(1669),u={getMaterial:function(t){return new s.z({color:t,flatShading:!1,reflectivity:.8,side:s.g})},makeRenderer:function(){return new a.a}},l={getMaterial:function(t){return new s.z({color:t,flatShading:!1,reflectivity:.8,side:s.g})},makeRenderer:function(){return new s.O({antialias:!0})}},c=function(){if(void 0===i){o()(!0,"Call forceSoftwareRendering()");var t=document.createElement("canvas"),e=t.getContext("webgl");null===e&&(e=t.getContext("experimental-webgl"));var n=null!==e&&e instanceof WebGLRenderingContext;t.remove(),i=n?l:u}return i},h=function(){i=u}},1671:function(t,e,n){},1672:function(t,e,n){},1748:function(t,e,n){"use strict";n.r(e);var i=n(57),r=n(0),o=n(1667),s=function(){var t=/^[og]\s*(.+)?/,e=/^mtllib /,n=/^usemtl /;function i(){var t={objects:[],object:{},vertices:[],normals:[],colors:[],uvs:[],materialLibraries:[],startObject:function(t,e){if(this.object&&!1===this.object.fromDeclaration)return this.object.name=t,void(this.object.fromDeclaration=!1!==e);var n=this.object&&"function"===typeof this.object.currentMaterial?this.object.currentMaterial():void 0;if(this.object&&"function"===typeof this.object._finalize&&this.object._finalize(!0),this.object={name:t||"",fromDeclaration:!1!==e,geometry:{vertices:[],normals:[],colors:[],uvs:[]},materials:[],smooth:!0,startMaterial:function(t,e){var n=this._finalize(!1);n&&(n.inherited||n.groupCount<=0)&&this.materials.splice(n.index,1);var i={index:this.materials.length,name:t||"",mtllib:Array.isArray(e)&&e.length>0?e[e.length-1]:"",smooth:void 0!==n?n.smooth:this.smooth,groupStart:void 0!==n?n.groupEnd:0,groupEnd:-1,groupCount:-1,inherited:!1,clone:function(t){var e={index:"number"===typeof t?t:this.index,name:this.name,mtllib:this.mtllib,smooth:this.smooth,groupStart:0,groupEnd:-1,groupCount:-1,inherited:!1};return e.clone=this.clone.bind(e),e}};return this.materials.push(i),i},currentMaterial:function(){if(this.materials.length>0)return this.materials[this.materials.length-1]},_finalize:function(t){var e=this.currentMaterial();if(e&&-1===e.groupEnd&&(e.groupEnd=this.geometry.vertices.length/3,e.groupCount=e.groupEnd-e.groupStart,e.inherited=!1),t&&this.materials.length>1)for(var n=this.materials.length-1;n>=0;n--)this.materials[n].groupCount<=0&&this.materials.splice(n,1);return t&&0===this.materials.length&&this.materials.push({name:"",smooth:this.smooth}),e}},n&&n.name&&"function"===typeof n.clone){var i=n.clone(0);i.inherited=!0,this.object.materials.push(i)}this.objects.push(this.object)},finalize:function(){this.object&&"function"===typeof this.object._finalize&&this.object._finalize(!0)},parseVertexIndex:function(t,e){var n=parseInt(t,10);return 3*(n>=0?n-1:n+e/3)},parseNormalIndex:function(t,e){var n=parseInt(t,10);return 3*(n>=0?n-1:n+e/3)},parseUVIndex:function(t,e){var n=parseInt(t,10);return 2*(n>=0?n-1:n+e/2)},addVertex:function(t,e,n){var i=this.vertices,r=this.object.geometry.vertices;r.push(i[t+0],i[t+1],i[t+2]),r.push(i[e+0],i[e+1],i[e+2]),r.push(i[n+0],i[n+1],i[n+2])},addVertexPoint:function(t){var e=this.vertices;this.object.geometry.vertices.push(e[t+0],e[t+1],e[t+2])},addVertexLine:function(t){var e=this.vertices;this.object.geometry.vertices.push(e[t+0],e[t+1],e[t+2])},addNormal:function(t,e,n){var i=this.normals,r=this.object.geometry.normals;r.push(i[t+0],i[t+1],i[t+2]),r.push(i[e+0],i[e+1],i[e+2]),r.push(i[n+0],i[n+1],i[n+2])},addColor:function(t,e,n){var i=this.colors,r=this.object.geometry.colors;r.push(i[t+0],i[t+1],i[t+2]),r.push(i[e+0],i[e+1],i[e+2]),r.push(i[n+0],i[n+1],i[n+2])},addUV:function(t,e,n){var i=this.uvs,r=this.object.geometry.uvs;r.push(i[t+0],i[t+1]),r.push(i[e+0],i[e+1]),r.push(i[n+0],i[n+1])},addUVLine:function(t){var e=this.uvs;this.object.geometry.uvs.push(e[t+0],e[t+1])},addFace:function(t,e,n,i,r,o,s,a,u){var l=this.vertices.length,c=this.parseVertexIndex(t,l),h=this.parseVertexIndex(e,l),d=this.parseVertexIndex(n,l);if(this.addVertex(c,h,d),this.colors.length>0&&this.addColor(c,h,d),void 0!==i&&""!==i){var p=this.uvs.length;c=this.parseUVIndex(i,p),h=this.parseUVIndex(r,p),d=this.parseUVIndex(o,p),this.addUV(c,h,d)}if(void 0!==s&&""!==s){var f=this.normals.length;c=this.parseNormalIndex(s,f),h=s===a?c:this.parseNormalIndex(a,f),d=s===u?c:this.parseNormalIndex(u,f),this.addNormal(c,h,d)}},addPointGeometry:function(t){this.object.geometry.type="Points";for(var e=this.vertices.length,n=0,i=t.length;n<i;n++)this.addVertexPoint(this.parseVertexIndex(t[n],e))},addLineGeometry:function(t,e){this.object.geometry.type="Line";for(var n=this.vertices.length,i=this.uvs.length,r=0,o=t.length;r<o;r++)this.addVertexLine(this.parseVertexIndex(t[r],n));var s=0;for(o=e.length;s<o;s++)this.addUVLine(this.parseUVIndex(e[s],i))}};return t.startObject("",!1),t}function r(t){o.s.call(this,t),this.materials=null}return r.prototype=Object.assign(Object.create(o.s.prototype),{constructor:r,load:function(t,e,n,i){var r=this,s=new o.i(r.manager);s.setPath(this.path),s.load(t,(function(t){e(r.parse(t))}),n,i)},setMaterials:function(t){return this.materials=t,this},parse:function(r){console.time("OBJLoader");var s=new i;-1!==r.indexOf("\r\n")&&(r=r.replace(/\r\n/g,"\n")),-1!==r.indexOf("\\\n")&&(r=r.replace(/\\\n/g,""));for(var a=r.split("\n"),u="",l="",c=[],h="function"===typeof"".trimLeft,d=0,p=a.length;d<p;d++)if(u=a[d],0!==(u=h?u.trimLeft():u.trim()).length&&"#"!==(l=u.charAt(0)))if("v"===l){var f=u.split(/\s+/);switch(f[0]){case"v":s.vertices.push(parseFloat(f[1]),parseFloat(f[2]),parseFloat(f[3])),f.length>=7&&s.colors.push(parseFloat(f[4]),parseFloat(f[5]),parseFloat(f[6]));break;case"vn":s.normals.push(parseFloat(f[1]),parseFloat(f[2]),parseFloat(f[3]));break;case"vt":s.uvs.push(parseFloat(f[1]),parseFloat(f[2]))}}else if("f"===l){for(var m=u.substr(1).trim().split(/\s+/),v=[],g=0,b=m.length;g<b;g++){var y=m[g];if(y.length>0){var w=y.split("/");v.push(w)}}var x=v[0];for(g=1,b=v.length-1;g<b;g++){var j=v[g],C=v[g+1];s.addFace(x[0],j[0],C[0],x[1],j[1],C[1],x[2],j[2],C[2])}}else if("l"===l){var z=u.substring(1).trim().split(" "),S=[],L=[];if(-1===u.indexOf("/"))S=z;else for(var E=0,O=z.length;E<O;E++){var M=z[E].split("/");""!==M[0]&&S.push(M[0]),""!==M[1]&&L.push(M[1])}s.addLineGeometry(S,L)}else if("p"===l){var k=u.substr(1).trim().split(" ");s.addPointGeometry(k)}else if(null!==(c=t.exec(u))){var V=(" "+c[0].substr(1).trim()).substr(1);s.startObject(V)}else if(n.test(u))s.object.startMaterial(u.substring(7).trim(),s.materialLibraries);else if(e.test(u))s.materialLibraries.push(u.substring(7).trim());else{if("s"!==l){if("\0"===u)continue;throw new Error('THREE.OBJLoader: Unexpected line: "'+u+'"')}if((c=u.split(" ")).length>1){var I=c[1].trim().toLowerCase();s.object.smooth="0"!==I&&"off"!==I}else s.object.smooth=!0;(_=s.object.currentMaterial())&&(_.smooth=s.object.smooth)}s.finalize();var T=new o.n;T.materialLibraries=[].concat(s.materialLibraries);for(d=0,p=s.objects.length;d<p;d++){var A=s.objects[d],U=A.geometry,P=A.materials,F="Line"===U.type,D="Points"===U.type,G=!1;if(0!==U.vertices.length){var R=new o.d;R.addAttribute("position",new o.j(U.vertices,3)),U.normals.length>0?R.addAttribute("normal",new o.j(U.normals,3)):R.computeVertexNormals(),U.colors.length>0&&(G=!0,R.addAttribute("color",new o.j(U.colors,3))),U.uvs.length>0&&R.addAttribute("uv",new o.j(U.uvs,2));for(var B,H=[],N=0,W=P.length;N<W;N++){var q=P[N],_=void 0;if(null!==this.materials)if(_=this.materials.create(q.name),!F||!_||_ instanceof o.q){if(D&&_&&!(_ instanceof o.E)){var J=new o.E({size:10,sizeAttenuation:!1});o.t.prototype.copy.call(J,_),J.color.copy(_.color),J.map=_.map,_=J}}else{var Z=new o.q;o.t.prototype.copy.call(Z,_),Z.color.copy(_.color),_=Z}_||((_=F?new o.q:D?new o.E({size:1,sizeAttenuation:!1}):new o.A).name=q.name),_.flatShading=!q.smooth,_.vertexColors=G?o.N:o.B,H.push(_)}if(H.length>1){for(N=0,W=P.length;N<W;N++){q=P[N];R.addGroup(q.groupStart,q.groupCount,N)}B=F?new o.r(R,H):D?new o.D(R,H):new o.x(R,H)}else B=F?new o.r(R,H[0]):D?new o.D(R,H[0]):new o.x(R,H[0]);B.name=A.name,T.add(B)}}return console.timeEnd("OBJLoader"),T}}),r}(),a=n(99),u=n(602),l={flute:16425499,holder:7061992,insert:16425499,probe_tip:9707832,shaft:9934743},c=function(t){return e=t,Object.keys(l).includes(e)?new o.f(l[t]):new o.f("gray");var e},h=n(1668),d=n(1670),p=(n(1671),function(t){var e=t.width,n=t.pixels,i=t.unit,o=t.translate,s=Math.max(5,Math.min(15,Math.round(n))),a="".concat(s,"px");return r.createElement("figure",{id:"scaleContainer"},r.createElement("div",{id:"scaleSquare",style:{width:a,height:a}}),r.createElement("figcaption",null,function(t,e,n){if(e<0)throw new Error("Scale width must be positive");return"millimeters"===t?function(t,e){var n=e("mm",{context:"millimetres"}),i=e("cm",{context:"centimetres"}),r=e("m",{context:"metres"});return t<10?"".concat(t," ").concat(n.translatedText):t>=10&&t<1e3?"".concat(t/10," ").concat(i.translatedText):"".concat(t/1e3," ").concat(r.translatedText)}(e,n):function(t,e){var n=e("in",{context:"inches"}),i=e("ft",{context:"feet"});return t<1?"1/".concat(1/t," ").concat(n.translatedText):t>=1&&t<12?"".concat(t," ").concat(n.translatedText):"".concat(t/12," ").concat(i.translatedText)}(e,n)}(i,e,o)))}),f=(n(1672),n(14)),m=n(9),v=n(12),g=n(47),b=n(22),y=n.n(b),w={inches:[1/16,1/8,.25,1,4,12,36,360],millimeters:[.1,1,5,10,50,100,1e3]},x=.5,j=function(t,e){for(var n=w[t],i=0,r=n[i];r*e<5;)(i+=1)>=n.length?r*=10:r=n[i];return{minorStep:r*("inches"===t?8:10),subdivisionStep:r}},C=function(t,e,n,i){var r=[],s=j(i,n),a=function(t,e,n,i,r){y()(e>0,"Width must be greater than 0"),y()(n>0,"Height must be greater than 0"),y()(i>0,"Minor step size must be greater than 0"),y()(r>0,"Subdivision step size must be greater than 0");var o=x*e,s=x*n,a=i/r;t.push(-o,0,.1,o,0,.1),t.push(0,-s,.1,0,s,.1);for(var u=0,l=1;l*i<=o;l+=1){var c=l*i;t.push(c,-s,0,c,s,0),t.push(-c,-s,0,-c,s,0),u+=4}for(var h=1;h*i<=s;h+=1){var d=h*i;t.push(-o,d,0,o,d,0),t.push(-o,-d,0,o,-d,0),u+=4}for(var p=0,f=1;f*r<=o;f+=1)if(f%a!==0){var m=f*r;t.push(m,-s,0,m,s,0),t.push(-m,-s,0,-m,s,0),p+=4}for(var v=1;v*r<=s;v+=1)if(v%a!==0){var g=v*r;t.push(-o,g,0,o,g,0),t.push(-o,-g,0,o,-g,0),p+=4}return{minorCount:u,subdivisionCount:p}}(r,t,e,s.minorStep,s.subdivisionStep),u=a.minorCount,l=a.subdivisionCount,c=new o.d,h=0,d=1,p=2;c.addGroup(0,4,h),c.addGroup(4,u,d),c.addGroup(4+u,l,p);return c.addAttribute("position",new o.j(r,3)),c},z=function(){return[new o.q({color:new o.f(6710886),linewidth:1.5}),new o.q({color:new o.f(10212847),linewidth:1}),new o.q({color:new o.f(13495031),linewidth:.5})]},S=function(t){y()(t>0&&t!==1/0,"Zoom value must be a valid positive number");var e=new o.e(3/t,20),n=new o.y({color:0});return new o.x(e,n)},L=function(){function t(e,n,i,r,s,a){Object(m.a)(this,t),this.displayDensity=void 0,this.group=void 0,this.unit=void 0,y()(s>0&&s!==1/0,"Zoom value must be a valid positive number"),y()(n>0,"Screen height must be positive"),y()(i>0,"Screen width must be positive"),this.group=new o.n,this.unit=a;var u=new o.L;e.getSize(u),u.multiplyScalar(1/r);var l=new o.L;e.getCenter(l);var c=l.x+x*u.x,h=l.y+x*u.y,d=Math.ceil(i/s),p=Math.ceil(n/s),f=2*Math.max(c,d),v=2*Math.max(h,p);this.displayDensity=Math.min(i/d,n/p);var g=new o.r(C(f,v,this.displayDensity,this.unit),z());g.translateZ(e.min.z);var b=S(s),w=l.z+x*u.z;b.translateZ(w),this.group.name="grid",this.group.add(g),this.group.add(b)}return Object(v.a)(t,[{key:"getGroup",value:function(){return this.group}},{key:"getSubdivisionInfo",value:function(){var t=j(this.unit,this.displayDensity).subdivisionStep;return{pixels:t*this.displayDensity,step:t}}}]),t}(),E=function(t){var e=new o.c,n=!0,i=!1,r=void 0;try{for(var s,a=t[Symbol.iterator]();!(n=(s=a.next()).done);n=!0){var u=s.value;e.expandByObject(u)}}catch(h){i=!0,r=h}finally{try{n||null==a.return||a.return()}finally{if(i)throw r}}var l=new o.L;e.getSize(l);var c=new o.L;return e.getCenter(c),{boundingBox:e,toolSize:l,toolCentre:c}},O=function(){var t=Object(h.getRendererCreator)().makeRenderer();t.setClearColor(new o.f("white"),100);var e=new o.G,n=new o.H("white",.75);e.add(n),e.add(n.target);var i=new o.H("white",.25);e.add(i),e.add(i.target);var r=new o.a("white",.5);return e.add(r),{camera:new o.C(0,0,0,0,-1e3,1e3),fillLight:i,keyLight:n,renderer:t,scene:e}},M=function(){function t(e){Object(m.a)(this,t),this.clientHeight=void 0,this.clientWidth=void 0,this.currentToolComponents=void 0,this.currentUnit=void 0,this.fillLightAngle=.463,this.keyLightAngle=.611,this.mountPoint=void 0,this.setScale=void 0,this.setup=void 0,this.setup=O(),this.currentToolComponents=[],this.clientWidth=0,this.clientHeight=0,this.currentUnit="millimeters",this.setScale=e}return Object(v.a)(t,[{key:"mount",value:function(t,e){this.mountPoint=t,e(this.setup.renderer.domElement),this.resize()}},{key:"render",value:function(){this.setup.renderer.render(this.setup.scene,this.setup.camera)}},{key:"resize",value:function(){var t=Object(g.a)(this.mountPoint,"Not mounted");this.clientWidth=t.clientWidth,this.clientHeight=t.clientHeight,this.setup.renderer.setSize(this.clientWidth,this.clientHeight),this.update(this.currentToolComponents,this.currentUnit)}},{key:"unmount",value:function(){var t;this.clearScene(),null===(t=this.mountPoint)||void 0===t||t.removeChild(this.setup.renderer.domElement)}},{key:"update",value:function(t,e){var n;(this.clearScene(),this.currentUnit=e,this.currentToolComponents=t,t.length>0)&&(n=this.setup.scene).add.apply(n,Object(f.a)(t));this.updateCamera(),this.updateLights()}},{key:"clearScene",value:function(){var t;(t=this.setup.scene).remove.apply(t,Object(f.a)(this.currentToolComponents))}},{key:"updateCamera",value:function(){!function(t,e,n,i,r,o,s){i.left=-r/2,i.right=r/2,i.bottom=-o/2,i.top=o/2;var a=E(e),u=a.boundingBox,l=a.toolSize,c=a.toolCentre;i.position.x=c.x,i.position.y=c.y;i.position.z=c.z+l.z/2+500;i.zoom=.7*Math.min(r/l.x,o/l.y),i.updateProjectionMatrix();var h=t.getObjectByName("grid");if(void 0!==h&&t.remove(h),!u.isEmpty()){var d=new L(u,o,r,.7,i.zoom,n),p=d.getGroup();t.add(p),s(d.getSubdivisionInfo())}}(this.setup.scene,this.currentToolComponents,this.currentUnit,this.setup.camera,this.clientWidth,this.clientHeight,this.setScale)}},{key:"updateLights",value:function(){!function(t,e,n,i,r){var o=E(t),s=o.toolSize,a=o.toolCentre,u=s.length();e.position.set(a.x-Math.tan(i)*u,a.y+Math.tan(i)*u,u),n.position.set(a.x+Math.tan(r)*u,a.y,u),e.target.position.set(a.x,a.y,a.z),n.target.position.set(a.x,a.y,a.z),e.target.updateMatrixWorld(),n.target.updateMatrixWorld()}(this.currentToolComponents,this.setup.keyLight,this.setup.fillLight,this.keyLightAngle,this.fillLightAngle)}}]),t}(),k={pixels:0,step:0},V=function(t){var e=t.objectsToDraw,n=t.translate,o=t.unit,s=r.useRef(null),a=r.useRef(null),u=r.useState(k),l=Object(i.a)(u,2),c=l[0],h=l[1],f=r.useMemo((function(){return new M(h)}),[h]);return r.useEffect((function(){if(null!==s.current){var t=s.current;f.mount(t,(function(e){t.insertBefore(e,a.current)}));var e=function(){f.resize(),f.render()},n=new d.default(e);n.observe(s.current),window.addEventListener("resize",e);return function(){f.unmount(),window.removeEventListener("resize",e),n.disconnect()}}}),[f]),r.useEffect((function(){f.resize(),f.update(e,o),f.render()}),[f,e,o]),r.createElement("div",{id:"container",ref:s},r.createElement("div",{id:"overlay",ref:a},r.createElement(p,{width:c.step,pixels:c.pixels,translate:n,unit:o})))},I=function(t){return Object.keys(t).map((function(e){return function(t,e){var n=Object(h.getRendererCreator)().getMaterial(e);return t.traverse((function(t){t instanceof o.x&&(t.material=n)})),t}(function(t){var e=(new s).parse(t),n=-Math.PI/2;return e.rotateX(n),e}(t[e]),c(e))}))};e.default=function(t){var e=t.loadOBJs,n=r.useState(void 0),o=Object(i.a)(n,2),s=o[0],l=o[1];if(r.useEffect((function(){var t=Object(u.a)(l),n=Object(i.a)(t,2),r=n[0],o=n[1];return e().then(I).then(r).catch((function(t){console.warn(t)})),o}),[e,l]),void 0===s)return r.createElement("div",{id:"undefinedPreview"});var c=Object(a.b)(t.tool).units;return r.createElement(V,{objectsToDraw:s,unit:c,translate:t.translate})}}}]);