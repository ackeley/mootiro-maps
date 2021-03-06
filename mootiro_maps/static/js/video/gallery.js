(function () {
  var youtubeQueue;
  var youtubePlayer;
  var vimeoQueue;
  var vimeoPlayer;
  var playerWidth = 400;
  var playerHeight = 266;

  var VideoGallery = function () {
    var that = this;
    $(".video-entry").live("click", function (ev) {
      var $this = $(this);
      var service = $this.attr('data-service');
      var video_id = $this.attr('data-video-id');

      that.play(service, video_id);
    });
  };

  window.VideoGallery = VideoGallery;

  VideoGallery.prototype.addVideo = function (video) {
    var $videoList = $("#video-gallery-player-list");

    // Create the player for first video
    if ($videoList.children().length == 0) {
      this.createPlayer(video.service, video.video_id, false);
    }

    var title = video.title;
    var description = video.description;

    if (title.length > 40) {
        title = title.substr(0, 35) + '...';
    }
    if (description.length > 25) {
        description = description.substr(0, 22) + '...';
    }

    var $videoEntry = '<li class="video-entry" id="' +
    'video_' + video.id + '" data-service="' +
    video.service + '" data-video-id="' +
    video.video_id + '" title="' +
    video.title + '\n\n' + video.description + '"><img class="video-thumb" src="' +
    video.thumbnail_url + '"><span class="video-title">' +
    title + '</span><span class="video-description">' +
    description + '</span></li>'
    $videoList.append($videoEntry);
  };

  VideoGallery.prototype.play = function (service, video_id) {
    if (this.currentVideo.service != service) {
      this.stop();
    }
    if (service == 'YT') {
      this.playYoutube(video_id);
    } else if (service == 'VI') {
      this.playVimeo(video_id);
    }
    this.currentVideo = { service: service, video_id: video_id };

  };

  VideoGallery.prototype.stop = function () {
    if (!this.currentVideo) return;

    if (this.currentVideo.service == 'YT') {
      this.stopYoutube();
    } else if (this.currentVideo.service == 'VI') {
      this.stopVimeo();
    }
  };

  VideoGallery.prototype.playYoutube = function (video_id) {
    if (!youtubePlayer) {
      if (this.youtubeInitialized) {
        youtubeQueue = video_id;
      } else {
        this.createYoutubePlayer(video_id, true);
      }
    } else {
      $(youtubePlayer).height(playerHeight);
      youtubePlayer.loadVideoById(video_id, 0, "large");
    }
  };

  VideoGallery.prototype.stopYoutube = function (video_id) {
    if (!youtubePlayer) return;

    youtubePlayer.stopVideo();
    $(youtubePlayer).height(0);
  };

  VideoGallery.prototype.playVimeo = function (video_id) {
    if (this.currentVideo.video_id == video_id) {
      vimeoPlayer.api_play()
    } else {
      // We cant load a new video using the same vimeo player, so lets remove it
      // and create a new one.
      $('#vimeoplayer').remove();
      $('#video-gallery-player').append('<div id="vimeoplayer"></div>');
      this.createVimeoPlayer(video_id, true);
    }
  };

  VideoGallery.prototype.stopVimeo = function (video_id) {
    if (!vimeoPlayer) return;
    vimeoPlayer.api_pause();
    $(vimeoplayer).hide();
  };

  VideoGallery.prototype.createPlayer = function (service, video_id, autoplay) {
    this.currentVideo = { service: service, video_id: video_id };
    if (service == 'YT') {
      this.createYoutubePlayer(video_id, autoplay);
    } else if (service == 'VI') {
      this.createVimeoPlayer(video_id, autoplay);
    }

  };

  VideoGallery.prototype.createYoutubePlayer = function (video_id, autoplay) {
    if (this.youtubeInitialized || !video_id) return;

    if (autoplay) {
      youtubeQueue = video_id;
    }
    var params = { allowScriptAccess: "always" };
    var atts = { id: "youtubeplayer" };
    swfobject.embedSWF("http://www.youtube.com/v/" + video_id + "?version=3&enablejsapi=1",
                       "youtubeplayer", playerWidth.toString(), playerHeight.toString(), "8", null, null, params, atts);
    this.youtubeInitialized = true;
  };

  VideoGallery.prototype.createVimeoPlayer = function (video_id, autoplay) {
    if (!video_id) return;

    if (autoplay) {
      autoplay = 1;
    } else {
      autoplay = 0;
    }

    var vars = {'clip_id': video_id,'server': 'vimeo.com','show_title': 1,'show_byline': 0,'show_portrait': 0,'fullscreen': 1,'js_api': 1,'autoplay': autoplay};
    var params  = {'swliveconnect':true,'fullscreen': 0,'allowscriptaccess': 'always','allowfullscreen':true,'wmode':'opaque'};
    var atts = { };
    swfobject.embedSWF("http://vimeo.com/moogaloop.swf",
        "vimeoplayer", playerWidth.toString(), playerHeight.toString(), "9.0.0", null, vars, params, atts);

    this.vimeoInitialized = true;
  };

  window.onYouTubePlayerReady = function (playerid) {
    youtubePlayer = document.getElementById("youtubeplayer");
    if (youtubeQueue) {
      youtubePlayer.loadVideoById(youtubeQueue, 0, "large");
    }
  };

  window.vimeo_player_loaded = function (){
    vimeoPlayer = document.getElementById('vimeoplayer');
  };
})();
