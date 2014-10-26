'use strict';

/* Directives */

// Not used and never working - kept here for future reference.
//themortgagemeter.directive('chart', function() {
//    return {
//		//restrict: 'EA' if you want it available as an attribute as well (ng-chart, presumably!)
//        restrict: 'E',
//        link: function(scope, elem, attrs) {
//			var chart = null, opts = { };
//			scope.$watch(attrs.ngModel, function(v){
//				alert(v);
//        		if(!chart){
//        		    chart = $.plot(elem, v , opts);
//        		    elem.show();
//        		}else{
//        		    chart.setData(v);
//        		    chart.setupGrid();
//        		    chart.draw();
//        		}
//			});
//        }
//    };
//});
