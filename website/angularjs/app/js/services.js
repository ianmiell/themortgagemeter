'use strict';

/* Services */
angular.module('themortgagemeterbestmortgagesservice',['ngResource']).factory('MortgageComparisonBestMortgages', function($resource){
	return $resource('/rest/best_mortgages/:n_results/:mortgage_type/:eligibility/:institution_code/:ltv/:initial_period', {}, {
			query: {method:'GET', params:{n_results:'0', mortgage_type:'X',eligibility:'X', institution_code:'X', ltv:'0', initial_period:'0'}, isArray:true}
	});
});

angular.module('themortgagemeterconversionsservice',['ngResource']).factory('MortgageComparisonConversions', function($resource){
	return $resource('/rest/get_conversions/',{}, {
		query: {method:'GET',params:{},isArray:true}
	});
});


angular.module('themortgagemeterchangesservice',['ngResource']).factory('MortgageComparisonChanges', function($resource){
	return $resource('/rest/latest_n_changes/:n_changes/',{}, {
		query: {method:'GET',params:{n_changes:'0'},isArray:true}
	});
});


//switch to a post at some point?
angular.module('themortgagemetersubscribeservice',['ngResource']).factory('MortgageComparisonSubscribe', function($resource){
	return $resource('/rest/subscribe_email/:email_address/',{}, {
		//query: {method:'GET',params:{email_address:''},isArray:true}
		query: {method:'GET',params:{email_address:''}}
	});
});


