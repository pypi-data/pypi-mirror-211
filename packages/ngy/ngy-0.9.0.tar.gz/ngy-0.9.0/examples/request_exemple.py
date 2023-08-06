#!/usr/bin/env python
# coding: utf-8

import NGY

my_request = NGY.Request(( 43.553859, 1.364688, 43.394638, 1.580797),
                         zoom_list=range(6,16),
                         layer="GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN25TOUR.CV",
                         style="normal",
                         projection="PM",
                         format="jpeg")

my_request.fetch_data()
my_request.save('Lacroix-Falgarde.mbtiles', 'Lacroix-Falgarde - 02/06/2023')

