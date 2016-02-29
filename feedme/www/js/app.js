// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'

$global = {};

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

  $global.cardTypes = [{
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

  $http({
    method: 'GET',
    url: 'http://54.149.190.97:8889/'
  }).then(function successCallback(response) {
      var feeds = response.data.feed;
      feeds.reverse(); // in reverse time order.
      $global.cardTypes = [];
      cardId = 0;
      for(var feed of feeds) {
        if(feed.image.length == 0) continue;
        $global.cardTypes.push({
          'title': feed.title,
          'image': feed.image,
          'content': feed.content,
          'cardId': cardId
        })
        cardId += 1;
      }
      $scope.cardSwiped();
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.cards = Array.prototype.slice.call($global.cardTypes, 0, 0);
  $scope.cardIndex = 0;

  $scope.cardSwiped = function(index) {
    $scope.addCard();
  };

  $scope.cardSwipedLeft = function(index) {
    // kick off the platform web client
    Ionic.io();

    // this will give you a fresh user or the previously saved 'current user'
    var user = Ionic.User.current();

    // if the user doesn't have an id, you'll need to give it one.
    if (!user.id) {
      user.id = Ionic.User.anonymousId();
      // user.id = 'your-custom-user-id';
    }

    //persist the user
    user.save();

    console.log('user id');
  }

  $scope.cardSwipedRight = function(index) {

  }

  $scope.cardDestroyed = function(index) {
    $scope.cards.splice(index, 1);
  };

  $scope.addCard = function() {
    if($scope.cardIndex < $global.cardTypes.length) {  
      var newCard = $global.cardTypes[$scope.cardIndex];    
      $scope.cardIndex += 1;  

      newCard.id = Math.random();
      $scope.cards.push(angular.extend({}, newCard));
      console.log('new card image', newCard.image);

      // preload next image in the stack.
      if($scope.cardIndex < $global.cardTypes.length) {
        var nextCard = $global.cardTypes[$scope.cardIndex];
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

.controller('ContentCtrl', function($scope, $stateParams) {
  console.log($global.cardTypes);
  for(var cardType of $global.cardTypes) { // find content with cardId.
    if(cardType.cardId == $stateParams.cardId) {
      $scope.content = cardType.content;
      $scope.title = cardType.title;
    }
  }

  $scope.swipe = function(direction) {
    window.history.go(-1);
  }
  
})

;
