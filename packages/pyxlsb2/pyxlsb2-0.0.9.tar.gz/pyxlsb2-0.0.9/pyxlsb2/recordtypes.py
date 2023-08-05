# All record types
# Taken from [MS-XLSB]
# https://docs.microsoft.com/en-us/openspecs/office_file_formats/ms-xlsb/30e2eaae-0b1e-4e8e-a465-e1ce5575868d
ROW_HDR = 0
CELL_BLANK = 1
CELL_RK = 2
CELL_ERROR = 3
CELL_BOOL = 4
CELL_REAL = 5
CELL_ST = 6
CELL_ISST = 7
FMLA_STRING = 8
FMLA_NUM = 9
FMLA_BOOL = 10
FMLA_ERROR = 11
SST_ITEM = 19
PCDI_MISSING = 20
PCDI_NUMBER = 21
PCDI_BOOLEAN = 22
PCDI_ERROR = 23
PCDI_STRING = 24
PCDI_DATETIME = 25
PCDI_INDEX = 26
PCDIA_MISSING = 27
PCDIA_NUMBER = 28
PCDIA_BOOLEAN = 29
PCDIA_ERROR = 30
PCDIA_STRING = 31
PCDIA_DATETIME = 32
PCR_RECORD = 33
PCR_RECORD_DT = 34
FRT_BEGIN = 35
FRT_END = 36
AC_BEGIN = 37
AC_END = 38
NAME = 39
INDEX_ROW_BLOCK = 40
INDEX_BLOCK = 42
FONT = 43
FMT = 44
FILL = 45
BORDER = 46
XF = 47
STYLE = 48
CELL_META = 49
VALUE_META = 50
MDB = 51
BEGIN_FMD = 52
END_FMD = 53
BEGIN_MDX = 54
END_MDX = 55
BEGIN_MDX_TUPLE = 56
END_MDX_TUPLE = 57
MDX_MBR_ISTR = 58
STR = 59
COL_INFO = 60
CELL_R_STRING = 62
D_VAL = 64
SXVCELL_NUM = 65
SXVCELL_STR = 66
SXVCELL_BOOL = 67
SXVCELL_ERR = 68
SXVCELL_DATE = 69
SXVCELL_NIL = 70
FILE_VERSION = 128
BEGIN_SHEET = 129
END_SHEET = 130
BEGIN_BOOK = 131
END_BOOK = 132
BEGIN_WS_VIEWS = 133
END_WS_VIEWS = 134
BEGIN_BOOK_VIEWS = 135
END_BOOK_VIEWS = 136
BEGIN_WS_VIEW = 137
END_WS_VIEW = 138
BEGIN_CS_VIEWS = 139
END_CS_VIEWS = 140
BEGIN_CS_VIEW = 141
END_CS_VIEW = 142
BEGIN_BUNDLE_SHS = 143
END_BUNDLE_SHS = 144
BEGIN_SHEET_DATA = 145
END_SHEET_DATA = 146
WS_PROP = 147
WS_DIM = 148
PANE = 151
SEL = 152
WB_PROP = 153
WB_FACTOID = 154
FILE_RECOVER = 155
BUNDLE_SH = 156
CALC_PROP = 157
BOOK_VIEW = 158
BEGIN_SST = 159
END_SST = 160
BEGIN_A_FILTER = 161
END_A_FILTER = 162
BEGIN_FILTER_COLUMN = 163
END_FILTER_COLUMN = 164
BEGIN_FILTERS = 165
END_FILTERS = 166
FILTER = 167
COLOR_FILTER = 168
ICON_FILTER = 169
TOP10_FILTER = 170
DYNAMIC_FILTER = 171
BEGIN_CUSTOM_FILTERS = 172
END_CUSTOM_FILTERS = 173
CUSTOM_FILTER = 174
A_FILTER_DATE_GROUP_ITEM = 175
MERGE_CELL = 176
BEGIN_MERGE_CELLS = 177
END_MERGE_CELLS = 178
BEGIN_PIVOT_CACHE_DEF = 179
END_PIVOT_CACHE_DEF = 180
BEGIN_PCD_FIELDS = 181
END_PCD_FIELDS = 182
BEGIN_PCD_FIELD = 183
END_PCD_FIELD = 184
BEGIN_PCD_SOURCE = 185
END_PCD_SOURCE = 186
BEGIN_PCDS_RANGE = 187
END_PCDS_RANGE = 188
BEGIN_PCDF_ATBL = 189
END_PCDF_ATBL = 190
BEGIN_PCDI_RUN = 191
END_PCDI_RUN = 192
END_PIVOT_CACHE_RECORDS = 194
BEGIN_PCD_HIERARCHIES = 195
END_PCD_HIERARCHIES = 196
BEGIN_PCD_HIERARCHY = 197
END_PCD_HIERARCHY = 198
BEGIN_PCDH_FIELDS_USAGE = 199
END_PCDH_FIELDS_USAGE = 200
BEGIN_EXT_CONNECTION = 201
END_EXT_CONNECTION = 202
BEGIN_EC_DB_PROPS = 203
END_EC_DB_PROPS = 204
BEGIN_EC_OLAP_PROPS = 205
END_EC_OLAP_PROPS = 206
BEGIN_PCDS_CONSOL = 207
END_PCDS_CONSOL = 208
BEGIN_PCDSC_PAGES = 209
END_PCDSC_PAGES = 210
BEGIN_PCDSC_PAGE = 211
END_PCDSC_PAGE = 212
BEGIN_PCDSCP_ITEM = 213
END_PCDSCP_ITEM = 214
BEGIN_PCDSC_SETS = 215
END_PCDSC_SETS = 216
BEGIN_PCDSC_SET = 217
END_PCDSC_SET = 218
BEGIN_PCDF_GROUP = 219
END_PCDF_GROUP = 220
BEGIN_PCDFG_ITEMS = 221
END_PCDFG_ITEMS = 222
BEGIN_PCDFG_RANGE = 223
END_PCDFG_RANGE = 224
BEGIN_PCDFG_DISCRETE = 225
END_PCDFG_DISCRETE = 226
END_PCDSD_TUPLE_CACHE = 228
BEGIN_PCDSDTC_ENTRIES = 229
END_PCDSDTC_ENTRIES = 230
END_PCDSDTCE_MEMBER = 234
BEGIN_PCDSDTC_QUERIES = 235
END_PCDSDTC_QUERIES = 236
BEGIN_PCDSDTC_QUERY = 237
END_PCDSDTC_QUERY = 238
BEGIN_PCDSDTC_SETS = 239
END_PCDSDTC_SETS = 240
BEGIN_PCDSDTC_SET = 241
END_PCDSDTC_SET = 242
BEGIN_PCD_CALC_ITEMS = 243
END_PCD_CALC_ITEMS = 244
BEGIN_PCD_CALC_ITEM = 245
END_PCD_CALC_ITEM = 246
BEGIN_P_RULE = 247
END_P_RULE = 248
BEGIN_PR_FILTERS = 249
END_PR_FILTERS = 250
BEGIN_PR_FILTER = 251
END_PR_FILTER = 252
BEGIN_P_NAMES = 253
END_P_NAMES = 254
BEGIN_P_NAME = 255
END_P_NAME = 256
BEGIN_PN_PAIRS = 257
END_PN_PAIRS = 258
BEGIN_PN_PAIR = 259
END_PN_PAIR = 260
BEGIN_EC_WEB_PROPS = 261
END_EC_WEB_PROPS = 262
BEGIN_EC_WP_TABLES = 263
END_ECWP_TABLES = 264
BEGIN_EC_PARAMS = 265
END_EC_PARAMS = 266
BEGIN_EC_PARAM = 267
END_EC_PARAM = 268
BEGIN_PCDKPIS = 269
END_PCDKPIS = 270
BEGIN_PCDKPI = 271
END_PCDKPI = 272
BEGIN_DIMS = 273
END_DIMS = 274
BEGIN_DIM = 275
END_DIM = 276
INDEX_PART_END = 277
BEGIN_STYLE_SHEET = 278
END_STYLE_SHEET = 279
BEGIN_SX_VIEW = 280
END_SXVI = 281
BEGIN_SXVI = 282
BEGIN_SXVIS = 283
END_SXVIS = 284
BEGIN_SXVD = 285
END_SXVD = 286
BEGIN_SXVDS = 287
END_SXVDS = 288
BEGIN_SXPI = 289
END_SXPI = 290
BEGIN_SXPIS = 291
END_SXPIS = 292
BEGIN_SXDI = 293
END_SXDI = 294
BEGIN_SXDIS = 295
END_SXDIS = 296
BEGIN_SXLI = 297
END_SXLI = 298
BEGIN_SXLI_RWS = 299
END_SXLI_RWS = 300
BEGIN_SXLI_COLS = 301
END_SXLI_COLS = 302
BEGIN_SX_FORMAT = 303
END_SX_FORMAT = 304
BEGIN_SX_FORMATS = 305
END_SX_FORMATS = 306
BEGIN_SX_SELECT = 307
END_SX_SELECT = 308
BEGIN_ISXVD_RWS = 309
END_ISXVD_RWS = 310
BEGIN_ISXVD_COLS = 311
END_ISXVD_COLS = 312
END_SX_LOCATION = 313
BEGIN_SX_LOCATION = 314
END_SX_VIEW = 315
BEGIN_SXTHS = 316
END_SXTHS = 317
BEGIN_SXTH = 318
END_SXTH = 319
BEGIN_ISXTH_RWS = 320
END_ISXTH_RWS = 321
BEGIN_ISXTH_COLS = 322
END_ISXTH_COLS = 323
BEGIN_SXTDMPS = 324
END_SXTDMPS = 325
BEGIN_SXTDMP = 326
END_SXTDMP = 327
BEGIN_SXTH_ITEMS = 328
END_SXTH_ITEMS = 329
BEGIN_SXTH_ITEM = 330
END_SXTH_ITEM = 331
BEGIN_METADATA = 332
END_METADATA = 333
BEGIN_ESMDTINFO = 334
MDTINFO = 335
END_ESMDTINFO = 336
BEGIN_ESMDB = 337
END_ESMDB = 338
BEGIN_ESFMD = 339
END_ESFMD = 340
BEGIN_SINGLE_CELLS = 341
END_SINGLE_CELLS = 342
BEGIN_LIST = 343
END_LIST = 344
BEGIN_LIST_COLS = 345
END_LIST_COLS = 346
BEGIN_LIST_COL = 347
END_LIST_COL = 348
BEGIN_LIST_XML_C_PR = 349
END_LIST_XML_C_PR = 350
LIST_CC_FMLA = 351
LIST_TR_FMLA = 352
BEGIN_EXTERNALS = 353
END_EXTERNALS = 354
SUP_BOOK_SRC = 355
SUP_SELF = 357
SUP_SAME = 358
SUP_TABS = 359
BEGIN_SUP_BOOK = 360
PLACEHOLDER_NAME = 361
EXTERN_SHEET = 362
EXTERN_TABLE_START = 363
EXTERN_TABLE_END = 364
EXTERN_ROW_HDR = 366
EXTERN_CELL_BLANK = 367
EXTERN_CELL_REAL = 368
EXTERN_CELL_BOOL = 369
EXTERN_CELL_ERROR = 370
EXTERN_CELL_STRING = 371
BEGIN_ESMDX = 372
END_ESMDX = 373
BEGIN_MDX_SET = 374
END_MDX_SET = 375
BEGIN_MDX_MBR_PROP = 376
END_MDX_MBR_PROP = 377
BEGIN_MDX_KPI = 378
END_MDX_KPI = 379
BEGIN_ESSTR = 380
END_ESSTR = 381
BEGIN_PRF_ITEM = 382
END_PRF_ITEM = 383
BEGIN_PIVOT_CACHE_IDS = 384
END_PIVOT_CACHE_IDS = 385
BEGIN_PIVOT_CACHE_ID = 386
END_PIVOT_CACHE_ID = 387
BEGIN_ISXVIS = 388
END_ISXVIS = 389
BEGIN_COL_INFOS = 390
END_COL_INFOS = 391
BEGIN_RW_BRK = 392
END_RW_BRK = 393
BEGIN_COL_BRK = 394
END_COL_BRK = 395
BRK = 396
USER_BOOK_VIEW = 397
INFO = 398
C_USR = 399
USR = 400
BEGIN_USERS = 401
EOF = 403
UCR = 404
RR_INS_DEL = 405
RR_END_INS_DEL = 406
RR_MOVE = 407
RR_END_MOVE = 408
RR_CHG_CELL = 409
RR_END_CHG_CELL = 410
RR_HEADER = 411
RR_USER_VIEW = 412
RR_REN_SHEET = 413
RR_INSERT_SH = 414
RR_DEF_NAME = 415
RR_NOTE = 416
RR_CONFLICT = 417
RRTQSIF = 418
RR_FORMAT = 419
RR_END_FORMAT = 420
RR_AUTO_FMT = 421
BEGIN_USER_SH_VIEWS = 422
BEGIN_USER_SH_VIEW = 423
END_USER_SH_VIEW = 424
END_USER_SH_VIEWS = 425
ARR_FMLA = 426
SHR_FMLA = 427
TABLE = 428
BEGIN_EXT_CONNECTIONS = 429
END_EXT_CONNECTIONS = 430
BEGIN_PCD_CALC_MEMS = 431
END_PCD_CALC_MEMS = 432
BEGIN_PCD_CALC_MEM = 433
END_PCD_CALC_MEM = 434
BEGIN_PCDHG_LEVELS = 435
END_PCDHG_LEVELS = 436
BEGIN_PCDHG_LEVEL = 437
END_PCDHG_LEVEL = 438
BEGIN_PCDHGL_GROUPS = 439
END_PCDHGL_GROUPS = 440
BEGIN_PCDHGL_GROUP = 441
END_PCDHGL_GROUP = 442
END_PCDHGLG_MEMBERS = 444
BEGIN_PCDHGLG_MEMBER = 445
END_PCDHGLG_MEMBER = 446
BEGIN_QSI = 447
END_QSI = 448
BEGIN_QSIR = 449
END_QSIR = 450
BEGIN_DELETED_NAMES = 451
END_DELETED_NAMES = 452
BEGIN_DELETED_NAME = 453
END_DELETED_NAME = 454
BEGIN_QSIFS = 455
END_QSIFS = 456
BEGIN_QSIF = 457
END_QSIF = 458
BEGIN_AUTO_SORT_SCOPE = 459
END_AUTO_SORT_SCOPE = 460
BEGIN_CF_RULE = 463
END_CF_RULE = 464
BEGIN_ICON_SET = 465
END_ICON_SET = 466
BEGIN_DATABAR = 467
END_DATABAR = 468
BEGIN_COLOR_SCALE = 469
END_COLOR_SCALE = 470
CFVO = 471
EXTERN_VALUE_META = 472
BEGIN_COLOR_PALETTE = 473
END_COLOR_PALETTE = 474
INDEXED_COLOR = 475
MARGINS = 476
PRINT_OPTIONS = 477
PAGE_SETUP = 478
BEGIN_HEADER_FOOTER = 479
END_HEADER_FOOTER = 480
BEGIN_SX_CRT_FORMAT = 481
END_SX_CRT_FORMAT = 482
BEGIN_SX_CRT_FORMATS = 483
END_SX_CRT_FORMATS = 484
WS_FMT_INFO = 485
BEGIN_MGS = 486
END_MGS = 487
BEGIN_MG_MAPS = 488
END_MG_MAPS = 489
BEGIN_MG = 490
END_MG = 491
BEGIN_MAP = 492
END_MAP = 493
H_LINK = 494
BEGIN_D_CON = 495
END_D_CON = 496
BEGIN_D_REFS = 497
END_D_REFS = 498
D_REF = 499
BEGIN_SCEN_MAN = 500
END_SCEN_MAN = 501
BEGIN_SCT = 502
END_SCT = 503
SLC = 504
BEGIN_DXFS = 505
END_DXFS = 506
DXF = 507
BEGIN_TABLE_STYLES = 508
END_TABLE_STYLES = 509
BEGIN_TABLE_STYLE = 510
END_TABLE_STYLE = 511
TABLE_STYLE_ELEMENT = 512
TABLE_STYLE_CLIENT = 513
BEGIN_VOL_DEPS = 514
END_VOL_DEPS = 515
BEGIN_VOL_TYPE = 516
END_VOL_TYPE = 517
BEGIN_VOL_MAIN = 518
END_VOL_MAIN = 519
BEGIN_VOL_TOPIC = 520
END_VOL_TOPIC = 521
VOL_SUBTOPIC = 522
VOL_REF = 523
VOL_NUM = 524
VOL_ERR = 525
VOL_STR = 526
VOL_BOOL = 527
BEGIN_SORT_STATE = 530
END_SORT_STATE = 531
BEGIN_SORT_COND = 532
END_SORT_COND = 533
BOOK_PROTECTION = 534
SHEET_PROTECTION = 535
RANGE_PROTECTION = 536
PHONETIC_INFO = 537
BEGIN_EC_TXT_WIZ = 538
END_EC_TXT_WIZ = 539
BEGIN_ECTW_FLD_INFO_LST = 540
END_ECTW_FLD_INFO_LST = 541
BEGIN_EC_TW_FLD_INFO = 542
FILE_SHARING = 548
OLE_SIZE = 549
DRAWING = 550
LEGACY_DRAWING = 551
LEGACY_DRAWING_HF = 552
WEB_OPT = 553
BEGIN_WEB_PUB_ITEMS = 554
END_WEB_PUB_ITEMS = 555
BEGIN_WEB_PUB_ITEM = 556
END_WEB_PUB_ITEM = 557
BEGIN_SX_COND_FMT = 558
END_SX_COND_FMT = 559
BEGIN_SX_COND_FMTS = 560
END_SX_COND_FMTS = 561
BK_HIM = 562
COLOR = 564
BEGIN_INDEXED_COLORS = 565
END_INDEXED_COLORS = 566
BEGIN_MRU_COLORS = 569
END_MRU_COLORS = 570
MRU_COLOR = 572
BEGIN_D_VALS = 573
END_D_VALS = 574
SUP_NAME_START = 577
SUP_NAME_VALUE_START = 578
SUP_NAME_VALUE_END = 579
SUP_NAME_NUM = 580
SUP_NAME_ERR = 581
SUP_NAME_ST = 582
SUP_NAME_NIL = 583
SUP_NAME_BOOL = 584
SUP_NAME_FMLA = 585
SUP_NAME_BITS = 586
SUP_NAME_END = 587
END_SUP_BOOK = 588
CELL_SMART_TAG_PROPERTY = 589
BEGIN_CELL_SMART_TAG = 590
END_CELL_SMART_TAG = 591
BEGIN_CELL_SMART_TAGS = 592
END_CELL_SMART_TAGS = 593
BEGIN_SMART_TAGS = 594
END_SMART_TAGS = 595
SMART_TAG_TYPE = 596
BEGIN_SMART_TAG_TYPES = 597
END_SMART_TAG_TYPES = 598
BEGIN_SX_FILTERS = 599
END_SX_FILTERS = 600
BEGIN_SXFILTER = 601
END_SX_FILTER = 602
BEGIN_FILLS = 603
END_FILLS = 604
BEGIN_CELL_WATCHES = 605
END_CELL_WATCHES = 606
CELL_WATCH = 607
BEGIN_CR_ERRS = 608
END_CR_ERRS = 609
CRASH_REC_ERR = 610
BEGIN_FONTS = 611
END_FONTS = 612
BEGIN_BORDERS = 613
END_BORDERS = 614
BEGIN_FMTS = 615
END_FMTS = 616
BEGIN_CELL_XFS = 617
END_CELL_XFS = 618
BEGIN_STYLES = 619
END_STYLES = 620
BIG_NAME = 625
BEGIN_CELL_STYLE_XFS = 626
END_CELL_STYLE_XFS = 627
BEGIN_COMMENTS = 628
END_COMMENTS = 629
BEGIN_COMMENT_AUTHORS = 630
END_COMMENT_AUTHORS = 631
COMMENT_AUTHOR = 632
BEGIN_COMMENT_LIST = 633
END_COMMENT_LIST = 634
BEGIN_COMMENT = 635
END_COMMENT = 636
COMMENT_TEXT = 637
BEGIN_OLE_OBJECTS = 638
OLE_OBJECT = 639
END_OLE_OBJECTS = 640
BEGIN_SXRULES = 641
END_SX_RULES = 642
BEGIN_ACTIVE_X_CONTROLS = 643
ACTIVE_X = 644
END_ACTIVE_X_CONTROLS = 645
BEGIN_PCDSDTCE_MEMBERS_SORT_BY = 646
BEGIN_CELL_IGNORE_ECS = 648
CELL_IGNORE_EC = 649
END_CELL_IGNORE_ECS = 650
CS_PROP = 651
CS_PAGE_SETUP = 652
BEGIN_USER_CS_VIEWS = 653
END_USER_CS_VIEWS = 654
BEGIN_USER_CS_VIEW = 655
END_USER_CS_VIEW = 656
BEGIN_PCD_SFCI_ENTRIES = 657
END_PCDSFCI_ENTRIES = 658
PCDSFCI_ENTRY = 659
BEGIN_LIST_PARTS = 660
LIST_PART = 661
END_LIST_PARTS = 662
SHEET_CALC_PROP = 663
BEGIN_FN_GROUP = 664
FN_GROUP = 665
END_FN_GROUP = 666
SUP_ADDIN = 667
SXTDMP_ORDER = 668
CS_PROTECTION = 669
BEGIN_WS_SORT_MAP = 671
END_WS_SORT_MAP = 672
BEGIN_RR_SORT = 673
END_RR_SORT = 674
RR_SORT_ITEM = 675
FILE_SHARING_ISO = 676
BOOK_PROTECTION_ISO = 677
SHEET_PROTECTION_ISO = 678
CS_PROTECTION_ISO = 679
RANGE_PROTECTION_ISO = 680
RW_DESCENT = 1024
KNOWN_FONTS = 1025
BEGIN_SX_TUPLE_SET = 1026
END_SX_TUPLE_SET = 1027
END_SX_TUPLE_SET_HEADER = 1029
BEGIN_SX_TUPLE_SET_DATA = 1031
END_SX_TUPLE_SET_DATA = 1032
BEGIN_SX_TUPLE_SET_ROW = 1033
END_SX_TUPLE_SET_ROW = 1034
SX_TUPLE_SET_ROW_ITEM = 1035
NAME_EXT = 1036
PCDH14 = 1037
BEGIN_PCD_CALC_MEM14 = 1038
END_PCD_CALC_MEM14 = 1039
SXTH14 = 1040
BEGIN_SPARKLINE_GROUP = 1041
END_SPARKLINE_GROUP = 1042
SPARKLINE = 1043
SXDI14 = 1044
WS_FMT_INFO_EX14 = 1045
BEGIN_CF_RULE14 = 1048
END_CF_RULE14 = 1049
CFVO14 = 1050
BEGIN_DATABAR14 = 1051
BEGIN_ICON_SET14 = 1052
D_VAL14 = 1053
BEGIN_D_VALS14 = 1054
COLOR14 = 1055
BEGIN_SPARKLINES = 1056
END_SPARKLINES = 1057
BEGIN_SPARKLINE_GROUPS = 1058
END_SPARKLINE_GROUPS = 1059
SXVD14 = 1061
BEGIN_SX_VIEW14 = 1062
END_SX_VIEW14 = 1063
BEGIN_SX_VIEW16 = 1064
END_SX_VIEW16 = 1065
BEGIN_PCD14 = 1066
END_PCD14 = 1067
BEGIN_EXT_CONN14 = 1068
END_EXT_CONN14 = 1069
BEGIN_SLICER_CACHE_IDS = 1070
END_SLICER_CACHE_IDS = 1071
BEGIN_SLICER_CACHE_ID = 1072
END_SLICER_CACHE_ID = 1073
BEGIN_SLICER_CACHE = 1075
END_SLICER_CACHE = 1076
BEGIN_SLICER_CACHE_DEF = 1077
END_SLICER_CACHE_DEF = 1078
BEGIN_SLICERS_EX = 1079
END_SLICERS_EX = 1080
BEGIN_SLICER_EX = 1081
END_SLICER_EX = 1082
BEGIN_SLICER = 1083
END_SLICER = 1084
SLICER_CACHE_PIVOT_TABLES = 1085
SLICER_CACHE_OLAP_ITEM = 1096
SLICER_CACHE_SELECTION = 1098
END_SLICER_CACHE_NATIVE = 1101
SLICER_CACHE_NATIVE_ITEM = 1102
RANGE_PROTECTION14 = 1103
RANGE_PROTECTION_ISO14 = 1104
CELL_IGNORE_EC14 = 1105
LIST14 = 1111
CF_ICON = 1112
BEGIN_SLICER_CACHES_PIVOT_CACHE_IDS = 1113
BEGIN_SLICERS = 1115
END_SLICERS = 1116
WB_PROP14 = 1117
BEGIN_SX_EDIT = 1118
END_SX_EDIT = 1119
BEGIN_SX_EDITS = 1120
END_SX_EDITS = 1121
BEGIN_SX_CHANGE = 1122
END_SX_CHANGE = 1123
BEGIN_SX_CHANGES = 1124
END_SX_CHANGES = 1125
SX_TUPLE_ITEMS = 1126
BEGIN_SLICER_STYLE = 1128
END_SLICER_STYLE = 1129
SLICER_STYLE_ELEMENT = 1130
BEGIN_STYLE_SHEET_EXT14 = 1131
END_STYLE_SHEET_EXT14 = 1132
BEGIN_SLICER_CACHES_PIVOT_CACHE_ID = 1133
BEGIN_PCD_CALC_MEM_EXT = 1137
END_PCD_CALC_MEM_EXT = 1138
BEGIN_PCD_CALC_MEMS_EXT = 1139
END_PCD_CALC_MEMS_EXT = 1140
PCD_FIELD14 = 1141
BEGIN_SLICER_STYLES = 1142
END_SLICER_STYLES = 1143
CF_RULE_EXT = 1146
BEGIN_SX_COND_FMT14 = 1147
END_SX_COND_FMT14 = 1148
BEGIN_SX_COND_FMTS14 = 1149
END_SX_COND_FMTS14 = 1150
BEGIN_SORT_COND14 = 1152
END_SORT_COND14 = 1153
END_D_VALS14 = 1154
END_ICON_SET14 = 1155
END_DATABAR14 = 1156
BEGIN_COLOR_SCALE14 = 1157
END_COLOR_SCALE14 = 1158
BEGIN_SXRULES14 = 1159
END_SXRULES14 = 1160
BEGIN_P_RULE14 = 1161
END_P_RULE14 = 1162
BEGIN_PR_FILTERS14 = 1163
END_PR_FILTERS14 = 1164
BEGIN_PR_FILTER14 = 1165
END_PR_FILTER14 = 1166
BEGIN_PRF_ITEM14 = 1167
END_PRF_ITEM14 = 1168
BEGIN_CELL_IGNORE_ECS14 = 1169
END_CELL_IGNORE_ECS14 = 1170
DXF14 = 1171
BEGIN_DX_F14S = 1172
END_DXF14S = 1173
FILTER14 = 1177
BEGIN_CUSTOM_FILTERS14 = 1178
CUSTOM_FILTER14 = 1180
ICON_FILTER14 = 1181
BEGIN_PIVOT_TABLE_REFS = 2051
END_PIVOT_TABLE_REFS = 2052
PIVOT_TABLE_REF = 2053
BEGIN_SXVCELLS = 2055
END_SXVCELLS = 2056
BEGIN_SX_ROW = 2057
END_SX_ROW = 2058
PCD_CALC_MEM15 = 2060
QSI15 = 2067
BEGIN_WEB_EXTENSIONS = 2068
END_WEB_EXTENSIONS = 2069
WEB_EXTENSION = 2070
ABS_PATH15 = 2071
TABLE_SLICER_CACHE_IDS = 2075
TABLE_SLICER_CACHE_ID = 2076
BEGIN_TABLE_SLICER_CACHE = 2077
END_TABLE_SLICER_CACHE = 2078
SX_FILTER15 = 2079
BEGIN_TIMELINE_CACHE_PIVOT_CACHE_IDS = 2080
END_TIMELINE_CACHE_PIVOT_CACHE_IDS = 2081
END_TIMELINE_CACHE_IDS = 2084
BEGIN_TIMELINE_CACHE_ID = 2085
END_TIMELINE_CACHE_ID = 2086
BEGIN_TIMELINES_EX = 2087
END_TIMELINES_EX = 2088
BEGIN_TIMELINE_EX = 2089
END_TIMELINE_EX = 2090
WORK_BOOK_PR15 = 2091
PCDH15 = 2092
BEGIN_TIMELINE_STYLE = 2093
END_TIMELINE_STYLE = 2094
TIMELINE_STYLE_ELEMENT = 2095
BEGIN_TIMELINE_STYLESHEET_EXT15 = 2096
END_TIMELINE_STYLESHEET_EXT15 = 2097
BEGIN_TIMELINE_STYLES = 2098
END_TIMELINE_STYLES = 2099
DXF15 = 2102
BEGIN_DXFS15 = 2103
END_DXFS15 = 2104
SLICER_CACHE_HIDE_ITEMS_WITH_NO_DATA = 2105
BEGIN_ITEM_UNIQUE_NAMES = 2106
END_ITEM_UNIQUE_NAMES = 2107
ITEM_UNIQUE_NAME = 2108
BEGIN_EXT_CONN15 = 2109
END_EXT_CONN15 = 2110
BEGIN_OLEDB_PR15 = 2111
END_OLEDB_PR15 = 2112
BEGIN_DATA_FEED_PR15 = 2113
END_DATA_FEED_PR15 = 2114
TEXT_PR15 = 2115
RANGE_PR15 = 2116
DB_COMMAND15 = 2117
BEGIN_DB_TABLES15 = 2118
END_DB_TABLES15 = 2119
DB_TABLE15 = 2120
BEGIN_DATA_MODEL = 2121
END_DATA_MODEL = 2122
BEGIN_MODEL_TABLES = 2123
END_MODEL_TABLES = 2124
MODEL_TABLE = 2125
END_MODEL_RELATIONSHIPS = 2127
MODEL_RELATIONSHIP = 2128
BEGIN_EC_TXT_WIZ15 = 2129
END_EC_TXT_WIZ15 = 2130
BEGIN_ECTW_FLD_INFO_LST15 = 2131
END_ECTW_FLD_INFO_LST15 = 2132
BEGIN_ECTW_FLD_INFO15 = 2133
FIELD_LIST_ACTIVE_ITEM = 2134
PIVOT_CACHE_ID_VERSION = 2135
SXDI15 = 2136
REVISION_PTR = 3073

_by_name = {k: v for k, v in locals().items() if not k.startswith('_')}
_by_num = {v: k for k, v in _by_name.items()}
# https://docs.microsoft.com/en-us/openspecs/office_file_formats/ms-xlsb/8cc503eb-12ab-4a47-bbc7-2dbcef47150b
_SUP_LINK_TYPES = {SUP_SELF, SUP_SAME, SUP_ADDIN, SUP_BOOK_SRC}
