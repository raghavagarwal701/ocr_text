calling the function def tap_ocr(action_object, image_before_action) and passing the object which is the name of the element. this will be given by the comman classifier function and image before is where we pass the screenbefore action this can be image path or numpy array or image file as bytes

this function will return three things does_match, bbox, end-start first is a boolean value which tells if the object is found or not, second is the bounding box of the object and third is the time taken to find the object


[2024-12-18 17:36:47,512: WARNING/MainProcess] [([[np.int32(45), np.int32(43)], [np.int32(127), np.int32(43)], [np.int32(127), np.int32(87)], [np.int32(45), np.int32(87)]], '5.36', np.float64(0.8356213050259841)), ([[np.int32(148), np.int32(158)], [np.int32(626), np.int32(158)], [np.int32(626), np.int32(232)], [np.int32(148), np.int32(232)]], 'Delivery in 9 Mins', np.float64(0.8966908785227115)), ([[np.int32(151), np.int32(233)], [np.int32(259), np.int32(233)], [np.int32(259), np.int32(271)], [np.int32(151), np.int32(271)]], 'Home', np.float64(0.9999703168869019)), ([[np.int32(282), np.int32(228)], [np.int32(856), np.int32(228)], [np.int32(856), np.int32(278)], [np.int32(282), np.int32(278)]], 'Prestige Shantiniketan Residenti__.', np.float64(0.8791056705504188)), ([[np.int32(186), np.int32(337)], [np.int32(546), np.int32(337)], [np.int32(546), np.int32(388)], [np.int32(186), np.int32(388)]], 'Search for "iphone"', np.float64(0.8652733759421771)), ([[np.int32(204), np.int32(538)], [np.int32(502), np.int32(538)], [np.int32(502), np.int32(570)], [np.int32(204), np.int32(570)]], 'EXCLUSIVE OFFER', np.float64(0.9970682789781031)), ([[np.int32(510), np.int32(540)], [np.int32(878), np.int32(540)], [np.int32(878), np.int32(570)], [np.int32(510), np.int32(570)]], 'ON YOUR NEXT ORDER', np.float64(0.9062054527195628)), ([[np.int32(196), np.int32(584)], [np.int32(884), np.int32(584)], [np.int32(884), np.int32(708)], [np.int32(196), np.int32(708)]], 'FRESH ONIONS', np.float64(0.6705287616484146)), ([[np.int32(706), np.int32(782)], [np.int32(784), np.int32(782)], [np.int32(784), np.int32(858)], [np.int32(706), np.int32(858)]], '2]', np.float64(0.11370442280589012)), ([[np.int32(151), np.int32(1080)], [np.int32(933), np.int32(1080)], [np.int32(933), np.int32(1125)], [np.int32(151), np.int32(1125)]], 'Your exclusive offer will be auto-applied to your cart', np.float64(0.7766044498743756)), ([[np.int32(192), np.int32(1183)], [np.int32(897), np.int32(1183)], [np.int32(897), np.int32(1296)], [np.int32(192), np.int32(1296)]], '[OWESTPRICES', np.float64(0.6580830066468135)), ([[np.int32(350), np.int32(1370)], [np.int32(727), np.int32(1370)], [np.int32(727), np.int32(1430)], [np.int32(350), np.int32(1430)]], '<100 Free cash', np.float64(0.7359746047656198)), ([[np.int32(147), np.int32(1535)], [np.int32(911), np.int32(1535)], [np.int32(911), np.int32(1604)], [np.int32(147), np.int32(1604)]], 'Trending in Prestige Shantiniketa:', np.float64(0.7285425448891659)), ([[np.int32(152), np.int32(1702)], [np.int32(254), np.int32(1702)], [np.int32(254), np.int32(1750)], [np.int32(152), np.int32(1750)]], 'R60', np.float64(0.6377182366139552)), ([[np.int32(492), np.int32(1702)], [np.int32(588), np.int32(1702)], [np.int32(588), np.int32(1750)], [np.int32(492), np.int32(1750)]], 'R23', np.float64(0.34720708374315473)), ([[np.int32(832), np.int32(1702)], [np.int32(920), np.int32(1702)], [np.int32(920), np.int32(1750)], [np.int32(832), np.int32(1750)]], 'R15', np.float64(0.3533754050731659)), ([[np.int32(127), np.int32(1779)], [np.int32(287), np.int32(1779)], [np.int32(287), np.int32(1815)], [np.int32(127), np.int32(1815)]], 'MRP =1e3', np.float64(0.31330055260578055)), ([[np.int32(473), np.int32(1779)], [np.int32(613), np.int32(1779)], [np.int32(613), np.int32(1815)], [np.int32(473), np.int32(1815)]], 'MRP R27', np.float64(0.6675114229326229)), ([[np.int32(806), np.int32(1778)], [np.int32(953), np.int32(1778)], [np.int32(953), np.int32(1815)], [np.int32(806), np.int32(1815)]], 'MRP 236', np.float64(0.5196981238261064)), ([[np.int32(525), np.int32(1955)], [np.int32(555), np.int32(1955)], [np.int32(555), np.int32(1967)], [np.int32(525), np.int32(1967)]], 'Doba', np.float64(0.12857401371002197)), ([[np.int32(120), np.int32(2012)], [np.int32(602), np.int32(2012)], [np.int32(602), np.int32(2062)], [np.int32(120), np.int32(2062)]], 'Get FREE delivery above ?99', np.float64(0.801414918438009)), ([[np.int32(84), np.int32(2198)], [np.int32(108), np.int32(2198)], [np.int32(108), np.int32(2226)], [np.int32(84), np.int32(2226)]], '2', np.float64(0.43776037568139614)), ([[np.int32(273), np.int32(2165)], [np.int32(363), np.int32(2165)], [np.int32(363), np.int32(2251)], [np.int32(273), np.int32(2251)]], '88', np.float64(0.8589267116136547)), ([[np.int32(525), np.int32(2199)], [np.int32(561), np.int32(2199)], [np.int32(561), np.int32(2235)], [np.int32(525), np.int32(2235)]], '@', np.float64(0.2017329882685468)), ([[np.int32(787), np.int32(2175)], [np.int32(885), np.int32(2175)], [np.int32(885), np.int32(2241)], [np.int32(787), np.int32(2241)]], "'", np.float64(0.50515147470378)), ([[np.int32(936), np.int32(2168)], [np.int32(1020), np.int32(2168)], [np.int32(1020), np.int32(2248)], [np.int32(936), np.int32(2248)]], '2', np.float64(0.9735687707749463)), ([[np.int32(474), np.int32(2238)], [np.int32(612), np.int32(2238)], [np.int32(612), np.int32(2264)], [np.int32(474), np.int32(2264)]], 'PORTRONICS', np.float64(0.9958613240198173)), ([[np.int32(47), np.int32(2259)], [np.int32(151), np.int32(2259)], [np.int32(151), np.int32(2295)], [np.int32(47), np.int32(2295)]], 'Saver', np.float64(0.9999867786099642)), ([[np.int32(223), np.int32(2253)], [np.int32(416), np.int32(2253)], [np.int32(416), np.int32(2303)], [np.int32(223), np.int32(2303)]], 'Categories', np.float64(0.9999680701013951)), ([[np.int32(721), np.int32(2257)], [np.int32(807), np.int32(2257)], [np.int32(807), np.int32(2295)], [np.int32(721), np.int32(2295)]], 'Cafe', np.float64(0.9999918937683105)), ([[np.int32(945), np.int32(2259)], [np.int32(1025), np.int32(2259)], [np.int32(1025), np.int32(2295)], [np.int32(945), np.int32(2295)]], 'Cart', np.float64(0.9999905824661255)), ([[np.float64(706.9820268028815), np.float64(850.1317018509494)], [np.float64(779.7729413566557), np.float64(858.6714995223043)], [np.float64(773.0179731971185), np.float64(895.8682981490506)], [np.float64(701.2270586433443), np.float64(886.3285004776957)]], '255', np.float64(0.6503481144700848))]
