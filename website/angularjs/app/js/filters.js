'use strict';

/* Filters */

// Takes the return values of the last_n_changes call and produces a table of changes.
angular.module('themortgagemeterchangesfilter', []).filter('change_filter', function() {
	return function(change_items) {
		var div, i, j, k, col, change_item, row, better, field;
		var col_list = ['rate_display','svr_display','apr_display','ltv_display','institution_name','eligibility_display','mortgage_type_display','booking_fee_display','initial_period_display'];
		// Ordering is important.
		var comparison_list = ['rate','apr','booking_fee'];
		div = '<table class="table table-condensed table-striped table-bordered table-hover"><thead><tr><td><b>Change Date</b></td><td><b>Headline Rate</b></td><td><b>SVR</b></td><td><b>APR</b></td><td><b>Loan to Value</b></td><td><b>Lender</b></td><td><b>Eligibility</b></td><td><b>Rate Type</b></td><td><b>Fees</b></td><td><b>Initial Rate Period</b></td></tr></thead><tbody>';
		for (i in change_items) {
			change_item = change_items[i]
			if (change_item['mortgage_type']) {
				// <tr> element is prepended at the end.
				// Sort out date
				row = '';
				row += '<td>' + change_item['change_date_display']['shared'] + '</td>';
				for (i=0;i<col_list.length;i++) {
					col=col_list[i];
					row += '<td>';
					if (change_item[col]['shared']) {
						row += change_item[col]['shared'][0];
					} else {
						for (j in change_item[col]['old']) {
							row += '<strike>' + change_item[col]['old'][j] + '</strike>' + ' ';
						}
						for (j in change_item[col]['new']) {
							row += change_item[col]['new'][j] + ' ';
						}
					}
					row += '</td>';
				}
				// Work out whether it's "better" or "worse" for the mortgage customer.
				better = '';
				for (i=0;i<comparison_list.length;i++) {
					col=comparison_list[i];
					//We are doing in order of importance, so break when set.
					if (!change_item[col]['shared']) {
						for (j=0;j < change_item[col]['old'].length && j < change_item[col]['new'].length; j++) {
							//console.log(i + ' ' + j + ' ' + change_item[col]['old'][j] + ' ' + change_item[col]['new'][j])
							if (change_item[col]['old'][j] > change_item[col]['new'][j]) {
								better = true;
								break;
							} else if (change_item[col]['old'][j] < change_item[col]['new'][j]) {
								better = false;
								break;
							} else {
								// they are equal; let's continue
							}
						}
					}
					if (better != '') { break; }
				}
				//console.log('better:' + better)
				if (better == true) {
					row = '<tr style="color: green">' + row;
				} else if (better == false) {
					row = '<tr style="color: red">' + row;
				} else {
					row = '<tr>' + row;
				}
				row += '</tr>';
				//console.log(row);
				div += row;
			} else if (change_item['old_mortgage'] || change_item['new_mortgage']) {
				if (change_item['old_mortgage']) {
					field = 'old_mortgage';
				} else if (change_item['new_mortgage']) {
					field = 'new_mortgage';
				}
				if (field == 'new_mortgage') {
					//console.log(change_item[field][0]['change_date_display']);
				}
				row = '<tr>';
				row += '<td>';
				if (field == 'old_mortgage') {row += '<strike>'}
				row += change_item[field][0]['change_date_display'];
				if (field == 'old_mortgage') {row += '</strike>'}
				row += '</td>';
				for (i=0;i<col_list.length;i++) {
					row += '<td>';
					if (field == 'old_mortgage') {row += '<strike>'}
					col=col_list[i];
					row += change_item[field][0][col];
					if (field == 'old_mortgage') {row += '</strike>'}
					row += '</td>';
				}
				row += '</tr>';
				div += row;
			}
		}
		return div;
	};
});

