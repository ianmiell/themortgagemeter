'use strict';

// Declare app level module which depends on filters, and services
var mortgagecomparison = angular.module('mortgagecomparison', ['mortgagecomparisonbestmortgagesservice','mortgagecomparisonconversionsservice','mortgagecomparisonchangesservice','mortgagecomparisonchangesfilter','mortgagecomparisonsubscribeservice']).config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/best_buys', {templateUrl: 'partials/best_buys.html', controller: MortgageListCtrl});
  $routeProvider.when('/latest_changes', {templateUrl: 'partials/latest_changes.html', controller: MortgageChangesCtrl});
  $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: MortgageListCtrl});
  $routeProvider.when('/graphs', {templateUrl: 'partials/graphs.html'});
  $routeProvider.otherwise({redirectTo: '/best_buys'});
}]);


