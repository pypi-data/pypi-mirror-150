"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1038],{349:(e,t,i)=>{function r(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}i.d(t,{m:()=>a});class n{constructor(e=!0){r(this,"_storage",{}),r(this,"_listeners",{}),e&&window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const i=this._listeners[e].indexOf(t);-1!==i&&this._listeners[e].splice(i,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(e){}}}const o=new n,a=(e,t,i=!0,r)=>a=>{const s=i?o:new n(!1),l=String(a.key);e=e||String(a.key);const d=a.initializer?a.initializer():void 0;s.addFromStorage(e);const c=()=>s.hasKey(e)?s.getValue(e):d;return{kind:"method",placement:"prototype",key:a.key,descriptor:{set(i){((i,r)=>{let n;t&&(n=c()),s.setValue(e,r),t&&i.requestUpdate(a.key,n)})(this,i)},get:()=>c(),enumerable:!0,configurable:!0},finisher(n){if(t&&i){const t=n.prototype.connectedCallback,i=n.prototype.disconnectedCallback;n.prototype.connectedCallback=function(){var i;t.call(this),this[`__unbsubLocalStorage${l}`]=(i=this,s.subscribeChanges(e,(e=>{i.requestUpdate(a.key,e)})))},n.prototype.disconnectedCallback=function(){i.call(this),this[`__unbsubLocalStorage${l}`]()}}t&&n.createProperty(a.key,{noAccessor:!0,...r})}}}},22311:(e,t,i)=>{i.d(t,{N:()=>n});var r=i(58831);const n=e=>(0,r.M)(e.entity_id)},40095:(e,t,i)=>{i.d(t,{e:()=>r});const r=(e,t)=>0!=(e.attributes.supported_features&t)},85415:(e,t,i)=>{i.d(t,{$:()=>r,f:()=>n});const r=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>r(e.toLowerCase(),t.toLowerCase())},8330:(e,t,i)=>{i.d(t,{P:()=>r});const r=(e,t,i=!0,r=!0)=>{let n,o=0;return(...a)=>{const s=()=>{o=!1===i?0:Date.now(),n=void 0,e(...a)},l=Date.now();o||!1!==i||(o=l);const d=t-(l-o);d<=0||d>t?(n&&(clearTimeout(n),n=void 0),o=l,e(...a)):n||!1===r||(n=window.setTimeout(s,d))}}},91038:(e,t,i)=>{i.r(t);i(51187),i(25782),i(53973),i(51095);var r=i(37500),n=i(33310),o=i(8636),a=i(1460),s=i(14516),l=i(349),d=i(47181),c=i(70518),h=i(85415),p=i(87744),u=i(8330),f=i(6936),m=i(24833),y=i(93491),v=i(11654);i(28007),i(10983),i(48932),i(52039),i(10174);function b(){b=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!_(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return E(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?E(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=H(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:x(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=x(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function g(e){var t,i=H(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function _(e){return e.decorators&&e.decorators.length}function w(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function x(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function H(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function E(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function C(e,t,i){return C="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=V(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},C(e,t,i||e)}function V(e){return V=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},V(e)}const P=["media-browser","config","developer-tools"],$="scrollIntoViewIfNeeded"in document.body,M={energy:1,map:2,logbook:3,history:4,"developer-tools":9,"media-browser":10,config:11},A={calendar:"M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z",energy:"M5 20V12H2L12 3L22 12H19V20H5M12 5.69L7 10.19V18H17V10.19L12 5.69M11.5 18V14H9L12.5 7V11H15L11.5 18Z",history:"M13.5,8H12V13L16.28,15.54L17,14.33L13.5,12.25V8M13,3A9,9 0 0,0 4,12H1L4.96,16.03L9,12H6A7,7 0 0,1 13,5A7,7 0 0,1 20,12A7,7 0 0,1 13,19C11.07,19 9.32,18.21 8.06,16.94L6.64,18.36C8.27,20 10.5,21 13,21A9,9 0 0,0 22,12A9,9 0 0,0 13,3",logbook:"M17,4V10L15,8L13,10V4H9V20H19V4H17M3,7V5H5V4C5,2.89 5.9,2 7,2H19C20.05,2 21,2.95 21,4V20C21,21.05 20.05,22 19,22H7C5.95,22 5,21.05 5,20V19H3V17H5V13H3V11H5V7H3M5,5V7H7V5H5M5,19H7V17H5V19M5,13H7V11H5V13Z",lovelace:"M19,5V7H15V5H19M9,5V11H5V5H9M19,13V19H15V13H19M9,17V19H5V17H9M21,3H13V9H21V3M11,3H3V13H11V3M21,11H13V21H21V11M11,15H3V21H11V15Z",map:"M12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5M12,2A7,7 0 0,1 19,9C19,14.25 12,22 12,22C12,22 5,14.25 5,9A7,7 0 0,1 12,2M12,4A5,5 0 0,0 7,9C7,10 7,12 12,18.71C17,12 17,10 17,9A5,5 0 0,0 12,4Z","media-browser":"M22 8V13.81C21.39 13.46 20.72 13.22 20 13.09V8H4V18H13.09C13.04 18.33 13 18.66 13 19C13 19.34 13.04 19.67 13.09 20H4C2.9 20 2 19.11 2 18V6C2 4.89 2.89 4 4 4H10L12 6H20C21.1 6 22 6.89 22 8M17 22L22 19L17 16V22Z","developer-tools":"M8,3A2,2 0 0,0 6,5V9A2,2 0 0,1 4,11H3V13H4A2,2 0 0,1 6,15V19A2,2 0 0,0 8,21H10V19H8V14A2,2 0 0,0 6,12A2,2 0 0,0 8,10V5H10V3M16,3A2,2 0 0,1 18,5V9A2,2 0 0,0 20,11H21V13H20A2,2 0 0,0 18,15V19A2,2 0 0,1 16,21H14V19H16V14A2,2 0 0,1 18,12A2,2 0 0,1 16,10V5H14V3H16Z"},L=(e,t,i,r)=>{const n=e.indexOf(i.url_path),o=e.indexOf(r.url_path);return n!==o?n<o?1:-1:S(t,i,r)},S=(e,t,i)=>{const r="lovelace"===t.component_name,n="lovelace"===i.component_name;if(t.url_path===e)return-1;if(i.url_path===e)return 1;if(r&&n)return(0,h.$)(t.title,i.title);if(r&&!n)return-1;if(n)return 1;const o=t.url_path in M,a=i.url_path in M;return o&&a?M[t.url_path]-M[i.url_path]:o?-1:a?1:(0,h.$)(t.title,i.title)},T=(0,s.Z)(((e,t,i,r)=>{if(!e)return[[],[]];const n=[],o=[];Object.values(e).forEach((e=>{r.includes(e.url_path)||!e.title&&e.url_path!==t||(P.includes(e.url_path)?o:n).push(e)}));const a=[...i].reverse();return n.sort(((e,i)=>L(a,t,e,i))),o.sort(((e,i)=>L(a,t,e,i))),[n,o]}));let O;!function(e,t,i,r){var n=b();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(w(o.descriptor)||w(n.descriptor)){if(_(o)||_(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(_(o)){if(_(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}k(o,n)}else t.push(o)}return t}(a.d.map(g)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-sidebar")],(function(e,t){class s extends t{constructor(...t){super(...t),e(this)}}return{F:s,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"alwaysExpand",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"editMode",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_notifications",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_updatesCount",value:()=>0},{kind:"field",decorators:[(0,n.SB)()],key:"_renderEmptySortable",value:()=>!1},{kind:"field",key:"_mouseLeaveTimeout",value:void 0},{kind:"field",key:"_tooltipHideTimeout",value:void 0},{kind:"field",key:"_recentKeydownActiveUntil",value:()=>0},{kind:"field",decorators:[(0,l.m)("sidebarPanelOrder",!0,{attribute:!1})],key:"_panelOrder",value:()=>[]},{kind:"field",decorators:[(0,l.m)("sidebarHiddenPanels",!0,{attribute:!1})],key:"_hiddenPanels",value:()=>["developer-tools"]},{kind:"field",key:"_sortable",value:void 0},{kind:"method",key:"render",value:function(){return this.hass?r.dy`
      ${this._renderHeader()}
      ${this._renderAllPanels()}
      ${this._renderDivider()}
      ${this._renderNotifications()}
      ${this._renderUserItem()}
      <div disabled class="bottom-spacer"></div>
      <div class="tooltip"></div>
    `:r.dy``}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("expanded")||e.has("narrow")||e.has("alwaysExpand")||e.has("_externalConfig")||e.has("_updatesCount")||e.has("_notifications")||e.has("editMode")||e.has("_renderEmptySortable")||e.has("_hiddenPanels")||e.has("_panelOrder")&&!this.editMode)return!0;if(!this.hass||!e.has("hass"))return!1;const t=e.get("hass");if(!t)return!0;const i=this.hass;return i.panels!==t.panels||i.panelUrl!==t.panelUrl||i.user!==t.user||i.localize!==t.localize||i.locale!==t.locale||i.states!==t.states||i.defaultPanel!==t.defaultPanel}},{kind:"method",key:"firstUpdated",value:function(e){C(V(s.prototype),"firstUpdated",this).call(this,e),(0,f.r)(this.hass.connection,(e=>{this._notifications=e}))}},{kind:"method",key:"updated",value:function(e){if(C(V(s.prototype),"updated",this).call(this,e),e.has("alwaysExpand")&&(0,c.X)(this,"expanded",this.alwaysExpand),e.has("editMode")&&(this.editMode?this._activateEditMode():this._deactivateEditMode()),!e.has("hass"))return;const t=e.get("hass");if(t&&t.locale===this.hass.locale||(0,c.X)(this,"rtl",(0,p.HE)(this.hass)),this._calculateCounts(),$&&(!t||t.panelUrl!==this.hass.panelUrl)){const e=this.shadowRoot.querySelector(".iron-selected");e&&e.scrollIntoViewIfNeeded()}}},{kind:"field",key:"_calculateCounts",value(){return(0,u.P)((()=>{let e=0;for(const t of Object.keys(this.hass.states))t.startsWith("update.")&&(0,m.hF)(this.hass.states[t])&&e++;this._updatesCount=e}),5e3)}},{kind:"method",key:"_renderHeader",value:function(){return r.dy`<div
      class="menu"
      @action=${this._handleAction}
      .actionHandler=${(0,y.K)({hasHold:!this.editMode,disabled:this.editMode})}
    >
      ${this.narrow?"":r.dy`
            <ha-icon-button
              .label=${this.hass.localize("ui.sidebar.sidebar_toggle")}
              .path=${"docked"===this.hass.dockedSidebar?"M21,15.61L19.59,17L14.58,12L19.59,7L21,8.39L17.44,12L21,15.61M3,6H16V8H3V6M3,13V11H13V13H3M3,18V16H16V18H3Z":"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"}
              @action=${this._toggleSidebar}
            ></ha-icon-button>
          `}
      ${this.editMode?r.dy`<mwc-button outlined @click=${this._closeEditMode}>
            ${this.hass.localize("ui.sidebar.done")}
          </mwc-button>`:r.dy`<div class="header">
            <img src="/static/icons/logo.png" height="100" width="100" alt="" />
          </div>`}
    </div>`}},{kind:"method",key:"_renderAllPanels",value:function(){var e;const[t,i]=T(this.hass.panels,this.hass.defaultPanel,this._panelOrder,this._hiddenPanels),n=null!==(e=this.route.path)&&void 0!==e&&e.startsWith("/hassio/")?"config":this.hass.panelUrl;return r.dy`
      <paper-listbox
        attr-for-selected="data-panel"
        class="ha-scrollbar"
        .selected=${n}
        @focusin=${this._listboxFocusIn}
        @focusout=${this._listboxFocusOut}
        @scroll=${this._listboxScroll}
        @keydown=${this._listboxKeydown}
      >
        ${this.editMode?this._renderPanelsEdit(t):this._renderPanels(t)}
        ${this._renderSpacer()}
        ${this._renderPanels(i)}
        ${this._renderExternalConfiguration()}
      </paper-listbox>
    `}},{kind:"method",key:"_renderPanels",value:function(e){return e.map((e=>this._renderPanel(e.url_path,e.url_path===this.hass.defaultPanel?e.title||this.hass.localize("panel.states"):this.hass.localize(`panel.${e.title}`)||e.title,e.icon,e.url_path!==this.hass.defaultPanel||e.icon?e.url_path in A?A[e.url_path]:void 0:A.lovelace)))}},{kind:"method",key:"_renderPanel",value:function(e,t,i,n){return"config"===e?this._renderConfiguration(t):r.dy`
          <a
            role="option"
            href=${`/${e}`}
            data-panel=${e}
            tabindex="-1"
            @mouseenter=${this._itemMouseEnter}
            @mouseleave=${this._itemMouseLeave}
          >
            <paper-icon-item>
              ${n?r.dy`<ha-svg-icon
                    slot="item-icon"
                    .path=${n}
                  ></ha-svg-icon>`:r.dy`<ha-icon slot="item-icon" .icon=${i}></ha-icon>`}
              <span class="item-text">${t}</span>
            </paper-icon-item>
            ${this.editMode?r.dy`<ha-icon-button
                  .label=${this.hass.localize("ui.sidebar.hide_panel")}
                  .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                  class="hide-panel"
                  .panel=${e}
                  @click=${this._hidePanel}
                ></ha-icon-button>`:""}
          </a>
        `}},{kind:"method",key:"_renderPanelsEdit",value:function(e){return r.dy`<div id="sortable">
        ${(0,a.l)([this._hiddenPanels,this._renderEmptySortable],(()=>this._renderEmptySortable?"":this._renderPanels(e)))}
      </div>
      ${this._renderSpacer()}
      ${this._renderHiddenPanels()} `}},{kind:"method",key:"_renderHiddenPanels",value:function(){return r.dy`${this._hiddenPanels.length?r.dy`${this._hiddenPanels.map((e=>{const t=this.hass.panels[e];return t?r.dy`<paper-icon-item
            @click=${this._unhidePanel}
            class="hidden-panel"
            .panel=${e}
          >
            ${t.url_path!==this.hass.defaultPanel||t.icon?t.url_path in A?r.dy`<ha-svg-icon
                  slot="item-icon"
                  .path=${A[t.url_path]}
                ></ha-svg-icon>`:r.dy`<ha-icon slot="item-icon" .icon=${t.icon}></ha-icon>`:r.dy`<ha-svg-icon
                  slot="item-icon"
                  .path=${A.lovelace}
                ></ha-svg-icon>`}
            <span class="item-text"
              >${t.url_path===this.hass.defaultPanel?this.hass.localize("panel.states"):this.hass.localize(`panel.${t.title}`)||t.title}</span
            >
            <ha-icon-button
              .label=${this.hass.localize("ui.sidebar.show_panel")}
              .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}
              class="show-panel"
            ></ha-icon-button>
          </paper-icon-item>`:""}))}
        ${this._renderSpacer()}`:""}`}},{kind:"method",key:"_renderDivider",value:function(){return r.dy`<div class="divider"></div>`}},{kind:"method",key:"_renderSpacer",value:function(){return r.dy`<div class="spacer" disabled></div>`}},{kind:"method",key:"_renderConfiguration",value:function(e){return r.dy` <a
      class="configuration-container"
      role="option"
      href="/config"
      data-panel="config"
      tabindex="-1"
      @mouseenter=${this._itemMouseEnter}
      @mouseleave=${this._itemMouseLeave}
    >
      <paper-icon-item class="configuration" role="option">
        <ha-svg-icon slot="item-icon" .path=${"M3,17V19H9V17H3M3,5V7H13V5H3M13,21V19H21V17H13V15H11V21H13M7,9V11H3V13H7V15H9V9H7M21,13V11H11V13H21M15,9H17V7H21V5H17V3H15V9Z"}></ha-svg-icon>
        ${!this.alwaysExpand&&this._updatesCount>0?r.dy`
              <span class="configuration-badge" slot="item-icon">
                ${this._updatesCount}
              </span>
            `:""}
        <span class="item-text">${e}</span>
        ${this.alwaysExpand&&this._updatesCount>0?r.dy`
              <span class="configuration-badge">${this._updatesCount}</span>
            `:""}
      </paper-icon-item>
    </a>`}},{kind:"method",key:"_renderNotifications",value:function(){const e=this._notifications?this._notifications.length:0;return r.dy`<div
      class="notifications-container"
      @mouseenter=${this._itemMouseEnter}
      @mouseleave=${this._itemMouseLeave}
    >
      <paper-icon-item
        class="notifications"
        role="option"
        @click=${this._handleShowNotificationDrawer}
      >

        <ha-svg-icon
          slot="item-icon"
          .path=${"M19.5 8C21.43 8 23 6.43 23 4.5C23 2.57 21.43 1 19.5 1C17.57 1 16 2.57 16 4.5C16 6.43 17.57 8 19.5 8M21 16V9.79C20.5 9.93 20 10 19.5 10C19.33 10 19.17 10 19 10V16C19 17.66 17.66 19 16 19H8C6.34 19 5 17.66 5 16V8C5 6.34 6.34 5 8 5H14C14 4.84 14 4.67 14 4.5C14 4 14.07 3.5 14.21 3H8C5.24 3 3 5.24 3 8V16C3 18.76 5.24 21 8 21H16C18.76 21 21 18.76 21 16Z"}
        ></ha-svg-icon>

        ${!this.alwaysExpand&&e>0?r.dy`
              <span class="notification-badge" slot="item-icon">
                ${e}
              </span>
            `:""}
        <span class="item-text">
          ${this.hass.localize("ui.notification_drawer.title")}
        </span>
        ${this.alwaysExpand&&e>0?r.dy` <span class="notification-badge">${e}</span> `:""}
      </paper-icon-item>
    </div>`}},{kind:"method",key:"_renderUserItem",value:function(){return r.dy`<a
      class=${(0,o.$)({profile:!0,"iron-selected":"profile"===this.hass.panelUrl})}
      href="/profile"
      data-panel="panel"
      tabindex="-1"
      role="option"
      aria-label=${this.hass.localize("panel.profile")}
      @mouseenter=${this._itemMouseEnter}
      @mouseleave=${this._itemMouseLeave}
    >
      <paper-icon-item>
        <ha-user-badge
          slot="item-icon"
          .user=${this.hass.user}
          .hass=${this.hass}
        ></ha-user-badge>

        <span class="item-text">
          ${this.hass.user?this.hass.user.name:""}
        </span>
      </paper-icon-item>
    </a>`}},{kind:"method",key:"_renderExternalConfiguration",value:function(){var e,t;return r.dy`${null!==(e=this.hass.user)&&void 0!==e&&e.is_admin||null===(t=this.hass.auth.external)||void 0===t||!t.config.hasSettingsScreen?"":r.dy`
          <a
            role="option"
            aria-label=${this.hass.localize("ui.sidebar.external_app_configuration")}
            href="#external-app-configuration"
            tabindex="-1"
            @click=${this._handleExternalAppConfiguration}
            @mouseenter=${this._itemMouseEnter}
            @mouseleave=${this._itemMouseLeave}
          >
            <paper-icon-item>
              <ha-svg-icon
                slot="item-icon"
                .path=${"M9.82,12.5C9.84,12.33 9.86,12.17 9.86,12C9.86,11.83 9.84,11.67 9.82,11.5L10.9,10.69C11,10.62 11,10.5 10.96,10.37L9.93,8.64C9.87,8.53 9.73,8.5 9.62,8.53L8.34,9.03C8.07,8.83 7.78,8.67 7.47,8.54L7.27,7.21C7.27,7.09 7.16,7 7.03,7H5C4.85,7 4.74,7.09 4.72,7.21L4.5,8.53C4.21,8.65 3.92,8.83 3.65,9L2.37,8.5C2.25,8.47 2.12,8.5 2.06,8.63L1.03,10.36C0.97,10.5 1,10.61 1.1,10.69L2.18,11.5C2.16,11.67 2.15,11.84 2.15,12C2.15,12.17 2.17,12.33 2.19,12.5L1.1,13.32C1,13.39 1,13.53 1.04,13.64L2.07,15.37C2.13,15.5 2.27,15.5 2.38,15.5L3.66,15C3.93,15.18 4.22,15.34 4.53,15.47L4.73,16.79C4.74,16.91 4.85,17 5,17H7.04C7.17,17 7.28,16.91 7.29,16.79L7.5,15.47C7.8,15.35 8.09,15.17 8.36,15L9.64,15.5C9.76,15.53 9.89,15.5 9.95,15.37L11,13.64C11.04,13.53 11,13.4 10.92,13.32L9.82,12.5M6,13.75C5,13.75 4.2,12.97 4.2,12C4.2,11.03 5,10.25 6,10.25C7,10.25 7.8,11.03 7.8,12C7.8,12.97 7,13.75 6,13.75M17,1H7A2,2 0 0,0 5,3V6H7V4H17V20H7V18H5V21A2,2 0 0,0 7,23H17A2,2 0 0,0 19,21V3A2,2 0 0,0 17,1Z"}
              ></ha-svg-icon>
              <span class="item-text">
                ${this.hass.localize("ui.sidebar.external_app_configuration")}
              </span>
            </paper-icon-item>
          </a>
        `}`}},{kind:"method",key:"_handleExternalAppConfiguration",value:function(e){e.preventDefault(),this.hass.auth.external.fireMessage({type:"config_screen/show"})}},{kind:"get",key:"_tooltip",value:function(){return this.shadowRoot.querySelector(".tooltip")}},{kind:"method",key:"_handleAction",value:function(e){"hold"===e.detail.action&&(0,d.B)(this,"hass-edit-sidebar",{editMode:!0})}},{kind:"method",key:"_activateEditMode",value:async function(){if(!O){const[e,t]=await Promise.all([i.e(3335).then(i.bind(i,56087)),i.e(651).then(i.bind(i,70651))]),r=document.createElement("style");r.innerHTML=t.sortableStyles.cssText,this.shadowRoot.appendChild(r),O=e.Sortable,O.mount(e.OnSpill),O.mount(e.AutoScroll())}await this.updateComplete,this._createSortable()}},{kind:"method",key:"_createSortable",value:function(){this._sortable=new O(this.shadowRoot.getElementById("sortable"),{animation:150,fallbackClass:"sortable-fallback",dataIdAttr:"data-panel",handle:"paper-icon-item",onSort:async()=>{this._panelOrder=this._sortable.toArray()}})}},{kind:"method",key:"_deactivateEditMode",value:function(){var e;null===(e=this._sortable)||void 0===e||e.destroy(),this._sortable=void 0}},{kind:"method",key:"_closeEditMode",value:function(){(0,d.B)(this,"hass-edit-sidebar",{editMode:!1})}},{kind:"method",key:"_hidePanel",value:async function(e){e.preventDefault();const t=e.currentTarget.panel;if(this._hiddenPanels.includes(t))return;this._hiddenPanels=[...this._hiddenPanels,t],this._renderEmptySortable=!0,await this.updateComplete;const i=this.shadowRoot.getElementById("sortable");for(;i.lastElementChild;)i.removeChild(i.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_unhidePanel",value:async function(e){e.preventDefault();const t=e.currentTarget.panel;this._hiddenPanels=this._hiddenPanels.filter((e=>e!==t)),this._renderEmptySortable=!0,await this.updateComplete;const i=this.shadowRoot.getElementById("sortable");for(;i.lastElementChild;)i.removeChild(i.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_itemMouseEnter",value:function(e){this.alwaysExpand||(new Date).getTime()<this._recentKeydownActiveUntil||(this._mouseLeaveTimeout&&(clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=void 0),this._showTooltip(e.currentTarget))}},{kind:"method",key:"_itemMouseLeave",value:function(){this._mouseLeaveTimeout&&clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=window.setTimeout((()=>{this._hideTooltip()}),500)}},{kind:"method",key:"_listboxFocusIn",value:function(e){this.alwaysExpand||"A"!==e.target.nodeName||this._showTooltip(e.target.querySelector("paper-icon-item"))}},{kind:"method",key:"_listboxFocusOut",value:function(){this._hideTooltip()}},{kind:"method",decorators:[(0,n.hO)({passive:!0})],key:"_listboxScroll",value:function(){(new Date).getTime()<this._recentKeydownActiveUntil||this._hideTooltip()}},{kind:"method",key:"_listboxKeydown",value:function(){this._recentKeydownActiveUntil=(new Date).getTime()+100}},{kind:"method",key:"_showTooltip",value:function(e){this._tooltipHideTimeout&&(clearTimeout(this._tooltipHideTimeout),this._tooltipHideTimeout=void 0);const t=this._tooltip,i=this.shadowRoot.querySelector("paper-listbox");let r=e.offsetTop+11;i.contains(e)&&(r-=i.scrollTop),t.innerHTML=e.querySelector(".item-text").innerHTML,t.style.display="block",t.style.top=`${r}px`,t.style.left=`${e.offsetLeft+e.clientWidth+4}px`}},{kind:"method",key:"_hideTooltip",value:function(){this._tooltipHideTimeout||(this._tooltipHideTimeout=window.setTimeout((()=>{this._tooltipHideTimeout=void 0,this._tooltip.style.display="none"}),10))}},{kind:"method",key:"_handleShowNotificationDrawer",value:function(){(0,d.B)(this,"hass-show-notifications")}},{kind:"method",key:"_toggleSidebar",value:function(e){"tap"===e.detail.action&&(0,d.B)(this,"hass-toggle-menu")}},{kind:"get",static:!0,key:"styles",value:function(){return[v.$c,r.iv`
        :host {
          height: 100%;
          display: block;
          overflow: hidden;
          -ms-user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          border-right: 1px solid var(--divider-color);
          background-color: var(--sidebar-background-color);
          width: 56px;
        }
        :host([expanded]) {
          width: 256px;
          width: calc(256px + env(safe-area-inset-left));
        }
        :host([rtl]) {
          border-right: 0;
          border-left: 1px solid var(--divider-color);
        }
        .menu {
          height: var(--header-height);
          box-sizing: border-box;
          display: flex;
          padding: 0 4px;
          border-bottom: 1px solid transparent;
          white-space: nowrap;
          font-weight: 400;
          color: var(--sidebar-menu-button-text-color, --primary-text-color);
          border-bottom: 1px solid var(--divider-color);
          background-color: var(
            --sidebar-menu-button-background-color,
            --primary-background-color
          );
          font-size: 20px;
          align-items: center;
          padding-left: calc(4px + env(safe-area-inset-left));
        }
        :host([rtl]) .menu {
          padding-left: 4px;
          padding-right: calc(4px + env(safe-area-inset-right));
        }
        :host([expanded]) .menu {
          width: calc(256px + env(safe-area-inset-left));
        }
        :host([rtl][expanded]) .menu {
          width: calc(256px + env(safe-area-inset-right));
        }
        .menu ha-icon-button {
          color: var(--sidebar-icon-color);
        }
        .title {
          margin-left: 19px;
          width: 100%;
          display: none;
        }
        :host([rtl]) .title {
          margin-left: 0;
          margin-right: 19px;
        }
        :host([narrow]) .title {
          margin: 0;
          padding: 0 16px;
        }
        :host([expanded]) .title {
          display: initial;
        }
        :host([expanded]) .menu mwc-button {
          margin: 0 8px;
        }
        .menu mwc-button {
          width: 100%;
        }
        #sortable,
        .hidden-panel {
          display: none;
        }

        paper-listbox {
          padding: 4px 0;
          display: flex;
          flex-direction: column;
          box-sizing: border-box;
          height: calc(100% - var(--header-height) - 132px);
          height: calc(
            100% - var(--header-height) - 132px - env(safe-area-inset-bottom)
          );
          overflow-x: hidden;
          background: none;
          margin-left: env(safe-area-inset-left);
        }

        :host([rtl]) paper-listbox {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }

        a {
          text-decoration: none;
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
          position: relative;
          display: block;
          outline: 0;
        }

        paper-icon-item {
          box-sizing: border-box;
          margin: 4px;
          padding-left: 12px;
          border-radius: 4px;
          --paper-item-min-height: 40px;
          width: 48px;
        }
        :host([expanded]) paper-icon-item {
          width: 248px;
        }
        :host([rtl]) paper-icon-item {
          padding-left: auto;
          padding-right: 12px;
        }

        ha-icon[slot="item-icon"],
        ha-svg-icon[slot="item-icon"] {
          color: var(--sidebar-icon-color);
        }

        .iron-selected paper-icon-item::before,
        a:not(.iron-selected):focus::before {
          border-radius: 10px;
          position: absolute;
          top: 0;
          right: 2px;
          bottom: 0;
          left: 2px;
          pointer-events: none;
          content: "";
          transition: opacity 15ms linear;
          will-change: opacity;
        }
        .iron-selected paper-icon-item::before {
          background-color: var(--sidebar-selected-icon-color);
          opacity: 0.12;
        }
        a:not(.iron-selected):focus::before {
          background-color: currentColor;
          opacity: var(--dark-divider-opacity);
          margin: 4px 8px;
        }
        .iron-selected paper-icon-item:focus::before,
        .iron-selected:focus paper-icon-item::before {
          opacity: 0.2;
        }

        .iron-selected paper-icon-item[pressed]:before {
          opacity: 0.37;
        }

        paper-icon-item span {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
        }

        a.iron-selected paper-icon-item ha-icon,
        a.iron-selected paper-icon-item ha-svg-icon {
          color: var(--sidebar-selected-icon-color);
        }

        a.iron-selected .item-text {
          color: var(--sidebar-selected-text-color);
        }

        paper-icon-item .item-text {
          display: none;
          max-width: calc(100% - 56px);
        }
        :host([expanded]) paper-icon-item .item-text {
          display: block;
        }

        .divider {
          bottom: 112px;
          padding: 10px 0;
        }
        .divider::before {
          content: " ";
          display: block;
          height: 1px;
          background-color: var(--divider-color);
        }
        .notifications-container,
        .configuration-container {
          display: flex;
          margin-left: env(safe-area-inset-left);
        }
        :host([rtl]) .notifications-container,
        :host([rtl]) .configuration-container {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }
        .notifications {
          cursor: pointer;
        }
        .notifications .item-text,
        .configuration .item-text {
          flex: 1;
        }
        .profile {
          margin-left: env(safe-area-inset-left);
        }
        :host([rtl]) .profile {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }
        .profile paper-icon-item {
          padding-left: 4px;
        }
        :host([rtl]) .profile paper-icon-item {
          padding-left: auto;
          padding-right: 4px;
        }
        .profile .item-text {
          margin-left: 8px;
        }
        :host([rtl]) .profile .item-text {
          margin-right: 8px;
        }

        .notification-badge,
        .configuration-badge {
          min-width: 20px;
          box-sizing: border-box;
          border-radius: 50%;
          font-weight: 400;
          background-color: var(--accent-color);
          line-height: 20px;
          text-align: center;
          padding: 0px 6px;
          color: var(--text-accent-color, var(--text-primary-color));
        }
        .configuration-badge {
          background-color: var(--primary-color);
        }
        ha-svg-icon + .notification-badge,
        ha-svg-icon + .configuration-badge {
          position: absolute;
          bottom: 14px;
          left: 26px;
          font-size: 0.65em;
        }

        .spacer {
          flex: 1;
          pointer-events: none;
        }

        .subheader {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
          padding: 16px;
          white-space: nowrap;
        }

        /* .dev-tools {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          padding: 0 8px;
          width: 256px;
          box-sizing: border-box;
        } */

        /* .dev-tools a {
          color: var(--sidebar-icon-color);
        } */

        .tooltip {
          display: none;
          position: absolute;
          opacity: 0.9;
          border-radius: 2px;
          white-space: nowrap;
          color: var(--sidebar-background-color);
          background-color: var(--sidebar-text-color);
          padding: 4px;
          font-weight: 500;
        }

        :host([rtl]) .menu ha-icon-button {
          -webkit-transform: scaleX(-1);
          transform: scaleX(-1);
        }
      `]}}]}}),r.oi)},10174:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(8636),a=i(70483),s=i(22311),l=i(65253);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function v(e,t,i){return v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=b(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},v(e,t,i||e)}function b(e){return b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},b(e)}!function(e,t,i,r){var n=d();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}h(o,n)}else t.push(o)}return t}(a.d.map(c)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-user-badge")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"user",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_personPicture",value:void 0},{kind:"field",key:"_personEntityId",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if(v(b(i.prototype),"willUpdate",this).call(this,e),e.has("user"))return void this._getPersonPicture();const t=e.get("hass");if(this._personEntityId&&t&&this.hass.states[this._personEntityId]!==t.states[this._personEntityId]){const e=this.hass.states[this._personEntityId];e?this._personPicture=e.attributes.entity_picture:this._getPersonPicture()}else!this._personEntityId&&t&&this._getPersonPicture()}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.user)return r.dy``;const e=this._personPicture;if(e)return r.dy`<div
        style=${(0,a.V)({backgroundImage:`url(${e})`})}
        class="picture"
      ></div>`;const t=(0,l.fm)(this.user.name);return r.dy`<div
      class="initials ${(0,o.$)({long:t.length>2})}"
    >
      ${t}
    </div>`}},{kind:"method",key:"_getPersonPicture",value:function(){if(this._personEntityId=void 0,this._personPicture=void 0,this.hass&&this.user)for(const e of Object.values(this.hass.states))if(e.attributes.user_id===this.user.id&&"person"===(0,s.N)(e)){this._personEntityId=e.entity_id,this._personPicture=e.attributes.entity_picture;break}}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: contents;
      }
      .picture {
        width: 40px;
        height: 40px;
        background-size: cover;
        border-radius: 50%;
      }
      .initials {
        display: inline-block;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--text-light-primary-color, var(--primary-text-color));
        overflow: hidden;
      }
      .initials.long {
        font-size: 80%;
      }
    `}}]}}),r.oi)},24833:(e,t,i)=>{i.d(t,{oF:()=>o,kK:()=>a,k6:()=>s,zG:()=>l,BD:()=>d,hF:()=>c,Sk:()=>h,UJ:()=>p});var r=i(49706),n=i(40095);const o=1,a=2,s=4,l=8,d=16,c=e=>e.state===r.uo&&(0,n.e)(e,o),h=e=>(e=>(0,n.e)(e,s)&&"number"==typeof e.attributes.in_progress)(e)||!!e.attributes.in_progress,p=(e,t)=>e.callWS({type:"update/release_notes",entity_id:t})},65253:(e,t,i)=>{i.d(t,{Pb:()=>r,CE:()=>n,uh:()=>o,r4:()=>a,Nq:()=>s,h8:()=>l,fm:()=>d,FH:()=>f});const r="system-admin",n="system-users",o=async e=>e.callWS({type:"config/auth/list"}),a=async(e,t,i,r)=>e.callWS({type:"config/auth/create",name:t,group_ids:i,local_only:r}),s=async(e,t,i)=>e.callWS({...i,type:"config/auth/update",user_id:t}),l=async(e,t)=>e.callWS({type:"config/auth/delete",user_id:t}),d=e=>e?e.trim().split(" ").slice(0,3).map((e=>e.substring(0,1))).join(""):"?",c=2143==i.j?"M12 2C6.47 2 2 6.5 2 12C2 17.5 6.5 22 12 22S22 17.5 22 12 17.5 2 12 2M12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4S20 7.58 20 12C20 16.42 16.42 20 12 20M8 14L7 8L10 10L12 7L14 10L17 8L16 14H8M8.56 16C8.22 16 8 15.78 8 15.44V15H16V15.44C16 15.78 15.78 16 15.44 16H8.56Z":null,h=2143==i.j?"M11,7H15V9H11V11H13A2,2 0 0,1 15,13V15A2,2 0 0,1 13,17H9V15H13V13H11A2,2 0 0,1 9,11V9A2,2 0 0,1 11,7M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z":null,p=2143==i.j?"M12 20C7.6 20 4 16.4 4 12S7.6 4 12 4 20 7.6 20 12 16.4 20 12 20M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M11 14H13V17H16V12H18L12 7L6 12H8V17H11V14":null,u=2143==i.j?"M12 2C17.5 2 22 6.5 22 12S17.5 22 12 22 2 17.5 2 12 6.5 2 12 2M12 4C10.1 4 8.4 4.6 7.1 5.7L18.3 16.9C19.3 15.5 20 13.8 20 12C20 7.6 16.4 4 12 4M16.9 18.3L5.7 7.1C4.6 8.4 4 10.1 4 12C4 16.4 7.6 20 12 20C13.9 20 15.6 19.4 16.9 18.3Z":null,f=(e,t,i)=>{const r=[],n=t=>e.localize(`ui.panel.config.users.${t}`);return t.is_owner&&r.push([c,n("is_owner")]),i&&t.system_generated&&r.push([h,n("is_system")]),t.local_only&&r.push([p,n("is_local")]),t.is_active||r.push([u,n("is_not_active")]),r}},93491:(e,t,i)=>{i.d(t,{K:()=>h});i(91156);var r=i(37500),n=i(57835),o=i(47181),a=i(36639);function s(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}const l="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0;class d extends HTMLElement{constructor(){super(),s(this,"holdTime",500),s(this,"ripple",void 0),s(this,"timer",void 0),s(this,"held",!1),s(this,"cancelled",!1),s(this,"dblClickTimeout",void 0),this.ripple=document.createElement("mwc-ripple")}connectedCallback(){Object.assign(this.style,{position:"absolute",width:l?"100px":"50px",height:l?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none",zIndex:"999"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((e=>{document.addEventListener(e,(()=>{this.cancelled=!0,this.timer&&(this.stopAnimation(),clearTimeout(this.timer),this.timer=void 0)}),{passive:!0})}))}bind(e,t={}){e.actionHandler&&(0,a.v)(t,e.actionHandler.options)||(e.actionHandler?(e.removeEventListener("touchstart",e.actionHandler.start),e.removeEventListener("touchend",e.actionHandler.end),e.removeEventListener("touchcancel",e.actionHandler.end),e.removeEventListener("mousedown",e.actionHandler.start),e.removeEventListener("click",e.actionHandler.end),e.removeEventListener("keyup",e.actionHandler.handleEnter)):e.addEventListener("contextmenu",(e=>{const t=e||window.event;return t.preventDefault&&t.preventDefault(),t.stopPropagation&&t.stopPropagation(),t.cancelBubble=!0,t.returnValue=!1,!1})),e.actionHandler={options:t},t.disabled||(e.actionHandler.start=e=>{let i,r;this.cancelled=!1,e.touches?(i=e.touches[0].pageX,r=e.touches[0].pageY):(i=e.pageX,r=e.pageY),t.hasHold&&(this.held=!1,this.timer=window.setTimeout((()=>{this.startAnimation(i,r),this.held=!0}),this.holdTime))},e.actionHandler.end=e=>{if(["touchend","touchcancel"].includes(e.type)&&this.cancelled)return;const i=e.target;e.cancelable&&e.preventDefault(),t.hasHold&&(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0),t.hasHold&&this.held?(0,o.B)(i,"action",{action:"hold"}):t.hasDoubleClick?"click"===e.type&&e.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"double_tap"})):(0,o.B)(i,"action",{action:"tap"})},e.actionHandler.handleEnter=e=>{13===e.keyCode&&e.currentTarget.actionHandler.end(e)},e.addEventListener("touchstart",e.actionHandler.start,{passive:!0}),e.addEventListener("touchend",e.actionHandler.end),e.addEventListener("touchcancel",e.actionHandler.end),e.addEventListener("mousedown",e.actionHandler.start,{passive:!0}),e.addEventListener("click",e.actionHandler.end),e.addEventListener("keyup",e.actionHandler.handleEnter)))}startAnimation(e,t){Object.assign(this.style,{left:`${e}px`,top:`${t}px`,display:null}),this.ripple.disabled=!1,this.ripple.startPress(),this.ripple.unbounded=!0}stopAnimation(){this.ripple.endPress(),this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler",d);const c=(e,t)=>{const i=(()=>{const e=document.body;if(e.querySelector("action-handler"))return e.querySelector("action-handler");const t=document.createElement("action-handler");return e.appendChild(t),t})();i&&i.bind(e,t)},h=(0,n.XM)(class extends n.Xe{update(e,[t]){return c(e.element,t),r.Jb}render(e){}})}}]);
//# sourceMappingURL=94824c05.js.map