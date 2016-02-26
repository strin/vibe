// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('starter', ['ionic', 'ionic.contrib.ui.cards'])

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
            div[0].style.right = '-' + (elem[0].width - window.innerWidth) +'px';
            

            setTimeout(function() {
              div[0].classList.add('move');
              div[0].style['transition'] = '5s';
              div[0].style['-webkit-transition'] = '5s';
              div[0].style['-moz-transition'] = '5s';
            }, 1000);
         });
     }
   };
})


.controller('CardsCtrl', function($scope, $http, $ionicSwipeCardDelegate) {

  $scope.cardTypes = [{
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
      $scope.cardTypes = [];
      cardId = 0;
      for(var feed of feeds) {
        if(feed.image.length == 0) continue;
        $scope.cardTypes.push({
          'title': feed.title,
          'image': feed.image,
          'cardId': cardId
        })
        cardId += 1;
      }
      $scope.cardSwiped();
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.cards = Array.prototype.slice.call($scope.cardTypes, 0, 0);
  $scope.cardIndex = 0;

  $scope.cardSwiped = function(index) {
    $scope.addCard();
  };

  $scope.cardDestroyed = function(index) {
    $scope.cards.splice(index, 1);
  };

  $scope.addCard = function() {
    var newCard = $scope.cardTypes[$scope.cardIndex];
    if($scope.cardIndex + 1 < $scope.cardTypes.length) {
      $scope.cardIndex += 1;
    }
    newCard.id = Math.random();
    $scope.cards.push(angular.extend({}, newCard));
    console.log('new card image', newCard.image);
  }
})

.controller('CardCtrl', function($scope, $ionicSwipeCardDelegate) {
  $scope.goAway = function() {
    var card = $ionicSwipeCardDelegate.getSwipeableCard($scope);
    card.swipe();
  };
});
