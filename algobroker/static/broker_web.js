"use strict"
var app = angular.module('myApp', ['ui.bootstrap', 'ngTouch',
				   'ui.grid']);

app.run(function($rootScope) {
    $rootScope.log = "";
    var source = new EventSource('/subscribe');
    source.addEventListener("log", function(event) {
	var data = JSON.parse(event.data);
	$rootScope.log += data.level + ": " + data.msg + "\n";
	$rootScope.$apply();
    });
    $rootScope.clearLog = function() {
	$rootScope.log = '';
	$rootScope.$apply();
    };
});

app.directive('onReadFile', function ($parse) {
    return {
	restrict: 'A',
	scope: false,
	link: function(scope, element, attrs) {
	    element.bind('change', function(e) {
		var onFileReadFn = $parse(attrs.onReadFile);
		var reader = new FileReader();
		reader.onload = function() {
		    var fileContents = reader.result;
		    // invoke parsed function on scope
		    // special syntax for passing in data
		    // to named parameters
		    // in the parsed function
		    // we are providing a value for the property 'contents'
		    // in the scope we pass in to the function
		    scope.$apply(function() {
			onFileReadFn(scope, {
			    'contents' : fileContents
			});
		    });
		};
		reader.readAsText(element[0].files[0]);
	    });
	}
    };
});

function play(audio, times, ended) {
    if (times <= 0) {
	return;
    }
    var played = 0;
    audio.addEventListener("ended", function() {
	played++;
	if (played < times) {
	    audio.play();
	} else if (ended) {
	    ended();
	}
    });
    audio.play();
}

app.controller('customersCtrl', function($scope, $http) {
    $scope.loadData = function() {
	$http.get("/test-data").success(function (response) {
	    $scope.names =
		response.records;
	});
    };
    $scope.localAlert = function() {
	var audio = new Audio("/static/high.ogg");
	play(audio, 3);
    };
    $scope.publish = function() {
	$http.get("/publish").success(function (response) {
	});
    };
});

app.controller('injectCtrl', function($scope, $http) {
    $scope.displayFileContents = function(contents) {
	$scope.textinput = contents;
    };
    $scope.injectData = function() {
	$http.post("/inject-data",
		   JSON.parse($scope.textinput),
		   {"headers": {
		       "context-type" :
		       "application/json"}}).success(function (response) {
			   $scope.result = "done";
		       });
    };
    $scope.injectControl = function() {
	$http.post("/inject-control",
		   JSON.parse($scope.textinput),
		   {"headers": {"context-type" :
				"application/json"}}).success(function (response) {
				    $scope.result = "done";
				});
    };
});

app.controller('TabsDemoCtrl', function ($scope, $window) {
});

app.controller('gridCtrl', function($scope) {
    $scope.myData = [
	{
	    "firstName" : "Cox",
	    "lastName" : "Carney"
	}
    ];
});
