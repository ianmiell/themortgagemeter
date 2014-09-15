var page = require('webpage').create(), system = require('system'), fs = require('fs'), origin, dest, steps;
if (system.args.length != 2) {
	console.log('usage: ' + system.args[0] + ' [url]');
	phantom.exit();
}
url   = system.args[1];
page.open(encodeURI(url), function (status) {
    if (status == 'success') {
	    	console.log(page.content);
		phantom.exit();
    }
});
