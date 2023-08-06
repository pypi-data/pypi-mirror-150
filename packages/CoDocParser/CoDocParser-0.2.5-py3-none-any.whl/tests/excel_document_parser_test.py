import json
import os

import pytest

from docparser.doc_parser_factory import DocParserFactory

# from tests.excel_config import ExcelConfig as Config
doc1_config = {}
test_config = {
    "id": "CMA",
    "name": "CMA config",
    "kv": {
        "VESSEL": {
            "position_pattern": [
                "^VESSEL:"
            ],
            "value_pattern": [
                "(?P<Vessel>[\\w\\W]*?)(?:\\r\\n|\\n|$)"
            ],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "VesselName",
                    "key": "Vessel"
                }
            ]
        },
        "VOYAGE": {
            "position_pattern": [
                "^VOYAGE:"
            ],
            "value_pattern": [
                "VOYAGE\\s*:\\s*(?P<VOYAGE>[\\w\\W]*)"
            ],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "VoyageNo",
                    "key": "VOYAGE"
                }
            ]
        },
        "POD ETA": {
            "position_pattern": [
                "^POD ETA"
            ],
            "value_pattern": [
                "POD\\s*ETA\\s*:\\s*(?P<ETA>\\d+/\\d+/\\d+)(?:\\r\\n|\\n)"
            ],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "EstimatedArrivalDate",
                    "key": "ETA"
                }
            ]
        },
        "DeliveryPlaceName": {
            "position_pattern": [
                "^OPERATIONAL LOAD PORT"
            ],
            "value_pattern": [
                "[\\w\\W]*?(?:\\n|\\r\\n)(?P<DELIVERY>.*)"
            ],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "DeliveryPlaceName",
                    "key": "DELIVERY"
                }
            ]
        },
        "BillOfLadingsId": {
            "position_pattern": [
                "^Please clear your cargo",
                "Please Pay freight against "
            ],
            "value_pattern": [
                "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4}\\s*[a-zA-Z]{3,}\\d{5,}[a-zA-Z]*)\\s*((Waybill)|(Negotiable))",
                "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4,}\\d{5,}[a-zA-Z]*)\\s*"

            ],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "BillOfLadingsId",
                    "key": "billoflading"
                }
            ]
        },
        "BillOfLadingsId1": {
            "position_pattern": [
                "^Please[\\w\\W]*BILL\\s*TYPE$",
                "^SCAC\\s{2,}B/L\\s*#$"
            ],
            "value_pattern": [
                "(?P<billoflading>[a-zA-Z]{4,}\\s*[a-zA-Z]*\\d{5,}[a-zA-Z]*)$",
            ],
            "repeat_count": 1,
            "find_mode": "v",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "BillOfLadingsId",
                    "key": "billoflading"
                }
            ]
        }
    },
    "table": {
        "containers": {
            "position_pattern": [
                "^CONTAINER\\s*#"
            ],
            "separator": " ",
            "find_mode": "v",
            "separator_mode": "regex",
            "column": [
                "ContainerNo"
            ],
            "behaviors": [
                {
                    "over_action": "row",
                    "value_pattern": [
                        "(?P<col_1>([a-zA-Z]{4,}\\d{7,}\\s*)*)"
                    ],
                    "action": []
                }
            ]
        }
    },
    "data_type_format": {
        "VoyageNo": {
            "data_type": "str",
            "filter": "r([/\\s])"
        },
        "EstimatedArrivalDate": {
            "data_type": "time",
            "format": "%m/%d/%Y",
            "filter": ""
        },
        "BillOfLadingsId": {
            "data_type": "str",
            "filter": "(\\s)"
        }
    },
    "address_repair": {
        "db": {
            "pub": {
                "user": "co",
                "pwd": "Co&23@2332$22",
                "server": "db.test.com:1433",
                "database": "CO_PUB"
            }
        },
        "repairs": [
            {
                "key": "DeliveryPlaceName",
                "db_key": "pub",
                "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
                "column": [
                    0,
                    1,
                    2,
                    3
                ],
                "value": 4,
                "mapping": "DeliveryPlaceId",
                "old_val_handle": "empty"
            }
        ]
    }
}
zim_config = {
    "id": "AN_ZIM_",
    "parse": {
        "id": "ZIM",
        "name": "ZIM config",
        "kv": {
            "Vessel/Voyage": {
                "position_pattern": [
                    "^Vessel/Voyage:",
                    "^Shipper:[\\W\\w]*?Vessel/Voyage"
                ],
                "value_pattern": [
                    "[\\w\\W]*TEL:\\d+-\\d+-\\d+[\\w\\W]*(?:\\n|\\r\\n)(?P<Vessel>([a-zA-Z]*\\s*)*[\\w\\W]*?)$",
                    "\\s*(?P<Vessel>.*?)(?:\\n|\\r\\n)(?P<ETA>\\d{1,}/\\d{1,}/\\d{2,})[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4,}\\d{7,})",
                    "\\s*(?P<Vessel>.*?)(?:\\n|\\r\\n)(?P<ETA>\\d{1,}/\\d{1,}/\\d{2,})",
                    "[\\w\\W]*?(?P<Vessel>([a-zA-Z]*\\s*)*[\\w\\W]*?(?:\\r\\n|\\n|$))"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VesselName",
                        "key": "Vessel",
                        "pattern_list": [
                            "(?P<value>[\\w\\W]*)\\s+?(.{7,})$"
                        ]
                    },
                    {
                        "keyword": "VoyageNo",
                        "key": "Vessel",
                        "pattern_list": [
                            "([\\w\\W]*)\\s+?(?P<value>.{7,})$"
                        ]
                    },
                    {
                        "keyword": "EstimatedArrivalDate",
                        "key": "ETA"
                    },
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            },
            "Bill of Lading": {
                "position_pattern": [
                    "^Exchange Method",
                    "Bill of Lading"
                ],
                "value_pattern": [
                    ".*\\s*([\\w\\s]*[\\r\\n])(?P<billoflading>[a-zA-Z]{4,}\\d{4,})(?:\\s|$)",
                    "(?P<billoflading>[a-zA-Z]{4,}\\d{4,})"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            },
            "Destination": {
                "position_pattern": [
                    "^Port of Loading"
                ],
                "value_pattern": [
                    "[\\w\\W]*?Port of Destination\\s*:\\s*(?P<PortofDestination>[^\\n]*?)(?:\\r\\n|\\n|$)Manifest\\s*Destination\\s*:\\s*(?P<ManifestDestination>[^\\r]*?)(?:\\r|\\n)",
                    "[\\w\\W]*?Port of Destination\\s*:\\s*(?P<PortofDestination>[^\\n]*?)(?:\\r\\n|\\n|$)Manifest\\s*Destination\\s*:\\s*(?P<ManifestDestination>[^\\r]*?)(?:\\r|\\n|$)"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DestinationPortName",
                        "key": "PortofDestination"
                    },
                    {
                        "keyword": "DeliveryPlaceName",
                        "key": "ManifestDestination"
                    }
                ]
            },
            "ETA": {
                "position_pattern": [
                    "^ETA:"
                ],
                "value_pattern": [
                    "(?P<ETA>\\d{1,}/\\d{1,}/\\d{2,})"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "EstimatedArrivalDate",
                        "key": "ETA",
                        "action_type": "append"
                    }
                ]
            }
        },
        "table": {
            "containers": {
                "position_pattern": [
                    "^Port of Loading",
                    "^Container"
                ],
                "separator": "     ",
                "find_mode": "h",
                "separator_mode": "regex",
                "column": [
                    "ContainerNo",
                    "ContainerSize"
                ],
                "behaviors": [
                    {
                        "over_action": "row",
                        "value_pattern": [
                            "\\s*(?P<col_1>[a-zA-Z]{4,}\\d{7,})[\\w\\W]*?\\s{4,}(?P<col_2>[a-zA-Z]{2,}\\d{2,})(?:\\s{4,}|\\r|\\n)[\\w\\W]*?$"
                        ],
                        "action": []
                    }
                ]
            }
        },
        "data_type_format": {
            "VoyageNo": {
                "data_type": "str",
                "filter": "([/\\s])"
            },
            "EstimatedArrivalDate": {
                "data_type": "time",
                "format": "%m/%d/%Y",
                "filter": ""
            }
        },
        "address_repair": {
            "db": {
                "pub": {
                    "user": "co",
                    "pwd": "Co&23@2332$22",
                    "server": "db.dev.com:1433",
                    "database": "CO_PUB"
                }
            },
            "repairs": [
                {
                    "key": "DestinationPortName",
                    "db_key": "pub",
                    "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
                    "column": [
                        0,
                        1,
                        2,
                        3
                    ],
                    "value": 4,
                    "mapping": "DestinationPortId",
                    "old_val_handle": "empty"
                },
                {
                    "key": "DeliveryPlaceName",
                    "db_key": "pub",
                    "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
                    "column": [
                        0,
                        1,
                        2,
                        3
                    ],
                    "value": 4,
                    "mapping": "DeliveryPlaceId",
                    "old_val_handle": "empty"
                }
            ]
        }
    }
}
cma_config = {
    "id": "AN_CMA_",
    "parse": {
        "id": "CMA",
        "name": "CMA config",
        "kv": {
            "VESSEL": {
                "position_pattern": [
                    "^VESSEL:"
                ],
                "value_pattern": [
                    "(?P<Vessel>[\\w\\W]*?)(?:\\r\\n|\\n|$)"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VesselName",
                        "key": "Vessel"
                    }
                ]
            },
            "VOYAGE": {
                "position_pattern": [
                    "^VOYAGE:"
                ],
                "value_pattern": [
                    "VOYAGE\\s*:\\s*(?P<VOYAGE>[^\\n\\r]*)(?:\\r|\\n)",
                    "VOYAGE\\s*:\\s*(?P<VOYAGE>[\\w\\W]*)"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VoyageNo",
                        "key": "VOYAGE"
                    }
                ]
            },
            "POD ETA": {
                "position_pattern": [
                    "^POD ETA"
                ],
                "value_pattern": [
                    "POD\\s*ETA\\s*:\\s*(?P<ETA>\\d+/\\d+/\\d+)(?:\\r\\n|\\n)"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "EstimatedArrivalDate",
                        "key": "ETA"
                    }
                ]
            },
            "DeliveryPlaceName": {
                "position_pattern": [
                    "^OPERATIONAL LOAD PORT"
                ],
                "value_pattern": [
                    "[\\w\\W]*(?:\\n|\\r\\n|)(?P<DELIVERY>.*)"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DeliveryPlaceName",
                        "key": "DELIVERY"
                    }
                ]
            },
            "DestinationPortName": {
                "position_pattern": [
                    "[\\w\\W]*?OPERATIONAL DISCH. PORT[\\w\\W]*"
                ],
                "value_pattern": [
                    "[^\\n]*?(?:\\n)(?P<DestinationPortName>[^\\n]*?)(?:\\n|$)",
                    "[^\\n]*(?P<DestinationPortName>.*)$"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DestinationPortName",
                        "key": "DestinationPortName"
                    }
                ]
            },
            "BillOfLadingsId": {
                "position_pattern": [
                    "^Please clear your cargo",
                    "Please Pay freight against "
                ],
                "value_pattern": [
                    "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4}\\s*[a-zA-Z]{3,}\\d{5,}[a-zA-Z]*)\\s*((Waybill)|(Negotiable))",
                    "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4,}\\d{5,}[a-zA-Z]*)\\s*"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            },
            "BillOfLadingsId1": {
                "position_pattern": [
                    "^Please[\\w\\W]*BILL\\s*TYPE$",
                    "^SCAC\\s{2,}B/L\\s*#$"
                ],
                "value_pattern": [
                    "(?P<billoflading>[a-zA-Z]{4,}\\s*[a-zA-Z]*\\d{5,}[a-zA-Z]*)$"
                ],
                "repeat_count": 1,
                "find_mode": "v",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            }
        },
        "table": {
            "containers": {
                "position_pattern": [
                    "^CONTAINER\\s*#"
                ],
                "separator": " ",
                "find_mode": "v",
                "separator_mode": "regex",
                "column": [
                    "ContainerNo"
                ],
                "behaviors": [
                    {
                        "over_action": "row",
                        "value_pattern": [
                            "(?P<col_1>([a-zA-Z]{4,}\\d{7,}\\s*)*)"
                        ],
                        "action": []
                    }
                ]
            }
        },
        "data_type_format": {
            "VoyageNo": {
                "data_type": "str",
                "filter": "r([/\\s])"
            },
            "EstimatedArrivalDate": {
                "data_type": "time",
                "format": "%m/%d/%Y",
                "filter": ""
            },
            "BillOfLadingsId": {
                "data_type": "str",
                "filter": "(\\s)"
            }
        },
        # "address_repair": {
        #     "db": {
        #         "pub": {
        #             "user": "co",
        #             "pwd": "Co&23@2332$22",
        #             "server": "db.test.com:1433",
        #             "database": "CO_PUB"
        #         }
        #     },
        #     "repairs": [
        #         {
        #             "key": "DeliveryPlaceName",
        #             "db_key": "pub",
        #             "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
        #             "column": [
        #                 0,
        #                 1,
        #                 2,
        #                 3
        #             ],
        #             "value": 4,
        #             "mapping": "DeliveryPlaceId",
        #             "old_val_handle": "empty"
        #         },
        #         {
        #             "key": "DestinationPortName",
        #             "db_key": "pub",
        #             "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
        #             "column": [
        #                 0,
        #                 1,
        #                 2,
        #                 3
        #             ],
        #             "value": 4,
        #             "mapping": "DestinationPortId",
        #             "old_val_handle": "empty"
        #         }
        #     ]
        # }
    }
}
oocl_config = {
    "id": "AN_OOCL_",
    "parse": {
        "id": "OOCL",
        "name": "OOCL config",
        "kv": {
            "B/L Number": {
                "position_pattern": [
                    "^Type of B/L"
                ],
                "value_pattern": [
                    "[\\w\\W]*B/L Number:\\s*(?P<billoflading>[a-zA-Z]+\\d+)\\s*B/L\\s*Vessel/Voyage\\s*:\\s*(?P<Vessel>[\\w\\s]*)(?:\\n|\\r)",
                    "[\\w\\W]*B/L Number:\\s*(?P<billoflading>[a-zA-Z]+\\d+)\\s*B/L\\s*Vessel/Voyage"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VesselName",
                        "key": "Vessel",
                        "pattern_list": [
                            "(?P<value>[\\w\\W]*)\\s+(?P<s2>\\w*)"
                        ]
                    },
                    {
                        "keyword": "VoyageNo",
                        "key": "Vessel",
                        "pattern_list": [
                            "(?P<s1>[\\w\\W]*)\\s+(?P<value>\\w*)"
                        ]
                    },
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            },
            "Vessel": {
                "position_pattern": [
                    "^VESSEL/VOYAGE[\\w\\W]*?ARRIVING AT POD"
                ],
                "value_pattern": [
                    "VESSEL/VOYAGE[\\w\\W]*?ARRIVING AT POD(?:\\s*|\\n)(?P<Vessel>[\\w\\W]*)\\s+(?P<VoyageNo>[a-zA-Z0-9]{4,})(?:\\s|\\n|$)"
                ],
                "repeat_count": 1,
                "find_mode": "v",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VesselName",
                        "key": "Vessel"
                    },
                    {
                        "keyword": "VoyageNo",
                        "key": "VoyageNo"
                    }
                ]
            },
            "ETA": {
                "position_pattern": [
                    "^ESTIMATE\\s*ARRIVAL\\s*AT\\s*POD"
                ],
                "value_pattern": [
                    "[\\w\\W]*?:\\s*(?P<name>[^\\n]*)(?:\\r|\\n)(?P<date>[a-zA-Z]*\\s*,\\s*\\d+\\s*[a-zA-Z]{2,}\\s*,\\s*\\d+\\s*\\d+:\\d+\\s*(PM|AM))"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DestinationPortName",
                        "key": "name"
                    },
                    {
                        "keyword": "EstimatedArrivalDate",
                        "key": "date"
                    }
                ]
            },
            "EST": {
                "position_pattern": [
                    "^EST\\s*CARGO\\s*AVAILABLE\\s*AT\\s*:"
                ],
                "value_pattern": [
                    "[\\w\\W]*?:\\s*(?P<name>[^\\n]*)(?:\\r|\\n)(?P<date>[a-zA-Z]*\\s*,\\s*\\d+\\s*[a-zA-Z]{2,}\\s*,\\s*\\d+\\s*\\d+:\\d+\\s*(PM|AM))"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DeliveryPlaceName",
                        "key": "name"
                    },
                    {
                        "keyword": "DeliveryEstimatedArrivalDate",
                        "key": "date"
                    }
                ]
            }
        },
        "table": {
            "containers": {
                "position_pattern": [
                    "CNTR\\s*SIZE/\\s*TYPE"
                ],
                "separator": "\n",
                "repl_separator": " ",
                "find_mode": "v",
                "separator_mode": "regex",
                "column": [
                    "ContainerNo",
                    "ContainerSize",
                    "ActualArrivalDate",
                    "ITNo"
                ],
                "behaviors": [
                    {
                        "over_action": "row",
                        "value_pattern": [
                            "(?P<col_2>\\d+[a-zA-Z]+)|(?P<col_1>[a-zA-Z]{4,}\\d{7,})|(?P<col_3>\\d+-\\d+-\\d+(?:T|)\\d+:\\d+:\\d+)|(?P<col_4>[a-zA-Z]{1,3}\\d+)"
                        ],
                        "action": []
                    },
                    {
                        "over_action": "end",
                        "value_pattern": [
                            "^(Remarks)"
                        ]
                    }
                ]
            }
        },
        "data_type_format": {
            "DeliveryEstimatedArrivalDate": {
                "data_type": "time",
                "format": "%A, %d %b, %Y %I:%M %p",
                "filter": ""
            },
            "EstimatedArrivalDate": {
                "data_type": "time",
                "format": "%A, %d %b, %Y %I:%M %p",
                "filter": ""
            }
        },
        "address_repair": {
            "db": {
                "pub": {
                    "user": "co",
                    "pwd": "Cocsp@20200312",
                    "server": "172.18.39.13:3344",
                    "database": "CO_PUB"
                }
            },
            # "repairs": [
            #     {
            #         "key": "DestinationPortName",
            #         "db_key": "pub",
            #         "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
            #         "column": [
            #             0,
            #             1,
            #             2,
            #             3
            #         ],
            #         "value": 4,
            #         "mapping": "DestinationPortId",
            #         "old_val_handle": "empty"
            #     },
            #     {
            #         "key": "DeliveryPlaceName",
            #         "db_key": "pub",
            #         "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
            #         "column": [
            #             0,
            #             1,
            #             2,
            #             3
            #         ],
            #         "value": 4,
            #         "mapping": "DeliveryPlaceId",
            #         "old_val_handle": "empty"
            #     }
            # ]
        }
    }
}
config_names = []

for k, v in test_config.get('kv').items():
    action = v.get('action')
    for _item in action:
        config_names.append((k, _item.get("keyword")))


class TestExcelDocumentParser:

    def test_excel_file_parse(self):
        """
        单文件测试
        :return:
        """
        print(json.dumps(cma_config))
        print("==============================")
        name = "oocl".upper()

        doc1_config["id"] = f"AN_{name}_"

        test_config["id"] = name
        test_config["name"] = f"{name} config"
        doc1_config["parse"] = test_config
        # print(test_config)
        print(json.dumps(doc1_config))
        str_dir = f"C:\\Users\\APing\\Desktop\\temp\\{name}"
        # str_dir = f"C:\\Users\\APing\\Desktop\\temp\\"
        files = os.listdir(str_dir)
        size = 0
        f_list = []
        _count = 1

        for f in files:
            # if _count > 10:
            #     break
            _count += 1
            if f != "bl2695880620.xlsx":
                continue
            if f.endswith('.xlsx') and not f.startswith('~'):
                # factory = DocParserFactory.create("excel2",
                #                                   r"C:\Users\APing\Desktop\temp\cma\ARR_JXTL311318.xlsx",
                #                                   test_config)
                factory = DocParserFactory.create("excel2", os.path.join(str_dir, f), oocl_config["parse"])
                result, errors = factory.parse()
                size += 1
                if len(result) == 0:
                    f_list.append({f: errors})
                else:
                    err_list = []
                    for nm in config_names:
                        v1 = result[0].get(nm[1])
                        if (v1 is None or v1 == "") and len(errors[0]) > 0 and len(
                                [x for x in errors[0].keys() if x.find(nm[0]) > -1]) > 0:
                            err_list.append(nm[1])
                            break
                    if len(err_list) > 0:
                        f_list.append({f: (err_list, errors)})

                print(f, result, errors)
        print(f"一共解析文件数量：{size}, err-size: {len(f_list)}")
        for _nm in f_list:
            print(_nm)
    # def test_excel_dir_parse(self):
    #     """
    #     测试文件夹下的拥有对应名称配置的excel文件
    #     :return:
    #     """
    #     path = os.getcwd() + "\\files"
    #     dirs = os.listdir(path)
    #     for file in dirs:
    #         name = file.split(".")[0]
    #         if ".xlsx" in file:
    #             _config = Config.get_config(name.lower())
    #             if _config is None:
    #                 continue
    #             factory = DocParserFactory.create("excel2", "%s\\%s.xlsx" % (path, name.lower()), _config)
    #             result, errors = factory.parse()
    #             print("=========================", file, "========================")
    #             print(_config)
    #             print(path + file)
    #             print(result)
    #             print(errors)
    #             print("------------------------------------------------------------")
    #             print("\r\n\r\n")


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
