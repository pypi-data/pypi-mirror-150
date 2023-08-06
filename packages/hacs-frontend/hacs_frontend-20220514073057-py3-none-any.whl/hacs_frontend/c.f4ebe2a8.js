import{a as e,f as t,e as i,i as n,$ as o,O as r,Q as a,r as d,n as l}from"./main-2af83765.js";import"./c.d84e7514.js";e([l("ha-button-menu")],(function(e,t){class l extends t{constructor(...t){super(...t),e(this)}}return{F:l,d:[{kind:"field",decorators:[i()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[i()],key:"menuCorner",value:()=>"START"},{kind:"field",decorators:[i({type:Number})],key:"x",value:void 0},{kind:"field",decorators:[i({type:Number})],key:"y",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[n("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return o`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .menuCorner=${this.menuCorner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
        .y=${this.y}
        .x=${this.x}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"firstUpdated",value:function(e){r(a(l.prototype),"firstUpdated",this).call(this,e),"rtl"===document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),t);
