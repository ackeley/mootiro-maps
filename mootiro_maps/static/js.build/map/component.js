(function(){define(["require","jquery"],function(e){var t,n,r;return t=e("jquery"),n=function(){function e(e,n){this.mediator=e,this.el=n,this.map=this.mediator,this.el&&(this.$el=t(document).find(this.el))}return e.prototype.name="Base Component",e.prototype.description="",e.prototype.hooks={},e.prototype.enabled=!1,e.prototype.setMap=function(e){this.map=e},e.prototype.enable=function(){return this.enabled=!0},e.prototype.disable=function(){return this.enabled=!1},e.prototype.init=function(e){return t.when(e)},e.prototype.destroy=function(){return!0},e}(),r=n,r})}).call(this);