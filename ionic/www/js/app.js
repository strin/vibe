// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'

$global = {
  'backend': 'http://54.149.190.97:8889',
  // 'backend': 'http://localhost:8889',
  // 'backend': '/feed',
};

var push = new Ionic.Push({});

push.register(function(token) {
  // Log out your device token (Save this!)
  console.log("Got Token:",token.token);
});

angular.module('starter', ['ionic','ionic.service.core', 'ionic.contrib.ui.cards'])

.config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  // setup an abstract state for the tabs directive
  .state('content', {
    url: '/content/:cardId',    
    templateUrl: 'templates/content.html',
    controller: 'ContentCtrl'
  })

  .state('main', {
    url: '/',    
    templateUrl: 'templates/main.html',
    controller: 'CardsCtrl'
  });

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/');

  $ionicConfigProvider.backButton.text('').icon('ion-chevron-left');
})

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if (window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

.directive('noScroll', function($document) {

  return {
    restrict: 'A',
    link: function($scope, $element, $attr) {

      $document.on('touchmove', function(e) {
        e.preventDefault();
      });
    }
  }
})

.directive('pan', function(){ 
   return {
     restrict: 'A',
     link: function($scope, $elem, $attr) {

      var setStyle = function () {
        // basic parameters.
        var windowHeight = window.innerHeight, 
          windowWidth = window.innerWidth;

        // get content meta data.
        if($scope.card.type == 'video') { // video.
          var h = $elem[0].videoHeight;
          var w = $elem[0].videoWidth;
        }else{ // album or images.
          var h = $elem[0].naturalHeight;
          var w = $elem[0].naturalWidth;
        }

        var ratio = w / h;

        console.log('elem', $elem, 'ratio', ratio, 'scope', $scope.card);

        // if it's a vertical card, then scale to fit screen width.
        // if it's a horizontal card, then scale ti fit 75% screen height.
        if(ratio < 1) {
          var contentWidth = windowWidth;
          var contentLeft = 0;
          var cardHeight = windowWidth / ratio;
          var cardTop = -(cardHeight - windowHeight) / 2;
        }else{
          var cardHeight = 0.75 * windowHeight;
          var cardTop = windowHeight / 2 - cardHeight / 2;
          var contentWidth = cardHeight * ratio;
          var contentLeft = -(contentWidth - windowWidth) / 2;
        }
        var div = $elem.parent();
        
        // var card = document.getElementById('cardCtrl');
        var card = div.parent().parent().parent();
        console.log('card tag', card[0].tagName);
        while(card.tagName != 'SWIPE-CARD' && card.tagName != null) {
          card = card.parent();
        }
        console.log('card parent', card);
        card = card[0];

        div[0].style['width'] = contentWidth + 'px';
        // div[0].style['left'] = contentLeft + 'px';  
        card.style['width'] = windowWidth + 'px';
        card.style['height'] = cardHeight + 'px';
        card.style['top'] = cardTop + 'px';  

        // translation effect.
        var translateDistance = ($elem[0].width - windowWidth);
        div[0].style['right'] = '-' + translateDistance +'px';

        setTimeout(function() {
          div[0].style['-webkit-transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
          div[0].style['transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
          div[0].style['-o-transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
          div[0].style['-ms-transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
          div[0].style['transition'] = '10s';
          div[0].style['-webkit-transition'] = '10s';
          div[0].style['-moz-transition'] = '10s';
        }, 1000);

        console.log('[card] loaded');
        // load summary async.
        $scope.loadSummary($scope.card);

        // preload next image in the stack.
        if($scope.cardIndex + 1 < $global.cardData.length) {
          var nextCard = $global.cardData[$scope.cardIndex + 1];
          var image = new Image();
          image.src = nextCard.data.cover;
        }

        // fade loading text.
        document.getElementById("loading-text").style.opacity = 0.;
      }

      $elem.on('error', function() {
        console.log('add card failed');
        $scope.cardSwipedLeft($scope.cardIndex);
      });

      $elem[0].addEventListener('loadedmetadata', function() {
       setStyle();
      });
      $elem.on('load', function() {
       setStyle();
      });
     }
   };
})



.controller('CardsCtrl', function($scope, $state, $http, $ionicSwipeCardDelegate, $sce, $ionicModal, $compile) {

  $global.cardData = [{
    title: 'Swipe down to clear the card',
    image: 'img/pic.png'
  }, {
    title: 'Where is this?',
    image: 'img/pic.png'
  }, {
    title: 'What kind of grass is this?',
    image: 'img/pic2.png'
  }, {
    title: 'What beach is this?',
    image: 'img/pic3.png'
  }, {
    title: 'What kind of clouds are these?',
    image: 'img/pic4.png'
  }];

  $http.get($global.backend + '/vibes', {
    params: {
      userid: getUserId(Ionic)
    }
  }).then(function successCallback(response) {
      var feeds = response.data.feed;
      feeds.reverse(); // in reverse time order.
      $global.cardData = [];
      cardId = 0;

      for(var feed of feeds) {

        if(feed.type == 'video') {
          feed.data = $sce.trustAsResourceUrl(feed.data);
        }else if(feed.type == 'album') {
          feed.data = JSON.parse(feed.data);
          for(var pic of feed.data) {
            pic.url = $sce.trustAsResourceUrl(pic.url);
          }
          feed.cover = feed.data[0].url;
        }else if(feed.type == 'article') {
          feed.data = JSON.parse(feed.data);
          if(feed.data.cover == null) { // hide cards without cover.
            continue;
          }
        }

        feed.cardId = cardId;
        feed.url = feed.link;

        $global.cardData.push(feed);
        cardId += 1;
      }

      $scope.addCard();
      console.log('scope cards', $scope.cards);
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.cards = Array.prototype.slice.call($global.cardData, 0, 0);
  $scope.cardIndex = -1;


  $scope.cardSwiped = function(index) {

  };

  $scope.loadSummary = function(card) {
    var url = card.url;
    $http.get($global.backend + '/summary', {
      params: {
        'url': url
      }
    }).then(function successCallback(response) {
      console.log('summaary:', response);
      card.summaries = response.data.summaries;
      if(card.summaries.length > 0) {
        card.summary = card.summaries[0];
        var titleEls = document.getElementsByClassName('title');
        var titleContentEls = document.getElementsByClassName('title-content');
        console.log('titles', document.getElementsByClassName('title'));
        var titleEl = titleEls[titleEls.length - 1];
        var titleContentEl = titleContentEls[titleContentEls.length - 1];
        titleEl.style['padding-top'] = '100px';
        titleContentEl.style['-webkit-transform'] = 'translate3d(0,-70px, 0)';
        titleContentEl.style['-webkit-transition'] = '0.5s';
      }
    }, function failureCallback(response) {
        
    });
  }


  $scope.showModal = function(templateUrl, url) {
    $ionicModal.fromTemplateUrl(templateUrl, {
      scope: $scope,
    }).then(function(modal) {
      $scope.modal = modal;
      $scope.url = url;
      $scope.modal.show();
    });
  }
   
  $scope.closeModal = function() {
    $scope.modal.hide();
    $scope.modal.remove()
  };

  $scope.showImage = function(card) {
    if(card.type == 'album') {
      // $scope.showModal('templates/albumview.html', card); // deprecated.
    }else if(card.type == 'video') {
      var elem = document.getElementById("cardVideo");
      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
      } else if (elem.mozRequestFullScreen) {
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
      }
    }else if(card.type == 'image') {
      $scope.showModal('templates/imgview.html', card.url);
    }else if(card.type == 'article') {
      $state.go('content', 
        {cardId: card.cardId}
      );
    }
  }

  $scope.removeCard = function() {
    setTimeout(function() {
      $scope.cards.splice(0, 1);  
    }, 500); // wait a couple of milliseconds for animation to complete.
  }

  $scope.cardSwipedLeft = function(index) {
    var url = $global.cardData[index].url;
    var userid = getUserId(Ionic);
    $http.post($global.backend + '/swipe', {
      'userid': getUserId(Ionic),
      'link': url,
      'action': 'dislike'
    }).then(function successCallback(response) {
    }, function failureCallback(response) {
        console.error('swipe to dislike failed', response);
    });

    $scope.addCard();
    $scope.removeCard();
  }

  $scope.cardSwipedRight = function(index) {
    var url = $global.cardData[index].url;
    var userid = getUserId(Ionic);
    $http.post($global.backend + '/swipe', {
      'userid': getUserId(Ionic),
      'link': url,
      'action': 'like'
    }).then(function successCallback(response) {
    }, function failureCallback(response) {
        console.error('swipe to like failed', response);
    });

    $scope.addCard();
    $scope.removeCard();
  }

  $scope.cardDestroyed = function(index) {
    
  };

  $scope.addCard = function() {
    console.log('[card] adding new card');
    document.getElementById("loading-text").style.opacity = 1.;

    if($scope.cardIndex + 1 < $global.cardData.length) {  
      $scope.cardIndex += 1; 

      var newCard = $global.cardData[$scope.cardIndex];    
      
      newCard.id = Math.random();
      
      $scope.cards.push(angular.extend({}, newCard));

    }else{
      console.log('all cards finished');
      document.getElementById('loading-text').innerHTML = "<h1>Wow, you've read all.</h1>"
    }
  }

})

.controller('CardCtrl', function($scope, $ionicSwipeCardDelegate) {
  $scope.goAway = function() {
    var card = $ionicSwipeCardDelegate.getSwipeableCard($scope);
    card.swipe();
  };
})

.controller('ContentCtrl', function($scope, $stateParams, $http, $compile, $ionicModal) {
  for(var cardType of $global.cardData) { // find content with cardId.
    if(cardType.cardId == $stateParams.cardId) {
      // $http.get(cardType.url).then(function successCallback(response) {
      //   $scope.content = reponse.data;
      //   $scope.title = cardType.title;    
      // }, function errorCallback(response) {
      //   // called asynchronously if an error occurs
      //   // or server returns response with an error status.
      // });

      $scope.content = cardType.data.content;
      $scope.title = cardType.title;
      
      $scope.showModal = function(templateUrl, url) {
        $ionicModal.fromTemplateUrl(templateUrl, {
          scope: $scope,
        }).then(function(modal) {
          $scope.modal = modal;
          $scope.url = url;
          $scope.modal.show();
        });
      };
       
      $scope.closeModal = function() {
        $scope.modal.hide();
        $scope.modal.remove()
      };


      $scope.showImageModal = function(url) {
        console.log('show image modal');
        $scope.showModal("templates/imgview.html", url);
      }

      function checkContentLoaded() {
        var vibeContent = document.getElementById('vibe-content');
        if(vibeContent.innerHTML.length == 0) {
          setTimeout(checkContentLoaded, 30);
          return;
        }
        var contentLinks = document.querySelectorAll('.vibe-content a');
        console.log('contentLinks', contentLinks);
        for(var ci = 0; ci < contentLinks.length; ci++) {
          var link = contentLinks[ci];
          link.setAttribute('target', '_blank');
        }

        // add image modal events.
        var imageLinks = document.querySelectorAll('.vibe-content figure img');
        for(var ci = 0; ci < imageLinks.length; ci++) {
          var link = imageLinks[ci];
          var src = link.getAttribute('src');
          link.setAttribute("ng-controller", "CardCtrl");
          link.setAttribute("ng-click", "showImageModal('" + src + "')");
        }

        // to enable the ng-click events, we need to compile 
        var figures = document.querySelectorAll('.vibe-content figure');
        for(var ci = 0; ci < figures.length; ci++) {
          $compile(figures[ci])($scope);
        }
      }
      checkContentLoaded();
    }
  }

  $scope.swipe = function(direction) {
    window.history.go(-1);
  }
  
})

;
