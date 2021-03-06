import os
import re
import xml
import xlwt
import requests
import html2text
from datetime import datetime
from bs4 import BeautifulSoup
from EmailDigestAPI import EmailDigestAPI

LA_HONDA_ALERTS_URLS = {

"https://www.google.com/alerts/feeds/01881685235415088200/785900736969966737": "3D Cart", 	
"https://www.google.com/alerts/feeds/01881685235415088200/15034893427377033339": "AppViewX",	
"https://www.google.com/alerts/feeds/01881685235415088200/3945196334568906320": "Allgress",	
"https://www.google.com/alerts/feeds/01881685235415088200/3895053026711783394": "Shadow Networks",	
"https://www.google.com/alerts/feeds/01881685235415088200/3895053026711781846": "RISC Networks",	
"https://www.google.com/alerts/feeds/01881685235415088200/16006159606632332629": "Madison Performance Group",	
"https://www.google.com/alerts/feeds/01881685235415088200/8293954029489445377": "Insight Sourcing Group",	
"https://www.google.com/alerts/feeds/01881685235415088200/499494254267437494": "Gorilla Group",	
"https://www.google.com/alerts/feeds/01881685235415088200/15590179751007293445": "G5 Marketing Cloud",	
"https://www.google.com/alerts/feeds/01881685235415088200/14010574549286786110": "Choozle",	
"https://www.google.com/alerts/feeds/01881685235415088200/5381574193926782161": "Carta Worldwide",	
"https://www.google.com/alerts/feeds/01881685235415088200/5381574193926782957": "CardCompliant",
"https://www.google.com/alerts/feeds/01881685235415088200/2074340360614458331": "Boardwalktech inc.",
"https://www.google.com/alerts/feeds/01881685235415088200/3592935426912946183": "AppVision",	
"https://www.google.com/alerts/feeds/01881685235415088200/16471529239774348669": "Allbound",	
"https://www.google.com/alerts/feeds/01881685235415088200/6867016919574609150": "AirVM",	
"https://www.google.com/alerts/feeds/01881685235415088200/6867016919574608947": "Kollective",	
"https://www.google.com/alerts/feeds/01881685235415088200/270940976034452635": "Frost & Sullivan",	
"https://www.google.com/alerts/feeds/01881685235415088200/7895182236465595993": "Atheer",	
"https://www.google.com/alerts/feeds/01881685235415088200/7895182236465598351": "On-site.com",	
"https://www.google.com/alerts/feeds/01881685235415088200/3736136606611410344": "Solar Universe",	
"https://www.google.com/alerts/feeds/01881685235415088200/3705460014693924276": "Persio",	
"https://www.google.com/alerts/feeds/01881685235415088200/8159947520343534399": "Nextpoint",	
"https://www.google.com/alerts/feeds/01881685235415088200/499494254267440870": "Load Delivered",	
"https://www.google.com/alerts/feeds/01881685235415088200/499494254267437666": "L2T Media",	
"https://www.google.com/alerts/feeds/01881685235415088200/499494254267437494": "Gorilla Group",	
"https://www.google.com/alerts/feeds/01881685235415088200/14896185663731945744": "1185 Design",	
"https://www.google.com/alerts/feeds/01881685235415088200/5189971791098822960": "Sikka Software",	
"https://www.google.com/alerts/feeds/01881685235415088200/7096444430998810942": "SiftShopping",	
"https://www.google.com/alerts/feeds/01881685235415088200/1670163236829257058": "RoweBots",	
"https://www.google.com/alerts/feeds/01881685235415088200/3194799286830201245": "RevGuard",
"https://www.google.com/alerts/feeds/01881685235415088200/3088492595662771291": "ProcessMaker",	
"https://www.google.com/alerts/feeds/01881685235415088200/3426160054791121083": "Prizm Media",	
"https://www.google.com/alerts/feeds/01881685235415088200/8787370919617563315": "Optimal Design",	
"https://www.google.com/alerts/feeds/01881685235415088200/17094137868519063378": "mHealthCoach",	
"https://www.google.com/alerts/feeds/01881685235415088200/8926108154886683113": "Plex Media",	
"https://www.google.com/alerts/feeds/01881685235415088200/14115942879497787873": "Polaris Wireless",
"https://www.google.com/alerts/feeds/01881685235415088200/2130808873652481474": "PK4 Media",	
"https://www.google.com/alerts/feeds/01881685235415088200/2130808873652479174": "Palo Alto Software",	
"https://www.google.com/alerts/feeds/01881685235415088200/13241143637501297070": "Nominum",	
"https://www.google.com/alerts/feeds/01881685235415088200/17196160893349309111": "NextLabs",	
"https://www.google.com/alerts/feeds/01881685235415088200/17068671559893515315": "Net-results Marketing",	
"https://www.google.com/alerts/feeds/01881685235415088200/17068671559893514561": "Motive Interactive",	
"https://www.google.com/alerts/feeds/01881685235415088200/4494309180953001895": "mFino",	
"https://www.google.com/alerts/feeds/01881685235415088200/2826329624352299548":	"Magnet Forensics",
"https://www.google.com/alerts/feeds/01881685235415088200/14317108868047637052": "Odyssey Entertainment",	
"https://www.google.com/alerts/feeds/01881685235415088200/816948197205629415": "Jolly Technologies",	
"https://www.google.com/alerts/feeds/01881685235415088200/14807507605359057354": "iCIMS Software",	
"https://www.google.com/alerts/feeds/01881685235415088200/15359687578736256443": "iboss Network Security", 	
"https://www.google.com/alerts/feeds/01881685235415088200/5380929414551813195": "HeartMath",	
"https://www.google.com/alerts/feeds/01881685235415088200/9275099499107901459": "FiveCurrents",	
"https://www.google.com/alerts/feeds/01881685235415088200/12421709880562650402": "Dwell Media",	
"https://www.google.com/alerts/feeds/01881685235415088200/10080842736212328967": "Diyotta",
"https://www.google.com/alerts/feeds/01881685235415088200/10080842736212330090": "Column Technologies",	
"https://www.google.com/alerts/feeds/01881685235415088200/17514557101728196027": "Brainspace",	
"https://www.google.com/alerts/feeds/01881685235415088200/17514557101728194918": "Armanta",	
"https://www.google.com/alerts/feeds/01881685235415088200/5209014021783445932": "Arcweb Technologies",	
"https://www.google.com/alerts/feeds/01881685235415088200/2399572001056470906": "Automated Financial Systems", 	
"https://www.google.com/alerts/feeds/01881685235415088200/15603391281520140920": "Adaptive Insights",	
"https://www.google.com/alerts/feeds/01881685235415088200/2399572001056471532": "Actian",	
"https://www.google.com/alerts/feeds/01881685235415088200/18325552412421077470": "Acclivity",	
"https://www.google.com/alerts/feeds/01881685235415088200/1742446693126818803": "Zadara Storage", 	
"https://www.google.com/alerts/feeds/01881685235415088200/1742446693126818155": "Vinimaya",	
"https://www.google.com/alerts/feeds/01881685235415088200/55753066454787096": "UniPrint.net",	
"https://www.google.com/alerts/feeds/01881685235415088200/55753066454786151": "Traction On Demand",	
"https://www.google.com/alerts/feeds/01881685235415088200/688498965239335058": "TeleWorld Solutions",	
"https://www.google.com/alerts/feeds/01881685235415088200/14731217787726283637": "Neurio",	
"https://www.google.com/alerts/feeds/01881685235415088200/5727019650172960684": "Jitterbit",	
"https://www.google.com/alerts/feeds/01881685235415088200/688498965239335913": "InGenius",	
"https://www.google.com/alerts/feeds/01881685235415088200/2947890462845478231": "Cooper Technology",
"https://www.google.com/alerts/feeds/01881685235415088200/14676584507752268591": "AppScale", 	
"https://www.google.com/alerts/feeds/01881685235415088200/9895832409332369961": "Leeyo Software",	
"https://www.google.com/alerts/feeds/01881685235415088200/9895832409332370582": "Anova",	
"https://www.google.com/alerts/feeds/01881685235415088200/14125290742422295994": "Starview",	
"https://www.google.com/alerts/feeds/01881685235415088200/10383856931979509078": "Soft Facade",	
"https://www.google.com/alerts/feeds/01881685235415088200/13483307918268297313": "SEMrush",	
"https://www.google.com/alerts/feeds/01881685235415088200/6650792899457161051": "Securonix",	
"https://www.google.com/alerts/feeds/01881685235415088200/6650792899457160317": "QuoteWizard",
"https://www.google.com/alerts/feeds/01881685235415088200/15119189875483697850": "LookbookHQ",	
"https://www.google.com/alerts/feeds/01881685235415088200/4037389486826159765": "Liquidware Labs",
"https://www.google.com/alerts/feeds/01881685235415088200/1416208555085607366": "Ion Interactive",	
"https://www.google.com/alerts/feeds/01881685235415088200/566334841030510822": "InfoObjects",	
"https://www.google.com/alerts/feeds/01881685235415088200/8537403745645558629": "IMPRES Technology Solutions",	
"https://www.google.com/alerts/feeds/01881685235415088200/5380929414551813195": "Digital Air Strike",	
"https://www.google.com/alerts/feeds/01881685235415088200/9740695934544709550": "Deque Systems",	
"https://www.google.com/alerts/feeds/01881685235415088200/15368891700584012547": "DemandGen",	
"https://www.google.com/alerts/feeds/01881685235415088200/10803326371220709970": "DatafactZ",
"https://www.google.com/alerts/feeds/01881685235415088200/8155334016307805355": "Cloudwick",	
"https://www.google.com/alerts/feeds/01881685235415088200/8155334016307804117": "Brandify",	
"https://www.google.com/alerts/feeds/01881685235415088200/14986475557110171124": "Balsam Brands",	
"https://www.google.com/alerts/feeds/01881685235415088200/68235837086144483": "Ataccama",	
"https://www.google.com/alerts/feeds/01881685235415088200/13162754668150338994": "Arbitech",		
"https://www.google.com/alerts/feeds/01881685235415088200/13689024525564415671": "Allied Wallet",	
"https://www.google.com/alerts/feeds/01881685235415088200/10471595259234386576": "10ZiG Technology",	
"https://www.google.com/alerts/feeds/01881685235415088200/10949992027258364775": "Zinio",	
"https://www.google.com/alerts/feeds/01881685235415088200/7984199580008752792": "Veriship",	
"https://www.google.com/alerts/feeds/01881685235415088200/10949992027258366914": "Vormittag Associates",	
"https://www.google.com/alerts/feeds/01881685235415088200/16719674260391889643": "Shotspotter",	
"https://www.google.com/alerts/feeds/01881685235415088200/713129825002064231": "Ridebidz",
"https://www.google.com/alerts/feeds/01881685235415088200/713129825002064978": "Revstream",	
"https://www.google.com/alerts/feeds/01881685235415088200/5355354714045597794": "Neudesic",	
"https://www.google.com/alerts/feeds/01881685235415088200/16022778460001054677": "Mavenlink",
"https://www.google.com/alerts/feeds/01881685235415088200/9488590286302457472": "Loot Crate",	
"https://www.google.com/alerts/feeds/01881685235415088200/17845762241566517103": "Interface Masters Technologies",
"https://www.google.com/alerts/feeds/01881685235415088200/6401573801981596389": "Insurance Technologies",
"https://www.google.com/alerts/feeds/01881685235415088200/3403340439658937800": "Chiro Touch",
"https://www.google.com/alerts/feeds/01881685235415088200/8302565038833926521": "Cavirin",
"https://www.google.com/alerts/feeds/01881685235415088200/619459383223154454": "Altova",	
"https://www.google.com/alerts/feeds/13466654299695330520/14971857197063709873": "3xLOGIC", 
"https://www.google.com/alerts/feeds/13466654299695330520/14971857197063712363": "Access Softek", 
"https://www.google.com/alerts/feeds/13466654299695330520/7953061017660228717": "Accordant Media",
"https://www.google.com/alerts/feeds/13466654299695330520/12252887737135754697": "ActivityRez",
"https://www.google.com/alerts/feeds/13466654299695330520/10361205557633879324": "AgileThought",
"https://www.google.com/alerts/feeds/13466654299695330520/8938856719271881997": "Airbiquity", 
"https://www.google.com/alerts/feeds/13466654299695330520/8376314018692697355": "AirSage",
"https://www.google.com/alerts/feeds/13466654299695330520/17322655652350211912": "AppThis",
"https://www.google.com/alerts/feeds/13466654299695330520/9631845521440810943": "Avanade", 
"https://www.google.com/alerts/feeds/13466654299695330520/16343642913285857719": "Balihoo",
"https://www.google.com/alerts/feeds/13466654299695330520/6029716097834068590": "Bedrock Technology Partners",
"https://www.google.com/alerts/feeds/13466654299695330520/6029716097834067331": "Blue Chip Tek",
"https://www.google.com/alerts/feeds/13466654299695330520/11436489709049132119": "BrightSign",
"https://www.google.com/alerts/feeds/13466654299695330520/11962719138877261432": "Business IT Source", 
"https://www.google.com/alerts/feeds/13466654299695330520/6959141662227606985": "Candi Controls",
"https://www.google.com/alerts/feeds/13466654299695330520/8050474147697364694": "CcIntegration", 
"https://www.google.com/alerts/feeds/13466654299695330520/17666209018888937196": "Clarifire",
"https://www.google.com/alerts/feeds/13466654299695330520/2334941422965611524": "Cloud Cruiser",
"https://www.google.com/alerts/feeds/13466654299695330520/17885223414657201916": "CloudAccess",
"https://www.google.com/alerts/feeds/13466654299695330520/55631883025841140": "ContextMedia",
"https://www.google.com/alerts/feeds/13466654299695330520/1103487255186079704": "Corent Technology",
"https://www.google.com/alerts/feeds/13466654299695330520/6377559386693398851": "Dasher Technologies", 
"https://www.google.com/alerts/feeds/13466654299695330520/3626046738560358261": "Denali Advanced Integration",
"https://www.google.com/alerts/feeds/13466654299695330520/9584199260620510979": "DH2i",
"https://www.google.com/alerts/feeds/13466654299695330520/6364192568276430824": "docSTAR",
"https://www.google.com/alerts/feeds/13466654299695330520/6326172318573928689": "DOOR3",
"https://www.google.com/alerts/feeds/13466654299695330520/16901160432456327656": "E-STET",
"https://www.google.com/alerts/feeds/13466654299695330520/9973157840582836927": "ECS Imaging Inc.", 
"https://www.google.com/alerts/feeds/13466654299695330520/5492712225867939228": "eGroup", 
"https://www.google.com/alerts/feeds/13466654299695330520/8665283408024576059": "Enterprise Vision Technologies",
"https://www.google.com/alerts/feeds/13466654299695330520/11384353388350349739": "Entisys360",
"https://www.google.com/alerts/feeds/13466654299695330520/10394687173636901754" : "EoCell",
"https://www.google.com/alerts/feeds/13466654299695330520/10394687173636899461" : "Firespring",
"https://www.google.com/alerts/feeds/13466654299695330520/15134977399596337541": "Fractureme.com", 
"https://www.google.com/alerts/feeds/13466654299695330520/477734780287099036": "FusionStorm", 
"https://www.google.com/alerts/feeds/13466654299695330520/14115709920536056813": "G5 Marketing", 
"https://www.google.com/alerts/feeds/13466654299695330520/11445523526561349012": "GlobeTouch", 
"https://www.google.com/alerts/feeds/13466654299695330520/4741467760900212027": "Groupware", 
"https://www.google.com/alerts/feeds/13466654299695330520/1194814179906302423": "H5 Technologies",
"https://www.google.com/alerts/feeds/13466654299695330520/10729875605318364586": "Hawk Ridge Systems", 
"https://www.google.com/alerts/feeds/13466654299695330520/18304040471736823950": "High Point Networks", 
"https://www.google.com/alerts/feeds/13466654299695330520/14031522574556904519" : "Higi", 
"https://www.google.com/alerts/feeds/13466654299695330520/1194814179906305687": "Informz", 
"https://www.google.com/alerts/feeds/13466654299695330520/13523396319524936800" : "Insight Sourcing Group", 
"https://www.google.com/alerts/feeds/13466654299695330520/18299370789804107852": "Integrated Archive Systems", 
"https://www.google.com/alerts/feeds/13466654299695330520/8620268085983530070": "iPromote", 
"https://www.google.com/alerts/feeds/13466654299695330520/12743713329663882141": "Kovarus", 
"https://www.google.com/alerts/feeds/13466654299695330520/10077370292122660730": "LeaseTeam", 
"https://www.google.com/alerts/feeds/13466654299695330520/505859988944708551": "Lextech", 
"https://www.google.com/alerts/feeds/13466654299695330520/8517408735847409092": "Lilee Systems", 
"https://www.google.com/alerts/feeds/13466654299695330520/5217580278088234381": "McKay Brothers", 
"https://www.google.com/alerts/feeds/13466654299695330520/15141931027598928270": "Metalab", 
"https://www.google.com/alerts/feeds/13466654299695330520/5217580278088237007": "Miva Merchant", 
"https://www.google.com/alerts/feeds/13466654299695330520/9848036304332026561": "MobileFuse", 
"https://www.google.com/alerts/feeds/13466654299695330520/3123552041878734335": "Mobileum", 
"https://www.google.com/alerts/feeds/13466654299695330520/18304040471736824118": "Myriad Supply",
"https://www.google.com/alerts/feeds/13466654299695330520/2560347210036421949": "Net-Results Marketing", 
"https://www.google.com/alerts/feeds/13466654299695330520/11869511842566280584": "NetEnrich", 
"https://www.google.com/alerts/feeds/13466654299695330520/901878212394848750": "Netronome", 
"https://www.google.com/alerts/feeds/13466654299695330520/9555339260781000396": "Noble Iron", 
"https://www.google.com/alerts/feeds/13466654299695330520/9973157840582839109": "Nth Generation Computing", 
"https://www.google.com/alerts/feeds/13466654299695330520/10038241897902526473": "Numecent", 
"https://www.google.com/alerts/feeds/13466654299695330520/8363628837348710371": "Oddz",
"https://www.google.com/alerts/feeds/13466654299695330520/8536906125741608356": "Open Systems International", 
"https://www.google.com/alerts/feeds/13466654299695330520/16094236708637318511": "Orasi", 
"https://www.google.com/alerts/feeds/13466654299695330520/15911493296506074862": "Think Passenger", 
"https://www.google.com/alerts/feeds/13466654299695330520/8116805304637372476": "Plex Media", 
"https://www.google.com/alerts/feeds/13466654299695330520/5072251280735711728": "Pluribus Networks", 
"https://www.google.com/alerts/feeds/13466654299695330520/8340627479340479870": "Practice Velocity", 
"https://www.google.com/alerts/feeds/13466654299695330520/16640446566158017434": "Pragmatic Works software", 
"https://www.google.com/alerts/feeds/13466654299695330520/10646156976650753020": "Prosper", 
"https://www.google.com/alerts/feeds/13466654299695330520/15985501571533633495": "Quantcast", 
"https://www.google.com/alerts/feeds/13466654299695330520/10699213993855095437": "QuanticMind", 
"https://www.google.com/alerts/feeds/13466654299695330520/1799391203381342930": "RevenueWire", 
"https://www.google.com/alerts/feeds/13466654299695330520/10646026746986868838": "ReverbNation", 
"https://www.google.com/alerts/feeds/13466654299695330520/5469007186104147722": "ScientiaMobile", 
"https://www.google.com/alerts/feeds/13466654299695330520/5088166459691921823": "Seal Software", 
"https://www.google.com/alerts/feeds/13466654299695330520/5095684281127310549": "SemiosBIO", 
"https://www.google.com/alerts/feeds/13466654299695330520/3732659456275506510": "Sigma Systems", 
"https://www.google.com/alerts/feeds/13466654299695330520/4619868575558710897": "SparkFun", 
"https://www.google.com/alerts/feeds/13466654299695330520/17174354787861175071": "Spillman Technologies", 
"https://www.google.com/alerts/feeds/13466654299695330520/11104846275936375223": "Square Root", 
"https://www.google.com/alerts/feeds/13466654299695330520/18205294697538025718": "StartApp", 
"https://www.google.com/alerts/feeds/13466654299695330520/14389563127027661818": "Summit Biosciences", 
"https://www.google.com/alerts/feeds/13466654299695330520/17932114411299775799": "Sureline Systems", 
"https://www.google.com/alerts/feeds/13466654299695330520/7982623278894418692": "The Nerdery", 
"https://www.google.com/alerts/feeds/13466654299695330520/11002048848400764297": "ThreatConnect", 
"https://www.google.com/alerts/feeds/13466654299695330520/17651088638394232153": "TITUS", 
"https://www.google.com/alerts/feeds/13466654299695330520/6979358158246694090": "TouchSuite", 
"https://www.google.com/alerts/feeds/13466654299695330520/2889460546644572078": "Trace3", 
"https://www.google.com/alerts/feeds/13466654299695330520/2645318899423341838": "Velodyne", 
"https://www.google.com/alerts/feeds/13466654299695330520/15654298440115524397": "VIA Motors", 
"https://www.google.com/alerts/feeds/13466654299695330520/5173561638742355964": "Zomazz", 
"https://www.google.com/alerts/feeds/02062406705762041312/5451535100808539110": "Zinio",
"https://www.google.com/alerts/feeds/02062406705762041312/15671211174766790806": "Bizagi",
"https://www.google.com/alerts/feeds/020624067057620413121/5451535100808537977": "User Testing",
"https://www.google.com/alerts/feeds/02062406705762041312/13734466308953168108":    "Softfacade",
"https://www.google.com/alerts/feeds/02062406705762041312/13734466308953168829":    "Shotspotter",
"https://www.google.com/alerts/feeds/02062406705762041312/11092147724755190784":    "scandigital",
"https://www.google.com/alerts/feeds/02062406705762041312/2656591414836911737": "Red Pine Signals",
"https://www.google.com/alerts/feeds/02062406705762041312/11893550640734866364":    "Pley",
"https://www.google.com/alerts/feeds/02062406705762041312/4965430515445539778": "PaperG",
"https://www.google.com/alerts/feeds/02062406705762041312/11893550640734865632":    "Mobile Defense",
"https://www.google.com/alerts/feeds/02062406705762041312/18127349940471102005":    "JadooTV",
"https://www.google.com/alerts/feeds/02062406705762041312/1842992242340862655": "Fuzz Productions",
"https://www.google.com/alerts/feeds/02062406705762041312/5769740845327470898": "Edifecs",
"https://www.google.com/alerts/feeds/02062406705762041312/14443331568096937893":    "Zoom Caffe",
"https://www.google.com/alerts/feeds/02062406705762041312/14852976520710281506":    "Yardi",
"https://www.google.com/alerts/feeds/02062406705762041312/14443331568096940018":    "WRS Materials",
"https://www.google.com/alerts/feeds/02062406705762041312/8615484252419376638": "Well.ca",
"https://www.google.com/alerts/feeds/02062406705762041312/8615484252419377547": "Votigo",
"https://www.google.com/alerts/feeds/02062406705762041312/8615484252419378175": "vitria",
"https://www.google.com/alerts/feeds/02062406705762041312/8933258069582921537": "VisiQuate",
"https://www.google.com/alerts/feeds/02062406705762041312/5746718541562635731": "Virtuos Ltd.",
"https://www.google.com/alerts/feeds/02062406705762041312/5746718541562635919": "Virool",
"https://www.google.com/alerts/feeds/02062406705762041312/18334767804339456745":    "VigilNet Community Monitoring",
"https://www.google.com/alerts/feeds/02062406705762041312/4021406299706766443": "Unbounce",
"https://www.google.com/alerts/feeds/02062406705762041312/8233567744689238324": "Ubiquity Global Services",
"https://www.google.com/alerts/feeds/02062406705762041312/4021406299706767568": "Tutela Tech",
"https://www.google.com/alerts/feeds/02062406705762041312/12122000424484240313":    "Tulip Retail",
"https://www.google.com/alerts/feeds/02062406705762041312/12122000424484240178":    "Thoughtworks",
"https://www.google.com/alerts/feeds/02062406705762041312/12122000424484239265":    "Optime Group",
"https://www.google.com/alerts/feeds/02062406705762041312/5740363056375727398": "Tasktop",
"https://www.google.com/alerts/feeds/02062406705762041312/3722266231542023458": "Systems in Motion",
"https://www.google.com/alerts/feeds/02062406705762041312/3722266231542023054": "Survey Analytics",
"https://www.google.com/alerts/feeds/13466654299695330520/11369072851201187872": "SugarCRM Marketing",
"https://www.google.com/alerts/feeds/02062406705762041312/632202047199448876":  "stat Health Services",
"https://www.google.com/alerts/feeds/02062406705762041312/3088495681118562133": "Smule",
"https://www.google.com/alerts/feeds/02062406705762041312/14607657986943534996":    "SMS, inc.",
"https://www.google.com/alerts/feeds/02062406705762041312/7903596616217591861": "SkyTree",
"https://www.google.com/alerts/feeds/02062406705762041312/7903596616217592967": "Sitecore",
"https://www.google.com/alerts/feeds/02062406705762041312/12883977902754348340":    "Signiant",
"https://www.google.com/alerts/feeds/02062406705762041312/12883977902754345668":    "Sift Shopping",
"https://www.google.com/alerts/feeds/02062406705762041312/10010665971850991801":    "Schedulicity",
"https://www.google.com/alerts/feeds/02062406705762041312/10010665971850993571":    "Rolith",
"https://www.google.com/alerts/feeds/02062406705762041312/692729505549121703":  "Referral Saasquatch",
"https://www.google.com/alerts/feeds/02062406705762041312/17193276624174069073":    "Recorded Future",
"https://www.google.com/alerts/feeds/02062406705762041312/8436229574644343393": "Recommind",
"https://www.google.com/alerts/feeds/02062406705762041312/1759710790041120949": "Realty Mogul",
"https://www.google.com/alerts/feeds/02062406705762041312/6991931469844997335": "Radiant Logic",
"https://www.google.com/alerts/feeds/02062406705762041312/6991931469844996642": "QuickMobile",
"https://www.google.com/alerts/feeds/02062406705762041312/11257665490522839832":    "Quantisense",
"https://www.google.com/alerts/feeds/02062406705762041312/11219233900047042895":    "Pulson",
"https://www.google.com/alerts/feeds/02062406705762041312/10429503542873433988":    "Promevo",
"https://www.google.com/alerts/feeds/02062406705762041312/10429503542873433334":    "Proformative",
"https://www.google.com/alerts/feeds/02062406705762041312/5240033680261613147": "prevoty",
"https://www.google.com/alerts/feeds/02062406705762041312/5771414264762800165": "Pretio Interactive",
"https://www.google.com/alerts/feeds/02062406705762041312/14135372739064166543":    "Plum Voice",
"https://www.google.com/alerts/feeds/02062406705762041312/164667081325941276":  "Percona",
"https://www.google.com/alerts/feeds/02062406705762041312/9070022432653348621": "PDHI",
"https://www.google.com/alerts/feeds/02062406705762041312/9070022432653348074": "Oversight Systems",
"https://www.google.com/alerts/feeds/02062406705762041312/17655246754798696192":    "Ontraport",
"https://www.google.com/alerts/feeds/02062406705762041312/6973255723239729332": "Neusoft",
"https://www.google.com/alerts/feeds/02062406705762041312/107409442514440098":  "Netwrix",
"https://www.google.com/alerts/feeds/02062406705762041312/11610665288912776873":    "neato",
"https://www.google.com/alerts/feeds/02062406705762041312/3508825709076618444": "navagate",
"https://www.google.com/alerts/feeds/02062406705762041312/3508825709076616710": "mycorporation.com",
"https://www.google.com/alerts/feeds/02062406705762041312/3508825709076616997": "Mulesoft",
"https://www.google.com/alerts/feeds/02062406705762041312/12931894682642024650":    "Mobile Action",
"https://www.google.com/alerts/feeds/02062406705762041312/6981264731603356147": "Malwarebytes",
"https://www.google.com/alerts/feeds/02062406705762041312/15191979296832764568":    "Main Street Hub",
"https://www.google.com/alerts/feeds/02062406705762041312/10156193641003657413":    "Lumo Bodytech",
"https://www.google.com/alerts/feeds/02062406705762041312/15613636266159631161":    "Odyssey Entertainment",
"https://www.google.com/alerts/feeds/02062406705762041312/17404663272574942251":    "LiveEnsure",
"https://www.google.com/alerts/feeds/02062406705762041312/1390794130710317575": "Lithium Technologies",
"https://www.google.com/alerts/feeds/02062406705762041312/17396427411805734271":    "Kubicam",
"https://www.google.com/alerts/feeds/02062406705762041312/6575616247985574918": "Knowledge Marketing",
"https://www.google.com/alerts/feeds/02062406705762041312/17396427411805735603":    "KeyedIn Solutions",
"https://www.google.com/alerts/feeds/02062406705762041312/200946860401571985":  "jamcracker",
"https://www.google.com/alerts/feeds/02062406705762041312/200946860401570976":  "interneer",
"https://www.google.com/alerts/feeds/02062406705762041312/3826162343940337764": "integrated biometrics",
"https://www.google.com/alerts/feeds/02062406705762041312/6223083195894846682": "ins zoom",
"https://www.google.com/alerts/feeds/13466654299695330520/12324172474754799099":    "inriver",
"https://www.google.com/alerts/feeds/02062406705762041312/16776894766737983124":    "information builders",
"https://www.google.com/alerts/feeds/13466654299695330520/14560956454094256184":    "icims software",
"https://www.google.com/alerts/feeds/02062406705762041312/2962025794278729148": "gyrus",
"https://www.google.com/alerts/feeds/02062406705762041312/11127422907426618749":    "gemini solutions",
"https://www.google.com/alerts/feeds/02062406705762041312/7395578459586164283": "fullarmor",
"https://www.google.com/alerts/feeds/02062406705762041312/13247670572481404415":    "freshbooks",
"https://www.google.com/alerts/feeds/02062406705762041312/109613453342847149":  "four winds interactive",
"https://www.google.com/alerts/feeds/02062406705762041312/1914311863843569760": "flowgear",
"https://www.google.com/alerts/feeds/02062406705762041312/16279816956832154522":    "etwater",
"https://www.google.com/alerts/feeds/02062406705762041312/16279816956832155729":    "ericom",
"https://www.google.com/alerts/feeds/02062406705762041312/14601896837141013602": "Contenix",
"https://www.google.com/alerts/feeds/02062406705762041312/1126258742458971627": "Moment Design",
"https://www.google.com/alerts/feeds/02062406705762041312/5657753612956061956": "SunCentral",
"https://www.google.com/alerts/feeds/02062406705762041312/9204548976826551664": "XG sciences",
"https://www.google.com/alerts/feeds/02062406705762041312/2072179285307919018": "Kiip",
"https://www.google.com/alerts/feeds/02062406705762041312/7019550178776333209": "Sojern",
"https://www.google.com/alerts/feeds/02062406705762041312/7019550178776333510": "Xirrus",
"https://www.google.com/alerts/feeds/02062406705762041312/12011210292130282520": "Allocadia",
"https://www.google.com/alerts/feeds/02062406705762041312/12011210292130281856": "Binwise",
"https://www.google.com/alerts/feeds/02062406705762041312/11660103569085035494": "Meridian Clean Coal",
"https://www.google.com/alerts/feeds/02062406705762041312/6392144421683957432": "Mocana",
"https://www.google.com/alerts/feeds/02062406705762041312/12011210292130282520": "Proxio",
"https://www.google.com/alerts/feeds/02062406705762041312/14443331568096937640": "Starview",
"https://www.google.com/alerts/feeds/02062406705762041312/8615484252419376870": "Stratogent",
"https://www.google.com/alerts/feeds/02062406705762041312/15632915224957884581": "TurnCommerce",
"https://www.google.com/alerts/feeds/02062406705762041312/5746718541562638237": "Vionx",
"https://www.google.com/alerts/feeds/02062406705762041312/15632915224957882477": "Virtual Bridges",
"https://www.google.com/alerts/feeds/02062406705762041312/18334767804339457246": "ViZn Energy",
"https://www.google.com/alerts/feeds/02062406705762041312/6661669010023826466": "Zoom Technologies",
"https://www.google.com/alerts/feeds/02062406705762041312/8233567744689240336": "ActMobile",
"https://www.google.com/alerts/feeds/02062406705762041312/4021406299706765511": "Armanta",
"https://www.google.com/alerts/feeds/02062406705762041312/6751348586596979261": "Leeyo",
"https://www.google.com/alerts/feeds/02062406705762041312/5238135823142398697": "Search Technologies",
"https://www.google.com/alerts/feeds/02062406705762041312/5740363056375729869": "Secure64",
"https://www.google.com/alerts/feeds/02062406705762041312/16371578590400077312": "Soraa",
"https://www.google.com/alerts/feeds/02062406705762041312/1782326813927722798": "Scribblelive",
"https://www.google.com/alerts/feeds/02062406705762041312/5228429197450360129": "360pi",
"https://www.google.com/alerts/feeds/02062406705762041312/3088495681118562550": "ActivEngage",
"https://www.google.com/alerts/feeds/02062406705762041312/2176721985226159447": "Act-On Software",
"https://www.google.com/alerts/feeds/02062406705762041312/2176721985226160603": "Adaptive Planning",
"https://www.google.com/alerts/feeds/02062406705762041312/7903596616217593985": "AppLovin",
"https://www.google.com/alerts/feeds/02062406705762041312/7833637987667539397": "Ayla Networks",
"https://www.google.com/alerts/feeds/02062406705762041312/7903596616217594296": "BigML",
"https://www.google.com/alerts/feeds/02062406705762041312/12766643275826260061": "BuildDirect",
"https://www.google.com/alerts/feeds/02062406705762041312/3811454850071931956": "Comodo",
"https://www.google.com/alerts/feeds/02062406705762041312/4350246155083242847": "Coupa Software",
"https://www.google.com/alerts/feeds/02062406705762041312/9454263677642889586": "EngagePoint",
"https://www.google.com/alerts/feeds/02062406705762041312/17193276624174070004": "Enterprise Engineering",
"https://www.google.com/alerts/feeds/02062406705762041312/8436229574644345338": "eShipGlobal",
"https://www.google.com/alerts/feeds/02062406705762041312/12930299050015098788": "iboss",
"https://www.google.com/alerts/feeds/02062406705762041312/9845147377187965561": "Kontiki",
"https://www.google.com/alerts/feeds/02062406705762041312/14596073740068426969": "Meltwater",
"https://www.google.com/alerts/feeds/02062406705762041312/12317356517016336115": "Mobify",
"https://www.google.com/alerts/feeds/02062406705762041312/3368120317282496202": "Outsystems",
"https://www.google.com/alerts/feeds/02062406705762041312/14534779934515597310": "Quantifind",
"https://www.google.com/alerts/feeds/02062406705762041312/11697718741169257071": "Quixey",
"https://www.google.com/alerts/feeds/02062406705762041312/9798962351390451465": "RGB Spectrum",
"https://www.google.com/alerts/feeds/02062406705762041312/14189370591100224223": "Rimini Street",
"https://www.google.com/alerts/feeds/02062406705762041312/11678059886279920551": "Rise Interactive",
"https://www.google.com/alerts/feeds/02062406705762041312/14189370591100224118": "Real-Time Innovations",
"https://www.google.com/alerts/feeds/02062406705762041312/15634272773826690271": "ShareThrough",
"https://www.google.com/alerts/feeds/02062406705762041312/1952998804414674328": "ShippingEasy",
"https://www.google.com/alerts/feeds/02062406705762041312/4248703195252150694": "TraceSecurity",
"https://www.google.com/alerts/feeds/02062406705762041312/14199054692078207438": "VoiceBox Technologies",
"https://www.google.com/alerts/feeds/02062406705762041312/9088983416957814343": "3esi",
"https://www.google.com/alerts/feeds/02062406705762041312/866446058370717187": "Acclivity",
"https://www.google.com/alerts/feeds/02062406705762041312/18391294624796254": "Acquia",
"https://www.google.com/alerts/feeds/02062406705762041312/16461820305707803567": "Adexa",
"https://www.google.com/alerts/feeds/02062406705762041312/8043453079708019667": "Amperics",
"https://www.google.com/alerts/feeds/02062406705762041312/528568041899009378": "Anthem Media Group",
"https://www.google.com/alerts/feeds/02062406705762041312/18208327643445941080": "Appointment-Plus",
"https://www.google.com/alerts/feeds/02062406705762041312/18208327643445943061": "Artec Group",
"https://www.google.com/alerts/feeds/02062406705762041312/8197277581016720571": "Asigra",
"https://www.google.com/alerts/feeds/02062406705762041312/8810453785864400720": "Atlantis Computing",
"https://www.google.com/alerts/feeds/02062406705762041312/3815617076212362936": "Automation Anywhere",
"https://www.google.com/alerts/feeds/02062406705762041312/12219022977072856547": "Blue Jeans Network",
"https://www.google.com/alerts/feeds/02062406705762041312/1081338962497421778": "Blue Wave Media",
"https://www.google.com/alerts/feeds/02062406705762041312/16585002916782872318": "BlueCat Networks",
"https://www.google.com/alerts/feeds/02062406705762041312/11303193489297562381": "Brainspace",
"https://www.google.com/alerts/feeds/02062406705762041312/13328510058997422486": "Chaordix",
"https://www.google.com/alerts/feeds/02062406705762041312/7638990815327381860": "Comilion",
"https://www.google.com/alerts/feeds/02062406705762041312/12487352408347965472": "Continuum Analytics",
"https://www.google.com/alerts/feeds/02062406705762041312/15618437625746337895": "CTC America",
"https://www.google.com/alerts/feeds/02062406705762041312/16479446172795132828": "Digital Defense",
"https://www.google.com/alerts/feeds/02062406705762041312/9802622504040440941": "Digital Dream Labs",
"https://www.google.com/alerts/feeds/02062406705762041312/2308958562630037518": "Dwell Media",
"https://www.google.com/alerts/feeds/02062406705762041312/9615978415870236504": "Echo Sec",
"https://www.google.com/alerts/feeds/02062406705762041312/2578744933996684994": "Elastic Path",
"https://www.google.com/alerts/feeds/02062406705762041312/9342015003890982679": "Encepta",
"https://www.google.com/alerts/feeds/02062406705762041312/8169993311602351141": "Engine Yard",
"https://www.google.com/alerts/feeds/02062406705762041312/2641415568862031826": "Enprecis",
"https://www.google.com/alerts/feeds/02062406705762041312/6503229101590592373": "Electric Cloud",
"https://www.google.com/alerts/feeds/13466654299695330520/4038571174568239769":"Innovolt",
"https://www.google.com/alerts/feeds/13466654299695330520/8116805304637372476":"Plex Media",
"https://www.google.com/alerts/feeds/13466654299695330520/1103487255186077813":"Deque Systems",
"https://www.google.com/alerts/feeds/13466654299695330520/14526097733999371029":"Digital Air Strike Marketing",
"https://www.google.com/alerts/feeds/13466654299695330520/5194078567190119068":"eXplorance",
"https://www.google.com/alerts/feeds/13466654299695330520/4850408063435830141":"Grandstream Networks",
"https://www.google.com/alerts/feeds/13466654299695330520/13357752628413143058":"Haivision",
"https://www.google.com/alerts/feeds/13466654299695330520/7095923152758469433":"Halfpenny Technologies",
"https://www.google.com/alerts/feeds/13466654299695330520/16045694062059617395":"Impact Financial Systems",
"https://www.google.com/alerts/feeds/13466654299695330520/13956169297468481071":"Ingenious Med",
"https://www.google.com/alerts/feeds/13466654299695330520/14319666356235721505":"Innovest Systems",
"https://www.google.com/alerts/feeds/13466654299695330520/5384932753816902500":"Intelex",
"https://www.google.com/alerts/feeds/13466654299695330520/18364391379436489053":"iotum",
"https://www.google.com/alerts/feeds/13466654299695330520/3925966518163966447":"PC Connection PCCC",
"https://www.google.com/alerts/feeds/13466654299695330520/5810579531890136314":"World Wide Technology",
"https://www.google.com/alerts/feeds/13466654299695330520/15955123983804453751":"gravitytank",
"https://www.google.com/alerts/feeds/13466654299695330520/749013797226874438":"Cooper Technology",
"https://www.google.com/alerts/feeds/13466654299695330520/7864614278597615906":"Igloo Software",
"https://www.google.com/alerts/feeds/13466654299695330520/1190946517984484525":"Think Passenger",
"https://www.google.com/alerts/feeds/13466654299695330520/5937813447947498127":"Sift Shopping",
"https://www.google.com/alerts/feeds/13466654299695330520/2602515567548598041":"Vitria Technology Inc",

}

def removeHTMLTags(data):
	  p = re.compile(r'<.*?>')
	  return p.sub('', data)

def cleanTitle(title):
	  title = removeHTMLTags(str(title))
	  title = title.replace('&lt;b&gt;', '')
	  title = title.replace('&lt;/b&gt;', '')
	  title = title.replace('&amp;#39;', '\'')
	  return title

def cleanLink(link):
	  link = str(link)
	  start = link.find('url=')
	  link = link[start + 4:]
	  end = link.find('&amp')
	  link = link[:end]
	  return link

def cleanDate(date):
	  date = removeHTMLTags(str(date))
	  end = date.find('T')
	  date = date[:end]
	  return date

def writeToSheet(sheet, title, company, link, date, cur_row):
	  sheet.write(cur_row, 3, unicode(title, "utf-8"))
	  sheet.write(cur_row, 1, unicode(company, "utf-8"))
	  sheet.write(cur_row, 4, unicode(link, "utf-8"))
	  sheet.write(cur_row, 0, unicode(date, "utf-8"))

def processSheet(sheet):
	  sheet.col(3).width = 256 * 60
	  sheet.col(1).width = 256 * 15
	  sheet.col(4).width = 256 * 100
	  sheet.col(0).width = 256 * 10

def savewb(wb):
	  wbname = 'Google_Alerts_%s' % (datetime.now().strftime("%m-%d-%y")) + '.xls'
	  wbname = os.getcwd() + '/alerts_spreadsheets/' + wbname

	  print 'Processing completed...'
	  print 'Saving to ' + wbname + '...'
	  wb.save(wbname)

def createSpreadsheet():
	  wb = xlwt.Workbook()
	  sheet = wb.add_sheet("Google Alerts")
	  style = xlwt.easyxf('font: bold 1')
	  sheet.write(0, 3, 'Headline', style)
	  sheet.write(0, 1, 'Company', style)
	  sheet.write(0, 4, 'URL', style)
	  sheet.write(0, 0, 'Date', style)

	  cur_row = 1

	  for url in LA_HONDA_ALERTS_URLS:
			print 'Processing google alerts for ' + LA_HONDA_ALERTS_URLS[url] + '...'
			r = requests.get(url)
			xml = r.text
			soup = BeautifulSoup(xml)

			for title, link, date in zip(soup.findAll('title')[1:], soup.findAll('link')[1:], soup.findAll('published')):
				  title = cleanTitle(title)
				  link = cleanLink(link)
				  date = cleanDate(date)

				  writeToSheet(sheet, title, LA_HONDA_ALERTS_URLS[url], link, date, cur_row)
				  cur_row = cur_row + 1

	  processSheet(sheet)
	  savewb(wb)

USERNAME = 'sorcererdailyupdate@gmail.com'
PASSWORD = 'CrothersStoreySidDrew2015'
DAVID_EMAIL = ['david@lahondaadvisors.com']

def main():
	  createSpreadsheet()
	  wbname = os.getcwd() + '/alerts_spreadsheets/' + 'Google_Alerts_%s' % (datetime.now().strftime("%m-%d-%y")) + '.xls'
	  date = datetime.now()
	  subject = 'Google Alerts Update for ' + date.strftime('%m-%d-%Y')
	  email_body = 'Hi David,\n\nAttached are Google Alerts updates for ' + date.strftime('%m-%d-%Y') + '\n\nBest,\nSid'

	  email_digest = EmailDigestAPI(USERNAME, PASSWORD)
	  email_digest.send_mail(DAVID_EMAIL, subject, email_body, files = [wbname])


if __name__ == "__main__":
	  main()
