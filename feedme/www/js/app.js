// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'

$global = {
  'backend': 'http://54.149.190.97:8889',
  // 'backend': 'http://localhost:8889',
  // 'backend': '/feed',
};

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
     link: function(scope, elem, attr) {
         elem.on('load', function() {
            var w = elem.width,
                h = elem.height;

            var div = elem.parent();
            var translateDistance = (elem[0].width - window.innerWidth);
            div[0].style.right = '-' + translateDistance +'px'; // initial card position.
            

            setTimeout(function() {
              // div[0].classList.add('move');
              div[0].style['-webkit-transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
              div[0].style['transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
              div[0].style['-o-transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
              div[0].style['-ms-transform'] = 'translate3d(-' + translateDistance + 'px,0, 0)';
              div[0].style['transition'] = '10s';
              div[0].style['-webkit-transition'] = '10s';
              div[0].style['-moz-transition'] = '10s';
            }, 1000);
         });
     }
   };
})



.controller('CardsCtrl', function($scope, $state, $http, $ionicSwipeCardDelegate) {

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

  console.log('loading');
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
        if(feed.image.length == 0) continue;
        $global.cardData.push({
          'title': feed.title,
          'image': feed.image,
          'content': feed.content,
          'url': feed.link,
          'cardId': cardId
        })
        cardId += 1;
      }
      $scope.addCard();
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.cards = Array.prototype.slice.call($global.cardData, 0, 0);
  $scope.cardIndex = -1;

  $scope.cardSwiped = function(index) {

  };

  $scope.cardSwipedLeft = function(index) {
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
    $scope.cards.splice(0, 1);
  }

  $scope.cardSwipedRight = function(index) {
    var url = $global.cardData[index].url;
    var userid = getUserId(Ionic);
    $http.post($global.backend + '/swipe', {
      'userid': getUserId(Ionic),
      'link': url,
      'action': 'dislike'
    }).then(function successCallback(response) {
    }, function failureCallback(response) {
        console.error('swipe to like failed', response);
    });

    $scope.addCard();
    $scope.cards.splice(0, 1);
  }

  $scope.cardDestroyed = function(index) {
    
  };

  $scope.addCard = function() {
    if($scope.cardIndex + 1 < $global.cardData.length) {  
      $scope.cardIndex += 1; 

      var newCard = $global.cardData[$scope.cardIndex];    
      
      newCard.id = Math.random();
      $scope.cards.push(angular.extend({}, newCard));
      console.log('new card image', newCard.image);

      // preload next image in the stack.
      if($scope.cardIndex + 1 < $global.cardData.length) {
        var nextCard = $global.cardData[$scope.cardIndex + 1];
        var image = new Image();
        image.src = nextCard.image;
      }
    }
  }

})

.controller('CardCtrl', function($scope, $ionicSwipeCardDelegate) {
  $scope.goAway = function() {
    var card = $ionicSwipeCardDelegate.getSwipeableCard($scope);
    card.swipe();
  };
})

.controller('ContentCtrl', function($scope, $stateParams, $http) {
  console.log($global.cardData);
  for(var cardType of $global.cardData) { // find content with cardId.
    if(cardType.cardId == $stateParams.cardId) {
      $http.get($scope.url).then(function successCallback(response) {
        $scope.content = reponse.data;
        $scope.title = cardType.title;    
      }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
      
    }
  }

  $scope.swipe = function(direction) {
    window.history.go(-1);
  }
  
})

;
