'use strict';

/* Controllers */
function MortgageListCtrl($scope,MortgageComparisonBestMortgages,MortgageComparisonConversions) {
	$scope.orderingchoice   = 'rate';
	$scope.ltvchoice        = '6000';
	$scope.n_results        = '0';
	$scope.mortgage_type    = 'X';
	$scope.eligibility      = 'X';
	$scope.institution_code = 'X';
	$scope.initial_period   = '0';
	$scope.conversions      = MortgageComparisonConversions.query();
	$scope.dochange = function() {
		$scope.mortgages = MortgageComparisonBestMortgages.query({n_results : $scope.n_results, ltv: $scope.ltvchoice, mortgage_type: $scope.mortgage_type, eligibility: $scope.eligibility, institution_code: $scope.institution_code, initial_period: $scope.initial_period});
	}
	$scope.dochange();
}

function MortgageChangesCtrl($scope,$http,MortgageComparisonChanges,MortgageComparisonSubscribe) {
	$scope.changes      = MortgageComparisonChanges.query();
	$scope.email_result = ''
	$scope.dosubscribe = function() {
		$scope.email_result = MortgageComparisonSubscribe.query({email_address : $scope.email});
	}
}

