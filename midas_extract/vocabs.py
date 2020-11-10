"""
A set of common vocabularies used in MIDAS queries.

"""

UK_COUNTIES = """ABERDEENSHIRE,ALDERNEY,ANGUS,ANTRIM,ARGYLL (IN HIGHLAND REGION),
ARGYLL (IN STRATHCLYDE REGION),ARGYLLSHIRE,ARMAGH,ASCENSION IS,
AUSTRALIA (ADDITIONAL ISLANDS),AVON,AYRSHIRE,BANFFSHIRE,BEDFORDSHIRE,
BERKSHIRE,BERWICKSHIRE,BORDERS,BOUVET ISLAND,BRECKNOCKSHIRE,BRITISH VIRGIN ISLANDS,
BUCKINGHAMSHIRE,BUTESHIRE,CAERNARFONSHIRE,CAITHNESS,CAMBRIDGESHIRE,CARDIGANSHIRE,
CARLOW,CARMARTHENSHIRE,CAVAN,CAYMAN ISLANDS,CENTRAL,CHANNEL ISLANDS,CHESHIRE,
CHRISTMAS ISLAND,CLACKMANNANSHIRE,CLARE,CLEVELAND,CLWYD,COCOS ISLAND,COOK ISLANDS,
CORK,CORNWALL,CUMBERLAND,CUMBRIA,CYPRUS,DENBIGHSHIRE,DERBYSHIRE,DETACHED ISLANDS,
DEVON,DONEGAL,DORSET,DOWN,DUBLIN,DUMFRIES & GALLOWAY,DUMFRIESSHIRE,DUNBARTONSHIRE,
DURHAM,DYFED,EAST LOTHIAN,EAST SUSSEX,ESSEX,FALKLAND IS,FERMANAGH,FIFE,FLINTSHIRE,
FORFARSHIRE,GALWAY,GLAMORGANSHIRE,GLOUCESTERSHIRE,GRAMPIAN,GREATER LONDON,
GREATER MANCHESTER,GUADALOUPE,GUERNSEY,GWENT,GWYNEDD,HAMPSHIRE,HAWAII,HEREFORD,
HEREFORD & WORCESTER,HERTFORDSHIRE,HIGHLAND,HUMBERSIDE,HUNTINGDONSHIRE,INVERNESS-SHIRE,
ISLE OF ANGLESEY,ISLE OF MAN,ISLE OF WIGHT,ISLES OF SCILLY,JERSEY,KENT,KERRY,KILDARE,
KILKENNY,KINCARDINESHIRE,KINROSS-SHIRE,KIRKCUDBRIGHTSHIRE,LANARKSHIRE,LANARKSHIRE,
LANCASHIRE,LAOIS,LEICESTERSHIRE,LEITRIM,LIMERICK,LINCOLNSHIRE,LONDONDERRY,LONGFORD,
LOTHIAN,LOUTH,MALDIVES,MALTA,MAYO,MEATH,MEDITERRANEAN ISLANDS,MERIONETHSHIRE,
MERSEYSIDE,MIDDLESEX,MID GLAMORGAN,MIDLOTHIAN,MIDLOTHIAN (IN BORDERS REGION),
MIDLOTHIAN (IN LOTHIAN REGION),MONAGHAN,MONMOUTHSHIRE,MONTGOMERYSHIRE,MORAY,
MORAY (IN GRAMPIAN REGION),MORAY (IN HIGHLAND REGION),NAIRNSHIRE,NORFOLK,
NORTHAMPTONSHIRE,NORTHUMBERLAND,NORTH YORKSHIRE,NOTTINGHAMSHIRE,OCEAN ISLANDS,
OFFALY,ORKNEY,OXFORDSHIRE,PACIFIC ISLANDS NORTH OF EQUATOR,PEEBLESHIRE,PEMBROKESHIRE,
PERTHSHIRE,PERTHSHIRE (IN CENTRAL REGION),PERTHSHIRE (IN TAYSIDE REGION),
PHOENIX ISLANDS,POWYS,POWYS (NORTH),POWYS (SOUTH),RADNORSHIRE,RENFREWSHIRE,ROSCOMMON,
ROSS & CROMARTY,ROXBURGHSHIRE,RUTLAND,SANTA CRUZ ISLANDS,SARK,SELKIRKSHIRE,SEYCHELLES,
SHETLAND,SHROPSHIRE,SINGAPORE,SLIGO,SOLOMON ISLANDS,SOMERSET,SOUTHERN LINE ISLANDS,
SOUTH GEORGIA,SOUTH GLAMORGAN,SOUTH ORKNEYS,SOUTH SHETLAND,SOUTH YORKSHIRE,
SPAIN (CANARY ISLANDS),STAFFORDSHIRE,ST HELENA,STIRLING,STIRLING (IN CENTRAL REGION),
STIRLING (IN STRATHCLYDE REGION),STRATHCLYDE,SUFFOLK,SURREY,SUSSEX,SUTHERLAND,TAYSIDE,
TIPPERARY,TURKS & CAICOS ISLANDS,TYNE & WEAR,TYRONE,WARWICKSHIRE,WATERFORD,WESTERN ISLES,
WEST GLAMORGAN,WEST LOTHIAN,WEST LOTHIAN (IN CENTRAL REGION),
WEST LOTHIAN (IN LOTHIAN REGION),WESTMEATH,WEST MIDLANDS,WESTMORLAND,WEST SUFFOLK,
WEST SUSSEX,WEST YORKSHIRE,WEXFORD,WICKLOW,WIGTOWNSHIRE,WILTSHIRE,WORCESTERSHIRE,
YORKSHIRE""".lower().replace('\n', '').split(',')

DATA_TYPES = ['CLBD', 'CLBN', 'CLBR', 'CLBW', 'DCNN', 'FIXD', 'ICAO', 'LPMS', 'RAIN', 
'SHIP', 'WIND', 'WMO']

TABLE_NAMES = ['TD', 'WD', 'RD', 'RH', 'RS', 'ST', 'WH', 'WM', 'RO']