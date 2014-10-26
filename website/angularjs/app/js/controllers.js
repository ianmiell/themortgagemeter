'use strict';

/* Controllers */
function MortgageListCtrl($scope,TheMortgageMeterBestMortgages,TheMortgageMeterConversions) {
	$scope.orderingchoice   = 'rate';
	$scope.ltvchoice        = '6000';
	$scope.n_results        = '0';
	$scope.mortgage_type    = 'X';
	$scope.eligibility      = 'X';
	$scope.institution_code = 'X';
	$scope.initial_period   = '0';
	$scope.conversions      = TheMortgageMeterConversions.query();
	$scope.dochange = function() {
		$scope.mortgages = TheMortgageMeterBestMortgages.query({n_results : $scope.n_results, ltv: $scope.ltvchoice, mortgage_type: $scope.mortgage_type, eligibility: $scope.eligibility, institution_code: $scope.institution_code, initial_period: $scope.initial_period});
	}
	$scope.dochange();
}

function MortgageChangesCtrl($scope,$http,TheMortgageMeterChanges,TheMortgageMeterSubscribe) {
	$scope.changes      = TheMortgageMeterChanges.query();
	$scope.email_result = ''
	$scope.dosubscribe = function() {
		$scope.email_result = TheMortgageMeterSubscribe.query({email_address : $scope.email});
	}
}

