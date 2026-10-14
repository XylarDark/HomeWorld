# L_Field placement

Greybox mass for the field zone. The contract is Lib/02_Zones/gather/FIELD.json. This file is the coordinate list. Content/Python/place_field_greybox.py reads the JSON block and does not invent a spot.

Units are meters. The meadow centre is the arrival. There is no path and no landing ring. Herb centres are frozen in this file: at least 30 m apart, inside the meadow and off the edge bands. The scatter was seeded 20261014, but no generator ships with the repo, so edit a centre here rather than re-seeding. A dual adds one node 1 m east. A triple adds that node and one node 1 m north.

The two forest edges use one pine sequence and one 12 m step. The south-west corner pine is shared. Cliff faces are three masses on the north lip. The river is the 7 m channel on the east. Authored beast-pad offsets from the old field are not placed. A few pines stand in the meadow, far apart. Bulls match the herb-centre count. Half stand 2.5 m from a herb. The other half stay at least 8 m from every herb.

```json
{
  "player": {
    "x": 0,
    "y": 0,
    "z": 1.1,
    "yaw": 0
  },
  "floor": {
    "label": "SM_Field_Floor",
    "x": 0,
    "y": 0,
    "z": -0.5,
    "sx": 420,
    "sy": 420,
    "sz": 1
  },
  "cliffs": [
    {
      "label": "SM_Field_Cliff_A",
      "x": -140,
      "y": 214,
      "z": 4,
      "sx": 120,
      "sy": 8,
      "sz": 8
    },
    {
      "label": "SM_Field_Cliff_B",
      "x": 0,
      "y": 218,
      "z": 6,
      "sx": 100,
      "sy": 16,
      "sz": 12
    },
    {
      "label": "SM_Field_Cliff_C",
      "x": 140,
      "y": 212,
      "z": 3,
      "sx": 120,
      "sy": 6,
      "sz": 6
    }
  ],
  "drop": {
    "label": "SM_Field_Cliff_Drop",
    "x": 0,
    "y": 230,
    "z": -28.5,
    "sx": 420,
    "sy": 40,
    "sz": 1
  },
  "river": {
    "label": "SM_Field_River",
    "x": 213.5,
    "y": 0,
    "z": -1.5,
    "sx": 7,
    "sy": 420,
    "sz": 2
  },
  "river_bank": {
    "label": "SM_Field_River_Bank",
    "x": 218,
    "y": 0,
    "z": 1.5,
    "sx": 2,
    "sy": 420,
    "sz": 4
  },
  "forest": {
    "y_south": -210,
    "x_west": -210,
    "start": -210,
    "end": 210,
    "step": 12,
    "sequence": [
      "SM_Size_Pine_S",
      "SM_Size_Pine_M",
      "SM_Size_Pine_L",
      "SM_Size_Pine_M"
    ]
  },
  "herbs": [
    {
      "x": 81.9,
      "y": -117.1,
      "kind": "triple"
    },
    {
      "x": 96.5,
      "y": 110.6,
      "kind": "dual"
    },
    {
      "x": 32.8,
      "y": -60.9,
      "kind": "dual"
    },
    {
      "x": -51.1,
      "y": 9.4,
      "kind": "dual"
    },
    {
      "x": 106.8,
      "y": 156.3,
      "kind": "dual"
    },
    {
      "x": -23.0,
      "y": -68.2,
      "kind": "dual"
    },
    {
      "x": -158.4,
      "y": 122.6,
      "kind": "single"
    },
    {
      "x": 73.8,
      "y": 171.1,
      "kind": "single"
    },
    {
      "x": 1.2,
      "y": 45.1,
      "kind": "single"
    },
    {
      "x": -85.1,
      "y": -28.1,
      "kind": "single"
    },
    {
      "x": -107.7,
      "y": -153.2,
      "kind": "single"
    },
    {
      "x": -59.2,
      "y": -140.1,
      "kind": "single"
    },
    {
      "x": -162.7,
      "y": -80.3,
      "kind": "single"
    },
    {
      "x": 154.5,
      "y": 143.0,
      "kind": "single"
    },
    {
      "x": 169.4,
      "y": -147.6,
      "kind": "single"
    },
    {
      "x": -49.5,
      "y": -45.1,
      "kind": "single"
    },
    {
      "x": -106.6,
      "y": 161.2,
      "kind": "single"
    },
    {
      "x": 6.8,
      "y": -178.2,
      "kind": "single"
    },
    {
      "x": 177.6,
      "y": -83.2,
      "kind": "single"
    },
    {
      "x": -148.4,
      "y": 14.2,
      "kind": "single"
    },
    {
      "x": 98.7,
      "y": -3.3,
      "kind": "triple"
    },
    {
      "x": -144.8,
      "y": -50.9,
      "kind": "dual"
    },
    {
      "x": 27.4,
      "y": 163.0,
      "kind": "dual"
    },
    {
      "x": -173.7,
      "y": -176.4,
      "kind": "dual"
    },
    {
      "x": -66.3,
      "y": -98.4,
      "kind": "dual"
    },
    {
      "x": 81.9,
      "y": 31.0,
      "kind": "dual"
    },
    {
      "x": -93.3,
      "y": 77.0,
      "kind": "single"
    },
    {
      "x": -86.4,
      "y": -125.9,
      "kind": "single"
    },
    {
      "x": -171.7,
      "y": -16.3,
      "kind": "single"
    },
    {
      "x": 31.7,
      "y": -10.1,
      "kind": "single"
    },
    {
      "x": 40.4,
      "y": 59.6,
      "kind": "single"
    },
    {
      "x": 72.4,
      "y": -177.1,
      "kind": "single"
    },
    {
      "x": 134.7,
      "y": 178.2,
      "kind": "single"
    },
    {
      "x": 104.9,
      "y": -84.7,
      "kind": "single"
    },
    {
      "x": -4.0,
      "y": -37.1,
      "kind": "single"
    },
    {
      "x": 29.7,
      "y": 118.8,
      "kind": "single"
    },
    {
      "x": -117.9,
      "y": 97.5,
      "kind": "single"
    },
    {
      "x": -40.6,
      "y": 178.8,
      "kind": "single"
    },
    {
      "x": -23.6,
      "y": -153.6,
      "kind": "single"
    },
    {
      "x": -118.2,
      "y": -28.7,
      "kind": "single"
    },
    {
      "x": 143.0,
      "y": -71.5,
      "kind": "triple"
    },
    {
      "x": -100.1,
      "y": -64.0,
      "kind": "dual"
    },
    {
      "x": 125.4,
      "y": -143.5,
      "kind": "dual"
    },
    {
      "x": 29.9,
      "y": -108.8,
      "kind": "dual"
    },
    {
      "x": 44.0,
      "y": -138.4,
      "kind": "dual"
    },
    {
      "x": 60.5,
      "y": 93.1,
      "kind": "dual"
    },
    {
      "x": -21.3,
      "y": 5.3,
      "kind": "single"
    },
    {
      "x": -35.0,
      "y": 41.9,
      "kind": "single"
    },
    {
      "x": -142.7,
      "y": 172.2,
      "kind": "single"
    },
    {
      "x": -55.6,
      "y": 151.9,
      "kind": "single"
    },
    {
      "x": 156.4,
      "y": 62.9,
      "kind": "single"
    },
    {
      "x": 176.7,
      "y": 163.7,
      "kind": "single"
    },
    {
      "x": 57.0,
      "y": 144.9,
      "kind": "single"
    },
    {
      "x": -114.8,
      "y": -115.5,
      "kind": "single"
    },
    {
      "x": 87.2,
      "y": -42.1,
      "kind": "single"
    },
    {
      "x": 159.9,
      "y": 109.0,
      "kind": "single"
    },
    {
      "x": -2.8,
      "y": 127.9,
      "kind": "single"
    },
    {
      "x": -174.1,
      "y": 95.4,
      "kind": "single"
    },
    {
      "x": 118.1,
      "y": 23.9,
      "kind": "single"
    },
    {
      "x": -66.3,
      "y": -178.0,
      "kind": "single"
    },
    {
      "x": -107.9,
      "y": 2.0,
      "kind": "triple"
    },
    {
      "x": 39.3,
      "y": -172.7,
      "kind": "dual"
    },
    {
      "x": 10.2,
      "y": 74.1,
      "kind": "dual"
    },
    {
      "x": -141.5,
      "y": -134.2,
      "kind": "dual"
    },
    {
      "x": -46.2,
      "y": 77.8,
      "kind": "dual"
    },
    {
      "x": 135.2,
      "y": -17.7,
      "kind": "dual"
    },
    {
      "x": 54.7,
      "y": 16.9,
      "kind": "single"
    },
    {
      "x": 82.8,
      "y": 70.8,
      "kind": "single"
    },
    {
      "x": -119.4,
      "y": 127.6,
      "kind": "single"
    },
    {
      "x": 105.8,
      "y": -171.3,
      "kind": "single"
    },
    {
      "x": -80.1,
      "y": 104.1,
      "kind": "single"
    },
    {
      "x": -13.9,
      "y": -118.4,
      "kind": "single"
    },
    {
      "x": 112.0,
      "y": 63.5,
      "kind": "single"
    },
    {
      "x": -142.1,
      "y": -180.0,
      "kind": "single"
    },
    {
      "x": -143.1,
      "y": 71.5,
      "kind": "single"
    },
    {
      "x": 175.0,
      "y": -13.8,
      "kind": "single"
    },
    {
      "x": -72.5,
      "y": 45.1,
      "kind": "single"
    },
    {
      "x": 150.3,
      "y": 32.5,
      "kind": "single"
    },
    {
      "x": -37.3,
      "y": 114.6,
      "kind": "single"
    },
    {
      "x": 129.1,
      "y": 121.1,
      "kind": "single"
    },
    {
      "x": -4.0,
      "y": 174.8,
      "kind": "triple"
    },
    {
      "x": -179.8,
      "y": 27.5,
      "kind": "dual"
    },
    {
      "x": 147.5,
      "y": -105.9,
      "kind": "dual"
    },
    {
      "x": 9.0,
      "y": -82.4,
      "kind": "dual"
    },
    {
      "x": 180.0,
      "y": 39.8,
      "kind": "dual"
    },
    {
      "x": 56.6,
      "y": -84.2,
      "kind": "dual"
    },
    {
      "x": -74.2,
      "y": 180.0,
      "kind": "single"
    },
    {
      "x": 61.0,
      "y": -16.9,
      "kind": "single"
    },
    {
      "x": 146.0,
      "y": -174.7,
      "kind": "single"
    },
    {
      "x": -174.7,
      "y": 165.0,
      "kind": "single"
    },
    {
      "x": -25.4,
      "y": 151.7,
      "kind": "single"
    },
    {
      "x": -179.9,
      "y": -111.6,
      "kind": "single"
    },
    {
      "x": -111.7,
      "y": 42.1,
      "kind": "single"
    },
    {
      "x": 9.4,
      "y": -139.0,
      "kind": "single"
    },
    {
      "x": -130.8,
      "y": -86.8,
      "kind": "single"
    },
    {
      "x": -178.1,
      "y": -52.6,
      "kind": "single"
    },
    {
      "x": -175.3,
      "y": -143.3,
      "kind": "single"
    },
    {
      "x": 132.8,
      "y": 85.4,
      "kind": "single"
    },
    {
      "x": 179.2,
      "y": -45.9,
      "kind": "single"
    },
    {
      "x": 120.6,
      "y": -49.1,
      "kind": "single"
    },
    {
      "x": -18.1,
      "y": 88.4,
      "kind": "triple"
    },
    {
      "x": 83.2,
      "y": -148.0,
      "kind": "dual"
    },
    {
      "x": 116.6,
      "y": -114.1,
      "kind": "dual"
    },
    {
      "x": 15.4,
      "y": 17.2,
      "kind": "dual"
    }
  ],
  "trees": [
    {
      "label": "SM_Field_Tree_01",
      "mesh": "SM_Size_Pine_S",
      "x": -52.9,
      "y": -104.7
    },
    {
      "label": "SM_Field_Tree_02",
      "mesh": "SM_Size_Pine_M",
      "x": 10.8,
      "y": -40.3
    },
    {
      "label": "SM_Field_Tree_03",
      "mesh": "SM_Size_Pine_L",
      "x": -132.6,
      "y": 2.2
    },
    {
      "label": "SM_Field_Tree_04",
      "mesh": "SM_Size_Pine_S",
      "x": -129.0,
      "y": -122.8
    },
    {
      "label": "SM_Field_Tree_05",
      "mesh": "SM_Size_Pine_M",
      "x": -112.9,
      "y": -83.0
    },
    {
      "label": "SM_Field_Tree_06",
      "mesh": "SM_Size_Pine_L",
      "x": 38.2,
      "y": 134.3
    },
    {
      "label": "SM_Field_Tree_07",
      "mesh": "SM_Size_Pine_S",
      "x": 142.9,
      "y": -136.0
    },
    {
      "label": "SM_Field_Tree_08",
      "mesh": "SM_Size_Pine_M",
      "x": 107.5,
      "y": -63.1
    }
  ],
  "bulls": [
    {
      "label": "SK_Field_Bull_001",
      "x": 84.4,
      "y": -117.1,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_002",
      "x": 96.5,
      "y": 113.1,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_003",
      "x": 35.3,
      "y": -60.9,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_004",
      "x": -51.1,
      "y": 11.9,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_005",
      "x": 109.3,
      "y": 156.3,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_006",
      "x": -23.0,
      "y": -65.7,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_007",
      "x": -155.9,
      "y": 122.6,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_008",
      "x": 73.8,
      "y": 173.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_009",
      "x": 3.7,
      "y": 45.1,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_010",
      "x": -85.1,
      "y": -25.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_011",
      "x": -105.2,
      "y": -153.2,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_012",
      "x": -59.2,
      "y": -137.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_013",
      "x": -160.2,
      "y": -80.3,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_014",
      "x": 154.5,
      "y": 145.5,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_015",
      "x": 171.9,
      "y": -147.6,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_016",
      "x": -49.5,
      "y": -42.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_017",
      "x": -104.1,
      "y": 161.2,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_018",
      "x": 6.8,
      "y": -175.7,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_019",
      "x": 180.1,
      "y": -83.2,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_020",
      "x": -148.4,
      "y": 16.7,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_021",
      "x": 101.2,
      "y": -3.3,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_022",
      "x": -144.8,
      "y": -48.4,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_023",
      "x": 29.9,
      "y": 163.0,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_024",
      "x": -173.7,
      "y": -173.9,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_025",
      "x": -63.8,
      "y": -98.4,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_026",
      "x": 81.9,
      "y": 33.5,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_027",
      "x": -90.8,
      "y": 77.0,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_028",
      "x": -86.4,
      "y": -123.4,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_029",
      "x": -169.2,
      "y": -16.3,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_030",
      "x": 31.7,
      "y": -7.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_031",
      "x": 42.9,
      "y": 59.6,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_032",
      "x": 72.4,
      "y": -174.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_033",
      "x": 137.2,
      "y": 178.2,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_034",
      "x": 104.9,
      "y": -82.2,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_035",
      "x": -1.5,
      "y": -37.1,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_036",
      "x": 29.7,
      "y": 121.3,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_037",
      "x": -115.4,
      "y": 97.5,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_038",
      "x": -40.6,
      "y": 181.3,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_039",
      "x": -21.1,
      "y": -153.6,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_040",
      "x": -118.2,
      "y": -26.2,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_041",
      "x": 145.5,
      "y": -71.5,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_042",
      "x": -100.1,
      "y": -61.5,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_043",
      "x": 127.9,
      "y": -143.5,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_044",
      "x": 29.9,
      "y": -106.3,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_045",
      "x": 46.5,
      "y": -138.4,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_046",
      "x": 60.5,
      "y": 95.6,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_047",
      "x": -18.8,
      "y": 5.3,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_048",
      "x": -35.0,
      "y": 44.4,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_049",
      "x": -140.2,
      "y": 172.2,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_050",
      "x": -55.6,
      "y": 154.4,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_051",
      "x": 158.9,
      "y": 62.9,
      "yaw": 180,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_052",
      "x": 176.7,
      "y": 166.2,
      "yaw": 270,
      "beside": true
    },
    {
      "label": "SK_Field_Bull_053",
      "x": 72.8,
      "y": -104.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_054",
      "x": 85.8,
      "y": 98.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_055",
      "x": 94.9,
      "y": 138.9,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_056",
      "x": -20.4,
      "y": -60.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_057",
      "x": -140.8,
      "y": 109.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_058",
      "x": 65.6,
      "y": 152.1,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_059",
      "x": -75.6,
      "y": -25.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_060",
      "x": -95.7,
      "y": -136.2,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_061",
      "x": -52.6,
      "y": -124.5,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_062",
      "x": -144.6,
      "y": -71.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_063",
      "x": 137.3,
      "y": 127.1,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_064",
      "x": 150.6,
      "y": -131.2,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_065",
      "x": -94.8,
      "y": 143.3,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_066",
      "x": 6.1,
      "y": -158.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_067",
      "x": 157.9,
      "y": -74.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_068",
      "x": -131.9,
      "y": 12.7,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_069",
      "x": 87.7,
      "y": -3.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_070",
      "x": -128.7,
      "y": -45.2,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_071",
      "x": -76.0,
      "y": -123.9,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_072",
      "x": 24.3,
      "y": 144.9,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_073",
      "x": -154.4,
      "y": -156.8,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_074",
      "x": -58.9,
      "y": -87.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_075",
      "x": 72.8,
      "y": 27.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_076",
      "x": -83.0,
      "y": 68.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_077",
      "x": 90.8,
      "y": -90.2,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_078",
      "x": -152.6,
      "y": -14.5,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_079",
      "x": 64.4,
      "y": -157.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_080",
      "x": 119.8,
      "y": 158.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_081",
      "x": 108.1,
      "y": 97.1,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_082",
      "x": 26.4,
      "y": 105.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_083",
      "x": -104.8,
      "y": 86.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_084",
      "x": -36.1,
      "y": 158.9,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_085",
      "x": 112.1,
      "y": -57.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_086",
      "x": -21.0,
      "y": -136.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_087",
      "x": 16.7,
      "y": -36.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_088",
      "x": -105.0,
      "y": -25.5,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_089",
      "x": -89.0,
      "y": -56.9,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_090",
      "x": 111.5,
      "y": -127.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_091",
      "x": 26.6,
      "y": -96.7,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_092",
      "x": 53.9,
      "y": -11.6,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_093",
      "x": 30.0,
      "y": 77.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_094",
      "x": -49.8,
      "y": 20.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_095",
      "x": 39.1,
      "y": -123.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_096",
      "x": -109.7,
      "y": -57.7,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_097",
      "x": 13.4,
      "y": -128.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_098",
      "x": -63.8,
      "y": 78.7,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_099",
      "x": 53.8,
      "y": 82.7,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_100",
      "x": -126.9,
      "y": 153.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_101",
      "x": 28.1,
      "y": 38.4,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_102",
      "x": -49.4,
      "y": 135.0,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_103",
      "x": 139.1,
      "y": 55.9,
      "yaw": 90,
      "beside": false
    },
    {
      "label": "SK_Field_Bull_104",
      "x": -158.8,
      "y": 100.2,
      "yaw": 90,
      "beside": false
    }
  ]
}
```
