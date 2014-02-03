(function(){var e=Object.prototype.hasOwnProperty,t=function(t,n){function i(){this.constructor=t}for(var r in n)e.call(n,r)&&(t[r]=n[r]);return i.prototype=n.prototype,t.prototype=new i,t.__super__=n.prototype,t};define(["require","underscore","backbone","text!templates/map/_searchbox.html","text!templates/map/_layersbox.html"],function(e){var n,r,i,s;return s=e("underscore"),n=e("backbone"),i=function(n){function r(){r.__super__.constructor.apply(this,arguments)}return t(r,n),r.prototype.events={"click .search":"onSearchBtnClick","change .location-type":"onTypeChange"},r.prototype.initialize=function(){return this.template=s.template(e("text!templates/map/_searchbox.html"))},r.prototype.render=function(){var e;return e=this.template(),this.$el.html(e),this},r.prototype.onTypeChange=function(){var e;return e=this.$(".location-type").val(),e==="address"?(this.$(".latLng-container").hide(),this.$(".address-container").show()):(this.$(".address-container").hide(),this.$(".latLng-container").show())},r.prototype.onSearchBtnClick=function(){var e,t;return t=this.$(".location-type").val(),e=t==="address"?this.$(".address").val():[parseFloat(this.$(".lat").val().replace(",",".")),parseFloat(this.$(".lng").val().replace(",","."))],this.search(t,e),!1},r.prototype.search=function(e,t){return e==null&&(e="address"),this.trigger("search",{type:e,position:t}),this},r}(n.View),r=function(n){function r(){r.__super__.constructor.apply(this,arguments)}return t(r,n),r.prototype.events={"click .layer .item":"toggleLayer","click .layer .collapser":"toggleSublist","click .feature":"highlightFeature"},r.prototype.initialize=function(){return this.template=s.template(e("text!templates/map/_layersbox.html"))},r.prototype.render=function(e){var t;return this.layers=e,t=this.template({layers:this.layers}),this.$el.html(t),this.$(".sublist").hide(),this},r.prototype.toggleLayer=function(e){var t,n,r,i;return t=this.$(e.currentTarget),i=t.attr("data-layer"),r=t.attr("data-visible")==="true",n=r?"hide":"show",this.trigger(n,i),t.attr("data-visible",!r),t.toggleClass("on off")},r.prototype.toggleSublist=function(e){var t,n;return t=this.$(e.currentTarget),n=t.parent().next(".sublist"),console.log(n),t.find("i").toggleClass("icon-chevron-right icon-chevron-down"),n.toggle()},r.prototype.highlightFeature=function(e){var t,n;return t=this.$(e.currentTarget),n=parseInt(t.attr("data-id")),this.trigger("highlight_feature",n)},r}(n.View),{SearchBoxView:i,LayersBoxView:r}})}).call(this);