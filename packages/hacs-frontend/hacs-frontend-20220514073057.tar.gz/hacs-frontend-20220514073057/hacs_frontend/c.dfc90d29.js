import{a as t,H as e,e as i,m as o,$ as s,n as r}from"./main-2af83765.js";import{m as a}from"./c.d0af35b1.js";import"./c.80f50c51.js";import"./c.8bde5a37.js";import"./c.743a15a1.js";import"./c.d608b0a2.js";import"./c.7aca5ec5.js";let d=t([r("hacs-generic-dialog")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[i()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"header",value:void 0},{kind:"field",decorators:[i()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o(((t,e)=>null==t?void 0:t.find((t=>t.id===e))))},{kind:"method",key:"render",value:function(){if(!this.active||!this.repository)return s``;const t=this._getRepository(this.hacs.repositories,this.repository);return s`
      <hacs-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?a.html(this.content||"",t):a.html(this.content||""):this.content||""}
      </hacs-dialog>
    `}}]}}),e);export{d as HacsGenericDialog};
