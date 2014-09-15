// Run like this:
// phantomjs <args> <file>
var page = require('webpage').create(), system = require('system'), fs = require('fs'), origin, dest, steps;
// args:
// propertyValue: 300000
// LTV tiers: "60","70","75","80","85","90","95","100":
// mortgageAmount: 180000, 210000, 225000, 240000, 255000, 270000, 285000, 300000
// ftb, nc-mh, nc-r, ec-mh, ec-bm, ec-de, ec-sf
if (system.args.length != 6) {
	//console.log('usage: ' + system.args[0] + ' [mortgage_type] [ltv] [mortgage_amount] [filename]');
	console.log('usage: ' + system.args[0] + ' [mortgage_type] [property_value] [mortgage_amount] [ltv] [filename] if ltv is 0, then we do not use it');
	phantom.exit();
}
mortgage_type   = system.args[1];
property_value  = system.args[2];
mortgage_amount = system.args[3];
ltv             = system.args[4];
filename        = system.args[5];
if (ltv != "0" && mortgage_type == "ec-bm") {
	url = 'http://www.nationwide.co.uk/mortgages/interestrates-types/rates.htm?buyerType=' + mortgage_type + '&loanToValueTier=' + ltv + '&mortgageAmount=' + mortgage_amount + '&mortgageTerm=25';
} else {
	url = 'http://www.nationwide.co.uk/mortgages/interestrates-types/rates.htm?buyerType=' + mortgage_type + '&propertyValue=' + property_value + '&mortgageAmount=' + mortgage_amount + '&mortgageTerm=25';
}
page.open(encodeURI(url), function (status) {
    if (status == 'success') {
		result = page.evaluate(function() {
			return document.getElementById('mortgageAjaxResults').innerHTML;
		});
//URL=http://www.nationwide.co.uk/Nationwide.Cms.WebApp/_ToolsAndCalculators/Mortgages/Rates/getMortgageRates.ashx?buyerType=ftb&loanToValueTier=60&productType=all&mortgageTerm=25&mortgageAmount=180000&submit=true
		// This can be then dumped into a file and read in as a BS object:
		//>>> res = BeautifulSoup(the_page,'html5')
		//console.log(result);
		//The mortgage amount is too high for the property value. <- if that's there, it's fine, just ignore and write NONE out
		if (result) {
			fs.write(filename, result, 'w');
		} else {
			//console.log('else');
			no_mortgages = page.content.match(/(The mortgage amount is too high for the property value.)/ig)
			if (no_mortgages) {
				fs.write(filename, 'NONE', 'w');
			} else {
				fs.write(filename, 'FAILED', 'w');
			}
		}
		fs.write('/tmp/content', url + '\n\n' + page.content, 'w');
		page.render('/tmp/content.pdf');
		phantom.exit();
    }
});
