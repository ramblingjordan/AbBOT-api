import { IIPAddressBlock } from "./IPValidation";

const ips: IIPAddressBlock[] = [

    { town: `Allen`, segment1: 24, segment2: 27, segment3low: 72, segment3high: 72 },
    
    { town: `Alpine`, segment1: 65, segment2: 65, segment3low: 132, segment3high: 132 },
    
    { town: `Alvin`, segment1: 50, segment2: 175, segment3low: 228, segment3high: 228 },
    
    { town: `Arlington`, segment1: 23, segment2: 117, segment3low: 126, segment3high: 126 },
    
    { town: `Austin`, segment1: 24, segment2: 153, segment3low: 156, segment3high: 156 },
    { town: `Austin`, segment1: 66, segment2: 193, segment3low: 112, segment3high: 113 },
    { town: `Austin`, segment1: 50, segment2: 94, segment3low: 23, segment3high: 23 },
    
    { town: `Beaumont`, segment1: 24, segment2: 173, segment3low: 59, segment3high: 59 },
    { town: `Beaumont`, segment1: 63, segment2: 174, segment3low: 138, segment3high: 138 },
    
    { town: `Benbrook`, segment1: 24, segment2: 219, segment3low: 225, segment3high: 225 },
    
    { town: `Conroe`, segment1: 50, segment2: 15, segment3low: 108, segment3high: 108 },
    { town: `Conroe`, segment1: 50, segment2: 21, segment3low: 240, segment3high: 240 },
    
    { town: `Dallas`, segment1: 32, segment2: 144, segment3low: 6, segment3high: 7 },
    { town: `Dallas`, segment1: 17, segment2: 253, segment3low: 118, segment3high: 118 },
    { town: `Dallas`, segment1: 67, segment2: 216, segment3low: 80, segment3high: 95 },
    { town: `Dallas`, segment1: 23, segment2: 119, segment3low: 13, segment3high: 15 },
    { town: `Dallas`, segment1: 64, segment2: 197, segment3low: 59, segment3high: 59 },
    { town: `Dallas`, segment1: 32, segment2: 135, segment3low: 78, segment3high: 98 },
    { town: `Dallas`, segment1: 4, segment2: 68, segment3low: 19, segment3high: 10 },
    { town: `Dallas`, segment1: 63, segment2: 133, segment3low: 167, segment3high: 167 },
    { town: `Dallas`, segment1: 65, segment2: 155, segment3low: 134, segment3high: 135 },
    { town: `Dallas`, segment1: 68, segment2: 109, segment3low: 248, segment3high: 248 },
    { town: `Dallas`, segment1: 64, segment2: 56, segment3low: 170, segment3high: 170 },
    { town: `Dallas`, segment1: 32, segment2: 149, segment3low: 194, segment3high: 197 },
    { town: `Dallas`, segment1: 32, segment2: 168, segment3low: 139, segment3high: 139 },
    { town: `Dallas`, segment1: 68, segment2: 90, segment3low: 101, segment3high: 101 },
    { town: `Dallas`, segment1: 24, segment2: 242, segment3low: 248, segment3high: 248 },
    { town: `Dallas`, segment1: 23, segment2: 33, segment3low: 244, segment3high: 247 },
    { town: `Dallas`, segment1: 23, segment2: 33, segment3low: 247, segment3high: 247 },
    { town: `Dallas`, segment1: 66, segment2: 106, segment3low: 98, segment3high: 98 },
    
    { town: `Denton`, segment1: 47, segment2: 184, segment3low: 118, segment3high: 121 },
    { town: `Denton`, segment1: 24, segment2: 206, segment3low: 145, segment3high: 145 },
    
    { town: `Fort Worth`, segment1: 12, segment2: 184, segment3low: 253, segment3high: 254 },
    { town: `Fort Worth`, segment1: 47, segment2: 32, segment3low: 223, segment3high: 223 },
    { town: `Fort Worth`, segment1: 12, segment2: 203, segment3low: 146, segment3high: 147 },
    { town: `Fort Worth`, segment1: 12, segment2: 90, segment3low: 92, segment3high: 92 },
    
    { town: `Friendswood`, segment1: 50, segment2: 207, segment3low: 209, segment3high: 209 },
    
    { town: `Grapevine`, segment1: 64, segment2: 134, segment3low: 76, segment3high: 76 },
    
    { town: `Haltom City`, segment1: 66, segment2: 169, segment3low: 188, segment3high: 189 },
    
    { town: `Houston`, segment1: 66, segment2: 78, segment3low: 229, segment3high: 231 },
    { town: `Houston`, segment1: 66, segment2: 161, segment3low: 197, segment3high: 197 },
    { town: `Houston`, segment1: 66, segment2: 3, segment3low: 44, segment3high: 46 },
    { town: `Houston`, segment1: 50, segment2: 162, segment3low: 44, segment3high: 44 },
    { town: `Houston`, segment1: 45, segment2: 17, segment3low: 135, segment3high: 135 },
    
    { town: `Hurst`, segment1: 68, segment2: 91, segment3low: 35, segment3high: 35 },
    
    { town: `Irving`, segment1: 64, segment2: 129, segment3low: 174, segment3high: 174 },
    { town: `Irving`, segment1: 50, segment2: 84, segment3low: 165, segment3high: 165 },
    { town: `Irving`, segment1: 64, segment2: 195, segment3low: 138, segment3high: 143 },
    
    { town: `Lewisville`, segment1: 47, segment2: 187, segment3low: 76, segment3high: 76 },
    
    { town: `Lubbock`, segment1: 12, segment2: 38, segment3low: 125, segment3high: 125 },
    
    { town: `McAllen`, segment1: 24, segment2: 243, segment3low: 98, segment3high: 98 },
    { town: `McAllen`, segment1: 24, segment2: 243, segment3low: 150, segment3high: 152 },
    { town: `McAllen`, segment1: 67, segment2: 10, segment3low: 39, segment3high: 39 },
    
    { town: `Plano`, segment1: 47, segment2: 185, segment3low: 248, segment3high: 248 },

    { town: `Richardson`, segment1: 47, segment2: 186, segment3low: 233, segment3high: 233 },
    { town: `Richardson`, segment1: 63, segment2: 199, segment3low: 94, segment3high: 94 },
    { town: `Richardson`, segment1: 63, segment2: 203, segment3low: 212, segment3high: 213 },
    { town: `Richardson`, segment1: 64, segment2: 218, segment3low: 64, segment3high: 64 },
    { town: `Richardson`, segment1: 64, segment2: 252, segment3low: 212, segment3high: 238 },
    { town: `Richardson`, segment1: 65, segment2: 64, segment3low: 221, segment3high: 223 },
    { town: `Richardson`, segment1: 65, segment2: 68, segment3low: 3, segment3high: 4 },
    { town: `Richardson`, segment1: 66, segment2: 136, segment3low: 184, segment3high: 187 },
    { town: `Richardson`, segment1: 66, segment2: 137, segment3low: 185, segment3high: 185},
    { town: `Richardson`, segment1: 66, segment2: 142, segment3low: 202, segment3high: 202},
    { town: `Richardson`, segment1: 67, segment2: 38, segment3low: 82, segment3high: 82 },
    { town: `Richardson`, segment1: 68, segment2: 72, segment3low: 157, segment3high: 158 },

    { town: `Rosenberg`, segment1: 66, segment2: 235, segment3low: 81, segment3high: 81 },
    
    { town: `San Antonio`, segment1: 12, segment2: 7, segment3low: 34, segment3high: 35 },
    { town: `San Antonio`, segment1: 12, segment2: 207, segment3low: 43, segment3high: 43 },
    { town: `San Antonio`, segment1: 15, segment2: 117, segment3low: 166, segment3high: 166 },
    { town: `San Antonio`, segment1: 15, segment2: 120, segment3low: 172, segment3high: 172 },
    { town: `San Antonio`, segment1: 15, segment2: 128, segment3low: 234, segment3high: 235 },
    { town: `San Antonio`, segment1: 15, segment2: 132, segment3low: 71, segment3high: 72 },
    { town: `San Antonio`, segment1: 15, segment2: 133, segment3low: 222, segment3high: 222 },
    { town: `San Antonio`, segment1: 15, segment2: 134, segment3low: 233, segment3high: 234 },
    { town: `San Antonio`, segment1: 15, segment2: 138, segment3low: 0, segment3high: 1 },
    { town: `San Antonio`, segment1: 15, segment2: 143, segment3low: 78, segment3high: 78 },
    { town: `San Antonio`, segment1: 15, segment2: 150, segment3low: 168, segment3high: 169 },
    { town: `San Antonio`, segment1: 15, segment2: 156, segment3low: 247, segment3high: 248 },
    { town: `San Antonio`, segment1: 15, segment2: 157, segment3low: 163, segment3high: 163 },
    { town: `San Antonio`, segment1: 15, segment2: 159, segment3low: 219, segment3high: 219 },
    { town: `San Antonio`, segment1: 15, segment2: 160, segment3low: 97, segment3high: 99 },
    { town: `San Antonio`, segment1: 15, segment2: 160, segment3low: 200, segment3high: 202 },
    { town: `San Antonio`, segment1: 15, segment2: 162, segment3low: 246, segment3high: 249 },
    { town: `San Antonio`, segment1: 15, segment2: 176, segment3low: 79, segment3high: 81 },
    { town: `San Antonio`, segment1: 15, segment2: 181, segment3low: 151, segment3high: 152 },
    { town: `San Antonio`, segment1: 15, segment2: 189, segment3low: 87, segment3high: 88 },
    { town: `San Antonio`, segment1: 15, segment2: 190, segment3low: 132, segment3high: 132 },
    { town: `San Antonio`, segment1: 15, segment2: 193, segment3low: 69, segment3high: 70 },
    { town: `San Antonio`, segment1: 15, segment2: 211, segment3low: 169, segment3high: 169 },
    { town: `San Antonio`, segment1: 15, segment2: 219, segment3low: 34, segment3high: 34 },
    { town: `San Antonio`, segment1: 15, segment2: 232, segment3low: 43, segment3high: 43 },
    { town: `San Antonio`, segment1: 15, segment2: 154, segment3low: 136, segment3high: 137 },
    { town: `San Antonio`, segment1: 15, segment2: 131, segment3low: 196, segment3high: 200 },
    { town: `San Antonio`, segment1: 15, segment2: 235, segment3low: 202, segment3high: 203 },
    { town: `San Antonio`, segment1: 15, segment2: 237, segment3low: 79, segment3high: 79 },
    { town: `San Antonio`, segment1: 15, segment2: 243, segment3low: 228, segment3high: 229 },
    { town: `San Antonio`, segment1: 40, segment2: 141, segment3low: 126, segment3high: 126 },
    
    { town: `San Marcos`, segment1: 24, segment2: 155, segment3low: 227, segment3high: 227 },

    { town: `Schertz`, segment1: 45, segment2: 21, segment3low: 35, segment3high: 35 },

    { town: `Seguin`, segment1: 67, segment2: 78, segment3low: 77, segment3high: 77 },
]
