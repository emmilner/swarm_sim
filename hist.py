import numpy as np
import matplotlib.pyplot as plt
graphs = 1
#deliver = [3, 4, 8, 35, 39, 70, 109, 115,121,142,185,262,302,325,354,371,435,438,451,494,657,700,707,842,887,914,1005,1111,1272,1344,1374,1387,1507,1640,1709,1876,1910,1981,2173,2376,2816,3060,3182,3213,3542,3775,3804,4605,5932,8179,6,360,632,1210,4247,26,184,342,482,963,715,961,1226,2508,4340,42,156,1282,4024,4956,270,849,1998,2299,2390,235,457,1182,1628,1885,44,237,864,1083,1128,13,293,815,1167,1871,480,1181,3059,3268,5319,205,233,238,1805,3497]
#collect = [10,13,191,219,794,1,263,709,1863,2628,105,258,1002,1335,2927,122,408,437,1168,4403,8,113,320,478,3226,1,50,439,1756,3537,1,93,156,1942,10652,388,495,1214,1664,1933,51,66,224,732,2448,2,30,84,455,526,161,197,301,2363,2382,1,51,155,1083,1408,1,1197,1542,2861,4465,109,536,736,962,1643,29,45,185,2344,3033,141,153,171,451,748,14,26,145,876,4032,1,87,437,1856,3673,37,284,310,455,1279,1,1,556,1355,2777]
deliver = [5685,5913,2461,5603,941,1596,6801,7330,1215,10483,2187,3476,169,1438,482,1108,2196,3742,3527,5627,360,6237,378,3895,5379,7848,3006,3314,4138,6768,6174,8142,3678,10189,2520,10942,1046,1767,484,3042,4363,4712,345,9888,1907,3225,3424,3786,70,4234]
collect = [512,851,578,2339,1799,8702,1602,12519,749,5218,2,58,48,921,1997,2435,2086,5918,103,2193,120,2504,46,1942,210,2499,65,4896,1,3394,111,2405,67,3591,452,2830,61,2968,2291,5577,6,3292,264,304,44,8742,1845,3547,1420,1504]

if graphs == 2:
	fig, ax = plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True)
	plt.grid(True)
	ax[1].hist(deliver)
	ax[0].hist(collect)
	ax[0].set_xlabel('Time taken (s)')
	ax[1].set_xlabel('Time taken (s)')
	ax[0].set_ylabel('Number of occurrences')
	ax[1].set_ylabel('Number of occurrences')
	ax[1].set_title('Time to deliver box')
	ax[0].set_title('Time to find box')
	ax[0].grid(True)
	ax[1].grid(True)
if graphs == 1:
	plt.hist(deliver)
	plt.xlabel('Time taken (s)')
	plt.ylabel('Number of occurrences')
	plt.title('Time to deliver one box')
	plt.grid(True)

plt.show()