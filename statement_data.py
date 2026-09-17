"""
ข้อมูลและตัวแปลงรายการเดินบัญชี (Statement) ธนาคารกรุงไทย
ร้านศรีบุตรา โดย นายณัฐวุฒิ ศรีบุตรา บัญชี 6153107532
ประจำเดือนมิถุนายน 2569 (01/06/69 - 30/06/69)
"""

from typing import List, Dict, Any

# รายการธุรกรรมทั้ง 126 รายการ (ฝาก 79, ถอน 47)
JUNE_TRANSACTIONS = [

    # Page 1
    {"date": "2026-06-01", "time": "07:55", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "1020-0891462504", "withdrawal": 874.19, "deposit": 0.0, "balance": 123613.48, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-06-01", "time": "11:15", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "1020-0891462504", "withdrawal": 694.43, "deposit": 0.0, "balance": 122919.05, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-06-01", "time": "16:36", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "1020-0891462504", "withdrawal": 426.93, "deposit": 0.0, "balance": 122492.12, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-06-02", "time": "02:45", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 545.20, "balance": 123037.32, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-02", "time": "09:14", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 10262.00, "deposit": 0.0, "balance": 112775.32, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-02", "time": "12:28", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 817.80, "balance": 113593.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-02", "time": "17:01", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 14444.00, "deposit": 0.0, "balance": 99149.12, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-02", "time": "18:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 55010.00, "balance": 154159.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-02", "time": "22:21", "type": "โอนเงินออก (SW)", "desc": "Trt 100125753136", "withdrawal": 17100.00, "deposit": 0.0, "balance": 137059.12, "channel": "Transfer", "branch": "0"},
    {"date": "2026-06-03", "time": "02:40", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1107.20, "balance": 138166.32, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-03", "time": "08:41", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1660.80, "balance": 139827.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-03", "time": "09:54", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6140134137", "withdrawal": 20000.00, "deposit": 0.0, "balance": 119827.12, "channel": "Transfer", "branch": "615"},
    {"date": "2026-06-04", "time": "02:27", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1619.60, "balance": 121446.72, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-04", "time": "11:39", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2429.40, "balance": 123876.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-04", "time": "17:04", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 21000.00, "balance": 144876.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-04", "time": "17:10", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 13140.00, "balance": 158016.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-04", "time": "18:27", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 4690.00, "deposit": 0.0, "balance": 153326.12, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-05", "time": "01:50", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-1391212259- Future Amount: 445 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 445.00, "balance": 153771.12, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-06-05", "time": "02:27", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1979.60, "balance": 155750.72, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-05", "time": "12:14", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2932.40, "balance": 158683.12, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-05", "time": "17:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 5000.00, "balance": 163683.12, "channel": "Welfare", "branch": "108682"},

    # Page 2
    {"date": "2026-06-06", "time": "02:09", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "20933-0891462504", "withdrawal": 1885.68, "deposit": 0.0, "balance": 161797.44, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-06-06", "time": "02:38", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1201.20, "balance": 162998.64, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-06", "time": "09:18", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1801.80, "balance": 164800.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-06", "time": "15:23", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 5511.00, "deposit": 0.0, "balance": 159289.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-06", "time": "16:10", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 5434.00, "deposit": 0.0, "balance": 153855.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-06", "time": "16:43", "type": "เงินโอนเข้า (IORSDT)", "desc": "014-4260193786", "withdrawal": 0.0, "deposit": 250.00, "balance": 154105.44, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-06-06", "time": "20:06", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 500.00, "deposit": 0.0, "balance": 153605.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-07", "time": "02:38", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1428.80, "balance": 155034.24, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-07", "time": "09:30", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2143.20, "balance": 157177.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-07", "time": "16:27", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 4373.00, "deposit": 0.0, "balance": 152804.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-08", "time": "02:25", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1334.00, "balance": 154138.44, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-08", "time": "13:21", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2001.00, "balance": 156139.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-08", "time": "17:11", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 8560.00, "balance": 164699.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-08", "time": "17:14", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 6000.00, "balance": 170699.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-08", "time": "18:26", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 3995.00, "deposit": 0.0, "balance": 166704.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-08", "time": "18:27", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 992.00, "deposit": 0.0, "balance": 165712.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-09", "time": "02:23", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 793.40, "balance": 166505.84, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-09", "time": "12:23", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1175.60, "balance": 167681.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-09", "time": "17:08", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 4025.00, "balance": 171706.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-10", "time": "02:20", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1347.20, "balance": 173053.64, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-10", "time": "12:45", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2020.80, "balance": 175074.44, "channel": "Welfare", "branch": "108682"},

    # Page 3
    {"date": "2026-06-10", "time": "17:08", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 3000.00, "balance": 178074.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-11", "time": "02:36", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 609.80, "balance": 178684.24, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-11", "time": "12:01", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 866.20, "balance": 179550.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-11", "time": "15:41", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1178.00, "deposit": 0.0, "balance": 178372.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-11", "time": "15:41", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1122.00, "deposit": 0.0, "balance": 177250.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-11", "time": "17:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 600.00, "balance": 177850.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-12", "time": "02:21", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1134.40, "balance": 178984.84, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-12", "time": "11:59", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1549.60, "balance": 180534.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-13", "time": "02:28", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 958.60, "balance": 181493.04, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-13", "time": "09:22", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1334.40, "balance": 182827.44, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-13", "time": "15:19", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 3496.00, "deposit": 0.0, "balance": 179331.44, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-13", "time": "18:25", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 3474.50, "deposit": 0.0, "balance": 175856.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-13", "time": "18:27", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1224.00, "deposit": 0.0, "balance": 174632.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-14", "time": "02:14", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1330.80, "balance": 175963.74, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-14", "time": "09:22", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1893.20, "balance": 177856.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-15", "time": "01:36", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-0673204406- Future Amount: 15 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 15.00, "balance": 177871.94, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-06-15", "time": "02:14", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 577.20, "balance": 178449.14, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-15", "time": "08:28", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 14386.00, "deposit": 0.0, "balance": 164063.14, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-15", "time": "10:26", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 865.80, "balance": 164928.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-15", "time": "17:09", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 2000.00, "balance": 166928.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-15", "time": "18:00", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 11534.00, "deposit": 0.0, "balance": 155394.94, "channel": "Biller", "branch": "615"},

    # Page 4
    {"date": "2026-06-16", "time": "02:26", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 497.20, "balance": 155892.14, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-16", "time": "11:49", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 745.80, "balance": 156637.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-16", "time": "17:04", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 157637.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-17", "time": "02:14", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 540.00, "balance": 158177.94, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-17", "time": "11:45", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 808.00, "balance": 158985.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-17", "time": "17:08", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 406.00, "balance": 159391.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-17", "time": "17:18", "type": "เงินโอนเข้า (IORSDT)", "desc": "034-020252729243", "withdrawal": 0.0, "deposit": 72.00, "balance": 159463.94, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-06-17", "time": "17:33", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 606.00, "deposit": 0.0, "balance": 158857.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-17", "time": "17:34", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1131.00, "deposit": 0.0, "balance": 157726.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-18", "time": "02:17", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 466.00, "balance": 158192.94, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-18", "time": "10:44", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 16138.00, "deposit": 0.0, "balance": 142054.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-18", "time": "11:47", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 699.00, "balance": 142753.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-19", "time": "02:10", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 454.80, "balance": 143208.74, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-19", "time": "12:11", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 682.20, "balance": 143890.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-19", "time": "17:08", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 2000.00, "balance": 145890.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-20", "time": "02:17", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 525.20, "balance": 146416.14, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-20", "time": "09:51", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 787.80, "balance": 147203.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-20", "time": "14:15", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "025-BILLERID", "withdrawal": 2148.00, "deposit": 0.0, "balance": 145055.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-20", "time": "15:26", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 6240.00, "deposit": 0.0, "balance": 138815.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-20", "time": "15:29", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 537.00, "deposit": 0.0, "balance": 138278.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-20", "time": "18:27", "type": "ฝากเงินผ่าน ADM (ATSDC)", "desc": "K31368-6153107532", "withdrawal": 0.0, "deposit": 21500.00, "balance": 159778.94, "channel": "Cash_ADM", "branch": "863"},

    # Page 5
    {"date": "2026-06-20", "time": "18:35", "type": "จ่ายค่าสินค้า/บริการ (NMPSWP)", "desc": "010753700088205-1406755315900001832", "withdrawal": 100.00, "deposit": 0.0, "balance": 159678.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-20", "time": "18:58", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 500.00, "deposit": 0.0, "balance": 159178.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-21", "time": "02:09", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 396.00, "balance": 159574.94, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-21", "time": "09:36", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 594.00, "balance": 160168.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-22", "time": "02:11", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 708.00, "balance": 160876.94, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-22", "time": "08:50", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 4754.00, "deposit": 0.0, "balance": 156122.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-22", "time": "09:55", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 709.00, "balance": 156831.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-22", "time": "13:00", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 3690.00, "deposit": 0.0, "balance": 153141.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-22", "time": "13:03", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 17602.00, "deposit": 0.0, "balance": 135539.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-22", "time": "13:03", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1500.00, "deposit": 0.0, "balance": 134039.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-22", "time": "13:04", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 898.00, "deposit": 0.0, "balance": 133141.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-22", "time": "17:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 134141.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-22", "time": "21:11", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6290345389", "withdrawal": 10000.00, "deposit": 0.0, "balance": 124141.94, "channel": "Transfer", "branch": "615"},
    {"date": "2026-06-23", "time": "02:21", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 153.00, "balance": 124294.94, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-23", "time": "09:58", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 200.00, "balance": 124494.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-23", "time": "18:24", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 7460.00, "deposit": 0.0, "balance": 117034.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-24", "time": "02:17", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 524.40, "balance": 117559.34, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-24", "time": "11:11", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 786.60, "balance": 118345.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-24", "time": "12:05", "type": "เงินโอนเข้า (NBSDT)", "desc": "TR fr 6290345389", "withdrawal": 0.0, "deposit": 10000.00, "balance": 128345.94, "channel": "Transfer_In", "branch": "629"},
    {"date": "2026-06-24", "time": "21:25", "type": "โอนเงินออก-พร้อมเพย์ (MORWSW)", "desc": "TR TO EWalletID 004999164653999", "withdrawal": 2380.00, "deposit": 0.0, "balance": 125965.94, "channel": "Transfer", "branch": "615"},
    {"date": "2026-06-24", "time": "22:13", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-2088203596", "withdrawal": 0.0, "deposit": 130.00, "balance": 126095.94, "channel": "Transfer_In", "branch": "615"},

    # Page 6
    {"date": "2026-06-25", "time": "02:18", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 518.20, "balance": 126614.14, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-25", "time": "12:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 719.80, "balance": 127333.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-25", "time": "19:11", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1892.00, "deposit": 0.0, "balance": 125441.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-26", "time": "02:38", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 435.80, "balance": 125877.74, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-26", "time": "12:15", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 600.20, "balance": 126477.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-27", "time": "02:02", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-1781580747- Future Amount: 385 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 385.00, "balance": 126862.94, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-06-27", "time": "07:38", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 13600.00, "deposit": 0.0, "balance": 113262.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-27", "time": "15:36", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 2491.00, "deposit": 0.0, "balance": 110771.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-27", "time": "18:37", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 500.00, "deposit": 0.0, "balance": 110271.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-28", "time": "02:24", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 236.20, "balance": 110508.14, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-28", "time": "08:31", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 143.80, "balance": 110651.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-28", "time": "15:25", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 5500.00, "deposit": 0.0, "balance": 105151.94, "channel": "Transfer", "branch": "615"},
    {"date": "2026-06-28", "time": "18:44", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 6230.00, "deposit": 0.0, "balance": 98921.94, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-29", "time": "02:09", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 313.60, "balance": 99235.54, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-29", "time": "08:15", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 4165.00, "deposit": 0.0, "balance": 95070.54, "channel": "Biller", "branch": "615"},
    {"date": "2026-06-29", "time": "10:33", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 241.40, "balance": 95311.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-30", "time": "01:51", "type": "ดอกเบี้ยเงินฝาก (IPS)", "desc": "", "withdrawal": 0.0, "deposit": 152.49, "balance": 69814.43, "channel": "Interest", "branch": "0"},
    {"date": "2026-06-30", "time": "02:27", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 180.00, "balance": 95491.94, "channel": "Paotang", "branch": "615"},
    {"date": "2026-06-30", "time": "12:13", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6140134137", "withdrawal": 9000.00, "deposit": 0.0, "balance": 86491.94, "channel": "Transfer", "branch": "615"},
    {"date": "2026-06-30", "time": "13:40", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 270.00, "balance": 86761.94, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-06-30", "time": "22:24", "type": "โอนเงินออก (SW)", "desc": "Trt 100125753136", "withdrawal": 17100.00, "deposit": 0.0, "balance": 69661.94, "channel": "Transfer", "branch": "0"}
]

# รายการธุรกรรมเดือนกรกฎาคม 2569 ทั้ง 143 รายการ (ฝาก 98, ถอน 45)
JULY_TRANSACTIONS = [
    # Page 1
    {"date": "2026-07-01", "time": "04:44", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 274.40, "balance": 70088.83, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-01", "time": "10:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 411.60, "balance": 70500.43, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-01", "time": "12:16", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "1020-0891462504", "withdrawal": 694.43, "deposit": 0.0, "balance": 69806.00, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-07-01", "time": "13:09", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "1020-0891462504", "withdrawal": 874.19, "deposit": 0.0, "balance": 68931.81, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-07-01", "time": "16:58", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "1020-0891462504", "withdrawal": 426.93, "deposit": 0.0, "balance": 68504.88, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-07-01", "time": "17:35", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 69504.88, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-02", "time": "02:56", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1480.00, "balance": 70984.88, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-02", "time": "11:45", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2220.00, "balance": 73204.88, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-02", "time": "17:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 73450.00, "balance": 146654.88, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-03", "time": "02:46", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 917.60, "balance": 147572.48, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-03", "time": "12:24", "type": "หักบัญชีอัตโนมัติ (CGSWP)", "desc": "20933-0891462504", "withdrawal": 11855.01, "deposit": 0.0, "balance": 135717.47, "channel": "CGSWP", "branch": "615"},
    {"date": "2026-07-03", "time": "13:36", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1376.40, "balance": 137093.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-03", "time": "17:10", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 30826.00, "balance": 167919.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-04", "time": "01:52", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-2211685762- Future Amount: 299 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 299.00, "balance": 168218.87, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-04", "time": "01:54", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-2211685762- Future Amount: 105 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 105.00, "balance": 168323.87, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-04", "time": "01:55", "type": "เงินโอนเข้า (IORSDT)", "desc": "014-6034097716- Future Amount: 120 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 120.00, "balance": 168443.87, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-04", "time": "02:40", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1244.00, "balance": 169687.87, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-04", "time": "08:37", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 9859.00, "deposit": 0.0, "balance": 159828.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-04", "time": "08:46", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1732.00, "balance": 161560.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-04", "time": "12:09", "type": "จ่ายค่าสินค้า/บริการ (NMPSWP)", "desc": "010753700088205-1406755315900001832", "withdrawal": 3310.00, "deposit": 0.0, "balance": 158250.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-04", "time": "13:56", "type": "โอนเงินออก (IORSWT)", "desc": "014-4087793848", "withdrawal": 800.00, "deposit": 0.0, "balance": 157450.87, "channel": "Transfer", "branch": "615"},

    # Page 2
    {"date": "2026-07-04", "time": "15:15", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 500.00, "deposit": 0.0, "balance": 156950.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-04", "time": "15:31", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 10000.00, "deposit": 0.0, "balance": 146950.87, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-05", "time": "02:30", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1591.20, "balance": 148542.07, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-05", "time": "04:08", "type": "เงินโอนเข้า (IORSDT)", "desc": "014-4260193786", "withdrawal": 0.0, "deposit": 250.00, "balance": 148792.07, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-05", "time": "08:29", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 12101.00, "deposit": 0.0, "balance": 136691.07, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-05", "time": "09:11", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 2386.80, "balance": 139077.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-05", "time": "19:00", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 3770.50, "deposit": 0.0, "balance": 135307.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-05", "time": "19:01", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1969.00, "deposit": 0.0, "balance": 133338.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-05", "time": "19:02", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1684.00, "deposit": 0.0, "balance": 131654.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-06", "time": "02:43", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1264.40, "balance": 132918.77, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-06", "time": "11:38", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1896.60, "balance": 134815.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-06", "time": "17:09", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 12000.00, "balance": 146815.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-06", "time": "17:17", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 19000.00, "balance": 165815.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-06", "time": "17:20", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 2000.00, "balance": 167815.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-06", "time": "19:31", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 11662.00, "deposit": 0.0, "balance": 156153.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-06", "time": "19:32", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1304.00, "deposit": 0.0, "balance": 154849.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-07", "time": "02:50", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1097.60, "balance": 155946.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-07", "time": "13:18", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1646.40, "balance": 157593.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-07", "time": "19:10", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 7000.00, "balance": 164593.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-08", "time": "02:48", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 756.00, "balance": 165349.37, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-08", "time": "12:58", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1134.00, "balance": 166483.37, "channel": "Welfare", "branch": "108682"},

    # Page 3
    {"date": "2026-07-08", "time": "17:03", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 5000.00, "balance": 171483.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-09", "time": "02:28", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1121.00, "balance": 172604.37, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-09", "time": "13:35", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1550.00, "balance": 174154.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-09", "time": "17:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 2000.00, "balance": 176154.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-10", "time": "02:38", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1065.20, "balance": 177219.57, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-10", "time": "08:45", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 12365.00, "deposit": 0.0, "balance": 164854.57, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-10", "time": "12:26", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1597.80, "balance": 166452.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-10", "time": "17:01", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1695.00, "balance": 168147.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-10", "time": "17:19", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 7978.00, "deposit": 0.0, "balance": 160169.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-10", "time": "17:19", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 3390.00, "deposit": 0.0, "balance": 156779.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-11", "time": "02:45", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 681.20, "balance": 157460.57, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-11", "time": "09:41", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 962.80, "balance": 158423.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-11", "time": "15:04", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "025-BILLERID", "withdrawal": 2219.00, "deposit": 0.0, "balance": 156204.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-11", "time": "16:16", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 9751.00, "deposit": 0.0, "balance": 146453.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-11", "time": "19:22", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 500.00, "deposit": 0.0, "balance": 145953.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-12", "time": "02:33", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1002.60, "balance": 146955.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-12", "time": "09:33", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1413.40, "balance": 148369.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-13", "time": "01:47", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-1941287596- Future Amount: 156 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 156.00, "balance": 148525.37, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-13", "time": "02:15", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 767.20, "balance": 149292.57, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-13", "time": "11:05", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1058.80, "balance": 150351.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-13", "time": "17:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 4000.00, "balance": 154351.37, "channel": "Welfare", "branch": "108682"},

    # Page 4
    {"date": "2026-07-13", "time": "17:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 3000.00, "balance": 157351.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-13", "time": "17:10", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 158351.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-13", "time": "19:53", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 3577.00, "deposit": 0.0, "balance": 154774.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-14", "time": "02:15", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 623.60, "balance": 155397.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-14", "time": "09:41", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 11899.00, "deposit": 0.0, "balance": 143498.97, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-14", "time": "11:56", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 935.40, "balance": 144434.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-14", "time": "12:20", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 5000.00, "deposit": 0.0, "balance": 139434.37, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-14", "time": "17:34", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 140434.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-14", "time": "19:10", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 4072.00, "deposit": 0.0, "balance": 136362.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-14", "time": "19:11", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1200.00, "deposit": 0.0, "balance": 135162.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-15", "time": "02:12", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 607.60, "balance": 135769.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-15", "time": "13:59", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 911.40, "balance": 136681.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-15", "time": "18:58", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 5000.00, "deposit": 0.0, "balance": 131681.37, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-15", "time": "19:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 132681.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-16", "time": "02:19", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 535.80, "balance": 133217.17, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-16", "time": "12:00", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 719.20, "balance": 133936.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-16", "time": "17:09", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 10000.00, "deposit": 0.0, "balance": 123936.37, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-17", "time": "02:19", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 532.00, "balance": 124468.37, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-17", "time": "11:09", "type": "ฝากเงิน (SDCH)", "desc": "", "withdrawal": 0.0, "deposit": 20000.00, "balance": 144468.37, "channel": "Cash_Deposit", "branch": "641"},
    {"date": "2026-07-17", "time": "12:10", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 798.00, "balance": 145266.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-17", "time": "17:05", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 200.00, "balance": 145466.37, "channel": "Welfare", "branch": "108682"},

    # Page 5
    {"date": "2026-07-18", "time": "02:29", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 685.60, "balance": 146151.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-18", "time": "09:28", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 3133.00, "deposit": 0.0, "balance": 143018.97, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-18", "time": "09:28", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 1775.00, "deposit": 0.0, "balance": 141243.97, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-18", "time": "09:29", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 979.40, "balance": 142223.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-18", "time": "15:15", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1100.00, "deposit": 0.0, "balance": 141123.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-18", "time": "18:27", "type": "ฝากเงินผ่าน ADM (ATSDC)", "desc": "K31368-6153107532", "withdrawal": 0.0, "deposit": 29500.00, "balance": 170623.37, "channel": "Cash_ADM", "branch": "863"},
    {"date": "2026-07-19", "time": "01:46", "type": "เงินโอนเข้า (NBSDT)", "desc": "TR fr 6410579489- Future Amount: 392 - Tran: NBSDT", "withdrawal": 0.0, "deposit": 392.00, "balance": 171015.37, "channel": "Transfer_In", "branch": "641"},
    {"date": "2026-07-19", "time": "02:21", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 1504.20, "balance": 172519.57, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-19", "time": "08:57", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1691.80, "balance": 174211.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-20", "time": "02:17", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 421.80, "balance": 174633.17, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-20", "time": "10:18", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 276.20, "balance": 174909.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-20", "time": "20:04", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 15000.00, "deposit": 0.0, "balance": 159909.37, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-21", "time": "01:49", "type": "เงินโอนเข้า (IORSDT)", "desc": "030-020430768398- Future Amount: 150 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 150.00, "balance": 160059.37, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-21", "time": "02:17", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 376.40, "balance": 160435.77, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-21", "time": "09:51", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 564.60, "balance": 161000.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-21", "time": "10:59", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6410298447", "withdrawal": 3500.00, "deposit": 0.0, "balance": 157500.37, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-21", "time": "11:29", "type": "ฝากเงิน (SDCH)", "desc": "", "withdrawal": 0.0, "deposit": 18500.00, "balance": 176000.37, "channel": "Cash_Deposit", "branch": "641"},
    {"date": "2026-07-21", "time": "17:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 233.00, "balance": 176233.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-22", "time": "02:13", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 460.60, "balance": 176693.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-22", "time": "11:36", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 562.40, "balance": 177256.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-22", "time": "18:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 178256.37, "channel": "Welfare", "branch": "108682"},

    # Page 6
    {"date": "2026-07-23", "time": "01:41", "type": "เงินโอนเข้า (IORSDT)", "desc": "004-0571254085- Future Amount: 30 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 30.00, "balance": 178286.37, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-23", "time": "02:26", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 288.20, "balance": 178574.57, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-23", "time": "12:50", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 398.80, "balance": 178973.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-23", "time": "17:06", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 179973.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-24", "time": "02:32", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 355.60, "balance": 180328.97, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-24", "time": "10:47", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 13991.00, "deposit": 0.0, "balance": 166337.97, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-24", "time": "13:41", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 510.40, "balance": 166848.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-24", "time": "17:08", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 167848.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-25", "time": "02:22", "type": "เงินโอนเข้า (IORSDT)", "desc": "030-020258546744- Future Amount: 130 - Tran: IORSDT", "withdrawal": 0.0, "deposit": 130.00, "balance": 167978.37, "channel": "Transfer_In", "branch": "615"},
    {"date": "2026-07-25", "time": "02:58", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 582.80, "balance": 168561.17, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-25", "time": "09:25", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 874.20, "balance": 169435.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-25", "time": "15:34", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "011-BILLERID", "withdrawal": 9295.00, "deposit": 0.0, "balance": 160140.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-25", "time": "18:08", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 13559.00, "deposit": 0.0, "balance": 146581.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-25", "time": "18:24", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 500.00, "deposit": 0.0, "balance": 146081.37, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-25", "time": "20:06", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6150680118", "withdrawal": 300.00, "deposit": 0.0, "balance": 145781.37, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-26", "time": "02:30", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 912.80, "balance": 146694.17, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-26", "time": "08:54", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 978.20, "balance": 147672.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-26", "time": "09:13", "type": "เงินโอนเข้า (NBSDT)", "desc": "TR fr 6141468802", "withdrawal": 0.0, "deposit": 60.00, "balance": 147732.37, "channel": "Transfer_In", "branch": "614"},
    {"date": "2026-07-27", "time": "02:11", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 369.20, "balance": 148101.57, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-27", "time": "10:12", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 335.80, "balance": 148437.37, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-27", "time": "11:41", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "002-BILLERID", "withdrawal": 4040.00, "deposit": 0.0, "balance": 144397.37, "channel": "Biller", "branch": "615"},

    # Page 7
    {"date": "2026-07-27", "time": "17:06", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 14440.50, "deposit": 0.0, "balance": 129956.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-27", "time": "17:06", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 6390.00, "deposit": 0.0, "balance": 123566.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-27", "time": "17:34", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 124566.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-28", "time": "02:30", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 556.40, "balance": 125123.27, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-28", "time": "09:31", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 704.60, "balance": 125827.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-29", "time": "02:00", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID- Future Amount: 1500 - Tran: MORPSW", "withdrawal": 1500.00, "deposit": 0.0, "balance": 124327.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-29", "time": "02:17", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 112.40, "balance": 124440.27, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-29", "time": "09:52", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 168.60, "balance": 124608.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-30", "time": "02:09", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 446.40, "balance": 125055.27, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-30", "time": "09:34", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 575.60, "balance": 125630.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-31", "time": "02:24", "type": "เงินโอนเข้า (SD)", "desc": "Paotang Credit", "withdrawal": 0.0, "deposit": 676.00, "balance": 126306.87, "channel": "Paotang", "branch": "615"},
    {"date": "2026-07-31", "time": "12:11", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "60/40/กรมบัญชีกลาง/200068", "withdrawal": 0.0, "deposit": 1004.00, "balance": 127310.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-31", "time": "12:21", "type": "โอนเงินออก (NBSWT)", "desc": "TR to 6140134137", "withdrawal": 9000.00, "deposit": 0.0, "balance": 118310.87, "channel": "Transfer", "branch": "615"},
    {"date": "2026-07-31", "time": "15:32", "type": "จ่ายค่าสินค้า/บริการ (MORPSW)", "desc": "004-BILLERID", "withdrawal": 1128.00, "deposit": 0.0, "balance": 117182.87, "channel": "Biller", "branch": "615"},
    {"date": "2026-07-31", "time": "17:07", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 2000.00, "balance": 119182.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-31", "time": "17:08", "type": "ค่าสินค้า/สวัสดิการ/อื่นๆ (BSD14)", "desc": "CR.to Welfare/กรมบัญชีกลาง/108778", "withdrawal": 0.0, "deposit": 1000.00, "balance": 120182.87, "channel": "Welfare", "branch": "108682"},
    {"date": "2026-07-31", "time": "22:09", "type": "โอนเงินออก (SW)", "desc": "Trt 100125753136", "withdrawal": 17100.00, "deposit": 0.0, "balance": 103082.87, "channel": "Transfer", "branch": "0"}
]

RAW_TRANSACTIONS = JUNE_TRANSACTIONS + JULY_TRANSACTIONS

def verify_checksum() -> Dict[str, Any]:
    # 1. June Checksum
    june_dep = round(sum(tx["deposit"] for tx in JUNE_TRANSACTIONS), 2)
    june_wdr = round(sum(tx["withdrawal"] for tx in JUNE_TRANSACTIONS), 2)
    june_cdep = sum(1 for tx in JUNE_TRANSACTIONS if tx["deposit"] > 0)
    june_cwdr = sum(1 for tx in JUNE_TRANSACTIONS if tx["withdrawal"] > 0)
    june_passed = (june_dep == 209085.49 and june_wdr == 263758.73 and june_cdep == 79 and june_cwdr == 47)
    
    # 2. July Checksum
    july_dep = round(sum(tx["deposit"] for tx in JULY_TRANSACTIONS), 2)
    july_wdr = round(sum(tx["withdrawal"] for tx in JULY_TRANSACTIONS), 2)
    july_cdep = sum(1 for tx in JULY_TRANSACTIONS if tx["deposit"] > 0)
    july_cwdr = sum(1 for tx in JULY_TRANSACTIONS if tx["withdrawal"] > 0)
    july_passed = (july_dep == 296781.00 and july_wdr == 263512.56 and july_cdep == 98 and july_cwdr == 45)
    
    # 3. Overall Checksum
    tot_dep = round(sum(tx["deposit"] for tx in RAW_TRANSACTIONS), 2)
    tot_wdr = round(sum(tx["withdrawal"] for tx in RAW_TRANSACTIONS), 2)
    
    return {
        "june_passed": june_passed,
        "june_dep": june_dep,
        "june_wdr": june_wdr,
        "july_passed": july_passed,
        "july_dep": july_dep,
        "july_wdr": july_wdr,
        "tot_dep": tot_dep,
        "tot_wdr": tot_wdr,
        "all_passed": june_passed and july_passed,
        "total_records": len(RAW_TRANSACTIONS)
    }

STATEMENT_6_MONTHS_SUMMARY = {
    "account_name": "ร้านศรีบุตรา โดย นายณัฐวุฒิ ศรีบุตรา",
    "account_no": "6153107532",
    "bank": "ธนาคารกรุงไทย สาขาหล่มสัก (615)",
    "period_start": "2026-01-01",
    "period_end": "2026-06-30",
    "days": 181,
    "months": 6,
    "total_deposits": 1369253.49,
    "total_withdrawals": 1446741.47,
    "monthly_average_sales": 228208.92,
    "net_cash_flow": -77487.98,
    "opening_balance": 147302.41,
    "closing_balance": 69661.94,
    "pnd94_gross_sales": 1369253.49,
    "pnd94_flat_tax": 30155.21,
    "pnd94_actual_tax": 6846.27,
    "pnd94_savings": 23308.94
}

STATEMENT_8_MONTHS_SUMMARY = {
    "account_name": "ร้านศรีบุตรา โดย นายณัฐวุฒิ ศรีบุตรา",
    "account_no": "6153107532",
    "bank": "ธนาคารกรุงไทย สาขาหล่มสัก (615)",
    "period_start": "2026-01-01",
    "period_end": "2026-08-31",
    "days": 243,
    "months": 8,
    "pages": 36,
    "total_deposits": 2038286.49,
    "total_withdrawals": 2117292.19,
    "deposit_count": 426,
    "withdrawal_count": 318,
    "total_transactions": 744,
    "opening_balance": 147302.41,
    "closing_balance": 68296.71,
    "monthly_average_sales": 254785.81,
    "annual_projected": 3057429.74,
    "vat_limit": 1800000.0,
    "vat_breached": True,
    "vat_breach_date": "2026-08-03",
    "vat_over_amount": 238286.49,
    "monthly_breakdown": [
        {"month": "2569-01 (ม.ค.)", "net_balance": 106352.91, "verified_deposits": 219048.00, "verified_withdrawals": 259997.50},
        {"month": "2569-02 (ก.พ.)", "net_balance": 129826.19, "verified_deposits": 208762.00, "verified_withdrawals": 185288.72},
        {"month": "2569-03 (มี.ค.)", "net_balance": 136105.61, "verified_deposits": 221984.00, "verified_withdrawals": 215704.58},
        {"month": "2569-04 (เม.ย.)", "net_balance": 114131.32, "verified_deposits": 256821.00, "verified_withdrawals": 278795.29},
        {"month": "2569-05 (พ.ค.)", "net_balance": 124487.67, "verified_deposits": 253553.00, "verified_withdrawals": 243196.65},
        {"month": "2569-06 (มิ.ย.)", "net_balance": 69661.94, "verified_deposits": 209085.49, "verified_withdrawals": 263758.73},
        {"month": "2569-07 (ก.ค.)", "net_balance": 103082.87, "verified_deposits": 296781.00, "verified_withdrawals": 263512.56},
        {"month": "2569-08 (ส.ค.)", "net_balance": 68296.71, "verified_deposits": 372251.00, "verified_withdrawals": 407038.16},
    ]
}

if __name__ == "__main__":
    res = verify_checksum()
    print("Verification Result:", res)
    print("8-Month Summary Total Deposits:", STATEMENT_8_MONTHS_SUMMARY["total_deposits"])
    print("8-Month Over VAT Limit by:", STATEMENT_8_MONTHS_SUMMARY["vat_over_amount"])

