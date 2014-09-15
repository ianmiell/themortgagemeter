array format ["OUR INPUT","Product","Maximum loan size formatted","Rate Type","Product Type","Eligibility","Customer Type","Benefit solution","Maximum LTV","Initial rate","Differential to BBR","Standard Variable Rate","APR","Maximum loan size","Booking fee","Charge end date"]]
/*
var productList = [
["N647H","2 yr Fixed Homebuyer","&pound;550k","Fixed","2 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.6","0.0264","n/a","0.0424","0.042","550000","995","2/1/2014"],
["N647R","2 yr Fixed Remortgage","&pound;550k","Fixed","2 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.6","0.0264","n/a","0.0424","0.042","550000","995","2/1/2014"],
["N648H","2 yr Fixed Homebuyer","&pound;1m","Fixed","2 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.7","0.0284","n/a","0.0424","0.042","1000000","995","2/1/2014"],
["N648R","2 yr Fixed Remortgage","&pound;1m","Fixed","2 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.7","0.0284","n/a","0.0424","0.041","1000000","995","2/1/2014"],

["N666H","2 yr Fixed Homebuyer","&pound;1m","Fixed","2 year Fixed rate","Non-loyalty","Mover|FTB","Free valuation and Â£250 cashback","0.75","0.0309","n/a","0.0424","0.042","1000000","995","2/1/2014"],
["N666R","2 yr Fixed Remortgage","&pound;1m","Fixed","2 year Fixed rate","Non-loyalty","Remortgage","Free valuation and standard legal fees paid","0.75","0.0309","n/a","0.0424","0.042","1000000","995","2/1/2014"],
["N667H","2 yr Fixed Homebuyer","&pound;1m","Fixed","2 year Fixed rate","All","Mover|FTB","Free valuation and Â£250 cashback","0.75","0.0344","n/a","0.0424","0.042","1000000","0","2/1/2014"],
["N667R","2 yr Fixed Remortgage","&pound;1m","Fixed","2 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.75","0.0344","n/a","0.0424","0.042","1000000","0","2/1/2014"],

["N651H","2 yr Fixed Homebuyer","&pound;550k","Fixed","2 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.8","0.0349","n/a","0.0424","0.043","550000","995","2/1/2014"],
["N651R","2 yr Fixed Remortgage","&pound;550k","Fixed","2 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.8","0.0349","n/a","0.0424","0.043","550000","995","2/1/2014"],
["N652H","2yr Fixed Homebuyer First Time Buyer ONLY","&pound;550k","Fixed","2 year Fixed rate","All","FTB only","Free valuation and &pound;250 cashback","0.85","0.0399","n/a","0.0424","0.044","550000","495","2/1/2014"],
["N657C","DIRECT 2 yr Fixed Core","&pound;350k","Fixed","2 year Fixed rate","All","Mover|FTB|Remortgage","none","0.6","0.0235","n/a","0.0424","0.041","350000","1995","2/1/2014"],
["N658H","DIRECT 2 yr Fixed Homebuyer","&pound;550k","Fixed","2 year Fixed rate","Non-loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.85","0.0399","n/a","0.0424","0.044","550000","995","2/1/2014"],
["N658R","DIRECT 2 yr Fixed Remortgage","&pound;550k","Fixed","2 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.85","0.0399","n/a","0.0424","0.044","550000","995","2/1/2014"],
["N659H","DIRECT 2 yr Fixed Homebuyer","&pound;300k","Fixed","2 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.9","0.0499","n/a","0.0424","0.045","300000","495","2/1/2014"],

["N670H","DIRECT ONLY 2yr Fixed Homebuyer Existing Customer","&pound;1m","Fixed","2 year Fixed rate","Loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0309","n/a","0.0424","0.042","1000000","745","2/1/2014"],
["N670R","DIRECT ONLY 2yr Fixed Remortgage Existing Customer","&pound;1m","Fixed","2 year Fixed rate","Loyalty","Remortgage","Free valuation and standard legal fees paid","0.75","0.0309","n/a","0.0424","0.042","1000000","745","2/1/2014"],

["N665H","DIRECT ONLY 2yr Fixed Homebuyer Existing Customer","&pound;550k","Fixed","2 year Fixed rate","Loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.85","0.0399","n/a","0.0424","0.043","550000","745","2/1/2014"],
["E707H","3 yr Fixed Homebuyer","&pound;1m","Fixed","3 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.7","0.0349","n/a","0.0424","0.041","1000000","0","2/1/2015"],
["E707R","3 yr Fixed Remortgage","&pound;1m","Fixed","3 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.7","0.0349","n/a","0.0424","0.041","1000000","0","2/1/2015"],

["E710H","3 yr Fixed Homebuyer","&pound;550k","Fixed","3 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0329","n/a","0.0424","0.041","550000","995","2/1/2015"],

["E708R","3 yr Fixed Remortgage","&pound;550k","Fixed","3 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.75","0.0369","n/a","0.0424","0.042","550000","0","2/1/2015"],
["E709H","3 yr Fixed Homebuyer","&pound;550k","Fixed","3 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.85","0.0419","n/a","0.0424","0.044","550000","495","2/1/2015"],
["G562H","4 yr Fixed First Time Buyer ONLY","&pound;550k","Fixed","4 year Fixed rate","All","FTB only","Free valuation and &pound;250 cashback","0.85","0.0449","n/a","0.0424","0.044","550000","495","2/1/2016"],
["K548H","5 yr Fixed Homebuyer","&pound;1m","Fixed","5 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.7","0.0379","n/a","0.0424","0.043","1000000","995","2/1/2017"],
["K548R","5 yr Fixed Remortgage","&pound;1m","Fixed","5 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.7","0.0379","n/a","0.0424","0.042","1000000","995","2/1/2017"],
["K549H","5 yr Fixed Homebuyer","&pound;550k","Fixed","5 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0399","n/a","0.0424","0.043","550000","995","2/1/2017"],
["K549R","5 yr Fixed Remortgage","&pound;550k","Fixed","5 year Fixed rate","All","Remortgage","Free valuation and standard legal fees paid","0.75","0.0399","n/a","0.0424","0.043","550000","995","2/1/2017"],
["K550H","5 yr Fixed Homebuyer","&pound;550k","Fixed","5 year Fixed rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.85","0.0489","n/a","0.0424","0.047","550000","995","2/1/2017"],
["K551H","5 yr Fixed First Time Buyer ONLY","&pound;250k","Fixed","5 year Fixed rate","All"," FTB only","Free valuation and &pound;250 cashback","0.9","0.0575","n/a","0.0424","0.05","250000","495","2/1/2017"],
["V623H","2 yr Tracker Homebuyer","&pound;1m","Tracker","2 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.7","0.0299","0.0249","0.0424","0.041","1000000","199","2nd anniversary"],
["U054R","TF 2 yr Tracker Remortgage","&pound;1m","Tracker","2 year Tracker rate","All","Remortgage","Free valuation and standard legal fees paid","0.7","0.0299","0.0249","0.0424","0.041","1000000","199","2nd anniversary"],
["V624H","2 yr Tracker Homebuyer","&pound;1m","Tracker","2 year Tracker rate","Non-loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.7","0.0264","0.0214","0.0424","0.041","1000000","995","2nd anniversary"],
["U055R","TF 2 yr Tracker Remortgage","&pound;1m","Tracker","2 year Tracker rate","Non-loyalty","Remortgage","Free valuation and standard legal fees paid","0.7","0.0264","0.0214","0.0424","0.04","1000000","995","2nd anniversary"],
["U051R","TF 2 yr Tracker Remortgage","&pound;550k","Tracker","2 year Tracker rate","Non-loyalty","Remortgage","Free valuation and standard legal fees paid","0.75","0.0275","0.0225","0.0424","0.041","550000","995","2nd anniversary"],
["V625H","2 yr Tracker Homebuyer","&pound;550k","Tracker","2 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.8","0.0329","0.0279","0.0424","0.042","550000","995","2nd anniversary"],
["V625R","2 yr Tracker Remortgage","&pound;550k","Tracker","2year Tracker rate","All","Remortgage","Free valuation and standard legal fees paid","0.8","0.0325","0.0275","0.0424","0.042","550000","995","2nd anniversary"],
["V595H","2 yr Tracker Homebuyer","&pound;550k","Tracker","2 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.85","0.0399","0.0349","0.0424","0.044","550000","995","2nd anniversary"],
["V595R","2 yr Tracker Remortgage","&pound;550k","Tracker","2 year Tracker rate","All","Remortgage","Free valuation and standard legal fees paid","0.85","0.0419","0.0369","0.0424","0.044","550000","995","2nd anniversary"],
["V626H","2 yr Tracker Homebuyer","&pound;300k","Tracker","2 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.9","0.0499","0.0449","0.0424","0.045","300000","495","2nd anniversary"],
["U044R","TF DIRECT 2 yr Tracker Remo","&pound;250k","Tracker","2 year Tracker rate","All","Remortgage","Free valuation and standard legal fees paid","0.6","0.0195","0.0145","0.0424","0.04","250000","1995","2nd anniversary"],
["V620H","DIRECT 2yr Tracker Homebuyer","&pound;550k","Tracker","2 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0275","0.0225","0.0424","0.041","550000","995","2nd anniversary"],
["V629H","DIRECT ONLY 2yr Tracker Homebuyer Existing Customer","&pound;1m","Tracker","2 year Tracker rate","Loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.7","0.0264","0.0214","0.0424","0.041","1000000","745","2nd anniversary"],
["U058R","TF DIRECT ONLY 2yr Tracker Remo Existing Customer","&pound;1m","Tracker","2 year Tracker rate","Loyalty","Remortgage","Free valuation and standard legal fees paid","0.7","0.0264","0.0214","0.0424","0.04","1000000","745","2nd anniversary"],
["U053R","TF DIRECT ONLY 2yr Tracker Remo Existing Customer","&pound;550k","Tracker","2 year Tracker rate","Loyalty","Remortgage","Free valuation and standard legal fees paid","0.75","0.0275","0.0225","0.0424","0.041","550000","745","2nd anniversary"],
["D174H","3 yr Tracker Homebuyer","&pound;550k","Tracker","3 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0299","0.0249","0.0424","0.04","550000","995","3rd anniversary"],
["U045R","TF 3 yr Tracker Remortgage","&pound;550k","Tracker","3 year Tracker rate","All","Remortgage","Free valuation and standard legal fees paid","0.75","0.0299","0.0249","0.0424","0.04","550000","995","3rd anniversary"],
["D172H","3 yr Tracker Homebuyer","&pound;550k","Tracker","3 year Tracker rate","All","Mover|FTB","Free valuation and &pound;250 cashback","0.8","0.0349","0.0299","0.0424","0.043","550000","995","3rd anniversary"],
["D172r","3 yr Tracker Remortgage","&pound;550k","Tracker","3 year Tracker rate","All","Remortgage","Free valuation and standard legal fees paid","0.8","0.0349","0.0299","0.0424","0.043","550000","995","3rd anniversary"],

<!-- updated rates -->
["N669L","Existing Customers Moving Home Exclusive 2yr Fixed Homebuyer","&pound;1m","Fixed","2 year Fixed rate","Loyalty","Mover","Free valuation and &pound;250 cashback","0.75","0.0309","n/a","0.0424","0.042","1000000","495","2 January 2014"],
["N660L","Existing Customers Moving Home Exclusive 2yr Fixed Homebuyer","&pound;550k","Fixed","2 year Fixed rate","Loyalty","Mover","Free valuation and &pound;250 cashback","0.80","0.0349","n/a","0.0424","0.042","550000","495","2 January 2014"],
["E709L","Existing Customers Moving Home Exclusive 3yr Fixed Homebuyer","&pound;550k","Fixed","3 year Fixed rate","Loyalty","Mover","Free valuation and &pound;250 cashback","0.85","0.0419","n/a","0.0424","0.043","550000","0","2 January 2014"],
["V628L","Existing Customers Moving Home Exclusive 3yr Tracker Homebuyer","&pound;1m","Tracker","2 year Tracker rate","Loyalty","Mover","Free valuation and &pound;250 cashback","0.70","0.0264","0.0214","0.0424","0.041","1000000","495","2 January 2014"],

<!-- end updated rates -->

<!-- flexible rates -->
["P199H","DIRECT ONLY Flexible Offset Homebuyer Existing Customer","&pound;1m","Flexible","Flexible Offset Lifetime Tracker rate","Loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0329","0.0279","n/a","0.034","1000000","745","Lifetime Tracker"],

["P199R","DIRECT ONLY Flexible Offset Homebuyer","&pound;1m","Flexible","Flexible Offset Lifetime Tracker rate","Loyalty","Remortgage","Free valuation and standard legal fees paid","0.75","0.0329","0.0279","n/a","0.034","1000000","745","Lifetime Tracker"],

["P187H","DIRECT Flexible Offset Homebuyer","&pound;1m","Flexible","Flexible Offset Lifetime Tracker rate","Non-loyalty","Mover|FTB","Free valuation and &pound;250 cashback","0.75","0.0329","0.0279","n/a","0.034","1000000","995","Lifetime Tracker"],

["P187R","DIRECT Flexible Offset Remortgage","&pound;1m","Flexible","Flexible Offset Lifetime Tracker rate","Non-loyalty","Remortgage","Free valuation and standard legal fees paid","0.75","0.0329","0.0279","n/a","0.034","1000000","995","Lifetime Tracker"]
<!-- end flexible rates -->

];
*/

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

var descriptionText = new Array();

descriptionText ["Fixed"]   = "<strong>Fixed rate</strong> - repayments remain the same during the fixed rate period, no matter what happens to interest rates.";

descriptionText ["Tracker"] = "<strong>Tracker rate</strong> - Your payments will increase or decrease in line with the Bank of England base rate. You will need to ensure you can afford any changes in payments.";

descriptionText ["Flexible"] = "<strong>Flexible Offset mortgage</strong> gives you added freedom. It allows you to offset your savings against your mortgage. So the more money there is in your savings pot, the less interest you'll be charged and you could pay off your mortgage earlier. Your payments will increase or decrease in line with the Bank of England base rate. You will need to ensure you can afford any changes in payments.";

var termText = new Array();

termText ["2Y-Fixed"]   = "A two year deal is one of the shortest fixed rate terms Santander offer. At the end of the fixed rate period, you will need to select a new deal or you will revert to our Standard Variable Rate (SVR). Your budget will need to accommodate any changes to your mortgage payments in two years time.";

termText ["2Y-Tracker"] = "Our tracker rates are available over two or three years. The rate tracks above  the Bank of England base rate during the tracker term. At the end of the tracker term you will need to select a new product, or you will revert to our Standard Variable Rate (SVR).";

termText ["3Y-Fixed"]   = "A three or four year fix rate deal provides you with a great choice of how long you would like to have fixed monthly payments for. At the end of the fixed rate period, you will need to select a new deal, or you will revert to our Standard Variable Rate (SVR).";

termText ["3Y-Tracker"] = termText ["2Y-Tracker"];

termText ["4Y-Fixed"]   = termText ["3Y-Fixed"];

termText ["4Y-Tracker"] = "Three and four years deals provide a balance between fixed rate peace of mind and the length of term you are tied in for.";

termText ["5Y-Fixed"]   = "These are currently the longest fixed rate deals Santander provides. You will know what your repayments will be over five years, giving you peace of mind. You will also benefit from only having paid one booking fee during the five year fixed rate period. However, at the end of the fixed rate period you will need to select a new deal or you will revert to our Standard Variable Rate (SVR).";

termText ["5Y-Tracker"] = "Five year deals provide the longest possible peace of mind with Santander for the fixed rate period. You will not have to pay any additional booking fees during this time.";

termText ["Flexible"] = "This is a Lifetime Tracker rate and means you needn't look for a new deal every few years.";
